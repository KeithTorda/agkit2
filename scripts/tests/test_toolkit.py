"""Regression tests for the AG Kit v2.5 scripts.

Run from the kit root:
  python -m unittest scripts/tests/test_toolkit.py -v

Fixtures are built in temporary directories. Nothing here depends on the kit being a git
checkout; the git-scoping test builds its own throwaway repository and skips without git.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

TOOLKIT = Path(__file__).resolve().parents[2]
SCRIPTS = TOOLKIT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_optional(name: str, rel: str):
    path = TOOLKIT / rel
    return load_module(name, path) if path.is_file() else None


validate_kit = load_module("agkit_validate_kit", SCRIPTS / "validate_kit.py")
validation_runner = load_module("validation_runner", SCRIPTS / "validation_runner.py")
checklist = load_module("checklist", SCRIPTS / "checklist.py")
css_audit = load_module("agkit_css_audit", SCRIPTS / "css_audit.py")
naming_check = load_module("agkit_naming_check", SCRIPTS / "naming_check.py")
ui_verify = load_module("agkit_ui_verify", SCRIPTS / "ui_verify.py")
build_quick_reference = load_module("agkit_build_quick_reference", SCRIPTS / "build_quick_reference.py")

security_scan = load_optional("agkit_security_scan", "skills/vulnerability-scanner/scripts/security_scan.py")
dependency_analyzer = load_optional("agkit_dependency_analyzer", "skills/vulnerability-scanner/scripts/dependency_analyzer.py")
bundle_analyzer = load_optional("agkit_bundle_analyzer", "skills/performance-profiling/scripts/bundle_analyzer.py")
geo_checker = load_optional("agkit_geo_checker", "skills/seo-fundamentals/scripts/geo_checker.py")
react_performance = load_optional("agkit_react_performance", "skills/nextjs-react-expert/scripts/react_performance_checker.py")

USER_PATH = "C:/Users/" + "Keith"


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip("\n"), "utf-8")
    return path


def make_tool(folder: Path, name: str, exit_code: int = 0, output: str = "") -> Path:
    """A fake command-line tool that prints `output` and exits with `exit_code` (POSIX and Windows)."""
    folder.mkdir(parents=True, exist_ok=True)
    body = folder / f"_{name}_impl.py"
    body.write_text(f"import sys\nprint({output!r})\nsys.exit({exit_code})\n", "utf-8")
    if os.name == "nt":
        tool = folder / f"{name}.cmd"
        tool.write_text(f'@echo off\r\n"{sys.executable}" "{body}" %*\r\nexit /b %errorlevel%\r\n', "utf-8")
    else:
        tool = folder / name
        tool.write_text(f"#!{sys.executable}\nimport runpy\nrunpy.run_path({str(body)!r}, run_name='__main__')\n", "utf-8")
        tool.chmod(tool.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return tool


def run_main(func, argv: list[str]) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = func(argv)
    return code, out.getvalue()


# ---------------------------------------------------------------------------------------------
# Fixture kit for validate_kit / build_quick_reference
# ---------------------------------------------------------------------------------------------
AGENT_BODY = """
# Demo Agent

## Role
Owns demo files.

## How you work
**Read now:** `KIT/skills/demo-skill/SKILL.md`

## Build
Build it.

## Repair
Fix it.

## Decide
Choose.

## Never
Leak secrets.

## As a subagent
Return files and findings in under 200 words.

