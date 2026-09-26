---
doc: 08-quality
project: <slug>
version: 0.1.0
status: draft
owner: test-engineer
updated: YYYY-MM-DD
---

<!--
Owner: test-engineer (Phase 3). Input: 01 development goals, 02 acceptance criteria and NFRs, 06 flows, 07 security testing.
IDs defined here:
  TC-001 ...  test cases, defined as the first cell of the test case table. Each row names the R-xxx or NFR-xx it verifies.
Checker rules: every Must requirement needs at least one TC in the full set; a TC that maps to no requirement is an error.
Test cases here are the acceptance-level cases that prove requirements; unit tests are written during the build and not listed one by one.
-->

# Quality

## Quality goals

<!-- Restate the development goals from 01 (DG-xx) as the targets this strategy must meet: coverage, performance, accessibility, security. -->

## Test strategy

<!-- The pyramid for this system. Most tests where logic is cheapest to test; few, valuable end-to-end tests. -->

| Level | Scope | Tool | Runs | Owner |
|---|---|---|---|---|
| Unit | pure logic: totals, rules, validators | <!-- Pest / PHPUnit, Vitest, pytest --> | every push | the building agent |
| Integration / feature | endpoints with database, auth, jobs | | every push | backend-specialist |
| End-to-end | the key flows in a real browser | <!-- Playwright --> | every push to main, before release | test-engineer |
| Manual / UAT | real users on real devices | checklist | per milestone | client + test-engineer |

## Test environments and data

<!-- Where tests run (CI, staging), seed data, anonymised copies of production data (never raw personal data), test accounts per role, devices and browsers to cover. -->

## Test cases

<!-- One row per acceptance-level case. Steps can be short; the acceptance criterion in 02 holds the detail. Level: unit, feature, e2e, manual. -->

| ID | Title | Level | Covers | Steps and data | Expected |
|---|---|---|---|---|---|
| TC-001 | | | R-001 | | |

## Performance budgets

<!-- Each budget with how it is measured and the NFR it proves. -->

| Metric | Budget | How measured | Covers |
|---|---|---|---|
| | | | |

## Accessibility

<!-- Target level (from 02), automated checks (axe in Playwright), manual checks (keyboard-only pass, screen reader on the key flow, 200% zoom, 390 px width), who does them and when. -->

## Security testing

<!-- The cases 07 asks for: authorization tests per role, input validation, scanner runs, dependency audit. -->

## User acceptance testing

<!-- Who tests, on what devices, with what script, in which milestone, and what "accepted" means (signed checklist, pilot results). -->

## Entry and exit criteria

<!-- When a milestone can start testing (build deployed to staging, seed data loaded) and when it is accepted (all Must TCs pass, no open Critical/High defects, UAT signed). -->

## Definition of done

<!--
Applies to every task in 10. Proportional to risk, per the `code-rules` tiers:
- The task's verify line was run and passed; output recorded.
- Tier 1 (normal): project lint/type/test for touched files.
- Tier 2 (auth, money, permissions, migrations, public API): full checks, tests for the logic, /review on the diff.
- Tier 3 (release): verify_all and the deploy steps, client approval.
- Docs listed in 12 for this task updated.
-->

## Defect severity

| Severity | Meaning | Release rule |
|---|---|---|
| Critical | data loss, money wrong, security hole, system unusable | blocks release |
| High | a Must requirement fails with no workaround | blocks release |
| Medium | workaround exists | fix or accept with the client |
| Low | cosmetic | backlog |
