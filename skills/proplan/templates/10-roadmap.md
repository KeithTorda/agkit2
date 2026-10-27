---
doc: 10-roadmap
project: <slug>
version: 0.1.0
status: draft
owner: product-planner
updated: YYYY-MM-DD
---

<!-- AGKIT2 2.8.0 planning scaffold. Keep machine-readable IDs/fields and use only relevant content. Replace illustrative rows and examples with the actual brief. Do not invent evidence, approvals, dates or locale-specific obligations. Shared core/design/verification rules govern decisions and checks; this template adds no universal approval or task-count gate. -->


# Roadmap

## Approach

<!-- State delivery priorities, capacity, estimate basis and relevant uncertainty. Contingency follows the actual risks; no fixed task count, duration or buffer percentage is required. -->
## Milestones

<!-- Group tasks into useful deliverable outcomes. Preserve the parseable T checkbox and owner/estimate/depends/covers/verify field names. Owners and dependencies must exist; each task has meaningful observable verification. -->
### M1 <Milestone name> (<weeks>)


- [ ] **T-001** <Task outcome>
  - owner: <agent> · estimate: 1d · depends: - · covers: R-001
  - verify: <command or observation that fails when the work is wrong>

## Critical path

<!-- Identify the actual dependency chain and capacity limits. Use a diagram only when it helps; do not invent dates to populate a gantt chart. -->
```mermaid
gantt
  title <System name>
  dateFormat YYYY-MM-DD
  excludes weekends
  section M1
  T-001 Task name :t001, YYYY-MM-DD, 1d
```

## Release plan

<!-- State what reaches which environment and how it is observed/accepted. A planned release task does not grant otherwise missing external authorization. -->
## Buffer and contingency

<!-- State contingency explicitly with its rationale and response to risk. A justified zero is possible; do not import a universal percentage. -->
## Definition of done

<!-- A task checkbox changes only after its verification has evidence. Use verify-changes and relevant docs; record incomplete prerequisites instead of pretending completion. -->
