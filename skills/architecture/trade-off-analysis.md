# Record an architecture decision

Record a decision when its rationale, compatibility or recovery cost would otherwise be lost. A database, tenancy boundary, durable queue, identity approach or offline consistency model may deserve an ADR. A small local reversible choice can remain in the task plan or code.

Use the repository's existing ADR location, numbering and metadata. For `/proplan`, preserve its templates and document IDs so supporting scripts/callers remain compatible. Do not add a parallel documentation system.

## Practical template

```markdown
# ADR-<id>: <specific decision>
Status: Proposed | Accepted | Superseded by <id>
Date: YYYY-MM-DD

## Context and evidence
The requirement, current behavior, decisive constraints and what forces a choice.
Link relevant requirements, measurements or existing contracts.

## Viable options
Compare actual alternatives on the dimensions that matter here.
Include keeping/extending the current system when feasible.

## Decision
State the boundary, source of truth, chosen mechanism and supported environment.

## Consequences and safeguards
Accepted costs, failure semantics, compatibility, rollout and recovery limits.

## Validation
What test, measurement or rehearsal supports the important assumptions?
What remains unknown?

## Revisit when
A concrete signal or changed requirement that would reopen this decision.
```

Version/API details belong in the decision when material and verified; do not freeze a guessed "latest" stack into reusable guidance.

## Compare honestly

Use alternatives the team could actually operate. "Industry standard" is not a reason by itself. Tie each benefit to a requirement and each cost to its owner: coordination, monthly spend, migration risk, failure recovery or maintenance effort. Label estimates rather than inventing exact costs.

Separate a decision from an unresolved experiment. A proposed architecture can include a time-bounded prototype to resolve a question without presenting a hypothesis as a proven capability.

## Changing course

Preserve the old rationale and mark it superseded when meaningful history exists. Link the replacement and explain what evidence/requirement changed. Do not retroactively rewrite historical decisions to make the new choice look inevitable.
