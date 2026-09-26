#!/usr/bin/env python3
"""SEO checker for public pages: HTML, PHP/Blade, Astro, Vue, Svelte and Next.js.

  error    a document (<html>/<head>) or Next.js root layout with no title
  warning  missing meta description, page marked noindex, more than one <h1>
  info     missing Open Graph tags or canonical link, title/description length,
           Next.js pages without their own metadata, no robots.txt / sitemap

Image alt text and <html lang> are accessibility errors and are reported by
accessibility_checker.py; this script does not repeat them.

Usage:
    python seo_checker.py <project-or-file> [--json] [--fail-on error|warning|never] [--verbose]

Exit codes: 0 ok, 1 findings at/above --fail-on (default: error), 2 usage error.
"""
from __future__ import annotations

import argparse
import bisect
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Iterator

# ---------------------------------------------------------------------------
# Shared helpers (same block in every AG Kit skill script; stdlib only)
# ---------------------------------------------------------------------------
SKIP_DIRS = frozenset({
    "node_modules", "vendor", "dist", "build", ".next", ".nuxt", ".svelte-kit",
    ".output", "out", ".git", ".hg", ".svn", "__pycache__", ".venv", "venv",
    ".tox", ".mypy_cache", ".pytest_cache", ".ruff_cache", "coverage", ".turbo",
    ".cache", ".vercel", ".expo", ".agents", ".agent", ".idea", ".vscode",
})
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


def utf8_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def read_text(path: Path) -> str:
    """Read a text file as UTF-8 (BOM and UTF-16 aware). Never raises."""
    try:
        data = path.read_bytes()
    except OSError:
        return ""
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return data.decode("utf-16", errors="replace")
    return data.decode("utf-8-sig", errors="replace")


def iter_files(root: Path, suffixes: Iterable[str], skip_dirs: frozenset[str] = SKIP_DIRS) -> Iterator[Path]:
    """Yield files under root (or root itself) whose name ends with one of suffixes."""
    ends = tuple(s.lower() for s in suffixes)
    if root.is_file():
        if root.name.lower().endswith(ends):
            yield root
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in skip_dirs)
        for name in sorted(filenames):
            if name.lower().endswith(ends):
                yield Path(dirpath) / name


def rel(path: Path, root: Path) -> str:
    base = root if root.is_dir() else root.parent
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return path.as_posix()


def line_finder(text: str):
    starts = [0] + [m.end() for m in re.finditer("\n", text)]
    return lambda index: bisect.bisect_right(starts, index)


def make_finding(severity: str, file: str, line: int | None, rule: str, message: str) -> dict[str, Any]:
    return {"severity": severity, "file": file, "line": line, "rule": rule, "message": message}


def summarize(findings: list[dict[str, Any]]) -> dict[str, int]:
    counts = {level: 0 for level in SEVERITY_ORDER}
    for item in findings:
        counts[item["severity"]] += 1
    counts["total"] = len(findings)
    return counts


def should_fail(findings: list[dict[str, Any]], fail_on: str) -> bool:
    if fail_on == "never":
        return False
    limit = SEVERITY_ORDER[fail_on]
    return any(SEVERITY_ORDER[item["severity"]] <= limit for item in findings)


def print_report(title: str, target: Path, findings: list[dict[str, Any]], files_checked: int,
                 verbose: bool = False, notes: Iterable[str] = (), per_file: int = 12) -> None:
    counts = summarize(findings)
    print(f"{title}: {target}")
    print(f"Checked {files_checked} file(s): {counts['error']} error(s), "
          f"{counts['warning']} warning(s), {counts['info']} info")
    for note in notes:
        print(f"  note: {note}")
    shown = [f for f in findings if verbose or f["severity"] != "info"]
    by_file: dict[str, list[dict[str, Any]]] = {}
    for item in sorted(shown, key=lambda f: (f["file"], f["line"] or 0, SEVERITY_ORDER[f["severity"]])):
        by_file.setdefault(item["file"], []).append(item)
    for file, items in by_file.items():
        print(f"\n{file}")
        for item in items[:per_file]:
            where = f"L{item['line']}" if item["line"] else "-"
            print(f"  {where:>6}  {item['severity']:<7}  {item['message']}  [{item['rule']}]")
        if len(items) > per_file:
            print(f"  ... {len(items) - per_file} more in this file")
    infos = [f for f in findings if f["severity"] == "info"]
    if infos and not verbose:
        print("\nAdvisory (info - guidance, never a failure; --verbose lists each):")
        groups: dict[str, list[dict[str, Any]]] = {}
        for item in infos:
            groups.setdefault(item["rule"], []).append(item)
        for rule, items in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            first = items[0]
            where = f"{first['file']}:{first['line']}" if first["line"] else first["file"]
            print(f"  {len(items):>3}x [{rule}] {first['message']} (e.g. {where})")


