---
name: code-rules
version: 2.0.0
priority: P0
trigger: always_on
description: Apply when writing, building, refactoring, fixing, or verifying code — the four phases, the verification gates (required vs advisory checks), and the auto-fix policy. Skip for pure questions and text-only answers.
---

# Code Rules

## Phases (the only definition)
1. **ANALYZE** — read the relevant code, dependents, `DESIGN.md`, and memory; ask questions per `core-protocol` if the answer changes the build.
2. **PLAN** — for COMPLEX / NEW APP write `docs/plans/{task-slug}.md` (`plan-writing` skill; Antigravity Planning Mode is this phase). Simple tasks: 1–3 lines in the response.
3. **BUILD** — implement per the plan and the agent's skills; tests for logic changes; keep diffs focused.
4. **VERIFY** — run the gate below and fix required failures before reporting done. Report evidence (`verify-changes` skill), not claims.

## Verification gates
- Fast (every task): `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .`
- Release / before deploy: `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/verify_all.py . --url http://localhost:3000`
- Kit self-check (after editing the kit itself): `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/validate_kit.py`

**Required** (block "done"): security scan at high+, lint, type check, tests — detected per stack (npm/vitest/jest, pytest, `php artisan test`/Pest/PHPUnit; Pint + Larastan for PHP; ruff/mypy for Python; a missing tool is a note, not a failure). **Advisory** (reported only): UX audit, accessibility heuristics, SEO/GEO, schema heuristics, bundle, mobile, API, i18n, Lighthouse, Playwright smoke. "No tests configured" passes with a warning — logic changes still need tests.

## UI-render gate (required — the only definition)
A change that affects rendered UI is not done until it has been **seen in the browser**. Run the
`browser-verification` skill (`/see`) and report its Visual Verification Report: rendered output,
computed styles vs `DESIGN.md` tokens, console and network errors, one interaction pass, and the
breakpoint matrix. Reading the source is not verification of a render.

Required failures from this gate: the route does not render, an uncaught console error, a failed
request for the route's own data, or an interaction that does not work. Token violations, spacing
rhythm, and polish are advisory.

**Escape hatch** — skip the gate when there is no dev server, no browser is available, or the change
is non-visual (logic, config, build, docs). Skipping is allowed; skipping silently is not: state
which reason applied in one line under "Not verified".

## Fix at the source (required)
A fix changes the thing that is wrong: the container's constraint, the token, the rule that owns the
behaviour. An **override is not a fix**: `!important`, an inline layout style, a wrapper element added
to win the cascade, a more specific selector, a margin or `absolute` hack on a child to compensate for
its parent, a `catch` that hides the error, a platform `if` around a layout cause. Each of these moves
the bug and breaks the next change. When you replace CSS or code, delete what you replaced. Method for
UI: `ui-repair` (`/fix-ui`); organisation: `css-architecture`. For CSS this is checked rather than trusted: `scripts/css_audit.py` (required in `checklist.py`) fails on `!important` and inline colours, on a `var()` nothing defines, and on one token defined twice with different values outside a theme selector — the usual reason a text colour changes on its own.

## Unique, searchable names (required)
Files are `<domain>-<role>.<ext>` (`invoice-table.tsx`, `invoice-table.css`), never bare
`utils.ts`, `helpers.ts`, `styles.css`, `types.ts`, or a second `index.*` outside route conventions;
no two files in a repo share a basename. Exported symbols are domain-prefixed and intention-revealing
(`formatInvoiceTotal`, not `format`); CSS classes and custom properties are component-prefixed
(`.invoice-table__row`, `--invoice-table-gap`); tokens are namespaced (`--color-*`, `--space-*`).
Check: `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/naming_check.py .` (runs
inside `checklist.py`). Detail and the banned-generic list: `clean-code`.

## Auto-fix policy
Failures of required checks (security high+, lint, type errors, failing tests) are fixed automatically. Advisory findings (UX, SEO, GEO, mobile, API heuristics) are reported; ask before making changes they suggest that touch design or scope — **except an agent's own un-reviewed UI in the same task**, which it critiques and refines without asking (`browser-verification` §2b). Asking permission to improve your own first draft is not caution; it is shipping the draft.

## Individual scripts
Each skill's scripts are listed in its `SKILL.md` and run as `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/<skill>/scripts/<script>.py <project>`. The catalog is in `quick-reference`.

## Baseline (September 2026)
Next.js 16 · React 19.2, compiler-first when the React Compiler is enabled (check the flag before removing manual memo) · TypeScript 5.9+ · Tailwind v4 · `motion/react` · Node 24 LTS, Hono for standalone APIs (Express only in existing code) · ESLint 9 flat config · Python 3.13+ with Ruff · PHP 8.4 / Laravel 12 with Pest, Pint, Larastan · Postgres 17/18 · Prisma 7 / Drizzle / Eloquent · UUIDv7 · Expo SDK 54+ / Reanimated 4 · OWASP Top 10:2025. Details live in the skills.
