"""A consistent screenshot record must not imply that its visual quality was inspected."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ui_verify


def blank_png(path: Path, width: int) -> None:
    """A real, blank PNG is enough to pass artifact checks; its design is not assessed."""
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    header = struct.pack(">IIBBBBB", width, 1, 8, 2, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                     + chunk(b"IDAT", zlib.compress(b"\x00" + b"\xff\xff\xff" * width))
                     + chunk(b"IEND", b""))


class VisualReviewEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for width in (390, 1440):
            blank_png(self.root / f"after-{width}.png", width)
        self.verdict = {"route": "/x", "widths": [390, 1440], "status": "pass", "consoleErrors": 0,
                        "failedRequests": 0, "interaction": "pass", "notVerified": []}

    def review(self, widths=(390, 1440), status="pass"):
        self.verdict["visualReview"] = {"status": status, "views": [
            {"width": width, "status": status,
             "observation": f"At {width}px the search label remains visible above its control."}
            for width in widths]}
        return self.verdict["visualReview"]

    def save(self):
        (self.root / "verdict.json").write_text(json.dumps(self.verdict), encoding="utf-8")

    def verify(self, *args, **kwargs):
        self.save()
        return ui_verify.verify(self.root, *args, **kwargs)

    def cli(self, *args):
        self.save()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = ui_verify.main([str(self.root), *args])
        return code, output.getvalue()

    def test_legacy_api_and_verdict_keep_pass_but_do_not_establish_visual_quality(self):
        result = self.verify(None, False)
        self.assertEqual("pass", result["status"])
        self.assertEqual("not-recorded", result["visualReviewStatus"])
        self.assertIn("Artifact and record consistency only", result["verificationScope"])
        self.assertIn("Does not inspect screenshot appearance", result["verificationScope"])
        self.assertIn("observer truth", result["verificationScope"])
        self.assertIn("do not establish visual quality", " ".join(result["notes"]))
        code, text = self.cli()
        self.assertEqual(0, code)
        self.assertIn("[PASS] artifact/record consistency", text)
        self.assertIn("recorded visual review: not-recorded", text)

    def test_strict_review_is_opt_in_and_missing_review_fails(self):
        result = self.verify(require_visual_review=True)
        self.assertEqual("fail", result["status"])
        self.assertEqual("not-recorded", result["visualReviewStatus"])
        self.assertIn("requires a visualReview record", " ".join(result["issues"]))
        code, text = self.cli("--require-visual-review", "--json")
        self.assertEqual(1, code)
        self.assertEqual("not-recorded", json.loads(text)["visualReviewStatus"])

    def test_partial_review_cannot_claim_full_visual_coverage(self):
        self.review((390,))
        result = self.verify()
        self.assertEqual("pass", result["status"], "optional partial review does not break legacy artifact policy")
        self.assertEqual("not-verified", result["visualReviewStatus"])
        self.assertIn("1440", " ".join(result["notes"]))
        strict = self.verify(require_visual_review=True)
        self.assertEqual("fail", strict["status"])
        self.assertIn("every requested width", " ".join(strict["issues"]))
        self.assertEqual("pass", self.verify((390,), False, True)["status"])

    def test_requested_width_override_requires_review_at_that_width(self):
        blank_png(self.root / "after-768.png", 768)
        self.verdict["widths"].append(768)
        self.review()
        result = self.verify((390, 768), require_visual_review=True)
        self.assertEqual("fail", result["status"])
        self.assertEqual("not-verified", result["visualReviewStatus"])
        self.assertIn("768", " ".join(result["notes"]))

    def test_review_width_must_be_claimed_and_have_an_after_screenshot(self):
        self.review((390, 768, 1440))
        result = self.verify()
        self.assertEqual("fail", result["status"])
        self.assertEqual("invalid", result["visualReviewStatus"])
        self.assertIn("not claimed", " ".join(result["issues"]))
        blank_png(self.root / "after-768.png", 768)
        self.assertEqual("fail", self.verify()["status"], "a screenshot alone is not a claimed review width")
        self.verdict["widths"].append(768)
        (self.root / "after-768.png").unlink()
        self.assertIn("has no after-768.png", " ".join(self.verify()["issues"]))

    def test_review_and_view_statuses_must_be_known(self):
        for value in (None, True, "complete", "PASS", [], {}):
            for target in ("review", "view"):
                with self.subTest(value=value, target=target):
                    review = self.review()
                    (review if target == "review" else review["views"][0])["status"] = value
                    result = self.verify()
                    self.assertEqual("fail", result["status"])
                    self.assertEqual("invalid", result["visualReviewStatus"])

    def test_review_widths_are_unique_css_integers(self):
        for value in (True, False, "390", 390.0, 99, 10000, None, [], {}):
            with self.subTest(width=value):
                review = self.review()
                review["views"][0]["width"] = value
                self.assertEqual("invalid", self.verify()["visualReviewStatus"])
        review = self.review()
        review["views"].append(dict(review["views"][0]))
        self.assertIn("duplicate width 390", " ".join(self.verify()["issues"]))

    def test_each_view_requires_a_nonempty_recorded_observation(self):
        for value in (None, "", " \n\t", True, [], {}):
            with self.subTest(observation=value):
                review = self.review()
                review["views"][0]["observation"] = value
                self.assertEqual("invalid", self.verify()["visualReviewStatus"])
        review = self.review()
        review["views"][0].pop("observation")
        self.assertEqual("fail", self.verify()["status"])

    def test_malformed_optional_review_is_not_silently_accepted(self):
        for value in (None, [], "pass", {}, {"status": "pass", "views": {}},
                      {"status": "pass", "views": [None]}):
            with self.subTest(review=value):
                self.verdict["visualReview"] = value
                self.assertEqual("invalid", self.verify()["visualReviewStatus"])

    def test_recorded_visual_failure_contradicts_passing_overall_verdict(self):
        review = self.review(status="fail")
        review["views"][0]["observation"] = "The search control overlaps the navigation at 390px."
        result = self.verify()
        self.assertEqual("fail", result["status"])
        self.assertEqual("fail", result["visualReviewStatus"])
        self.assertIn("verdict says pass but visualReview records a visual failure", " ".join(result["issues"]))

    def test_failed_view_cannot_be_hidden_by_review_summary(self):
        review = self.review()
        review["views"][0]["status"] = "fail"
        result = self.verify()
        self.assertEqual("fail", result["status"])
        self.assertEqual("fail", result["visualReviewStatus"])
        self.assertIn("visualReview says pass but a view", " ".join(result["issues"]))

    def test_unverified_review_stays_unverified_and_fails_strict_mode(self):
        self.review(status="not-verified")
        result = self.verify()
        self.assertEqual("pass", result["status"])
        self.assertEqual("not-verified", result["visualReviewStatus"])
        self.assertEqual("fail", self.verify(require_visual_review=True)["status"])
        review = self.review()
        review["views"][0]["status"] = "not-verified"
        result = self.verify()
        self.assertEqual("fail", result["status"], "a pass summary cannot hide an unverified view")
        self.assertEqual("not-verified", result["visualReviewStatus"])

    def test_empty_review_never_establishes_visual_quality(self):
        self.review(())
        self.assertEqual("not-verified", self.verify()["visualReviewStatus"])
        self.assertEqual("fail", self.verify(require_visual_review=True)["status"])

    def test_good_recorded_review_passes_strictly_without_claiming_observer_truth(self):
        self.review()
        result = self.verify(require_visual_review=True)
        self.assertEqual("pass", result["status"])
        self.assertEqual("pass", result["visualReviewStatus"])
        self.assertIn("does not inspect images or verify the observations", " ".join(result["notes"]))
        self.assertEqual(0, self.cli("--require-visual-review")[0])

    def test_honest_skip_remains_skip_in_strict_mode_and_never_claims_review(self):
        self.verdict.update(status="skipped", reason="Browser unavailable in this environment")
        for with_record in (False, True):
            with self.subTest(with_record=with_record):
                if with_record:
                    self.review()
                result = self.verify(require_visual_review=True)
                self.assertEqual("skipped", result["status"])
                self.assertEqual("skipped", result["visualReviewStatus"])
                self.assertIn("not established", " ".join(result["notes"]))
                self.assertEqual(0, self.cli("--require-visual-review")[0])
        self.verdict.pop("reason")
        self.assertEqual("fail", self.verify(require_visual_review=True)["status"])


if __name__ == "__main__":
    unittest.main()
