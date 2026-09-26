#!/usr/bin/env python3
"""Database schema validator: Prisma (single or multi-file), Drizzle, Laravel migrations, raw SQL.

  error    a Prisma model with no identifier (@id, @@id, @unique or @@unique),
           a SQL CREATE TABLE with no primary key
  warning  Laravel foreignId() without constrained()/references() (no FK
           constraint), Drizzle table with no primary key
  info     foreign-key columns without an index (Prisma does not add one on
           Postgres), models without createdAt, non-PascalCase model names

Usage:
    python schema_validator.py <project-or-file> [--json] [--fail-on error|warning|never] [--verbose]

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
# Schema checks
# ---------------------------------------------------------------------------
PRISMA_SCALARS = {"String", "Int", "BigInt", "Float", "Decimal", "Boolean", "DateTime", "Json", "Bytes"}


class SchemaValidator:
    def __init__(self, target: Path) -> None:
        self.target = target
        self.findings: list[dict[str, Any]] = []
        self.files_checked = 0
        self.kinds: dict[str, int] = {}

    def add(self, severity: str, file: str, line: int | None, rule: str, message: str) -> None:
        self.findings.append(make_finding(severity, file, line, rule, message))

    def count(self, kind: str) -> None:
        self.files_checked += 1
        self.kinds[kind] = self.kinds.get(kind, 0) + 1

    def check_prisma(self, path: Path, text: str) -> None:
        self.count("prisma")
        file = rel(path, self.target)
        find_line = line_finder(text)
        clean = re.sub(r"//[^\n]*", lambda m: " " * len(m.group(0)), text)
        mysql_fk_mode = bool(re.search(r"provider\s*=\s*\"mysql\"", clean)) and "relationMode" not in clean
        for model in re.finditer(r"^\s*model\s+(\w+)\s*\{(.*?)^\s*\}", clean, re.S | re.M):
            name, body = model.group(1), model.group(2)
            line = find_line(model.start(1))
            if not re.search(r"@id\b|@@id\b|@unique\b|@@unique\b", body):
                self.add("error", file, line, "prisma-identifier",
                         f"Model '{name}' has no @id, @@id or unique field; Prisma requires one")
            if not name[0].isupper():
                self.add("info", file, line, "prisma-naming",
                         f"Model '{name}' is not PascalCase; use @@map(\"{name}\") to keep the table name")
            if not re.search(r"^\s*(createdAt|created_at)\s", body, re.M):
                self.add("info", file, line, "prisma-timestamps", f"Model '{name}' has no createdAt field")

            fields: dict[str, str] = {}
            for field in re.finditer(r"^\s*(\w+)\s+(\w+)(\??|\[\])?([^\n]*)$", body, re.M):
                if field.group(1).startswith("@@"):
                    continue
                fields[field.group(1)] = field.group(4)
            fk_columns: set[str] = set()
            for relation in re.finditer(r"@relation\([^)]*fields\s*:\s*\[([^\]]+)\]", body):
                fk_columns.update(col.strip() for col in relation.group(1).split(","))
            indexed_first: set[str] = set()
            for index in re.finditer(r"@@(?:index|unique|id)\(\s*(?:fields\s*:\s*)?\[\s*([\w]+)", body):
                indexed_first.add(index.group(1))
            for column, attrs in fields.items():
                if re.search(r"@id\b|@unique\b", attrs):
                    indexed_first.add(column)
            for column in sorted(fk_columns - indexed_first):
                if mysql_fk_mode:
                    continue  # MySQL/InnoDB creates an index for foreign keys automatically
                self.add("info", file, find_line(model.start() + body.find(column)), "prisma-fk-index",
                         f"'{name}.{column}' is a foreign key without @@index([{column}]); joins and cascades scan the table")

    def check_drizzle(self, path: Path, text: str) -> None:
        self.count("drizzle")
        file = rel(path, self.target)
        find_line = line_finder(text)
        for table in re.finditer(r"(?:pgTable|mysqlTable|sqliteTable)\(\s*[\"'](\w+)[\"']", text):
            depth_end = text.find("\n)", table.end())
            chunk = text[table.end(): depth_end if depth_end != -1 else table.end() + 4000]
            if ".primaryKey()" not in chunk and "primaryKey(" not in chunk:
                self.add("warning", file, find_line(table.start()), "drizzle-primary-key",
                         f"Table '{table.group(1)}' has no primary key")

    def check_laravel_migration(self, path: Path, text: str) -> None:
        self.count("laravel")
        file = rel(path, self.target)
        find_line = line_finder(text)
        for stmt in re.finditer(r"\$table->foreignId\(\s*[\"'](\w+)[\"']\s*\)([^;]*);", text):
            if not re.search(r"->(constrained|references)\(", stmt.group(2)):
                self.add("warning", file, find_line(stmt.start()), "laravel-fk-constraint",
                         f"foreignId('{stmt.group(1)}') has no ->constrained(); no foreign key is created")
        for stmt in re.finditer(r"\$table->unsignedBigInteger\(\s*[\"'](\w+_id)[\"']\s*\)([^;]*);", text):
            column = stmt.group(1)
            if not re.search(rf"->foreign\(\s*[\"']{column}[\"']", text) and "->index(" not in stmt.group(2):
                self.add("info", file, find_line(stmt.start()), "laravel-fk-index",
                         f"'{column}' looks like a foreign key but has no ->foreign() or ->index(); prefer foreignId()->constrained()")
        if re.search(r"Schema::create\(", text) and not re.search(r"->(id|increments|bigIncrements|uuid|ulid)\(|->primary\(", text):
            self.add("warning", file, find_line(text.find("Schema::create")), "laravel-primary-key",
                     "Schema::create without id()/primary(); the table has no primary key")

    def check_sql(self, path: Path, text: str) -> None:
        self.count("sql")
        file = rel(path, self.target)
        find_line = line_finder(text)
        clean = re.sub(r"--[^\n]*|/\*.*?\*/", lambda m: " " * len(m.group(0)), text, flags=re.S)
        for table in re.finditer(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`\"\[]?([\w.]+)[`\"\]]?\s*\(", clean, re.I):
            end = matching_paren(clean, table.end() - 1)
            body = clean[table.end():end]
            if not re.search(r"PRIMARY\s+KEY", body, re.I):
                self.add("error", file, find_line(table.start()), "sql-primary-key",
                         f"CREATE TABLE {table.group(1)} has no PRIMARY KEY")
            for column in re.finditer(r"^\s*[`\"]?(\w+_id)[`\"]?\s+\w+", body, re.M | re.I):
                name = column.group(1)
                if not re.search(rf"REFERENCES|FOREIGN\s+KEY\s*\(\s*[`\"]?{name}", body, re.I) and \
                        not re.search(rf"CREATE\s+(UNIQUE\s+)?INDEX[^;]*\(\s*[`\"]?{name}", clean, re.I):
                    self.add("info", file, find_line(table.end() + column.start()), "sql-fk",
                             f"{table.group(1)}.{name} has no REFERENCES constraint or index")

    def run(self) -> None:
        for path in iter_files(self.target, (".prisma", ".ts", ".js", ".php", ".sql")):
            name = path.name.lower()
            if name.endswith(".prisma"):
                self.check_prisma(path, read_text(path))
            elif name.endswith(".sql"):
                self.check_sql(path, read_text(path))
            elif name.endswith(".php"):
                if "migrations" in [p.lower() for p in path.parts]:
                    self.check_laravel_migration(path, read_text(path))
            elif re.search(r"schema|table|db", name) and not re.search(r"\.(test|spec|d)\.", name):
                text = read_text(path)
                if re.search(r"from\s+[\"']drizzle-orm/", text):
                    self.check_drizzle(path, text)


def matching_paren(text: str, open_index: int) -> int:
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i
    return len(text)


def main() -> int:
    utf8_console()
    parser = base_parser("Validate database schemas (Prisma, Drizzle, Laravel migrations, SQL).")
    args = parser.parse_args()
    target = resolve_target(parser, args.project)
    validator = SchemaValidator(target)
    validator.run()
    kinds = ", ".join(f"{count} {kind}" for kind, count in sorted(validator.kinds.items())) or "none"
    notes = [f"schema files: {kinds}"]
    return emit(args, "schema_validator", "Schema validation", target, validator.findings, validator.files_checked, notes)


if __name__ == "__main__":
    raise SystemExit(main())
