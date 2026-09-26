---
doc: 09-operations
project: <slug>
version: 0.1.0
status: draft
owner: devops-engineer
updated: YYYY-MM-DD
---

<!--
Owner: devops-engineer (Phase 3). Input: 03 deployment view, 07 secrets, 08 environments, 01 availability goals.
IDs: none defined here. Refer to NFR-xx for availability, RPO/RTO and backups, and to T-xxx for setup tasks once 10 exists.
Size to the client: shared hosting with cPanel and a weekly backup can be the right answer; say why.
Every procedure here must be something a second person could follow at 22:00 without calling the author.
-->

# Operations

## Environments

| Environment | Purpose | Host | URL | Data | Who deploys |
|---|---|---|---|---|---|
| Local | development | developer machine | localhost | seed | developer |
| Staging | UAT, pre-release checks | | | anonymised or seed | |
| Production | live | | | real | |

## Configuration and secrets

<!-- Environment variables per environment (names only, never values), where they are stored, who can change them, how a new secret is added and rotated. -->

## CI/CD pipeline

<!-- Stages in order, what fails the pipeline, and where it runs (GitHub Actions, GitLab CI). Example: install -> lint -> types -> tests -> build -> deploy to staging on main -> manual promote to production. -->

## Deploy procedure

<!-- Step by step for production, including the migration step, cache clearing, queue restart, and the smoke check after deploy. Deploy windows (outside business hours for a store or office). Who approves. -->

## Database migrations

<!-- How migrations run in deploy, how destructive changes are split (expand, migrate data, contract), and the backup taken before a risky migration. -->

## Backups and restore

<!-- What is backed up (database, uploaded files, configuration), how often, where (off-site, encrypted), retention, and the restore test schedule. State RPO (max data loss) and RTO (max downtime). -->

| Item | Frequency | Location | Retention | Restore tested |
|---|---|---|---|---|
| | | | | |

## Monitoring and alerting

| Signal | Tool | Threshold | Alert to | Action |
|---|---|---|---|---|
| Uptime | | | | |
| Errors | | | | |
| Disk, CPU, memory | | | | |
| Backup success | | | | |
| TLS certificate expiry | | | | |

## Logging

<!-- What is logged, where, retention, and what must never be logged (passwords, tokens, full ID numbers, personal data beyond need). -->

## Rollback and incident response

<!-- How to roll back a bad release (previous release folder, container tag, Vercel instant rollback), how to roll back or forward a failed migration, who is called, how the client is informed, and the short post-incident note. -->

## Maintenance

<!-- OS and dependency updates (cadence, who), certificate renewal, log rotation, storage growth, licence renewals, domain renewal dates. -->

## Cost

<!-- Monthly running cost by item (hosting, domain, email, SMS, storage, backups) in the client's currency. -->

## Handover and runbooks

<!-- Runbooks to write (link 12): deploy, restore, rotate a secret, add a user, what to do when the site is down. Accounts and credentials handed to the client and how. -->
