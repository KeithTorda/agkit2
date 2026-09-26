#!/usr/bin/env python3
"""Static CSS audit: why text is the wrong colour, with file:line, before opening a browser.

Finds a custom property defined twice with different values outside any theme scope, a var()
nothing defines, a colour pair in one rule that cannot be read, inline colour styles, the same
selector coloured in several files, and overrides (`!important`).

Advisory by default (exit 0). --strict: errors exit 1 and `!important` counts as an error.

Ignored: node_modules, vendor, dist, build and other generated folders, *.min.css, and
compiled or vendor bundles that start with a `/*!` licence banner. Framework variables
(--tw-*, --bs-*, Tailwind v4 theme namespaces when Tailwind is used) and variables set from
markup or JavaScript count as defined. CSS modules, Vue `<style scoped>`, Svelte and Astro
styles are component-scoped, so the same selector in two of them is not an override.

Scans .css/.scss/.sass/.less plus <style> blocks and style="" attributes in markup files.

Usage:
  python css_audit.py .
  python css_audit.py . --json
  python css_audit.py . --strict --report css-audit.json
Exit codes: 0 ok (always, unless --strict), 1 errors with --strict, 2 usage.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

SKIP_DIRS = {"node_modules", "vendor", "dist", "build", ".next", ".nuxt", ".output", ".svelte-kit",
             ".astro", ".git", "out", "coverage", "__pycache__", ".venv", "venv", "storage",
             "bower_components", ".turbo", ".vercel", ".cache", "target"}
SKIP_REL_PREFIXES = ("public/build/", "public/vendor/", "public/css/filament", "static/vendor/",
                     "assets/vendor/", "wwwroot/lib/")
STYLE_EXT = {".css", ".scss", ".sass", ".less"}
MARKUP_EXT = {".html", ".htm", ".vue", ".svelte", ".astro", ".jsx", ".tsx", ".php"}
SCRIPT_EXT = {".js", ".ts", ".jsx", ".tsx", ".mjs", ".vue", ".svelte", ".astro"}
MAX_BYTES = 1_500_000

# Selectors under which a token is expected to be redefined: theming, not collision.
THEME_SELECTOR = re.compile(
    r"(\.dark|\[data-theme|\[data-mode|\[data-color|:root\s*\.|:root\[|\.light|\.theme-|@media|"
    r"prefers-color-scheme|@supports|@container|:host|@custom-variant|@variant|:where\(\.dark|"
    r"\[data-bs-theme)", re.I)
REDUCED_MOTION_OR_PRINT = re.compile(r"prefers-reduced-motion|@media\s+print|forced-colors", re.I)
FRAMEWORK_VAR_PREFIXES = ("--tw-", "--bs-", "--wp--", "--wp-", "--mdc-", "--mui-", "--chakra-", "--radix-",
                          "--swiper-", "--fa-", "--plyr-", "--toastify-", "--rdp-", "--sonner-",
                          "--vaul-", "--leaflet-", "--fc-", "--glide-", "--splide-", "--flowbite-", "--daisy")
TAILWIND_NAMESPACES = ("--color-", "--font-", "--text-", "--spacing", "--radius", "--shadow-", "--inset-shadow-",
                       "--drop-shadow-", "--blur-", "--breakpoint-", "--container-", "--ease-", "--animate-",
                       "--leading-", "--tracking-", "--perspective-", "--aspect-", "--default-", "--font-weight-",
                       "--text-shadow-")

COMMENT = re.compile(r"/\*.*?\*/", re.S)
VAR_DEF = re.compile(r"(?<![\w-])(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]*)")
PROPERTY_AT = re.compile(r"@property\s+(--[A-Za-z0-9_-]+)")
VAR_USE = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)\s*(,([^()]|\([^()]*\))*)?\)")
COLOR_DECL = re.compile(r"(?<![\w-])(color|background-color|background)\s*:\s*([^;{}]+)")
IMPORTANT_DECL = re.compile(r"(?<![\w-])([a-z-]+)\s*:\s*([^;{}]*?!\s*important)", re.I)
INLINE_STYLE = re.compile(r"""\bstyle\s*=\s*(["'])(.*?)\1""", re.S)
STYLE_BLOCK = re.compile(r"<style([^>]*)>(.*?)</style>", re.S | re.I)
JS_VAR_DEF = re.compile(r"""["'`](--[A-Za-z0-9_-]+)["'`]\s*[:,)]|setProperty\(\s*["'`](--[A-Za-z0-9_-]+)""")
VENDOR_BANNER = re.compile(r"^\s*/\*!.{0,400}?(v\d|licen[sc]e|bootstrap|tailwind|normalize|font ?awesome|"
                           r"animate\.css|swiper|bulma|foundation|materialize)", re.I | re.S)

NAMED = {"white": "#ffffff", "black": "#000000", "red": "#ff0000", "transparent": None,
         "inherit": None, "currentcolor": None, "initial": None, "unset": None, "none": None}

SEVERITY_ORDER = {"error": 0, "warn": 1, "note": 2}


def utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass


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
    rel: str
    text: str                # comments blanked, offsets and newlines preserved
    raw: str                 # original text (for justification comments)
    offset: int = 0          # line offset when the CSS came from a <style> block
    origin: str = "css"      # css | style-block | markup
    scoped: bool = False     # CSS modules, <style scoped>, Svelte, Astro
    blocks: list = field(default_factory=list)


def line_of(text: str, idx: int, offset: int = 0) -> int:
    return text.count("\n", 0, idx) + 1 + offset


def blank_comments(text: str) -> str:
    """Replace comments with spaces (newlines kept) so indices and line numbers stay true."""
    return COMMENT.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


# ---------------------------------------------------------------- colour parsing
def parse_color(value: str) -> tuple[float, float, float] | None:
    """An opaque sRGB colour as 0-1 floats, or None (unknown, translucent, gradient, keyword)."""
    # Never str.rstrip("!important"): rstrip takes a character set and turns "#7a7a7a" into
    # "#7a7a7". Strip the keyword with a regex.
    v = re.sub(r"\s*!\s*important\s*$", "", value.strip().lower()).strip()
    if v in NAMED:
        v = NAMED[v] or ""
        if not v:
            return None
    m = re.fullmatch(r"#([0-9a-f]{3,8})", v)
    if m:
        h = m.group(1)
        if len(h) not in (3, 4, 6, 8):
            return None
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) == 8 and int(h[6:8], 16) < 255:
            return None      # translucent: the real colour depends on what is underneath
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]
    m = re.fullmatch(r"rgba?\(([^)]+)\)", v)
    if m:
        parts = [p for p in re.split(r"[,\s/]+", m.group(1).strip()) if p]
        try:
            if len(parts) >= 4:
                alpha = float(parts[3][:-1]) / 100 if parts[3].endswith("%") else float(parts[3])
                if alpha < 1:
                    return None
            nums = [float(p[:-1]) / 100 if p.endswith("%") else float(p) / 255 for p in parts[:3]]
            return tuple(nums) if len(nums) == 3 else None  # type: ignore[return-value]
        except ValueError:
            return None
    m = re.fullmatch(r"hsla?\(([^)]+)\)", v)
    if m:
        parts = [p for p in re.split(r"[,\s/]+", m.group(1).strip()) if p]
        try:
            h = float(re.sub(r"deg$", "", parts[0])) % 360 / 360
            s = float(parts[1].rstrip("%")) / 100
            light = float(parts[2].rstrip("%")) / 100
            if len(parts) >= 4:
                alpha = float(parts[3][:-1]) / 100 if parts[3].endswith("%") else float(parts[3])
                if alpha < 1:
                    return None
        except (ValueError, IndexError):
            return None

        def hue(p: float, q: float, t: float) -> float:
            t %= 1
            if t < 1 / 6:
                return p + (q - p) * 6 * t
            if t < 1 / 2:
                return q
            if t < 2 / 3:
                return p + (q - p) * (2 / 3 - t) * 6
            return p
        if s == 0:
            return (light, light, light)
        q = light * (1 + s) if light < 0.5 else light + s - light * s
        p = 2 * light - q
        return (hue(p, q, h + 1 / 3), hue(p, q, h), hue(p, q, h - 1 / 3))
    return None


