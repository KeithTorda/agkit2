---
name: see-doc
description: "/see-doc — Renders a generated PDF and reports what actually came out: page images to look at, page size, embedded fonts, glyph survival, content near the edge, and a difference image against an official blank form. Use before calling any generated document done, and whenever output must match a government template."
version: 2.3.0
---

# /see-doc

The document equivalent of `/see`. Reading the template tells you what you wrote; only rendering the
file tells you what the recipient receives. A generated document that was never opened is not
verified.

**Input:** the text after `/see-doc` is the path to the generated file, optionally followed by the
blank official form to compare against (`/see-doc out/coe.pdf resources/forms/coe-rev2026.pdf`). If
empty, use the file produced by the most recent change; if that is unclear, ask for the path in one
line.
**Agent:** `backend-specialist` owns generation; read
`C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/backend-specialist.md`.
**Skills:** `@[skills/document-generation]` (core + `pdf.md`; `official-forms.md` when a template is
involved).

## Steps

1. **Generate with real data.** Not a fixture with "Test Test" — the longest name in the database, a
   name containing `ñ`, an amount over a million, and one empty optional field. Most document bugs
   only appear at the awkward values.
2. **Run the checker.**
   ```bash
   python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/doc_verify.py <file.pdf> \
     --outdir .agents/verify/<task-slug> --page-size <a4|letter|legal|folio> --glyphs "₱,ñ" \
     [--reference <blank-form.pdf>]
   ```
3. **Look at the rendered pages.** Open every `page-*.png` it wrote. State what you actually see,
   per page — not what the template was supposed to produce.
4. **Look at the diff** (when `--reference` was given). It shows only what you drew on top of the
   authority's form. Your values should be there, in their boxes, and nothing else. Form elements
   appearing in the diff mean you moved or redrew something that was theirs.
5. **Check the pagination story.** Page 2 onward: do table headers repeat, did a signature block or
   a row split across the break, is there an orphan heading, is the page count bounded.
6. **Report**, splitting required failures from advisory findings.

## Output

```markdown
## Document Verification Report
### Target
- File: <path> · <n> pages · <size>mm · reference: <blank form or none>
### Rendered
- <what you saw, per page>
### Checks
- Page size: <pass/fail> · Fonts embedded: <pass/fail> · Text extractable: <pass/fail>
- Glyphs (₱, ñ): <pass/fail> · Content near edge: <count>
### Template match
- <changed-pixel ratio per page, and what the diff image shows — or "no reference">
### Findings
- Required: <wrong page size, missing glyphs, unembedded font, clipped content, misaligned values>
- Advisory: <spacing, polish, non-blocking>
### Not verified
- <what needs a human eye or a real printer>
```

## Rules

- **Looking at the images is the point.** The verdict JSON catches what is mechanical; alignment,
  overflow into the next box, and a value one line too low are only caught by opening the PNG.
- A required failure blocks done: wrong page size, a non-standard font not embedded, `₱` or `ñ`
  absent from the extracted text, no extractable text at all, or content inside the non-printable
  edge.
- Never "improve" an official form to make a value fit — shrink or truncate the value by the
  agency's rule instead (`official-forms.md` §4).
- If the checker cannot run (no `pypdfium2` and no poppler), say so in one line and name it as the
  escape-hatch reason. Never report a document as verified on the strength of the source template.
- For a document that will be printed at a counter, one physical print on the real paper is still
  owed; list it under "Not verified" until it has happened.

## Verification

- `.agents/verify/<task-slug>/doc-verdict.json` exists, and its `status` is `pass` or the failures
  are reported as required findings.
- The report names the exact file, its page count and page size.
- Every rendered page was opened and described; when a reference was given, the diff was read.
