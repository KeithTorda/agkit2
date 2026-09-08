# PDF generation — reports, receipts, certificates, official forms

Read when producing any PDF. The format decision, authorisation and job rules are in
[SKILL.md](./SKILL.md); this file is how to actually render one that survives printing and audit.

## 1. Two families — pick by what the document is

**HTML → PDF** (headless Chrome via Puppeteer/Playwright/Browsershot, or WeasyPrint)
Use when the document mirrors something you already lay out in HTML and CSS: a statement, a summary
report, an itemised list, anything with flowing content that paginates. You get CSS, your existing
tokens, and one layout to maintain.

**Programmatic layout** (ReportLab, PDFKit, FPDF, dompdf, PHPWord→PDF)
Use when position is the requirement, not the appearance: a certificate where the name sits on a
specific line of a pre-printed design, an official form whose boxes must align with the government
template, a thermal receipt at a fixed width. Also the right answer when you need thousands of small
documents fast — a Chrome instance per document is the wrong shape.

**Overlay** (fill an existing PDF: pdf-lib, pypdf, FPDI)
Use when an authority publishes the form as a PDF and you must put values into it. Do not rebuild
their form; draw on top of it. This is usually correct for COMELEC, BIR and DepEd templates.

## 2. Print CSS — the part everyone skips

An HTML page that looks right in the browser paginates badly by default.

```css
@page { size: A4; margin: 18mm 15mm; }
@page :first { margin-top: 12mm; }

/* repeat the header on every page of a long table — the single highest-value rule here */
thead { display: table-header-group; }
tfoot { display: table-footer-group; }
tr, img, figure, .signature-block { break-inside: avoid; }
h2, h3 { break-after: avoid; }          /* never a heading alone at the bottom */

/* backgrounds and borders print only if you say so */
.status-paid { print-color-adjust: exact; -webkit-print-color-adjust: exact; }

@media print {
  nav, .no-print, button { display: none; }
  a[href^="http"]::after { content: " (" attr(href) ")"; }  /* links are dead on paper */
}
```

Page numbers: `@page { @bottom-right { content: "Page " counter(page) " of " counter(pages); } }`
works in WeasyPrint and print engines that implement CSS Paged Media. **Chrome does not support the
margin boxes** — with Puppeteer use `headerTemplate` / `footerTemplate` with `displayHeaderFooter`,
and remember to set `margin` or the templates are invisible.

Also: `A4` (210×297mm), not `Letter`, for Philippine and most non-US recipients. Government forms are
often **Legal / Folio (8.5×13in)** — check the actual form before assuming.

## 3. Fonts — why `₱` and `ñ` come out as boxes

The renderer only has the fonts you give it. A headless Chrome in a slim container has almost none.

- Embed the font with the document (`@font-face` with a local file, or the library's font
  registration). Do not rely on a system font being present in production.
- Verify the face actually contains `₱` (U+20B1). Many otherwise complete fonts do not. If it does
  not, use one that does rather than substituting `PHP` or `P`.
- Set `lang` and let the text render as UTF-8 end to end. Composed vs decomposed `ñ` both appear in
  real data — normalise (NFC) before rendering.

## 4. Headless Chrome in production

It is a browser. Treat it like one.

- **Never one instance per request.** Keep a pool, or run generation in a queue with limited
  concurrency. Two simultaneous month-end reports will exhaust memory otherwise.
- Wait for the real signal — `networkidle` plus an explicit "content ready" marker — not a timeout.
  A chart that had not finished drawing produces a blank box, silently.
- `printBackground: true` or every background colour disappears.
- The container needs the browser's system libraries; the base image that runs your app usually does
  not have them. This is the most common "works locally, empty PDF in production".
- It renders whatever URL you give it. If that URL is user-influenced you have built an SSRF: render
  from trusted local HTML, or an allowlisted route with a signed, short-lived token.

## 5. Receipts, invoices and certificates

Documents with authority have requirements beyond layout.

- **The number is issued, not derived.** Sequence it in the database (a table with a unique
  constraint, or a sequence), inside the transaction that creates the record. Never compute it from
  a count, which repeats under concurrency.
- **Reprints are marked.** The first print and the fifth look identical otherwise; label reprints
  and record who reprinted and when.
- **Cancellation is a document, not a delete.** Void with a reason and keep both. An official series
  with a gap in it is a finding.
- **The document is a snapshot.** Store the rendered PDF, or every input including the price, tax
  rate and issuer details as they were at issue. Regenerating later from live tables produces a
  different document with the same number.
- **Verification.** For a certificate that leaves your control, put a verification path on it — a
  code or QR resolving to a page that confirms it, so a recipient can check without calling you.
- Amount in words for financial documents, if the recipient's process expects it; get the Philippine
  peso/centavo phrasing right and test at 0, 1, and above one million.

## 6. Before you call it done

- **Open the PDF.** Not the HTML — the PDF, in a real viewer, at the real page size. Every check
  below fails silently otherwise.
- Print it, or preview at 100%: nothing clipped at the margins, no orphan heading, table headers
  repeat on page 2, the signature block did not split across pages.
- `₱`, `ñ`, and any long identifier render correctly and select as real text (a searchable PDF, not
  an image of one).
- Page count is bounded — a report with an unbounded table needs a row cap or a job.
- File size is sane; a 40 MB PDF usually means unoptimised images.
- Text is selectable and the reading order is sensible if the document must be accessible.
