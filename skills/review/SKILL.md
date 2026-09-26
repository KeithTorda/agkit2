---
name: review
description: "/review - Attacks a diff as a hostile reviewer and reports concrete defects (untested edge, unhandled error path, race, security hole, silent wrong answer) ranked by consequence. On-demand deep check; part of tier 2 verification (auth, payments, permissions, migrations, shared code) and before a PR."
version: 2.5.0
---

# /review

**Input:** the text after `/review` narrows the scope (`/review src/checkout`). Empty: the uncommitted diff; clean tree: the last commit.
**Read now:** `KIT/skills/adversarial-review/SKILL.md` (attack categories, finding format, severity).
**Agent when needed:** `KIT/agents/security-auditor.md` if the diff touches auth, payments or user input; `KIT/agents/code-archaeologist.md` for unfamiliar code.

When it runs: the user asks, or the change is tier 2 or higher in `code-rules`. A copy change or a single component does not need it.

## Steps

1. **Scope.** `git diff` (or `git diff --staged`; `git show HEAD` on a clean tree). Review the code on disk, not your memory of writing it.
2. **Requirement.** One line: what the change must do. If you cannot state it, that is finding 1.
3. **Delegate if you can.** `invoke_subagent` a reviewer with only the diff scope and the requirement (the `self` subagent, or `security-auditor` for sensitive code). Do not explain why the code is correct; that talks the reviewer into agreeing. Review in-session when subagents are unavailable.
4. **Attack** every category in `adversarial-review`, then trace each finding: CONFIRMED only if you followed the path to the wrong value, otherwise SUSPECTED.
5. **Report** ranked by consequence (format in `adversarial-review`, with `Reviewed: <scope> · <subagent | in-session>`).

## Rules

- Findings only; do not fix in this turn unless the user asks.
- Every finding names concrete inputs and a concrete wrong outcome. No input and no consequence: drop it or mark it Low.
- Finding nothing is a valid result; say so and list the categories you attacked. Do not pad with style nits.
- A durable dead end found here goes to memory as a `[failure]` (`memory-system`).
