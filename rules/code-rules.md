---
name: code-rules
version: 2.5.0
priority: P0
trigger: always_on
description: Code conventions and risk-tiered verification - which checks to run for which change, fixing at the source, naming, security basics, stack baseline.
---

# Code Rules

## Verification by risk tier
| Tier | Examples | Run | Then |
|---|---|---|---|
| 0 - trivial | copy, a style value, a comment, config value | nothing | report; offer a check in one line if useful |
| 1 - normal | a component, an endpoint, a few files | the project's own lint/type/test for touched files, if they exist and are fast (`python "KIT/scripts/checklist.py" . --quick`) | fix failures you caused |
| 2 - risky | auth, payments, permissions, migrations, data deletion, public API, shared utilities | `checklist.py . --full`; add or update tests for the logic; `/review` on the diff | no "done" with a failing required check |
| 3 - release | deploy, production data | `KIT/scripts/verify_all.py` + the `/deploy` steps | user approval before production |

Visual changes: when a dev server is running and the change affects layout, look at it (`/see`) at one mobile and one desktop width. No server, no browser, or a non-visual change: skip and say so.
Required failures (block done at tier 2-3): security high+, type errors, failing tests. Everything else (lint style, naming, CSS audit, UX/SEO heuristics) is advisory.
The user can always ask for more: `/verify`, `/see`, `/review`, `/test`.

## Fix at the source
Change the thing that owns the behaviour: the container's layout, the token, the function, the query. Overrides move the bug: `!important`, an inline style to win the cascade, a wrapper added only to beat a selector, a margin hack on a child to cover its parent, a `catch` that hides an error. Use them only when the source is outside your control (third-party CSS you cannot configure) and leave a one-line comment saying why. Method: `ui-repair`, `css-architecture`.

## Names
Follow the project's naming. In new code prefer searchable, domain-specific names (`invoice-table.tsx`, `formatInvoiceTotal`, `.invoice-table__row`) over `utils.ts`, `helpers.js`, `styles.css`, `data`, `handleClick2`. `naming_check.py` reports; it does not block.

## Security basics (always)
Validate input at the boundary. Parameterised queries or the ORM. Secrets from environment variables only; never print or commit them. Authorisation checked on the server for every protected action. Escape output.

## Tests
Write or update tests for logic that money, auth, permissions or data integrity depends on, and when the user asks. Otherwise judge: a test that would catch a real regression is worth it; a test of a static component usually is not.

## Stack baseline (September 2026, use when the project has no preference)
Next.js 16 · React 19.2 (React Compiler aware) · TypeScript 5.9+ · Tailwind v4 · Node 24 LTS, Hono for standalone APIs · Python 3.13 + Ruff · PHP 8.4 / Laravel 12 + Pest · Postgres 17/18 · Prisma 7 / Drizzle / Eloquent · Expo SDK 54+. The project's existing stack always wins.
