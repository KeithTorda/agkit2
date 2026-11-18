#!/usr/bin/env python3
"""Audit any application project against Keith Master Kit Stack-Agnostic CSS & Markup Rules."""
from __future__ import annotations

import re
import sys
from pathlib import Path

LOCKED_OR_FRAMEWORK_CSS = {
    "keith-ui-tokens.css",
    "globals.css",
    "app.css",
    "tailwind.css",
    "style.css",
    "08-COMPACT-PURE-CONTRAST-OVERRIDE.css",
    "nice-select.css",
}
SKIP_DIRS = {"node_modules", "vendor", "icons", ".git", ".next", "storage", "dist", "build"}

FORBIDDEN_CUSTOM_CSS_SELECTORS = re.compile(
    r"(?m)^\s*(?:html|body|h[1-6]|a|p|label|table|\.(?:card|btn|badge|table|form-|modal|nav-pills|page-))\b"
)
RAW_HEX_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")
BANNED_MARKUP_PATTERNS = [
    (re.compile(r"\b(?:text-dark|text-black|bg-white|bg-light)\b(?!\s+dark:)"), "Unpaired light-only color utility (breaks Dark Mode; use semantic tokens like bg-card / .ui-subtle-box / dark: pair)"),
    (re.compile(r"javascript:void\(0\)", re.IGNORECASE), "Invalid javascript:void(0) trigger (use <button type=\"button\">)"),
    (re.compile(r"\b(?:Lorem ipsum|John Doe)\b", re.IGNORECASE), "Leftover placeholder/sample text"),
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

    for css_file in iter_project_files(project_root, {".css"}):
        if css_file.name in LOCKED_OR_FRAMEWORK_CSS:
            continue
        cleaned = strip_css_comments(css_file.read_text("utf-8", errors="replace"))
        rel = css_file.relative_to(project_root)

        if "!important" in cleaned:
            violations.append(f"{rel}: '!important' is banned in custom domain CSS (use @layer and semantic tokens)")
        for match in FORBIDDEN_CUSTOM_CSS_SELECTORS.finditer(cleaned):
            violations.append(f"{rel}: Unscoped tag/framework selector '{match.group(0).strip()}' in custom CSS (use .app-* namespace)")
            break
        hex_matches = RAW_HEX_COLOR.findall(cleaned)
        if hex_matches:
            violations.append(f"{rel}: Raw hex color(s) {sorted(set(hex_matches))[:5]} outside token file (use var(--ui-*) / semantic tokens)")

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

    print("[PASS] 0 CSS conflicts, 0 unpaired light-only utilities, 0 placeholder leftovers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
