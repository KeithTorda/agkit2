---
name: rule-03-code-standards
version: 3.0.0
priority: P0
trigger: glob
globs: "**/*.ts, **/*.tsx, **/*.js, **/*.jsx, **/*.mjs, **/*.vue, **/*.svelte, **/*.php, **/*.py, **/*.css, **/*.scss, **/*.html, **/*.blade.php, **/*.dart, **/*.sql"
description: Rule 03 - clean, organized, maintainable code in any stack. Existing stack first, domain names, no CSS override hacks, complete states, no dead code.
---

# RULE 03 — CODE STANDARDS

## Respect the project

1. Read before writing: the files you will touch, their neighbors, `package.json` / `composer.json` / lockfiles, and any `README`, `DESIGN.md`, `AGENTS.md` or `docs/` notes.
2. Use the stack, libraries, folder structure and patterns already in the project. Do not switch frameworks, CSS systems, ORMs or state libraries unless the user asks.
3. Add a new dependency only for a concrete need the project cannot already cover. Check the installed version's real API before using it.
4. Match the existing formatting and lint config.

## Naming

- Names describe the domain: `posReceiptTotal`, `fetchBranchInventory`, `PayrollPeriodCard` — not `data`, `temp`, `handleClick2`, `utils2`.
- One name per concept across the codebase. If the database says `branch`, the UI does not say `store`.
- Files are named after what they export. No `new-`, `final-`, `copy-` prefixes.
- Booleans read as questions: `isPaid`, `hasStock`, `canVoid`.

## Structure

- One component, function or class does one job. Split when a file mixes unrelated responsibilities, not to hit a line count.
- Shared UI goes in the shared components folder; shared logic goes in the shared lib/services folder. Do not copy-paste the same block into three files.
- Keep business rules out of UI components. Totals, permissions and status transitions live in services/actions/server code.
- Put types/interfaces next to the code that owns them, or in the project's established types folder.

## CSS and styling

- Fix the rule or token that owns the problem. Do not stack overrides on overrides.
- No `!important` unless overriding third-party CSS you cannot change, and then with a one-line comment saying why.
- No inline `style=` for layout fixes. Inline style is allowed only for truly dynamic values (computed width, user-chosen color).
- Colors, spacing, radius, shadows and fonts come from tokens (`rule-01-unified-theme-system`).
- Remove the old CSS you replaced.

## Every data screen handles all states

Loading, empty, error, success — and for forms: validation errors, submitting, disabled. A screen that only handles the happy path is not finished.

## Errors

- Handle errors where you can do something useful; otherwise let them reach the shared error handler.
- Never swallow an error silently (`catch {}`), never `console.log` and continue as if it worked.
- User-facing error messages say what happened and what to do next. Internal details stay in logs.

## Cleanliness

- Delete code you replaced. No commented-out blocks, no unused imports, no leftover `console.log` / `dd()` / `print` debugging.
- Comments explain why, not what. Remove comments that restate the code.
- No magic numbers for business values (VAT rate, max discount, session timeout); use a named constant or config.
