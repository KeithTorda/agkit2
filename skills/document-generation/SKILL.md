---
name: document-generation
description: "Generating files people download or receive: spreadsheet exports (CSV, XLSX), PDFs (reports, receipts, invoices, certificates, official forms), and editable Word documents. Covers which format to produce, where generation runs, streaming large exports, and the correctness rules money and official documents require. Use for: export, download, generate report, invoice, receipt, certificate, payslip, printable, print view."
version: 2.3.0
---

# Document Generation

> A file someone downloads is a product surface. It outlives the page that made it: it gets emailed,
> printed, filed, audited, and opened in software you do not control. Bugs in it are permanent.

| File | Read when |
|---|---|
| [spreadsheets.md](./spreadsheets.md) | Any CSV or XLSX export, or data going into Excel |
| [pdf.md](./pdf.md) | Any PDF: report, receipt, invoice, certificate, official form, print view |
| [office-docs.md](./office-docs.md) | The recipient must open it and **edit** it (DOCX) |
| [official-forms.md](./official-forms.md) | The output must match a form an authority publishes (COMELEC, BIR, DepEd, LGU, registrar) |

## 1. Decide three things, in this order

### 1.A Which format

- The recipient will **re-analyse the numbers** (sort, filter, pivot, import) → **CSV or XLSX**.
  Never a PDF table someone has to retype.
- The recipient will **read, print, file, or must not alter it** → **PDF**.
- The recipient must **fill in or edit and return it** (a government submission, a contract) →
  **DOCX from a template**.
- Unsure → **CSV**. It is the smallest, it streams, it never breaks, and every tool opens it.

Asking for "Excel" almost always means "the data, in a thing Excel opens". CSV satisfies that.
Reach for XLSX only when you need multiple sheets, formulas, number or date formatting, frozen
headers, or column widths — reasons that come from the document, not from the word "Excel".

### 1.B Where it runs

- **Server-side** is the default for anything carrying money, personal data, or authority. The
  server already holds the truth and the permissions.
- **Client-side** only when the data is already loaded, already the user's own, small, and carries
  no authority — a table the user is looking at, dumped to CSV.
- **Never client-side** for a receipt, invoice, payslip, certificate, or anything official. A file
  the browser assembles is a file the user can trivially forge before it is sent on.

### 1.C In the request, or as a job

- Bounded rows and under ~2 seconds → generate in the request, stream the response.
- Anything else → **queue a job**, return an id immediately, and deliver by notification plus a
  download link (expiring, authorised on fetch).
- "Bounded" means you counted. A report that is fine on 200 rows is a gateway timeout on 200,000,
  and it always reaches 200,000 in production, not in your test.

## 2. Rules every generated file follows

1. **Authorise the export exactly like the screen.** This is the most common real defect in this
   area: the UI filters to the user's branch, the export endpoint takes `?branch=` and trusts it.
   Re-apply every row-level rule server-side, from the session, not from the query string.
2. **Stream, do not accumulate.** Iterate a cursor or chunk the query and write as you go. Building
   the whole file in memory is what takes the server down on month-end.
3. **Money is never a float.** Integer minor units or decimal all the way through; format once, at
   the edge, with an explicit currency and locale.
4. **State the timezone.** Render dates in the user's zone and print the zone in the header. A
   report whose "today" is UTC is wrong for everyone reading it locally.
5. **Encoding is explicit.** UTF-8 with a BOM for CSV (or Excel mangles `ñ`), and embedded fonts in
   PDF (or `₱` and `ñ` come out as boxes).
6. **The filename carries scope and date**: `sales-2026-09-01_2026-09-07-branch-tuguegarao.csv`.
   `export.csv` in a Downloads folder is worthless a week later.
7. **Financial and official documents are immutable.** Store the rendered file, or a complete
   snapshot of its inputs. Regenerating a January receipt with September's prices and tax rates
   produces a different document with the same number — which is an audit finding, not a bug report.
8. **Never interpolate user data into a cell or a template without escaping it.** A spreadsheet cell
   beginning `=`, `+`, `-`, or `@` executes when opened (`spreadsheets.md`); an unescaped value in an
   HTML-to-PDF template is the same injection you would never allow on a page.

## 3. What this looks like wrong and right

```text
WRONG — the shape most export endpoints start as
  GET /api/reports/sales.xlsx?branch=3&from=2026-01-01
  rows = db.query("... WHERE branch_id = :branch")        # branch from the query string
  wb = new Workbook(); rows.forEach(r => sheet.addRow(r)) # whole result set in memory
  return wb.write()                                       # in the request, 40s, no timeout budget
  → any user reads any branch; the box falls over at month-end; the total is a float sum.

RIGHT
  POST /api/reports/sales            { from, to }         # scope comes from the session, never input
  → authorise(user, "report.sales"), resolve branch from the user, count rows first
  → small: stream CSV in the response
  → large: dispatch a job; return { reportId }; job streams a cursor into the file,
    stores it, and notifies with an expiring, authorised download URL
  → totals summed as integer minor units, formatted once at write time, timezone in the header.
```

## 4. Stack defaults

One line each; the libraries, their traps, and the code live in the sub-files.

- **PHP / Laravel** — `maatwebsite/excel` (`FromQuery` + chunking) for spreadsheets;
  `barryvdh/laravel-dompdf` for simple documents or Browsershot for CSS-heavy ones; `PHPWord` for
  DOCX. Generation belongs in a queued Job, not a controller.
- **Node / TypeScript** — `exceljs` streaming writer (or plain CSV) for spreadsheets; Puppeteer or
  Playwright for HTML-to-PDF, `pdfkit` for programmatic layout; `docxtemplater` for DOCX.
- **Python** — `openpyxl` in `write_only` mode or `xlsxwriter`; WeasyPrint for HTML-to-PDF,
  ReportLab for exact placement; `python-docx` / `docxtpl` for DOCX.

## 5. Done

1. The export re-applies the caller's permissions server-side; it cannot be widened by input.
2. Generation streams or chunks; the row count it was tested at is stated, and a large run was tried.
3. Anything slow runs as a job with a download link, not in the request.
4. Money, dates, and timezone are correct in the file itself, not only on screen.
5. `ñ`, `₱`, and long identifiers with leading zeros survive a round trip through Excel and a PDF
   viewer — opened and checked, not assumed.
6. Official or financial documents are reproducible: the file or its complete inputs are stored.
7. `/see-doc` run: the file was rendered, `doc-verdict.json` says `pass`, and the page images were
   **looked at** — not just produced. A document nobody opened is not verified.
8. The file was opened in the software the recipient actually uses before the task was called done.
