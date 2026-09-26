---
name: clean-code
description: Pragmatic coding conventions - follow the project first, readable names, small focused functions, no speculative abstraction, update every dependent, and how to simplify existing code safely. Use when writing, editing, refactoring or simplifying code, or when reviewing code for readability.
version: 2.5.0
---

# Clean Code

Working code that the next person can read and change. These are conventions, not gates: the project's existing style wins, and nothing here blocks "done" on its own. Firm items are marked; they are about correctness, not taste.

## Principles

| Principle | In practice |
|---|---|
| Single responsibility | If describing a function needs "and", consider splitting it |
| DRY, later | Duplicate twice; extract on the third use, once the shape has stopped changing |
| KISS | The simplest solution that fully solves the problem |
| YAGNI | Do not build what nothing uses yet |
| Leave it better | Tidy what you touch, within the task's scope; no drive-by rewrites |

## Names (convention)

Follow the project's naming first: its casing, file layout and vocabulary. In new code, prefer names that say what the thing is in the domain and that someone can find with a search:

| Element | Prefer | Over |
|---|---|---|
| Variables | `pendingOrderCount` | `n`, `data`, `temp` |
| Functions | `formatInvoiceTotal()`, `getUserById()` (verb + noun) | `process()`, `handle()`, `doStuff()` |
| Booleans | `isActive`, `hasPermission`, `canEdit` | `active2`, `flag` |
| Constants | `MAX_RETRY_COUNT` (or the language's convention) | bare `3` in the code |
| Files | `invoice-table.tsx`, `invoice-total.test.ts`, `InvoiceController.php` | a growing `utils.ts`, `helpers.js`, `styles.css` |

- Short names are fine in small scopes (`i`, `row`, `e` in a handler).
- A shared `lib/` or `utils/` folder is fine; a single catch-all file that everything imports is the thing to avoid.
- If a name needs a comment to explain it, a better name usually exists.
- **Firm:** a rename updates every reference in the same change. Search for the old name first; do not leave broken imports or half-renamed call sites.
- CSS class naming: `css-architecture`. `python "KIT/scripts/naming_check.py" .` reports naming findings as advisory notes.

## Size and shape (signals, not limits)

Long functions, many parameters and deep nesting are signals to look again, not rules to satisfy:

| Signal | Usual response |
|---|---|
| A function doing several things (often past ~40 lines) | Split along the steps it performs |
| More than ~4 parameters | Pass an options object or a domain type |
| Nesting past ~3 levels | Guard clauses and early returns |
| Two abstractions for one feature | Check whether one is enough |

A clear 60-line function beats three 20-line functions that must be read together. Do not split coherent code to hit a number.

## Over-engineering to avoid

| Instead of | Do |
|---|---|
| Comments that restate the code | Comment the why, the non-obvious, the workaround and its reason |
| A helper for a one-liner used once | Inline it |
| A factory for two objects, an interface with one implementation, a wrapper that only delegates | Use the concrete thing; extract a seam when a second implementation or a test needs it |
| Magic numbers in business logic | Named constants (tax rates, limits, timeouts) |
| A custom cache or memoisation without a measured hot path | Measure first |
| A state machine for three states | `if` / `switch` (a real workflow with many states and transitions is a different case) |

## Before editing a shared file

Check who depends on it: what imports it, what it imports, which tests cover it. **Firm:** change the file and every dependent in the same task, so the build is never left half-migrated.

## Simplifying existing code

Triggered by "simplify", "clean up", "refactor", or code that is hard to change.

1. Understand what the code does and why it was written this way; find the tests that cover it.
2. Remove dead code: unused imports, unreachable branches, commented-out blocks, flags for features that shipped, stale TODOs.
3. Flatten nesting with early returns; replace nested loops with `filter` / `map` where it reads better.
4. Inline trivial abstractions; merge functions that always change together; simplify data structures.
5. **Firm:** preserve behaviour. Run the existing tests and the build (tier per `code-rules`); if there are no tests around risky logic, add a characterisation test first or say it was not verified.

Keep complexity that a measured hot path, the framework, the user's chosen pattern, or a known next step needs. If removing an abstraction might break something you cannot see, ask.

## Working style

- Feature requested: write it; no tutorial narration in the reply.
- Bug reported: fix the cause; explain it in one line.
- Requirement unclear: state the assumption and proceed, or ask per `core-protocol` when the answer changes what gets built.
- Verification: follow the `code-rules` tier for the change; report what ran and what did not.
