---
name: review
description: "/review — Attacks the current diff as a hostile reviewer and reports concrete defects: the untested edge, the unhandled error path, the race, the security hole, and the silent wrong answer, ranked by blast radius. Use before committing, before a PR, or before reporting a non-trivial change done."
version: 1.0.0
---

# /review

**Input:** the text after `/review` narrows the scope (`/review src/checkout`). If it is empty, review the current uncommitted diff; if the tree is clean, review the last commit.
**Agent:** read `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/code-archaeologist.md` for reading unfamiliar code; `agents/security-auditor.md` when the diff touches auth, payments, or user input.
**Skills:** `@[skills/adversarial-review]` (attack categories, finding format, severity); `@[skills/clean-code]` for style-level findings.

## Steps

1. **Scope.** Run `git diff` (or `git diff --staged`; `git show HEAD` on a clean tree). Review the code on disk, not your memory of writing it.
2. **Requirement.** State in one line what the change must do. If you cannot, that is finding #1.
3. **Delegate if you can.** Spawn a subagent with the diff and the requirement — a reviewer that did not write the code cannot inherit its assumptions. Do not explain why the code is correct; that talks the reviewer into agreeing. Review in-session only when delegation is unavailable.
4. **Attack** every category in `adversarial-review`: edges, error paths, concurrency and state, trust boundaries, data integrity, the silent wrong answer, and the callers you changed around.
5. **Trace before labeling.** A finding is CONFIRMED only if you followed the path to the wrong value; otherwise SUSPECTED.
6. **Report** in the format below, ranked by consequence.

## Output

```markdown
## Adversarial Review
### Requirement
- <what this change must do>
### Reviewed
- <diff scope> · <subagent | in-session>

### Findings
1. **[Critical|High|Medium|Low]** <one-sentence defect>
   - Failure: <concrete inputs or timing → wrong output, crash, corrupted state>
   - Where: <file:line>
   - Verdict: CONFIRMED | SUSPECTED
   - Fix: <the change>

### Cleared
- <categories attacked and found sound>
### Not reviewed
- <what could not be checked and why>
```

## Rules

- **Findings only — do not fix in this turn** unless the user asks. Report, then let them choose.
- Every finding names concrete inputs and a concrete wrong outcome. No input and no consequence means it is an opinion, not a bug; drop it or demote it to Low.
- Rank by consequence, not by effort to fix. Silent data corruption outranks a crash; a crash outranks a style nit.
- Finding nothing is a valid result — say so plainly and name which categories you attacked. Do not pad with style nits to look thorough.
- Record durable dead ends found here as `[failure]` entries (`memory-system`).

## Verification

- The report names the exact diff scope reviewed.
- Every finding has inputs, a wrong outcome, a location, and a CONFIRMED/SUSPECTED verdict.
- The Cleared section lists which attack categories were actually run, so the review is auditable.
- Severity ordering is by consequence, highest first.
