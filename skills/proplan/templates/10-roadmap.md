---
doc: 10-roadmap
project: <slug>
version: 0.1.0
status: draft
owner: project-planner
updated: YYYY-MM-DD
---

<!--
Owner: project-planner (Phase 4). Input: every document before it.
IDs defined here:
  M1, M2 ...  milestones, one heading each: "### M1 Foundation and menu (weeks 1-2)".
  T-001 ...   tasks, as checkbox lines under a milestone (format below). /orchestrate executes one milestone at a time.
  RK-01 ...   lite set only: top risks table at the end (full set: 11-risks).
Task format (the checker parses it; keep the field names):
  - [ ] **T-001** One reviewable outcome, in the imperative
    - owner: <kit agent name, or "Name (human)"> · estimate: 1d · depends: T-000 or - · covers: R-001, NFR-02
    - verify: <command or observation with a concrete pass/fail signal, including the negative case>
Checker rules: every task has an owner, a verify line and covers at least one existing R-, NFR- or DG- id; depends lists
existing T-ids with no cycles; every Must requirement is covered by a task; the roadmap states a buffer.
Sizing: 0.5-3 days per task. A task that needs "and" to describe usually splits. 5-12 tasks per milestone.
Order: dependencies first (schema -> shared rules -> API -> UI -> tests), riskiest unknown early (a timeboxed spike whose output is a decision).
Every milestone ends with something the client can see or use.
-->

# Roadmap

## Approach

<!--
- Team and capacity (people x days per week), start date, estimate unit (developer days).
- Estimation basis (similar past work, three-point estimates for risky tasks).
- Buffer: state it explicitly (15-25% for a known stack, more for new technology or unclear scope) and where it is held.
- What decides the order (dependencies, risk, client demo dates).
-->

## Milestones

### M1 <Milestone name> (<weeks>)

<!-- Exit: one sentence the client can check at the milestone demo. -->

- [ ] **T-001** <Task outcome>
  - owner: <agent> · estimate: 1d · depends: - · covers: R-001
  - verify: <command or observation that fails when the work is wrong>

## Critical path

<!-- The longest dependency chain, as "T-001 → T-002 → ...". Name the tasks whose slip moves the launch date and why. With one developer, say so: everything is sequential, but the chain still shows what cannot be reordered. -->

```mermaid
gantt
  title <System name>
  dateFormat YYYY-MM-DD
  excludes weekends
  section M1
  T-001 Task name :t001, YYYY-MM-DD, 1d
```

## Release plan

<!-- What ships at each milestone, to which environment, and who accepts it. Include the pilot or parallel run for systems that replace a manual process. -->

## Buffer and contingency

<!-- Buffer size and the rule for spending it; what gets cut first if time runs out (usually Should requirements, then Could). -->

## Definition of done

<!-- Point to 08 (full set) or state it here (lite): verify line run and recorded, `code-rules` tier checks for the task's risk, docs from 12 updated. -->
