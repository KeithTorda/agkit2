#!/usr/bin/env python3
"""GEO checker: how quotable public pages are for AI answer engines.

Scores route entry points (HTML, Next.js app/pages routes, Astro/Vue/Svelte
pages, Blade views) on structure an answer engine can lift: one H1, H2
sections, JSON-LD, author and date on articles, FAQ/list/table content, direct
answer phrasing. It follows local imports (content.tsx, *.mdx) so thin route
wrappers are scored on the content they render, preferring the English locale.

The score is guidance. Low-scoring pages are reported as info and the script
exits 0 unless --min-score is given. Markdown docs, tests, layouts and
components are not scored.

Usage:
    python geo_checker.py <project> [--json] [--min-score N] [--verbose]

Exit codes: 0 ok, 1 average score below --min-score, 2 usage error.
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
# GEO scoring
# ---------------------------------------------------------------------------
GEO_SKIP_DIRS = SKIP_DIRS | {
    ".github", "test", "tests", "__tests__", "spec", "e2e", "components", "partials",
    "layouts", "includes", "storybook-static", "stories",
}
PAGE_SUFFIXES = {".html", ".htm", ".jsx", ".tsx", ".astro", ".vue", ".svelte", ".php"}
ARTICLE_SEGMENTS = {"blog", "blogs", "article", "articles", "post", "posts", "news"}


def _lower_parts(file_path: Path, root: Path | None = None) -> list[str]:
    path = file_path
    if root is not None:
        try:
            path = file_path.relative_to(root)
        except ValueError:
            pass
    return [part.lower() for part in path.parts]


def is_page_file(file_path: Path, root: Path | None = None) -> bool:
    """Return True only for route entry points, not layouts or components.

    Path parts are taken relative to root, so a project that happens to live
    under a folder named build/ or tests/ is still scanned.
    """
    suffix = file_path.suffix.lower()
    name_lower = file_path.name.lower()
    if suffix not in PAGE_SUFFIXES:
        return False
    parts = _lower_parts(file_path, root)
    if any(part in GEO_SKIP_DIRS for part in parts[:-1]):
        return False
    if suffix in {".html", ".htm"}:
        return True

    name = file_path.stem.lower()
    if name.endswith((".test", ".spec", ".stories")) or name.startswith(("test_", "spec_", "_")):
        return False

    if suffix == ".php":
        # Blade views under resources/views are pages; plain PHP only when it renders a document.
        if name_lower.endswith(".blade.php"):
            return "views" in parts and not {"layouts", "components", "partials", "errors", "vendor", "emails"} & set(parts)
        return False

    # Next.js App Router: only page.tsx/page.jsx is a public route entry.
    if "app" in parts:
        return name == "page"

    # Pages directories (Next.js pages router, Astro, Nuxt, SvelteKit-style routes).
    if "pages" in parts:
        route_parts = parts[parts.index("pages") + 1:]
        return "api" not in route_parts
    if "routes" in parts:
        return name in {"page", "index", "+page"}
    return False


def find_web_pages(project_path: Path) -> list[Path]:
    """Find public-facing route source files deterministically."""
    root = project_path if project_path.is_dir() else project_path.parent
    files = [path for path in iter_files(project_path, tuple(PAGE_SUFFIXES)) if is_page_file(path, root)]
    return sorted(set(files), key=lambda item: item.as_posix())[:200]


def _read_route_content(file_path: Path) -> str:
    """Read a route and its directly imported local content modules.

    Next.js route entries often delegate all visible markup to content.tsx or
    localized MDX files. Static analysis must follow those imports or it scores
    a thin wrapper instead of the page users and crawlers receive.
    """
    content = read_text(file_path)
    import_paths = re.findall(r"(?:import|from)\s+(?:[^'\"]+?\s+from\s+)?['\"](\.{1,2}/[^'\"]+)['\"]", content)
    extensions = ("", ".tsx", ".ts", ".jsx", ".js", ".mdx", ".md")
    seen = {file_path.resolve()}
    resolved_imports = []
    for import_path in import_paths:
        base = (file_path.parent / import_path).resolve()
        candidates = [Path(f"{base}{extension}") for extension in extensions]
        candidates.extend(base / f"index{extension}" for extension in extensions[1:])
        for candidate in candidates:
            if not candidate.is_file() or candidate.resolve() in seen:
                continue
            seen.add(candidate.resolve())
            resolved_imports.append(candidate)
            break

    # A localized wrapper renders one locale at a time. Analyze the canonical
    # English source rather than concatenating mutually exclusive H1s.
    canonical_locale = [item for item in resolved_imports if ".en." in item.name.lower()]
    selected = canonical_locale or resolved_imports
    chunks = [content]
    chunks.extend(read_text(item) for item in selected)
    return "\n".join(chunks)


def check_page(file_path: Path, project_path: Path | None = None) -> dict:
    """Score a route source file without requiring article metadata on product docs."""
    try:
        content = _read_route_content(file_path)
    except (OSError, ValueError) as exc:
        return {"file": str(file_path), "passed": [], "issues": [f"Error: {exc}"], "score": 0}

    issues = []
    passed = []
    optional_points = 0
    lower_content = content.lower()
    parts = set(_lower_parts(file_path, project_path))
    is_article = bool(parts & ARTICLE_SEGMENTS)
    is_root_landing = file_path.parent.name.lower() in {"app", "pages"} or file_path.stem.lower() == "index"

    heading_content = re.sub(r"```.*?```", "", content, flags=re.S)
    heading_content = re.sub(r"`(?:\\.|[^`])*`", "", heading_content, flags=re.S)
    heading_content = re.sub(r"<!--.*?-->", "", heading_content, flags=re.S)
    h1_count = len(re.findall(r"<h1[^>]*>", heading_content, re.I))
    h1_count += len(re.findall(r"^#\s+\S", heading_content, re.M))
    h2_count = len(re.findall(r"<h2[^>]*>", heading_content, re.I))
    h2_count += len(re.findall(r"^##\s+\S", heading_content, re.M))
    required_total = 1 if is_root_landing else 2
    required_passed = 0

    if h1_count == 1:
        passed.append("Single H1 heading (clear topic)")
        required_passed += 1
    elif h1_count == 0:
        issues.append("No H1 heading - page topic unclear")
    else:
        issues.append(f"Multiple H1 headings ({h1_count}) - topic is ambiguous")

    if not is_root_landing:
        repeated_heading = h2_count >= 1 and ".map(" in content
        if h2_count >= 2 or repeated_heading:
            detail = "dynamic repeated" if repeated_heading and h2_count < 2 else str(h2_count)
            passed.append(f"{detail} H2 subheadings (good structure)")
            required_passed += 1
        else:
            issues.append("Add at least two H2 subheadings for scannable content")

    if "application/ld+json" in lower_content:
        passed.append("JSON-LD structured data found")
        optional_points += 10
    if re.search(r'"@type"\s*:\s*"(Organization|Person|Brand|Article|FAQPage|LocalBusiness|GovernmentOrganization|Product)"', content, re.I):
        passed.append("Recognizable schema entity found")
        optional_points += 5

    author_patterns = ("author", "byline", "written-by", "contributor", 'rel="author"')
    has_author = any(pattern in lower_content for pattern in author_patterns)
    date_patterns = ("datepublished", "datemodified", "datetime=", "pubdate", "article:published")
    has_date = any(pattern in lower_content for pattern in date_patterns)
    if is_article:
        required_total += 2
        if has_author:
            passed.append("Author attribution found")
            required_passed += 1
        else:
            issues.append("Article has no author attribution")
        if has_date:
            passed.append("Publication date found")
            required_passed += 1
        else:
            issues.append("Article has no publication date")
    else:
        optional_points += 3 if has_author else 0
        optional_points += 3 if has_date else 0

    optional_checks = (
        (r"<details|faq|frequently.?asked|\"FAQPage\"", "FAQ section detected", 5),
        (r"<(ul|ol)[^>]*>", "Structured list content found", 5),
        (r"<table[^>]*>", "Comparison table found", 5),
        (r"\d+%|according to|data\s+(shows|reveals)|\d+x\s+(faster|better|more)", "Data-backed claims found", 5),
        (r"is defined as|refers to|means that|in short,|simply put,|<dfn", "Direct-answer phrasing found", 5),
    )
    for pattern, label, points in optional_checks:
        if re.search(pattern, content, re.I):
            passed.append(label)
            optional_points += points

    base_score = (required_passed / required_total * 70) if required_total else 70
    score = min(100, round(base_score + min(optional_points, 30)))
    display = rel(file_path, project_path) if project_path else file_path.as_posix()
    return {"file": display, "passed": passed, "issues": issues, "score": score}


def main() -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description="Score public pages for AI-citation readiness (advisory).")
    parser.add_argument("project", nargs="?", default=".", help="project directory (default: .)")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--min-score", type=int, default=0,
                        help="exit 1 when the average score is below this (default: 0 = advisory only)")
    parser.add_argument("--verbose", "-v", action="store_true", help="list passed checks too")
    args = parser.parse_args()
    target = resolve_target(parser, args.project)
    root = target if target.is_dir() else target.parent

    pages = find_web_pages(target)
    results = [check_page(page, root) for page in pages]
    average = round(sum(r["score"] for r in results) / len(results)) if results else None
    failed = average is not None and args.min_score > 0 and average < args.min_score

    if args.json:
        print(json.dumps({"script": "geo_checker", "project": str(target), "pages_checked": len(results),
                          "average_score": average, "min_score": args.min_score, "passed": not failed,
                          "pages": results}, indent=2, ensure_ascii=False))
        return 1 if failed else 0

    print(f"GEO check: {target}")
    if not results:
        print("No public page entry points found (HTML, app/**/page.tsx, pages/, routes/, Blade views).")
        return 0
    print(f"Scored {len(results)} page(s); average {average}%. Guidance only: 60%+ is reasonable, 80%+ is strong.")
    for result in sorted(results, key=lambda r: r["score"]):
        marker = "ok " if result["score"] >= 60 else "low"
        print(f"  {marker} {result['score']:>3}%  {result['file']}")
        if result["score"] < 60 or args.verbose:
            for issue in result["issues"][:3]:
                print(f"            - {issue}")
        if args.verbose:
            for item in result["passed"]:
                print(f"            + {item}")
    low = sum(r["score"] < 60 for r in results)
    gate = f"min-score {args.min_score}" if args.min_score else "advisory"
    print(f"\nResult: {'FAIL' if failed else 'PASS'} - average {average}%, {low} of {len(results)} page(s) below 60% ({gate})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
