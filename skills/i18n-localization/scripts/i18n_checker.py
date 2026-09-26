#!/usr/bin/env python3
"""i18n checker: locale file completeness and likely hard-coded UI strings.

Locale layouts understood: locales/<lang>/<ns>.json, messages/<lang>.json
(next-intl), lang/<lang>.json and lang/<lang>/*.php keys are not parsed (PHP
arrays), *.po files (untranslated msgstr).

  error    invalid locale JSON, keys present in the base language but missing
           in another language
  warning  untranslated .po entries, likely hard-coded user-facing strings in
           files that do not use the i18n helper (only when the project uses i18n)
  info     extra keys that the base language does not have

The base language is "en" when present, otherwise the language with the most keys.
Hard-coded string scanning is skipped for projects with no i18n setup unless
--strict is given.

Usage:
    python i18n_checker.py <project> [--strict] [--json] [--fail-on error|warning|never] [--verbose]

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
# i18n checks
# ---------------------------------------------------------------------------
I18N_SKIP_DIRS = SKIP_DIRS | {"tests", "test", "spec", "specs", "__tests__", "e2e", "stories"}
LOCALE_DIRS = {"locales", "locale", "translations", "lang", "i18n", "messages", "intl", "l10n"}
LOCALE_CODE = re.compile(r"^[a-z]{2,3}([-_][A-Za-z]{2,4})?$")
CODE_SUFFIXES = {".tsx": "jsx", ".jsx": "jsx", ".vue": "markup", ".svelte": "markup", ".astro": "markup",
                 ".php": "markup", ".html": "markup", ".py": "python"}
I18N_USAGE = re.compile(
    r"\buseTranslations?\s*\(|(?<![\w$.])t\s*\(\s*[\"'`]|\$t\s*\(|\bgettext\s*\(|(?<![\w$])_\s*\(\s*[\"']"
    r"|\bFormattedMessage\b|\bi18n\.|\bTrans\b|(?<![\w$])__\s*\(\s*[\"']|@lang\s*\(|\btrans\s*\(|\btrans_choice\s*\(|\bgetTranslations\s*\(")
TEXT_NODE = re.compile(r">\s*([A-Z][A-Za-z][A-Za-z ,.!?'-]{2,80}?)\s*</")
TEXT_ATTR = re.compile(r"\b(?:title|placeholder|label|alt|aria-label)\s*=\s*[\"']([A-Z][A-Za-z ,.!?'-]{2,80})[\"']")
PY_FLASH = re.compile(r"\bflash\s*\(\s*[\"']([A-Z][^\"']{4,100})[\"']")


def flatten_keys(value: Any, prefix: str = "") -> set[str]:
    keys: set[str] = set()
    if not isinstance(value, dict):
        return keys
    for key, child in value.items():
        name = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(child, dict):
            keys.update(flatten_keys(child, name))
        else:
            keys.add(name)
    return keys


class I18nChecker:
    def __init__(self, target: Path, strict: bool) -> None:
        self.target = target
        self.strict = strict
        self.findings: list[dict[str, Any]] = []
        self.files_checked = 0
        self.languages: list[str] = []
        self.applicable = False

    def add(self, severity: str, file: str, line: int | None, rule: str, message: str) -> None:
        self.findings.append(make_finding(severity, file, line, rule, message))

    def locale_files(self) -> list[Path]:
        found = []
        for path in iter_files(self.target, (".json", ".po"), I18N_SKIP_DIRS):
            parts = {p.lower() for p in path.relative_to(self.target).parts[:-1]} if self.target.is_dir() else set()
            if parts & LOCALE_DIRS and path.name not in {"package.json", "tsconfig.json"}:
                found.append(path)
        return found

    def check_locales(self, files: list[Path]) -> None:
        # family (locale root folder) -> language -> namespace -> (keys, file label)
        families: dict[str, dict[str, dict[str, tuple[set[str], str]]]] = {}
        for path in files:
            file = rel(path, self.target)
            self.files_checked += 1
            if path.suffix == ".po":
                text = read_text(path)
                empty = len(re.findall(r'^msgid\s+"(?!")[^\n]*\nmsgstr\s+""\s*$(?!\n")', text, re.M))
                if empty:
                    self.add("warning", file, None, "po-untranslated", f"{empty} untranslated entr(y/ies) (empty msgstr)")
                continue
            try:
                data = json.loads(read_text(path))
            except json.JSONDecodeError as exc:
                self.add("error", file, exc.lineno, "locale-json", f"Invalid locale JSON: {exc.msg}")
                continue
            if LOCALE_CODE.match(path.stem):            # messages/en.json
                family, language, namespace = rel(path.parent, self.target), path.stem, "(file)"
            elif LOCALE_CODE.match(path.parent.name):   # locales/en/common.json
                family, language, namespace = rel(path.parent.parent, self.target), path.parent.name, path.stem
            else:
                continue
            families.setdefault(family, {}).setdefault(language, {})[namespace] = (flatten_keys(data), file)

        self.languages = sorted({lang for langs in families.values() for lang in langs})
        for family, locales in sorted(families.items()):
            if len(locales) < 2:
                continue
            base = "en" if "en" in locales else max(locales, key=lambda lang: sum(len(k) for k, _ in locales[lang].values()))
            for namespace in sorted(set().union(*(set(ns) for ns in locales.values()))):
                base_keys, _ = locales[base].get(namespace, (set(), ""))
                for language in sorted(locales):
                    if language == base:
                        continue
                    if namespace not in locales[language]:
                        if base_keys:
                            self.add("error", f"{family}/{language}", None, "missing-keys",
                                     f"No '{namespace}' file for '{language}' ({len(base_keys)} key(s) in '{base}')")
                        continue
                    keys, file = locales[language][namespace]
                    missing = sorted(base_keys - keys)
                    extra = sorted(keys - base_keys)
                    if missing:
                        self.add("error", file, None, "missing-keys",
                                 f"{len(missing)} key(s) missing vs '{base}': {', '.join(missing[:8])}{' ...' if len(missing) > 8 else ''}")
                    if extra:
                        self.add("info", file, None, "extra-keys",
                                 f"{len(extra)} key(s) not in '{base}': {', '.join(extra[:5])}")

    def project_uses_i18n(self, code_files: list[Path], locale_files: list[Path]) -> bool:
        if locale_files:
            return True
        for manifest in ("package.json", "composer.json"):
            text = read_text(self.target / manifest).lower() if self.target.is_dir() else ""
            if any(name in text for name in ("i18next", "next-intl", "react-intl", "vue-i18n", "@lingui", "svelte-i18n", "laravel-lang")):
                return True
        return any(I18N_USAGE.search(read_text(path)) for path in code_files[:300])

    def check_hardcoded(self, code_files: list[Path]) -> None:
        reported = 0
        for path in code_files:
            text = read_text(path)
            self.files_checked += 1
            if I18N_USAGE.search(text):
                continue  # file already uses the helper; remaining literals are usually intentional
            kind = CODE_SUFFIXES[path.suffix.lower()]
            patterns = (PY_FLASH,) if kind == "python" else (TEXT_NODE, TEXT_ATTR)
            find_line = line_finder(text)
            hits = []
            for pattern in patterns:
                for m in pattern.finditer(text):
                    value = m.group(1).strip()
                    if value.lower().startswith(("http", "todo")):
                        continue
                    hits.append((find_line(m.start()), value))
            if hits:
                first_line, first_value = hits[0]
                more = f" (+{len(hits) - 1} more)" if len(hits) > 1 else ""
                self.add("warning", rel(path, self.target), first_line, "hardcoded-string",
                         f"Likely hard-coded UI text '{first_value[:50]}'{more}; wrap it in the translation helper")
                reported += 1
            if reported >= 100:
                break

    def run(self) -> None:
        locale_files = self.locale_files()
        code_files = [p for p in iter_files(self.target, tuple(CODE_SUFFIXES), I18N_SKIP_DIRS)
                      if not re.search(r"\.(test|spec|stories|d)\.\w+$", p.name)]
        self.check_locales(locale_files)
        self.applicable = self.strict or self.project_uses_i18n(code_files, locale_files)
        if self.applicable:
            self.check_hardcoded(code_files)


def main() -> int:
    utf8_console()
    parser = base_parser("Check locale completeness and likely hard-coded UI strings.")
    parser.add_argument("--strict", action="store_true", help="scan hard-coded strings even when no i18n setup is detected")
    args = parser.parse_args()
    target = resolve_target(parser, args.project)
    checker = I18nChecker(target, args.strict)
    checker.run()
    notes = [f"languages: {', '.join(checker.languages) or 'none found'}"]
    if not checker.applicable:
        notes.append("no i18n framework or locale files detected; hard-coded string scan skipped (use --strict to force)")
    return emit(args, "i18n_checker", "i18n check", target, checker.findings, checker.files_checked, notes,
                {"applicable": checker.applicable, "languages": checker.languages})


if __name__ == "__main__":
    raise SystemExit(main())
