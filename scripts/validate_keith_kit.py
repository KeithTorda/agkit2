#!/usr/bin/env python3
"""Validate Keith Master Kit v5.0.0 structure, frontmatter, byte budgets, first-party UI kit, and zero third-party template remnants."""
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
BANNED_THIRD_PARTY_TERMS = re.compile(r"\b(?:StarCodeKH|Dompet|DexignLab|dlabnav|data-sibebarbg)\b", re.IGNORECASE)


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

    if (KIT_ROOT / "reference-template").exists():
        errors.append("Third-party reference-template/ must not exist in v5.0.0+")

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

    # Validate first-party catalog & portable UI kit
    catalog_files = list((KIT_ROOT / "component-catalog").glob("*.md"))
    if len(catalog_files) != 8:
        errors.append(f"Expected 8 component-catalog/*.md files, found {len(catalog_files)}")

    tokens_css = KIT_ROOT / "ui-kit" / "keith-ui-tokens.css"
    settings_js = KIT_ROOT / "ui-kit" / "keith-ui-settings.js"
    if not tokens_css.is_file():
        errors.append("Missing ui-kit/keith-ui-tokens.css")
    else:
        css_text = tokens_css.read_text("utf-8")
        for req in ("@layer tokens", "--ui-ink:", "--on-primary:", "--primary-ink:"):
            if req not in css_text:
                errors.append(f"ui-kit/keith-ui-tokens.css missing '{req}'")
    if not settings_js.is_file():
        errors.append("Missing ui-kit/keith-ui-settings.js")
    if not (KIT_ROOT / "scripts" / "audit_project_hygiene.py").is_file():
        errors.append("Missing scripts/audit_project_hygiene.py")

    # Verify zero third-party template terms in active kit docs/rules/skills/agents/ui-kit
    for check_dir in ("rules", "skills", "agents", "component-catalog", "ui-kit"):
        for fpath in (KIT_ROOT / check_dir).rglob("*"):
            if fpath.is_file():
                m = BANNED_THIRD_PARTY_TERMS.search(fpath.read_text("utf-8", errors="replace"))
                if m:
                    errors.append(f"{fpath.relative_to(KIT_ROOT)} contains third-party leftover '{m.group(0)}'")

    print(f"Keith Master Kit Validation: {KIT_ROOT}")
    print(f"  Rules: {len(list(rules_dir.glob('*.md')))} files | Skills: {len(list((KIT_ROOT / 'skills').iterdir()))} | Agents: {len(list((KIT_ROOT / 'agents').glob('*.md')))}")
    print(f"  First-Party Catalog Guides: {len(catalog_files)} | UI Kit Engine: OK")
    for warn in warnings:
        print(f"  [WARN] {warn}")
    for err in errors:
        print(f"  [ERROR] {err}")

    if errors:
        print(f"[FAIL] {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"[PASS] 0 errors, 0 warning(s). Ready for Antigravity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
