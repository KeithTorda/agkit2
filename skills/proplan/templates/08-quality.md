---
doc: 08-quality
project: <slug>
version: 0.1.0
status: draft
owner: qa-engineer
updated: YYYY-MM-DD
---

<!-- AGKIT2 2.8.0 planning scaffold. Keep machine-readable IDs/fields and use only relevant content. Replace illustrative rows and examples with the actual brief. Do not invent evidence, approvals, dates or locale-specific obligations. Shared core/design/verification rules govern decisions and checks; this template adds no universal approval or task-count gate. -->


# Quality

## Quality goals

<!-- Link relevant DG/NFR outcomes and distinguish proposed budgets from measured baselines. -->
## Test strategy

<!-- Choose the test level that observes important behavior at reasonable cost. The table illustrates options; delete irrelevant rows and align ownership with the actual work split. -->
| Level | Scope | Tool | Runs | Owner |
|---|---|---|---|---|
| Unit | pure logic: totals, rules, validators |  | every push | the building agent |
| Integration / feature | endpoints with database, auth, jobs | | every push | backend-engineer |
| End-to-end | the key flows in a real browser |  | every push to main, before release | qa-engineer |
| Manual / UAT | real users on real devices | checklist | per milestone | client + qa-engineer |

## Test environments and data

<!-- State real environments, synthetic/deterministic data, supported platforms and unavailable dependencies. Do not copy raw production personal data into fixtures. -->
## Test cases

<!-- Define TC IDs once and cover Must requirements in the full set. Focus on valuable success, boundary, denial and recovery behavior; do not list static implementation trivia. -->
| ID | Title | Level | Covers | Steps and data | Expected |
|---|---|---|---|---|---|
| TC-001 | | | R-001 | | |

## Performance budgets

<!-- Use justified metrics/workloads with a measurement method and NFR link. Do not invent numeric targets to satisfy a heuristic. -->
| Metric | Budget | How measured | Covers |
|---|---|---|---|
| | | | |

## Accessibility

<!-- Combine suitable automated checks with relevant keyboard/focus/readability/assistive checks. State tested devices/widths honestly. -->
## Security testing

<!-- Exercise meaningful trust and resource-permission boundaries requested by 07; scanner output does not replace authorization tests. -->
## User acceptance testing

<!-- Identify actual participants, tasks, device context and acceptance evidence when UAT is part of the project. Do not invent user signoff. -->
## Entry and exit criteria

<!-- Use criteria appropriate to the milestone and product consequence. Separate a real blocker from accepted nonblocking polish. -->
## Definition of done

<!-- Use the task verify criterion and verify-changes policy. Run relevant behavior evidence and required project checks; report incomplete/skipped checks honestly. Do not create tests for every reversible prose/style edit. -->
## Defect severity

<!-- Classify by actual consequence and affected users. Cosmetic defects can still matter when they obscure content or prevent the primary task. -->
| Severity | Meaning | Release rule |
|---|---|---|
| Critical | data loss, money wrong, security hole, system unusable | blocks release |
| High | a Must requirement fails with no workaround | blocks release |
| Medium | workaround exists | fix or accept with the client |
| Low | cosmetic | backlog |
