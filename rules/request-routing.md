---
name: request-routing
version: 2.5.0
priority: P0
trigger: always_on
description: Which agent or command handles a request. Agents are KIT/agents/<name>.md and can also run as native subagents.
---

# Request Routing

## Commands (`KIT/skills/<command>/SKILL.md`)
| Command | Use |
|---|---|
| `/proplan <system>` | Professional plan for a system: goals, requirements, architecture, data, API, UX, security, tests, roadmap, full docs. Runs planning subagents. `--lite` for small systems |
| `/plan <task>` | Task list with owners and verify lines in `docs/plans/<slug>.md`. No code |
| `/create <app>` | New app end to end |
| `/motionv <brief>` | Motion video as code: brief, storyboard, HyperFrames (default) or Remotion build, render to MP4/WebM/GIF, frame check. `/motionv doctor` checks and installs the tools |
| `/orchestrate <task or plan path>` | Multi-domain build with subagents; can execute a `/proplan` milestone |
| `/updatekit` | Fetches the latest release of AG Kit from GitHub and syncs Antigravity |
| `/enhance` `/brainstorm` `/debug` `/test` `/verify` `/see` `/see-doc` `/fix-ui` `/review` `/deploy` `/status` `/remember` | As named; each skill states its steps |

## Agents
| Agent | Takes |
|---|---|
| `frontend-specialist` | web UI: components, pages, layout, CSS, Tailwind, React, Vue, Blade |
| `mobile-developer` | React Native, Expo, Flutter, iOS, Android |
| `backend-specialist` | API, server, auth, webhooks, jobs, Laravel, exports (PDF, Excel, DOCX, receipts) |
| `database-architect` | schema, migrations, queries, indexes, ORM |
| `solution-architect` | system architecture, integration design, ADRs, tech choices, scaling |
| `ux-architect` | user flows, screen inventory, information architecture, wireframe specs |
| `product-manager` | goals, requirements, user stories, acceptance criteria, scope, MVP |
| `project-planner` | milestones, work breakdown, estimates, dependencies, `/plan` files |
| `plan-reviewer` | adversarial review of a plan or spec before build |
| `test-engineer` | tests, test strategy, coverage, Playwright, Vitest, Pest, pytest |
| `debugger` | bugs, errors, crashes, regressions |
| `security-auditor` | security review, OWASP, secrets, threat model, data privacy |
| `penetration-tester` | authorised offensive testing only |
| `performance-optimizer` | slow pages, bundle size, Web Vitals, queries under load |
| `seo-specialist` | SEO, metadata, structured data, sitemap |
| `devops-engineer` | deploy, CI/CD, Docker, VPS, Nginx, rollback |
| `documentation-writer` | README, docs, API docs, changelog, user manuals |
| `code-archaeologist` | legacy and undocumented code, modernisation |
| `explorer-agent` | read-only codebase map and feasibility |
| `orchestrator` | coordinating several agents on one task |

- A pure question needs no agent.
- Unclear domain: pick the closest specialist; do not ask which agent.
- One domain, one agent. Several domains: `orchestrator` (or run the agents yourself in order: database → backend → frontend → tests).
