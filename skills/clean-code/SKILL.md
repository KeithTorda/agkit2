---
name: clean-code
description: Pragmatic coding standards for every code change — naming, function limits (30 lines, 4 parameters, nesting 3), no over-engineering, dependent-file checks, simplification of existing code, and how to act on verification results. Use whenever writing, editing, refactoring, or simplifying code.
version: 2.0.0
---

# Clean Code

> Concise, direct, solution-focused. The user wants working code, not a lesson.

## Principles

| Principle | Rule |
|---|---|
| SRP | One job, one reason to change — if describing it needs "and", split it |
| DRY | Extract duplicates once they repeat, not before |
| KISS | The simplest solution that works |
| YAGNI | Do not build what nothing uses yet |
| Boy Scout | Leave touched code cleaner than you found it |

## Naming

| Element | Convention |
|---|---|
| Variables | Reveal intent: `userCount`, not `n` |
| Functions | Verb + noun: `getUserById()` |
| Booleans | Question form: `isActive`, `hasPermission`, `canEdit` |
| Constants | `SCREAMING_SNAKE`: `MAX_RETRY_COUNT` |

If a name needs a comment, rename it.

### Unique, searchable names

Policy: global `code-rules` "Unique, searchable names". The rules:

- Files are `<domain>-<role>.<ext>`: `invoice-table.tsx`, `invoice-total.test.ts`. Banned bare filenames, any extension: `utils.ts helpers.ts styles.css types.ts constants.ts common.ts misc.ts`. `index.*` only where the framework needs it (route folders). No two files in a repo share a basename.
- Exported or shared identifiers are domain-prefixed and intention-revealing: `formatInvoiceTotal`, `useCartItems`, `InvoiceTable`. Never `Component2`, `NewButton`, `data`, `item`, `temp`, `result`, `handleClick`, `doStuff`, `process`, `manager`, `helper`. Local loop variables may be short (`i`, `row`).
- A rename updates every reference: grep the old name first, then change all of them in the same task.
- CSS classes and custom properties: `css-architecture`. Check: `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/naming_check.py .`

## Limits

| Measure | Limit |
|---|---|
| Function length | ≤ 30 lines (aim for 5–15) |
| Parameters | ≤ 4; beyond that, pass an options object |
| Nesting | ≤ 3 levels; use guard clauses and early returns |
| Abstractions per feature | ≤ 2 |
| Dead code | 0 |

Structure: guard clauses first, small functions composed, related code colocated, one level of abstraction per function, no unexpected mutation of inputs.

## Anti-patterns

| Instead of | Do |
|---|---|
| Commenting every line | Delete obvious comments; let code self-document |
| A helper for a one-liner | Inline it |
| Factory for two objects, interface with one implementation, wrapper that only delegates | Direct instantiation; use the class |
| `utils.ts` with one function | Put the code where it is used |
| Magic numbers | Named constants |
| God functions | Split by responsibility |
| Custom cache or memoization without a measured hot path | Remove it; measure first |
| State machine for three states | `if` / `switch` |
| "First we import…" tutorials in responses | Just write the code |

## Working style

| Situation | Action |
|---|---|
| Feature requested | Write it directly |
| Bug reported | Fix it; explain the cause in one line |
| Requirement unclear | Follow the global `core-protocol` questions rule; otherwise state assumptions |

## Before editing a file, check dependents

| Question | Why |
|---|---|
| What imports this file? | Callers break on signature changes |
| What does it import? | Interface changes ripple |
| Which tests cover it? | They still have to pass |
| Is it shared? | Several places are affected |

Edit the file and every dependent in the same task. Never leave broken imports or half-updated call sites.

## Simplifying existing code

Triggered by "simplify", "clean up", "reduce complexity", or when the limits above are exceeded.

1. Understand first: what the code does, why it was written this way, which tests cover it.
2. Remove dead code: unused imports, unreachable branches, commented-out code, flags for launched features, stale TODOs.
3. Flatten nesting with early returns and `filter` / `map` over nested loops.
4. Inline trivial abstractions; merge related functions; simplify data structures.
5. Prove behavior is preserved: run the existing tests and the build.

Keep complexity when a measured hot path needs it, a framework requires it, the user chose the pattern, or a known near-term extension depends on it. If unsure, ask before removing an abstraction.

## Self-check before "done"

| Check | Question |
|---|---|
| Goal | Did I do exactly what was asked? |
| Files | Did I update every affected file? |
| Works | Did I run it? (`@[skills/verify-changes]`) |
| Clean | Lint and types pass; edge cases handled? |

The verification gates are in `C:/Users/Keith/.gemini/config/rules/code-rules.md`; the fast gate is `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .`. Any agent runs any check that applies to its change.

## Auto-fix policy

Auto-fix policy: global `code-rules` rule (required failures are fixed automatically; advisory findings are reported, and design/scope changes they suggest are confirmed first). Apply it; do not restate it.

Report script results briefly: what failed, what was fixed, what remains advisory.
