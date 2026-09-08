from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

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


validate_kit = load_module("agkit_validate_kit", SCRIPTS / "validate_kit.py")
security_scan = load_module("agkit_security_scan", TOOLKIT / "skills/vulnerability-scanner/scripts/security_scan.py")
dependency_analyzer = load_module("agkit_dependency_analyzer", TOOLKIT / "skills/vulnerability-scanner/scripts/dependency_analyzer.py")
bundle_analyzer = load_module("agkit_bundle_analyzer", TOOLKIT / "skills/performance-profiling/scripts/bundle_analyzer.py")
validation_runner = load_module("agkit_validation_runner", SCRIPTS / "validation_runner.py")
geo_checker = load_module("agkit_geo_checker", TOOLKIT / "skills/seo-fundamentals/scripts/geo_checker.py")
react_performance = load_module(
    "agkit_react_performance",
    TOOLKIT / "skills/nextjs-react-expert/scripts/react_performance_checker.py",
)


class ToolkitRegressionTests(unittest.TestCase):
    def test_toolkit_self_validation_passes(self):
        findings = validate_kit.validate(TOOLKIT)
        errors = [item for item in findings if item.severity == "error"]
        self.assertEqual([], errors)

    def test_security_scanner_ignores_patterns_inside_strings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sample.py").write_text(
                """PATTERN = r'eval\\s*\\('
TOKEN = 'YOUR_API_KEY'
""",
                "utf-8",
            )
            report = security_scan.run_full_scan(str(root), "all")
            self.assertEqual(0, report["summary"]["critical"])
            self.assertEqual(0, report["summary"]["high"])

    def test_security_scanner_detects_executable_eval_and_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_key = "sk_live_" + "12345678901234567890"
            (root / "bad.py").write_text(
                f"api_key = '{fake_key}'\neval(user_input)\n",
                "utf-8",
            )
            report = security_scan.run_full_scan(str(root), "all")
            self.assertGreaterEqual(report["summary"]["critical"], 1)
            self.assertGreaterEqual(report["summary"]["high"], 1)
            self.assertTrue(security_scan._should_fail(report, "high"))

    def test_security_scanner_detects_nested_nextjs_header_configuration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"private":true}', "utf-8")
            web = root / "web"
            web.mkdir()
            (web / "next.config.ts").write_text(
                'const headers = [{ key: "Content-Security-Policy", value: "frame-ancestors \'none\'" }];',
                "utf-8",
            )
            report = security_scan.run_full_scan(str(root), "config")
            config = report["scans"]["configuration"]
            self.assertTrue(config["checks"]["security_headers_config"])
            self.assertFalse(any("security-header" in item.get("issue", "") for item in config["findings"]))

    def test_dependency_analyzer_flags_missing_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"dependencies":{"demo":"latest"}}', "utf-8")
            report = dependency_analyzer.analyze(root)
            issues = {item["issue"] for item in report["findings"]}
            self.assertIn("Missing JavaScript lock file", issues)
            self.assertIn("Unbounded dependency version", issues)

    def test_bundle_analyzer_flags_oversized_asset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            asset = root / "dist" / "app.js"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"x" * 2048)
            report = bundle_analyzer.analyze(root, file_warn_kib=1, file_fail_kib=2, total_fail_kib=100)
            self.assertTrue(report["findings"])
            self.assertEqual("high", report["findings"][0]["severity"])

    def test_geo_checker_follows_localized_mdx_and_skips_layouts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            route = root / "web" / "src" / "app" / "docs" / "demo"
            route.mkdir(parents=True)
            (route / "page.tsx").write_text(
                'import En from "./content.en.mdx";\n'
                'import Vi from "./content.vi.mdx";\n'
                'export default function Page(){ return <En />; }\n',
                "utf-8",
            )
            (route / "content.en.mdx").write_text(
                "# Demo\n\n## Overview\nText.\n\n## Usage\nText.\n",
                "utf-8",
            )
            (route / "content.vi.mdx").write_text(
                "# Trình diễn\n\n## Tổng quan\nNội dung.\n\n## Sử dụng\nNội dung.\n",
                "utf-8",
            )
            (route.parent / "layout.tsx").write_text(
                "export default function Layout({children}){return <div>{children}</div>}\n",
                "utf-8",
            )

            pages = geo_checker.find_web_pages(root)
            self.assertEqual([route / "page.tsx"], pages)
            result = geo_checker.check_page(route / "page.tsx", root)
            self.assertGreaterEqual(result["score"], 60)
            self.assertFalse(any("Multiple H1" in issue for issue in result["issues"]))

    def test_react_checker_ignores_generated_next_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            web = root / "web"
            source = web / "src" / "app"
            generated = web / ".next" / "types"
            source.mkdir(parents=True)
            generated.mkdir(parents=True)
            (web / "package.json").write_text(
                '{"dependencies":{"next":"16.2.10","react":"19.2.3"}}',
                "utf-8",
            )
            (source / "page.tsx").write_text(
                "export default function Page(){return <main><h1>Safe</h1></main>}\n",
                "utf-8",
            )
            (generated / "page.ts").write_text(
                "async function generated(){await one();\nawait two();}\n",
                "utf-8",
            )

            checker = react_performance.PerformanceChecker(str(root))
            # Resolve paths: macOS temp dirs use /var -> /private/var symlinks.
            scanned = {path.resolve() for path in checker._iter_files(["ts", "tsx"])}
            self.assertIn((source / "page.tsx").resolve(), scanned)
            self.assertNotIn((generated / "page.ts").resolve(), scanned)
            self.assertTrue(checker.run())
            self.assertEqual([], checker.issues)

    def test_no_legacy_directories(self):
        for legacy in ("workflows", "agent"):
            self.assertFalse((TOOLKIT / legacy).exists(), f"{legacy}/ must not exist in the toolkit")
        # In the installed plugin directory, rules live in ~/.gemini/config/rules, not inside the plugin.
        # In the source repository, rules/ holds the source files distributed by install.ps1.
        if not (TOOLKIT / ".git").exists():
            self.assertFalse((TOOLKIT / "rules").exists(), "rules/ must not exist in the installed plugin directory")

    def test_every_agent_skill_reference_resolves(self):
        skills = {p.name for p in (TOOLKIT / "skills").iterdir() if p.is_dir()}
        for agent in (TOOLKIT / "agents").glob("*.md"):
            raw = validate_kit.extract_frontmatter(agent.read_text("utf-8"))
            self.assertIsNotNone(raw, agent.name)
            data = validate_kit.fallback_frontmatter(raw)
            for skill in validate_kit.normalize_list(data.get("skills")):
                with self.subTest(agent=agent.name, skill=skill):
                    self.assertIn(skill, skills)

    # --- procedural spine: the failures observed in use (rules not reaching the model) ---
    KIT_PREFIX = "C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/"

    def _rules_dir(self):
        # global rules live beside the plugin: ~/.gemini/config/rules (dev checkout: ../global/rules)
        for cand in (TOOLKIT.parent / "global" / "rules", Path.home() / ".gemini" / "config" / "rules"):
            if (cand / "core-protocol.md").exists():
                return cand
        self.skipTest("global rules directory not found")

    AGENT_HEADINGS = [
        "## Own",
        "## Build (new work)",
        "## Repair (existing work that is wrong)",
        "## Decide",
        "## Never",
        "## Done",
    ]
    BANNED_AGENT_PHRASES = ("the agent should", "consider ", "try to", "it is recommended", "you might")
    BIG_BUILDER_AGENTS = {"frontend-specialist.md", "mobile-developer.md", "backend-specialist.md"}

    @staticmethod
    def _skill_paths(line: str):
        # Agents abbreviate after the first path: `.../skills/<name>/...` or full prefix.
        return re.findall(r"skills/([\w-]+)/", line)

    def test_every_agent_follows_v22_skeleton(self):
        for agent in (TOOLKIT / "agents").glob("*.md"):
            body = agent.read_text("utf-8")
            # strip fenced blocks so template ## lines inside examples do not count as headings
            outside = re.sub(r"```.*?```", "", body, flags=re.S)
            headings = [ln.strip() for ln in outside.splitlines() if ln.startswith("## ")]
            with self.subTest(agent=agent.name):
                self.assertEqual(headings, self.AGENT_HEADINGS, "six headings, exact text, in order")

    def test_every_agent_read_lines_resolve_and_match_frontmatter(self):
        for agent in (TOOLKIT / "agents").glob("*.md"):
            body = agent.read_text("utf-8")
            with self.subTest(agent=agent.name):
                now = re.search(r"^\*\*Read now:\*\*(.*)$", body, re.M)
                self.assertIsNotNone(now, "missing '**Read now:**' line")
                now_skills = self._skill_paths(now.group(1))
                self.assertTrue(1 <= len(now_skills) <= 3, "Read now names 1-3 skills")
                for s in now_skills:
                    self.assertTrue((TOOLKIT / "skills" / s / "SKILL.md").exists(), f"Read now skill missing: {s}")
                fm = validate_kit.normalize_list(
                    validate_kit.fallback_frontmatter(validate_kit.extract_frontmatter(body)).get("skills"))
                self.assertEqual(now_skills, fm, "Read now must equal frontmatter skills, in order")
                when = re.search(r"^\*\*Read when:\*\*(.*)$", body, re.M)
                if when:
                    for ref in re.findall(r"`([^`]*skills/[^`]+)`", when.group(1)):
                        rel = ref.split("ag-kit-v2/")[-1] if "ag-kit-v2/" in ref else ref
                        rel = rel.lstrip(". /")
                        self.assertTrue((TOOLKIT / rel).exists(), f"Read when path does not resolve: {ref}")

    def test_agents_within_size_cap(self):
        # 8K for the three big builders, 7K for the orchestrator (holds the canonical
        # ownership table), 6K for the rest.
        for agent in (TOOLKIT / "agents").glob("*.md"):
            if agent.name in self.BIG_BUILDER_AGENTS:
                cap = 8000
            elif agent.name == "orchestrator.md":
                cap = 7000
            else:
                cap = 6000
            with self.subTest(agent=agent.name):
                self.assertLessEqual(agent.stat().st_size, cap, f"{agent.name} over {cap}B")

    def test_agents_use_imperative_voice(self):
        for agent in (TOOLKIT / "agents").glob("*.md"):
            low = agent.read_text("utf-8").lower()
            for phrase in self.BANNED_AGENT_PHRASES:
                with self.subTest(agent=agent.name, phrase=phrase):
                    self.assertNotIn(phrase, low, f"banned phrasing '{phrase.strip()}'")

    def test_no_prose_duplicated_across_skill_files(self):
        # Catches the React-Compiler-paragraph class of token waste: the same long prose run
        # copied into more than one SKILL.md. Scoped to skills (agents share the v2.2 skeleton
        # by design, which the skeleton + size-cap tests already constrain). A 24-word run is
        # long enough that shared pointers and one-line rules do not trip it, but a copied paragraph does.
        # Command wrappers (description starts with "/") legitimately mirror the steps and
        # report format of the skill they wrap; exclude them and compare content skills only.
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
        self.assertEqual(dupes, [], f"duplicated prose across skills: {sorted(set(dupes))[:5]}")

    # A skill core an agent loads on every task is L2, capped at 8 KB by the architecture so that
    # depth lives in Read-when sub-files. This is a RATCHET, not a flat cap: a core already over
    # 8 KB is pinned at its current size, so it can shrink but never grow, and the debt stays
    # visible. Splitting one is a normal change — lower its number here in the same commit.
    L2_CAP = 8000
    L2_PINNED = {
        # skill: (max bytes, why it is not 8 KB yet)
        "frontend-design": (13300, "judgment is the product here (§0.C read, §0.F screen read, "
                                   "§4.0, §4.7 copy); five sub-files already split out"),
        "browser-verification": (9900, "carries the anti-fabrication contract (ui_verify) and the "
                                 "disqualifier list; troubleshooting.md and computed-styles.md split out"),
        "tailwind-patterns": (8200, "owed a split"),
        "api-patterns": (8400, "owed a split"),
        "nodejs-best-practices": (11300, "owed a split"),
        "testing-patterns": (9200, "owed a split"),
        "vulnerability-scanner": (10400, "owed a split"),
        "red-team-tactics": (8500, "owed a split"),
        "shell-ops": (8100, "owed a split"),
    }

    def test_read_now_skill_cores_do_not_grow(self):
        read_now = set()
        for agent in (TOOLKIT / "agents").glob("*.md"):
            line = re.search(r"^\*\*Read now:\*\*(.*)$", agent.read_text("utf-8"), re.M)
            if line:
                read_now.update(self._skill_paths(line.group(1)))
        self.assertTrue(read_now, "no Read-now skills found")
        for skill in sorted(read_now):
            core = TOOLKIT / "skills" / skill / "SKILL.md"
            cap, why = self.L2_PINNED.get(skill, (self.L2_CAP, "L2 cap"))
            with self.subTest(skill=skill):
                self.assertLessEqual(
                    core.stat().st_size, cap,
                    f"{skill}/SKILL.md is {core.stat().st_size}B, over {cap}B ({why}) — "
                    "move depth into a Read-when sub-file, or lower the pin if you shrank it")

    def test_ui_verify_rejects_one_capture_reported_as_many_widths(self):
        """The observed failure: three viewports reported PASS from a single desktop capture."""
        ui_verify = load_module("agkit_ui_verify", SCRIPTS / "ui_verify.py")
        png = bytes.fromhex(  # 1x1 PNG, patched below to carry the width we want in its IHDR
            "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
            "890000000a49444154789c6300010000050001" "0d0a2db4" "0000000049454e44ae426082")

        def fake(path: Path, width: int, salt: bytes = b""):
            data = bytearray(png)
            data[16:20] = width.to_bytes(4, "big")
            path.write_bytes(bytes(data) + salt)

        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            # one 1440 capture, copied and renamed as the 390 and 768 "passes"
            for name in ("after-1440.png", "after-390.png", "after-768.png"):
                fake(d / name, 1440)
            (d / "verdict.json").write_text(json.dumps(
                {"route": "/x", "widths": [390, 768, 1440], "consoleErrors": 0,
                 "failedRequests": 0, "status": "pass"}), "utf-8")
            got = ui_verify.verify(d, (390, 768, 1440), False)
            self.assertEqual("fail", got["status"])
            joined = " ".join(got["issues"])
            self.assertIn("identical image", joined, "must catch one capture reused as several")
            self.assertIn("not taken at the width it reports", joined,
                          "must catch a screenshot whose pixels contradict its filename")

        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            for i, w in enumerate((390, 768, 1440)):
                fake(d / f"after-{w}.png", w, salt=bytes([i]))  # genuinely different files
            (d / "verdict.json").write_text(json.dumps(
                {"route": "/x", "widths": [390, 768, 1440], "consoleErrors": 0,
                 "failedRequests": 0, "status": "pass"}), "utf-8")
            self.assertEqual("pass", ui_verify.verify(d, (390, 768, 1440), False)["status"],
                             "a real three-width verification must not be flagged")

    def test_css_audit_parses_colours_and_separates_theming_from_collision(self):
        css_audit = load_module("agkit_css_audit", SCRIPTS / "css_audit.py")

        # Regression: str.rstrip("!important") takes a CHARACTER SET, so it ate trailing
        # a/i/m/n/o/p/r/t and turned "#7a7a7a" into "#7a7a7" — unparseable, so the contrast
        # check was silently skipped for a whole class of colours.
        for value, expect in (("#7a7a7a", (0.478, 0.478, 0.478)),
                              ("#1a2b3a", (0.102, 0.169, 0.227)),
                              ("#000 !important", (0.0, 0.0, 0.0))):
            got = css_audit.parse_color(value)
            self.assertIsNotNone(got, f"{value} must parse")
            for a, b in zip(got, expect):
                self.assertAlmostEqual(a, b, places=2, msg=f"{value} parsed wrong")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tokens.css").write_text(
                ":root { --text: #1a1d23; --bg: #ffffff; }\n"
                ".dark { --text: #e8ecf1; --bg: #12151b; }\n"
                "@media (prefers-color-scheme: dark) { :root { --text: #e8ecf1; } }\n", "utf-8")
            (root / "ok.css").write_text(".card { color: var(--text); background: var(--bg); }\n", "utf-8")
            kinds = {f.kind for f in css_audit.audit(root)}
            self.assertEqual(set(), kinds,
                             "theme redefinition under .dark / @media is not a collision")

            # the real defect: same token, different value, no theme selector in the chain
            (root / "later.css").write_text(
                ":root { --text: #14171d; }\n"
                ".pill { color: var(--nothing-defines-this); }\n"
                ".bad { color: #8a929e; background-color: #a7aeb8; }\n", "utf-8")
            found = css_audit.audit(root)
            kinds = {f.kind for f in found}
            for expected in ("token-collision", "undefined-var", "contrast"):
                self.assertIn(expected, kinds, f"must report {expected}")
            self.assertTrue(any(f.severity == "error" for f in found))

    def test_gate_policy_is_always_on(self):
        rules = self._rules_dir()
        fm = validate_kit.fallback_frontmatter(validate_kit.extract_frontmatter((rules / "code-rules.md").read_text("utf-8")))
        self.assertEqual(str(fm.get("trigger")), "always_on", "code-rules defines done; it cannot be model_decision")

    def test_always_on_spine_contains_literal_gate_commands(self):
        rules = self._rules_dir()
        spine = (rules / "core-protocol.md").read_text("utf-8")
        for needle in ("scripts/checklist.py", "/see", "/review", "Read the agent file", "plan line"):
            with self.subTest(needle=needle):
                self.assertIn(needle, spine, f"core-protocol must inline: {needle}")

    def test_required_checks_gate_only(self):
        ok = validation_runner.CheckResult("a", "c", "failed", required=False)
        bad = validation_runner.CheckResult("b", "c", "failed", required=True)
        self.assertTrue(validation_runner.suite_success([ok]))
        self.assertFalse(validation_runner.suite_success([ok, bad]))

    def test_runner_finds_embedded_toolkit_for_external_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            located = validation_runner.locate_toolkit_root(project, str(SCRIPTS / "checklist.py"))
            self.assertEqual(TOOLKIT, located)


if __name__ == "__main__":
    unittest.main()