def emit(args: argparse.Namespace, script: str, title: str, target: Path, findings: list[dict[str, Any]],
         files_checked: int, notes: Iterable[str] = (), extra: dict[str, Any] | None = None) -> int:
    notes = list(notes)
    failed = should_fail(findings, args.fail_on)
    if args.json:
        payload = {"script": script, "project": str(target), "files_checked": files_checked,
                   "summary": summarize(findings), "passed": not failed, "fail_on": args.fail_on,
                   "notes": notes, "findings": findings}
        payload.update(extra or {})
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_report(title, target, findings, files_checked, args.verbose, notes)
        counts = summarize(findings)
        print(f"\nResult: {'FAIL' if failed else 'PASS'} - {counts['error']} error(s), {counts['warning']} warning(s), "
              f"{counts['info']} info (fail-on: {args.fail_on})")
    return 1 if failed else 0


def base_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("project", nargs="?", default=".", help="project directory or single file (default: .)")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--fail-on", choices=("error", "warning", "never"), default="error",
                        help="exit 1 when a finding at or above this level exists (default: error)")
    parser.add_argument("--verbose", "-v", action="store_true", help="list every info finding")
    return parser


def resolve_target(parser: argparse.ArgumentParser, value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.exists():
        parser.error(f"path not found: {path}")
    return path

# ---------------------------------------------------------------------------
# SEO checks
# ---------------------------------------------------------------------------
PAGE_SUFFIXES = (".html", ".htm", ".php", ".astro", ".vue", ".svelte", ".jsx", ".tsx", ".js", ".ts")
SEO_SKIP_DIRS = SKIP_DIRS | {"test", "tests", "__tests__", "spec", "e2e", "examples", "storybook-static", "stories"}
NEXT_LAYOUT = re.compile(r"^layout\.(tsx|jsx|ts|js)$")
NEXT_PAGE = re.compile(r"^page\.(tsx|jsx|mdx|ts|js)$")


def meta_content(text: str, key: str, attr: str = "name") -> str | None:
    for tag in re.finditer(r"<meta\b[^>]*>", text, re.I):
        if re.search(rf"\b{attr}\s*=\s*[\"']{re.escape(key)}[\"']", tag.group(0), re.I):
            content = re.search(r"\bcontent\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|\{([^}]*)\})", tag.group(0), re.I)
            return next((g for g in content.groups() if g is not None), "") if content else ""
    return None


class SEOChecker:
    def __init__(self, target: Path) -> None:
        self.target = target
        self.root = target if target.is_dir() else target.parent
        self.findings: list[dict[str, Any]] = []
        self.files_checked = 0
        self.public_pages = 0

    def add(self, severity: str, file: str, line: int | None, rule: str, message: str) -> None:
        self.findings.append(make_finding(severity, file, line, rule, message))

    def check_document(self, text: str, file: str, find_line) -> None:
        lowered = text.lower()
        head_pos = max(lowered.find("<head"), 0)
        line = find_line(head_pos)
        title = re.search(r"<title\b[^>]*>(.*?)</title\s*>", text, re.S | re.I)
        dynamic_title = re.search(r"<title\b[^>]*>\s*(\{\{|\{|<\?|@yield|@section|\$)", text, re.I)
        if not title and not re.search(r"@yield\(\s*[\"']title|<x-slot\s+name=\"title\"|@section\(\s*[\"']title", text):
            self.add("error", file, line, "title", "Document has no <title>")
        elif title and not dynamic_title:
            value = re.sub(r"\s+", " ", title.group(1)).strip()
            if not value:
                self.add("error", file, find_line(title.start()), "title", "Empty <title>")
            elif len(value) > 60:
                self.add("info", file, find_line(title.start()), "title-length",
                         f"Title is {len(value)} characters; search results cut off around 60")
        description = meta_content(text, "description")
        if description is None:
            self.add("warning", file, line, "meta-description", "No <meta name=\"description\">")
        elif description and "{" not in description and not (50 <= len(description) <= 160):
            self.add("info", file, line, "description-length",
                     f"Meta description is {len(description)} characters; 50-160 fits search snippets")
        robots = meta_content(text, "robots") or ""
        if "noindex" in robots.lower():
            self.add("warning", file, line, "noindex", "Page is marked noindex; remove it if this page should be found")
        if meta_content(text, "og:title", "property") is None and meta_content(text, "og:title") is None:
            self.add("info", file, line, "open-graph", "No Open Graph tags; shared links will have no preview card")
        if not re.search(r"rel\s*=\s*[\"']canonical[\"']", text, re.I):
            self.add("info", file, line, "canonical", "No canonical link; add one if the page is reachable at several URLs")

    def check_next_layout(self, text: str, file: str, find_line) -> None:
        metadata = re.search(r"export\s+(const\s+metadata\b|(async\s+)?function\s+generateMetadata\b)", text)
        if not metadata:
            self.add("error", file, 1, "title", "Root layout exports no metadata; pages have no <title>")
            return
        block = text[metadata.start():metadata.start() + 2000]
        if not re.search(r"\btitle\s*:", block):
            self.add("error", file, find_line(metadata.start()), "title", "Root metadata has no title")
        if not re.search(r"\bdescription\s*:", block):
            self.add("warning", file, find_line(metadata.start()), "meta-description", "Root metadata has no description")
        if not re.search(r"\bopenGraph\s*:", block):
            self.add("info", file, find_line(metadata.start()), "open-graph", "Root metadata has no openGraph; shared links will have no preview card")

    def check_file(self, path: Path) -> None:
        text = read_text(path)
        if not text:
            return
        file = rel(path, self.target)
        find_line = line_finder(text)
        name = path.name.lower()
        parts = [p.lower() for p in path.parts]
        suffix = path.suffix.lower()
        checked = False

        if suffix in {".html", ".htm", ".php", ".astro", ".vue", ".svelte"} and re.search(r"<html\b|<head\b", text, re.I):
            if "partials" not in parts and "components" not in parts and not re.search(r"<svelte:head|<Head\b", text):
                self.check_document(text, file, find_line)
                checked = True
        elif "app" in parts and NEXT_LAYOUT.match(name) and path.parent.name.lower() == "app":
            self.check_next_layout(text, file, find_line)
            checked = True
        elif "app" in parts and NEXT_PAGE.match(name) and "(" not in path.parent.name:
            checked = True
            if not re.search(r"export\s+(const\s+metadata\b|(async\s+)?function\s+generateMetadata\b)", text) \
                    and path.parent.name.lower() != "app":
                self.add("info", file, 1, "page-metadata",
                         "Page has no metadata export; it inherits the root title and description")

        if checked or (suffix in {".jsx", ".tsx"} and ("pages" in parts or "app" in parts)):
            self.files_checked += 1
            self.public_pages += 1
            h1s = [m.start() for m in re.finditer(r"<h1\b", text, re.I)]
            if len(h1s) > 1:
                self.add("warning", file, find_line(h1s[1]), "multiple-h1", f"{len(h1s)} <h1> elements; use one per page")

    def run(self) -> None:
        for path in iter_files(self.target, PAGE_SUFFIXES, SEO_SKIP_DIRS):
            if re.search(r"\.(test|spec|stories|d)\.\w+$", path.name) or path.name.endswith(".min.js"):
                continue
            if path.suffix.lower() in {".js", ".ts"} and not NEXT_LAYOUT.match(path.name.lower()):
                continue
            self.check_file(path)
        if self.target.is_dir() and self.public_pages:
            found = {p.name.lower() for p in iter_files(
                self.root, ("robots.txt", "robots.ts", "robots.js", "sitemap.xml", "sitemap.ts", "sitemap.js"), SEO_SKIP_DIRS)}
            if not found & {"robots.txt", "robots.ts", "robots.js"}:
                self.add("info", "(project)", None, "robots-txt", "No robots.txt (or app/robots.ts) found")
            if not found & {"sitemap.xml", "sitemap.ts", "sitemap.js"}:
                self.add("info", "(project)", None, "sitemap", "No sitemap.xml (or app/sitemap.ts) found")


def main() -> int:
    utf8_console()
    parser = base_parser("SEO checks for public pages (title, description, noindex, headings, sharing tags).")
    args = parser.parse_args()
    target = resolve_target(parser, args.project)
    checker = SEOChecker(target)
    checker.run()
    notes = ["image alt text and <html lang> are reported by accessibility_checker.py"]
    if not checker.files_checked:
        notes.append("no page files or documents found")
    return emit(args, "seo_checker", "SEO check", target, checker.findings, checker.files_checked, notes)


if __name__ == "__main__":
    raise SystemExit(main())
