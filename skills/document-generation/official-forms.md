# Official forms — replicating a template you are not allowed to change

Read when the output must match a form some authority publishes: COMELEC, BIR, DepEd, PhilHealth,
SSS, LGU, a school's registrar form. The rule here is different from every other document: **you are
not designing anything.** The layout is given, it is often legally significant, and "close enough"
is rejected at the counter.

## 1. Get the authority's own file first

In order of what you should try:

1. **The published PDF.** Almost every agency publishes one. This is the highest-fidelity input and
   it makes approach A below possible.
2. **The published DOCX/XLS.** Fill it as a template ([office-docs.md](./office-docs.md)) and, if a
   PDF is needed, print it once to PDF and use that as your reference.
3. **A clean scan**, 300 DPI, flatbed, not a phone photo. Last resort — a photo has perspective
   distortion and you will chase alignment forever.

Store it in the repo under `resources/forms/<agency>-<form>-<revision>.pdf`, and record **where and
when you obtained it**. Forms get revised without announcement; the revision you built against is
part of the code, and the day someone reports "the office rejected it" the first question is which
revision you are producing.

## 2. Choose the approach by what you were given

### A. Overlay the authority's PDF — the default, and the only one with zero drift

Use their file as the background and draw values on top. The form is *theirs*, pixel for pixel; you
supply only the values. Nothing you do can shift a line or a box.

```python
# Python — pypdf overlay. Draw values on a transparent page, merge onto the official form.
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Doc", "resources/fonts/DejaVuSans.ttf"))  # has ₱ and ñ

form = PdfReader("resources/forms/comelec-cef1-rev2026.pdf")
page = form.pages[0]

buf = BytesIO()
c = canvas.Canvas(buf, pagesize=(page.mediabox.width, page.mediabox.height))
c.setFont("Doc", 10)
for field, (x, y) in FIELD_POSITIONS.items():      # points, origin BOTTOM-LEFT
    c.drawString(x, y, str(values[field]))
c.save(); buf.seek(0)

page.merge_page(PdfReader(buf).pages[0])
w = PdfWriter(); w.add_page(page)
with open(out, "wb") as f: w.write(f)
```

Node: `pdf-lib` (`PDFDocument.load` → `page.drawText`). PHP: `FPDI` on top of FPDF/TCPDF.

### B. The form is already fillable — check before doing any work

Many government PDFs are AcroForms with real named fields. If so, this is a two-line job and the
alignment problem does not exist. **Check every time**, before measuring anything:

```python
from pypdf import PdfReader
print(PdfReader("form.pdf").get_fields())     # None → not fillable; a dict → use the field names
```

Fill with `PdfWriter.update_page_form_field_values(...)`, then **flatten** it (set the field
read-only or render it flat) so the values cannot be edited after issue. An unflattened official
document is an editable one.

### C. Rebuild it — only when you have no usable file

You are reconstructing, so you must measure, and you must expect to iterate. Use it when all you
have is a scan, or when the form must reflow (a table with a variable number of rows).

## 3. Finding the coordinates without guessing

PDF coordinates are **points** (72 per inch) with the origin at the **bottom-left**. Screen tools
give you top-left pixels. Convert once, in one helper, or you will mix them up:

```python
PT_PER_MM = 72 / 25.4
def from_top(y_mm, page_height_pt):        # measured from the top edge in mm -> PDF y
    return page_height_pt - y_mm * PT_PER_MM
```

**Anchor to the form's own labels rather than to absolute numbers.** `pdfplumber` gives you the
bounding box of every word in the authority's file, so you can position relative to the label that
is already printed there — which survives a revision that shifts the layout slightly:

```python
import pdfplumber
with pdfplumber.open("resources/forms/coe-rev2026.pdf") as doc:
    page = doc.pages[0]
    for w in page.extract_words():
        print(f'{w["text"]:<22} x0={w["x0"]:7.1f} top={w["top"]:7.1f}')
    # place a value just right of a known label, on the same baseline:
    label = next(w for w in page.extract_words() if w["text"] == "PRECINCT")
    x = label["x1"] + 12
    y = page.height - label["bottom"]          # pdfplumber measures from the top
```

From a **scan**, measure in pixels at a known DPI: `points = pixels * 72 / dpi`. Scan at 300 DPI and
the arithmetic stays clean.

## 4. The rules that get a form rejected at the counter

- **Never move, restyle, or "improve" the form.** Not the wording, not the spacing, not the logo,
  not a typo the agency made. It is their document.
- **Values sit inside their box, on the baseline** — not overlapping the rule, not touching the
  border.
- **Do not let a value overflow its field.** A long name must shrink to fit or truncate by the
  agency's rule, never spill into the next box. Decide the rule and apply it consistently.
- **Page size is theirs.** Philippine government forms are frequently **Legal or Folio (8.5×13in)**,
  not A4. Producing A4 changes every measurement and gets rejected. Read it from their file rather
  than assuming.
- **Serial and control numbers** follow the agency's format exactly, including leading zeros and
  separators, and are issued from the database, not computed from a count ([pdf.md](./pdf.md) §5).
- **Signature and date blocks stay empty** unless you are authorised to fill them. A pre-signed
  official document is a serious problem, not a convenience.
- **Print one on the real paper** before shipping the feature. Screen alignment and printer
  alignment differ, and printers have a non-printable edge.

## 5. Verify it — do not assume it lines up

This is what `scripts/doc_verify.py` exists for. It renders the result, checks what silently breaks,
and diffs against the authority's blank form so misalignment is *visible*:

```bash
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/doc_verify.py \
  out/coe-filled.pdf \
  --reference resources/forms/coe-rev2026.pdf \
  --outdir .agents/verify/coe --page-size folio --glyphs "₱,ñ"
```

It writes `page-*.png`, `diff-p*.png` and `doc-verdict.json`. **Then open the images and look at
them.** The verdict catches page size, unembedded fonts, missing glyphs, unextractable text and
content near the edge; only your eyes catch a value sitting one line too low.

Read the diff image this way: it shows **only what you added** on top of their form. Your values
should appear, cleanly, in their boxes — and nothing else should. If parts of the form itself show
up in the diff, you moved or redrew something that was theirs.

## 6. Done

- The blank form is in the repo with its revision and where it came from.
- Approach A or B was used, or the reason a rebuild was unavoidable is written down.
- `doc_verify.py --reference` run; `doc-verdict.json` has `status: pass`; the rendered pages **and
  the diff images were looked at**, not just generated.
- Tested with the awkward real cases: the longest name in the database, a name with `ñ`, an amount
  over one million, an empty optional field.
- One printed on the paper the office actually uses.
