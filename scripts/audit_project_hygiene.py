#!/usr/bin/env python3
"""Audit an application project against Keith Master Kit Zero-Conflict CSS & Markup Rules."""
from __future__ import annotations

import re
import sys
from pathlib import Path

LOCKED_OR_VENDOR_CSS = {
    "style.css",
    "08-COMPACT-PURE-CONTRAST-OVERRIDE.css",
    "kit-theme-bridge.css",
    "nice-select.css",
}
SKIP_DIRS = {"node_modules", "vendor", "icons", ".git", "reference-template", "storage", "dist", "build"}

FORBIDDEN_APP_CSS_SELECTORS = re.compile(
    r"(?m)^\s*(?:html|body|h[1-6]|a|p|label|table|\.(?:card|btn|badge|table|form-|modal|nav-pills|page-|dlabnav|header|nav-header|sidebar-right|invoice-card)|\[data-(?:theme-version|primary|sibebarbg|headerbg|nav-headerbg))\b"
)
RAW_HEX_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")
BANNED_MARKUP_PATTERNS = [
    (re.compile(r"\b(?:text-dark|text-black|bg-white|bg-light)\b"), "Hardcoded light-only Bootstrap color utility (breaks Dark Mode / dark swatches; use .kit-subtle-box or .kit-muted)"),
    (re.compile(r"javascript:void\(0\)", re.IGNORECASE), "Invalid javascript:void(0) trigger (use <button type=\"button\">)"),
    (re.compile(r"\b(?:Lorem ipsum|DexignLab|Dompet|John Doe)\b", re.IGNORECASE), "Leftover template placeholder/sample text"),
]


def iter_project_files(root: Path, suffixes: set[str]):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def strip_css_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python audit_project_hygiene.py <project_directory>")
        return 2

    project_root = Path(sys.argv[1]).resolve()
    if not project_root.is_dir():
        print(f"[ERROR] Directory not found: {project_root}")
        return 2

    violations: list[str] = []

    # 1. Audit custom project CSS files (Layer 3: .app-* only)
    for css_file in iter_project_files(project_root, {".css"}):
        if css_file.name in LOCKED_OR_VENDOR_CSS:
            continue
        cleaned = strip_css_comments(css_file.read_text("utf-8", errors="replace"))
        rel = css_file.relative_to(project_root)

        if "!important" in cleaned:
            violations.append(f"{rel}: '!important' is banned in project app CSS (move shared theme overrides to locked kit bridge)")
        for match in FORBIDDEN_APP_CSS_SELECTORS.finditer(cleaned):
            violations.append(f"{rel}: Forbidden global/Bootstrap/template selector '{match.group(0).strip()}' in app CSS (use .app-* namespace)")
            break
        hex_matches = RAW_HEX_COLOR.findall(cleaned)
        if hex_matches:
            violations.append(f"{rel}: Raw hex color(s) {sorted(set(hex_matches))[:5]} in app CSS (use var(--kit-*) or var(--primary) tokens)")

    # 2. Audit view/component templates
    for view_file in iter_project_files(project_root, {".ejs", ".php", ".jsx", ".tsx", ".vue", ".html"}):
        content = view_file.read_text("utf-8", errors="replace")
        rel = view_file.relative_to(project_root)
        for regex, reason in BANNED_MARKUP_PATTERNS:
            match = regex.search(content)
            if match:
                violations.append(f"{rel}: Found '{match.group(0)}' — {reason}")

    print(f"Project Hygiene Audit: {project_root}")
    if violations:
        for item in violations:
            print(f"  [FAIL] {item}")
        print(f"[FAILED] {len(violations)} violation(s) found.")
        return 1

    print("[PASS] 0 CSS conflicts, 0 banned color utilities, 0 template leftovers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
