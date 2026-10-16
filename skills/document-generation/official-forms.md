# Fill or reproduce an authoritative form

An authoritative template supplies the layout. Preserve the actual approved form instead of applying a new visual direction. This workflow is template maintenance, so it does not need a new style question unless the user is designing a separate companion document.

## Establish the source and role

Obtain the actual authority's file or the supplied template, confirm its relevant revision, and record source/date/revision when useful. Forms and legal requirements change; verify the applicable current source rather than inventing an agency template from memory. Do not fabricate sample government records or official signatures.

Use an existing fillable PDF, DOCX/XLSX template or clean source PDF when available. A scan can be a reconstruction reference; a photograph may introduce distortion that requires correction before accurate measurement. Preserve the source and write output separately.

## Choose the least destructive method

1. Inspect PDF fields, annotations, page boxes, rotation and appearance streams. For a usable AcroForm, fill through supported field APIs and verify displayed values in relevant viewers.
2. If the form is nonfillable, overlay values on a preserved background when that suits the form and recipient. Overlay can still misalign because of page boxes, rotation, scaling and font metrics; it is not a zero-drift guarantee.
3. Fill a supplied editable template using its supported data-binding approach.
4. Reconstruct only when necessary and explain the limitation. A variable-length supplement may be more appropriate than changing an official fixed form.

Preserve editability when the recipient must continue filling it. If the workflow requires flattening, use a real flattening process and verify appearance; setting a read-only flag is not equivalent. Flattening is not cryptographic authenticity and can remove useful form semantics. Do not claim that an issued file is tamper-proof without an actual implemented verification/signature mechanism.

## Coordinates and field policies

PDF user units are commonly points, with page boxes/rotation affecting coordinates; many extraction APIs report top-origin positions. Check the actual library conventions. For a simple unrotated page, `points = millimeters * 72 / 25.4` and `y_from_bottom = page_height - y_from_top` can help, but baseline and text height still need inspection.

Use a named mapping of fields to coordinates/constraints, tied to the source revision. Anchoring to extracted labels can help but should fail visibly if labels move, duplicate or disappear. Never silently guess a new template revision.

Define legitimate handling for long names/addresses, multiline values, empty fields, checkboxes, dates and identifiers. Do not truncate essential legal identity without the actual form rule. A smaller font may fit a field but must remain legible. Keep signatures, seals and issuance fields empty unless the user has authorized valid content for them.

## Compare the actual result

Read page size from the source, not an assumed local convention; US Legal and 8.5-by-13-inch Folio differ. Render the filled output and blank reference through a consistent pipeline and inspect values, checkbox placement, text baseline, margins and the full page set. Differences should reflect intentional additions; anti-aliasing and rendering changes can add noise, so a diff alone is not proof.

The optional helper accepts supported flags such as `--reference`, `--outdir`, `--page-size` and `--glyphs`; inspect `--help` and use the actual intended size/characters. It now reports unique artifact paths rather than guaranteeing fixed image names at the output root. Read the outcome and automated scope; `INCOMPLETE` or unavailable rendering/reference comparison must be reported. Inspect rendered pages and any diff images yourself.

Test representative awkward values and required field behavior. Claim physical printer alignment only after a real print check. Report source revision, method, actual verification and any recipient/printer validation still outstanding; never guarantee acceptance by an authority from a source-code check.
