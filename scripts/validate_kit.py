#!/usr/bin/env python3
"""Self-validate the AG Kit v2 plugin.

Checks: JSON validity, frontmatter contracts (agents, skills), agent -> skill references,
skill/agent references inside markdown, absolute AG_KIT paths that must exist, local markdown
links, Python syntax, and leftover legacy patterns (.agents/agent/, "you have FAILED", ...).

Usage:
    python validate_kit.py            # validate the kit this script lives in
    python validate_kit.py --json
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - optional
    yaml = None

AG_KIT_URL_PREFIX = "C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
LEGACY_PATTERNS = {
    r"\.agents/agent/": "legacy path .agents/agent/ (use the absolute AG_KIT path)",
    r"\.agents/skills/": "legacy path .agents/skills/",
    r"\.agents/scripts/": "legacy path .agents/scripts/",
    r"you have FAILED": "banned phrasing",
    r"PROTOCOL VIOLATION": "banned phrasing",
    r"(?i)maestro rules?\b": "stale branding",
    r"Claude Write tool": "non-Antigravity tooling reference",
    r"minimum 3 (strategic )?questions": "removed question floor",
}


@dataclass
class Finding:
    severity: str
    code: str
    file: str
    line: int
    message: str


def add(findings: list[Finding], severity: str, code: str, path: Path, message: str, line: int = 1) -> None:
    findings.append(Finding(severity, code, path.as_posix(), line, message))


def extract_frontmatter(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    return text[4:end]


def fallback_frontmatter(raw: str) -> dict[str, object]:
    data: dict[str, object] = {}
    for line in raw.splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            key, value = match.groups()
            data[key] = value.strip().strip("\"'")
    return data


def parse_frontmatter(path: Path, rel: Path, findings: list[Finding]) -> dict[str, object] | None:
    raw = extract_frontmatter(path.read_text("utf-8", errors="replace"))
    if raw is None:
        add(findings, "error", "frontmatter.missing", rel, "Missing or unterminated YAML frontmatter")
        return None
    if yaml is None:
        return fallback_frontmatter(raw)
    try:
        data = yaml.safe_load(raw)
    except Exception as exc:  # noqa: BLE001
        add(findings, "error", "frontmatter.invalid_yaml", rel, str(exc))
        return None
    if not isinstance(data, dict):
        add(findings, "error", "frontmatter.not_mapping", rel, "Frontmatter must be a YAML mapping")
        return None
    return data


def normalize_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def validate_json(root: Path, findings: list[Finding]) -> None:
    for path in root.rglob("*.json"):
        if "__pycache__" in path.parts:
            continue
        try:
            json.loads(path.read_text("utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            add(findings, "error", "json.invalid", path.relative_to(root), str(exc), int(getattr(exc, "lineno", 1)))


def validate_version(root: Path, findings: list[Finding]) -> None:
    path = root / "VERSION"
    if not path.is_file():
        add(findings, "warning", "version.missing", Path("VERSION"), "VERSION file is missing")
        return
    value = path.read_text("utf-8").strip()
    if not re.fullmatch(r"\d{4}\.\d{1,2}\.\d{1,2}", value):
        add(findings, "warning", "version.format", Path("VERSION"), f"Expected YYYY.M.D, got {value!r}")


def validate_agents_and_skills(root: Path, findings: list[Finding]) -> tuple[set[str], set[str]]:
    agents: set[str] = set()
    skills: set[str] = set()
    skill_dirs = {p.name for p in (root / "skills").iterdir() if p.is_dir()}
    for skill_dir in sorted(skill_dirs):
        skill_md = root / "skills" / skill_dir / "SKILL.md"
        rel = skill_md.relative_to(root)
        if not skill_md.is_file():
            add(findings, "error", "skill.missing_skill_md", rel, "Skill directory without SKILL.md")
            continue
        data = parse_frontmatter(skill_md, rel, findings)
        if data is None:
            continue
        for field in ("name", "description"):
            if not data.get(field):
                add(findings, "error", "frontmatter.required_field", rel, f"Missing required field: {field}")
        if str(data.get("name", "")) != skill_dir:
            add(findings, "error", "frontmatter.name_mismatch", rel, f"name={data.get('name')!r}, expected {skill_dir!r}")
        if "version" in data and not SEMVER.match(str(data["version"])):
            add(findings, "warning", "frontmatter.version", rel, f"Non-semver version {data['version']!r}")
        desc = str(data.get("description", ""))
        if len(desc) < 40:
            add(findings, "warning", "skill.thin_description", rel, "Description should say what the skill does and when to use it")
        skills.add(skill_dir)

    for path in sorted((root / "agents").glob("*.md")):
        rel = path.relative_to(root)
        data = parse_frontmatter(path, rel, findings)
        if data is None:
            continue
        for field in ("name", "description", "skills"):
            if not data.get(field):
                add(findings, "error", "frontmatter.required_field", rel, f"Missing required field: {field}")
        if str(data.get("name", "")) != path.stem:
            add(findings, "error", "frontmatter.name_mismatch", rel, f"name={data.get('name')!r}, expected {path.stem!r}")
        if "Triggers on" not in str(data.get("description", "")):
            add(findings, "warning", "agent.no_triggers", rel, "Description should end with 'Triggers on: ...'")
        for skill in normalize_list(data.get("skills")):
            if skill not in skill_dirs:
                add(findings, "error", "reference.unknown_skill", rel, f"Agent references missing skill: {skill}")
        agents.add(path.stem)
    return agents, skills


def validate_markdown_references(root: Path, agents: set[str], skills: set[str], findings: list[Finding]) -> None:
    skill_ref = re.compile(r"@\[skills/([\w-]+)\]")
    agent_ref = re.compile(r"(?<![\w-])agents/([\w-]+)\.md")  # not inside e.g. parallel-agents/
    abs_ref = re.compile(re.escape(AG_KIT_URL_PREFIX) + r"([\w./-]+)")
    link = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for path in root.rglob("*.md"):
        text = path.read_text("utf-8", errors="replace")
        rel = path.relative_to(root)
        if path.parent == root:
            # Root-level docs (DECISIONS.md, CHANGES.md) describe legacy patterns; only check their links.
            for match in link.finditer(text):
                raw = match.group(1).strip().split()[0].strip("<>")
                if raw.startswith(("#", "http://", "https://", "mailto:", "C:/")):
                    continue
                target = (path.parent / unquote(raw.split("#", 1)[0])).resolve()
                if not target.exists():
                    add(findings, "error", "markdown.missing_link", rel, f"Missing local target: {raw}", text.count("\n", 0, match.start()) + 1)
            continue
        for match in skill_ref.finditer(text):
            if match.group(1) not in skills:
                add(findings, "error", "reference.unknown_skill", rel, f"Unknown skill @[skills/{match.group(1)}]", text.count("\n", 0, match.start()) + 1)
        for match in agent_ref.finditer(text):
            if match.group(1) not in agents:
                add(findings, "error", "reference.unknown_agent", rel, f"Unknown agent {match.group(1)}.md", text.count("\n", 0, match.start()) + 1)
        for match in abs_ref.finditer(text):
            target = root / match.group(1).rstrip(".,;:)`")
            if not target.exists():
                add(findings, "error", "reference.missing_path", rel, f"Absolute path does not exist: {match.group(1)}", text.count("\n", 0, match.start()) + 1)
        for match in link.finditer(text):
            raw = match.group(1).strip().split()[0].strip("<>")
            if raw.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:", "C:/")):
                continue
            target_text = unquote(raw.split("#", 1)[0])
            if not target_text:
                continue
            target = (path.parent / target_text).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                continue
            if not target.exists():
                add(findings, "error", "markdown.missing_link", rel, f"Missing local target: {target_text}", text.count("\n", 0, match.start()) + 1)
        for pattern, why in LEGACY_PATTERNS.items():
            for match in re.finditer(pattern, text):
                add(findings, "error", "legacy.pattern", rel, f"{why}: {match.group(0)!r}", text.count("\n", 0, match.start()) + 1)


def validate_python(root: Path, findings: list[Finding]) -> None:
    for path in root.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        try:
            ast.parse(path.read_text("utf-8"), filename=str(path))
        except (OSError, SyntaxError) as exc:
            add(findings, "error", "python.syntax", path.relative_to(root), str(exc), int(getattr(exc, "lineno", 1) or 1))
    script_pattern = re.compile(r'["\']((?:skills|scripts)/[^"\']+?\.py)["\']')
    for path in (root / "scripts").glob("*.py"):
        text = path.read_text("utf-8", errors="replace")
        for match in script_pattern.finditer(text):
            if not (root / match.group(1)).is_file():
                add(findings, "error", "reference.missing_script", path.relative_to(root), f"Referenced script does not exist: {match.group(1)}", text.count("\n", 0, match.start()) + 1)


def validate_layout(root: Path, findings: list[Finding]) -> None:
    is_repo = (root / "install.ps1").is_file() or (root / ".git").is_dir()
    legacy_dirs = ("workflows", "agent") if is_repo else ("rules", "workflows", "agent")
    for legacy in legacy_dirs:
        if (root / legacy).exists():
            add(findings, "error", "layout.legacy_dir", Path(legacy), f"Directory '{legacy}/' must not exist in the plugin (see DECISIONS.md)")
    if not (root / "plugin.json").is_file():
        add(findings, "error", "layout.plugin_json", Path("plugin.json"), "plugin.json is required")


def validate(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    validate_layout(root, findings)
    validate_json(root, findings)
    validate_version(root, findings)
    agents, skills = validate_agents_and_skills(root, findings)
    validate_markdown_references(root, agents, skills, findings)
    validate_python(root, findings)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AG Kit v2 structure and cross references")
    parser.add_argument("path", nargs="?", default=None, help="Kit root (defaults to this toolkit)")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = Path(args.path).resolve() if args.path else Path(__file__).resolve().parents[1]
    if not root.is_dir():
        parser.error(f"Toolkit directory does not exist: {root}")
    findings = validate(root)
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    if args.as_json:
        print(json.dumps({"toolkit": str(root), "passed": not errors, "errors": len(errors), "warnings": len(warnings), "findings": [f.__dict__ for f in findings]}, indent=2, ensure_ascii=False))
    else:
        print(f"AG Kit self-validation: {root}")
        for item in findings:
            print(f"[{item.severity.upper()}] {item.file}:{item.line} {item.code} - {item.message}")
        print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)")
        print("[PASS] Toolkit is structurally valid." if not errors else "[FAIL] Toolkit validation failed.")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
