# Workspace with Turborepo orchestration

## Fit and inspection

Use when multiple packages/deployables justify a workspace and Turborepo is selected. Do not create a monorepo for a small single app solely to match this template.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Define package ownership, explicit exports, dependency direction and task graph. Preserve the chosen workspace package manager and lockfile strategy.

- Cache only reproducible tasks with complete inputs/environment dependencies. Avoid caching private artifacts or assuming a cached command means the local app actually ran.

- Share code or tokens where a stable contract helps; avoid coupling every app to one giant common package. Each deployable keeps its own runtime and secret boundary.

New visual design follows `rule-01-unified-theme-system`; ask about style only if genuinely unclear. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Run affected package tasks and relevant cross-package checks, verify clean builds and cache invalidation where changed, and exercise the actual deployable rather than only its workspace command.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
