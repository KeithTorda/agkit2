# Agent Coordination

> Order of specialist agents when App Builder creates a new application. Ownership per file area is the table in `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/orchestrator.md`; concurrency rules are in `@[skills/parallel-agents]`.

## Pipeline

| Step | Agent or gate | Parallel | Needs | Produces |
|---|---|---|---|---|
| 0 | Questions (global `core-protocol` rule; format in `@[skills/brainstorming]`) | – | request | answers or stated defaults |
| 1 | `project-planner` | – | answers | `docs/plans/{task-slug}.md` in the `@[skills/plan-writing]` format (required for a new app) |
| 2 | `frontend-specialist` (web) or `mobile-developer` (mobile-only app) with `@[skills/design-spec]` | – | plan | `DESIGN.md` at the project root, required before any UI code; skip for API-only and CLI projects |
| 3 | `database-architect` | – | plan | schema, migrations, seed data |
| 4 | `backend-specialist` | – | schema | Route Handlers (`app/api/**`), Server Actions (`actions/**`), `lib/server/**` and `lib/dal.ts`, `middleware.ts`/`proxy.ts`; standalone APIs per `tech-stack.md` |
| 5 | `frontend-specialist` (web) or `mobile-developer` (mobile) | with 4 once the API contract exists | `DESIGN.md`, API contract | `app/**` pages, layouts, and components (except the backend paths in step 4) built from `DESIGN.md` tokens, calling the Server Actions and DAL functions |
| 6 | `test-engineer`; `security-auditor` when auth, payments, or uploads exist | yes | code | tests, audit findings |
| 7 | `devops-engineer` | – | all code | env setup, CI, preview deployment or dev server, health check and URL |

Skip any step the app does not need; a static site needs steps 0–2, 5, 6. Mobile apps with a backend use `backend-specialist` for the backend.

## Gates

- The plan file exists before specialists start (plan-file rule: global `core-protocol`; format: `@[skills/plan-writing]`).
- `DESIGN.md` exists before UI components or pages are written (global `design-rules` gate; format: `@[skills/design-spec]`).
- Each specialist edits only its owned file areas and reports changed paths; the coordinator integrates.
- Before "done": `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .` (required checks pass; auto-fix policy: global `code-rules` rule).

## Context passed to every agent

The original request, the user's answers and stated defaults, the plan file path, `DESIGN.md` (UI work), what previous agents produced (schema, API contract), and the files the agent owns. Fields: the delegation template in `@[skills/parallel-agents]`.
