---
name: orchestrate
description: "/orchestrate - Coordinates specialist subagents on a multi-domain task, or executes one milestone of a /proplan roadmap (/orchestrate docs/proplan/<slug> M1): settle shared decisions, delegate by file ownership, verify each task with evidence, integrate, report. Use when work spans backend, frontend, database, tests or security, or to build a planned milestone."
version: 2.5.0
---

# /orchestrate

**Input, two forms:**
- `/orchestrate <task>` - an ad-hoc multi-domain task.
- `/orchestrate docs/proplan/<slug> M<n>` - execute milestone `M<n>` from that plan's `10-roadmap.md`. A path to a `/plan` file (`docs/plans/<slug>.md`) works the same way, task by task.

**Agent:** `KIT/agents/orchestrator.md` (file-ownership table, trust boundary).
**Read now:** `KIT/skills/parallel-agents/SKILL.md` (runtime, briefs, budgets, synthesis). For a `/proplan` folder also `KIT/skills/proplan/SKILL.md` (document set, ID scheme, roadmap format).

Use the fewest agents the work needs. A single specialist is a valid outcome; if the task is one domain, hand it to that agent and stop orchestrating.

## Form 1: ad-hoc task

1. **Understand.** Read the request, `.agents/memory/MEMORY.md`, `DESIGN.md`, and the code the task touches. Use the `research` built-in subagent if available in your Antigravity version (otherwise `explorer-agent`) in parallel for independent questions about an unfamiliar codebase.
2. **Settle shared decisions** (data model, API contract, auth, design tokens) before any writer starts. Ask the user only if the answer changes what gets built (max 3 questions, each with a default).
3. **Plan.** A few tasks: list them in the reply with owner and verify line. More than about six tasks or several sessions: `project-planner` writes `docs/plans/<slug>.md` (`plan-writing` format). A whole system: suggest `/proplan` instead.
4. **Build.** `invoke_subagent` each owner with a full brief (`parallel-agents`). Parallel only for disjoint files with no open decision; chains (schema → API → UI → tests) run in order. Workspace per `parallel-agents`: `share` for disjoint files, `branch` worktrees for parallel code writers in a git repo, otherwise one writer at a time.
5. **Verify and integrate.** Check each result against its verify line; merge; run the checks the highest-risk change calls for (`code-rules` tier).
6. **Report** with the synthesis template in `parallel-agents`.

## Form 2: execute a /proplan milestone

1. **Load.** Read `docs/proplan/<slug>/00-overview.md` and `10-roadmap.md`. Find `M<n>` and its T-ids. For each task note its `owner`, `depends`, `verify`, files, estimate, and the IDs it cites (R-, NFR-, API-, ADR-, TC-). Read only the doc sections those IDs point to.
2. **Gate.** If `REVIEW.md` has an open blocker for this milestone, or a task depends on a T-id outside the milestone that is not done, stop and report it. Do not build around it.
3. **Order.** Build waves from `depends`: a task is ready when all its dependencies are done. Within a wave, parallel only where file sets are disjoint.
4. **Delegate.** For each ready T-id, `invoke_subagent` its `owner` with a brief carrying: the task text, the cited IDs with their doc excerpts, files it may write, its `verify` line as the acceptance check, and its estimate as the budget. Without `invoke_subagent`, do the tasks yourself as each owner in wave order.
5. **Mark done only with evidence.** A task is done when its `verify` line was run and passed. Update its status in `10-roadmap.md` (the marker format is defined in the `proplan` skill; typically `- [ ]` → `- [x]`) and add a short evidence note (command and result, or test name). Failed or partial tasks stay open with a one-line reason. Never tick a task because the code "should" work.
6. **Integrate.** Merge, then run the checks the milestone's highest-risk task calls for (`code-rules` tier 1-3). A failure goes back to the owning task.
7. **Update plan status.** In `00-overview.md`: milestone state (not started / in progress / done / blocked), date, tasks done out of total, open items. If a task changed a design decision, update the ADR or doc it came from (or flag it for the owner), then run `python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --write-traceability`; never edit `TRACEABILITY.md` by hand.
8. **Report** (below).

## Output

```markdown
## M<n> <milestone name>: <done | partial | blocked>
Tasks: <done>/<total>

| T-id | Owner | Status | Evidence |
|---|---|---|---|
| T-003 | database-architect | done | `npx prisma migrate dev` ok; `npm test schema` 8/8 |
| T-005 | frontend-specialist | open | verify failed: empty state missing on /orders |

Integrated checks: <commands> → <outcome>
Plan files updated: 10-roadmap.md, 00-overview.md
Decisions made: <material ones only>
Not verified: <what did not run and why>
Next: <next ready tasks or /orchestrate docs/proplan/<slug> M<n+1>>
```

## Rules

- Briefs name file, line and change; never "based on your findings, fix it".
- Do not report a worker's result before it returns.
- Stop and report when an agent repeats a failing action, crosses its ownership boundary, or needs an approval you do not have.
- No deploy, destructive migration or production data change without the user's approval, even if the roadmap lists it.
