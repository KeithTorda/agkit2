---
name: status
description: "/status — Summarizes project health without changing anything: stack and file counts, recent changes, required-check state, open plan tasks, memory, and running subagents. Use when the user asks where things stand, what is done, or what is pending."
version: 2.0.0
---

# /status

**Input:** optional path after `/status` (default `.`).
**Agent:** none; no specialist persona is needed.
**Skills:** `@[skills/memory-system]` only if the user asks what is remembered.

Read-only. `/status` reports state; it never edits, deploys, or probes ports, and it does not run the check gate — that is `/verify`.

## Steps

1. **Project.** Run `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/session_manager.py status .` for name, stack, detected features, and file count (`info` gives the JSON form if a later step needs it).
2. **Recent changes.** `git log --oneline -10` and `git status --short` for uncommitted work. Skip with a note if the project is not a git repo.
3. **Checks.** Report the last fast-gate result if `checklist.py` ran this session; otherwise say checks have not run this session and point to `/verify`. Do not run the gate here.
4. **Open items.** List `docs/plans/*.md` (format: `plan-writing`); for each, count `- [x]` and `- [ ]` tasks and name the next open task.
5. **Memory.** Report whether `<project>/.agents/memory/MEMORY.md` exists and how many entries it has; do not recite entries unless asked.
6. **Agents.** List subagents running or waiting in Agent Manager for this workspace, with their current task. When subagents are unavailable in this Antigravity surface (single-session mode, see `parallel-agents`), report `none (single-session mode)`.
7. **Dev server.** Report its URL only if one was started this session.

## Output

```
=== Project ===
Name: <name> · Path: <path> · Stack: <detected>
Features: <list> · Files: <total>

=== Recent changes ===
<hash> <subject>   (git log --oneline -10)
Uncommitted: <n> files   (or: clean | not a git repo)

=== Checks ===
Required: pass | fail | not run this session (→ /verify)

=== Open items ===
docs/plans/<slug>.md — 4/7 done · next: <task>

=== Memory ===
.agents/memory/MEMORY.md — 12 entries   (or: not created; use /remember)

=== Agents ===
frontend-specialist — dashboard components (running)
test-engineer — waiting on API   (or: none (single-session mode))

=== Dev server ===
http://localhost:3000 (started this session) | none
```

## Verification

- Every number comes from a command or file read in this session; no estimates.
- Missing pieces are reported as missing, not skipped; the check gate was not run from here.
