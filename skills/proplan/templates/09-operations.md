---
doc: 09-operations
project: <slug>
version: 0.1.0
status: draft
owner: devops-engineer
updated: YYYY-MM-DD
---

<!-- AGKIT2 2.8.0 planning scaffold. Keep machine-readable IDs/fields and use only relevant content. Replace illustrative rows and examples with the actual brief. Do not invent evidence, approvals, dates or locale-specific obligations. Shared core/design/verification rules govern decisions and checks; this template adds no universal approval or task-count gate. -->


# Operations

## Environments

<!-- Describe only actual environments and their purpose/data/access. A staging environment is useful when warranted, not an automatic extra service. -->
| Environment | Purpose | Host | URL | Data | Who deploys |
|---|---|---|---|---|---|
| Local | development | developer machine | localhost | seed | developer |
| Staging | UAT, pre-release checks | | | anonymised or seed | |
| Production | live | | | real | |

## Configuration and secrets

<!-- List required names and storage/rotation ownership, never secret values. -->
## CI/CD pipeline

<!-- Match project/provider capabilities and meaningful release checks. Identify artifact identity and failure behavior without requiring a generic pipeline shape. -->
## Deploy procedure

<!-- Prepare the concrete target/revision, data effects and recovery path. Use existing authorization; ask only for a consequential operation not already authorized. Verify the serving result and a key flow. -->
## Database migrations

<!-- Specify compatibility/order, backfills, validation and recovery. Distinguish app rollback from data restoration and avoid inferred production targets. -->
## Backups and restore

<!-- Align coverage, frequency, retention and restore validation with actual recovery needs. State RPO/RTO basis and untested assumptions. -->
| Item | Frequency | Location | Retention | Restore tested |
|---|---|---|---|---|
| | | | | |

## Monitoring and alerting

<!-- Choose actionable symptoms with an owner and response; remove irrelevant signal rows rather than creating noisy alerts. -->
| Signal | Tool | Threshold | Alert to | Action |
|---|---|---|---|---|
| Uptime | | | | |
| Errors | | | | |
| Disk, CPU, memory | | | | |
| Backup success | | | | |
| TLS certificate expiry | | | | |

## Logging

<!-- Make investigation possible while limiting sensitive data. State retention, access and correlation fields. -->
## Rollback and incident response

<!-- Identify a usable recovery target, data compatibility limits and escalation path. Avoid repeated speculative mutations during an incident. -->
## Maintenance

<!-- Assign maintenance the system actually needs and use the platform-supported mechanisms. -->
## Cost

<!-- Identify currency, assumptions and source/date for current provider costs. Estimates must be labeled and verified when used for a commitment. -->
## Handover and runbooks

<!-- Plan documents/access transfer for actual operators. Keep credentials in the appropriate secret channel rather than this file. -->
