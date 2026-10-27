---
name: enhance
description: "/enhance - Add a feature or improve something in an existing project while keeping its contracts and conventions. Use it for features and maintenance; use /create for a brand-new project."
version: 3.2.0
---

# /enhance

Add or improve behavior inside the current codebase and leave it consistent.

## Steps

1. Read the request, the files you will touch, their callers, related tests and any DESIGN.md, README or `docs/plans/` notes.
2. Pick the owning agent from the kit-core agent table. Use `KIT/skills/parallel-agents/SKILL.md` only when the change spans several areas.
3. Write the change as a user outcome in one or two lines, then list what it touches: callers, types, routes, data, UI states, translations, docs.
4. Ask once only when a missing product or permission decision changes the result. Decide routine details from how the project already works.
5. Plan to fit: a short task list for small work, `KIT/skills/plan-writing/SKILL.md` for work that spans sessions.
6. For a redesign or new visual direction, ask one short style question only when the direction is truly unclear. Theme work follows rule-01-unified-theme-system; update DESIGN.md when the design system changes.
7. Implement the full slice: update dependent contracts, remove replaced code paths, keep the existing stack and libraries (rule-03-code-standards).
8. For integration changes between systems, keep table ownership and the outbox/webhook flow intact (rule-04-system-integration).
9. For performance work, measure before and after with `KIT/skills/performance-profiling/SKILL.md`.

## Stack notes

- Laravel: add a migration for schema changes; never edit a migration that already ran in production.
- Next.js: keep server/client boundaries as they are unless the change needs a move.
- Expo: check both platforms' behavior in code for any native API you add.

## Output

Report in the rule-02 shape with the changed files and routes. Tests and browser checks are listed as "not run" unless the user asked for them (kit-core).

Avoid unrelated refactors and new libraries without a concrete reason.

## Before you finish, check

- [ ] The change is integrated into every caller and route, not left as a proposal.
- [ ] Replaced code and CSS are deleted.
- [ ] Loading, empty, error and success states exist for touched screens.
- [ ] Docs that describe the changed behavior are updated.
