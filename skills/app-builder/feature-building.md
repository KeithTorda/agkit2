# Feature Building

Adding a feature to an existing project (`/enhance`).

## Analysis

```
Request: "add payment system"

Required changes:
  Database: orders, payments tables
  Backend:  checkout action, /api/webhooks/stripe
  Frontend: CheckoutForm, PaymentSuccess
  Config:   Stripe keys in .env.example
Dependencies: stripe package; existing authentication
Scope: DB + 2 routes + 2 components + config, touches money → multi-file, tier 2
```

## Process

1. Read the existing architecture: the modules the change touches, `DESIGN.md`, `docs/plans/`, `.agents/memory/MEMORY.md`.
2. Size it (`core-protocol`): obvious change → do it; a few files → 3-6 line plan in the reply; big → `docs/plans/<slug>.md` (`plan-writing`).
3. UI follows `DESIGN.md`. Missing: new page-level UI → write a short one (`design-spec`); a component change → match existing styles and say so.
4. Apply with the owning specialist(s); update importers and callers in the same task.
5. Verify by tier (`code-rules`); when a dev server is running and layout changed, look at it.

## Error handling

| Error | Strategy |
|---|---|
| TypeScript error | Fix the type or add the missing import; no `any` or `@ts-ignore` to silence it |
| Missing dependency | Install it with the project's package manager |
| Port conflict | Use the next free port and say which |
| Database error | Check migration state and the connection string |

Recovery: detect → attempt the fix → if it fails, report the exact error and offer an alternative → roll back only when the change left the project broken.
