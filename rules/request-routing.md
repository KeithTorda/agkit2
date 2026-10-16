---
name: request-routing
version: 2.8.2
priority: P0
trigger: always_on
description: Route by the changed contract and required expertise; commands are optional entrypoints rather than mandatory ceremony.
---

# Routing

A pure question can be answered directly. For action, choose the nearest role by the contract being changed, not the number of matching keywords. For a mixed task, identify necessary ownership boundaries and dependency order; do not force an entire team or a fixed database/backend/frontend sequence when it does not fit. An explicit user-selected role takes precedence.

## Agents
| Role | Expertise |
|---|---|
| `frontend-specialist` | web pages, components, layout, styles and client interaction |
| `mobile-developer` | native mobile screens, platform integration and mobile interaction |
| `backend-specialist` | server behavior, APIs, jobs, auth integration and exports |
| `database-architect` | schema, migrations, transactions, persistence and queries |
| `solution-architect` | system boundaries, architecture and consequential technology choices |
| `ux-architect` | flows, navigation, screen/state structure and information hierarchy |
| `product-manager` | goals, scope, requirements and acceptance criteria |
| `project-planner` | executable milestones, dependencies and task plans |
| `plan-reviewer` | feasibility and contract gaps in a proposed plan |
| `test-engineer` | behavior tests, fixtures, regression strategy and test evidence |
| `debugger` | reproduction, competing causes and root-cause repair |
| `security-auditor` | defensive security review and confirmed trust-boundary defects |
| `penetration-tester` | authorized active security testing within explicit scope |
| `performance-optimizer` | measured latency, runtime, memory, query or bundle bottlenecks |
| `seo-specialist` | crawl/index metadata, structured content and discoverability |
| `devops-engineer` | CI, deployment, environments, operations and rollback |
| `documentation-writer` | technical/user documentation tied to actual behavior |
| `code-archaeologist` | legacy behavior, dependencies and safe modernization |
| `explorer-agent` | read-only structure, contracts and feasibility discovery |
| `orchestrator` | integration of independent work across necessary owners |

Role files are `KIT/agents/<name>.md`. Without native delegation, perform the role directly. Delegate only bounded independent work with shared decisions and clear ownership.

## Commands

| Commands | Purpose |
|---|---|
| `/create` `/enhance` | Build new work or extend the existing project |
| `/plan` `/proplan` `/brainstorm` | Plan execution or compare approaches |
| `/debug` `/fix-ui` `/see` `/see-doc` | Diagnose defects or inspect real output |
| `/test` `/verify` `/review` | Run tests, establish evidence or review a diff |
| `/orchestrate` `/deploy` | Coordinate work or perform an authorized release |
| `/status` `/remember` | Read progress or save requested project context |
| `/updatekit` `/doctor` | Maintain or diagnose the kit installation |
| `/motionv` | Produce or edit a motion/video deliverable |

Read `KIT/skills/<command>/SKILL.md` for the selected workflow. Natural-language requests can invoke it too. Use problem-solving for difficult diagnosis/tradeoffs and quick-reference only when the full catalog helps.
