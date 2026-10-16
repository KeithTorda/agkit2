---
name: plan
description: "Write or update a lightweight executable plan without implementing code when the request is planning-only. Use /plan for a bounded feature, fix or multi-file change; /proplan supports a system document set."
version: 2.8.2
---

# /plan

Use `KIT/agents/project-planner.md` and `KIT/skills/plan-writing/SKILL.md`. Read the relevant existing plan, source and accepted decisions before creating another plan for the same work.

Define the outcome, scope, important assumptions and dependencies. Ask only for a missing decision that materially changes the plan. For a new visual direction, follow the style/reference conversation in design-rules; a plan need not prematurely invent final visual tokens.

Write `docs/plans/<slug>.md` when a durable plan is useful or requested. Use tasks that have an owner, concrete result and meaningful verification. Show consequential uncertainty instead of fixed task quotas or invented schedules. Use proplan when the user requests a system specification or the work warrants linked domain documents, without forcing a command switch as an approval ceremony.

For a planning-only request, deliver the plan path, key decisions, readiness and next executable work, then stop. If the user already asked to plan and implement, the planning step does not revoke that authorization; continue once required decisions are settled.
