---
name: architecture
description: Architecture decision framework — context discovery, trade-off analysis, pattern selection, and ADR templates. Use when choosing a system structure, comparing patterns (monolith, modular, microservices, event-driven), or documenting an architectural decision; not for writing code.
version: 2.0.0
---

# Architecture Decision Framework

> Requirements drive architecture. Trade-offs inform decisions. ADRs capture rationale.

Read only the file the request needs:

| File | Use when |
|---|---|
| [context-discovery.md](./context-discovery.md) | Starting a design: scale, team, timeline, domain, constraints; MVP / SaaS / enterprise classification |
| [pattern-selection.md](./pattern-selection.md) | Choosing a pattern: decision tree, the three questions, anti-patterns |
| [trade-off-analysis.md](./trade-off-analysis.md) | Documenting a decision: ADR template, storage in `docs/architecture/` |
| [patterns-reference.md](./patterns-reference.md) | Comparing data-access, domain, distributed, and API patterns |
| [examples.md](./examples.md) | Reference decisions for MVP, SaaS, and enterprise projects |

Related: `@[skills/database-design]` for schema design, `@[skills/api-patterns]` for API style.

## Core principles

- **Start simple.** Add a pattern only when a requirement proves it necessary; patterns are cheap to add later and expensive to remove. A modular monolith wins until scale, team size, or independent deploys force the split — not before.
- **Dependencies point inward.** Business logic depends on nothing; adapters (DB, HTTP, UI, third-party SDKs) depend on it, never the reverse. If the domain layer imports the ORM or the web framework, the arrow is backwards.
- **High cohesion, low coupling.** Group by feature/domain, not by technical layer (`orders/` owning its logic, not `controllers/ + services/ + models/` smeared across the tree). Test for a real boundary: it can change its internals without callers noticing, and you can state what it owns in one sentence.

## Before finalizing

- Requirements and constraints are understood. Questions: follow the global `core-protocol` rule.
- Each significant decision has a trade-off analysis and a simpler alternative considered.
- ADRs are written for decisions that are expensive to reverse.
- The chosen patterns match the team's expertise.
