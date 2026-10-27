---
name: plan
description: "/plan - Write or update a lightweight plan file for a bounded feature, fix or multi-file change, without writing code. Use /proplan instead for a whole new system."
version: 3.2.0
---

# /plan

Produce one executable plan file per rule-05-planning-and-docs, then stop unless implementation was also requested.

## Steps

1. Act as `KIT/agents/product-planner.md` and follow `KIT/skills/plan-writing/SKILL.md`.
2. Look in `docs/plans/` for an existing plan on the same work. If one exists, update it and add a "Changes" note instead of creating a new file.
3. Read the relevant source and accepted decisions so the plan names real files, tables and routes.
4. Write the goal, scope in/out, decisions, and assumptions. Ask once only for a decision that changes the plan.
5. Break the work into steps, each with an owner agent, files/areas, and a checkable "Done when".
6. If the work creates a new system or add-on, include table ownership and sync design (rule-04-system-integration).
7. List risks and open questions. Leave final visual tokens to the design step when the style is still undecided.
8. Save to `docs/plans/<yyyy-mm-dd>-<slug>.md`.
9. If the work turns out to need goals, architecture, API and roadmap documents, switch to `/proplan` and say why in one line.

## Output

In chat: a 3-6 line summary, the file path, key decisions, and the first step to execute. For a planning-only request, stop there. If the user asked to plan and build, continue into implementation once blocking questions are answered.

## Before you finish, check

- [ ] The plan is saved as a `.md` file and the path is in the reply.
- [ ] Every step has an owner and a checkable "Done when".
- [ ] Open questions are listed, not guessed.
- [ ] No code was written for a planning-only request.
