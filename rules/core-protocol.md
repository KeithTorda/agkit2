---
name: core-protocol
version: 2.0.0
priority: P0
trigger: always_on
description: How the agent works on every request — routing to a specialist, loading skills on demand, the questions policy, the announcement line, and the plan-file rule.
---

# Core Protocol

Every task is held to `engineering-excellence` (how to think — always on) and, for code, `code-rules` (the phases and gates). This file is the mechanics: route, load, ask, announce, plan.

## Loading
- Route the request with `request-routing`, then read that agent's file: `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/<agent>.md`.
- Load a skill only when its description matches the task. Inside a skill, read `SKILL.md` first, then only the section files it points to for the current need. Never load every skill in an agent's list up front.
- Precedence: global rules → agent file → skill. A `DESIGN.md` in the project overrides design guidance in any skill.

## Questions
Ask only when the answer changes what you would build — scope, data model, security, architecture, or a design direction you cannot infer. New app or multi-file feature: ask 1–3 targeted questions in one message before planning. Bug fix, single-file change, UI tweak: proceed and state your assumptions. Never ask twice before starting; if the user says "proceed", proceed with stated defaults.

## Announcement
At most one line at the top of a code or design response: `🤖 @<agent> · skills: <a>, <b>`. It is informational, never a gate. No other announcement formats exist.

## Plan file
Required for NEW APP and COMPLEX tasks (multi-file or structural change): `docs/plans/{task-slug}.md`, kebab-case, never `plan.md`/`PLAN.md` (format: `plan-writing` skill). Simple tasks: a 1–3 line plan in the response is enough. A missing plan file never blocks a simple task.

## Phases and verification
Phases (ANALYZE → PLAN → BUILD → VERIFY), the required-vs-advisory check split, and the auto-fix policy are defined once in `code-rules`. Do not redefine them. Any UI work also applies `design-rules` (the `DESIGN.md` gate), even if that rule did not auto-load.

## Multi-agent work
Use the minimum number of agents the task needs; a single specialist is a valid outcome. File ownership per agent is defined in `agents/orchestrator.md`; the delegation method in the `parallel-agents` skill.
