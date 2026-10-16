---
name: adversarial-review
description: Review a change for consequential defects using concrete failure scenarios, affected callers and evidence. Use for requested code reviews or changes where an independent correctness review is useful; report findings without inventing issues.
version: 2.8.2
---

# Adversarial Review

Determine whether the actual change meets its intended behavior under realistic inputs and failures. A useful review can find no defects; the goal is reliable findings, not a quota or a display of suspicion.

## Establish the review boundary

Read the diff, requirement, nearby implementation, affected callers and relevant tests. Separate newly introduced defects from pre-existing problems. Identify important invariants: access is scoped to the correct account, money and stock remain consistent, retries do not repeat side effects, old consumers still understand the contract.

When requirements are incomplete, infer ordinary behavior from tests and callers. Label material uncertainty instead of manufacturing a finding. For an independent reviewer, provide the requirement and raw diff with enough surrounding context; avoid coaching them toward a predetermined conclusion.

## Try to disprove important assumptions

Choose scenarios relevant to the change:

| Surface | Concrete probes |
|---|---|
| Inputs | Empty input, boundary values, duplicate identifiers, Unicode, malformed external data, unexpectedly large collections |
| Failure paths | Rejected promises, timeouts, partial writes, failed cleanup, unavailable dependencies, retries after an unknown result |
| State and timing | Concurrent writes, duplicate delivery, stale responses, stale closures, check-then-act gaps, cancellation during work |
| Access | Authentication versus authorization, ownership, tenant boundaries, field-level write/read permissions, server enforcement |
| Data | Transactions, rounding, timestamp interpretation, pagination stability, migration compatibility, deleted or orphaned records |
| Consumers | Changed exports/types, response shape, configuration, route names, persisted state and callers outside the edited folder |

Trace the failing path before reporting it. Use an existing focused test or small reproduction when it would settle an important question. Do not run a whole security engagement or performance benchmark for an unrelated diff.

Example: an order is inserted before stock is reserved. If reservation fails, an order remains without stock. Confirm whether the calls share a transaction or compensating workflow before claiming oversell. A missing transaction keyword alone is not proof.

## Findings must explain consequence

For each actionable defect include severity, a concise title, exact location, input/timing, expected behavior, actual consequence, evidence and a targeted correction. Rank by impact, likelihood and exposure in this project.

Distinguish **confirmed**, **supported by code reasoning**, and **needs reproduction**. Treat speculation as a question or limitation. Style preferences and possible future scaling issues do not belong among defect findings.

Use the repository's severity convention. Without one: critical for plausible severe compromise or irreversible data loss; high for major user-facing failure; medium for meaningful but bounded incorrect behavior; low for smaller real defects. A category alone does not establish severity.

## Finish with an honest scope statement

Lead with important findings, then reviewed scope and material gaps. State when no actionable defects were found without implying proof of correctness. If fixes are requested, apply them and verify affected contracts. A review-only request stays review-only.

Use `systematic-debugging` for an unresolved reproduction, `testing-patterns` for regression coverage, and `vulnerability-scanner` for a genuinely broader security assessment.
