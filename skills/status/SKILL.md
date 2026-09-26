---
name: status
description: "/status - Read-only summary of where a project stands: stack, recent and uncommitted changes, last check result, open /plan tasks, /proplan milestones and task progress, memory, running subagents, dev server. Use when the user asks where things stand, what is done, or what is next."
version: 2.5.0
---

# /status

**Input:** optional path after `/status` (default `.`).
**Agent:** none.

Read-only. `/status` reports; it never edits, deploys, probes ports, or runs the check gate (that is `/verify`). Run the independent reads below in parallel.

## Steps

1. **Project.** `python "KIT/scripts/session_manager.py" status .` for name, stack, detected features and file count.
2. **Changes.** `git log --oneline -10` and `git status --short`. Not a git repo: say so.
3. **Checks.** Report the last `checklist.py` or test result from this session. Nothing ran: say "not run this session" and point to `/verify`.
4. **Plans (`/plan`).** For each `docs/plans/*.md`: count `- [x]` and `- [ ]` tasks, name the next open task.
5. **Proplans (`/proplan`).** For each `docs/proplan/*/10-roadmap.md`:
   - per milestone: tasks done out of total, and state (done / in progress / not started / blocked);
   - the next ready T-id (open, all `depends` done) with its owner;
   - open blockers in that folder's `REVIEW.md`, if any.
   Read the status marker as the `proplan` skill defines it (checkbox `- [x]`/`- [ ]`, or a `status:` field). Use the milestone state in `00-overview.md` only if the roadmap has none, and say which source you used.
6. **Memory.** Whether `.agents/memory/MEMORY.md` exists and how many entries it has; do not recite entries unless asked.
7. **Agents.** Subagents running or waiting for this workspace, with their current task. None or no `invoke_subagent` in this surface: `none`.
8. **Dev server.** Its URL only if one was started this session.

## Output

```
Project   <name> · <stack> · <n> files · <path>
Changes   <hash> <subject> (last 3) · uncommitted: <n> files | clean | not a git repo
Checks    pass | fail (<what>) | not run this session → /verify

Plans
  docs/plans/<slug>.md          4/7 · next: <task>

Proplans
  docs/proplan/<slug>/          M1 done 6/6 · M2 in progress 3/8 · M3 not started 0/5
    next ready: T-014 <title> (backend-specialist)
    review blockers: none | <n> open (REVIEW.md)

Memory    .agents/memory/MEMORY.md, 12 entries | not created (/remember)
Agents    frontend-specialist: dashboard components (running) | none
Dev       http://localhost:3000 | none
```

Every number comes from a command or file read in this session. A missing piece is reported as missing, not skipped.
