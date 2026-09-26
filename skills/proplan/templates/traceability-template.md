# Traceability

<!--
This file is generated. Do not fill it by hand:
    python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --write-traceability
The script reads the documents and writes the tables between the two markers below. Text outside the markers is kept,
so a short introduction or notes may go above the start marker or below the end marker.
The checker fails with "out of date" when the documents change and this file is not regenerated.
Columns: Goal (01) -> Requirement (02) -> Screens / APIs (06, 05; lite: 03) -> Tasks with milestone (10) -> Tests (08, full set)
-> Status (covered, GAP: no task, GAP: no test, not planned).
The generated content looks like the block below; the placeholder rows disappear on the first run.
-->

<!-- proplan:traceability:start -->

## Functional requirements

| Goal | Requirement | Priority | Screens / APIs | Tasks | Tests | Status |
|---|---|---|---|---|---|---|
| G-01 | R-001 Requirement title | Must | S-01, API-01 | T-001 (M1) | TC-001 | covered |

## Non-functional requirements

| Dev goal | NFR | Tasks | Tests | Status |
|---|---|---|---|---|
| DG-01 | NFR-01 Quality attribute | T-001 (M1) | TC-001 | covered |

## Goals

| Goal | Requirements |
|---|---|
| G-01 Goal title | R-001 |

<!-- proplan:traceability:end -->
