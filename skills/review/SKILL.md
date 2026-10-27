---
name: review
description: "/review - Review a diff for real correctness, behavior and security defects backed by source evidence. Use it when the user asks for a code review."
version: 3.2.0
---

# /review

Find defects that would cause a wrong outcome, with a concrete scenario for each. Invoking /review is the request, so perform the review. Use the method in `KIT/skills/adversarial-review/SKILL.md`.

## Steps

1. Set the scope: files or commits named by the user, else the current task's uncommitted diff. On a clean tree, ask which revision or branch to review.
2. Read the diff, then the full changed files and their callers.
3. Write the intended behavior in one or two lines.
4. Trace the paths that matter for this change: success, validation error, empty or boundary input, concurrent requests and permission checks.
5. Check the change against rule-06-security-baseline (server-side auth, safe queries, secrets, money records) and rule-04-system-integration when it touches ERP sync.
6. For each finding, record: scenario, wrong outcome, file and line, and impact. Mark it Confirmed or Possible.
7. For large or sensitive changes, give an independent reviewer the requirement and the diff, without your reasoning for why it is correct, via `KIT/skills/parallel-agents/SKILL.md`. If delegation is unavailable, review directly and say so.
8. Review-only request: report, do not edit. If fixing is part of the task, apply the confirmed fixes.

## Output

| # | Severity | Location | Scenario and impact | Status |
|---|---|---|---|---|

List the highest-impact findings first. If none are found, say "No actionable defects in the inspected scope" and name what was inspected. Skip pure style preferences.

## Before you finish, check

- [ ] Each finding has a reachable scenario and a file location.
- [ ] Confirmed and Possible findings are separated.
- [ ] Files were not edited on a review-only request.
- [ ] Gaps in what was inspected are stated.
