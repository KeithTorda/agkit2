#!/usr/bin/env python3
"""API validator: OpenAPI specs and route handlers (Next.js, Express/Hono, FastAPI/Flask/Django, Laravel).

  error    OpenAPI spec that does not parse, has no version/paths, or an
           operation without responses
  warning  handler reads the request body with no visible validation, request
           body written straight to the database (mass assignment), stack
           traces sent to the client, path parameters missing from the spec
  info     operations without summary/operationId, handlers with no error
           handling (fine when the framework has a global handler)

Handlers are found by content (route definitions), not by file name.

Usage:
    python api_validator.py <project-or-file> [--json] [--fail-on error|warning|never] [--verbose]

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
# API checks
# ---------------------------------------------------------------------------
CODE_SUFFIXES = (".ts", ".js", ".mjs", ".cjs", ".py", ".php")
SPEC_NAME = re.compile(r"^(openapi|swagger)(\.[\w-]+)?\.(json|ya?ml)$|\.openapi\.(json|ya?ml)$", re.I)
HTTP_METHODS = ("get", "post", "put", "patch", "delete", "head", "options", "trace")
ROUTE_MARKERS = re.compile(
    r"export\s+(?:async\s+)?function\s+(GET|POST|PUT|PATCH|DELETE)\b"          # Next.js route handlers
    r"|\b(?:app|router|api|server|route|routes)\.(?:get|post|put|patch|delete|all|route)\(\s*[\"'`/]"  # Express/Hono/Fastify
    r"|@(?:app|router|api|bp|blueprint)\.(?:get|post|put|patch|delete|route)\("  # FastAPI/Flask
    r"|Route::(?:get|post|put|patch|delete|match|any|resource|apiResource)\("   # Laravel routes
    r"|extends\s+(?:Controller|BaseController)\b"                               # Laravel controllers
    r"|@api_view\(|\bAPIView\b|\bViewSet\b"                                     # Django REST
    r"|export\s+default\s+(?:async\s+)?function\s+handler\b",                   # Next.js pages/api
)
BODY_READ = re.compile(
    r"\breq\.body\b|\brequest\.json\(\)|\breq\.json\(\)|\bc\.req\.(?:json|parseBody|formData)\(\)"
    r"|\bawait\s+request\.formData\(\)|\$request->(?:all|input|post|except|only)\("
    r"|\$_(?:POST|REQUEST)\b|request\.(?:get_json|form|POST|data)\b")
VALIDATION = re.compile(
    r"(?<!JSON)(?<!qs)\.(?:safe)?[pP]arse(?:Async)?\(|\bz\.object\b|\bzValidator\b|\bJoi\.|\byup\.|\bv\.(?:parse|object)\b"
    r"|\bvalidate(?:Sync|Async)?\(|\bvalidationResult\(|\bcheckSchema\(|\bplainToInstance\(|\bIsString\(\)"
    r"|->validate(?:d)?\(|Validator::make\(|\bFormRequest\b|\w+Request\s+\$request|->validated\(\)"
    r"|\bBaseModel\b|from\s+fastapi\b|\bis_valid\(\)|\bSerializer\(|Schema\(\)\.load\(|\bajv\b|\bTypeBox\b|\bt\.Object\(",
    re.I)


class ApiValidator:
    def __init__(self, target: Path) -> None:
        self.target = target
        self.findings: list[dict[str, Any]] = []
        self.files_checked = 0
        self.specs = 0
        self.handlers = 0

    def add(self, severity: str, file: str, line: int | None, rule: str, message: str) -> None:
        self.findings.append(make_finding(severity, file, line, rule, message))

    # -- OpenAPI -----------------------------------------------------------------
    def check_spec(self, path: Path) -> None:
        text = read_text(path)
        file = rel(path, self.target)
        self.specs += 1
        if path.suffix.lower() != ".json":
            if not re.search(r"^(openapi|swagger)\s*:", text, re.M):
                self.add("error", file, 1, "spec-version", "No top-level openapi:/swagger: version")
            if not re.search(r"^paths\s*:", text, re.M):
                self.add("error", file, 1, "spec-paths", "No top-level paths:")
            self.add("info", file, None, "spec-yaml",
                     "YAML spec checked for structure only; run a full linter (e.g. npx @redocly/cli lint) for detail")
            return
        try:
            spec = json.loads(text)
        except json.JSONDecodeError as exc:
            self.add("error", file, exc.lineno, "spec-parse", f"Invalid JSON: {exc.msg}")
            return
        if not isinstance(spec, dict):
            self.add("error", file, 1, "spec-parse", "Spec root is not an object")
            return
        if "openapi" not in spec and "swagger" not in spec:
            self.add("error", file, 1, "spec-version", "No openapi/swagger version field")
        info = spec.get("info") if isinstance(spec.get("info"), dict) else {}
        if not info.get("title") or not info.get("version"):
            self.add("warning", file, 1, "spec-info", "info.title and info.version are required by OpenAPI")
        paths = spec.get("paths")
        if not isinstance(paths, dict):
            self.add("error", file, 1, "spec-paths", "No paths object")
            return
        for route, item in paths.items():
            if not isinstance(item, dict):
                continue
            shared = [p for p in item.get("parameters", []) if isinstance(p, dict)]
            for method in HTTP_METHODS:
                op = item.get(method)
                if not isinstance(op, dict):
                    continue
                label = f"{method.upper()} {route}"
                if not op.get("responses"):
                    self.add("error", file, None, "spec-responses", f"{label}: no responses defined")
                if not (op.get("summary") or op.get("description")):
                    self.add("info", file, None, "spec-summary", f"{label}: no summary or description")
                if not op.get("operationId"):
                    self.add("info", file, None, "spec-operation-id", f"{label}: no operationId (client generators need it)")
                params = shared + [p for p in op.get("parameters", []) if isinstance(p, dict)]
                declared = {p.get("name") for p in params if p.get("in") == "path"}
                has_refs = any("$ref" in p for p in params)
                for name in re.findall(r"\{([^}]+)\}", route):
                    if name not in declared and not has_refs:
                        self.add("warning", file, None, "spec-path-param", f"{label}: path parameter '{name}' is not declared")

    # -- handlers ----------------------------------------------------------------
    def check_handler(self, path: Path, text: str) -> None:
        file = rel(path, self.target)
        find_line = line_finder(text)
        self.handlers += 1
        body = BODY_READ.search(text)
        if body and not VALIDATION.search(text):
            self.add("warning", file, find_line(body.start()), "input-validation",
                     "Request body is read but no validation is visible (zod/valibot, FormRequest/validate(), pydantic...)")
        for m in re.finditer(r"::(?:create|forceCreate|insert)\(\s*\$request->all\(\)|->(?:fill|update|forceFill)\(\s*\$request->all\(\)", text):
            self.add("warning", file, find_line(m.start()), "mass-assignment",
                     "$request->all() written to the model; use $request->validated() or only([...])")
        for m in re.finditer(r"\.(?:create|update|upsert|insert|createMany)\(\s*\{\s*data\s*:\s*(?:req\.body|body|await\s+req(?:uest)?\.json\(\))\s*[,}]", text):
            self.add("warning", file, find_line(m.start()), "mass-assignment",
                     "Raw request body written to the database; parse it with a schema and pick the allowed fields")
        for m in re.finditer(r"\b(?:err|error|e|ex|exc|exception)\.stack\b|getTraceAsString\(\)|traceback\.format_exc\(\)", text):
            window = text[max(0, m.start() - 200):m.end() + 50]
            if re.search(r"json|send|response|Response|return|jsonify|res\.", window):
                self.add("warning", file, find_line(m.start()), "stack-leak",
                         "Stack trace appears to be sent in a response; log it server-side and return a generic message")
        uses_await = re.search(r"\bawait\b", text)
        handles = re.search(r"\btry\s*[:{]|\.catch\(|\bexcept\b|->onError|app\.onError|errorHandler|HTTPException|abort\(", text)
        if uses_await and not handles and not path.suffix == ".php":
            self.add("info", file, None, "error-handling",
                     "No try/catch in async handlers; fine if a framework-level error handler exists")

    def run(self) -> None:
        for path in iter_files(self.target, CODE_SUFFIXES + (".json", ".yaml", ".yml")):
            name = path.name
            if SPEC_NAME.search(name):
                self.files_checked += 1
                self.check_spec(path)
                continue
            if not name.lower().endswith(CODE_SUFFIXES) or re.search(r"\.(test|spec|d)\.\w+$|\.min\.js$", name):
                continue
            text = read_text(path)
            if ROUTE_MARKERS.search(text):
                self.files_checked += 1
                self.check_handler(path, text)


def main() -> int:
    utf8_console()
    parser = base_parser("Validate OpenAPI specs and API route handlers (validation, mass assignment, error leaks).")
    args = parser.parse_args()
    target = resolve_target(parser, args.project)
    validator = ApiValidator(target)
    validator.run()
    notes = [f"{validator.specs} spec file(s), {validator.handlers} handler file(s)"]
    if not validator.files_checked:
        notes.append("no OpenAPI spec or route handlers found")
    return emit(args, "api_validator", "API validation", target, validator.findings, validator.files_checked, notes)


if __name__ == "__main__":
    raise SystemExit(main())
