# Feature Building

> Adding a feature to an existing project (`/enhance`).

## Analysis

```
Request: "add payment system"

Required changes:
  Database: orders, payments tables
  Backend:  /api/checkout, /api/webhooks/stripe (or server actions)
  Frontend: CheckoutForm, PaymentSuccess
  Config:   Stripe keys in .env.example
Dependencies: stripe package; existing authentication
Scope: DB + 2 routes + 2 components + config → multi-file → plan file
```

## Process

1. Read the existing architecture: `docs/plans/*.md`, `DESIGN.md`, the modules the change touches, project memory if loaded.
2. Scope per the plan-file rule (global `core-protocol`): multi-file or structural → `docs/plans/{task-slug}.md` in the `@[skills/plan-writing]` format; simple → a 1–3 line plan in the response.
3. UI added or changed → align with `DESIGN.md` (global `design-rules` gate). If it is missing: new page-level UI → create `DESIGN.md` first (`@[skills/design-spec]`, by `frontend-specialist` or, for a mobile-only app, `mobile-developer`); component-level change → infer from existing styles, say so, offer to create it; bug fixes and trivial tweaks skip the gate.
4. Apply with the owning specialist(s); edit dependents in the same task (`@[skills/clean-code]`).
5. Verify: affected tests, `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .`, then confirm in the running dev server (hot reload) when one is up.

## Error handling

| Error | Strategy |
|---|---|
| TypeScript error | Fix the type or add the missing import |
| Missing dependency | Install it with the project's package manager |
| Port conflict | Suggest an alternative port |
| Database error | Check migration state and the connection string |

Recovery: detect → attempt the fix → if it fails, report the exact error and offer an alternative → roll back only when the change left the project broken.
