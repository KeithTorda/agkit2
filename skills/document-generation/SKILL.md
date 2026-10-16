---
name: document-generation
description: "Create and integrate useful PDF, DOCX, CSV and XLSX output, from one-off files to application exports. Match requested format and templates, preserve data accuracy and authorization, then inspect actual content and layout in the appropriate viewer."
version: 2.8.2
---

# Documents and exports

Treat a document as a usable deliverable. Identify who reads or edits it, the requested format, content source, template, page or sheet structure, locale, and delivery path. A single generated report and a production export endpoint need different engineering.

## Match the requested artifact

Honor an explicit format: “Excel” may mean an actual `.xlsx` workbook, and a request for editable Word should produce `.docx`. Do not silently substitute CSV for a workbook or a PDF image for editable text. If the request is open, use PDF for stable reading/printing, DOCX for editable prose, XLSX for structured worksheets/formulas, and CSV for a simple interoperable data table.

For every new visual document design, ask one short style-and-reference question and wait unless already answered or delegated. A supplied template can answer the reference part; ask only for a remaining material style choice. Maintenance within an approved template follows it without repeat intake. Do not recreate an authority's form from memory.

| Output | Read |
|---|---|
| CSV, XLSX and application data exports | [spreadsheets.md](spreadsheets.md) |
| PDF, print layouts, receipts and certificates | [pdf.md](pdf.md) |
| Editable Word documents | [office-docs.md](office-docs.md) |
| Exact official templates and fillable forms | [official-forms.md](official-forms.md) |

## Preserve meaning and correctness

Use supplied or authoritative data and truthful wording. Keep identifiers with leading zeros as text, exact money as a domain-appropriate decimal or minor-unit representation, and formulas distinct from displayed values. Distinguish date-only values from instants; use the intended locale and time zone where interpretation matters. Include currency, units, period, source or generation date when useful to the recipient.

Choose fonts that cover the content and embed them when the format/pipeline supports it. Check language-specific characters, names and symbols such as `ñ` and `₱` when present. Escape untrusted template content and mitigate spreadsheet formula injection for untrusted text fields without destroying legitimate typed numeric cells or requested formulas.

## For an application export

Authorize generation and download at the real data boundary; input may select permitted scope but cannot grant access. Preserve tenant and row restrictions, protect stored files, sanitize filenames and avoid sensitive data in public URLs or logs. A signed expiring link is a bearer capability; choose revocation/access behavior appropriate to the product.

Choose client or server generation from trust, data location, volume and reproducibility. Server-issued financial or official records require authoritative server inputs and identifiers; server rendering alone does not make them tamper-proof. Offline or local document creation can be valid when its role is explicit. A browser-generated convenience copy must not masquerade as an authoritative issued record.

Bound work and memory. Small exports can be generated directly; large or expensive jobs may need chunking, streaming, cancellation, queueing, retention, and retry behavior. Estimate and measure the relevant dataset rather than imposing a universal time threshold or always counting a huge query first.

For issued records, preserve the rendered file or sufficient immutable inputs/versioned rules to reproduce it when the product requires an audit trail. Taxes, fields, numbering and retention depend on current applicable requirements; verify those rather than inventing compliance.

## Verify the deliverable

Open or parse the final file to confirm format, content, row/page counts, formulas, totals, dates and identifiers. Render page-oriented output and inspect actual pages, including long content, tables, headers, page breaks and the last page. For workbooks inspect relevant sheets, formulas and cached/recalculated values with compatible tooling; test a round trip when the receiving software matters.

Use available document-specific tools and project checks. `python "KIT/scripts/doc_verify.py" <file>` may help gather evidence for supported formats; inspect its actual output and rendered pages. A generated verdict is not a substitute for visual review or numeric validation. State which viewer/render pipeline was used and any compatibility, recalculation or printing limits.

Deliver the actual artifact or implemented export with a meaningful filename, verification result and any remaining setup. Never promise a perfect layout, legal compliance, formula correctness or error-free behavior from a successful save alone.
