---
name: enhance
description: "/enhance - Adds or changes a feature in an existing application: read the current state, scope the change, apply it with the owning specialist, verify by risk tier. Use when the user asks to add, update, extend or improve something in a project that already exists."
version: 2.5.0
---

# /enhance

**Input:** the text after `/enhance` is the change (or a `docs/plans/<slug>.md` to build).
**Agent:** the owner from the table in `KIT/agents/orchestrator.md` (`frontend-specialist`, `backend-specialist`, `mobile-developer`, `database-architect`; `performance-optimizer` for speed or bundle work). Several owners → `/orchestrate`. Undocumented or legacy code → read `KIT/agents/code-archaeologist.md` first.
**Read when:** feature analysis → `KIT/skills/app-builder/feature-building.md`; performance → `KIT/skills/performance-profiling/SKILL.md`; plus the owner's own skills for the task.

## Steps

1. **Current state.** Read the code the change touches, `DESIGN.md`, `.agents/memory/MEMORY.md`, and any plan in `docs/plans/`. `python "KIT/scripts/session_manager.py" info .` gives the stack and features when the project is unfamiliar.
2. **Scope.** One file or an obvious change: do it. A few files: 3-6 line plan in the reply. Big or multi-session: `docs/plans/<slug>.md` (`plan-writing`), or `/proplan` if it is really a new subsystem. Ask only if blocked (max 3 questions, each with a default).
3. **Conflicts.** If the request contradicts the project (for example "use Firebase" in a Postgres app), say so once and offer the consistent option; the user decides.
4. **Design.** UI changes follow `DESIGN.md`. Missing: new page-level UI → write a short one first (`design-spec`); a component change → match the existing styles and say so. Bug fixes need neither.
5. **Apply.** Smallest change that fully solves it; update every importer and caller in the same task; delete what you replace. For performance work, measure a baseline first and keep the change only if the numbers improve.
6. **Verify by tier** (`code-rules`): tier 1 runs the project's lint/types/tests for touched files; tier 2 (auth, money, permissions, migrations, shared utilities) adds `checklist.py . --full`, tests for the logic, and `/review`. When a dev server is running and layout changed, look at it.

## Output

```markdown
<What now works, one or two lines>
Files: <new / updated>
Checks: <commands> → <outcome>
See it: <route or command>
Assumptions: <if any>
Not verified: <what did not run>
```
