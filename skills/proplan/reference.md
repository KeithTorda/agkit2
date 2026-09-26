# /proplan reference: IDs and checker

Part of `KIT/skills/proplan/SKILL.md`. The ID rules every /proplan agent follows and what `proplan_check.py` enforces.

## ID conventions

| ID | Meaning | Defined in | Defined as |
|---|---|---|---|
| G-01 | business goal | 01 | heading `### G-01 Name` |
| DG-01 | development goal (quality/engineering target) | 01 | heading |
| KPI-01 | success metric | 01 | first cell of the metrics table |
| R-001 | functional requirement | 02 | heading; body has `Priority:`, `Goals:`, `Story:`, `AC1: Given ... when ... then ...` |
| NFR-01 | non-functional requirement | 02 | heading; body has a number and `Serves DG-xx` |
| API-01 | endpoint | 05 (lite: 03) | heading in 05 with `Serves: R-xxx`; lite: first cell of the API table |
| S-01 | screen | 06 | first cell of the screen inventory table |
| TH-01 | threat | 07 | first cell of the STRIDE table |
| TC-001 | test case | 08 | first cell of the test case table, `Covers` column lists R-/NFR-ids |
| M1 | milestone | 10 | heading `### M1 Name (weeks)` |
| T-001 | task | 10 | `- [ ] **T-001** outcome` + `owner · estimate · depends · covers` line + `verify:` line |
| RK-01 | risk | 11 (lite: 10) | first cell of the register table |
| DOC-01 | document to produce | 12 | first cell of the table |
| ADR-001 | architecture decision | `adr/ADR-001-<slug>.md` | the file itself |
| RV-01 | review finding | REVIEW.md | first cell of the findings table |

Rules every agent follows: define an ID once, in its home document; cite IDs anywhere; never renumber or reuse an ID (a dropped requirement becomes `Priority: Won't` with a note); widths are fixed (R-001 not R-1).

What counts as a definition:
- **Headings**: a heading whose first token is an ID (`### R-001 ...`, `### API-03 ...`).
- **Table rows**: the first cell of a row defines the ID only when the table's header row starts with `ID` (`| ID | ... |`), or when the table is in that ID's home document (for example the `| KPI | Metric |` table in 01) and the ID is not already a heading there. Any other table whose first column holds IDs (a requirement-to-screen map in 06, a summary table in 02) only cites them, so it never causes a duplicate or wrong-home error. Use an `ID` header only for the table that defines the IDs.
- **Tasks**: the `- [ ] **T-001**` checkbox line.
- **Milestones**: `### M1 Name` headings in 10. A milestone reference is counted only in a heading, as a whole table cell (`| M2 |`), or next to the word "milestone" ("milestone M2", "M2 milestone", "Milestones M1..M3"); a bare "M4" in prose ("Apple M4 laptop") is not an ID.

## Checker

```powershell
python "KIT/scripts/proplan_check.py" docs/proplan/<slug>                         # set from 00-overview 'set:', else auto-detect
python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --write-traceability    # regenerate TRACEABILITY.md, then check
python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --lite --json
python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --stage design         # end of Phase 3
```

`--stage design` is for the end of Phase 3: it does not require 10-13, TRACEABILITY.md or REVIEW.md, skips the Must-requirement task and test coverage checks, and ignores references to T-, RK- and milestone IDs (they are defined in Phase 4). Everything else is checked. The default `--stage final` checks everything.

It fails (exit 1) on: missing files for the set; missing frontmatter keys or H1; bad ID syntax; IDs defined twice or outside their home; dangling references; a requirement without priority or without a Given/when/then line; a Must requirement with no task (and, full set, no test case); a task without owner, verify line or covered requirement; circular task dependencies; a goal no requirement serves; ADR files misnumbered or missing sections; a stale TRACEABILITY.md; an open blocker in REVIEW.md (a `Blocker` row whose Status starts with "open", any case). It warns on: empty sections, leftover placeholders or TBD, NFRs without a number, requirements with no goal, tasks without estimate, owners that are not kit agents (mark people `owner: Name (human)`), no buffer in the roadmap. Exit 2 = usage error.

## Handoff summary example

Phase 6 summary for the bundled lite example, in the exact line order SKILL.md prescribes:

```text
Kape Norte Counter POS plan ready: docs/proplan/cafe-pos/ (lite set, v1.0.0, checker PASS with 0 warnings)

What it delivers: a counter POS on one Android tablet for a one-branch café: menu with modifiers, cash and GCash (static QR +
reference number), SC/PWD discounts, Bluetooth receipts, voids with supervisor PIN, shift cash count, and a daily report on the
owner's phone. Selling continues offline and syncs later.
Architecture: offline-capable PWA + Laravel 12 API on a small VPS (ADR-001) - the only option that keeps selling during outages
and gives the owner reports from home without hardware in the café.
Scope: 12 requirements (11 Must), 6 NFRs; out: loyalty, inventory deduction, GCash API, multi-branch, BIR accreditation.
Development goals: 80% coverage on money modules; add-item 100 ms p95 on the tablet; WCAG 2.2 AA; 8 h offline with no lost or
duplicate orders.
Schedule: M1 foundation (Oct 8), M2 sell and pay (Oct 26), M3 control, reports, pilot (Nov 6), launch Nov 16; 19 tasks,
30 days + 5 days buffer. Critical path runs through printing (T-010) and sync (T-008, T-009).
Top risks: Web Bluetooth printer support (spike on day 1 of T-010); late tablet/printer purchase (models sent by Oct 5);
receipt wording approval (T-016 starts Oct 26).
Review: 7 findings, 6 fixed, 1 accepted (no kitchen display; owner confirmed).
Decisions for you: none.
Next: /orchestrate docs/proplan/cafe-pos M1
Not verified: VPS price and Singapore latency from Tuguegarao; the printer model's BLE profile.
```
