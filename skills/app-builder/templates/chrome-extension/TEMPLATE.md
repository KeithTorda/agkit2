# Browser extension

## Fit and inspection

Use for the selected supported browser extension target. Inspect manifest version, permission model, target browser APIs and store/distribution constraints.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Separate service worker/background lifecycle, content scripts and extension pages; persist state where worker suspension requires it.

- Request narrowly justified permissions and host access. Validate message senders/payloads and avoid exposing privileged actions to arbitrary pages.

- Honor the browser security policy; do not depend on remote executable code or unsafe evaluation to make a demo work. Verify current APIs before introducing version-specific behavior.

New visual design follows `rule-01-unified-theme-system`; ask about style only if genuinely unclear. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Load the extension in the target browser when available, exercise installation/reload, allowed-page behavior and denied/missing permission paths. Distinguish local testing from store submission.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
