---
name: systematic-debugging
description: Four-phase debugging method - reproduce, isolate, understand the root cause, fix and verify with a regression test. Use for any bug, crash, failing test or unexpected behaviour whose cause is not obvious, and for /debug.
version: 2.5.0
---

# Systematic Debugging

Understand the problem before changing code. Every edit follows a confirmed hypothesis.

## Phase 1: Reproduce

Trigger the issue reliably before fixing anything. Gather what you cannot find yourself (exact error text, file:line, expected vs actual, when it started), then run the failing path and capture its output.

```markdown
Steps: 1. <exact step> 2. <next step> → expected: <x>, actual: <y>
Rate: always | often | sometimes | rare
```

It will not reproduce: gather more data (logs, inputs, environment, data state) before proposing a fix. Never fix a symptom you cannot trigger.

## Phase 2: Isolate

- When did it start, and what changed? (`git log --oneline -20`, `git diff HEAD~5`, `git bisect` for a known-good commit)
- Every environment, every input, every user? Or only production, only one role, only large data?
- What is the smallest input and smallest code that still triggers it?
- List candidate causes by probability, each with the evidence that would confirm or rule it out. Independent hypotheses in a large codebase can be checked in parallel with `research` subagents (`parallel-agents`).

## Phase 3: Understand

Ask "why" until the answer is a decision or a line of code, not another symptom:

```markdown
1. Why does the page crash?    → `user` is undefined
2. Why is it undefined?        → the fetch returned 401
3. Why 401?                    → the token expired exactly at the boundary
4. Why does the boundary fail? → the expiry check uses `<` instead of `<=`   ← root cause
```

Confirm the root cause with evidence (a log line, a failing test, a value in the debugger) before changing anything.

## Phase 4: Fix and verify

- Smallest change that removes the root cause; update the callers of anything you changed.
- The Phase 1 reproduction now passes; related behaviour still works.
- Add a regression test that fails without the fix, when the code has a test setup. If not, say how you verified instead.
- Search for the same mistake elsewhere.
- Run the checks the change's tier calls for (`code-rules`); prove it per `verify-changes`.
- A durable cause the next session could repeat goes to memory as a `[failure]`.

## Useful commands

```powershell
git log --oneline -20; git diff HEAD~5                 # recent changes
git bisect start; git bisect bad; git bisect good <sha> # find the breaking commit
rg -n "errorPattern" src                                # locate the pattern (Select-String without ripgrep)
npx vitest run path/to/failing.test.ts                  # one test
php artisan test --filter=OrderTest                     # one Laravel test
Get-Content storage/logs/laravel.log -Tail 100          # Laravel log
pm2 logs app-name --err --lines 100                     # Node server logs
```

## Anti-patterns

| Avoid | Because |
|---|---|
| "Maybe if I change this..." | Random edits hide the cause and add bugs |
| "That can't be it" | Evidence beats intuition |
| Fixing before reproducing | The fix cannot be proven |
| Stopping at the first symptom | It returns in another form |
| Wrapping it in try/catch | Hides the error instead of fixing it (`code-rules`: fix at the source) |
