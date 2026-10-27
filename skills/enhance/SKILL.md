---
name: enhance
description: "Implement an addition or improvement in an existing project while preserving relevant contracts and conventions. Use /enhance for features and maintenance rather than a new project."
version: 2.8.3
---

# /enhance

Read the requested behavior, affected code, relevant project decisions and existing tests. Use the owning agent from the `kit-core` agent table; coordinate multiple domains through `parallel-agents` only when useful.

Describe the intended change in terms of the user's outcome and identify affected callers, data and UI states. Resolve a missing product/permission decision when it changes the deliverable; choose routine details using the current project. A short task list is enough for bounded work; use `plan-writing` for durable coordination.

For a new visual design or deliberate redesign, ask one short style question only if the direction is genuinely unclear. Theme and token work follows `rule-01-unified-theme-system`. Keep DESIGN.md aligned when the actual system changes.

Implement the complete requested slice, updating dependent contracts and removing replaced paths where safe. Avoid unrelated refactors or new libraries without a reason. For performance work, measure before and after using performance-profiling.

Do not automatically audit or run checks after an enhancement. Use `verify-changes` only when explicitly requested (kit-core). Report the resulting behavior, relevant files/routes, checks and material limitations. Continue until the authorized change is integrated rather than stopping at an implementation proposal.
