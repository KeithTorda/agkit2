#!/usr/bin/env python3
"""Static CSS audit: find why text is the wrong colour, before you ever open the browser.

The render shows the symptom. This finds the cause, with file:line — a custom property
defined twice with different values, a var() nothing defines, an inline style or
!important overriding a token, or a colour pair that cannot be read.

Scans .css/.scss plus <style> blocks and style="" attributes in .html/.blade.php/.vue/.jsx/.tsx.

Usage:
  python css_audit.py .
  python css_audit.py . --json report.json --fail-on error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SKIP_DIRS = {"node_modules", "vendor", "dist", "build", ".next", ".git", "out",
             "coverage", "__pycache__", ".venv", "storage", "public/build"}
STYLE_EXT = {".css", ".scss", ".sass", ".less"}
MARKUP_EXT = {".html", ".htm", ".vue", ".svelte", ".jsx", ".tsx", ".php"}

# Selectors under which a token is *expected* to be redefined — theming, not collision.
THEME_SELECTOR = re.compile(
    r"(\.dark|\[data-theme|:root\s*\.|\.light|@media|prefers-color-scheme|\.theme-|\[data-mode)",
    re.I)

COMMENT = re.compile(r"/\*.*?\*/", re.S)
VAR_DEF = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]+)")
VAR_USE = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)\s*(,([^()]|\([^()]*\))*)?\)")
COLOR_DECL = re.compile(r"(?<![\w-])(color|background-color|background)\s*:\s*([^;{}]+)")
IMPORTANT = re.compile(r"!\s*important", re.I)
INLINE_STYLE = re.compile(r"""style\s*=\s*(["'])(.*?)\1""", re.S)
STYLE_BLOCK = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)

NAMED = {"white": "#ffffff", "black": "#000000", "red": "#ff0000", "transparent": None,
         "inherit": None, "currentcolor": None, "initial": None, "unset": None, "none": None}


@dataclass
class Finding:
    severity: str            # error | warn | note
    kind: str
    file: str
    line: int
    message: str


@dataclass
class Doc:
    path: Path
    text: str
    offset: int = 0          # line offset when the CSS came from a <style> block
    origin: str = "css"
    var_defs: list = field(default_factory=list)


def line_of(text: str, idx: int, offset: int = 0) -> int:
    return text.count("\n", 0, idx) + 1 + offset


