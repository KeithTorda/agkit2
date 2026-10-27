---
name: plan
description: "Write or update a lightweight executable plan without implementing code when the request is planning-only. Use /plan for a bounded feature, fix or multi-file change; /proplan supports a system document set."
version: 2.8.2
---

# /plan

Use `KIT/agents/product-planner.md` and `KIT/skills/plan-writing/SKILL.md`. Read the relevant existing plan, source and accepted decisions before creating another plan for the same work.

Define the outcome, scope, important assumptions and dependencies. Ask only for a missing decision that materially changes the plan. For a new visual direction, a plan need not prematurely invent final visual tokens.

Always write the plan to `docs/plans/<yyyy-mm-dd>-<slug>.md` in the format of `rule-05-planning-and-docs`. Use tasks that have an owner, concrete result and meaningful verification. Show consequential uncertainty instead of fixed task quotas or invented schedules. Use proplan when the user requests a system specification or the work warrants linked domain documents, without forcing a command switch as an approval ceremony.

For a planning-only request, deliver the plan path, key decisions, readiness and next executable work, then stop. If the user already asked to plan and implement, the planning step does not revoke that authorization; continue once required decisions are settled.
