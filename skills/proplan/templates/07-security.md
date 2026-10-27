---
doc: 07-security
project: <slug>
version: 0.1.0
status: draft
owner: security-engineer
updated: YYYY-MM-DD
---

<!-- AGKIT2 2.8.0 planning scaffold. Keep machine-readable IDs/fields and use only relevant content. Replace illustrative rows and examples with the actual brief. Do not invent evidence, approvals, dates or locale-specific obligations. Shared core/design/verification rules govern decisions and checks; this template adds no universal approval or task-count gate. -->


# Security and Privacy

## Scope and assets

<!-- Identify relevant assets, identities, data and operational harm. Scale the assessment to this system; do not claim a checklist proves complete security. -->
## Trust boundaries

<!-- Trace real untrusted entrypoints and privilege/data transitions from the architecture. -->
## Threat model (STRIDE)

<!-- Use concrete reachable scenarios, prerequisites and consequences. STRIDE is a prompt for coverage, not a requirement to invent a threat in every category. Link controls to real requirements/tasks. -->
| ID | STRIDE | Where | Threat | Likelihood | Impact | Mitigation | Planned in |
|---|---|---|---|---|---|---|---|
| TH-01 | | | | | | | NFR-01 |

## Authorization matrix

<!-- Use actual role names and actions, including ownership/tenant conditions. Align server enforcement and API denial behavior; UI visibility alone is not authorization. -->
| Action | Role A | Role B | Role C |
|---|---|---|---|
| | | | |

## Authentication and sessions

<!-- Specify the identity/session lifecycle and relevant abuse/recovery controls. Prefer established provider/library capabilities and verify current guidance for consequential choices. -->
## Data privacy

<!-- Identify the actual jurisdiction, purposes, lawful basis/notice, minimization, access, retention/deletion, rights and incident ownership where applicable. Verify current authoritative requirements and timelines; never infer jurisdiction or legal compliance from this template. -->
## Secrets and configuration

<!-- List secret names/storage/access/rotation practices without values. Keep privileged material out of client bundles, examples and logs. -->
## Audit logging

<!-- Record security/business events needed for investigation with useful attribution and integrity/retention controls. Avoid unnecessary sensitive data and state actual access boundaries. -->
| Event | Fields | Retention |
|---|---|---|
| | | |

## Input, output and dependencies

<!-- Apply controls at real boundaries and evaluate dependency findings for reachability/impact. Generic scanner results are leads, not automatic confirmed exploits. -->
## Security testing

<!-- Connect important permission, validation and integrity controls to meaningful tests/review. Follow verify-changes when checks are requested rather than a separate rigid tier recipe. -->
## Residual risks

<!-- State confirmed remaining exposure, owner and actual acceptance. Do not fabricate approval or silently waive a material boundary failure. -->