## Done
Per `code-rules` tier.
"""


def agent_file(name: str = "demo-agent", extra_fm: str = "", skills: str = "[demo-skill]", body: str = AGENT_BODY) -> str:
    return (
        "---\n"
        f"name: {name}\n"
        'description: "Builds demo things for tests. Does not own anything real. Triggers on: demo, fixture."\n'
        "model: inherit\n"
        "subagent: true\n"
        "mainAgent: true\n"
        f"kit-skills: {skills}\n"
        "version: 2.5.0\n"
        f"{extra_fm}"
        "---\n" + textwrap.dedent(body)
    )


def rule_file(name: str, trigger: str = "always_on", body: str = "Body.\n", extra: str = "") -> str:
    return (f"---\nname: {name}\nversion: 2.5.0\npriority: P0\ntrigger: {trigger}\n{extra}"
            f"description: Test rule {name}.\n---\n\n# {name}\n\n{body}")


def build_fixture_kit(root: Path) -> Path:
    write(root / "plugin.json", '{"name": "ag-kit-v2"}')
    write(root / "VERSION", "2026.9.27\n")
    write(root / "install.ps1", f'$Default = "{USER_PATH}"\n')
    write(root / "rules" / "core-protocol.md", rule_file("core-protocol", body=f"`KIT` = `{USER_PATH}/.gemini/config/plugins/ag-kit-v2`.\n"))
    write(root / "rules" / "request-routing.md", rule_file("request-routing", body=(
        "## Commands\n| Command | Use |\n|---|---|\n| `/demo <x>` | Demo command |\n\n"
        "## Agents\n| Agent | Takes |\n|---|---|\n| `demo-agent` | demo work |\n")))
    write(root / "rules" / "quick-reference.md", rule_file("quick-reference", trigger="model_decision"))
    write(root / "rules" / "design-rules.md", rule_file("design-rules", trigger="glob", extra='globs: "**/*.css"\n'))
    write(root / "agents" / "demo-agent.md", agent_file())
    write(root / "skills" / "demo-skill" / "SKILL.md",
          "---\nname: demo-skill\ndescription: Demo reference skill used by the test suite fixture kit only.\nversion: 2.5.0\n---\n\n"
          "# Demo\n\nSee `KIT/agents/demo-agent.md` and `KIT/skills/demo/SKILL.md`.\n")
    write(root / "skills" / "demo" / "SKILL.md",
          '---\nname: demo\ndescription: "/demo - Runs the demo command for the fixture kit in tests."\nversion: 2.5.0\n---\n\n# /demo\n')
    write(root / "scripts" / "noop.py", "print('ok')\n")
    write(root / "scripts" / "build_quick_reference.py", "print('stub')\n")
    return root


def codes(findings, severity: str = "error") -> set[str]:
    return {f.code for f in findings if f.severity == severity}


class ValidateKitFixtureTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = build_fixture_kit(Path(self._tmp.name) / "kit")

    def tearDown(self):
        self._tmp.cleanup()

    def validate(self):
        return validate_kit.validate(self.root)

    def test_valid_fixture_has_no_errors(self):
        findings = self.validate()
        self.assertEqual([], [f for f in findings if f.severity == "error"], findings)

    def test_agent_tools_and_legacy_skills_keys_are_errors(self):
        write(self.root / "agents" / "demo-agent.md", agent_file(extra_fm="tools: [read_file]\nskills: demo-skill\n"))
        found = codes(self.validate())
        self.assertIn("agent.tools_key", found)
        self.assertIn("agent.legacy_skills_key", found)

    def test_agent_needs_native_frontmatter(self):
        text = agent_file().replace("model: inherit\n", "").replace("subagent: true\n", "")
        write(self.root / "agents" / "demo-agent.md", text.replace("name: demo-agent", "name: other"))
        found = codes(self.validate())
        self.assertTrue({"agent.model", "agent.subagent", "agent.name_mismatch"} <= found, found)

    def test_agent_kit_skills_must_exist(self):
        write(self.root / "agents" / "demo-agent.md", agent_file(skills="[demo-skill, no-such-skill]"))
        self.assertIn("reference.unknown_skill", codes(self.validate()))
        write(self.root / "agents" / "demo-agent.md", agent_file(skills="demo-skill"))
        self.assertIn("agent.kit_skills", codes(self.validate()), "kit-skills must be a list")

    def test_agent_sections_required_and_ordered(self):
        write(self.root / "agents" / "demo-agent.md", agent_file(body=AGENT_BODY.replace("## As a subagent", "## Handoff")))
        self.assertIn("agent.section_missing", codes(self.validate()))
        swapped = AGENT_BODY.replace("## Build\nBuild it.", "## TMP").replace("## Repair\nFix it.", "## Build\nBuild it.")
        swapped = swapped.replace("## TMP", "## Repair\nFix it.")
        write(self.root / "agents" / "demo-agent.md", agent_file(body=swapped))
        self.assertIn("agent.section_order", codes(self.validate()))

    def test_rules_hex_trigger_and_budget(self):
        write(self.root / "rules" / "code-rules.md", rule_file("code-rules", body="Use #1a2b3c for text.\n"))
        self.assertIn("rule.hex_colour", codes(self.validate()))
        write(self.root / "rules" / "code-rules.md", rule_file("code-rules", trigger="always"))
        self.assertIn("rule.trigger", codes(self.validate()))
        write(self.root / "rules" / "code-rules.md", rule_file("code-rules", body="word " * 3100))
        self.assertIn("rules.always_on_budget", codes(self.validate()))

    def test_budget_ignores_model_decision_and_glob_rules(self):
        write(self.root / "rules" / "quick-reference.md", rule_file("quick-reference", trigger="model_decision", body="x" * 20000))
        write(self.root / "rules" / "design-rules.md", rule_file("design-rules", trigger="glob", extra='globs: "**/*.css"\n', body="y" * 20000))
        self.assertNotIn("rules.always_on_budget", codes(self.validate()))

    def test_quick_reference_must_be_model_decision(self):
        write(self.root / "rules" / "quick-reference.md", rule_file("quick-reference", trigger="always_on"))
        self.assertIn("rule.quick_reference_trigger", codes(self.validate()))

    def test_routed_command_and_agent_must_exist(self):
        routing = self.root / "rules" / "request-routing.md"
        routing.write_text(routing.read_text("utf-8").replace("`/demo <x>`", "`/demo <x>` `/ghost`")
                           .replace("| `demo-agent` | demo work |", "| `demo-agent` | demo work |\n| `ghost-agent` | x |"), "utf-8")
        found = codes(self.validate())
        self.assertIn("routing.command_without_skill", found)
        self.assertIn("routing.agent_missing", found)

    def test_kit_references_resolve_and_placeholders_are_ignored(self):
        skill = self.root / "skills" / "demo-skill" / "SKILL.md"
        skill.write_text(skill.read_text("utf-8") + "\nPlaceholders: `KIT/skills/<name>/SKILL.md`, `KIT/agents/<name>.md`.\n", "utf-8")
        self.assertNotIn("reference.missing_path", codes(self.validate()))
        skill.write_text(skill.read_text("utf-8") + "\nBroken: `KIT/skills/missing-skill/SKILL.md` and KIT/agents/nobody.md.\n", "utf-8")
        missing = [f for f in self.validate() if f.code == "reference.missing_path"]
        self.assertEqual(2, len(missing), missing)

    def test_user_path_only_allowed_in_core_protocol(self):
        write(self.root / "skills" / "demo-skill" / "notes.md", f"Run python {USER_PATH}/x.py\n")
        hits = [f for f in self.validate() if f.code == "hygiene.user_path"]
        self.assertEqual(["skills/demo-skill/notes.md"], [f.file for f in hits])

    def test_obsolete_files_are_warnings(self):
        write(self.root / "rules" / "copy.md", "---\nname: copy\ntrigger: always\n---\n# Old\n" + "#ffffff " * 3000)
        write(self.root / "BRIEF-v2.5.md", "brief\n")
        findings = self.validate()
        self.assertEqual({"rules/copy.md", "BRIEF-v2.5.md"}, {f.file for f in findings if f.code == "obsolete.file"})
        self.assertEqual([], [f for f in findings if f.severity == "error"], "obsolete files must not add errors")

    def test_size_warnings_exempt_parts_and_templates(self):
        big = "---\nname: demo-skill\ndescription: Demo reference skill used by the test suite fixture kit only.\nversion: 2.5.0\n---\n" + "text " * 5000
        write(self.root / "skills" / "demo-skill" / "SKILL.md", big)
        write(self.root / "skills" / "demo-skill" / "parts" / "01-big.md", "part " * 9000)
        write(self.root / "skills" / "demo-skill" / "templates" / "big.md", "tmpl " * 9000)
        sized = {f.file for f in self.validate() if f.code == "size.skill"}
        self.assertEqual({"skills/demo-skill/SKILL.md"}, sized)

    def test_skill_name_must_match_folder(self):
        write(self.root / "skills" / "demo-skill" / "SKILL.md",
              "---\nname: wrong\ndescription: Demo reference skill used by the test suite fixture kit only.\nversion: 2.5.0\n---\n")
        self.assertIn("skill.name_mismatch", codes(self.validate()))

    def test_unquoted_colon_in_frontmatter_is_an_error(self):
        write(self.root / "skills" / "demo-skill" / "SKILL.md",
              "---\nname: demo-skill\ndescription: Use when: the fixture needs a broken description value.\nversion: 2.5.0\n---\n")
        found = codes(self.validate())
        self.assertTrue(found & {"frontmatter.unquoted_colon", "frontmatter.invalid_yaml"}, found)

    def test_frontmatter_parser_without_pyyaml(self):
        data = validate_kit.parse_frontmatter(
            'name: a\nkit-skills: [x, "y"]\nsubagent: true\nlist:\n  - one\n  - two\ndesc: >\n  folded\n  text\n')
        self.assertEqual(["x", "y"], data["kit-skills"])
        self.assertIs(True, data["subagent"])
        self.assertEqual(["one", "two"], data["list"])
        self.assertEqual("folded text", data["desc"])

    def test_quick_reference_build_uses_kit_paths_and_frontmatter(self):
        content = build_quick_reference.build(self.root)
        self.assertIn("trigger: model_decision", content)
        self.assertNotIn(USER_PATH, content)
        self.assertIn("| demo-agent | demo, fixture | demo-skill |", content)
        self.assertIn("| /demo |", content)
        self.assertIn("| demo-skill |", content)
        self.assertIn("`KIT/scripts/noop.py`", content)
        out = self.root / "rules" / "quick-reference.md"
        self.assertEqual(0, run_main(build_quick_reference.main, ["--kit", str(self.root), "--write"])[0])
        self.assertEqual(content, out.read_text("utf-8"))
        self.assertEqual(0, run_main(build_quick_reference.main, ["--kit", str(self.root), "--check"])[0])
        # the regenerated rule validates
        self.assertEqual([], [f for f in self.validate() if f.severity == "error"])


# ---------------------------------------------------------------------------------------------
# The real kit
# ---------------------------------------------------------------------------------------------
class RealKitTests(unittest.TestCase):
    def test_real_kit_validates(self):
        """The ship gate. Errors here are real (in-progress edits by other workers show up too)."""
        findings = validate_kit.validate(TOOLKIT)
        errors = [f"{f.file}:{f.line} {f.code} {f.message}" for f in findings if f.severity == "error"]
        self.assertEqual([], errors)

    def test_real_kit_rule_invariants(self):
        findings = validate_kit.validate(TOOLKIT)
        for code in ("rules.always_on_budget", "rule.hex_colour", "agent.tools_key", "agent.legacy_skills_key",
                     "python.syntax", "json.invalid"):
            with self.subTest(code=code):
                self.assertEqual([], [f for f in findings if f.code == code and f.severity == "error"])

    def test_no_legacy_directories(self):
        for legacy in ("workflows", "agent"):
            self.assertFalse((TOOLKIT / legacy).exists(), f"{legacy}/ must not exist in the toolkit")

    def test_scripts_have_no_user_path(self):
        for path in SCRIPTS.rglob("*.py"):
            with self.subTest(script=path.name):
                self.assertNotIn(USER_PATH, path.read_text("utf-8"))

    def test_every_script_has_help(self):
        for path in sorted(SCRIPTS.glob("*.py")):
            if path.name == "validation_runner.py":
                continue
            with self.subTest(script=path.name):
                proc = subprocess.run([sys.executable, str(path), "--help"], capture_output=True, text=True,
                                      encoding="utf-8", errors="replace", timeout=60)
                self.assertEqual(0, proc.returncode, proc.stderr[-500:])

    def test_proplan_check_accepts_bundled_example(self):
        script = SCRIPTS / "proplan_check.py"
        example = TOOLKIT / "skills" / "proplan" / "example" / "pos-lite"
        if not script.is_file() or not example.is_dir():
            self.skipTest("proplan_check.py or the pos-lite example is not present yet")
        proc = subprocess.run([sys.executable, str(script), str(example)], capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=120)
        self.assertEqual(0, proc.returncode, (proc.stdout + proc.stderr)[-1500:])

    def test_no_prose_duplicated_across_skill_files(self):
        """The same long prose run copied into more than one SKILL.md is wasted context.

        Command wrappers (description starts with "/") mirror the skill they wrap and are excluded.
        """
        def is_command(path):
            m = re.search(r"^description:\s*(.+)$", path.read_text("utf-8"), re.M)
            return bool(m) and m.group(1).lstrip("\"' ").startswith("/")

        seen: dict[str, str] = {}
        dupes = []
        for f in sorted((TOOLKIT / "skills").glob("*/SKILL.md")):
            if is_command(f):
                continue
            text = re.sub(r"```.*?```", "", f.read_text("utf-8"), flags=re.S)
            key = f"{f.parent.name}/SKILL.md"
            for para in re.split(r"\n\s*\n", text):
                words = re.findall(r"\w+", para.lower())
                for i in range(len(words) - 23):
                    shingle = " ".join(words[i:i + 24])
                    if shingle in seen and seen[shingle] != key:
                        dupes.append((seen[shingle], key))
                    seen[shingle] = key
        self.assertEqual([], sorted(set(dupes))[:5], "duplicated prose across skills")


# ---------------------------------------------------------------------------------------------
# checklist.py tiers
# ---------------------------------------------------------------------------------------------
class ChecklistTierTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name) / "proj"
        write(self.project / "pyproject.toml", '[project]\nname = "demo"\n\n[tool.mypy]\nstrict = false\n')
        write(self.project / "app_core.py", "def add(a: int, b: int) -> int:\n    return a + b\n")
        write(self.project / "tests" / "test_app_core.py", "def test_ok():\n    assert True\n")
        self.bin = self.project / ".venv" / ("Scripts" if os.name == "nt" else "bin")
        # no tool on PATH counts: the fixture decides what is installed
        self.no_path = mock.patch.object(checklist, "which", lambda name: None)
        self.no_path.start()

    def tearDown(self):
        self.no_path.stop()
        self._tmp.cleanup()

    def tools(self, ruff: int = 0, mypy: int | None = 0, pytest: int = 0):
        make_tool(self.bin, "ruff", ruff, "ruff: 3 problems" if ruff else "All checks passed!")
        if mypy is not None:
            make_tool(self.bin, "mypy", mypy, "Found 1 error" if mypy else "Success: no issues found")
        make_tool(self.bin, "pytest", pytest, "1 failed" if pytest else "1 passed")

    def run_checklist(self, *extra: str) -> tuple[int, dict]:
        code, out = run_main(checklist.main, [str(self.project), "--all-files", "--json", *extra])
        return code, json.loads(out)

    @staticmethod
    def by_category(report: dict) -> dict[str, dict]:
        return {r["category"]: r for r in report["results"]}

    def test_lint_failure_is_advisory(self):
        self.tools(ruff=1)
        code, report = self.run_checklist()
        self.assertEqual(0, code)
        cats = self.by_category(report)
        self.assertEqual("failed", cats["lint"]["status"])
        self.assertFalse(cats["lint"]["required"])
        self.assertEqual("passed", cats["types"]["status"])
        self.assertEqual("passed", cats["tests"]["status"])
        self.assertIn("Lint (ruff)", report["advisory_findings"])

    def test_strict_makes_advisory_fail(self):
        self.tools(ruff=1)
        code, report = self.run_checklist("--strict")
        self.assertEqual(1, code)
        self.assertFalse(report["success"])

    def test_failing_tests_are_required(self):
        self.tools(pytest=1)
        code, report = self.run_checklist()
        self.assertEqual(1, code)
        self.assertEqual(["Tests (pytest)"], report["required_failures"])

    def test_type_errors_are_required(self):
        self.tools(mypy=1)
        code, report = self.run_checklist()
        self.assertEqual(1, code)
        self.assertIn("Type check (mypy)", report["required_failures"])

    def test_missing_tool_is_a_note_not_a_failure(self):
        self.tools(mypy=None)
        code, report = self.run_checklist()
        self.assertEqual(0, code)
        types = self.by_category(report)["types"]
        self.assertEqual("missing", types["status"])
        self.assertIn(types["name"], report["not_verified"])

    def test_quick_has_no_security_or_audits_and_full_adds_them(self):
        self.tools()
        quick = checklist.build_steps(self.project, "quick", None)
        self.assertFalse({s.category for s in quick} & {"security", "audit"})
        full = checklist.build_steps(self.project, "full", None)
        cats = {s.category: s for s in full}
        self.assertIn("security", cats)
        self.assertTrue(cats["security"].required)
        audits = [s for s in full if s.category == "audit"]
        self.assertTrue(audits)
        self.assertFalse(any(s.required for s in audits), "audits are advisory")

    def test_empty_change_set_skips_everything(self):
        self.tools()
        steps = checklist.build_steps(self.project, "quick", [])
        self.assertTrue(all(s.skip_reason for s in steps), [(s.name, s.skip_reason) for s in steps])
        results = validation_runner.execute(steps)
        self.assertTrue(validation_runner.suite_success(results))
        self.assertEqual([], validation_runner.not_run(results))

    def test_changed_files_scope_the_linter(self):
        self.tools()
        steps = checklist.build_steps(self.project, "quick", ["app_core.py", "README.md"])
        lint = next(s for s in steps if s.category == "lint")
        self.assertEqual(["check", "app_core.py"], lint.commands[0][1:])
        types = next(s for s in steps if s.category == "types")
        self.assertEqual(["app_core.py"], types.commands[0][1:])

    def test_usage_error_exit_2(self):
        code, _ = run_main(checklist.main, [str(self.project / "does-not-exist")])
        self.assertEqual(2, code)

    def test_git_changed_files(self):
        if not shutil.which("git"):
            self.skipTest("git not installed")
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@t"}

        def git(*args):
            subprocess.run(["git", *args], cwd=self.project, check=True, capture_output=True, env=env)

        git("init", "-q")
        git("add", "-A")
        git("commit", "-qm", "init")
        with mock.patch.object(checklist, "which", shutil.which):
            self.assertEqual([], checklist.git_changed_files(self.project))
            (self.project / "app_core.py").write_text("x = 1\n", "utf-8")
            write(self.project / "new_module.py", "y = 2\n")
            self.assertEqual(["app_core.py", "new_module.py"], checklist.git_changed_files(self.project))
        self.assertIsNone(checklist.git_changed_files(Path(self._tmp.name)), "outside a repo -> None")


class RunnerTests(unittest.TestCase):
    def test_required_vs_advisory(self):
        adv = validation_runner.CheckResult("a", "lint", "failed", required=False)
        req = validation_runner.CheckResult("b", "tests", "failed", required=True)
        self.assertTrue(validation_runner.suite_success([adv]))
        self.assertFalse(validation_runner.suite_success([adv], strict=True))
        self.assertFalse(validation_runner.suite_success([adv, req]))

    def test_step_statuses_and_timing(self):
        ok = validation_runner.Step("ok", "tests", [[sys.executable, "-c", "print('3 passed')"]], required=True)
        bad = validation_runner.Step("bad", "tests", [[sys.executable, "-c", "import sys; sys.exit(1)"]], required=True)
        broken = validation_runner.Step("broken", "audit", [[sys.executable, "-c", "import sys; sys.exit(2)"]], kit_script=True)
        gone = validation_runner.Step("gone", "types", [["definitely-not-a-real-tool-xyz"]], required=True)
        results = validation_runner.execute([ok, bad, broken, gone])
        self.assertEqual(["passed", "failed", "error", "missing"], [r.status for r in results])
        self.assertEqual("3 passed", results[0].detail)
        self.assertGreaterEqual(results[0].duration_seconds, 0)
        table = validation_runner.summary_table(results)
        self.assertIn("FAIL", table)
        self.assertIn("ERROR", table)

    def test_required_timeout_fails(self):
        slow = validation_runner.Step("slow", "tests", [[sys.executable, "-c", "import time; time.sleep(5)"]],
                                      required=True, timeout=1)
        result = validation_runner.run_step(slow)
        self.assertEqual("failed", result.status)
        self.assertIn("timed out", result.detail)


# ---------------------------------------------------------------------------------------------
# css_audit.py and naming_check.py: advisory by default, --strict fails
# ---------------------------------------------------------------------------------------------
class CssAuditTests(unittest.TestCase):
    def test_parse_colour_regressions(self):
        # str.rstrip("!important") takes a character set and turned "#7a7a7a" into "#7a7a7".
        for value, expect in (("#7a7a7a", (0.478, 0.478, 0.478)), ("#1a2b3a", (0.102, 0.169, 0.227)),
                              ("#000 !important", (0.0, 0.0, 0.0))):
            got = css_audit.parse_color(value)
            self.assertIsNotNone(got, value)
            for a, b in zip(got, expect):
                self.assertAlmostEqual(a, b, places=2, msg=value)
        self.assertIsNone(css_audit.parse_color("rgba(0, 0, 0, 0.5)"), "translucent colours are not judged")

    def test_theming_is_not_collision_but_real_defects_are_found(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "tokens.css", """
                :root { --text: #1a1d23; --bg: #ffffff; }
                .dark { --text: #e8ecf1; --bg: #12151b; }
                @media (prefers-color-scheme: dark) { :root { --text: #e8ecf1; } }
            """)
            write(root / "ok.css", ".card { color: var(--text); background: var(--bg); }\n")
            self.assertEqual([], css_audit.audit(root))
            write(root / "later.css", """
                :root { --text: #14171d; }
                .pill { color: var(--nothing-defines-this); }
                .bad { color: #8a929e; background-color: #a7aeb8; }
            """)
            kinds = {f.kind for f in css_audit.audit(root)}
            self.assertTrue({"token-collision", "undefined-var", "contrast"} <= kinds, kinds)

    def test_important_is_a_warning_with_location_unless_strict(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "src" / "card.css", ".card { padding: 1rem; }\n.card-title { color: #111111 !important; }\n")
            found = [f for f in css_audit.audit(root) if f.kind == "important"]
            self.assertEqual(1, len(found))
            self.assertEqual(("warn", "src/card.css", 2), (found[0].severity, found[0].file, found[0].line))
            self.assertEqual(0, run_main(css_audit.main, [str(root)])[0], "advisory by default")
            strict = [f for f in css_audit.audit(root, strict=True) if f.kind == "important"]
            self.assertEqual("error", strict[0].severity)
            self.assertEqual(1, run_main(css_audit.main, [str(root), "--strict"])[0])

    def test_justified_and_reduced_motion_important(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "a.css", """
                @media (prefers-reduced-motion: reduce) {
                  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
                }
                /* third-party widget sets an inline width we cannot configure */
                .widget { width: 100% !important; }
            """)
            found = [f for f in css_audit.audit(root, strict=True) if f.kind == "important"]
            self.assertEqual(["note"], [f.severity for f in found])
            self.assertEqual(0, run_main(css_audit.main, [str(root), "--strict"])[0])

    def test_vendor_generated_modules_and_tailwind_are_not_false_positives(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "package.json", '{"devDependencies": {"tailwindcss": "4.1.0"}}')
            write(root / "src" / "app.css", """
                @import "tailwindcss";
                @theme { --color-brand: oklch(0.6 0.2 250); --font-display: "Inter", sans-serif; }
                .title { color: var(--color-red-500); font-family: var(--font-display); }
                .chip { background: var(--tw-gradient-from); }
                .bar { width: var(--progress); }
            """)
            write(root / "src" / "index.html", '<div class="bar" style="--progress: 40%"></div>\n')
            write(root / "src" / "a.module.css", ".root { color: #111111; }\n")
            write(root / "src" / "b.module.css", ".root { color: #222222; }\n")
            for vendor in ("node_modules/lib/x.css", "vendor/pkg/y.css", "dist/z.css", "public/build/w.css",
                           "assets/app.min.css"):
                write(root / vendor, ".x { color: var(--undefined) !important; }\n")
            write(root / "public" / "bootstrap.css", "/*! Bootstrap v5.3.3 | MIT License */\n.btn { color: var(--nope) !important; }\n")
            self.assertEqual([], [f"{f.kind} {f.file}" for f in css_audit.audit(root)])

    def test_project_under_a_build_folder_is_still_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "build" / "client-site"
            write(root / "site.css", ".x { color: var(--missing-token); }\n")
            self.assertEqual(["undefined-var"], [f.kind for f in css_audit.audit(root)])

    def test_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "a.css", ".a { color: red !important; }\n")
            code, out = run_main(css_audit.main, [str(root), "--json"])
            data = json.loads(out)
            self.assertEqual((0, 1), (code, data["warnings"]))


class NamingCheckTests(unittest.TestCase):
    def test_advisory_by_default_strict_fails_on_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "src" / "utils.ts", "export const formatInvoiceTotal = 1;\n")
            findings = naming_check.run(root)
            self.assertEqual(["generic-filename"], [f.check for f in findings if f.severity == "error"])
            self.assertEqual(0, run_main(naming_check.main, [str(root)])[0])
            self.assertEqual(1, run_main(naming_check.main, [str(root), "--strict"])[0])

    def test_conventions_are_not_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "src" / "invoices" / "types.ts", "export type InvoiceRow = {};\n")
            write(root / "src" / "invoices" / "utils.ts", "export const invoiceTotal = 1;\n")
            write(root / "app" / "a" / "page.tsx", "export default function Page() {}\n")
            write(root / "app" / "b" / "page.tsx", "export default function Page() {}\n")
            write(root / "src" / "a.module.css", ".root { color: red; }\n")
            write(root / "src" / "b.module.css", ".root { color: blue; }\n")
            write(root / "src" / "app.css", "@theme { --spacing: 0.25rem; }\n:root { --background: white; --radius: 4px; }\n")
            write(root / "tests" / "Feature" / "UserTest.php", "<?php\n")
            write(root / "tests" / "Unit" / "UserTest.php", "<?php\n")
            write(root / "node_modules" / "x" / "utils.js", "export const data = 1;\n")
            self.assertEqual([], [f"{f.check} {f.file}" for f in naming_check.run(root)])

    def test_duplicate_global_class_and_generic_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "css" / "header.css", ".nav-link { color: red; }\n")
            write(root / "css" / "footer.css", ".nav-link { color: blue; }\n")
            write(root / "src" / "orders.ts", "export const data = [];\n")
            checks = {f.check for f in naming_check.run(root)}
            self.assertTrue({"duplicate-class", "generic-export"} <= checks, checks)


# ---------------------------------------------------------------------------------------------
# ui_verify.py
# ---------------------------------------------------------------------------------------------
PNG_1X1 = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
    "890000000a49444154789c6300010000050001" "0d0a2db4" "0000000049454e44ae426082")


def fake_png(path: Path, width: int, salt: bytes = b"") -> None:
    data = bytearray(PNG_1X1)
    data[16:20] = width.to_bytes(4, "big")
    path.write_bytes(bytes(data) + salt)


class UiVerifyTests(unittest.TestCase):
    def verdict(self, d: Path, **extra):
        payload = {"route": "/x", "widths": [390, 1440], "consoleErrors": 0, "failedRequests": 0, "status": "pass"}
        payload.update(extra)
        (d / "verdict.json").write_text(json.dumps(payload), "utf-8")

    def test_rejects_one_capture_reported_as_many_widths(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            for name in ("after-1440.png", "after-390.png", "after-768.png"):
                fake_png(d / name, 1440)
            self.verdict(d, widths=[390, 768, 1440])
            got = ui_verify.verify(d, (390, 768, 1440))
            self.assertEqual("fail", got["status"])
            joined = " ".join(got["issues"])
            self.assertIn("identical image", joined)
            self.assertIn("not taken at the width it reports", joined)

    def test_real_verification_passes_with_default_and_hidpi_widths(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            fake_png(d / "after-390.png", 780, b"\x01")         # 2x mobile capture
            fake_png(d / "after-1440.png", 1800, b"\x02")       # 1.25x Windows scaling
            self.verdict(d)
            self.assertEqual("pass", ui_verify.verify(d)["status"])
            self.assertEqual(0, run_main(ui_verify.main, [str(d)])[0])

    def test_honest_skip_exits_zero_and_bare_skip_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            self.verdict(d, status="skipped", reason="no dev server running")
            self.assertEqual("skipped", ui_verify.verify(d)["status"])
            self.assertEqual(0, run_main(ui_verify.main, [str(d)])[0])
            self.verdict(d, status="skipped")
            self.assertEqual(1, run_main(ui_verify.main, [str(d)])[0])

    def test_missing_directory_fails(self):
        self.assertEqual("fail", ui_verify.verify(Path(tempfile.gettempdir()) / "agkit-no-such-dir")["status"])


# ---------------------------------------------------------------------------------------------
# Skill scripts (owned by the skills; kept here as regression tests while their APIs hold)
# ---------------------------------------------------------------------------------------------
class SkillScriptRegressionTests(unittest.TestCase):
    def need(self, module, name: str):
        if module is None:
            self.skipTest(f"{name} not present")

    def test_security_scanner_ignores_patterns_inside_strings(self):
        self.need(security_scan, "security_scan.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sample.py").write_text("PATTERN = r'eval\\s*\\('\nTOKEN = 'YOUR_API_KEY'\n", "utf-8")
            report = security_scan.run_full_scan(str(root), "all")
            self.assertEqual(0, report["summary"]["critical"])
            self.assertEqual(0, report["summary"]["high"])

    def test_security_scanner_detects_executable_eval_and_secret(self):
        self.need(security_scan, "security_scan.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_key = "sk_live_" + "12345678901234567890"
            (root / "bad.py").write_text(f"api_key = '{fake_key}'\neval(user_input)\n", "utf-8")
            report = security_scan.run_full_scan(str(root), "all")
            self.assertGreaterEqual(report["summary"]["critical"], 1)
            self.assertGreaterEqual(report["summary"]["high"], 1)
            self.assertTrue(security_scan._should_fail(report, "high"))

    def test_dependency_analyzer_flags_missing_lock(self):
        self.need(dependency_analyzer, "dependency_analyzer.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"dependencies":{"demo":"latest"}}', "utf-8")
            issues = {item["issue"] for item in dependency_analyzer.analyze(root)["findings"]}
            self.assertIn("Missing JavaScript lock file", issues)
            self.assertIn("Unbounded dependency version", issues)

    def test_bundle_analyzer_flags_oversized_asset(self):
        self.need(bundle_analyzer, "bundle_analyzer.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            asset = root / "dist" / "app.js"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"x" * 2048)
            report = bundle_analyzer.analyze(root, file_warn_kib=1, file_fail_kib=2, total_fail_kib=100)
            self.assertTrue(report["findings"])
            self.assertEqual("high", report["findings"][0]["severity"])

    def test_react_checker_ignores_generated_next_output(self):
        self.need(react_performance, "react_performance_checker.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            web = root / "web"
            source, generated = web / "src" / "app", web / ".next" / "types"
            source.mkdir(parents=True)
            generated.mkdir(parents=True)
            (web / "package.json").write_text('{"dependencies":{"next":"16.2.10","react":"19.2.3"}}', "utf-8")
            (source / "page.tsx").write_text("export default function Page(){return <main><h1>Safe</h1></main>}\n", "utf-8")
            (generated / "page.ts").write_text("async function generated(){await one();\nawait two();}\n", "utf-8")
            checker = react_performance.PerformanceChecker(str(root))
            scanned = {path.resolve() for path in checker._iter_files(["ts", "tsx"])}
            self.assertIn((source / "page.tsx").resolve(), scanned)
            self.assertNotIn((generated / "page.ts").resolve(), scanned)



# ---------------------------------------------------------------------------------------------
# proplan_check.py: stages, milestone detection, review blockers, row definitions
# ---------------------------------------------------------------------------------------------
proplan_check = load_optional("agkit_proplan_check", "scripts/proplan_check.py")
POS_LITE = TOOLKIT / "skills" / "proplan" / "example" / "pos-lite"


class ProplanCheckTests(unittest.TestCase):
    def setUp(self):
        if proplan_check is None or not POS_LITE.is_dir():
            self.skipTest("proplan_check.py or the pos-lite example is not present")
        self._tmp = tempfile.TemporaryDirectory()
        self.plan = Path(self._tmp.name) / "cafe-pos"
        shutil.copytree(POS_LITE, self.plan)

    def tearDown(self):
        self._tmp.cleanup()

    def append(self, name: str, text: str) -> None:
        path = self.plan / name
        path.write_text(path.read_text("utf-8") + "\n" + textwrap.dedent(text).lstrip("\n"), "utf-8")

    def findings(self, stage: str = "final", severity: str = "error"):
        rep, _stats = proplan_check.run(self.plan, None, False, stage)
        return [f for f in rep.findings if f.severity == severity]

    def test_copy_of_example_passes(self):
        self.assertEqual([], self.findings())

    def test_design_stage_skips_later_files_tasks_and_risks(self):
        (self.plan / "10-roadmap.md").unlink()
        (self.plan / "TRACEABILITY.md").unlink()
        self.append("03-architecture.md", "Mitigation lands in T-050 and RK-09.\n")
        final = {f.code for f in self.findings("final")}
        self.assertTrue({"file.missing", "trace.must_task", "id.dangling"} <= final, final)
        self.assertEqual([], self.findings("design"))

    def test_design_stage_still_catches_dangling_requirements(self):
        (self.plan / "10-roadmap.md").unlink()
        (self.plan / "TRACEABILITY.md").unlink()
        self.append("03-architecture.md", "This also serves R-099.\n")
        self.assertEqual({"id.dangling"}, {f.code for f in self.findings("design")})

    def test_bare_m_token_in_prose_is_not_a_milestone(self):
        self.append("03-architecture.md", "The developer tests on an Apple M4 laptop and an M9 chip.\n")
        self.assertEqual([], self.findings())

    def test_milestone_near_word_heading_or_cell_is_checked(self):
        for text in ("This ships in milestone M9.\n", "## M9 extras\n\nText.\n",
                     "| Item | When |\n|---|---|\n| Loyalty | M9 |\n"):
            with self.subTest(text=text.splitlines()[0]):
                shutil.rmtree(self.plan)
                shutil.copytree(POS_LITE, self.plan)
                self.append("03-architecture.md", text)
                msgs = [f.message for f in self.findings() if f.code == "id.dangling"]
                self.assertTrue(any("M9" in m for m in msgs), msgs)

    def test_review_blocker_status_starting_with_open(self):
        write(self.plan / "REVIEW.md", """
            ---
            doc: REVIEW
            project: cafe-pos
            version: 1.0.0
            status: in-review
            ---

            # Review

            ## Findings

            | ID | Severity | Check | Where | Finding | Fix | Status |
            |---|---|---|---|---|---|---|
            | RV-01 | Blocker | contradictions | 02 | Two refund rules | Pick one | Open (waiting on client) |
            | RV-02 | Blocker | scope | 02 | Loyalty creep | Cut it | fixed in 1.0.1 |
            """)
        blockers = [f for f in self.findings() if f.code == "review.blocker"]
        self.assertEqual(["RV-01"], [f.message.split()[0] for f in blockers])

    def test_citation_table_outside_home_is_not_a_definition(self):
        self.append("03-architecture.md", """
            ## Requirement to container map

            | Requirement | Container |
            |---|---|
            | R-001 | API |
            | R-002 | PWA |
            """)
        self.assertEqual([], self.findings())

    def test_id_header_table_outside_home_is_a_definition(self):
        self.append("03-architecture.md", """
            ## Extra requirements

            | ID | Requirement |
            |---|---|
            | R-001 | Duplicate of the sign-in requirement |
            """)
        self.assertIn("id.home", {f.code for f in self.findings()})

    def test_summary_table_in_home_document_does_not_duplicate_headings(self):
        self.append("02-requirements.md", """
            ## Summary

            | Requirement | Priority |
            |---|---|
            | R-001 | Must |
            """)
        self.assertNotIn("id.duplicate", {f.code for f in self.findings()})

    def test_cli_stage_flag(self):
        (self.plan / "10-roadmap.md").unlink()
        (self.plan / "TRACEABILITY.md").unlink()
        code, out = run_main(proplan_check.main, [str(self.plan), "--stage", "design"])
        self.assertEqual(0, code, out)
        self.assertIn("stage: design", out)
        code, _ = run_main(proplan_check.main, [str(self.plan)])
        self.assertEqual(1, code)


if __name__ == "__main__":
    unittest.main()
