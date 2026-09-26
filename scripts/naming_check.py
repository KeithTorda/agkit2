#!/usr/bin/env python3
"""Naming check: searchable, domain-specific names (code-rules "Names"). Advisory.

Checks and severities:
  generic-filename    error    utils / helpers / misc / common / styles / temp as a file name in a
                               generic folder (src/, lib/, components/, the root) - rename to
                               <domain>-<role>. `invoices/types.ts` is fine: the folder names it.
  duplicate-basename  warning  two source files share a name (framework conventions and tests excluded)
  duplicate-class     warning  the same class selector defined in more than one global stylesheet
                               (CSS modules and scoped component styles excluded)
  generic-export      warning  an exported identifier from a generic list (helper, data, temp, ...)
  custom-property     note     a custom property with no namespace (--blue, --gap); Tailwind @theme
                               tokens and the shadcn/ui token set are excluded

`!important` is reported by css_audit.py, not here.

Advisory by default (exit 0). --strict: errors exit 1.
Exit codes: 0 ok, 1 errors with --strict, 2 usage.

Usage:
  python naming_check.py .
  python naming_check.py . --json
  python naming_check.py . --strict
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

SKIP_DIRS = {"node_modules", "dist", "build", "out", ".next", ".nuxt", ".output", "vendor", "coverage",
             "__pycache__", "storage", "bower_components", "target", "venv", "env", "site-packages",
             "migrations", "bootstrap"}
STYLE_SUFFIXES = {".css", ".scss", ".sass", ".less"}
SCRIPT_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".cts"}
SOURCE_SUFFIXES = SCRIPT_SUFFIXES | STYLE_SUFFIXES | {".py", ".php", ".vue", ".svelte", ".astro", ".html", ".go", ".rs", ".dart"}
GENERIC_STEMS = {"utils", "util", "helpers", "helper", "misc", "common", "stuff", "temp", "tmp", "functions", "things", "styles"}
GENERIC_PARENTS = {"", "src", "lib", "app", "components", "shared", "common", "utils", "helpers", "js", "scripts",
                   "includes", "inc", "core", "assets", "static", "public", "resources", "source"}
GENERIC_EXPORTS = {"Component2", "NewButton", "data", "item", "temp", "result", "doStuff", "helper",
                   "handleClick2", "foo", "bar", "stuff", "thing", "obj", "myFunction"}
# Basenames that frameworks and tools repeat on purpose (first dot-segment, case-insensitive).
ALLOWED_STEMS = {
    "index", "page", "layout", "route", "loading", "error", "not-found", "template", "default",
    "global-error", "middleware", "proxy", "opengraph-image", "twitter-image", "icon", "sitemap", "robots",
    "manifest", "head", "+page", "+layout", "+server", "+error", "_app", "_document",
    "__init__", "__main__", "conftest", "main", "app", "setup", "server", "client", "config", "settings",
    "models", "views", "urls", "admin", "apps", "forms", "tests", "serializers", "schemas", "routes",
    "show", "edit", "create", "form", "types", "constants", "styles", "schema", "actions", "hooks", "store",
    "api", "handler", "service", "controller", "module", "readme", "changelog", "license", "skill",
}
ALLOWED_NAMES = {"design.md", "agents.md", "claude.md", "gemini.md", "globals.css", "dockerfile", "makefile", "procfile"}
I18N_DIRS = {"locales", "lang", "i18n", "translations", "messages"}
TEST_NAME = re.compile(r"(^test_|_test\.|\.test\.|\.spec\.|test\.php$|tests?\.py$)", re.I)
SHADCN_TOKENS = {"background", "foreground", "card", "card-foreground", "popover", "popover-foreground", "primary",
                 "primary-foreground", "secondary", "secondary-foreground", "muted", "muted-foreground", "accent",
                 "accent-foreground", "destructive", "destructive-foreground", "border", "input", "ring", "radius",
                 "sidebar", "chart-1", "chart-2", "chart-3", "chart-4", "chart-5", "spacing"}
SEVERITY = {"generic-filename": "error", "duplicate-basename": "warning", "duplicate-class": "warning",
            "generic-export": "warning", "custom-property": "note"}
MAX_BYTES = 1_500_000

BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
LINE_COMMENT_RE = re.compile(r"(?<![:\\\w\"'])//[^\n]*")
PRELUDE_RE = re.compile(r"([^{};]*)\{")
PAREN_RE = re.compile(r"\([^()]*\)")
COMBINATOR_RE = re.compile(r"\s*[>+~]\s*|\s+")
CLASS_RE = re.compile(r"\.(-?[_a-zA-Z][\w-]*)")
CUSTOM_PROP_RE = re.compile(r"(?<![\w(,-])(--[A-Za-z0-9_-]+)\s*:")
PREFIXED_PROP_RE = re.compile(r"[a-z][a-z0-9]*-[a-z0-9-]+", re.I)
THEME_BLOCK_RE = re.compile(r"@theme\b[^{]*\{", re.I)
VENDOR_BANNER = re.compile(r"^\s*/\*!", re.S)
EXPORT_DECL_RE = re.compile(r"\bexport\s+(?:default\s+)?(?:async\s+)?(?:function\*?|const|let|var|class|type|interface|enum)\s+([A-Za-z_$][\w$]*)")
EXPORT_LIST_RE = re.compile(r"\bexport\s*\{([^}]*)\}")


def utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass


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


def is_scoped_style(path: Path) -> bool:
    return ".module." in path.name.lower()


def is_convention(path: Path) -> bool:
    name = path.name.lower()
    if name in ALLOWED_NAMES or stem_of(name) in ALLOWED_STEMS or ".config." in name or name.startswith("."):
        return True
    if TEST_NAME.search(name) or any(p in {"tests", "test", "__tests__", "spec", "e2e"} for p in path.parts):
        return True
    if re.match(r"^\[.*\]$", stem_of(name)) or stem_of(name).startswith(("[", "(", "@")):
        return True        # dynamic route segments
    return bool({path.parent.name.lower(), path.parent.parent.name.lower()} & I18N_DIRS)


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
        rel_path = path.relative_to(root)
        rel = rel_path.as_posix()
        suffix = path.suffix.lower()
        if suffix not in SOURCE_SUFFIXES:
            continue
        parent = rel_path.parent.name.lower() if rel_path.parent != Path(".") else ""
        if stem_of(path.name) in GENERIC_STEMS and parent in GENERIC_PARENTS:
            findings.append(Finding("generic-filename", SEVERITY["generic-filename"], rel,
                                    f"'{path.name}' in a generic folder says nothing about what it holds; "
                                    f"rename to <domain>-<role>{suffix} or move it into the feature folder"))
        if is_convention(rel_path):
            continue
        by_name[path.name.lower()].append(rel)
    for name, paths in sorted(by_name.items()):
        if len(paths) > 1:
            findings.append(Finding("duplicate-basename", SEVERITY["duplicate-basename"], paths[0],
                                    f"'{name}' also at: {', '.join(paths[1:4])}" + (" ..." if len(paths) > 4 else "")))


def theme_spans(text: str) -> list[tuple[int, int]]:
    spans = []
    for m in THEME_BLOCK_RE.finditer(text):
        depth, i = 1, m.end()
        while i < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        spans.append((m.start(), i))
    return spans


def check_styles(files: list[Path], root: Path, findings: list[Finding]) -> None:
    class_sites: dict[str, list[str]] = defaultdict(list)
    for path in files:
        if path.suffix.lower() not in STYLE_SUFFIXES:
            continue
        raw = read_text(path)
        if VENDOR_BANNER.match(raw[:200]):
            continue
        rel = path.relative_to(root).as_posix()
        text = strip_comments(raw, path.suffix.lower())
        if not is_scoped_style(path):
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
        spans = theme_spans(text)
        reported: set[str] = set()
        for m in CUSTOM_PROP_RE.finditer(text):
            name = m.group(1)
            bare = name[2:]
            if name in reported or any(a <= m.start() < b for a, b in spans):
                continue
            if PREFIXED_PROP_RE.fullmatch(bare) or bare.lower() in SHADCN_TOKENS:
                continue
            reported.add(name)
            findings.append(Finding("custom-property", SEVERITY["custom-property"], f"{rel}:{line_of(text, m.start())}",
                                    f"'{name}' has no namespace (--color-*, --space-*, --<component>-<property>)"))
    for name, sites in sorted(class_sites.items()):
        files_hit = sorted({site.rsplit(":", 1)[0] for site in sites})
        if len(files_hit) > 1:
            findings.append(Finding("duplicate-class", SEVERITY["duplicate-class"], files_hit[0],
                                    f"'.{name}' is defined in {len(files_hit)} global stylesheets: {', '.join(sites[:4])}"))


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
        if path.suffix.lower() not in SCRIPT_SUFFIXES or path.name.endswith(".d.ts"):
            continue
        rel = path.relative_to(root).as_posix()
        text = strip_comments(read_text(path), path.suffix.lower())
        reported: set[str] = set()
        for name, index in exported_names(text):
            if name in GENERIC_EXPORTS and name not in reported:
                reported.add(name)
                findings.append(Finding("generic-export", SEVERITY["generic-export"], f"{rel}:{line_of(text, index)}",
                                        f"exported '{name}' is a generic name; use one that says what it is"))


def run(root: Path) -> list[Finding]:
    files = list(iter_files(root))
    findings: list[Finding] = []
    check_filenames(files, root, findings)
    check_styles(files, root, findings)
    check_exports(files, root, findings)
    return findings


def counts(findings: list[Finding]) -> dict[str, int]:
    return {level: sum(f.severity == level for f in findings) for level in ("error", "warning", "note")}


def summary_line(findings: list[Finding], failed: bool = False) -> str:
    c = counts(findings)
    label = "FAIL" if failed else ("PASS" if not findings else "ADVISORY")
    return f"naming_check: {label} - {c['error']} error(s), {c['warning']} warning(s), {c['note']} note(s)"


def print_report(root: Path, findings: list[Finding], failed: bool) -> None:
    print(f"[naming check] {root}")
    for check in SEVERITY:
        group = [f for f in findings if f.check == check]
        if not group:
            continue
        print(f"\n[{SEVERITY[check]}] {check} ({len(group)})")
        for item in group[:40]:
            print(f"  {item.file}: {item.detail}")
        if len(group) > 40:
            print(f"  ... and {len(group) - 40} more (--json)")
    print(f"\n{summary_line(findings, failed)}")


def main(argv: list[str] | None = None) -> int:
    utf8_stdio()
    ap = argparse.ArgumentParser(description="Searchable-naming check (advisory).",
                                 epilog="Exit codes: 0 ok (advisory), 1 errors with --strict, 2 usage.")
    ap.add_argument("project", nargs="?", default=".", type=Path)
    ap.add_argument("--strict", action="store_true", help="errors fail (exit 1)")
    ap.add_argument("--json", action="store_true", help="print findings as JSON to stdout")
    args = ap.parse_args(argv)
    root = args.project.resolve()
    if not root.is_dir():
        print(f"naming_check: not a directory: {root}", file=sys.stderr)
        return 2
    findings = run(root)
    failed = args.strict and counts(findings)["error"] > 0
    if args.json:
        print(json.dumps({"project": str(root), "strict": args.strict, **counts(findings),
                          "findings": [asdict(f) for f in findings]}, indent=2))
    else:
        print_report(root, findings, failed)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
