---
doc: 12-documentation
project: <slug>
version: 0.1.0
status: draft
owner: documentation-writer
updated: YYYY-MM-DD
---

<!--
Owner: documentation-writer (Phase 4). Input: 06 (users), 09 (runbooks), 10 (milestones and tasks).
IDs defined here:
  DOC-01 ...  documents to produce during the build, defined as the first cell of the table.
Plan documentation as work: each document has an audience, an owner agent, a due point (a milestone or a T-id) and a
"done when" that can be checked. Documentation nobody owns is not written.
Write for the reader's language and setting: a cashier guide for Filipino staff may be in Filipino or Taglish with screenshots;
an API reference is in English.
-->

# Documentation Plan

## Documents to produce

| ID | Document | Audience | Owner | Due | Location and format | Done when |
|---|---|---|---|---|---|---|
| DOC-01 | README (setup, scripts, structure) | developers | documentation-writer | M1 | README.md | a fresh clone runs with the documented commands |
| DOC-02 | DESIGN.md | builders | frontend-specialist | M1 | DESIGN.md | tokens and rules used by the first screens |
| DOC-03 | API reference | integrators, frontend | backend-specialist | | | |
| DOC-04 | Runbook: deploy, restore, rotate secrets | operator | devops-engineer | | | |
| DOC-05 | User guide per role | end users | documentation-writer | | | |
| DOC-06 | Admin guide | client admin | documentation-writer | | | |
| DOC-07 | Privacy notice | data subjects | security-auditor | | | reviewed by the client's counsel or DPO |
| DOC-08 | CHANGELOG | client, developers | documentation-writer | every release | CHANGELOG.md | entry per release |
| DOC-09 | Handover pack (accounts, credentials procedure, contacts) | client | documentation-writer | launch | | client signs receipt |

<!-- Delete the rows that do not apply; add training material, video walkthroughs or printed quick cards if the users need them. -->

## Standards

<!-- Where docs live (repo /docs, client drive), format (Markdown, PDF export for the client), screenshots policy (updated when the screen changes), language, versioning with releases. -->

## Keeping docs current

<!-- Which changes require a doc update (tie to the definition of done in 08), and who checks at each milestone. -->
