#!/usr/bin/env python3
"""Static accessibility audit for HTML, JSX/TSX, Vue, Svelte, Astro and PHP/Blade templates.

Reports only what can be read from source, with file:line:

  error    image without alt, form field without a label, button or link with no
           accessible name, <html> without lang, viewport that disables zoom
  warning  click handlers on non-interactive elements without role/tabindex/key
           handler, positive tabindex, autoplay media without muted, iframe
           without title, aria-hidden on focusable elements, document without
           <title>, duplicate ids
  info     no skip link in a full document

Component tags (<Button>, <Input>) are not treated as native elements, and spread
props ({...props}) are assumed to carry the missing attribute. Runtime checks
(contrast of rendered colours, focus order) need a browser: see
playwright_runner.py --a11y or Lighthouse.

Usage:
    python accessibility_checker.py <project-or-file> [--json] [--fail-on error|warning|never]

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
# Accessibility checks
# ---------------------------------------------------------------------------
MARKUP_SUFFIXES = (".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".php")
TAG_ATTRS = r"((?:[^>\"'{}]|\"[^\"]*\"|'[^']*'|\{(?:[^{}]|\{[^{}]*\})*\})*)"
ICON_COMPONENT = re.compile(r"^(Icon\w*|\w*Icon|Lucide\w*|Fa[A-Z]\w*|Hi[A-Z]\w*|Md[A-Z]\w*|Io[A-Z]\w*|Bi[A-Z]\w*|Svg\w*)$")
NAME_ATTR = re.compile(r"\b(aria-label|aria-labelledby|title|:aria-label|v-bind:aria-label)\s*=", re.I)
SPREAD = re.compile(r"\{\s*\.\.\.")
SKIP_INPUT_TYPES = {"hidden", "submit", "button", "reset", "image"}


def attr_value(attrs: str, name: str) -> str | None:
    match = re.search(rf"(?<![\w:-]){name}\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|\{{([^{{}}]*)\}}|([^\s>]+))", attrs, re.I)
    if not match:
        return None
    return next(g for g in match.groups() if g is not None)


def has_attr(attrs: str, name: str) -> bool:
    return re.search(rf"(?<![\w:-])(?::|v-bind:)?{name}(\s*=|\s|$|/)", attrs, re.I) is not None


def has_accessible_text(body: str) -> bool:
    """True when element content gives it a name (or might, via an expression)."""
    for svg in re.finditer(r"<svg\b.*?</svg\s*>", body, re.S | re.I):
        if re.search(r"<title>\s*\S", svg.group(0), re.I):
            return True
    for img in re.finditer(r"<img\b" + TAG_ATTRS + ">", body, re.I):
        alt = attr_value(img.group(1), "alt")
        if alt and alt.strip():
            return True
    stripped = re.sub(r"<svg\b.*?</svg\s*>", " ", body, flags=re.S | re.I)
    stripped = re.sub(r"<i\b[^>]*>\s*</i\s*>", " ", stripped, flags=re.I)
    for comp in re.finditer(r"<([A-Z][\w.]*)", stripped):
        if not ICON_COMPONENT.match(comp.group(1).split(".")[-1]):
            return True  # unknown component: may render text
    if re.search(r"\{[^{}]*\}|@lang|__\(|\{\{", stripped):
        return True  # expression: text decided at runtime
    text = re.sub(r"<[^>]+>", " ", stripped)
    text = re.sub(r"&nbsp;|&#160;", " ", text)
    return bool(text.strip())


class A11yChecker:
    def __init__(self, target: Path) -> None:
        self.target = target
        self.findings: list[dict[str, Any]] = []
        self.files_checked = 0

    def add(self, severity: str, file: str, line: int | None, rule: str, message: str) -> None:
        self.findings.append(make_finding(severity, file, line, rule, message))

    def check_file(self, path: Path) -> None:
        text = read_text(path)
        if not text:
            return
        self.files_checked += 1
        file = rel(path, self.target)
        find_line = line_finder(text)
        is_jsx = path.suffix.lower() in {".jsx", ".tsx"}
        # Remove comments so commented-out markup is not reported (keep offsets).
        text = re.sub(r"<!--.*?-->|\{/\*.*?\*/\}", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)
        lowered = text.lower()

        label_for = {v for v in re.findall(r"\b(?:for|htmlFor)\s*=\s*[\"'{]\s*[\"']?([\w:.-]+)", text)}
        label_spans = [(m.start(), m.end()) for m in re.finditer(r"<label\b.*?</label\s*>", text, re.S | re.I)]
        uses_next_image = bool(re.search(r"from\s+[\"'](next/image|astro:assets|@unpic/\w+)[\"']", text))

        # Images.
        img_tags = r"<(img" + (r"|Image" if uses_next_image else "") + r")\b" + TAG_ATTRS + ">"
        for m in re.finditer(img_tags, text):
            attrs = m.group(2)
            if has_attr(attrs, "alt") or SPREAD.search(attrs) or re.search(r"aria-hidden\s*=\s*[\"'{]?\s*true|role\s*=\s*[\"']presentation", attrs, re.I):
                continue
            self.add("error", file, find_line(m.start()), "img-alt",
                     f"<{m.group(1)}> without alt (use alt=\"\" only for decorative images)")

        # Form fields.
        for m in re.finditer(r"<(input|select|textarea)\b" + TAG_ATTRS + ">", text):
            tag, attrs = m.group(1), m.group(2)
            input_type = (attr_value(attrs, "type") or "text").strip().lower()
            if tag == "input" and input_type in SKIP_INPUT_TYPES:
                if input_type == "image" and not has_attr(attrs, "alt"):
                    self.add("error", file, find_line(m.start()), "img-alt", "<input type=\"image\"> without alt")
                continue
            if NAME_ATTR.search(attrs) or SPREAD.search(attrs):
                continue
            field_id = attr_value(attrs, "id")
            if field_id and field_id.strip("\"' ") in label_for:
                continue
            if any(start < m.start() < end for start, end in label_spans):
                continue
            hint = " (placeholder is not a label)" if has_attr(attrs, "placeholder") else ""
            self.add("error", file, find_line(m.start()), "form-label",
                     f"<{tag}> has no label, aria-label or aria-labelledby{hint}")

        # Buttons and links need a name.
        for m in re.finditer(r"<(button|a)\b" + TAG_ATTRS + r">(.*?)</\1\s*>", text, re.S):
            tag, attrs, body = m.group(1), m.group(2), m.group(3)
            if tag == "a" and not has_attr(attrs, "href"):
                if re.search(r"\bon[cC]lick\s*=", attrs):
                    self.add("warning", file, find_line(m.start()), "anchor-button",
                             "<a> with a click handler but no href is not keyboard reachable; use <button>")
                continue
            if NAME_ATTR.search(attrs) or SPREAD.search(attrs) or has_accessible_text(body):
                continue
            what = "Button" if tag == "button" else "Link"
            self.add("error", file, find_line(m.start()), "control-name",
                     f"{what} has no accessible name (icon-only? add aria-label or visually hidden text)")

        # Document-level checks (raw documents and framework root layouts).
        html_tag = re.search(r"<html\b" + TAG_ATTRS + ">", text)
        if html_tag and not has_attr(html_tag.group(1), "lang"):
            self.add("error", file, find_line(html_tag.start()), "html-lang", "<html> without lang attribute")
        viewport = re.search(r"<meta\b[^>]*name\s*=\s*[\"']viewport[\"'][^>]*>", text, re.I)
        if viewport and re.search(r"user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0)?\b", viewport.group(0), re.I):
            self.add("error", file, find_line(viewport.start()), "zoom-disabled",
                     "Viewport meta blocks pinch zoom (user-scalable=no / maximum-scale=1)")
        if html_tag and not is_jsx:
            if not re.search(r"<title\b", lowered):
                self.add("warning", file, find_line(html_tag.start()), "document-title", "Document has no <title>")
            if "<body" in lowered and not re.search(r"href\s*=\s*[\"']#[\w-]+[\"'][^>]*>\s*skip|class\s*=\s*[\"'][^\"']*skip", lowered):
                self.add("info", file, find_line(lowered.find("<body")), "skip-link",
                         "No skip-to-content link; helpful when a long nav precedes the main content")
            ids = re.findall(r"\sid\s*=\s*[\"']([^\"'{}$]+)[\"']", text)
            dupes = sorted({i for i in ids if ids.count(i) > 1})
            if dupes:
                self.add("warning", file, None, "duplicate-id", f"Duplicate id(s): {', '.join(dupes[:5])}")

        # Click handlers on non-interactive elements.
        for m in re.finditer(r"<(div|span|li|section|article|p|td|tr|img)\b" + TAG_ATTRS + ">", text):
            attrs = m.group(2)
            if not re.search(r"(?<![\w-])(onClick|onclick|@click|v-on:click|on:click)\s*=", attrs):
                continue
            keyboard = re.search(r"on[kK]ey(Down|Up|Press)|@keydown|@keyup|on:keydown", attrs)
            role = re.search(r"\brole\s*=", attrs)
            focusable = re.search(r"tab[iI]ndex\s*=", attrs)
            if not (keyboard and role and focusable):
                missing = [name for name, ok in (("role", role), ("tabindex", focusable), ("key handler", keyboard)) if not ok]
                self.add("warning", file, find_line(m.start()), "click-non-interactive",
                         f"<{m.group(1)}> with a click handler lacks {', '.join(missing)}; prefer <button>")

        for m in re.finditer(r"tab[iI]ndex\s*=\s*(?:[\"']|\{)\s*([1-9]\d*)", text):
            self.add("warning", file, find_line(m.start()), "positive-tabindex",
                     f"tabindex={m.group(1)} overrides the natural focus order; use 0 or -1")
        for m in re.finditer(r"<(audio|video)\b" + TAG_ATTRS + ">", text, re.I):
            attrs = m.group(2).lower()
            if "autoplay" in attrs and "muted" not in attrs:
                self.add("warning", file, find_line(m.start()), "autoplay",
                         f"<{m.group(1).lower()}> autoplays with sound; add muted (and controls)")
        for m in re.finditer(r"<iframe\b" + TAG_ATTRS + ">", text, re.I):
            if not has_attr(m.group(1), "title") and not SPREAD.search(m.group(1)):
                self.add("warning", file, find_line(m.start()), "iframe-title", "<iframe> without title")
        for m in re.finditer(r"<(button|a|input|select|textarea)\b" + TAG_ATTRS + ">", text):
            if re.search(r"aria-hidden\s*=\s*[\"'{]?\s*true", m.group(2), re.I) and not re.search(r"tab[iI]ndex\s*=\s*[\"'{]?\s*-1", m.group(2)):
                self.add("warning", file, find_line(m.start()), "aria-hidden-focusable",
                         f"aria-hidden on a focusable <{m.group(1)}>; screen readers lose it but keyboard still reaches it")
        for m in re.finditer(r"<(?!button\b)(\w+)\b" + TAG_ATTRS + ">", text):
            attrs = m.group(2)
            if re.search(r"\brole\s*=\s*[\"']button[\"']", attrs) and m.group(1)[0].islower():
                if not (re.search(r"tab[iI]ndex\s*=", attrs) and re.search(r"on[kK]ey|@key|on:key", attrs)):
                    self.add("warning", file, find_line(m.start()), "role-button",
                             "role=\"button\" needs tabindex=\"0\" and an Enter/Space key handler; prefer <button>")

    def run(self) -> None:
        for path in iter_files(self.target, MARKUP_SUFFIXES):
            self.check_file(path)


def main() -> int:
    utf8_console()
    parser = base_parser("Static accessibility audit (alt text, labels, names, lang, keyboard access).")
    args = parser.parse_args()
    target = resolve_target(parser, args.project)
    checker = A11yChecker(target)
    checker.run()
    notes = ["static checks only; verify contrast and focus order in a browser (Lighthouse or playwright_runner.py --a11y)"]
    return emit(args, "accessibility_checker", "Accessibility check", target, checker.findings, checker.files_checked, notes)


if __name__ == "__main__":
    raise SystemExit(main())
