# Editable Word documents

Produce DOCX when requested or when the recipient needs an editable prose artifact, template workflow, comments or tracked changes. PDF can be an additional reading/print copy when useful; do not replace the requested Word file without agreement.

## Use the right source

If a supplied template controls the layout, preserve its structure, styles, headers/footers, fields, numbering and content controls. For a new document, build a suitable structure with named paragraph/character/table styles rather than direct-formatting every run. Both template filling and programmatic authoring are valid; choose from fidelity, repeatability and editing needs.

For a new visual design complete the shared style/reference intake before inventing the look. An established approved template does not need a duplicate questionnaire. Use real content to test headings, lists, tables and pagination.

## Library boundaries and traps

Choose an available supported tool: template engines and document-object libraries have different strengths. Verify the installed library's escaping and text/run handling rather than double-escaping XML blindly. User data containing `&`, `<`, line breaks or non-ASCII names should remain text without corrupting the package.

Word may split a visible placeholder across multiple XML runs. Test actual templates, repeated sections and optional content; use the engine's supported mechanism or inspect the document structure when a replacement fails. Do not use naive ZIP-wide search/replace that can corrupt relationships or formatting.

Use supported paragraph/line-break and table APIs. Keep image aspect ratio and explicit dimensions where needed, preserve alt text for meaningful images, and maintain sensible heading and table semantics. Field codes, page numbers, references and the table of contents may require an actual office application update; distinguish an inserted field from a verified updated result.

## Editing quality

Make the final document comfortable to maintain. Use coherent margins, section breaks, page numbering, widow/orphan and keep-with-next controls where useful. Test long titles, large tables, empty optional fields and multiple pages. Avoid forcing pagination with blank paragraphs or placing the whole report inside one giant table.

Check font availability/embedding permissions and realistic fallback; no font is installed everywhere. A LibreOffice render, Microsoft Word render and browser preview may paginate differently. DOCX-to-PDF conversion is a useful verification/delivery path but its result should be inspected, especially when a template requires exact placement.

## Verify and deliver

Open/parse the final DOCX, confirm required content, absence of unresolved placeholders and appropriate styles. Render pages with available office/document tools and inspect actual layout. Check repeated tables and fields as relevant. Do not claim that Word opened without a repair prompt unless Word was actually used.

The compatible document helper can collect structural/render results, with limited automated scope and reported artifact paths. Review its outcome and actual page images; missing rendering is an unverified part, not a visual pass. Deliver the editable file plus an optional verified PDF if requested, and state the tools and compatibility limits actually observed.
