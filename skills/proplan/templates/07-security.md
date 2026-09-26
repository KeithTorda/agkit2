---
doc: 07-security
project: <slug>
version: 0.1.0
status: draft
owner: security-auditor
updated: YYYY-MM-DD
---

<!--
Owner: security-auditor (Phase 1 notes, Phase 3 full document). Input: 02, 03, 04, 05, 06.
IDs defined here:
  TH-01 ...  threats, defined as the first cell of the threat model table.
Each threat names its mitigation and where the mitigation is planned (NFR-xx, R-xxx or T-xxx), so the reviewer can see it is not only written down.
Scale to the system: a brochure site needs a page; a system with money, personal data or government records needs all sections.
-->

# Security and Privacy

## Scope and assets

<!-- What is worth protecting: money, personal data, accounts, admin control, availability during business hours, reputation. Rank them. -->

## Trust boundaries

<!-- Where untrusted input enters: browsers, public forms, mobile apps, webhooks, file uploads, imports, third-party APIs, staff devices. A mermaid diagram of 03's containers with the boundaries marked is enough. -->

## Threat model (STRIDE)

<!--
Walk each container and key flow through STRIDE: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.
Likelihood and impact: Low / Medium / High. Keep threats specific to this system ("cashier voids a paid cash order and keeps the money"), not generic ("hackers").
-->

| ID | STRIDE | Where | Threat | Likelihood | Impact | Mitigation | Planned in |
|---|---|---|---|---|---|---|---|
| TH-01 | | | | | | | NFR-01 |

## Authorization matrix

<!-- Roles as columns, actions as rows. Allowed = Y, denied = blank, conditional = the condition ("own records", "with supervisor PIN"). Enforced on the server for every action; 05 maps endpoints to it. -->

| Action | Role A | Role B | Role C |
|---|---|---|---|
| | | | |

## Authentication and sessions

<!-- Credential type per role, password or PIN rules, hashing (Argon2id or bcrypt), MFA for admin accounts where the risk warrants it, lockout and rate limits, session lifetime and idle timeout, device or token revocation. -->

## Data privacy

<!--
For systems that process personal information of people in the Philippines, the Data Privacy Act of 2012 (RA 10173), its IRR and NPC issuances apply. Plan for:
- Inventory: which personal and sensitive personal information is collected (link 04 personal data inventory), from whom, for what purpose.
- Lawful basis and privacy notice: consent or another basis; the notice shown at collection, in plain language.
- Proportionality: collect only what the purpose needs; mask where full values are not needed (show last 4 digits of an ID).
- Access: who can see it (authorization matrix), and logging of access to sensitive records.
- Retention and disposal: tied to the purpose and legal retention periods (04 retention table).
- Data subject rights: how a person asks for access, correction or deletion, and who handles it.
- Breach handling: who decides, how affected people and the National Privacy Commission are notified within the required period (72 hours from knowledge for notifiable breaches under current NPC rules).
- Registration and DPO: whether the client must register its processing system or designate a Data Protection Officer under current NPC circulars; the client confirms with its counsel.
Other jurisdictions: name the law and the equivalent items.
-->

## Secrets and configuration

<!-- Where secrets live (environment variables, the host's secret store), who can read them, rotation, what must never reach the client bundle or the repository. -->

## Audit logging

<!-- Events recorded, fields (who, what, when, from where, before/after), retention, who can read the log, and that it is append-only. -->

| Event | Fields | Retention |
|---|---|---|
| | | |

## Input, output and dependencies

<!-- Validation at the boundary, output escaping, file upload rules (type, size, storage outside the web root), CSRF, CORS, security headers, dependency audit and lockfiles. -->

## Security testing

<!-- What 08 must include: authorization tests per matrix row that matters, scanner runs, a manual review of the money or approval paths. Tier 2 per `code-rules` for these changes. -->

## Residual risks

<!-- Threats accepted rather than mitigated, with who accepted them. Carry the significant ones to 11-risks. -->
