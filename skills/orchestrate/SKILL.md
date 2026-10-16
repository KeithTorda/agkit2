---
name: orchestrate
description: "Coordinate a multi-domain task or execute a plan/milestone through shared contracts, explicit ownership and integrated evidence. Use /orchestrate with a task or plan path."
version: 2.8.2
---

# /orchestrate

Use `KIT/agents/orchestrator.md` and `KIT/skills/parallel-agents/SKILL.md`. Input can be a task, `docs/plans/<slug>.md`, or `docs/proplan/<slug> M<n>`. Read the relevant plan and source before assigning work.

## Scope and organize

Establish the intended outcome, current authorization and shared decisions. For a new visual design, collect the style/reference answer once through design-rules and carry it to workers. Assign explicit writable paths and contracts; parallelize only independent work. Use actual tool capabilities rather than presumed agent names or workspace parameters. Without delegation tools, do the roles sequentially and say so.

For plan execution, identify the selected tasks, dependencies, verify criteria and relevant requirement/API/ADR excerpts. An unresolved blocker stops the affected task; unrelated ready work can continue. Do not silently build around a contradictory permission or data contract.

## Integrate and prove

Review each worker's output and actual evidence. Resolve contract differences, integrate in dependency order, then check the assembled behavior with verify-changes. A worker's isolated test pass does not establish that the whole flow works.

Update authorized task progress only after the stated criterion has evidence. For proplan use `- [ ]` to `- [x]`, add a concise command/result note, and update the overview when useful. Keep stable IDs; regenerate TRACEABILITY.md with proplan_check rather than editing generated rows. A plan task does not create authorization for otherwise unapproved external actions.

Finish with integrated behavior, task state, material decisions, verification and remaining dependencies. Do not stop merely because all workers returned if the requested result still needs integration.
