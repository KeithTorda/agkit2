# Trade-off Analysis and ADRs

Write an ADR (Architecture Decision Record) for decisions that are expensive to reverse: database, auth approach, hosting, multi-tenancy, sync/offline strategy, a load-bearing dependency, a public API shape. Do not write one for choices that a later commit can undo cheaply.

In `/proplan`, use the ADR template in `KIT/skills/proplan/templates/` if it differs from this one; the plan's checker expects its IDs. A worked example: `KIT/skills/proplan/example/pos-lite/adr/`.

## Template

```markdown
---
adr: ADR-001
title: <decision in a few words>
status: proposed | accepted | superseded by ADR-00X
date: YYYY-MM-DD
deciders: <client or owner>, developer
---

# ADR-001: <decision in a few words>

## Context
The problem, the constraints (team, budget, hosting, deadline, data sensitivity) and what forces a decision now. In a /proplan, cite the requirement IDs it serves (for example NFR-02, R-009).

## Options
| Option | Pros | Cons | Cost / complexity |
|---|---|---|---|
| A | ... | ... | Low |
| B | ... | ... | Medium |

## Decision
What we chose, specifically (versions, services, boundaries).

## Why
Two or three reasons tied to the constraints and requirements above.

## Trade-offs accepted
What we give up and why that is acceptable now.

## Consequences
- Positive: ...
- Negative: ...
- Mitigation: ...

## Revisit when
The signal that should reopen this decision (for example: more than 5 branches, offline use required, a second client).
```

## Where ADRs live

| Project | Location |
|---|---|
| `/proplan` | `docs/proplan/<slug>/adr/ADR-001-<short-title>.md` |
| Anything else | `docs/architecture/adr/ADR-001-<short-title>.md` |

Numbers are never reused. To change a decision, write a new ADR and mark the old one "Superseded by ADR-00X".

## Writing the trade-off well

- Name the constraint that decides it; "industry standard" is not a reason.
- Compare real options the project could build; a straw-man second option is worse than none.
- State the cost in the client's terms where it matters: hosting per month, time to build, what breaks if the developer leaves.
