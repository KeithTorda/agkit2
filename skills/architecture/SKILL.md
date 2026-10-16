---
name: architecture
description: Evaluate system boundaries, persistence, integration and deployment choices against real requirements. Use for material architecture trade-offs or ADRs, including the architecture portion of a plan; keep ordinary implementation decisions lightweight.
version: 2.8.2
---

# Architecture

Select a structure that supports required behavior and can be operated by the actual team. Preserve a sound existing architecture. A new structure needs a concrete problem, a viable simpler alternative and an explanation of its costs.

## Work from evidence

Identify users, business invariants, integrations, deployment constraints and likely failure modes. Distinguish measured demand, contractual requirements and guesses. Infer context from the repository and brief; ask only when an answer materially changes a hard-to-reverse decision. Do not start a fixed questionnaire for routine work.

Compare options against consistency, latency, availability, recovery, delivery effort, operating capacity and reversibility. User counts and team size alone do not select an architecture. A monolith can run at substantial scale; a small system may need isolated deployment for integration or regulatory reasons.

Name ownership for each state change. Identify transaction boundaries, asynchronous retries, duplicate handling and what users see after partial failure. Distributed components do not create reliability without these contracts.

## Read only relevant detail

| Reference | Read when |
|---|---|
| [context-discovery.md](context-discovery.md) | Important constraints/current-system behavior need discovery |
| [pattern-selection.md](pattern-selection.md) | Comparing deployment, data access, domain or async boundaries |
| [patterns-reference.md](patterns-reference.md) | Checking a pattern's costs and failure modes |
| [trade-off-analysis.md](trade-off-analysis.md) | Recording an important decision and its revisit signal |
| [examples.md](examples.md) | Looking for worked trade-offs, including offline/multi-tenant systems |

## Make the decision usable

Document the boundary, source of truth, neighbor contracts and material trade-offs. For expensive decisions, record an ADR using project conventions. A local reversible choice may need only a concise plan/code explanation.

Describe how to test the decision: failure injection, representative measurement, restore rehearsal, migration dry run or boundary tests. Label unverified assumptions and reconsideration signals. Do not promise zero downtime, security, scale or easy extraction without evidence.

Use `database-design` for schema/transactions, `api-patterns` for external contracts and `frontend-architecture` for UI ownership. Architecture advice does not authorize deployment or unrelated rewrites.
