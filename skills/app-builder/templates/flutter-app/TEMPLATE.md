# Flutter mobile product

## Fit and inspection

Use when Flutter is selected or existing. Inspect SDK constraints, package lock, platform configuration, build variants and target devices.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Compose reusable widgets and platform-aware behavior around the accepted brand. Respect MediaQuery, SafeArea, keyboard insets, text scaling and semantics.

- Choose state and persistence according to ownership, offline needs and team conventions; Riverpod, Bloc, Provider, Drift or another package is not mandatory.

- Keep async work, subscriptions and widget lifecycles safe. Use lazy lists for genuinely large/variable datasets and profile measured rebuild or rendering concerns.

For new visual design, complete the shared short style/reference intake and wait unless already answered or delegated. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Run relevant analyze/test/build checks, inspect a simulator/emulator or device, and exercise the changed flow, back behavior, text scaling and relevant failure states.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
