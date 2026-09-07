---
name: request-routing
version: 2.0.0
priority: P0
trigger: always_on
description: Classifies every request and routes it to the right specialist agent or slash command before any work starts.
---

# Request Routing

## 1. Classify
| Type | Signals | Response |
|---|---|---|
| QUESTION | what is, how does, explain | Text answer; no agent, no plan file |
| SURVEY | analyze, overview, map the codebase | `explorer-agent`, report only |
| SIMPLE CODE | add / change in one file, UI tweak | Specialist, **Build** steps, proceed directly |
| REPAIR | fix, broken, wrong, not working, out of place, misaligned, overlapping, cut off, regression | Specialist, **Repair** steps; UI → `/fix-ui` |
| COMPLEX CODE | build / implement / refactor across files | Specialist, plan file required |
| NEW APP | new app, from scratch, multi-page | `/create` → `project-planner` → `orchestrator` |
| MULTI-DOMAIN | frontend + backend + data in one task | `orchestrator` |
| COMMAND | `/plan` `/debug` `/test` `/verify` `/see` `/fix-ui` `/review` `/deploy` `/orchestrate` `/enhance` `/brainstorm` `/remember` `/status` `/create` | Read `skills/<command>/SKILL.md`, follow its Steps |

## 2. Pick the agent (`C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/<name>.md`)
| Agent | Triggers |
|---|---|
| frontend-specialist | component, react, next.js, vue, nuxt, blade, livewire, ui, css, tailwind, page |
| mobile-developer | mobile, react native, expo, flutter, ios, android |
| backend-specialist | backend, api, endpoint, service, auth, webhook, queue, laravel, php, artisan, eloquent |
| database-architect | database, sql, schema, migration, query, prisma, drizzle, eloquent schema |
| test-engineer | test, spec, coverage, e2e, playwright, vitest, flaky |
| debugger | bug, error, crash, stack trace, not working, regression |
| security-auditor | security, vulnerability, owasp, xss, injection, secrets |
| penetration-tester | exploit, attack simulation, red team (authorized only) |
| performance-optimizer | performance, slow, bundle size, lighthouse, web vitals |
| seo-specialist | seo, geo, ranking, meta tags, structured data, sitemap |
| devops-engineer | deploy, ci/cd, docker, server, release, rollback |
| project-planner | plan, roadmap, scope, milestones, task breakdown |
| product-manager | requirements, user story, prd, backlog, mvp, prioritize |
| documentation-writer | readme, api docs, changelog, docstring, adr |
| code-archaeologist | legacy, undocumented, modernize, brownfield |
| explorer-agent | explore, map codebase, architecture overview |
| orchestrator | orchestrate, multi-agent, full-stack, end-to-end |

Mobile ≠ frontend-specialist; a mobile app's backend goes to backend-specialist. If the user names `@agent`, use it. Unclear domain → the closest specialist, not the orchestrator. Then continue with `core-protocol` step 2: read that agent file now.
