---
doc: REVIEW
project: <slug>
version: 0.1.0
status: draft
owner: plan-reviewer
updated: YYYY-MM-DD
---

<!--
Owner: plan-reviewer (Phase 5). The reviewer did not write any of the documents it reviews.
IDs defined here:
  RV-01 ...  findings, defined as the first cell of the findings table.
Severity:
  blocker  the plan cannot be built as written or will build the wrong thing (Must requirement with no task, contradiction on money or auth, no rollback for a destructive migration)
  major    will cause rework or a missed date (untestable criteria, no buffer, missing NFR)
  minor    wording, consistency, small gaps
Status: open -> fixed (by whom, which version) or accepted (who accepted the risk and why).
The checker fails while any blocker is "open".
Every finding cites the document and the ID or line, the check that found it, and a concrete fix.
-->

# Plan Review

## Verdict

<!-- One of: Ready to build. / Ready after the listed fixes. / Not ready: <main reason>. Then 2-4 sentences on the plan's strongest and weakest parts. -->

## Checks run

| Check | Result | Findings |
|---|---|---|
| Untestable requirements (acceptance criteria without concrete values) | | |
| Missing NFRs (performance, availability, security, privacy, accessibility, data integrity) | | |
| Unowned tasks, tasks without a failing verify line | | |
| Circular or wrong-order dependencies | | |
| Scope creep (requirements with no goal, tasks with no requirement) | | |
| Estimates without buffer, tasks over 3 days, unrealistic capacity | | |
| Security gaps (threats without planned mitigation, authorization holes, personal data without retention) | | |
| Missing rollback or backup for deploys and migrations | | |
| IDs not traced (goals without requirements, Must without task or test) | | |
| Contradictions between documents | | |

## Findings

| ID | Severity | Check | Where | Finding | Fix | Status |
|---|---|---|---|---|---|---|
| RV-01 | | | | | | open |

## Decisions for the user

<!-- Findings the coordinator cannot fix without the user's call (scope cut, budget, deadline). Each with a recommended answer. -->

## Checker output

<!-- Paste the final result line of proplan_check.py after the fixes, e.g. "Result: PASS - 0 error(s), 2 warning(s)", and list accepted warnings. -->
