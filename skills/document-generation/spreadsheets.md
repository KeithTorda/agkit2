# Spreadsheet files and tabular exports

Honor a requested XLSX workbook. Use CSV when a simple interoperable table is the actual requirement, or offer it when format is open. CSV cannot preserve cell types, sheets, formulas, styling or date formats, and spreadsheet applications may reinterpret its contents. XLSX is appropriate when those capabilities or reliable identifier typing matter.

## Model cells by meaning

| Data | Representation and check |
|---|---|
| Identifier, phone, account or long digit string | Text cell; preserve leading zeros and full digits. Quoting CSV does not reliably prevent numeric conversion. |
| Money | Exact source calculation with explicit currency/precision; numeric spreadsheet cells plus a suitable display format when analysis is intended. |
| Date-only value | Preserve the intended calendar date and a clear format; do not route through a timezone conversion. |
| Instant or local schedule | State the relevant zone and represent it deliberately; an XLSX date serial has no inherent timezone. |
| Formula | A real formula only when requested/needed, distinguished from untrusted literal text. Check its references and recalculated result. |
| Untrusted description | Safe literal string handling; prevent formula execution without deleting meaningful content. |

Do not use `="..."` as a universal identifier workaround: it creates a formula. For untrusted text, use explicit string cell APIs in XLSX where possible and verify that the chosen library does not infer formula type. For CSV, escape syntax through a real CSV writer and use an injection mitigation appropriate to the receiving application, considering leading whitespace/control characters. A leading apostrophe can alter exported data and is not a universal round-trip guarantee. Typed negative numbers are not malicious text; avoid blanket sanitizing numeric cells. Do not include an executable exploit in ordinary sample data.

## Encoding and interoperability

Use UTF-8 explicitly. A BOM may improve automatic opening in some Excel workflows, while other import tools prefer BOM-free CSV; choose from the actual receiving path. Delimiter, decimal separator and quoting need the recipient's/import contract. Test quotes, commas, line breaks, accented names and symbols when present.

For XLSX, use supported number/text formats and appropriate date handling. Preserve formulas and styles during edits unless requested otherwise. Some libraries write formulas without calculating cached values; Excel, LibreOffice, Sheets and preview tools may display them differently until recalculated. State that limit rather than claiming computed results were checked.

## Useful workbook structure

Use descriptive sheet names, readable headers and units. Add filters, freeze panes, widths, tables or conditional formatting when they help the actual task; no mandatory decorative dashboard. Scope, period and provenance should travel with a report when needed. Avoid merging cells in a data range that must sort/filter.

Choose totals from intended behavior. `SUM` includes hidden/filtered rows; `SUBTOTAL`/an appropriate equivalent may suit visible-row totals. A stored authoritative total can serve a different purpose. Verify totals against the same source population and exact arithmetic, not a visually plausible number.

## Volume and authorization

Application exports reapply the caller's permitted tenant/row scope at generation and download. A requested branch/filter can be valid input after authorization; it must not grant access. For large data use bounded queries, cursors/chunking, a suitable streaming/write-only writer or a background job when needed. Streaming an output file is not enough if the database first materializes every record in memory.

Respect response backpressure and cancellation in live streaming. A partially written file and a completed artifact have different lifecycle states. Choose filenames/headers safely, protect retained files and clean them under the actual retention policy.

## Verify

Parse/open the final file, confirm row counts and scope, inspect representative sheets/cells, and validate identifiers, formulas, totals, dates and strings. Test realistic data volume when scaling is part of the feature. Where receiving software matters, open/recalculate there or state the compatible tooling actually used. A successful save and a valid ZIP do not prove workbook correctness.
