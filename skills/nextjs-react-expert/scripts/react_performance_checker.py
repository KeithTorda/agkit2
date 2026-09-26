#!/usr/bin/env python3
"""React / Next.js correctness and performance checker (static, stdlib only).

  error    Next.js App Router mistakes that break the build or runtime:
           'use client' file exporting metadata, async client component,
           server page/layout importing client hooks, error.tsx without 'use client'
  warning  list items rendered by .map() without a key, independent sequential
           awaits (request waterfall), whole-library icon imports
  info     <img> instead of next/image, explicit /index barrel imports, fetch in
           useEffect, index used as key, very large client components

Memoization is not checked: with the React Compiler, manual memo is the exception.

Usage:
    python react_performance_checker.py <project> [--json] [--fail-on error|warning|never] [--verbose]
    (--fail-on-warnings is kept as an alias for --fail-on warning)

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
# React / Next.js checks
# ---------------------------------------------------------------------------
JSX_ATTRS = r"((?:[^>\"'{}]|\"[^\"]*\"|'[^']*'|\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})*)"
USE_CLIENT = re.compile(r"^\s*(?:(?://[^\n]*|/\*.*?\*/)\s*)*[\"']use client[\"']", re.S)
CLIENT_HOOK_IMPORT = re.compile(
    r"import\s*\{[^}]*\b(useState|useEffect|useReducer|useLayoutEffect|useRef|useContext|useTransition|useOptimistic|useActionState)\b[^}]*\}\s*from\s*[\"']react[\"']")
SERVER_ENTRY_FILES = {"page", "layout", "template", "not-found", "loading", "default"}
CLIENT_ONLY_FILES = {"error", "global-error"}
DECL_AWAIT = re.compile(r"^\s*(?:const|let|var)\s+(.+?)\s*=\s*await\s+(.+)$")
AWAIT_CALL = re.compile(r"^(?:new\s+)?[\w$.?]+(?:<[^>]*>)?\s*\(")


def full_statement(lines: list[str], start: int, limit: int = 30) -> str:
    """The expression that starts on lines[start], extended until its brackets balance."""
    parts, depth = [], 0
    for line in lines[start:start + limit]:
        parts.append(line)
        depth += line.count("(") + line.count("{") + line.count("[") - line.count(")") - line.count("}") - line.count("]")
        if depth <= 0:
            break
    statement = "\n".join(parts)
    return statement.split("=", 1)[1] if "=" in statement else statement


class PerformanceChecker:
    """Kept as a class so tests and other scripts can drive it directly."""

    def __init__(self, project_path: str) -> None:
        self.project_path = Path(project_path).resolve()
        self.findings: list[dict[str, Any]] = []
        self.files_checked = 0
        self.scan_roots = self._discover_scan_roots()
        self.is_next = any(self._package_has(root, '"next"') for root in self._package_dirs())

    # Backwards-compatible views used by older callers and tests.
    @property
    def issues(self) -> list[dict[str, Any]]:
        return [f for f in self.findings if f["severity"] == "error"]

    @property
    def warnings(self) -> list[dict[str, Any]]:
        return [f for f in self.findings if f["severity"] == "warning"]

    def _package_dirs(self) -> list[Path]:
        dirs = [self.project_path, self.project_path / "web"]
        for group in ("apps", "packages"):
            parent = self.project_path / group
            if parent.is_dir():
                dirs.extend(sorted(p for p in parent.iterdir() if p.is_dir()))
        return [d for d in dirs if (d / "package.json").is_file()]

    @staticmethod
    def _package_has(base: Path, needle: str) -> bool:
        return needle in read_text(base / "package.json")

    def _discover_scan_roots(self) -> list[Path]:
        """Prefer React source roots over generated or unrelated files."""
        candidates = []
        for base in self._package_dirs():
            if not (self._package_has(base, '"next"') or self._package_has(base, '"react"')):
                continue
            source = base / "src"
            candidates.append(source if source.is_dir() else base)
        return candidates or [self.project_path]

    def _iter_files(self, extensions: Iterable[str]) -> Iterator[Path]:
        seen: set[Path] = set()
        suffixes = tuple(f".{ext.lstrip('.')}" for ext in extensions)
        for root in self.scan_roots:
            for path in iter_files(root, suffixes):
                resolved = path.resolve()
                if resolved in seen or path.name.endswith(".d.ts"):
                    continue
                seen.add(resolved)
                yield path

    def add(self, severity: str, path: Path, line: int | None, rule: str, message: str) -> None:
        self.findings.append(make_finding(severity, rel(path, self.project_path), line, rule, message))

    # -- checks ----------------------------------------------------------------
    def check_file(self, path: Path) -> None:
        text = read_text(path)
        if not text:
            return
        self.files_checked += 1
        find_line = line_finder(text)
        is_client = bool(USE_CLIENT.match(text))
        parts = [p.lower() for p in path.parts]
        in_app_router = "app" in parts and "pages" not in parts[parts.index("app"):]
        stem = path.stem.lower()
        is_test = bool(re.search(r"\.(test|spec|stories)$", stem)) or "__tests__" in parts

        if self.is_next and in_app_router:
            if is_client and re.search(r"export\s+(const\s+metadata\b|(async\s+)?function\s+generateMetadata\b)", text):
                self.add("error", path, find_line(text.find("export")), "client-metadata",
                         "'use client' file exports metadata/generateMetadata; Next.js rejects this. Move metadata to a server file")
            if is_client and re.search(r"export\s+default\s+async\s+function", text):
                self.add("error", path, find_line(text.find("export default async")), "async-client-component",
                         "Client components cannot be async; fetch in a server component or use a data hook")
            if stem in SERVER_ENTRY_FILES and not is_client:
                hook = CLIENT_HOOK_IMPORT.search(text)
                if hook:
                    self.add("error", path, find_line(hook.start()), "server-client-hook",
                             f"Server {stem}.tsx imports {hook.group(1)}; add 'use client' or move the stateful part into a client component")
            if stem in CLIENT_ONLY_FILES and not is_client:
                self.add("error", path, 1, "error-boundary-client", f"{path.name} must start with 'use client'")

        # .map() rendering without key.
        for m in re.finditer(r"\.map\(\s*(?:async\s*)?\(?[^()=]*\)?\s*=>\s*(?:\{\s*return\s*)?\(?\s*<([A-Za-z][\w.]*)?" + JSX_ATTRS + r"/?>", text):
            tag, attrs = m.group(1), m.group(2) or ""
            if not tag:
                self.add("warning", path, find_line(m.start()), "map-key",
                         "Fragment <> returned from .map() cannot take a key; use <Fragment key=...>")
            elif not re.search(r"\bkey\s*=", attrs) and not re.search(r"\{\s*\.\.\.", attrs):
                self.add("warning", path, find_line(m.start()), "map-key",
                         f"<{tag}> rendered in .map() without a key")
        for m in re.finditer(r"\bkey\s*=\s*\{\s*(index|idx|i)\s*\}", text):
            self.add("info", path, find_line(m.start()), "index-key",
                     "Array index as key; use a stable id if the list can reorder or change")

        # Request waterfalls: two consecutive `const x = await call(...)` where the second call
        # does not use what the first returned. Awaiting an existing promise variable is not a waterfall.
        if not is_test:
            lines = text.split("\n")
            i = 0
            while i < len(lines) - 1:
                first, second = DECL_AWAIT.match(lines[i]), DECL_AWAIT.match(lines[i + 1])
                if first and second and AWAIT_CALL.match(first.group(2)) and AWAIT_CALL.match(second.group(2)):
                    names = re.findall(r"[A-Za-z_$][\w$]*", re.sub(r":\s*[\w$]+", "", first.group(1)))
                    statement = full_statement(lines, i + 1)
                    if names and not any(re.search(rf"(?<![\w$.]){re.escape(n)}\b", statement) for n in names):
                        self.add("warning", path, i + 1, "waterfall",
                                 "Sequential awaits that do not depend on each other; run them with Promise.all")
                        while i < len(lines) - 1 and DECL_AWAIT.match(lines[i + 1]):
                            i += 1
                i += 1

        # Bundle size.
        for m in re.finditer(r"import\s+\*\s+as\s+\w+\s+from\s+[\"'](lucide-react|react-icons/\w+|@mui/icons-material|@heroicons/react/[\w/]+|@tabler/icons-react)[\"']", text):
            self.add("warning", path, find_line(m.start()), "icon-namespace-import",
                     f"import * from '{m.group(1)}' pulls every icon into the bundle; import the icons you use")
        for m in re.finditer(r"(?:import\s+\w+\s+from|require\()\s*[\"']lodash[\"']", text):
            self.add("info", path, find_line(m.start()), "lodash-default-import",
                     "Default lodash import includes the whole library; import per method or use lodash-es")
        for m in re.finditer(r"from\s+[\"'](?:@/|~/|\.{1,2}/)[^\"']*/index[\"']", text):
            self.add("info", path, find_line(m.start()), "barrel-import",
                     "Import through an explicit /index barrel; importing the file directly keeps chunks smaller")
        if self.is_next and re.search(r"<img\b", text) and "next/image" not in text:
            self.add("info", path, find_line(text.find("<img")), "next-image",
                     "<img> in a Next.js app; next/image adds sizing, lazy loading and modern formats")
        for m in re.finditer(r"\buseEffect\(", text):
            window = text[m.end():m.end() + 600]
            if re.search(r"\bfetch\(|axios\.", window.split("}, [")[0]):
                self.add("info", path, find_line(m.start()), "effect-fetch",
                         "Data fetched in useEffect; a server component or TanStack Query/SWR avoids waterfalls and duplicate requests")
                break
        if is_client and len(text) > 40_000:
            self.add("info", path, 1, "large-client-component",
                     f"Client component is {len(text) // 1024} KB of source; split it or load heavy parts with dynamic()")

    def run(self) -> bool:
        """Run all checks. Returns True when there are no error-level findings."""
        self.findings = []
        self.files_checked = 0
        for path in self._iter_files(["ts", "tsx", "js", "jsx"]):
            if path.name.endswith((".min.js", ".config.js", ".config.ts", ".config.mjs")):
                continue
            self.check_file(path)
        return not self.issues


def main() -> int:
    utf8_console()
    parser = base_parser("React / Next.js correctness and performance checks.")
    parser.add_argument("--fail-on-warnings", action="store_true", help="alias for --fail-on warning")
    args = parser.parse_args()
    if args.fail_on_warnings:
        args.fail_on = "warning"
    target = resolve_target(parser, args.project)
    if not target.is_dir():
        parser.error(f"expected a project directory: {target}")
    checker = PerformanceChecker(str(target))
    checker.run()
    roots = ", ".join(rel(r, target) or "." for r in checker.scan_roots)
    notes = [f"scanned: {roots}" + ("" if checker.is_next else " (no Next.js dependency found; Next-specific checks skipped)")]
    return emit(args, "react_performance_checker", "React performance", target, checker.findings, checker.files_checked, notes)


if __name__ == "__main__":
    raise SystemExit(main())
