---
name: plan-writing
description: Writes short, specific, verifiable implementation plans as docs/plans/{task-slug}.md — the kit's only plan format (slug, sections, checkbox tasks each with an owner and a verify line that can fail). Use for new apps and multi-file or structural changes, for /plan, and whenever work needs a task breakdown before building.
version: 2.0.0
---

# Plan Writing

This skill owns the plan-file format. `core-protocol`, `code-rules`, `project-planner`, `/plan`, `/create`, `/enhance`, `/orchestrate`, and `/status` all point here for it.

*When* a plan file is required — NEW APP and COMPLEX tasks only; simple tasks get a 1–3 line plan in the response, and a missing plan file never blocks one — is the `core-protocol` rule. Follow it there. This file is what goes in the file once one is needed.

## File and slug

- Path: `docs/plans/{task-slug}.md`. Create `docs/plans/` if missing; in a monorepo use the repository root, not a package folder. Never `plan.md` or `PLAN.md` — the slug is what makes plans findable and lets several coexist.
- Slug: 2–4 key words from the request, kebab-case, at most 30 characters (`ecommerce-cart.md`, `dark-mode.md`, `auth-fix.md`).
- Continue an existing plan for the same task instead of starting a new one.

Antigravity's Planning Mode is the PLAN phase; the phases (ANALYZE → PLAN → BUILD → VERIFY) are defined in `C:/Users/Keith/.gemini/config/rules/code-rules.md` and may head sections inside a plan.

## Principles

| Principle | Wrong | Right |
|---|---|---|
| Short | 50 tasks with sub-sub-tasks | 5–12 tasks, one line each; more → split into several plans |
| Specific | "Set up project" | "Run `npx create-next-app@latest`" |
| Specific | "Add authentication" | "Install Better Auth; create `src/lib/auth.ts` and `app/api/auth/[...all]/route.ts`" |
| Verifiable | "Verify the component works" | "Run the dev server, toggle dark mode, background switches" |
| Ordered | Unordered list | Dependencies first, parallel work marked, verification last |

Content follows the task type — new project: stack decision, MVP scope, file structure. Feature: affected files, new dependencies, how to verify. Bug fix: root cause, file and line, how to test the fix. Multi-agent work: an owner per task (ownership table in `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/orchestrator.md`).

## A good task vs a vague one

Every task is a `- [ ]` checkbox carrying an **owner** and a **verify line that can actually fail** — one that names a command or observation with a concrete pass/fail signal you could paste back. If you cannot write one, the task is too vague; split it until you can.

```text
Vague:  - [ ] Add login
        (no owner, no files, "verify: it works" — nothing to run, nothing that can fail)

Sharp:  - [ ] Add email/password login with Better Auth (owner: backend-specialist)
        - files: src/lib/auth.ts, app/api/auth/[...all]/route.ts
        - verify: POST /api/auth/sign-in with a seeded user → 200 + session cookie;
          wrong password → 401
```

The sharp version names the owner, the exact files, and a check whose failure is observable — including the negative case.

## Sections (the only format)

```markdown
# <Task name>

## Goal
One sentence: what exists when this is done, and for whom.

## Assumptions
- <decisions made without asking: stack, platform, data model — one-line reason each>

## Scope
- In: ...
- Out: ... (explicit non-goals)

## Tasks
- [ ] 1. <specific action> (owner: database-architect) — verify: <command or observation that fails if wrong>
- [ ] 2. <specific action> (owner: backend-specialist; after 1) — verify: ...
- [ ] 3. <specific action> (owner: frontend-specialist; parallel with 2) — verify: ...
- [ ] 4. Tests for the logic above (owner: test-engineer) — verify: suite green

## Done when
- [ ] <main success criterion>
- [ ] `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .` — required checks pass
```

Rules for the tasks:

- Dependencies are stated inline (`after 1`) and are hard blockers only; tasks with disjoint files and no blocker are marked `parallel with`.
- Verification is always the last task; `Done when` includes the checklist command.
- Phase names (`## BUILD`, `## VERIFY`) may group the tasks when the plan spans phases; the sections above stay in this order.
- Mark `[x]` only after the verify line passed; the plan is the progress record `/status` reads.
