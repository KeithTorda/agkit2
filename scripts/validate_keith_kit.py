#!/usr/bin/env python3
"""Validate Keith Master Kit structure, Antigravity frontmatter, byte budgets, and template catalog."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]
ALLOWED_PLUGIN_KEYS = {
    "name", "displayName", "version", "description", "logo",
    "suggestedPrompts", "author", "homepage", "repository", "disabled",
}
ALLOWED_TRIGGERS = {"always_on", "glob", "model_decision", "manual"}
RULE_MAX_BYTES = 24000
RULE_SOFT_BYTES = 12000


def parse_frontmatter(text: str) -> dict[str, str] | None:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return None
    end_idx = normalized.find("\n---", 4)
    if end_idx < 0:
        return None
    result: dict[str, str] = {}
    for line in normalized[4:end_idx].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line.strip())
        if match:
            result[match.group(1)] = match.group(2).strip().strip("\"'")
    return result


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    manifest_path = KIT_ROOT / "plugin.json"
    version_path = KIT_ROOT / "VERSION"
    if not manifest_path.is_file():
        errors.append("Missing plugin.json")
    else:
        manifest = json.loads(manifest_path.read_text("utf-8"))
        unknown_keys = set(manifest.keys()) - ALLOWED_PLUGIN_KEYS
        if unknown_keys:
            errors.append(f"plugin.json contains unsupported keys: {sorted(unknown_keys)}")
        if version_path.is_file() and manifest.get("version") != version_path.read_text("utf-8").strip():
            errors.append("VERSION does not match plugin.json version")

    # Validate rules
    rules_dir = KIT_ROOT / "rules"
    if not (rules_dir / "AGENTS.md").is_file():
        errors.append("Missing consolidated rules/AGENTS.md")
    for rule_file in sorted(rules_dir.glob("*.md")):
        raw_bytes = rule_file.read_bytes()
        text = raw_bytes.decode("utf-8")
        if len(raw_bytes) > RULE_MAX_BYTES:
            errors.append(f"{rule_file.name} exceeds 24 KB limit ({len(raw_bytes)} bytes)")
        elif len(raw_bytes) > RULE_SOFT_BYTES:
            warnings.append(f"{rule_file.name} exceeds 12 KB soft target ({len(raw_bytes)} bytes)")

        if rule_file.name == "AGENTS.md":
            if text.startswith("---"):
                errors.append("rules/AGENTS.md must be plain markdown without YAML frontmatter")
            continue

        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{rule_file.name}: missing YAML frontmatter")
            continue
        if "priority" in fm:
            errors.append(f"{rule_file.name}: unsupported 'priority' key in frontmatter")
        trigger = fm.get("trigger", "")
        if trigger not in ALLOWED_TRIGGERS:
            errors.append(f"{rule_file.name}: invalid trigger {trigger!r}")
        if trigger == "glob" and not fm.get("globs"):
            errors.append(f"{rule_file.name}: glob trigger requires 'globs'")

    # Validate skills
    for skill_dir in sorted((KIT_ROOT / "skills").iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"skills/{skill_dir.name}: missing SKILL.md")
            continue
        fm = parse_frontmatter(skill_md.read_text("utf-8"))
        if not fm:
            errors.append(f"skills/{skill_dir.name}/SKILL.md: missing frontmatter")
        elif fm.get("name") != skill_dir.name:
            errors.append(f"skills/{skill_dir.name}/SKILL.md: name={fm.get('name')!r} != {skill_dir.name!r}")

    # Validate subagents
    for agent_md in sorted((KIT_ROOT / "agents").glob("*.md")):
        fm = parse_frontmatter(agent_md.read_text("utf-8"))
        if not fm:
            errors.append(f"agents/{agent_md.name}: missing frontmatter")
            continue
        if fm.get("name") != agent_md.stem:
            errors.append(f"agents/{agent_md.name}: name mismatch")
        if fm.get("subagent") != "true":
            errors.append(f"agents/{agent_md.name}: subagent must be true")
        if fm.get("mainAgent") != "false":
            errors.append(f"agents/{agent_md.name}: mainAgent must be false")
        if not fm.get("tools") or fm.get("tools") == "[]":
            errors.append(f"agents/{agent_md.name}: tools must be explicitly declared so subagent is not read-only")

    # Validate downloaded Bootstrap 5 template & component catalog
    tpl_dir = KIT_ROOT / "reference-template" / "bootstrap-5-dashboard-pro"
    html_count = len(list(tpl_dir.glob("*.html"))) if tpl_dir.is_dir() else 0
    if html_count < 60:
        errors.append(f"Expected >=60 template HTML pages in {tpl_dir}, found {html_count}")
    if not (tpl_dir / "css" / "style.css").is_file():
        errors.append("Missing reference-template/bootstrap-5-dashboard-pro/css/style.css")

    catalog_files = list((KIT_ROOT / "component-catalog").glob("*.md"))
    if len(catalog_files) < 8:
        errors.append(f"Expected 8 component-catalog/*.md files, found {len(catalog_files)}")

    bridge_css = KIT_ROOT / "component-catalog" / "08-COMPACT-PURE-CONTRAST-OVERRIDE.css"
    if not bridge_css.is_file():
        errors.append("Missing component-catalog/08-COMPACT-PURE-CONTRAST-OVERRIDE.css")
    else:
        bridge_text = bridge_css.read_text("utf-8")
        for required_token in ("--kit-ink:", "--on-primary:", "--on-sidebar:", "--primary-ink:"):
            if required_token not in bridge_text:
                errors.append(f"08-COMPACT-PURE-CONTRAST-OVERRIDE.css missing token {required_token}")

    if not (KIT_ROOT / "scripts" / "audit_project_hygiene.py").is_file():
        errors.append("Missing scripts/audit_project_hygiene.py")

    print(f"Keith Master Kit Validation: {KIT_ROOT}")
    print(f"  Rules: {len(list(rules_dir.glob('*.md')))} files | Skills: {len(list((KIT_ROOT / 'skills').iterdir()))} | Agents: {len(list((KIT_ROOT / 'agents').glob('*.md')))}")
    print(f"  Template HTML Pages: {html_count} | Catalog Guides: {len(catalog_files)}")
    for warn in warnings:
        print(f"  [WARN] {warn}")
    for err in errors:
        print(f"  [ERROR] {err}")

    if errors:
        print(f"[FAIL] {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"[PASS] 0 errors, {len(warnings)} warning(s). Ready for Antigravity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
