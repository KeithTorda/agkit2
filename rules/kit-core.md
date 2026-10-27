---
name: kit-core
version: 3.0.0
priority: P0
trigger: always_on
description: Kit plumbing - where the kit lives, which rule covers what, which agent or command fits a request, and that checks run only when asked.
---

# Kit Core

`KIT` = `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2`. Replace KIT with that installed root before using paths, and quote shell arguments. Agents live in `KIT/agents/`, skills and slash commands in `KIT/skills/`, helper scripts in `KIT/scripts/`. Active rules sit beside the plugin under `config/rules/`.

## Rules

| Rule | Covers |
|---|---|
| `rule-01-unified-theme-system` | UI theming: one token system, Light/Dark/System |
| `rule-02-work-style` | Language, tone, deciding, finishing, reporting, approvals |
| `rule-03-code-standards` | Code organization, naming, CSS, states, errors, cleanliness |
| `rule-04-system-integration` | New systems and add-ons: Option B ERP integration |
| `rule-05-planning-and-docs` | Plan files and project documentation |
| `rule-06-security-baseline` | Auth, permissions, input, secrets, money records, uploads |

Each topic has one owner rule. If two instructions seem to conflict, the user's current message wins, then the more specific rule. In Expo/React Native, apply Rule 01's token, three-mode and accessibility parts; its CSS, `color-scheme` and hydration items do not apply.

## Checks run only when asked

Tests, lint/build runs, audits, browser inspection, screenshots, `/see`, `/test`, `/verify` and `/review` run only when the user asks. Do not run or offer them automatically after implementation. Rule 01's verification items are met by reviewing the code for token use in both themes; rendered and test runs happen only on request, and the report lists them as "not run".

## Agents
| Role | Use for |
|---|---|
| `lead` | big or cross-area tasks: split work, assign agents, integrate, final report |
| `architect` | system design, tech choices, ADRs, integration design, reviewing plans |
| `product-planner` | goals, requirements, user stories, acceptance criteria, task plans |
| `ux-designer` | flows, sitemap, screen list and states, DESIGN.md, token set |
| `frontend-engineer` | web UI: React/Next, Blade, Bootstrap, Tailwind, theming, SEO |
| `backend-engineer` | APIs, services, auth, jobs, webhooks, exports, outbox sync |
| `database-engineer` | schema, migrations, indexes, queries, seeds, data ownership |
| `mobile-engineer` | Expo/React Native/Flutter apps, offline, device features, store builds |
| `qa-engineer` | tests, test plans, code review on request |
| `debugger` | bugs, errors, crashes, regressions, measured performance problems |
| `security-engineer` | security review, threat model, authorized penetration testing |
| `devops-engineer` | servers, CI/CD, Docker, env, backups, deploy, rollback |
| `docs-writer` | README, guides, API docs, manuals, handover |
| `explorer` | read-only codebase mapping, legacy code explanation, feasibility |

Agent files are `KIT/agents/<name>.md`. Pick the agent that owns what is being changed; an agent the user names wins. Small single-area tasks go straight to that agent; use `lead` only when work spans several areas. UI defects with a known cause go to `frontend-engineer`; regressions with an unknown cause go to `debugger`. Without native delegation, do the role yourself.

## Commands

| Commands | Purpose |
|---|---|
| `/create` `/enhance` | Build new work or extend the existing project |
| `/plan` `/proplan` `/brainstorm` | Plan a feature, plan a whole system, compare approaches |
| `/debug` `/fix-ui` `/see` `/see-doc` | Diagnose defects or inspect real output (on request) |
| `/test` `/verify` `/review` | Run tests, establish evidence or review a diff (on request) |
| `/orchestrate` `/deploy` | Coordinate multi-agent work or perform an authorized release |
| `/status` `/remember` | Read progress or save requested project context |
| `/updatekit` `/doctor` | Maintain or diagnose the kit installation |

Read `KIT/skills/<command>/SKILL.md` for the selected workflow. Natural-language requests can trigger it too. Use quick-reference only when the full catalog helps.
