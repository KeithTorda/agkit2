---
name: orchestrate
description: "/orchestrate - Coordinate work that spans several areas, or execute a plan or milestone, by assigning owners, settling shared contracts and integrating the result. Pass a task, a plan path or a proplan milestone."
version: 3.2.0
---

# /orchestrate

Run multi-agent work as `KIT/agents/lead.md` and deliver one integrated result.

## Input

- A task description
- `docs/plans/<yyyy-mm-dd>-<slug>.md`
- `docs/proplan/<slug> M<n>` (one milestone)

## Steps

1. Read the plan (if any) and the source it touches. Pick the tasks to run now and note their dependencies and "Done when" or verify lines.
2. Pull the excerpts each task needs: requirement, API, ADR, accepted style answer. Settle shared contracts (names, payloads, roles, tokens) before anyone writes code.
3. Assign each task to its owning agent with explicit writable paths. Follow `KIT/skills/parallel-agents/SKILL.md` for briefs. Run tasks in parallel only when their files and inputs do not overlap.
4. Without delegation tools, do the roles one after another and say so in the report.
5. When a task is blocked by a missing decision or a conflicting contract, pause that task and keep running unrelated ready work. Ask the user once about the blocker.
6. Review each result. Fix mismatched names, payloads, permissions and states, then integrate in dependency order.
7. Update the plan: tick finished tasks; add "not verified" next to tasks with no check run. In proplan roadmaps change `- [ ]` to `- [x]` with a short note.
8. For proplan sets, keep IDs stable and regenerate TRACEABILITY.md with `python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --write-traceability` instead of editing generated rows.
9. Run `KIT/skills/verify-changes/SKILL.md` only if the user asked for verification (kit-core).

Avoid treating a plan task as approval for production deploys, data deletion or other actions listed in rule-02-work-style.

## Output

Report in the rule-02 shape: integrated behavior, task states, decisions, checks run or not run, and remaining blockers.

## Before you finish, check

- [ ] All worker outputs are merged and their contracts agree.
- [ ] The plan file reflects the real state of each task.
- [ ] Blocked tasks and their reasons are listed.
- [ ] Nothing is reported as verified unless a check ran.
