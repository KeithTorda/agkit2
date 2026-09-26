---
doc: 02-requirements
project: <slug>
version: 0.1.0
status: draft
owner: product-manager
updated: YYYY-MM-DD
---

<!--
Owner: product-manager (Phase 1). A small-team SRS in the spirit of ISO/IEC/IEEE 29148: needs first, then verifiable requirements.
IDs defined here:
  R-001 ...   functional requirements (three digits), one heading each: "### R-001 Cashier signs in with a PIN".
  NFR-01 ...  non-functional requirements (two digits), one heading each.
Each R-xxx section must contain:
  - Priority: Must | Should | Could | Won't   (MoSCoW; Must = the system fails its purpose without it)
  - Goals: G-xx                               (the business goal it serves; none means scope creep or a missing goal)
  - Story: As a <persona>, I want <capability> so that <benefit>.
  - Acceptance: one or more lines "AC1: Given <state>, when <action>, then <observable result>" on ONE line each.
Checker rules: every R has a priority and at least one Given/when/then line; every Must R is covered by a task (10) and, in the full set, a test case (08).
Good acceptance criteria use concrete values (amounts, counts, messages, roles) and cover the unhappy paths: empty, invalid, permission denied, offline, duplicate, boundary.
Bad: "The system should be fast and easy to use." Good: "Given 40 queued orders, when the connection returns, then all 40 reach the server within 5 minutes and none is created twice."
Put Won't items under Scope > Out, not as R-ids, unless the client needs to see them rejected explicitly.
-->

# Requirements

## Stakeholders

<!-- Everyone who uses, pays for, approves, or is affected by the system, including regulators and outside parties (accountant, LGU office, school registrar). -->

| Stakeholder | Interest | Involvement |
|---|---|---|
| | | |

## Personas

<!-- 2-4 personas. Each: name and role, context (device, environment, time pressure), skill level, what they need most. Base them on real users the client described, not stereotypes. -->

## Scope

In:
<!-- Capabilities this version delivers, as short bullets. -->

Out (this version):
<!-- What is not built, and the phase it moves to if known. Be explicit; this list stops scope creep. -->

## Constraints

<!-- Legal (Data Privacy Act RA 10173, tax/receipt rules, accessibility law), budget, deadline, existing systems, devices, hosting, languages (English, Filipino, a regional language). -->

## Functional requirements

### R-001 <Short requirement name>

- Priority: Must
- Goals: G-01
- Story: As a <persona>, I want <capability> so that <benefit>.
- Acceptance:
  - AC1: Given <state>, when <action>, then <observable result>.
  - AC2: Given <error or edge state>, when <action>, then <observable result>.

## Non-functional requirements

<!--
One heading per NFR, each with a measurable target and the development goal it serves ("Serves DG-01"). Categories (ISO/IEC 25010, trimmed):
- Performance: response times at a percentile, on named hardware and network.
- Reliability and availability: uptime, offline behaviour, data loss tolerance (RPO), recovery time (RTO).
- Security: authentication strength, authorization model, session limits, OWASP ASVS level.
- Privacy: personal data collected, purpose, retention, who can see it (RA 10173 when Philippine residents' data is processed).
- Usability and accessibility: WCAG level, minimum target sizes, supported languages.
- Compatibility: browsers, devices, screen widths, printers, OS versions.
- Maintainability: coverage, CI, setup time, documentation.
- Data integrity: money representation, uniqueness rules, audit trail.
A requirement without a number cannot be tested; the checker warns when an NFR has no number.
-->

### NFR-01 <Quality attribute>

## Business rules

<!-- Rules that hold regardless of screen: computations, legal rules, numbering, rounding. Example: "Senior Citizen discount: remove VAT, then deduct 20% of the VAT-exempt price." Reference them from the requirements that use them. -->

## Open questions

<!-- Only questions that change a requirement. Each with a recommended default and who answers. -->
