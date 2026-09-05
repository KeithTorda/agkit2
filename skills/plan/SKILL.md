---
name: plan
description: "/plan — Writes an implementation plan to docs/plans/{task-slug}.md without writing code. Use when the user wants a plan, task breakdown, or estimate before building, and before any new app or multi-file change."
version: 2.0.0
---

# /plan

**Input:** the text after `/plan` is the request.
**Agent:** read `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/project-planner.md`.
**Skills:** `@[skills/plan-writing]` (the plan format: file, slug, sections); `@[skills/brainstorming]` (question format); `@[skills/architecture]` only for structural decisions.

## Steps

1. Read existing context: `docs/plans/*.md`, `DESIGN.md`, project memory if loaded, and the code the request touches. This is the ANALYZE phase; phases are defined in `C:/Users/Keith/.gemini/config/rules/code-rules.md`.
2. Questions per the global `core-protocol` rule; whatever you do not ask, write into the plan's Assumptions section instead of guessing silently.
3. Write `docs/plans/{task-slug}.md` in the `plan-writing` format: Goal, Assumptions, Scope, Tasks as `- [ ]` checkboxes with an owner and a `verify:` line, Done-when. Phase names may be headings when the task spans phases.
4. Do not write code files. This command ends with the plan.
5. Report the exact path and the next command.

## Naming

Plan-file rule: the global `core-protocol` rule. Slug and path (2–4 key words, kebab-case, at most 30 characters, `docs/plans/{task-slug}.md`): `plan-writing`.

## Output

```
Plan created: docs/plans/<slug>.md
Tasks: <n> · Agents: <list> · Assumptions: <n>
Next: /create <slug> for a new app, /enhance <slug> for an existing app, or edit the plan first.
```

## Verification

- The file exists at `docs/plans/<slug>.md` and no code files changed.
- Every task has an owner and a concrete `verify:` line; Done-when includes the checklist command.
