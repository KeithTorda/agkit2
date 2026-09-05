---
name: debug
description: "/debug — Investigates a bug systematically: reproduce, isolate, find the root cause, fix, verify, add a regression test. Use when something errors, crashes, misbehaves, or a test fails and the cause is not obvious."
version: 2.0.0
---

# /debug

**Input:** the text after `/debug` is the symptom (error text, failing test, or behavior).
**Agent:** read `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/debugger.md`.
**Skills:** `@[skills/systematic-debugging]` (method), `@[skills/verify-changes]` (proof), `@[skills/testing-patterns]` for the regression test.

## Steps

Run the four phases of `systematic-debugging` in order; do not skip ahead to a fix.

1. **Reproduce.** Gather what you cannot find yourself (error text, file:line, expected vs actual, recent changes via `git log --oneline -20` and `git diff`), then run the failing path and capture its output before touching code. If it will not reproduce, collect more data — never fix a symptom you cannot trigger.
2. **Isolate.** When did it start and what changed? Narrow to the smallest input, environment, and code that still triggers it. List candidate causes ordered by probability, each with the evidence that confirms or rules it out.
3. **Understand.** Ask "why" down to the root cause — a decision or a specific line, not another symptom. Confirm it with evidence before changing anything.
4. **Fix and verify.** Smallest change that removes the root cause; check dependents of the edited file (`clean-code`) and scan for the same mistake elsewhere. Re-run the reproduction and affected tests, add a regression test that fails without the fix, and run `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .` for the required checks.

## Output

```markdown
## Debug: <issue>
Symptom: <what happens> · Reproduced with: `<command>` → <output>
Root cause: <why it happens, file:line>
Fix: <what changed and why>
Verification: `<command>` → <result> · Regression test: <path>
Prevention: <validation, test, or guard added>
```

## Rules

- No random edits; every change follows a confirmed hypothesis.
- Explain why, not only what; if the cause is outside the reported area, say so.

## Verification

- The original reproduction passes, and the regression test fails without the fix.
- Required checks pass; no unrelated files changed.
