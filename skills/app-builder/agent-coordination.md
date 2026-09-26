# Agent Coordination

Which specialists build a new app, in what order. File ownership is the table in `KIT/agents/orchestrator.md`; runtime, briefs and concurrency are in `KIT/skills/parallel-agents/SKILL.md`. Use the fewest agents the app needs; a small site is one `frontend-specialist` pass, done by you.

## Pipeline

| Step | Agent | Parallel | Needs | Produces |
|---|---|---|---|---|
| 0 | you (questions only if blocked, max 3 with defaults) | - | request | answers or stated defaults |
| 1 | `project-planner`, or `/proplan --lite` for a bigger app | - | answers | `docs/plans/<slug>.md` or `docs/proplan/<slug>/`; a short in-reply plan for a small site |
| 2 | `frontend-specialist` (web) or `mobile-developer` (mobile-only) with `design-spec` | with 3 | brief | `DESIGN.md` at the project root; skip for API-only and CLI |
| 3 | `database-architect` | with 2 | plan | schema, migrations, seed data |
| 4 | `backend-specialist` | - | schema | Route Handlers, Server Actions, `lib/dal.ts`, `proxy.ts`, auth; or the standalone API; or Laravel `app/**`, `routes/**` |
| 5 | `frontend-specialist` or `mobile-developer` | with 4 once the API contract is written down | `DESIGN.md`, contract | pages, layouts, components from `DESIGN.md` tokens |
| 6 | `test-engineer`; `security-auditor` when auth, payments, uploads or personal data exist | yes | code | tests for the risky logic, audit findings |
| 7 | `devops-engineer` (only when deploying) | - | all code | env setup, CI, preview deploy, health check |

Skip steps the app does not need: a static site is steps 0, 2, 5 and a build check. Mobile apps with a backend use `backend-specialist` for it.

## Handoffs

- A written contract (schema, API shape, `DESIGN.md` tokens) exists before the agents that consume it start; parallel work across an open decision causes rework.
- Each specialist edits only its owned areas and returns changed paths, commands run and their output.
- You integrate, then verify by the highest-risk part of the app (`code-rules` tier).

## Brief contents

The original request, answers and defaults, the plan path, `DESIGN.md` for UI work, what earlier agents produced (schema, contract), the files the agent owns, and how to verify. Template: `parallel-agents`.
