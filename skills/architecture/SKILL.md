---
name: architecture
description: Architecture decisions - context discovery, pattern selection (monolith, modular monolith, services, event-driven), trade-off analysis and ADRs. Use when choosing a system structure, comparing patterns, documenting a hard-to-reverse decision, or writing the architecture part of a /proplan; not for writing code.
version: 2.5.0
---

# Architecture

Requirements drive the structure; trade-offs are written down; decisions that are expensive to reverse get an ADR. Everything else in a small project can be decided in one line and changed later.

Read only the file the request needs:

| File | Use when |
|---|---|
| `context-discovery.md` | Starting a design: scale, team, timeline, domain, constraints; project classification |
| `pattern-selection.md` | Choosing a pattern: decision tree, the three questions, over-engineering signs |
| `patterns-reference.md` | Comparing data-access, domain-logic and distributed patterns side by side |
| `trade-off-analysis.md` | Writing an ADR: template, numbering, where it lives |
| `examples.md` | Reference decisions for projects like Nikko's: LGU portal, POS/inventory, SaaS, larger systems |

Related: `database-design` (schema, the data-model document), `api-patterns` (API style and contract).

## Principles

- **Start simple.** Add a pattern when a requirement proves it necessary; patterns are cheap to add later and expensive to remove. A modular monolith is the right default until scale, team size or independent deploys force a split.
- **Dependencies point inward.** Business rules should not import the web framework or the ORM's query details; adapters (DB, HTTP, UI, third-party SDKs) depend on the rules, not the reverse. In a small Laravel or Next.js app this can be as light as keeping pricing, stock and permission logic in plain functions or action classes rather than in controllers and components.
- **High cohesion, low coupling.** Group by feature or domain (`orders/` owning its logic) rather than smearing one feature across `controllers/`, `services/`, `models/`. A real boundary can change its internals without callers noticing, and you can say what it owns in one sentence.
- **Boring by default.** Prefer the stack in `code-rules` (or the project's existing stack) and well-known hosting. A new technology needs a named problem it solves.

## Depth by stakes

| Situation | What to produce |
|---|---|
| Small site or feature inside an existing app | One line in the reply: the structure and why |
| New app, a few modules, one developer | A short architecture section in the `/plan` file, plus an ADR only for the choices that are hard to reverse (database, auth, hosting, multi-tenancy) |
| Client system, several roles, money or government data, or a team | `/proplan` (below) |

## In `/proplan`

`solution-architect` owns phase 2 (architecture decision) of `/proplan` and uses this skill as its reference. Templates are in `KIT/skills/proplan/templates/`; follow them over the shapes in this skill when they differ.

1. **Inputs.** Read the plan's overview, goals (`G-`) and requirements (`R-`, `NFR-`) documents. Run `context-discovery.md` against them; list any context the documents do not answer as an open question rather than inventing it.
2. **Options.** For the system shape and each consequential choice (database, auth, hosting, integration style, offline or real-time needs), hold two viable options and compare them with `pattern-selection.md` and `patterns-reference.md`.
3. **`03-architecture.md`.** Write the context (users, external systems), the containers (apps, services, database, queues, third parties) with a simple diagram (Mermaid is fine), the module boundaries and what each owns, how each `NFR-` is met, deployment, and the risks you are accepting.
4. **ADRs.** One file per hard-to-reverse decision in `docs/proplan/<slug>/adr/`, numbered `ADR-001`, `ADR-002`, ... using the template in `trade-off-analysis.md` (or the proplan template). Each ADR names the `R-`/`NFR-` IDs it serves so `proplan_check.py` can trace it.
5. **Checkpoint.** Present the recommended architecture with its main trade-off to Nikko before phase 3 builds on it. The data model (`04-data-model.md`) is written next by `database-architect` with `database-design`.

## Before finalising

- The constraints you designed for are written down, and the ones you assumed are marked as assumptions.
- Each significant decision names a simpler alternative and why it was not enough.
- ADRs exist for decisions that are expensive to reverse, and only for those.
- The team (often one developer) can build and run what you chose.
