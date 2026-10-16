---
name: review
description: "Review a diff for concrete behavior, correctness and security defects with source evidence. Use /review for a requested review or a justified sensitive-change check; do not manufacture findings."
version: 2.8.2
---

# /review

Read `KIT/skills/adversarial-review/SKILL.md`. Use an explicit scope when supplied; otherwise inspect the current task's diff. On a clean tree identify the intended revision before reviewing arbitrary history. Read actual code and callers alongside the diff.

State the intended behavior, then trace important success, error, boundary, concurrency and authorization paths relevant to the change. Support each finding with a concrete scenario, reachable wrong outcome, source location and consequence. Distinguish confirmed defects from uncertain hypotheses. Style preferences without a material effect are not defects.

An independent reviewer can improve confidence for substantial changes. Give them the requirement and artifacts without an explanation of why the implementation is correct; use available tools via parallel-agents. Review directly when delegation is unavailable and describe it honestly.

For a review-only request, report findings without changing files. If fixing is already part of the authorized task, implement justified fixes and verify them. Present the highest-impact findings first, or state that no actionable defects were found within the inspected scope. Include relevant evidence gaps; a clean review does not promise zero future bugs.
