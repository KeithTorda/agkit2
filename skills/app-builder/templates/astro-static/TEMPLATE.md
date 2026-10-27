# Astro content or static site

## Fit and inspection

Use when the selected foundation is Astro and most content can be rendered ahead of time or through its supported server mode. Check content sources, update workflow, hosting and whether any interactive islands or server routes are needed.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Use conventional pages, layouts and content collections supported by the installed release. Keep a clear content schema and meaningful metadata.

- Hydrate islands only where interaction needs them. A contact form still needs a real submission destination and failure/success behavior.

- Choose static export or the required hosting adapter deliberately; do not promise every server feature works on arbitrary static hosting.

New visual design follows `rule-01-unified-theme-system`; ask about style only if genuinely unclear. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Build the selected output, inspect representative routes and content entries, test navigation/assets, and verify forms through their actual endpoint when implemented.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
