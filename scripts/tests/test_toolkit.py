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
            (root / "bad.py").write_text(
                """api_key = 'sk_live_12345678901234567890'
eval(user_input)
""",
                "utf-8",
            )  # agkit: allow-secret
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
        is_repo = (TOOLKIT / "install.ps1").is_file() or (TOOLKIT / ".git").is_dir()
        legacy_dirs = ("workflows", "agent") if is_repo else ("rules", "workflows", "agent")
        for legacy in legacy_dirs:
            self.assertFalse((TOOLKIT / legacy).exists(), f"{legacy}/ must not exist in the plugin")

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

    def test_every_agent_has_imperative_read_now_line_with_resolvable_paths(self):
        for agent in (TOOLKIT / "agents").glob("*.md"):
            body = agent.read_text("utf-8")
            with self.subTest(agent=agent.name):
                self.assertIn("**Read now**", body, "agent must tell the model to read its skills, not rely on YAML")
                m = re.search(r"^\*\*Read now\*\*.*$", body, re.M)
                self.assertIsNotNone(m, "Read now line missing")
                paths = re.findall(r"`" + re.escape(self.KIT_PREFIX) + r"(skills/[^`]+)`", m.group(0))
                self.assertTrue(paths, "Read now line has no skill paths")
                for rel in paths:
                    self.assertTrue((TOOLKIT / rel).exists(), f"Read now path does not resolve: {rel}")
                # Read now must match the frontmatter skills list exactly (no drift)
                raw = validate_kit.extract_frontmatter(body)
                fm = validate_kit.normalize_list(validate_kit.fallback_frontmatter(raw).get("skills"))
                listed = [Path(r).parts[1] for r in paths]
                self.assertEqual(listed, fm, "Read now paths drifted from frontmatter skills")

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
