---
name: plan
description: "/plan - Writes a task-list plan to docs/plans/<slug>.md without writing code: goal, assumptions, scope, tasks with owner and verify line. Use when the user wants a plan, breakdown or estimate before building a feature or a multi-file change. For a whole system with full documentation, use /proplan."
version: 2.5.0
---

# /plan

**Input:** the text after `/plan` is the request.
**Agent:** `KIT/agents/project-planner.md`.
**Read now:** `KIT/skills/plan-writing/SKILL.md` (the format). Read `KIT/skills/brainstorming/SKILL.md` only if you need to ask questions.

For a new system, a client project, or anything that needs requirements, architecture, data model and a milestone roadmap as documents, use `/proplan` (`KIT/skills/proplan/SKILL.md`); `/plan` is the lightweight task list.

## Steps

1. Read existing context: `docs/plans/*.md`, `DESIGN.md`, `.agents/memory/MEMORY.md`, and the code the request touches.
2. Ask only if blocked (max 3 questions, each with a default). Everything you did not ask goes under Assumptions.
3. Write `docs/plans/<slug>.md` in the `plan-writing` format.
4. No code files. The command ends with the plan.

## Output

```
Plan: docs/plans/<slug>.md
Tasks: <n> · Owners: <list> · Assumptions: <n>
Next: /enhance <slug> or /orchestrate docs/plans/<slug>.md, or edit the plan first.
```
