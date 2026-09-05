---
name: systematic-debugging
description: Four-phase debugging method — reproduce, isolate, understand the root cause, fix and verify with a regression test. Use for any bug, crash, failing test, or unexpected behavior whose cause is not obvious, and for /debug.
version: 2.0.0
---

# Systematic Debugging

> Understand the problem before changing code. No guessing.

## Phase 1: Reproduce

Reliably trigger the issue before fixing anything.

```markdown
Steps: 1. <exact step> 2. <next step> → expected: <x>, actual: <y>
Rate: always | often | sometimes | rare
```

If it cannot be reproduced, gather more data (logs, inputs, environment) before proposing a fix.

## Phase 2: Isolate

- When did it start? What changed? (`git log --oneline -20`, `git diff HEAD~5`)
- Does it happen in every environment, for every input?
- What is the smallest reproduction? The smallest change that triggers it?

## Phase 3: Understand

Find the cause, not the symptom. Ask "why" until the answer is a decision or a line of code rather than another symptom:

```markdown
1. Why does the page crash?    → `user` is undefined
2. Why is it undefined?        → the fetch returned 401
3. Why 401?                    → the token expired exactly at the boundary
4. Why does the boundary fail? → the expiry check uses `<` instead of `<=`   ← root cause
```

## Phase 4: Fix and verify

- Smallest change that removes the root cause; check dependents of the edited file (`@[skills/clean-code]`).
- The reproduction from Phase 1 passes; related functionality still works; no new issues.
- Add a regression test that fails without the fix.
- Check similar code for the same mistake.
- Prove it per `@[skills/verify-changes]`.

## Useful commands

```bash
git log --oneline -20 && git diff HEAD~5        # recent changes
grep -rn "errorPattern" --include="*.ts" src      # locate the pattern
npx vitest run path/to/failing.test.ts            # run one test
pm2 logs app-name --err --lines 100               # server logs
```

## Anti-patterns

| Avoid | Because |
|---|---|
| "Maybe if I change this…" | Random edits hide the cause and add bugs |
| "That can't be it" | Evidence beats intuition |
| Fixing before reproducing | The fix cannot be proven |
| Stopping at the first symptom | It returns in another form |
