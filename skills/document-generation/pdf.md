# PDF and print output

Choose a pipeline from the document's behavior, not a favorite package. Existing HTML/CSS can suit flowing reports; a programmatic layout engine can suit precise positioning; filling or overlaying an actual PDF can preserve an official template. Inspect the selected library/renderer and supported version rather than assuming all CSS print engines behave alike.

## Layout and pagination

Set page size, orientation and margins from the brief/template/recipient, not the user's country alone. Letter, A4, US Legal and 8.5-by-13-inch Folio are different sizes. Inspect PDF page boxes and rotation when exact alignment matters.

Use real content and test first, middle and last pages. Check running headers/footers, page numbering, long tables, row breaks, headings at page ends, signature blocks, oversized images and blank trailing pages. A `break-inside: avoid` rule cannot keep an object larger than a page intact; the layout needs a real overflow/splitting policy.

For HTML printing, useful concepts include `@page`, print-only visibility, repeated table headings and deliberate break rules. Browser and paged-media support varies by version. Verify current behavior of margin boxes, counters and header/footer templates in the actual renderer instead of assuming a historical limitation is still true. Do not globally append every URL if it damages the document; link annotations and print references serve different needs.

## Fonts and content

Package or embed suitable licensed fonts when supported. Check glyph coverage and extraction/search for actual names, languages and symbols. A system font available locally may be absent in a container. Font embedding does not itself ensure accessible reading order or tags.

Use semantic source structure and a tagging-capable pipeline when accessible PDF is required. Inspect reading order and relevant assistive-technology behavior. A scanned page is not a searchable or fully accessible text document merely because it looks correct. Avoid claiming accessibility compliance from an extraction test alone.

## Reliable generation

Wait for actual content readiness, fonts, charts and required images; a fixed sleep or global network-idle condition may be unreliable when analytics/polling continue. Bound work and concurrency based on the environment. A small local generation task need not have a queue; a large production workload may need pooling/jobs and resource limits.

Treat HTML/templates and render URLs as a security boundary. Escape untrusted values, restrict remote fetches/paths and do not render arbitrary user URLs with privileged network/file access. Keep authentication and temporary-file handling scoped; do not disable the browser sandbox merely to avoid diagnosing setup.

## Issued records

For financial or official records, implement required issuance, unique identifiers, audit history, void/reprint behavior and versioned inputs according to the actual business/current requirements. A sequence or unique constraint can prevent concurrent duplicate IDs; a row count is not a safe issuance strategy. Server rendering alone provides no digital signature or tamper-proof guarantee.

Verification URLs or QR codes can be useful when authorized and implemented, but avoid exposing sensitive data in a public verification page. Preserve the rendered record or reproducible inputs/rules where required. Do not invent universal tax, retention, amount-in-words or numbering rules.

## Inspect the actual PDF

Parse the final file and render its real pages. Inspect layout, clipping, glyphs, full critical values, image quality, table continuation and page count. Compare to a supplied reference when exact matching is required. A print preview is useful; real-printer alignment is a separate check and should only be claimed when performed.

`KIT/scripts/doc_verify.py` can gather supported structural/render evidence. Read its reported artifact locations and outcome. Its automated scope is limited; `INCOMPLETE` means some required checks could not finish, and a successful helper invocation is not human visual approval. Review produced images yourself and state the actual viewer/render path and any unverified requirements.
