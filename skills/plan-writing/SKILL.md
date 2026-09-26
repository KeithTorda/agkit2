---
name: plan-writing
description: The kit's task-list plan format, docs/plans/<slug>.md - goal, assumptions, scope, and 5-12 checkbox tasks each with an owner and a verify line that can fail. Use for /plan, for big features or multi-session work that needs a breakdown, and whenever a plan is longer than a few lines.
version: 2.5.0
---

# Plan Writing

When to plan at all is in `core-protocol`: trivial work gets no plan, normal work gets 3-6 lines in the reply, big work gets a file. This skill is what goes in the file.

For a whole system (goals, requirements, architecture, data, API, UX, security, tests, roadmap as a document set), use `/proplan` (`KIT/skills/proplan/SKILL.md`). This format is the lightweight one.

## File and slug

- Path: `docs/plans/<slug>.md`. Create `docs/plans/` if missing; in a monorepo use the repository root.
- Slug: 2-4 key words, kebab-case, at most 30 characters (`ecommerce-cart`, `dark-mode`, `auth-fix`). Never `plan.md` or `PLAN.md`; the slug lets several plans coexist.
- Continue an existing plan for the same task instead of starting a new one.

## Principles

| Principle | Wrong | Right |
|---|---|---|
| Short | 50 tasks with sub-sub-tasks | 5-12 tasks, one line each; more → split the plan or use `/proplan` |
| Specific | "Set up project" | "Run `npx create-next-app@latest shop --ts --tailwind --app --src-dir`" |
| Specific | "Add authentication" | "Install Better Auth; create `src/lib/auth.ts` and `app/api/auth/[...all]/route.ts`" |
| Verifiable | "Verify the component works" | "Dev server: toggle dark mode on /settings, background switches, choice survives reload" |
| Ordered | Unordered list | Dependencies first, parallel work marked, verification last |

Content follows the task type. New project: stack decision, MVP scope, file structure. Feature: affected files, new dependencies, how to verify. Bug fix: root cause, file and line, how to test the fix. Multi-agent work: an owner per task from the ownership table in `KIT/agents/orchestrator.md`.

## A good task vs a vague one

Every task is a `- [ ]` checkbox with an **owner** and a **verify line that can fail**: a command or observation with a pass/fail signal you could paste back. If you cannot write one, split the task until you can.

```text
Vague:  - [ ] Add login
        (no owner, no files, "verify: it works")

Sharp:  - [ ] Add email/password login with Better Auth (owner: backend-specialist)
        - files: src/lib/auth.ts, app/api/auth/[...all]/route.ts
        - verify: POST /api/auth/sign-in with a seeded user → 200 + session cookie;
          wrong password → 401
```

## Format

```markdown
# <Task name>

## Goal
One sentence: what exists when this is done, and for whom.

## Assumptions
- <decisions made without asking: stack, platform, data model - one-line reason each>

## Scope
- In: ...
- Out: ... (explicit non-goals)

## Tasks
- [ ] 1. <specific action> (owner: database-architect) - verify: <command or observation that fails if wrong>
- [ ] 2. <specific action> (owner: backend-specialist; after 1) - verify: ...
- [ ] 3. <specific action> (owner: frontend-specialist; parallel with 2) - verify: ...
- [ ] 4. Tests for the logic above (owner: test-engineer) - verify: suite green

## Done when
- [ ] <main success criterion, observable>
- [ ] Checks for the highest-risk task pass per `code-rules` tier (tier 1: project lint/types/tests; tier 2: `checklist.py . --full`, tests, /review)
```

Rules for tasks:

- Dependencies inline (`after 1`) are hard blockers only; tasks with disjoint files and no blocker are marked `parallel with`.
- Verification is the last task. Name the tier the plan needs instead of a fixed gate.
- Phase headings (`## Build`, `## Verify`) may group tasks in a long plan; the sections keep this order.
- Mark `[x]` only after the verify line passed. The plan is the progress record `/status` and `/orchestrate` read.
