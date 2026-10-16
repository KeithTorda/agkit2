#!/usr/bin/env python3
"""Check UI evidence artifacts and recorded observations for consistency.

A report can claim several widths passed. This checks the evidence behind the claim: every
promised width has a screenshot, each screenshot's pixel width matches the width its filename
claims (at a device pixel ratio of 1, 1.25, 1.5, 2 or 3), and no two screenshots are the same file.

Screenshots are named <before|after>-<cssWidth>.png, e.g. after-390.png, after-1440.png.
This checks PNG metadata and records, not the appearance of the rendered UI. A pass does not
establish visual quality, that someone inspected the screenshots, or that observations are true.

An optional verdict.visualReview records status (pass, fail or not-verified) and views. Each view
has an integer CSS width, one of those statuses, and a nonempty observation describing what was
seen. Review widths must be unique, claimed by the verdict, and have an after screenshot.
--require-visual-review additionally requires a recorded pass covering every requested width.

Widths: --widths wins; otherwise the widths listed in verdict.json; otherwise 390,1440 (legacy
example defaults, not a universal coverage requirement). A verdict with status "skipped" and a reason (no dev
server, no browser) is an honest skip and exits 0.

Usage:
  python ui_verify.py .agents/verify/<task-slug>
  python ui_verify.py .agents/verify/dashboard --widths 390,768,1440 --require-before --json
  python ui_verify.py .agents/verify/dashboard --require-visual-review --json
Exit codes: 0 consistent artifacts/records (or honestly skipped), 1 evidence problem, 2 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

DEFAULT_WIDTHS = (390, 1440)
DEVICE_PIXEL_RATIOS = (1, 1.25, 1.5, 1.75, 2, 2.5, 3)
NAME = re.compile(r"^(before|after)-(\d{3,4})\.png$", re.I)
REQUIRED_KEYS = ("route", "widths", "status")
VISUAL_STATUSES = {"pass", "fail", "not-verified"}
VERIFICATION_SCOPE = (
    "Artifact and record consistency only: checks PNG metadata, file uniqueness and verdict/review "
    "records. Does not inspect screenshot appearance, assess visual quality or verify observer truth."
)


def _png_size(path: Path) -> tuple[int, int] | None:
    """Width and height from the PNG IHDR chunk - no image library needed."""
    try:
        with path.open("rb") as fh:
            head = fh.read(24)
    except OSError:
        return None
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return None
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def _digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def _as_width(value: object) -> int | None:
    try:
        return int(str(value).strip().rstrip("px"))
    except ValueError:
        return None


def _check_visual_review(verdict: dict | None, claimed_widths: list[int], wanted: tuple[int, ...],
                         have_after: dict[int, dict], report: dict, required: bool) -> None:
    """Validate a recorded review, without claiming to perform or substantiate that review."""
    if verdict is None or "visualReview" not in verdict:
        report["notes"].append("No visual review recorded; consistent artifacts do not establish visual quality.")
        if required:
            report["issues"].append("--require-visual-review requires a visualReview record")
        return

    review = verdict["visualReview"]
    invalid: list[str] = []
    if not isinstance(review, dict):
        invalid.append("visualReview must be an object with status and views")
        review = {}
    review_status = review.get("status")
    if not isinstance(review_status, str) or review_status not in VISUAL_STATUSES:
        invalid.append("visualReview status must be pass, fail or not-verified")
    views = review.get("views")
    if not isinstance(views, list):
        invalid.append("visualReview views must be a list")
        views = []

    seen: set[int] = set()
    view_statuses: list[str] = []
    for index, view in enumerate(views):
        label = f"visualReview views[{index}]"
        if not isinstance(view, dict):
            invalid.append(f"{label} must be an object with width, status and observation")
            continue
        width = view.get("width")
        if isinstance(width, bool) or not isinstance(width, int) or not 100 <= width <= 9999:
            invalid.append(f"{label} width must be an integer CSS width from 100 to 9999")
        else:
            if width in seen:
                invalid.append(f"visualReview has duplicate width {width}")
            seen.add(width)
            if width not in claimed_widths:
                invalid.append(f"visualReview width {width} is not claimed in verdict widths")
            if width not in have_after:
                invalid.append(f"visualReview width {width} has no after-{width}.png")
        view_status = view.get("status")
        if not isinstance(view_status, str) or view_status not in VISUAL_STATUSES:
            invalid.append(f"{label} status must be pass, fail or not-verified")
        else:
            view_statuses.append(view_status)
        observation = view.get("observation")
        if not isinstance(observation, str) or not observation.strip():
            invalid.append(f"{label} must include a nonempty observation of the rendered view")

    if invalid:
        report["issues"].extend(invalid)
        report["visualReviewStatus"] = "invalid"
        return

    if review_status == "fail" or "fail" in view_statuses:
        report["visualReviewStatus"] = "fail"
        if str(verdict.get("status", "")).lower() == "pass":
            report["issues"].append("verdict says pass but visualReview records a visual failure")
    elif review_status == "not-verified" or "not-verified" in view_statuses:
        report["visualReviewStatus"] = "not-verified"
    else:
        report["visualReviewStatus"] = "pass" if set(wanted) <= seen else "not-verified"

    if review_status == "pass" and any(s != "pass" for s in view_statuses):
        report["issues"].append("visualReview says pass but a view records fail or not-verified")
    missing = sorted(set(wanted) - seen)
    if missing:
        report["notes"].append("Visual review does not cover requested width(s): " + ", ".join(map(str, missing)))
    report["notes"].append(
        f"Recorded visual review: {report['visualReviewStatus']}; this checker does not inspect images "
        "or verify the observations.")
    if required and report["visualReviewStatus"] != "pass":
        report["issues"].append("--require-visual-review requires a passing review covering every requested width")


def verify(dirpath: Path, widths: tuple[int, ...] | None = None, require_before: bool = False,
           require_visual_review: bool = False) -> dict:
    """Check artifact/record consistency; optionally require recorded visual review coverage."""
    report: dict = {"dir": str(dirpath), "screenshots": [], "issues": [], "notes": [],
                    "verificationScope": VERIFICATION_SCOPE, "visualReviewStatus": "not-recorded"}

    if not dirpath.is_dir():
        report["issues"].append(f"no verification directory at {dirpath} - the check did not run")
        report["status"] = "fail"
        return report

    verdict_path = dirpath / "verdict.json"
    verdict: dict | None = None
    if not verdict_path.is_file():
        report["issues"].append("verdict.json missing - a report with no verdict file is only a claim")
    else:
        try:
            loaded = json.loads(verdict_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            report["issues"].append(f"verdict.json is not valid JSON: {exc}")
        else:
            if not isinstance(loaded, dict):
                report["issues"].append("verdict.json must be a JSON object")
            else:
                verdict = loaded
                missing = [k for k in REQUIRED_KEYS if k not in verdict]
                if missing:
                    report["issues"].append(f"verdict.json missing key(s): {', '.join(missing)}")

    status = str((verdict or {}).get("status", "")).lower()
    if verdict is not None and status not in {"pass", "fail", "skipped"}:
        report["issues"].append("verdict status must be pass, fail or skipped")
    if status == "skipped":
        if verdict and isinstance(verdict.get("reason"), str) and verdict["reason"].strip():
            report["notes"].append(f"verification skipped: {verdict['reason']}")
            report["visualReviewStatus"] = "skipped"
            report["notes"].append("Visual review was not established because verification was skipped.")
            report["status"] = "skipped" if not report["issues"] else "fail"
        else:
            report["issues"].append("verdict is 'skipped' with no reason - name the missing precondition")
            report["status"] = "fail"
        return report

    raw_widths = (verdict or {}).get("widths")
    claimed_widths: list[int] = []
    if isinstance(raw_widths, list):
        for value in raw_widths:
            width = _as_width(value)
            if isinstance(value, bool) or width is None or not 100 <= width <= 9999:
                report["issues"].append(f"invalid claimed CSS width: {value!r}")
            else:
                claimed_widths.append(width)
        if len(claimed_widths) != len(set(claimed_widths)):
            report["issues"].append("verdict widths must not contain duplicates")
    elif verdict is not None:
        report["issues"].append("verdict widths must be a list of CSS widths")
    if status == "pass" and not claimed_widths:
        report["issues"].append("passing verdict must list the widths actually rendered")
    if status == "pass" and not (isinstance(verdict.get("route"), str) and verdict["route"].strip()):
        report["issues"].append("passing verdict must name the rendered route")
    wanted = tuple(widths) if widths else (tuple(claimed_widths) or DEFAULT_WIDTHS)
    report["widths"] = list(wanted)

    shots: dict[str, dict[int, dict]] = {}
    by_hash: dict[str, list[str]] = {}
    for png in sorted(dirpath.glob("*.png")):
        m = NAME.match(png.name)
        size = _png_size(png)
        digest = _digest(png)
        entry: dict = {"file": png.name, "sha256_16": digest, "pixels": list(size) if size else None}
        if not m:
            entry["note"] = "not named <before|after>-<width>.png; not counted as evidence"
            report["screenshots"].append(entry)
            continue
        state, claimed = m.group(1).lower(), int(m.group(2))
        entry["state"], entry["claimedWidth"] = state, claimed
        if size is None:
            report["issues"].append(f"{png.name}: not a readable PNG")
        elif not any(abs(size[0] - claimed * dpr) <= 2 for dpr in DEVICE_PIXEL_RATIOS):
            report["issues"].append(
                f"{png.name} is {size[0]}px wide but its name claims {claimed}px - this screenshot was not "
                "taken at the width it reports")
        by_hash.setdefault(digest, []).append(png.name)
        shots.setdefault(state, {})[claimed] = entry
        report["screenshots"].append(entry)

    for names in by_hash.values():
        if len(names) > 1:
            report["issues"].append(
                f"identical image reported as different views: {', '.join(names)} (same bytes) - these cannot "
                "be captures of different widths or states")

    have_after = shots.get("after", {})
    for w in wanted:
        if w not in have_after:
            report["issues"].append(f"no after-{w}.png - width {w} was never rendered")
    if require_before and not shots.get("before"):
        report["issues"].append("no before-*.png - on a repair this is the only proof the defect existed")

    if verdict is not None:
        for w in claimed_widths:
            if w not in have_after:
                report["issues"].append(f"verdict.json claims width {w} was checked, but no after-{w}.png exists")
        if status == "pass":
            for key in ("consoleErrors", "failedRequests"):
                val = verdict.get(key)
                if isinstance(val, bool) or not isinstance(val, int) or val < 0:
                    report["issues"].append(f"passing verdict must record a nonnegative integer {key}")
                elif val > 0:
                    report["issues"].append(f"verdict says pass but {key} is {val} - that is a failure")
            interaction = verdict.get("interaction")
            if interaction == "not-applicable":
                reason = verdict.get("interactionReason")
                if not isinstance(reason, str) or not reason.strip():
                    report["issues"].append("not-applicable interaction must include interactionReason")
            elif interaction != "pass":
                report["issues"].append("passing verdict must record interaction pass or justified not-applicable")
            if not isinstance(verdict.get("notVerified"), list):
                report["issues"].append("passing verdict must record notVerified as a list")
            elif verdict["notVerified"]:
                report["issues"].append("verdict says pass while checks remain not verified")
        if status == "fail":
            report["notes"].append("verdict.json records a failed verification")

    _check_visual_review(verdict, claimed_widths, wanted, have_after, report, require_visual_review)
    report["status"] = "fail" if report["issues"] or status == "fail" else "pass"
    return report


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Check UI artifact and record consistency; does not assess visual quality.",
                                 epilog="Exit codes: 0 consistent or honestly skipped, 1 evidence problem, 2 usage.")
    ap.add_argument("dir", type=Path, help=".agents/verify/<task-slug>")
    ap.add_argument("--widths", help="CSS widths that need an after-<width>.png (default: verdict.json, else 390,1440)")
    ap.add_argument("--require-before", action="store_true", help="a repair must also carry before-<width>.png")
    ap.add_argument("--require-visual-review", action="store_true",
                    help="require a recorded passing visualReview for every requested width; does not inspect images")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    ap.add_argument("--report", type=Path, help="also write the JSON result here")
    args = ap.parse_args(argv)

    widths = None
    if args.widths:
        try:
            widths = tuple(int(w) for w in args.widths.split(",") if w.strip())
        except ValueError:
            ap.error("--widths must be comma-separated integers, e.g. 390,1440")
        if not widths or any(not 100 <= w <= 9999 for w in widths) or len(widths) != len(set(widths)):
            ap.error("--widths must contain unique CSS widths from 100 to 9999")
    result = verify(args.dir, widths, args.require_before, args.require_visual_review)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        label = {"pass": "[PASS]", "skipped": "[SKIP]"}.get(result["status"], "[FAIL]")
        counted = len([s for s in result["screenshots"] if s.get("claimedWidth")])
        print(f"{label} artifact/record consistency: {args.dir} - {counted} screenshot(s), "
              f"{len(result['issues'])} issue(s); recorded visual review: {result['visualReviewStatus']}")
        print(f"  . {result['verificationScope']}")
        for issue in result["issues"]:
            print(f"  - {issue}")
        for note in result["notes"]:
            print(f"  . {note}")
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
