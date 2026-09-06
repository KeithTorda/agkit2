---
name: core-protocol
version: 2.1.0
priority: P0
trigger: always_on
description: The ordered procedure for every request — classify, read the agent file, read its skills, print the plan line, build, run the gates, report evidence. Do these steps in order; do not skip one.
---

# Core Protocol — do this, in this order, on every request

`engineering-excellence` is how to think. `code-rules` holds the gate policy. This file is what you
do, step by step. A text-only QUESTION stops after step 1.

## 1. Classify
Use the table in `request-routing`. Output one of: QUESTION, SURVEY, SIMPLE CODE, COMPLEX CODE,
NEW APP, MULTI-DOMAIN, COMMAND. A QUESTION gets a text answer and ends here.

## 2. Read the agent file
Pick the agent from the routing table. **Read the file now:**
`C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/<agent>.md`. Do not build from memory of
what the agent does; read it. If the user wrote `@agent`, use that one.

## 3. Read the skill files the agent names
The agent file has a "Read now:" line with absolute paths. Read every file on it before writing
code. Inside a skill, `SKILL.md` first, then only the sub-files it points to for this task. A
COMMAND (`/plan`, `/see`, `/review`, ...) is a skill at
`C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/<command>/SKILL.md`; read it and follow its
Steps.

## 4. Ask only if the answer changes the build
Scope, data model, security, architecture, or a design direction you cannot infer. NEW APP or
multi-file feature: at most 1-3 questions, one message, before planning. Bug fix, single file, UI
tweak: do not ask; proceed and state assumptions. Never a second round; on "proceed", proceed with
stated defaults.

## 5. Print the plan line
First line of every code or design response, exactly this shape, then nothing else on that line:

`@<agent> · skills: <a>, <b> · steps: <the ordered steps you will run for this task>`

Example: `@frontend-specialist · skills: frontend-design, browser-verification · steps: screen read → build → checklist → /see → report`

This line is mandatory. It proves you routed, loaded, and planned. No other announcement format.

## 6. Plan file when required
NEW APP and COMPLEX CODE: write `docs/plans/{task-slug}.md` (kebab-case; format in the
`plan-writing` skill) before code. SIMPLE CODE: 1-3 plan lines in the response are enough.

## 7. Build
Follow the agent file and the skills you read. Tests for logic changes. Focused diffs. UI work:
the design read, screen read, and `DESIGN.md` gate come from `frontend-design` / `design-rules`;
you already read them in step 3.

## 8. Run the gates (literal commands, every code task)
1. `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .` — required
   checks (security high+, lint, types, tests) must pass. Fix failures; do not report around them.
2. **If anything rendered changed:** run `/see` (read
   `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/see/SKILL.md` and follow it). Look at the
   page, critique your own draft, refine it, look again. A UI change you have not seen is not done.
   Skip only with a stated reason (no dev server / not visual / no browser).
3. Non-trivial diff: `/review` (`skills/review/SKILL.md`) before you call it done.
Required-vs-advisory detail and the auto-fix policy are in `code-rules` (always on).

## 9. Report evidence
What changed, the exact commands run and what they printed, what you assumed, and a "Not verified"
line for anything you did not run. "Passing", "fixed", "works" without the output you saw is a
claim, not a report. Record a durable dead end as a `[failure]` entry (`memory-system`).

## Multi-agent work
Fewest agents that fit; one specialist is a valid answer. File ownership: `agents/orchestrator.md`.
Delegation method: `parallel-agents` skill. Precedence when files disagree: global rules → agent
file → skill; a project `DESIGN.md` overrides any skill's design guidance.
