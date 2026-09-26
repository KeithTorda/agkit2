#!/usr/bin/env python3
"""Mobile audit for React Native / Expo and Flutter source.

Only files that import react-native, expo-*, @react-navigation or
package:flutter are checked.

  error    auth tokens or passwords written to AsyncStorage / SharedPreferences
           (plain-text storage; use expo-secure-store / Keychain / flutter_secure_storage)
  warning  FlatList keyExtractor returning the index, touchables with no
           accessible name, touch targets under 44pt with no hitSlop, font
           scaling disabled, text under 11pt, useEffect listeners without
           cleanup, Animated config without useNativeDriver, Flutter setState
           after await without a mounted check, IconButton without tooltip
  info     .map() inside ScrollView, index keys, project-level gaps (no safe-area
           handling, no error boundary, no dark mode), console.log calls, pure black
           backgrounds. Info never fails.

Usage:
    python mobile_audit.py <project-or-file> [--json] [--fail-on error|warning|never] [--verbose]

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
# Mobile audit
# ---------------------------------------------------------------------------
MOBILE_SKIP_DIRS = SKIP_DIRS | {"ios", "android", "Pods", ".dart_tool", ".gradle", "web-build"}
RN_MARKER = re.compile(r"from\s+[\"'](react-native|expo[\w/-]*|@react-navigation/[\w-]+|react-native-[\w-]+)[\"']|require\([\"']react-native[\"']\)")
FLUTTER_MARKER = re.compile(r"import\s+[\"']package:flutter/")
SENSITIVE_KEY = r"[^\"'`]*(token|jwt|password|passwd|secret|session|refresh|credential)[^\"'`]*"
TOUCHABLE = r"(Pressable|TouchableOpacity|TouchableHighlight|TouchableWithoutFeedback|TouchableNativeFeedback)"
JSX_ATTRS = r"((?:[^>\"'{}]|\"[^\"]*\"|'[^']*'|\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})*)"


def matching_block(text: str, open_index: int, open_ch: str = "{", close_ch: str = "}") -> int:
    """Return the index just after the bracket that closes text[open_index]. Strings are skipped."""
    depth, i, quote = 0, open_index, None
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'`":
            quote = ch
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


class MobileAuditor:
    def __init__(self, target: Path) -> None:
        self.target = target
        self.findings: list[dict[str, Any]] = []
        self.files_checked = 0
        self.rn_files = 0
        self.flutter_files = 0
        self.seen: dict[str, bool] = {"safe_area": False, "error_boundary": False, "dark_mode": False}
        self.console_logs: list[tuple[str, int, int]] = []

    def add(self, severity: str, file: str, line: int | None, rule: str, message: str) -> None:
        self.findings.append(make_finding(severity, file, line, rule, message))

    def check_react_native(self, text: str, file: str, find_line) -> None:
        if re.search(r"SafeAreaView|useSafeAreaInsets|SafeAreaProvider|expo-router", text):
            self.seen["safe_area"] = True
        if re.search(r"ErrorBoundary|componentDidCatch|getDerivedStateFromError", text):
            self.seen["error_boundary"] = True
        if re.search(r"useColorScheme|Appearance\.|colorScheme", text):
            self.seen["dark_mode"] = True

        for m in re.finditer(rf"AsyncStorage\.(setItem|multiSet)\(\s*[\"'`]{SENSITIVE_KEY}[\"'`]", text, re.I):
            self.add("error", file, find_line(m.start()), "insecure-token-storage",
                     "Sensitive value written to AsyncStorage (plain text); use expo-secure-store or react-native-keychain")

        for m in re.finditer(r"<ScrollView\b", text):
            end = text.find("</ScrollView", m.end())
            if end != -1 and re.search(r"\.map\(", text[m.end():end]):
                self.add("info", file, find_line(m.start()), "scrollview-map",
                         ".map() inside ScrollView renders every row at once; use FlatList/FlashList if the list can grow")
        for m in re.finditer(r"keyExtractor\s*=\s*\{\s*\(\s*\w+\s*,\s*(\w+)\s*\)\s*=>\s*(?:String\()?\s*(\w+)", text):
            if m.group(1) == m.group(2):
                self.add("warning", file, find_line(m.start()), "index-key",
                         "keyExtractor returns the index; rows re-render and lose state on insert/delete")
        for m in re.finditer(r"\bkey\s*=\s*\{\s*(index|idx|i)\s*\}", text):
            self.add("info", file, find_line(m.start()), "index-key",
                     "Array index as key; use a stable id if items can be inserted, removed or reordered")

        for m in re.finditer(rf"<{TOUCHABLE}\b{JSX_ATTRS}(/?)>", text):
            tag, attrs, self_closing = m.group(1), m.group(2), m.group(3)
            line = find_line(m.start())
            body = ""
            if not self_closing:
                close = text.find(f"</{tag}", m.end())
                body = text[m.end():close] if close != -1 else ""
            labelled = re.search(r"accessibilityLabel|aria-label|\{\s*\.\.\.", attrs) or re.search(r"<Text\b", body)
            if not labelled:
                self.add("warning", file, line, "touchable-label",
                         f"<{tag}> has no accessibilityLabel and no <Text> child; screen readers announce nothing")
            if "hitSlop" not in attrs:
                style = re.search(r"style\s*=\s*\{\{([^{}]*)\}\}", attrs)
                if style:
                    sizes = [int(v) for v in re.findall(r"\b(?:width|height)\s*:\s*(\d+)", style.group(1))]
                    if sizes and min(sizes) < 44:
                        self.add("warning", file, line, "touch-target",
                                 f"<{tag}> is {min(sizes)}pt with no hitSlop; aim for 44pt (iOS) / 48dp (Android)")

        for m in re.finditer(r"\buseEffect\(\s*(?:async\s*)?\(\s*\)\s*=>\s*\{", text):
            open_index = m.end() - 1
            body = text[open_index:matching_block(text, open_index)]
            if re.search(r"addEventListener\(|addListener\(|\.subscribe\(|setInterval\(|\.on\(\s*[\"']", body) \
                    and not re.search(r"\breturn\b", body):
                self.add("warning", file, find_line(m.start()), "effect-cleanup",
                         "useEffect adds a listener/interval but returns no cleanup; it leaks on unmount")

        for m in re.finditer(r"Animated\.(timing|spring|decay)\(", text):
            call_end = matching_block(text, m.end() - 1, "(", ")")
            if "useNativeDriver" not in text[m.end():call_end]:
                self.add("warning", file, find_line(m.start()), "native-driver",
                         f"Animated.{m.group(1)} without useNativeDriver (React Native warns; true for transform/opacity)")

        for m in re.finditer(r"allowFontScaling\s*=\s*\{\s*false\s*\}|maxFontSizeMultiplier\s*=\s*\{\s*1(\.0)?\s*\}", text):
            self.add("warning", file, find_line(m.start()), "font-scaling",
                     "Font scaling disabled; users with large text settings cannot read this")
        for m in re.finditer(r"\bfontSize\s*:\s*(\d+(?:\.\d+)?)", text):
            if float(m.group(1)) < 11:
                self.add("warning", file, find_line(m.start()), "small-text", f"fontSize {m.group(1)} is below 11pt")
        for m in re.finditer(r"backgroundColor\s*:\s*[\"'](#000000|#000|black)[\"']", text, re.I):
            self.add("info", file, find_line(m.start()), "style-pure-black",
                     "Pure black background; fine for OLED themes, a near-black is softer. Follow DESIGN.md.")
        logs = len(re.findall(r"\bconsole\.log\(", text))
        if logs:
            self.console_logs.append((file, find_line(text.find("console.log(")), logs))

    def check_flutter(self, text: str, file: str, find_line) -> None:
        if re.search(r"SafeArea\(|MediaQuery\.of\(context\)\.padding|Scaffold\(", text):
            self.seen["safe_area"] = True
        if re.search(r"darkTheme\s*:|ThemeMode\.", text):
            self.seen["dark_mode"] = True
        self.seen["error_boundary"] = True  # Flutter has ErrorWidget/FlutterError by default

        for m in re.finditer(rf"\.set(String|StringList)\(\s*[\"']{SENSITIVE_KEY}[\"']", text, re.I):
            self.add("error", file, find_line(m.start()), "insecure-token-storage",
                     "Sensitive value written to SharedPreferences (plain text); use flutter_secure_storage")
        for m in re.finditer(r"\)\s*async\s*\{", text):
            open_index = m.end() - 1
            body = text[open_index:matching_block(text, open_index)]
            first_await = body.find("await ")
            set_state = body.find("setState(", first_await if first_await != -1 else len(body))
            if first_await != -1 and set_state != -1 and "mounted" not in body[first_await:set_state]:
                self.add("warning", file, find_line(open_index + set_state), "set-state-after-await",
                         "setState after await without `if (!mounted) return;` throws when the widget is gone")
        for m in re.finditer(r"\bIconButton\(", text):
            call_end = matching_block(text, m.end() - 1, "(", ")")
            if not re.search(r"\b(tooltip|semanticLabel)\s*:", text[m.end():call_end]):
                self.add("warning", file, find_line(m.start()), "icon-button-tooltip",
                         "IconButton without tooltip; screen readers get no name")
        for m in re.finditer(r"textScaleFactor\s*:\s*1(\.0)?\b|TextScaler\.noScaling", text):
            self.add("warning", file, find_line(m.start()), "font-scaling",
                     "Text scaling disabled; users with large text settings cannot read this")
        for m in re.finditer(r"fontSize\s*:\s*(\d+(?:\.\d+)?)", text):
            if float(m.group(1)) < 11:
                self.add("warning", file, find_line(m.start()), "small-text", f"fontSize {m.group(1)} is below 11pt")

    def run(self) -> None:
        for path in iter_files(self.target, (".tsx", ".ts", ".jsx", ".js", ".dart"), MOBILE_SKIP_DIRS):
            if path.name.endswith((".min.js", ".d.ts", ".config.js", ".config.ts")):
                continue
            text = read_text(path)
            is_dart = path.suffix == ".dart"
            if is_dart and FLUTTER_MARKER.search(text):
                self.flutter_files += 1
                handler = self.check_flutter
            elif not is_dart and RN_MARKER.search(text):
                self.rn_files += 1
                handler = self.check_react_native
            else:
                continue
            self.files_checked += 1
            handler(text, rel(path, self.target), line_finder(text))
        self.project_checks()

    def project_checks(self) -> None:
        if not self.files_checked or not self.target.is_dir():
            return
        if not self.seen["safe_area"]:
            self.add("info", "(project)", None, "safe-area",
                     "No SafeAreaView / useSafeAreaInsets / SafeArea found; content may sit under the notch or home bar")
        if self.rn_files and not self.seen["error_boundary"]:
            self.add("info", "(project)", None, "error-boundary",
                     "No error boundary found; one render error blanks the whole app")
        if not self.seen["dark_mode"]:
            self.add("info", "(project)", None, "dark-mode",
                     "No colour-scheme handling found; fine if the design is light-only")
        if self.console_logs:
            total = sum(count for _, _, count in self.console_logs)
            file, line, _ = self.console_logs[0]
            self.add("info", file, line, "console-log",
                     f"{total} console.log call(s) in {len(self.console_logs)} file(s); strip them in release builds")


def main() -> int:
    utf8_console()
    parser = base_parser("Mobile audit for React Native / Expo and Flutter source.")
    args = parser.parse_args()
    target = resolve_target(parser, args.project)
    auditor = MobileAuditor(target)
    auditor.run()
    notes = [f"{auditor.rn_files} React Native file(s), {auditor.flutter_files} Flutter file(s)"]
    if not auditor.files_checked:
        notes.append("no React Native or Flutter source found; nothing to audit")
    return emit(args, "mobile_audit", "Mobile audit", target, auditor.findings, auditor.files_checked, notes)


if __name__ == "__main__":
    raise SystemExit(main())