# ---------------------------------------------------------------- colour parsing
def parse_color(value: str) -> tuple[float, float, float] | None:
    # NOTE: never use str.rstrip("!important") here — rstrip takes a CHARACTER SET, so it eats
    # trailing a/i/m/n/o/p/r/t and silently turns "#7a7a7a" into "#7a7a7", which then fails to
    # parse and skips the contrast check without a word. Strip the keyword with a regex.
    v = re.sub(r"\s*!\s*important\s*$", "", value.strip().lower()).strip()
    if v in NAMED:
        v = NAMED[v] or ""
        if not v:
            return None
    m = re.fullmatch(r"#([0-9a-f]{3,8})", v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        if len(h) >= 6:
            return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        return None
    m = re.fullmatch(r"rgba?\(([^)]+)\)", v)
    if m:
        parts = re.split(r"[,\s/]+", m.group(1).strip())
        try:
            nums = []
            for p in parts[:3]:
                nums.append(float(p[:-1]) / 100 if p.endswith("%") else float(p) / 255)
            return tuple(nums) if len(nums) == 3 else None
        except ValueError:
            return None
    m = re.fullmatch(r"hsla?\(([^)]+)\)", v)
    if m:
        parts = re.split(r"[,\s/]+", m.group(1).strip())
        try:
            h = float(re.sub(r"deg$", "", parts[0])) % 360 / 360
            s = float(parts[1].rstrip("%")) / 100
            light = float(parts[2].rstrip("%")) / 100
        except (ValueError, IndexError):
            return None

        def hue(p, q, t):
            t %= 1
            if t < 1 / 6: return p + (q - p) * 6 * t
            if t < 1 / 2: return q
            if t < 2 / 3: return p + (q - p) * (2 / 3 - t) * 6
            return p
        if s == 0:
            return (light, light, light)
        q = light * (1 + s) if light < 0.5 else light + s - light * s
        p = 2 * light - q
        return (hue(p, q, h + 1 / 3), hue(p, q, h), hue(p, q, h - 1 / 3))
    return None


def relative_luminance(rgb: tuple[float, float, float]) -> float:
    def chan(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ---------------------------------------------------------------- collection
def collect(root: Path) -> list[Doc]:
    docs: list[Doc] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        ext = path.suffix.lower()
        if ext in STYLE_EXT:
            try:
                docs.append(Doc(path, COMMENT.sub("", path.read_text("utf-8", errors="replace"))))
            except OSError:
                continue
        elif ext in MARKUP_EXT:
            try:
                raw = path.read_text("utf-8", errors="replace")
            except OSError:
                continue
            for m in STYLE_BLOCK.finditer(raw):
                docs.append(Doc(path, COMMENT.sub("", m.group(1)),
                                offset=raw.count("\n", 0, m.start(1)), origin="style-block"))
            docs.append(Doc(path, raw, origin="markup"))
    return docs


def build_blocks(text: str) -> list[tuple[int, int, str, str]]:
    """Every {...} block as (start, end, own_selector, full_ancestor_chain).

    The chain matters: `--x` inside `@media (prefers-color-scheme: dark) { :root { ... } }`
    has the immediate selector `:root`, which looks like a collision until you can see the
    @media wrapping it. Theme redefinition is legitimate; only the chain shows that.
    """
    blocks: list[tuple[int, int, str, str]] = []
    stack: list[tuple[int, str]] = []
    pos = 0
    for m in re.finditer(r"[{}]", text):
        if m.group() == "{":
            sel = " ".join(text[pos:m.start()].split())[-160:]
            stack.append((m.end(), sel))
        else:
            if stack:
                start, sel = stack.pop()
                chain = " ".join(s for _, s in stack) + " " + sel
                blocks.append((start, m.start(), sel, chain.strip()))
        pos = m.end()
    return blocks


def chain_at(blocks: list[tuple[int, int, str, str]], idx: int) -> str:
    """The ancestor chain of the innermost block containing idx."""
    best, best_span = "", None
    for start, end, _sel, chain in blocks:
        if start <= idx < end:
            span = end - start
            if best_span is None or span < best_span:
                best, best_span = chain, span
    return best


# ---------------------------------------------------------------- checks
def audit(root: Path) -> list[Finding]:
    docs = collect(root)
    out: list[Finding] = []
    defs: dict[str, list[tuple[str, int, str, str]]] = {}   # name -> [(file,line,value,selector)]
    uses: list[tuple[str, str, int, bool]] = []             # (name,file,line,has_fallback)
    rule_props: dict[tuple[str, str], list[tuple[str, int]]] = {}  # (selector,prop) -> [(file,line)]

    for doc in docs:
        rel = str(doc.path.relative_to(root))
        if doc.origin == "markup":
            # inline style attributes only
            for m in INLINE_STYLE.finditer(doc.text):
                body = m.group(2)
                if COLOR_DECL.search(body):
                    out.append(Finding(
                        "warn", "inline-style", rel, line_of(doc.text, m.start()),
                        f'inline style sets a colour: style="{body.strip()[:60]}" — inline wins over '
                        "every stylesheet and cannot be themed or overridden at the source"))
            continue

        blocks = build_blocks(doc.text)
        for m in VAR_DEF.finditer(doc.text):
            name, value = m.group(1), m.group(2).strip()
            sel = chain_at(blocks, m.start())
            defs.setdefault(name, []).append((rel, line_of(doc.text, m.start(), doc.offset), value, sel))

        for m in VAR_USE.finditer(doc.text):
            uses.append((m.group(1), rel, line_of(doc.text, m.start(), doc.offset), bool(m.group(2))))

        for m in COLOR_DECL.finditer(doc.text):
            prop, value = m.group(1), m.group(2).strip()
            ln = line_of(doc.text, m.start(), doc.offset)
            sel = chain_at(blocks, m.start())
            if sel and not sel.lstrip().startswith("@"):
                rule_props.setdefault((sel, prop), []).append((rel, ln))
            if IMPORTANT.search(value):
                out.append(Finding(
                    "error", "important", rel, ln,
                    f"`{prop}: {value.strip()}` — !important on a colour is an override, not a fix; "
                    "it hides which rule really owns this and breaks the next change "
                    "(css-architecture: fix at the source)"))

        # same-rule colour + background pair -> contrast is computable exactly
        for block in re.finditer(r"([^{}]+)\{([^{}]*)\}", doc.text):
            sel, body = " ".join(block.group(1).split()), block.group(2)
            fg = bg = None
            for m in COLOR_DECL.finditer(body):
                val = m.group(2)
                resolved = resolve(val, defs)
                if m.group(1) == "color":
                    fg = resolved or fg
                else:
                    bg = resolved or bg
            if fg and bg:
                ratio = contrast_ratio(fg, bg)
                if ratio < 4.5:
                    out.append(Finding(
                        "error" if ratio < 3 else "warn", "contrast", rel,
                        line_of(doc.text, block.start(), doc.offset),
                        f"`{sel[:60]}` text contrast is {ratio:.2f}:1 (needs 4.5:1 for body text, "
                        "3:1 for large) — this text is hard or impossible to read"))

    # --- a var nothing defines: the text falls back to inherited, often invisible
    defined = set(defs)
    for name, rel, ln, has_fallback in uses:
        if name not in defined and not has_fallback:
            out.append(Finding(
                "error", "undefined-var", rel, ln,
                f"`var({name})` is used but {name} is never defined, and there is no fallback — "
                "the property is dropped and the element inherits, which is how text turns "
                "black-on-black or disappears"))

    # --- the same token defined twice with different values: the override the user keeps hitting
    for name, places in defs.items():
        real = [(f, l, v, s) for f, l, v, s in places if not THEME_SELECTOR.search(s or "")]
        values = {v.strip() for _, _, v, _ in real}
        if len(real) > 1 and len(values) > 1:
            where = "; ".join(f"{f}:{l} = {v.strip()[:28]}" for f, l, v, _ in real[:4])
            out.append(Finding(
                "error", "token-collision", real[-1][0], real[-1][1],
                f"`{name}` is defined {len(real)} times with different values outside any theme "
                f"scope: {where}. Whichever file loads last silently wins, so the colour "
                "changes depending on import order. One token, one definition."))

    # --- the same property set on the same selector in more than one file
    for (sel, prop), places in rule_props.items():
        files = {f for f, _ in places}
        if len(files) > 1:
            where = "; ".join(f"{f}:{l}" for f, l in places[:4])
            out.append(Finding(
                "warn", "cross-file-override", places[-1][0], places[-1][1],
                f"`{sel[:50]} {{ {prop} }}` is set in {len(files)} files — {where}. "
                "Load order decides which colour the user sees; move it to the one file that owns "
                "this component"))

    return out


def resolve(value: str, defs: dict, depth: int = 0):
    """Resolve a colour value, following var() one definition deep when unambiguous."""
    if depth > 4:
        return None
    m = VAR_USE.search(value)
    if m:
        name = m.group(1)
        places = defs.get(name, [])
        values = {v.strip() for _, _, v, _ in places}
        if len(values) == 1:
            return resolve(next(iter(values)), defs, depth + 1)
        fallback = m.group(2)
        return resolve(fallback.lstrip(","), defs, depth + 1) if fallback else None
    return parse_color(value)


def main() -> int:
    ap = argparse.ArgumentParser(description="Static CSS colour and override audit")
    ap.add_argument("project", nargs="?", default=".", type=Path)
    ap.add_argument("--json", type=Path, help="write findings as JSON")
    ap.add_argument("--fail-on", choices=("error", "warn", "never"), default="error")
    args = ap.parse_args()

    root = args.project.resolve()
    if not root.is_dir():
        print(f"[FAIL] not a directory: {root}", file=sys.stderr)
        return 2

    findings = audit(root)
    order = {"error": 0, "warn": 1, "note": 2}
    findings.sort(key=lambda f: (order[f.severity], f.file, f.line))

    errors = [f for f in findings if f.severity == "error"]
    warns = [f for f in findings if f.severity == "warn"]

    if args.json:
        args.json.write_text(json.dumps(
            {"errors": len(errors), "warnings": len(warns),
             "findings": [f.__dict__ for f in findings]}, indent=2), encoding="utf-8")

    if not findings:
        print("[PASS] CSS audit: no colour, token, or override problems found")
        return 0

    print(f"{'[FAIL]' if errors else '[WARN]'} CSS audit: {len(errors)} error(s), {len(warns)} warning(s)")
    for f in findings[:60]:
        mark = {"error": "E", "warn": "W", "note": "."}[f.severity]
        print(f"  [{mark}] {f.file}:{f.line}  {f.kind}\n      {f.message}")
    if len(findings) > 60:
        print(f"  ... and {len(findings) - 60} more")

    if args.fail_on == "never":
        return 0
    if args.fail_on == "warn":
        return 1 if findings else 0
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
