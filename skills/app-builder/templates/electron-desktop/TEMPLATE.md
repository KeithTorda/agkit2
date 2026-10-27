# Electron desktop product

## Fit and inspection

Use when Electron is chosen for desktop delivery and its resource/distribution tradeoffs fit. An existing native or other desktop stack need not migrate.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Keep the renderer isolated from privileged Node APIs. Expose a narrow validated preload/IPC contract and authorize privileged operations.

- Use supported secure window defaults and deliberate navigation/link handling. Do not disable sandbox/context isolation to work around an unexplained integration problem.

- Define file locations, persistence, window state, update/signing/distribution and offline needs from the actual product. A website preview does not establish packaged behavior.

New visual design follows `rule-01-unified-theme-system`; ask about style only if genuinely unclear. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Run the app and relevant IPC/security boundaries, test file paths and persistence, and validate a packaged target when available. Report signing or platform-specific packaging not performed.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
