---
name: enhance
description: "/enhance — Adds or changes a feature in an existing application: understand the current state, scope the change, apply it with the owning specialist, verify. Use when the user asks to add, update, extend, or improve something in a project that already exists."
version: 2.0.0
---

# /enhance

**Input:** the text after `/enhance` is the change.
**Agent:** the owning specialist from the ownership table in `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/orchestrator.md` (for example `frontend-specialist.md`, `backend-specialist.md`, `mobile-developer.md`, `database-architect.md`); `performance-optimizer.md` when the change is a speed or bundle-size optimization. Read `orchestrator.md` itself when the change spans more than one owner, and `code-archaeologist.md` first when the codebase is undocumented or legacy.
**Skills:** `@[skills/app-builder]` (`feature-building.md` only), `@[skills/clean-code]`, `@[skills/verify-changes]`; `@[skills/performance-profiling]` for optimization work; the specialist's own skills as the task needs them.

## Steps

1. **Current state.** `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/session_manager.py info .`, then read `docs/plans/*.md`, `DESIGN.md`, and the code paths the change touches. Apply project memory if loaded.
2. **Scope.** Bug fix, single-file change, or UI tweak: proceed and state assumptions. Multi-file or structural change: write `docs/plans/{task-slug}.md` (format: `plan-writing`) and show the affected files and scope before editing. Questions per the global `core-protocol` rule.
3. **Conflicts.** Warn when the request contradicts the project (for example "use Firebase" in a Postgres app) and offer the consistent option.
4. **Design** (global `design-rules` gate). UI changes follow `DESIGN.md`. If it is missing: new page-level UI → create `DESIGN.md` first (`design-spec`, by `frontend-specialist` or, for a mobile-only app, `mobile-developer`); component-level change → infer from existing styles, say so, offer to create it; bug fixes and trivial tweaks skip the gate.
5. **Apply.** Edit the file and all dependents in the same task (`clean-code`). Keep each change small; commit per change when the project uses git and the user expects commits. For a performance change, measure before optimizing: capture a baseline with `performance-profiling`, then re-measure after — keep the change only if the numbers improve, and never trade clarity for an unmeasured gain.
6. **Verify.** Run the affected tests and `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .`; when a dev server is running, confirm the change in the app (hot reload).

## Output

- What changed: files grouped by new / updated, assumptions made, checklist result.
- How to see it (route or command) and suggested follow-ups (`/test`, `/verify`).

## Verification

- Every edited file's importers still compile; no broken imports.
- Required checks pass; a plan file exists when the change was multi-file.
