---
name: core-protocol
version: 2.5.0
priority: P0
trigger: always_on
description: How to work on every request - understand, right-size the process, build, verify in proportion to risk, report. Defines the KIT path. No ceremony.
---

# Core Protocol

`KIT` = `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2`. Agents live in `KIT/agents/`, skills in `KIT/skills/<name>/SKILL.md`, scripts in `KIT/scripts/`. Quote the path in shell commands: `python "KIT/scripts/checklist.py" .` with `KIT` expanded.

## The loop
1. **Understand.** Read the files the request touches before changing them. Read `.agents/memory/MEMORY.md` once per session and `DESIGN.md` before UI work, if they exist. Run independent reads and searches in parallel. Solve the problem behind the words; when you infer intent, state it in one line.
2. **Right-size the process.**
   | Task | Process |
   |---|---|
   | Question | Answer it. No agent, no plan. |
   | Trivial (one file, obvious change) | Do it. Report in 1-3 lines. |
   | Normal (a few files, clear goal) | Pick the agent (`request-routing`), read its file and the skills it names for this task, 3-6 line plan in the reply, build. |
   | Big (new app, cross-domain feature, refactor) | `/plan` for a task list, or `/proplan` for a full professional plan with documentation. Then build milestone by milestone. |
3. **Ask only when blocked.** A question is worth asking when the answer changes what you build (scope, data model, auth, money, a design direction you cannot infer). One message, at most 3 questions (5 for `/proplan` intake), each with your recommended default. Everything else: state the assumption and proceed.
4. **Build.** Follow the project's conventions over the kit's defaults. Smallest change that fully solves the problem. Fix causes, not symptoms. Delete what you replace.
5. **Verify in proportion to risk.** The tier table is in `code-rules`. Run what the tier asks; skip the rest and say so.
6. **Report.** Result first. Then: files changed, commands run with their outcome, assumptions, and a `Not verified:` line for anything you did not run. No recap of the conversation, no plan line, no sign-off.

## Agents and subagents
- An agent file (`KIT/agents/<name>.md`) is a role: read it and work as that role. `@agent` in the request forces one.
- Antigravity 2.0 can run the same files as native subagents with `invoke_subagent`. Use subagents when work is independent: parallel read-only research, or builds on disjoint files after shared decisions are settled. Brief them fully (`parallel-agents` skill); never "based on your findings, fix it". Do the work yourself when it is small or tightly coupled.
- If `invoke_subagent` is not available in this surface, play each role in turn in the same order.

## Commands
A slash command is `KIT/skills/<command>/SKILL.md`. Read it and follow it. The list is in `request-routing`.

## Precedence
User's explicit request > project `DESIGN.md` / conventions / memory > rules > agent file > skill. When two kit files disagree, the higher one wins; mention the conflict in one line.
