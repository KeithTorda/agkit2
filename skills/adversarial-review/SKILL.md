---
name: adversarial-review
description: Attacks your own diff before you report it done — hunting the likeliest bug, the untested edge, the unhandled error path, the race, and the security hole, then reporting findings with concrete failure scenarios ranked by blast radius. Use before reporting done on a non-trivial change, before a commit or PR, and for /review.
version: 1.0.0
---

# Adversarial Review

> A review that sets out to confirm the code is fine will confirm the code is fine. Set out to break it.

Self-review fails for one reason: you already believe the code is correct — you just wrote it — so
"does this look right?" returns yes. The fix is to change the question. **Assume a defect exists and
go find it.** If you finish having found nothing, you either did not look hard enough or the change
is genuinely small; say which.

## The strong form

Spawn a subagent to review the diff. A fresh reviewer has no memory of the reasoning that produced
the code, so it cannot inherit the assumption that the reasoning was sound — the single biggest
source of missed bugs in self-review. Give it the diff and the requirement, not your explanation of
why the code is correct: explaining your logic to the reviewer is how you talk it into agreeing.

Reviewing in-session is the fallback. It still works if you follow the discipline below.

## Protocol

1. **Read the actual diff.** `git diff` (or `git diff --staged`). Review the code on disk, never your
   memory of what you wrote — the gap between those two is where bugs live.
2. **Restate the requirement in one line.** You cannot judge correctness without it. If you cannot
   state it crisply, that is the first finding.
3. **Hunt by category** (below). For each category, ask "what input or timing breaks this?" and try
   to construct it concretely.
4. **Falsify, do not confirm.** For every claim the code makes — "this is always non-null", "this
   runs once", "the user is authorized here" — look for the path where it is false.
5. **Check the blast radius.** Who else calls the function you changed? Who else consumes the type,
   the column, the endpoint? A change that is correct locally and breaks a caller is still a bug.
6. **Rank and report.** Severity by consequence, not by how easy it is to fix.

## Attack categories

- **The edge you did not test** — empty, exactly one, many, huge, zero, negative, `null`/`undefined`,
  duplicate, unicode and emoji, very long strings. Off-by-one at the boundary of every loop and slice.
- **The error path** — when the `await` throws, is it caught? Does the catch swallow it silently? Is
  partial state left behind — a row written without its child, a file created without cleanup, a
  loading flag never cleared? Error paths are the least-tested code in any change.
- **Concurrency and state** — two requests at once, a double-clicked button, a stale closure reading
  an old value, a state update after unmount, a check-then-act with a gap between the check and the
  act (`if (!exists) create()` under concurrency).
- **Trust boundaries** — is untrusted input validated at the boundary, or cast and trusted? Is
  authorization enforced on the server, or only by hiding the button? Is the SQL parameterised? Does
  user input reach a template, a shell, or a file path?
- **Data integrity** — a multi-step write with no transaction, an unbounded query, an N+1 introduced
  by a new relation, a migration that is not safe to run while the old code is live.
- **The silent wrong answer** — the worst class: no crash, no error, just an incorrect number, a
  wrong sort order, a timezone shifted by a day, a rounding error on money, a filter that quietly
  matches nothing. Look for these first; nothing alerts you to them.
- **What you changed around** — the caller you did not open, the test you did not run, the other
  consumer of the type you widened.

## What a real finding looks like

A finding is a concrete failure, not a vague worry. If you cannot say what input produces what wrong
result, you have a code-style opinion, not a bug.

```text
WEAK (theater — no input, no consequence, unfalsifiable)
  "Consider adding error handling to the fetch."
  "The state management here could be cleaner."
  "Might want to check for edge cases."

STRONG (a specific path to a specific wrong outcome)
  "getTotal() sums cart.items with reduce and no initial value. On an empty cart,
   reduce throws 'Reduce of empty array with no initial value' — the cart page
   500s for every new user. Repro: sign up, open /cart. Fix: reduce(fn, 0)."

  "checkout() writes the order, then decrements stock in a second query with no
   transaction. If the decrement fails, the order exists with stock never
   reserved — silent oversell. Two concurrent checkouts of the last item both
   succeed."
```

## Severity

| Level | Meaning |
|---|---|
| **Critical** | Data loss or corruption, an auth or injection hole, money computed wrong |
| **High** | A crash or a wrong result on a path real users hit |
| **Medium** | Wrong behavior on an uncommon path, or a missing error path |
| **Low** | Style, naming, a refactor that would help later |

Rank by consequence. A one-line fix that prevents silent data corruption outranks a large refactor
that prevents nothing.

## Report

```markdown
## Adversarial Review
### Requirement
- <one line: what this change must do>
### Reviewed
- <files / diff scope> · <in-session or subagent>

### Findings
1. **[Critical|High|Medium|Low]** <one-sentence defect>
   - Failure: <concrete inputs or timing → wrong output, crash, or corrupted state>
   - Where: <file:line>
   - Verdict: CONFIRMED (traced the failing path) | SUSPECTED (needs a run to prove)
   - Fix: <the change>

### Cleared
- <categories you attacked and found sound — say which, so the review is auditable>
### Not reviewed
- <what you could not check and why>
```

## Failure modes of the review itself

- **Confirmation review** — walking the diff agreeing with it. If every category comes back clean on
  a substantial change, you narrated the code instead of attacking it.
- **Style findings dressed as bugs** — naming and formatting are Low, and belong to `clean-code`.
  Padding a report with them hides the absence of real findings.
- **Reviewing your intent** — judging what the code was meant to do rather than what it does. Read
  the branches that exist, including the ones you did not think about while writing.
- **Stopping at the first finding** — fix it, then keep hunting. Bugs cluster; the code that had one
  edge unhandled usually has three.
- **Unfalsifiable findings** — "this might not scale" with no number, no query, no path. Either
  construct the failure or drop it.
- **Claiming CONFIRMED without tracing it** — if you did not follow the actual path to the actual
  wrong value, it is SUSPECTED. Mislabeling burns the user's trust in the whole report.

## Boundaries

Findings only — this skill does not fix. Apply fixes through the normal build-and-verify flow, and
prove them with `verify-changes`; UI findings go through the render gate (`browser-verification`).
Full security assessment belongs to `vulnerability-scanner` and `red-team-tactics`; this is the
security pass over *your own diff*, not an audit of the codebase.
