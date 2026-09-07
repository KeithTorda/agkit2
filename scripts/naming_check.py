#!/usr/bin/env python3
"""Naming check: unique, searchable names across a project (advisory gate).

Policy: global code-rules "Unique, searchable names". Method: clean-code (files, exports) and
css-architecture (classes, custom properties).

Checks and severities:
  duplicate-basename  warning   two files share a basename (route, config, i18n conventions excluded)
  banned-filename     error     utils / helpers / styles / types / constants / common / misc, any extension
  duplicate-class     warning   the same class selector is defined in more than one .css/.scss file
  custom-property     warning   a custom property with no namespace or component prefix (--blue, --gap)
  important           advisory  !important in project CSS (count per file)
  banned-export       warning   an exported identifier from the banned generic list (helper, data, ...)

Usage: python naming_check.py <project_root> [--json]
Exit code is always 0. The last line (stderr with --json) is "naming_check: E errors, W warnings, A advisory".
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

SKIP_DIRS = {"node_modules", ".git", "dist", "build", "out", ".next", "vendor", "coverage", "__pycache__", "storage"}
STYLE_SUFFIXES = {".css", ".scss", ".sass", ".less"}
SCRIPT_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".avif", ".woff", ".woff2", ".ttf", ".otf", ".mp4", ".pdf"}
DATA_SUFFIXES = {".json", ".yml", ".yaml", ".toml", ".lock", ".txt", ".xml", ".env", ".csv"}
BANNED_STEMS = {"utils", "helpers", "styles", "types", "constants", "common", "misc"}
BANNED_EXPORTS = {"Component2", "NewButton", "data", "item", "temp", "result", "handleClick", "doStuff", "process", "manager", "helper"}
# Basenames that frameworks and tools repeat on purpose (first dot-segment, case-insensitive).
ALLOWED_STEMS = {
    "index", "page", "layout", "route", "loading", "error", "not-found", "template", "default",
    "global-error", "middleware", "opengraph-image", "sitemap", "robots", "manifest",  # Next.js app router
    "__init__", "conftest", "main", "app", "setup",  # entry points and test setup
    "models", "views", "urls", "admin", "apps", "forms", "tests", "serializers",  # Django apps
    "show", "edit", "create", "form",  # Laravel resource views
}
ALLOWED_NAMES = {"readme.md", "skill.md", "template.md", "agents.md", "claude.md", "gemini.md", "changelog.md",
                 "license", "license.md", "design.md", "globals.css", "dockerfile", "makefile", "procfile"}
I18N_DIRS = {"locales", "lang", "i18n", "translations", "messages"}
SEVERITY = {"banned-filename": "error", "duplicate-basename": "warning", "duplicate-class": "warning",
            "custom-property": "warning", "banned-export": "warning", "important": "advisory"}
MAX_BYTES = 1_500_000

BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
LINE_COMMENT_RE = re.compile(r"(?<![:\\\w])//[^\n]*")
PRELUDE_RE = re.compile(r"([^{};]*)\{")
PAREN_RE = re.compile(r"\([^()]*\)")
COMBINATOR_RE = re.compile(r"\s*[>+~]\s*|\s+")
CLASS_RE = re.compile(r"\.(-?[_a-zA-Z][\w-]*)")
CUSTOM_PROP_RE = re.compile(r"(?<![\w(,-])(--[A-Za-z0-9_-]+)\s*:")
PREFIXED_PROP_RE = re.compile(r"[a-z][a-z0-9]*-[a-z0-9-]+", re.I)
IMPORTANT_RE = re.compile(r"!\s*important", re.I)
EXPORT_DECL_RE = re.compile(r"\bexport\s+(?:default\s+)?(?:async\s+)?(?:function\*?|const|let|var|class|type|interface|enum)\s+([A-Za-z_$][\w$]*)")
EXPORT_LIST_RE = re.compile(r"\bexport\s*\{([^}]*)\}")


@dataclass
class Finding:
    check: str
    severity: str
    file: str
    detail: str


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(filenames):
            if ".min." not in name:
                yield Path(dirpath) / name


def read_text(path: Path) -> str:
    try:
        if path.stat().st_size > MAX_BYTES:
            return ""
        return path.read_text("utf-8", errors="replace")
    except OSError:
        return ""


def strip_comments(text: str, suffix: str) -> str:
    """Blank out comments but keep their newlines so line numbers stay right."""
    text = BLOCK_COMMENT_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return text if suffix == ".css" else LINE_COMMENT_RE.sub("", text)


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def stem_of(name: str) -> str:
    return name.lower().split(".")[0]


def is_convention(path: Path) -> bool:
    name = path.name.lower()
    if name in ALLOWED_NAMES or stem_of(name) in ALLOWED_STEMS or ".config." in name:
        return True
    return name.startswith(".") or bool({path.parent.name, path.parent.parent.name} & I18N_DIRS)


def subject_classes(prelude: str) -> set[str]:
    """Class names in the last compound of each selector: `.layout .sidebar:hover` -> {sidebar}."""
    found: set[str] = set()
    for selector in prelude.split(","):
        selector = PAREN_RE.sub("", PAREN_RE.sub("", selector)).strip()
        if not selector or "&" in selector:
            continue
        found.update(CLASS_RE.findall(COMBINATOR_RE.split(selector)[-1]))
    return found


def check_filenames(files: list[Path], root: Path, findings: list[Finding]) -> None:
    by_name: dict[str, list[str]] = defaultdict(list)
    for path in files:
        rel = path.relative_to(root).as_posix()
        suffix = path.suffix.lower()
        if suffix in ASSET_SUFFIXES or suffix in DATA_SUFFIXES or is_convention(path):
            continue
        if stem_of(path.name) in BANNED_STEMS:
            findings.append(Finding("banned-filename", SEVERITY["banned-filename"], rel,
                                    f"'{stem_of(path.name)}' is a banned generic name; rename to <domain>-<role>{suffix}"))
        by_name[path.name.lower()].append(rel)
    for name, paths in sorted(by_name.items()):
        if len(paths) > 1:
            findings.append(Finding("duplicate-basename", SEVERITY["duplicate-basename"], paths[0],
                                    f"'{name}' also at: {', '.join(paths[1:])}"))


def check_styles(files: list[Path], root: Path, findings: list[Finding]) -> None:
    class_sites: dict[str, list[str]] = defaultdict(list)
    for path in files:
        if path.suffix.lower() not in STYLE_SUFFIXES:
            continue
        rel = path.relative_to(root).as_posix()
        text = strip_comments(read_text(path), path.suffix.lower())
        seen: set[str] = set()
        for match in PRELUDE_RE.finditer(text):
            prelude = match.group(1).strip()
            if not prelude or prelude.startswith(("@", "%")):
                continue
            leading = len(match.group(1)) - len(match.group(1).lstrip())
            line = line_of(text, match.start(1) + leading)
            for name in sorted(subject_classes(prelude) - seen):
                seen.add(name)
                class_sites[name].append(f"{rel}:{line}")
        for name in sorted({m.group(1) for m in CUSTOM_PROP_RE.finditer(text)}):
            if not PREFIXED_PROP_RE.fullmatch(name[2:]):
                findings.append(Finding("custom-property", SEVERITY["custom-property"], rel,
                                        f"'{name}' has no namespace or component prefix (--color-*, --<component>-<property>)"))
        count = len(IMPORTANT_RE.findall(text))
        if count:
            findings.append(Finding("important", SEVERITY["important"], rel,
                                    f"{count} !important; fix the layer order instead (css-architecture)"))
    for name, sites in sorted(class_sites.items()):
        files_hit = sorted({site.rsplit(":", 1)[0] for site in sites})
        if len(files_hit) > 1:
            findings.append(Finding("duplicate-class", SEVERITY["duplicate-class"], files_hit[0],
                                    f"'.{name}' is defined in {len(files_hit)} files: {', '.join(sites)}"))


def exported_names(text: str):
    for match in EXPORT_DECL_RE.finditer(text):
        yield match.group(1), match.start()
    for match in EXPORT_LIST_RE.finditer(text):
        for item in match.group(1).split(","):
            parts = item.replace("type ", " ").split()
            if parts:
                yield parts[-1], match.start()


def check_exports(files: list[Path], root: Path, findings: list[Finding]) -> None:
    for path in files:
        if path.suffix.lower() not in SCRIPT_SUFFIXES:
            continue
        rel = path.relative_to(root).as_posix()
        text = strip_comments(read_text(path), path.suffix.lower())
        reported: set[str] = set()
        for name, index in exported_names(text):
            if name in BANNED_EXPORTS and name not in reported:
                reported.add(name)
                findings.append(Finding("banned-export", SEVERITY["banned-export"], f"{rel}:{line_of(text, index)}",
                                        f"exported '{name}' is a banned generic identifier; use a domain-prefixed name"))


def run(root: Path) -> list[Finding]:
    files = list(iter_files(root))
    findings: list[Finding] = []
    check_filenames(files, root, findings)
    check_styles(files, root, findings)
    check_exports(files, root, findings)
    return findings


def summary_line(findings: list[Finding]) -> str:
    counts = {level: sum(f.severity == level for f in findings) for level in ("error", "warning", "advisory")}
    return f"naming_check: {counts['error']} errors, {counts['warning']} warnings, {counts['advisory']} advisory"


def print_report(root: Path, findings: list[Finding]) -> None:
    print(f"[NAMING CHECK] {root}")
    for check in SEVERITY:
        group = [f for f in findings if f.check == check]
        if not group:
            continue
        print(f"\n[{SEVERITY[check].upper()}] {check} ({len(group)})")
        for item in group:
            print(f"  {item.file}: {item.detail}")
    print(f"\n{summary_line(findings)}")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("Usage: python naming_check.py <project_root> [--json]")
        return 0
    root = Path(args[0]).resolve()
    if not root.is_dir():
        print(f"naming_check: not a directory: {root}")
        return 0
    findings = run(root)
    if "--json" in sys.argv:
        print(json.dumps([asdict(f) for f in findings], indent=2))
        print(summary_line(findings), file=sys.stderr)
    else:
        print_report(root, findings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
