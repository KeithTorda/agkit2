#!/usr/bin/env python3
"""Verify a generated document by rendering it and checking what actually came out.

A PDF that "looks right in the HTML" is not verified. This renders every page to PNG so the
agent can LOOK at it, and runs the checks that fail silently otherwise: page size, embedded
fonts, extractable text, glyph survival, and content spilling outside the printable area.

With --reference (the authority's own form), it also produces a per-page difference image so
misalignment against an official template is visible rather than assumed.

Usage:
  python doc_verify.py out.pdf --outdir .agents/verify/sales-report
  python doc_verify.py filled.pdf --reference blank-form.pdf --outdir .agents/verify/coe
  python doc_verify.py out.pdf --page-size legal --glyphs "₱,ñ" --margin-mm 10
"""
from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from pathlib import Path

PAGE_SIZES_MM = {           # name: (width, height) portrait, millimetres
    "a4": (210.0, 297.0),
    "letter": (215.9, 279.4),
    "legal": (215.9, 355.6),
    "folio": (215.9, 330.2),      # 8.5 x 13in — common for PH government forms
    "a5": (148.0, 210.0),
}
PT_PER_MM = 72.0 / 25.4

# Guaranteed present in every PDF viewer; not embedding them is normal, not a defect.
STANDARD_14 = {
    "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique",
    "Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic",
    "Courier", "Courier-Bold", "Courier-Oblique", "Courier-BoldOblique",
    "Symbol", "ZapfDingbats", "Arial", "Arial-Bold", "Arial,Bold",
}


def _mm(points: float) -> float:
    return points / PT_PER_MM


def _strip_subset(base_font: str) -> str:
    """'AAAAAA+DejaVuSans' -> 'DejaVuSans' (subset prefix is six caps and a plus)."""
    return base_font.split("+", 1)[1] if "+" in base_font[:8] else base_font


def render_pages(pdf: Path, outdir: Path, dpi: int, prefix: str) -> list[Path]:
    """Render each page to PNG. pypdfium2 first; poppler's pdftoppm as fallback."""
    outdir.mkdir(parents=True, exist_ok=True)
    try:
        import pypdfium2 as pdfium

        doc = pdfium.PdfDocument(str(pdf))
        out = []
        for i in range(len(doc)):
            img = doc[i].render(scale=dpi / 72).to_pil()
            path = outdir / f"{prefix}-p{i + 1}.png"
            img.save(path)
            out.append(path)
        return out
    except ImportError:
        pass
    import shutil
    import subprocess

    if not shutil.which("pdftoppm"):
        return []
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(outdir / prefix)],
        check=True, capture_output=True,
    )
    return sorted(outdir.glob(f"{prefix}-*.png"))


def diff_pages(generated: list[Path], reference: list[Path], outdir: Path) -> list[dict]:
    """Difference image per page: how far the generated document sits off the template."""
    from PIL import Image, ImageChops

    findings = []
    for i, (g, r) in enumerate(zip(generated, reference), start=1):
        a, b = Image.open(g).convert("L"), Image.open(r).convert("L")
        if a.size != b.size:
            b = b.resize(a.size)
        delta = ImageChops.difference(a, b)
        path = outdir / f"diff-p{i}.png"
        ImageChops.invert(delta).save(path)
        hist = delta.histogram()
        changed = sum(hist[40:])          # pixels differing by more than a faint amount
        findings.append({
            "page": i,
            "changedPixelRatio": round(changed / (a.size[0] * a.size[1]), 4),
            "diffImage": str(path),
        })
    return findings


