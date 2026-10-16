---
name: enhance
description: "Implement an addition or improvement in an existing project while preserving relevant contracts and conventions. Use /enhance for features and maintenance rather than a new project."
version: 2.8.2
---

# /enhance

Read the requested behavior, affected code, relevant project decisions and existing tests. Use the owning specialist from `KIT/agents/orchestrator.md`; coordinate multiple domains through `parallel-agents` only when useful.

Describe the intended change in terms of the user's outcome and identify affected callers, data and UI states. Resolve a missing product/permission decision when it changes the deliverable; choose routine details using the current project. A short task list is enough for bounded work; use `plan-writing` for durable coordination.

For a new visual design or deliberate redesign, follow design-rules: one conversational style/reference question, then wait unless answered or explicitly delegated. Maintenance within the accepted system uses that direction without repeated intake. Keep DESIGN.md aligned when the actual system changes.

Implement the complete requested slice, updating dependent contracts and removing replaced paths where safe. Avoid unrelated refactors or new libraries without a reason. For performance work, measure before and after using performance-profiling.

Use `verify-changes` for evidence matched to the consequence. Report the resulting behavior, relevant files/routes, checks and material limitations. Continue until the authorized change is integrated rather than stopping at an implementation proposal.
