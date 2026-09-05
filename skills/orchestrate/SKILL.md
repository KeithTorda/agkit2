---
name: orchestrate
description: "/orchestrate — Coordinates specialist subagents for a multi-domain task: parallel research, one plan, parallel build by file ownership, single verification, one synthesis report. Use when a task spans backend, frontend, database, tests, or security, or needs several perspectives."
version: 2.0.0
---

# /orchestrate

**Input:** the text after `/orchestrate` is the task.
**Agent:** read `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/orchestrator.md` (ownership table, trust boundary, budgets).
**Skills:** `@[skills/parallel-agents]` (phase concurrency, worker briefs, synthesis report), `@[skills/plan-writing]`.

## Steps

Phases are defined once in `C:/Users/Keith/.gemini/config/rules/code-rules.md`; this command maps subagents onto them.

1. **ANALYZE** — read-only research. Run `explorer-agent`, `security-auditor`, or domain specialists in parallel through Agent Manager; each returns findings with file references. Questions per the global `core-protocol` rule. If subagents are unavailable in this Antigravity surface, use the single-session fallback in `parallel-agents` (act as each specialist in turn, ownership order, writers sequentially) — the phases and ownership below still hold.
2. **PLAN** — single-threaded. Synthesize the research yourself; for a multi-file task write `docs/plans/{task-slug}.md` (`project-planner` or Planning Mode, format in `plan-writing`) with checkbox tasks, owners, verify lines, and dependencies. No writers before the plan exists.
3. **BUILD** — parallel only where file ownership does not overlap (table in `agents/orchestrator.md`). Dependency chains (schema → API → UI) run in order. Every brief follows the delegation template in `parallel-agents`: full context, allowed paths, expected artifact, verification, stop conditions.
4. **VERIFY** — `test-engineer` runs the integrated verification: `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .` plus the change-specific checks from `verify-changes`; the orchestrator reviews the report and routes required-check failures back to the owner.
5. **Synthesize** with the report template in `parallel-agents`; add your own analysis, not a paste of worker output.

Use the minimum number of agents the task needs. A single specialist is a valid outcome of orchestration.

## Output

The synthesis report from `parallel-agents`: contributions with evidence, integrated result, security and compatibility notes, remaining decisions.

## Rules

- Never write "based on your findings, fix it"; state file, line, and change.
- Do not report a worker's result before it has returned.
- Stop and report when an agent repeats a failing action, crosses its ownership boundary, or needs an approval you do not have.

## Verification

- Every dispatched agent appears in the report with its artifact and evidence.
- Required checks pass on the integrated code, not only inside isolated worktrees.
- No two agents wrote the same file.
