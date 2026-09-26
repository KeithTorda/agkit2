#!/usr/bin/env python3
"""UX audit for web UI source (HTML, CSS/SCSS, JSX/TSX, Vue, Svelte, Astro, PHP/Blade).

Static heuristics, grouped by how much they should matter:

  warning  real usability / accessibility / correctness problems that can be read
           from source: text contrast below 4.5:1 in a CSS rule, removed focus
           outline with no :focus-visible replacement, controls under 24px, text
           under 12px, heading levels skipped, missing viewport meta, motion with
           no prefers-reduced-motion handling anywhere in the project, layout
           properties in will-change, GSAP without cleanup, "click here" links.
  info     design guidance, never a failure: gradients, glass, glow, purple
           defaults, pure black/white, many font families, hard-coded colours
           instead of tokens, transitions on layout properties, hype words in copy.
           Style info is suppressed when DESIGN.md asks for that style.

Accessibility markup checks (alt text, labels, button names, lang) live in
accessibility_checker.py; this script does not repeat them.

Usage:
    python ux_audit.py <project-or-file> [--json] [--fail-on error|warning|never] [--verbose]

Exit codes: 0 ok, 1 findings at/above --fail-on (default: error; this audit
emits no errors, so it fails only with --fail-on warning), 2 usage error.
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
# UX audit
# ---------------------------------------------------------------------------
MARKUP_SUFFIXES = (".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".php")
STYLE_SUFFIXES = (".css", ".scss", ".sass", ".less")
UX_SKIP_DIRS = SKIP_DIRS | {"ui"}  # generated component libraries (shadcn components/ui)

# DESIGN.md keywords that make a style a deliberate choice (info is then suppressed).
DESIGN_STYLES = {
    "gradient": ("gradient", "mesh", "aurora"),
    "glass": ("glass", "frosted", "backdrop", "blur"),
    "glow": ("glow", "neon"),
    "purple": ("purple", "violet", "lavender"),
    "pure-black-white": ("pure black", "pure white", "#000", "#fff", "true black", "oled", "high contrast", "monochrome"),
    "motion": ("animation", "animated", "motion", "parallax"),
    "fonts": ("font", "typeface"),
}
NAMED_COLORS = {"white": (255, 255, 255), "black": (0, 0, 0)}
LAYOUT_PROPS = ("width", "height", "top", "left", "right", "bottom", "margin", "padding")
HYPE_WORDS = re.compile(
    r"\b(seamless(?:ly)?|revolutioni[sz]e|unlock(?:s|ing)?|elevate|supercharge|cutting[- ]edge|"
    r"game[- ]chang(?:er|ing)|next[- ]level|world[- ]class|effortless(?:ly)?|leverage|delve|"
    r"best[- ]in[- ]class|blazing(?:ly)?[- ]fast)\b", re.IGNORECASE)
NEUTRALS = "gray|slate|zinc|neutral|stone"


def parse_color(value: str) -> tuple[int, int, int] | None:
    value = re.sub(r"\s*!important\s*$", "", value.strip().lower())
    if value in NAMED_COLORS:
        return NAMED_COLORS[value]
    match = re.fullmatch(r"#([0-9a-f]{3,8})", value)
    if not match:
        return None
    digits = match.group(1)
    if len(digits) in (3, 4):
        if len(digits) == 4 and digits[3] != "f":
            return None
        digits = "".join(ch * 2 for ch in digits[:3])
    elif len(digits) == 8:
        if digits[6:] != "ff":
            return None
        digits = digits[:6]
    elif len(digits) != 6:
        return None
    return int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16)


def contrast_ratio(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    def lum(rgb: tuple[int, int, int]) -> float:
        channels = []
        for c in rgb:
            c = c / 255
            channels.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
        return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def to_px(value: str) -> float | None:
    match = re.match(r"\s*(-?\d*\.?\d+)\s*(px|rem|em)?\b", value)
    if not match:
        return None
    number = float(match.group(1))
    unit = match.group(2) or ("px" if number == 0 else None)
    if unit == "px":
        return number
    if unit in ("rem", "em"):
        return number * 16
    return None


def to_ms(value: str) -> float | None:
    match = re.match(r"\s*(\d*\.?\d+)(ms|s)\b", value)
    if not match:
        return None
    return float(match.group(1)) * (1 if match.group(2) == "ms" else 1000)


class UXAuditor:
    def __init__(self, target: Path) -> None:
        self.target = target
        self.root = target if target.is_dir() else target.parent
        self.findings: list[dict[str, Any]] = []
        self.files_checked = 0
        self.design_text = self._read_design_md()
        self.motion_uses: list[tuple[str, int]] = []
        self.reduced_motion_found = False
        self.font_families: dict[str, str] = {}
        self.has_tokens = False
        self._pending_hex: list[tuple[str, int]] = []

    # -- setup ---------------------------------------------------------------
    def _read_design_md(self) -> str:
        for candidate in (self.root / "DESIGN.md", self.root / "docs" / "DESIGN.md", self.root / "design.md"):
            if candidate.is_file():
                return read_text(candidate).lower()
        return ""

    def style_is_chosen(self, style: str) -> bool:
        return bool(self.design_text) and any(word in self.design_text for word in DESIGN_STYLES[style])

    def add(self, severity: str, file: str, line: int | None, rule: str, message: str) -> None:
        self.findings.append(make_finding(severity, file, line, rule, message))

    def style_info(self, style: str, file: str, line: int | None, rule: str, message: str) -> None:
        if self.style_is_chosen(style):
            return
        suffix = " Fine when DESIGN.md or the brief asks for it." if not self.design_text else " Not mentioned in DESIGN.md."
        self.add("info", file, line, rule, message + suffix)

    # -- CSS -----------------------------------------------------------------
    def audit_css(self, css: str, file: str, base_line: int, find_line, offset: int) -> None:
        """Audit a CSS text. offset is the index of css inside the original file text."""
        css_clean = re.sub(r"/\*.*?\*/", lambda m: " " * len(m.group(0)), css, flags=re.S)
        if re.search(r"prefers-reduced-motion", css_clean):
            self.reduced_motion_found = True
        has_focus_visible = ":focus-visible" in css_clean or "focus-visible" in css_clean
        for kf in re.finditer(r"@keyframes\s+([\w-]+)", css_clean):
            self.motion_uses.append((file, find_line(offset + kf.start())))
        if re.search(r"--[\w-]+\s*:", css_clean) or "@theme" in css_clean:
            self.has_tokens = True
        for rule in re.finditer(r"([^{}]+)\{([^{}]*)\}", css_clean):
            selector = rule.group(1).strip().split("\n")[-1].strip()
            if selector.startswith("@") or not selector:
                continue
            line = find_line(offset + rule.start(1) + len(rule.group(1)) - len(rule.group(1).lstrip()))
            self.audit_declarations(selector, rule.group(2), file, line, has_focus_visible)

    def audit_declarations(self, selector: str, body: str, file: str, line: int,
                           has_focus_visible: bool) -> None:
        decls: dict[str, str] = {}
        for part in body.split(";"):
            if ":" in part:
                prop, _, value = part.partition(":")
                decls[prop.strip().lower()] = value.strip()
        sel = selector.lower()

        # Contrast: only when both colours are declared in the same rule.
        fg = parse_color(decls.get("color", ""))
        bg_value = decls.get("background-color") or decls.get("background", "")
        bg = parse_color(bg_value) if bg_value and " " not in bg_value.strip() else None
        if fg and bg:
            ratio = contrast_ratio(fg, bg)
            if ratio < 4.5:
                extra = " (fails even for large text)" if ratio < 3 else " (passes only for large text)"
                self.add("warning", file, line, "contrast",
                         f"'{selector[:40]}' text contrast {ratio:.2f}:1, needs 4.5:1{extra}")

        # Focus visibility.
        outline = decls.get("outline", decls.get("outline-style", ""))
        if ":focus" in sel and ":focus-visible" not in sel and "\\:" not in sel and re.fullmatch(r"(none|0|0px)(\s*!important)?", outline.strip()):
            if not has_focus_visible:
                self.add("warning", file, line, "focus-visible",
                         f"'{selector[:40]}' removes the focus outline and the file has no :focus-visible style")

        # Text size.
        size = to_px(decls.get("font-size", ""))
        if size is not None and 0 < size < 12:
            self.add("warning", file, line, "small-text", f"font-size {decls['font-size']} is below 12px")

        # Target size on interactive selectors.
        if re.search(r"(^|[\s,>+~])(button|a|input|select)\b|\.btn|button|\[role=.?button|icon-?button", sel):
            heights = [to_px(decls[k]) for k in ("height", "min-height") if k in decls]
            heights = [h for h in heights if h is not None]
            if heights:
                height = max(heights)
                if 0 < height < 24:
                    self.add("warning", file, line, "target-size",
                             f"'{selector[:40]}' height {height:g}px is below the 24px minimum target (WCAG 2.5.8)")
                elif 24 <= height < 44:
                    self.add("info", file, line, "target-size-touch",
                             f"'{selector[:40]}' height {height:g}px; 44px is more comfortable on touch screens")

        # Performance.
        will_change = decls.get("will-change", "").lower()
        bad = [p for p in LAYOUT_PROPS if re.search(rf"\b{p}\b", will_change)]
        if bad:
            self.add("warning", file, line, "will-change-layout",
                     f"will-change on layout property ({', '.join(bad)}); use transform/opacity")
        for key in ("transition", "transition-property"):
            value = decls.get(key, "").lower()
            if not value:
                continue
            props = [p for p in LAYOUT_PROPS if re.search(rf"(^|[\s,]){p}\b", value)]
            if props:
                self.add("info", file, line, "transition-layout",
                         f"transition on {', '.join(props)} triggers layout each frame; transform/opacity is cheaper")
            elif re.search(r"(^|[\s,])all\b", value):
                self.add("info", file, line, "transition-all", "transition: all animates every property; list the ones you mean")
        duration = to_ms(decls.get("transition-duration", ""))
        if duration is None:
            timed = re.search(r"\d*\.?\d+m?s\b", decls.get("transition", ""))
            duration = to_ms(timed.group(0)) if timed else None
        if duration and duration > 1000:
            self.add("info", file, line, "slow-transition", f"transition of {duration:g}ms; UI feedback reads best at 150-400ms")
        if "animation" in decls or "animation-name" in decls:
            name = decls.get("animation-name", decls.get("animation", ""))
            if name and not re.match(r"\s*none\b", name):
                self.motion_uses.append((file, line))

        # Fonts.
        family = decls.get("font-family")
        if family:
            first = family.split(",")[0].strip().strip("\"'").lower()
            if first and not first.startswith("var(") and first not in {
                    "inherit", "initial", "system-ui", "sans-serif", "serif", "monospace", "-apple-system",
                    "ui-sans-serif", "ui-serif", "ui-monospace"}:
                self.font_families.setdefault(first, file)

        # Style guidance (info only).
        joined = " ".join(f"{k}:{v}" for k, v in decls.items()).lower()
        if "gradient(" in joined:
            self.style_info("gradient", file, line, "style-gradient",
                            "Gradient in use; check it frames one focal point rather than decorating everything.")
        if "backdrop-filter" in decls or "-webkit-backdrop-filter" in decls:
            self.style_info("glass", file, line, "style-glass",
                            "Glass effect (backdrop-filter); check text contrast over busy backgrounds.")
        shadow = decls.get("box-shadow", "") + " " + decls.get("text-shadow", "")
        if re.search(r"(^|,)\s*0(px)?\s+0(px)?\s+\d+px\s+(\d+px\s+)?(#|rgb|hsl)", shadow) and shadow.count(",") >= 1:
            self.style_info("glow", file, line, "style-glow", "Layered glow shadow; reads as decoration unless the brand calls for it.")
        if re.search(r"#(8b5cf6|a855f7|9333ea|7c3aed|6d28d9|a78bfa|c084fc)\b", joined):
            self.style_info("purple", file, line, "style-purple-default",
                            "Tailwind-default purple; pick the primary on purpose.")
        if bg and bg == (0, 0, 0):
            self.style_info("pure-black-white", file, line, "style-pure-black",
                            "Pure black background; a near-black is often softer.")

    # -- markup --------------------------------------------------------------
    def audit_markup(self, text: str, file: str, find_line, is_jsx: bool) -> None:
        lowered = text.lower()
        # Embedded CSS: <style> blocks and inline style attributes.
        for block in re.finditer(r"<style\b[^>]*>(.*?)</style\s*>", text, re.S | re.I):
            self.audit_css(block.group(1), file, 0, find_line, block.start(1))
        for attr in re.finditer(r"\bstyle\s*=\s*\"([^\"]*)\"", text):
            self.audit_declarations("[style]", attr.group(1), file, find_line(attr.start()), True)

        is_document = bool(re.search(r"<html\b", lowered))
        # Next.js / React frameworks inject the viewport meta; only raw documents need it.
        if is_document and not is_jsx and not re.search(r"<meta[^>]+name\s*=\s*[\"']viewport", lowered):
            self.add("warning", file, find_line(lowered.find("<html")), "viewport-meta",
                     "Document has no <meta name=\"viewport\">; the page will render zoomed out on phones")

        # Headings.
        headings = [(int(m.group(1)), m.start()) for m in re.finditer(r"<h([1-6])\b", text, re.I)]
        for (prev, _), (curr, pos) in zip(headings, headings[1:]):
            if curr > prev + 1:
                self.add("warning", file, find_line(pos), "heading-skip",
                         f"Heading level jumps from h{prev} to h{curr}; screen-reader outline has a gap")
        h1s = [pos for level, pos in headings if level == 1]
        if len(h1s) > 1 and is_document:
            self.add("info", file, find_line(h1s[1]), "multiple-h1", f"{len(h1s)} <h1> elements; one per page is clearer")

        # Navigation size.
        for nav in re.finditer(r"<nav\b.*?</nav\s*>", text, re.S | re.I):
            links = len(re.findall(r"<(a|Link|NavLink|router-link)\b", nav.group(0)))
            if links > 9:
                self.add("info", file, find_line(nav.start()), "nav-size",
                         f"{links} links in one <nav>; consider grouping")

        # Link purpose.
        for link in re.finditer(r"<(a|Link)\b[^>]*>\s*([^<{]{1,30}?)\s*</\1\s*>", text, re.I):
            label = link.group(2).strip().lower().rstrip(".")
            if label in {"click here", "here", "click"}:
                self.add("warning", file, find_line(link.start()), "link-purpose",
                         f"Link text '{link.group(2).strip()}' does not say where it goes")
            elif label in {"read more", "learn more", "more", "details"}:
                self.add("info", file, find_line(link.start()), "link-purpose-generic",
                         f"Generic link text '{link.group(2).strip()}'; add context (visually hidden text or aria-label)")

        # Class-based (Tailwind) checks.
        for tag in re.finditer(r"<([A-Za-z][\w.:-]*)\b((?:[^>\"'{}]|\"[^\"]*\"|'[^']*'|\{[^{}]*\})*)>", text):
            name, attrs = tag.group(1), tag.group(2)
            cls_match = re.search(r"\bclass(?:Name)?\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|\{`([^`]*)`\})", attrs)
            if not cls_match:
                continue
            classes = next(g for g in cls_match.groups() if g is not None)
            self.audit_classes(name, classes, file, find_line(tag.start()))

        # Motion libraries.
        if re.search(r"from\s+[\"'](framer-motion|motion/react|motion)[\"']", text) or "@keyframes" in lowered:
            self.motion_uses.append((file, find_line(max(lowered.find("motion"), 0))))
        if re.search(r"useReducedMotion|reducedMotion|prefers-reduced-motion|motion-reduce:|motion-safe:", text):
            self.reduced_motion_found = True
        if re.search(r"\bgsap\b", text) and re.search(r"\buse(Layout)?Effect\b", text):
            if not re.search(r"\.revert\(|\.kill\(|useGSAP|gsap\.context", text):
                self.add("warning", file, find_line(text.find("gsap")), "gsap-cleanup",
                         "GSAP used in a React effect without revert()/kill()/useGSAP; animations leak on unmount")
            self.motion_uses.append((file, find_line(text.find("gsap"))))

        # Visible copy.
        for node in re.finditer(r">([^<>{}]{3,300})<", text):
            words = HYPE_WORDS.findall(node.group(1))
            if words:
                self.add("info", file, find_line(node.start()), "copy-hype",
                         f"Hype word in UI copy ('{words[0]}'); say what the product does (design-rules: honest copy)")

        # Forms.
        for form in re.finditer(r"<form\b.*?</form\s*>", text, re.S | re.I):
            fields = len(re.findall(r"<(input|select|textarea)\b(?![^>]*type\s*=\s*[\"']?(hidden|submit|button))", form.group(0), re.I))
            if fields > 8 and not re.search(r"<fieldset|step|wizard", form.group(0), re.I):
                self.add("info", file, find_line(form.start()), "form-length",
                         f"Form with {fields} fields and no grouping; fieldsets or steps reduce load")

        # Hard-coded colours in components when tokens exist (checked after the walk).
        if is_jsx or file.endswith((".vue", ".svelte")):
            hexes = re.findall(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b(?![0-9a-fA-F])", re.sub(r"&#\w+;", "", text))
            if len(hexes) >= 4:
                self._pending_hex.append((file, len(hexes)))

    def audit_classes(self, tag: str, classes: str, file: str, line: int) -> None:
        tokens = set(classes.split())
        joined = " " + " ".join(tokens) + " "
        light_text = re.search(rf"\btext-({NEUTRALS})-(100|200|300|400)\b", joined)
        light_bg = re.search(rf"\bbg-(white|({NEUTRALS})-(50|100))\b", joined)
        if light_text and light_bg:
            self.add("warning", file, line, "contrast",
                     f"{light_text.group(0)} on {light_bg.group(0)} is below 4.5:1 contrast")
        if re.search(r"(^|\s)text-white(\s|$)", joined) and re.search(r"\bbg-(?!black|white|transparent)[a-z]+-(50|100|200|300)\b", joined):
            self.add("warning", file, line, "contrast", "text-white on a light (50-300) background is below 4.5:1 contrast")
        small = re.search(r"\btext-\[(\d+(?:\.\d+)?)px\]", joined)
        if small and float(small.group(1)) < 12:
            self.add("warning", file, line, "small-text", f"{small.group(0)} is below 12px")
        if re.search(r"(^|\s)(focus:)?outline-none(\s|$)", joined) and not re.search(r"focus(-visible)?:(ring|outline|border|shadow)", joined):
            self.add("warning", file, line, "focus-visible",
                     "outline-none without a focus-visible:ring/outline replacement; keyboard focus becomes invisible")
        if tag.lower() in {"button", "a"}:
            size = re.search(r"(?:^|\s)(?:h|size)-(\d+(?:\.5)?)(?=\s)", joined)
            if size and float(size.group(1)) * 4 < 24 and not re.search(r"\b(min-h|p|py)-(\d+)", joined):
                self.add("warning", file, line, "target-size",
                         f"<{tag}> with {size.group(0).strip()} ({float(size.group(1)) * 4:g}px) is below the 24px minimum target")
        if re.search(r"\banimate-(bounce|ping|pulse|\[)", joined):
            self.motion_uses.append((file, line))
        if re.search(r"\b(motion-reduce|motion-safe):", joined):
            self.reduced_motion_found = True
        if re.search(r"\bbg-(gradient|linear|radial|conic)-", joined):
            self.style_info("gradient", file, line, "style-gradient",
                            "Gradient in use; check it frames one focal point rather than decorating everything.")
        if re.search(r"\bbackdrop-blur", joined):
            self.style_info("glass", file, line, "style-glass",
                            "Glass effect (backdrop-blur); check text contrast over busy backgrounds.")
        if re.search(r"\b(bg|text|from|to|via|border|ring)-(purple|violet)-\d{2,3}\b", joined):
            self.style_info("purple", file, line, "style-purple-default",
                            "Tailwind-default purple/violet; pick the primary on purpose.")

    # -- driver --------------------------------------------------------------
    def run(self) -> None:
        for path in iter_files(self.target, MARKUP_SUFFIXES + STYLE_SUFFIXES, UX_SKIP_DIRS):
            if path.name.endswith((".min.css", ".min.js")):
                continue
            text = read_text(path)
            if not text:
                continue
            self.files_checked += 1
            file = rel(path, self.target)
            find_line = line_finder(text)
            if path.suffix.lower() in STYLE_SUFFIXES:
                self.audit_css(text, file, 0, find_line, 0)
            else:
                self.audit_markup(text, file, find_line, path.suffix.lower() in {".jsx", ".tsx"})
        self._project_checks()

    def _project_checks(self) -> None:
        if self.motion_uses and not self.reduced_motion_found:
            file, line = self.motion_uses[0]
            self.add("warning", file, line, "reduced-motion",
                     f"Animation used ({len(self.motion_uses)} place(s)) but no prefers-reduced-motion / "
                     "motion-reduce / useReducedMotion handling anywhere in the project")
        if len(self.font_families) > 2 and not self.style_is_chosen("fonts"):
            names = ", ".join(sorted(self.font_families)[:5])
            self.add("info", "(project)", None, "font-families",
                     f"{len(self.font_families)} font families ({names}); design-rules suggests at most two unless DESIGN.md says otherwise")
        if self.has_tokens:
            for file, count in self._pending_hex:
                self.add("info", file, None, "hard-coded-colors",
                         f"{count} hard-coded hex colours in a component while the project defines tokens; use the tokens")


def main() -> int:
    utf8_console()
    parser = base_parser("UX audit for web UI source. Real usability issues are warnings; style guidance is info.")
    args = parser.parse_args()
    target = resolve_target(parser, args.project)
    auditor = UXAuditor(target)
    auditor.run()
    notes = []
    if auditor.design_text:
        notes.append("DESIGN.md found: style guidance it covers is not reported")
    notes.append("markup accessibility (alt, labels, names, lang) is covered by accessibility_checker.py")
    return emit(args, "ux_audit", "UX audit", target, auditor.findings, auditor.files_checked, notes)


if __name__ == "__main__":
    raise SystemExit(main())
