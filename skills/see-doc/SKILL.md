---
name: see-doc
description: "Render and inspect generated PDF output for layout, text, page size and relevant template fidelity. Use /see-doc when document appearance or print/export behavior changes."
version: 2.8.2
---

# /see-doc

Use `KIT/skills/document-generation/SKILL.md` and the matching format guidance. Input is the generated file and, when applicable, its official/reference blank. Source inspection alone does not verify the delivered document.

Generate representative synthetic data that covers relevant long text, optional fields, amounts, glyphs and pagination without copying real personal records. For a PDF, use the actual expected paper size and glyphs:

```powershell
python "KIT/scripts/doc_verify.py" <file.pdf> --outdir .agents/verify/<task-slug> --page-size a4 --glyphs "₱,ñ"
```

Add `--reference <blank-form.pdf>` when the workflow requires template fidelity. The checker's available renderers and dependencies determine what evidence it can produce; inspect its outcome rather than assuming a pass.

Open the rendered pages. Look for clipping, overlap, unreadable type, broken glyphs, table/header continuation, awkward page breaks and signature/content placement. For long documents inspect all pages or explain the sampled scope and why; do not claim every page was reviewed if it was not. Inspect relevant diff images against an official form and distinguish intended value additions from moved/redrawn template content.

Preserve official form geometry and use the issuing authority's documented fit rules when applicable; do not silently truncate meaningful text. Interpret font/edge/text-extraction warnings in context, including intentionally scanned/artwork output. Fix actual defects within scope and render again.

Report the file, page count/size, pages inspected, mechanical outcomes, observed layout and remaining limits. Physical printer behavior stays unverified until tested on the intended printer/paper when that matters.