def inspect(pdf: Path, expect_size: str | None, glyphs: list[str], margin_mm: float) -> dict:
    import pdfplumber
    from pypdf import PdfReader

    report: dict = {"pages": [], "issues": []}
    reader = PdfReader(str(pdf))
    report["pageCount"] = len(reader.pages)

    # --- embedded fonts: a font the PDF only names is a font the recipient may not have
    named, embedded = set(), set()
    for page in reader.pages:
        fonts = (page.get("/Resources") or {}).get("/Font") or {}
        try:
            fonts = fonts.get_object()
        except AttributeError:
            pass
        for ref in (fonts or {}).values():
            try:
                f = ref.get_object()
            except AttributeError:
                continue
            base = str(f.get("/BaseFont", "?")).lstrip("/")
            named.add(base)
            desc = f.get("/FontDescriptor")
            descendants = f.get("/DescendantFonts")
            if descendants is not None and desc is None:
                try:
                    desc = descendants.get_object()[0].get_object().get("/FontDescriptor")
                except Exception:
                    desc = None
            try:
                desc = desc.get_object() if desc is not None else None
            except AttributeError:
                pass
            if desc and any(k in desc for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                embedded.add(base)
    # The PDF standard-14 fonts are present in every viewer, so "not embedded" is expected for
    # them and is not a defect. Generators often leave an unused Helvetica resource behind;
    # failing on that is noise. A NON-standard font that is not embedded is a real defect.
    missing_embed = {f for f in named - embedded if _strip_subset(f) not in STANDARD_14}
    standard_used = sorted({f for f in named - embedded if _strip_subset(f) in STANDARD_14})
    report["fonts"] = {
        "named": sorted(named),
        "notEmbedded": sorted(missing_embed),
        "standardNotEmbedded": standard_used,
    }
    if missing_embed:
        report["issues"].append(
            f"fonts not embedded: {', '.join(sorted(missing_embed))} — these substitute on "
            "another machine and shift the layout")
    if standard_used:
        report.setdefault("notes", []).append(
            f"standard PDF font(s) not embedded (fine, but they have no ₱ and metrics vary "
            f"slightly between viewers): {', '.join(standard_used)}")

    text_total = ""
    with pdfplumber.open(str(pdf)) as doc:
        for i, page in enumerate(doc.pages, start=1):
            w_mm, h_mm = _mm(page.width), _mm(page.height)
            text = page.extract_text() or ""
            text_total += text

            # --- content outside the printable area: clipped when printed
            limit = margin_mm * PT_PER_MM
            outside = [
                w for w in page.extract_words()
                if w["x0"] < limit or w["x1"] > page.width - limit
                or w["top"] < limit or w["bottom"] > page.height - limit
            ]
            entry = {
                "page": i,
                "sizeMm": [round(w_mm, 1), round(h_mm, 1)],
                "hasText": bool(text.strip()),
                "wordsOutsideMargin": len(outside),
            }
            if outside:
                entry["firstOutside"] = [w["text"] for w in outside[:5]]
                report["issues"].append(
                    f"page {i}: {len(outside)} word(s) within {margin_mm}mm of the edge "
                    f"(e.g. {', '.join(w['text'] for w in outside[:3])}) — printers clip this")
            if not text.strip():
                report["issues"].append(
                    f"page {i}: no extractable text — this is an image of a document, not a "
                    "searchable one; it cannot be copied, indexed, or read by a screen reader")
            report["pages"].append(entry)

    # --- page size
    if expect_size:
        want = PAGE_SIZES_MM.get(expect_size.lower())
        if not want:
            report["issues"].append(f"unknown --page-size {expect_size}")
        else:
            for p in report["pages"]:
                got = tuple(p["sizeMm"])
                ok = any(abs(got[0] - a) <= 2 and abs(got[1] - b) <= 2
                         for a, b in (want, want[::-1]))
                if not ok:
                    report["issues"].append(
                        f"page {p['page']} is {got[0]}x{got[1]}mm, expected "
                        f"{expect_size} ({want[0]}x{want[1]}mm)")

    # --- glyph survival: encoding damage shows up here, not on your screen
    missing = []
    for g in glyphs:
        if not g:
            continue
        norm = unicodedata.normalize("NFC", text_total)
        if g not in norm and unicodedata.normalize("NFC", g) not in norm:
            missing.append(g)
    report["glyphs"] = {"checked": glyphs, "missing": missing}
    if missing:
        report["issues"].append(
            f"expected glyph(s) absent from extracted text: {' '.join(missing)} — either the "
            "font lacks them or the encoding broke; they will not copy, search, or print reliably")

    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="Render and check a generated PDF")
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--reference", type=Path, help="the authority's blank form, to diff against")
    ap.add_argument("--outdir", type=Path, default=Path("doc-verify"))
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--page-size", help="a4 | letter | legal | folio | a5")
    ap.add_argument("--glyphs", default="", help='comma-separated, e.g. "₱,ñ"')
    ap.add_argument("--margin-mm", type=float, default=8.0)
    ap.add_argument("--report", type=Path, help="write the JSON verdict here")
    args = ap.parse_args()

    if not args.pdf.is_file():
        print(f"[FAIL] no such file: {args.pdf}", file=sys.stderr)
        return 2

    args.outdir.mkdir(parents=True, exist_ok=True)
    glyphs = [g.strip() for g in args.glyphs.split(",") if g.strip()]
    report = inspect(args.pdf, args.page_size, glyphs, args.margin_mm)

    pages = render_pages(args.pdf, args.outdir, args.dpi, "page")
    report["renderedPages"] = [str(p) for p in pages]
    if not pages:
        report["issues"].append("could not render pages (install pypdfium2 or poppler-utils) — "
                                "the visual check could not run")

    if args.reference:
        ref = render_pages(args.reference, args.outdir, args.dpi, "reference")
        if ref and pages:
            report["templateDiff"] = diff_pages(pages, ref, args.outdir)
            if len(ref) != len(pages):
                report["issues"].append(
                    f"page count differs from the template: {len(pages)} vs {len(ref)}")

    report["status"] = "fail" if report["issues"] else "pass"

    out = args.report or (args.outdir / "doc-verdict.json")
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"{'[PASS]' if report['status'] == 'pass' else '[FAIL]'} {args.pdf.name} — "
          f"{report['pageCount']} page(s), {len(report['issues'])} issue(s)")
    for issue in report["issues"]:
        print(f"  - {issue}")
    print(f"  rendered: {len(pages)} PNG(s) in {args.outdir}  ->  LOOK AT THEM")
    print(f"  verdict:  {out}")
    return 1 if report["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
