---
name: create
description: "/create — Scaffolds a new application end to end: questions, plan file, DESIGN.md, template-based build with specialist agents, verification, and a running dev server. Use when the user asks for a new app, site, API, or project from scratch."
version: 2.0.0
---

# /create

**Input:** the text after `/create` describes the app.
**Agents:** read `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/project-planner.md` for steps 1–2, then `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/orchestrator.md` for steps 3–6.
**Skills:** `@[skills/app-builder]` (read `project-detection.md`, then only the matching `templates/<name>/TEMPLATE.md`), `@[skills/brainstorming]` (question format), `@[skills/plan-writing]`, `@[skills/design-spec]` (UI projects), `@[skills/verify-changes]`.

## Steps

1. **Questions.** The questions policy is the global `core-protocol` rule's — a new app is the case where you ask before planning; the usual gaps to close are app type, core features, and target users. Ask them in one message; if the user says "proceed", build with stated defaults.
2. **Detect and plan.** Pick the project type and template (`app-builder/project-detection.md`). `project-planner` writes `docs/plans/{task-slug}.md` in the `plan-writing` format (stack and structure under Assumptions, checkbox tasks with owner and verify line). Present it in Planning Mode; continue to the build when the user approves or asked to proceed without review.
3. **Create DESIGN.md (UI projects).** `frontend-specialist` (web) or `mobile-developer` (mobile-only app) creates `DESIGN.md` at the project root with `design-spec` before any UI code — not `project-planner`. Skip for API-only and CLI projects.
4. **Build.** Follow `app-builder/agent-coordination.md`: `database-architect` (schema) → `backend-specialist` (API) → `frontend-specialist` or `mobile-developer` (UI against `DESIGN.md` tokens). File ownership is the table in `agents/orchestrator.md`. Use the minimum number of agents the task needs. A single specialist is a valid outcome of orchestration.
5. **Verify.** `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .` — required checks pass before "done" (auto-fix policy: global `code-rules` rule).
6. **Run.** Start the dev server with the template's command and report the URL and how to stop it.

## Output

- Plan file path, template used, tech stack summary.
- Files created (grouped by agent), checklist result, dev server URL.
- Suggested next steps: `/enhance`, `/test`, `/deploy preview`.

## Verification

- `docs/plans/{task-slug}.md` and, for UI apps, `DESIGN.md` exist.
- `checklist.py` reports no failed required checks.
- The dev server starts and the home route responds.
