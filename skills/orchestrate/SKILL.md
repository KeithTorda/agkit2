---
name: orchestrate
description: "Coordinate a multi-domain task or execute a plan/milestone through shared contracts, explicit ownership and integrated evidence. Use /orchestrate with a task or plan path."
version: 2.8.2
---

# /orchestrate

Use `KIT/agents/lead.md` and `KIT/skills/parallel-agents/SKILL.md`. Input can be a task, `docs/plans/<yyyy-mm-dd>-<slug>.md`, or `docs/proplan/<slug> M<n>`. Read the relevant plan and source before assigning work.

## Scope and organize

Establish the intended outcome and shared decisions. If a style answer was given, carry it to workers once. Assign explicit writable paths and contracts; parallelize only independent work. Use actual tool capabilities rather than presumed agent names or workspace parameters. Without delegation tools, do the roles sequentially and say so.

For plan execution, identify the selected tasks, dependencies, verify criteria and relevant requirement/API/ADR excerpts. An unresolved blocker stops the affected task; unrelated ready work can continue. Do not silently build around a contradictory permission or data contract.

## Integrate and prove

Review each worker's output and actual evidence. Resolve contract differences, integrate in dependency order and read the combined changes for mismatched names, payloads and states. Run verify-changes only if the user asked for verification.

Tick a task when its work is done; write 'not verified' next to it when no check ran. For proplan use `- [ ]` to `- [x]`, add a concise command/result note, and update the overview when useful. Keep stable IDs; regenerate TRACEABILITY.md with proplan_check rather than editing generated rows. A plan task does not create authorization for otherwise unapproved external actions.

Finish with integrated behavior, task state, material decisions, verification and remaining dependencies. Do not stop merely because all workers returned if the requested result still needs integration.
