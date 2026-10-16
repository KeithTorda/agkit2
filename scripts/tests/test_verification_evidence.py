"""Behavioral checks for honest verification reports; no browser/network required."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import validation_runner as runner
import ui_verify
import validate_kit


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


lint = load("evidence_lint_runner", "skills/lint-and-validate/scripts/lint_runner.py")
coverage = load("evidence_type_coverage", "skills/lint-and-validate/scripts/type_coverage.py")


def helper_main(module, project: Path, *args: str):
    output = io.StringIO()
    with mock.patch.object(sys, "argv", ["helper", str(project), "--json", *args]), \
            contextlib.redirect_stdout(output):
        code = module.main()
    return code, json.loads(output.getvalue())


class RunnerEvidenceTests(unittest.TestCase):
    def result(self, status: str, required: bool = True, **kwargs):
        return runner.CheckResult("Types", "types", status, required, **kwargs)

    def test_missing_or_broken_required_check_is_never_a_pass(self):
        for status in ("missing", "error"):
            with self.subTest(status=status):
                rows = [self.result("passed"), self.result(status)]
                payload = runner.report_payload("test", ROOT, "quick", rows, datetime.now(timezone.utc))
                self.assertTrue(payload["success"], "keep legacy process/exit policy")
                self.assertEqual("INCOMPLETE", payload["outcome"])
                self.assertFalse(payload["verified"])
                self.assertEqual(["Types"], payload["not_verified"])
                self.assertNotIn("PASS", runner.verdict_line(rows))

    def test_empty_and_inapplicable_runs_are_skipped(self):
        for rows in ([], [self.result("skipped")]):
            self.assertEqual("SKIPPED", runner.suite_outcome(rows))
            self.assertNotIn("PASS", runner.verdict_line(rows))

    def test_explicit_deferred_required_step_remains_unverified(self):
        rows = [self.result("passed"), self.result("skipped", skip_not_verified=True)]
        self.assertEqual("INCOMPLETE", runner.suite_outcome(rows))
        self.assertEqual([rows[1]], runner.not_run(rows))

    def test_completed_required_checks_pass_with_advisory_findings(self):
        rows = [self.result("passed"), self.result("failed", required=False)]
        self.assertEqual("PASS", runner.suite_outcome(rows))
        self.assertEqual("FAIL", runner.suite_outcome(rows, strict=True))

    def test_missing_later_command_cannot_erase_required_failure(self):
        step = runner.Step("Tests", "tests", [[sys.executable, "-c", "print('real regression');raise SystemExit(1)"],
                                                ["agkit-nonexistent-tool-xyz"]], required=True)
        result = runner.run_step(step)
        self.assertEqual("failed", result.status)
        self.assertEqual(1, result.exit_code)
        self.assertIn("real regression", result.detail)
        self.assertEqual("FAIL", runner.suite_outcome([result]))

    def test_broken_later_kit_command_cannot_erase_findings(self):
        step = runner.Step("Security", "security", [[sys.executable, "-c", "raise SystemExit(1)"],
                                                     [sys.executable, "-c", "raise SystemExit(2)"]],
                           required=True, kit_script=True)
        result = runner.run_step(step)
        self.assertEqual("failed", result.status)
        self.assertEqual(1, result.exit_code)

    def test_os_permission_error_is_incomplete_not_missing(self):
        with mock.patch.object(runner.subprocess, "run", side_effect=PermissionError("access denied")):
            result = runner.run_step(runner.Step("Types", "types", [["compiler"]], required=True))
        self.assertEqual("error", result.status)
        self.assertEqual("INCOMPLETE", runner.suite_outcome([result]))

    def test_stop_on_fail_preserves_unexecuted_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "must-not-run.txt"
            bad = runner.Step("tests", "tests", [[sys.executable, "-c", "raise SystemExit(1)"]], required=True)
            later = runner.Step("build", "build", [[sys.executable, "-c", f"open({str(marker)!r}, 'w').close()"]], required=True)
            rows = runner.execute([bad, later], stop_on_fail=True)
            self.assertFalse(marker.exists())
            self.assertEqual(["failed", "skipped"], [r.status for r in rows])
            self.assertEqual([rows[1]], runner.not_run(rows))


class UserPathHygieneTests(unittest.TestCase):
    def test_manifest_and_release_version_must_agree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("agents", "skills", "scripts"):
                (root / name).mkdir()
            (root / "VERSION").write_text("2.7.0", encoding="utf-8")
            (root / "plugin.json").write_text('{"version":"2.7.0"}', encoding="utf-8")
            validator = validate_kit.Validator(root)
            validator.check_layout()
            self.assertEqual([], validator.findings)
            (root / "plugin.json").write_text('{"version":"2.6.0"}', encoding="utf-8")
            validator.check_layout()
            self.assertIn("version.mismatch", [f.code for f in validator.findings])

    def test_portability_check_catches_other_users_and_drive_case(self):
        for prefix in ("D:/Users/", "c:\\users\\", "C:\\\\Users\\\\"):
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "notes.md").write_text(prefix + "Another Person/app", encoding="utf-8")
                validator = validate_kit.Validator(root)
                validator.check_hygiene()
                self.assertIn("hygiene.user_path", [f.code for f in validator.findings])


class UiVerdictEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for width in (390, 1440):
            # The consistency checker only reads PNG dimensions, not composition.
            header = b"\x89PNG\r\n\x1a\n" + (13).to_bytes(4, "big") + b"IHDR"
            (self.root / f"after-{width}.png").write_bytes(header + width.to_bytes(4, "big") + (600).to_bytes(4, "big"))
        self.verdict = {"route": "/x", "widths": [390, 1440], "status": "pass", "consoleErrors": 0,
                        "failedRequests": 0, "interaction": "pass", "notVerified": []}

    def verify(self):
        (self.root / "verdict.json").write_text(json.dumps(self.verdict), encoding="utf-8")
        return ui_verify.verify(self.root)

    def test_completed_evidence_is_accepted(self):
        self.assertEqual("pass", self.verify()["status"])

    def test_unknown_or_missing_status_cannot_become_a_pass(self):
        for status in (None, "complete", "", "banana"):
            self.verdict["status"] = status
            self.assertEqual("fail", self.verify()["status"])

    def test_required_observations_cannot_be_omitted(self):
        for field in ("consoleErrors", "failedRequests", "interaction", "notVerified"):
            value = self.verdict.pop(field)
            with self.subTest(field=field):
                self.assertEqual("fail", self.verify()["status"])
            self.verdict[field] = value

    def test_not_verified_and_failed_interaction_contradict_pass(self):
        self.verdict["notVerified"] = ["mobile modal state"]
        self.assertEqual("fail", self.verify()["status"])
        self.verdict["notVerified"] = []
        self.verdict["interaction"] = "fail"
        self.assertEqual("fail", self.verify()["status"])

    def test_boolean_or_negative_counts_do_not_fabricate_clean_console(self):
        for value in (False, -1, "0", None):
            self.verdict["consoleErrors"] = value
            self.assertEqual("fail", self.verify()["status"])

    def test_noninteractive_repair_can_explain_why_interaction_is_inapplicable(self):
        self.verdict["interaction"] = "not-applicable"
        self.assertEqual("fail", self.verify()["status"])
        self.verdict["interactionReason"] = "Static title colour repair; no control changed"
        self.assertEqual("pass", self.verify()["status"])

    def test_malformed_widths_are_reported_without_crashing(self):
        for value in (390, "390", {}, [True], [0], [390, 390], []):
            self.verdict["widths"] = value
            self.assertEqual("fail", self.verify()["status"])


class StaticHelperEvidenceTests(unittest.TestCase):
    def test_lint_without_any_tools_is_skipped_not_passed(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, report = helper_main(lint, Path(tmp))
            self.assertEqual(0, code)
            self.assertEqual("SKIPPED", report["outcome"])
            self.assertFalse(report["passed"])
            self.assertFalse(report["verified"])

    def test_missing_configured_linter_is_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(lint, "find_executable", return_value=None):
            root = Path(tmp)
            (root / "pyproject.toml").write_text("[tool.ruff]\n", encoding="utf-8")
            code, report = helper_main(lint, root)
            self.assertEqual(0, code)
            self.assertEqual("INCOMPLETE", report["outcome"])
            self.assertFalse(report["verified"])
            self.assertTrue(report["not_verified"])

    def test_type_source_scan_is_incomplete_without_compiler(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "app.ts").write_text("const n: number = 3;", encoding="utf-8")
            (root / "tsconfig.json").write_text("{}", encoding="utf-8")
            for extra in ([], ["--skip-compiler"]):
                code, report = helper_main(coverage, root, *extra)
                self.assertEqual(0, code)
                self.assertEqual("INCOMPLETE", report["outcome"])
                self.assertFalse(report["passed"])
                self.assertTrue(report["not_verified"])

    def test_heuristic_counts_do_not_create_correctness_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adapter.ts").write_text("\n".join(f"const value{i}: any = null; // @ts-ignore" for i in range(40)), encoding="utf-8")
            result = coverage.check_typescript_coverage(root, run_compiler=False)
            self.assertEqual([], result["errors"])
            self.assertTrue(result["warnings"])

    def test_python_syntax_errors_remain_real_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "broken.py").write_text("def missing(:", encoding="utf-8")
            code, report = helper_main(coverage, root)
            self.assertEqual(1, code)
            self.assertEqual("FAIL", report["outcome"])


if __name__ == "__main__":
    unittest.main()