def relative_luminance(rgb: tuple[float, float, float]) -> float:
    def chan(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ---------------------------------------------------------------- collection
def is_skipped(rel: Path) -> bool:
    parts = rel.parts[:-1]
    if any(p in SKIP_DIRS for p in parts):
        return True
    posix = rel.as_posix()
    return ".min." in rel.name or posix.startswith(SKIP_REL_PREFIXES)


def is_vendor_bundle(text: str) -> bool:
    return bool(VENDOR_BANNER.match(text[:600]))


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            path = Path(dirpath) / name
            rel = path.relative_to(root)
            if is_skipped(rel):
                continue
            yield path, rel


def _read(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_BYTES:
            return None
        return path.read_text("utf-8", errors="replace")
    except OSError:
        return None


def collect(root: Path) -> tuple[list[Doc], set[str], bool]:
    """Stylesheet docs, custom properties defined outside CSS, and whether Tailwind is in use."""
    docs: list[Doc] = []
    external_defs: set[str] = set()
    tailwind = False
    pkg = root / "package.json"
    if pkg.is_file():
        text = _read(pkg) or ""
        tailwind = '"tailwindcss"' in text or '"@tailwindcss/' in text
    for path, rel in iter_files(root):
        ext = path.suffix.lower()
        if ext not in STYLE_EXT and ext not in MARKUP_EXT and ext not in SCRIPT_EXT:
            continue
        raw = _read(path)
        if raw is None:
            continue
        rel_s = rel.as_posix()
        if ext in STYLE_EXT:
            if is_vendor_bundle(raw):
                continue
            if re.search(r"""@import\s+["']tailwindcss|@tailwind\s|@theme\b""", raw):
                tailwind = True
            scoped = ".module." in path.name.lower()
            docs.append(Doc(path, rel_s, blank_comments(raw), raw, scoped=scoped))
            continue
        if ext in MARKUP_EXT:
            for m in STYLE_BLOCK.finditer(raw):
                attrs = m.group(1).lower()
                scoped = ext in {".svelte", ".astro"} or "scoped" in attrs or "module" in attrs
                offset = raw.count("\n", 0, m.start(2))
                docs.append(Doc(path, rel_s, blank_comments(m.group(2)), m.group(2), offset=offset,
                                origin="style-block", scoped=scoped))
            docs.append(Doc(path, rel_s, raw, raw, origin="markup"))
            for m in INLINE_STYLE.finditer(raw):
                external_defs.update(n for n, _ in VAR_DEF.findall(m.group(2)))
        if ext in SCRIPT_EXT or ext in MARKUP_EXT:
            for m in JS_VAR_DEF.finditer(raw):
                external_defs.add(m.group(1) or m.group(2))
    return docs, external_defs, tailwind


def build_blocks(text: str) -> list[tuple[int, int, str, str]]:
    """Every {...} block as (start, end, own_selector, full_ancestor_chain).

    `--x` inside `@media (prefers-color-scheme: dark) { :root { ... } }` has the immediate
    selector `:root`; only the chain shows the @media, which makes it theming, not collision.
    """
    blocks: list[tuple[int, int, str, str]] = []
    stack: list[tuple[int, str]] = []
    pos = 0
    for m in re.finditer(r"[{};]", text):
        if m.group() == ";":
            pos = m.end()
            continue
        if m.group() == "{":
            sel = " ".join(text[pos:m.start()].split())[-160:]
            stack.append((m.end(), sel))
        elif stack:
            start, sel = stack.pop()
            chain = " ".join(s for _, s in stack) + " " + sel
            blocks.append((start, m.start(), sel, chain.strip()))
        pos = m.end()
    return blocks


def chain_at(blocks: list[tuple[int, int, str, str]], idx: int) -> str:
    best, best_span = "", None
    for start, end, _sel, chain in blocks:
        if start <= idx < end:
            span = end - start
            if best_span is None or span < best_span:
                best, best_span = chain, span
    return best


def justified(raw: str, idx: int) -> bool:
    """An override with a comment on its line or the line above says why - a note, not a warning."""
    line_start = raw.rfind("\n", 0, idx) + 1
    prev_start = raw.rfind("\n", 0, max(line_start - 1, 0)) + 1
    line_end = raw.find("\n", idx)
    window = raw[prev_start: line_end if line_end >= 0 else len(raw)]
    return "/*" in window or "//" in window


def is_framework_var(name: str, tailwind: bool) -> bool:
    if name.startswith(FRAMEWORK_VAR_PREFIXES):
        return True
    return tailwind and name.startswith(TAILWIND_NAMESPACES)


# ---------------------------------------------------------------- checks
def audit(root: Path, strict: bool = False) -> list[Finding]:
    docs, external_defs, tailwind = collect(root)
    out: list[Finding] = []
    defs: dict[str, list[tuple[str, int, str, str]]] = {}      # name -> [(file, line, value, chain)]
    uses: list[tuple[str, str, int, bool]] = []                 # (name, file, line, has_fallback)
    rule_props: dict[tuple[str, str], list[tuple[str, int]]] = {}
    pairs: list[tuple[Doc, str, int, str | None, str | None]] = []

    for doc in docs:
        rel = doc.rel
        if doc.origin == "markup":
            for m in INLINE_STYLE.finditer(doc.text):
                body = m.group(2)
                if COLOR_DECL.search(body) and "var(" not in body:
                    out.append(Finding(
                        "warn", "inline-style", rel, line_of(doc.text, m.start()),
                        f'inline style sets a colour: style="{body.strip()[:60]}" - inline wins over every '
                        "stylesheet and cannot be themed; move it to the component's CSS or a token"))
            continue

        doc.blocks = build_blocks(doc.text)
        for m in PROPERTY_AT.finditer(doc.text):
            external_defs.add(m.group(1))
        for m in VAR_DEF.finditer(doc.text):
            name, value = m.group(1), m.group(2).strip()
            chain = chain_at(doc.blocks, m.start())
            if not chain:
                continue          # not inside a rule: e.g. a SCSS map or a stray token
            defs.setdefault(name, []).append((rel, line_of(doc.text, m.start(), doc.offset), value, chain))
        for m in VAR_USE.finditer(doc.text):
            uses.append((m.group(1), rel, line_of(doc.text, m.start(), doc.offset), bool(m.group(2))))

        for m in COLOR_DECL.finditer(doc.text):
            prop = m.group(1)
            chain = chain_at(doc.blocks, m.start())
            if chain and not chain.lstrip().startswith("@") and not doc.scoped:
                rule_props.setdefault((chain, prop), []).append((rel, line_of(doc.text, m.start(), doc.offset)))

        for m in IMPORTANT_DECL.finditer(doc.text):
            prop, value = m.group(1), " ".join(m.group(2).split())
            ln = line_of(doc.text, m.start(), doc.offset)
            chain = chain_at(doc.blocks, m.start())
            if prop.startswith("--"):
                continue
            if REDUCED_MOTION_OR_PRINT.search(chain):
                continue          # the standard reduced-motion / print reset is not an override
            why = justified(doc.raw, m.start())
            severity = "error" if strict and not why else ("note" if why else "warn")
            out.append(Finding(
                severity, "important", rel, ln,
                f"`{chain[-50:]} {{ {prop}: {value[:50]} }}` - !important overrides the cascade; fix the rule "
                "that owns this (css-architecture: fix at the source)"
                + (" (a comment explains it)" if why else "; if the source is third-party CSS, add a one-line comment saying why")))

        # the same rule sets text and background: contrast is computable (resolved after all defs)
        for block in re.finditer(r"([^{}]+)\{([^{}]*)\}", doc.text):
            sel, body = " ".join(block.group(1).split()), block.group(2)
            fg = bg = None
            for m in COLOR_DECL.finditer(body):
                if m.group(1) == "color":
                    fg = m.group(2)
                else:
                    bg = m.group(2)
            if fg and bg:
                lead = len(block.group(1)) - len(block.group(1).lstrip())
                pairs.append((doc, sel, line_of(doc.text, block.start() + lead, doc.offset), fg, bg))

    for doc, sel, ln, fg_raw, bg_raw in pairs:
        fg, bg = resolve(fg_raw or "", defs), resolve(bg_raw or "", defs)
        if fg and bg:
            ratio = contrast_ratio(fg, bg)
            if ratio < 4.5:
                out.append(Finding(
                    "error" if ratio < 3 else "warn", "contrast", doc.rel, ln,
                    f"`{sel[:60]}` text contrast is {ratio:.2f}:1 (4.5:1 needed for body text, 3:1 for large "
                    "text) - hard or impossible to read"))

    defined = set(defs) | external_defs
    reported: set[tuple[str, str]] = set()
    for name, rel, ln, has_fallback in uses:
        if name in defined or has_fallback or is_framework_var(name, tailwind) or (name, rel) in reported:
            continue
        reported.add((name, rel))
        out.append(Finding(
            "error", "undefined-var", rel, ln,
            f"`var({name})` is used but {name} is never defined and has no fallback - the property is dropped "
            "and the element inherits, which is how text turns dark-on-dark or disappears"))

    for name, places in defs.items():
        real = [(f, l, v, s) for f, l, v, s in places if not THEME_SELECTOR.search(s or "")]
        values = {" ".join(v.split()) for _, _, v, _ in real}
        if len(real) > 1 and len(values) > 1:
            where = "; ".join(f"{f}:{l} = {v.strip()[:28]}" for f, l, v, _ in real[:4])
            out.append(Finding(
                "error", "token-collision", real[-1][0], real[-1][1],
                f"`{name}` is defined {len(real)} times with different values outside any theme scope: {where}. "
                "Whichever loads last wins, so the colour depends on import order. One token, one definition."))

    for (sel, prop), places in rule_props.items():
        files = {f for f, _ in places}
        if len(files) > 1:
            where = "; ".join(f"{f}:{l}" for f, l in places[:4])
            out.append(Finding(
                "warn", "cross-file-override", places[-1][0], places[-1][1],
                f"`{sel[:50]} {{ {prop} }}` is set in {len(files)} files ({where}); load order decides the colour. "
                "Keep it in the one file that owns the component."))

    out.sort(key=lambda f: (SEVERITY_ORDER[f.severity], f.file, f.line))
    return out


def resolve(value: str, defs: dict, depth: int = 0):
    """Resolve a colour value, following var() when its definition is unambiguous."""
    if depth > 4:
        return None
    m = VAR_USE.search(value)
    if m:
        places = defs.get(m.group(1), [])
        values = {" ".join(v.split()) for _, _, v, _ in places}
        if len(values) == 1:
            return resolve(next(iter(values)), defs, depth + 1)
        fallback = m.group(2)
        return resolve(fallback.lstrip(",").strip(), defs, depth + 1) if fallback and not places else None
    return parse_color(value)


def summarize(findings: list[Finding]) -> dict:
    return {level: sum(f.severity == level for f in findings) for level in ("error", "warn", "note")}


def main(argv: list[str] | None = None) -> int:
    utf8_stdio()
    ap = argparse.ArgumentParser(description="Static CSS colour, token and override audit (advisory).",
                                 epilog="Exit codes: 0 ok (advisory), 1 errors with --strict, 2 usage.")
    ap.add_argument("project", nargs="?", default=".", type=Path)
    ap.add_argument("--strict", action="store_true", help="errors fail (exit 1); uncommented !important is an error")
    ap.add_argument("--json", action="store_true", help="print findings as JSON to stdout")
    ap.add_argument("--report", type=Path, help="also write the JSON to this file")
    ap.add_argument("--limit", type=int, default=60, help="max findings printed (default 60)")
    args = ap.parse_args(argv)

    root = args.project.resolve()
    if not root.is_dir():
        print(f"css_audit: not a directory: {root}", file=sys.stderr)
        return 2

    findings = audit(root, strict=args.strict)
    counts = summarize(findings)
    payload = {"project": str(root), "strict": args.strict, "errors": counts["error"],
               "warnings": counts["warn"], "notes": counts["note"], "findings": [asdict(f) for f in findings]}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    failed = args.strict and counts["error"] > 0

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for f in findings[: args.limit]:
            mark = {"error": "E", "warn": "W", "note": "."}[f.severity]
            print(f"  [{mark}] {f.file}:{f.line}  {f.kind}\n      {f.message}")
        if len(findings) > args.limit:
            print(f"  ... and {len(findings) - args.limit} more (--limit, --json)")
        label = "FAIL" if failed else ("PASS" if not findings else "ADVISORY")
        print(f"css_audit: {label} - {counts['error']} error(s), {counts['warn']} warning(s), {counts['note']} note(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
