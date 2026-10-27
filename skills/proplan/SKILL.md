---
name: proplan
description: "/proplan - Plan a whole system as a linked document set (goals, requirements, architecture, contracts, roadmap) in docs/proplan/<slug>. Supports full, --lite and update modes."
version: 3.2.0
---

# /proplan

A system spec builders can execute and reviewers can challenge.

```text
/proplan <brief>            full set
/proplan --lite <brief>     compact set
/proplan update <slug> <change>
```

## Documents

Folder: `docs/proplan/<slug>/`. Keep these filenames.

| File | Owner | Holds |
|---|---|---|
| 00-overview.md | lead | Summary, set, decisions, assumptions, changes |
| 01-goals.md | product-planner | G-, DG-, KPI- |
| 02-requirements.md | product-planner | R-, NFR-, scope |
| 03-architecture.md | architect | Boundaries, integrations per rule-04-system-integration |
| 04-data-model.md | database-engineer | Entities, constraints, lifecycle |
| 05-api.md | backend-engineer | API- contracts, auth, retries |
| 06-ux.md | ux-designer | S- screens, states, design direction |
| 07-security.md | security-engineer | TH- threats, permissions |
| 08-quality.md | qa-engineer | TC- acceptance coverage |
| 09-operations.md | devops-engineer | Release, config, recovery |
| 10-roadmap.md | product-planner | M milestones, T- tasks |
| 11-risks.md | product-planner | RK- risks |
| 12-documentation.md | docs-writer | DOC- deliverables |
| 13-glossary.md | lead | Vocabulary |
| adr/ADR-001-<decision>.md | architect | Decision and consequences |
| TRACEABILITY.md | generated | Coverage links |
| REVIEW.md | architect | RV- findings |

Lite set: 00, 01, 02, 03, 10, TRACEABILITY. In lite, 03 adds **Data model summary** and **API summary** (API IDs in its table) and 10 holds a short RK- table.

IDs and checker rules: [reference.md](./reference.md). Role inputs: [briefs.md](./briefs.md). Start files from [templates/](./templates/). [example/pos-lite/](./example/pos-lite/) is a format sample only.

## Steps

1. Read the request, repo and docs. For brownfield work, have `explorer` map the code into `notes/codebase-map.md`.
2. Ask once only about decisions that change the outcome. If style is unclear, ask one style question and keep writing the other documents.
3. Pick full or lite, state assumptions, and create only the needed files from templates.
4. Write goals and requirements, then architecture and contracts. Compare options only where a real choice is open.
5. Detail data, API, UX, security, quality and operations. Make roles and permissions agree across 04, 05 and 07.
6. Plan milestones and tasks from finished contracts, with owner, dependencies and verify line.
7. Reconcile the set and review it for realistic failures in REVIEW.md.
8. Build traceability:
   ```powershell
   python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --stage design
   python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --write-traceability
   ```
   Fix errors; judge warnings on meaning.
9. Keep `status: draft` until the user actually approves.

For changes, follow [update.md](./update.md).

## Output

Path, set, key decisions, delivery order, top risks, checker result, open questions, next milestone. If implementation was also requested, continue with `/orchestrate`.

## Before you finish, check

- [ ] Every file in the chosen set exists and IDs are stable.
- [ ] 03 states table ownership and sync design.
- [ ] TRACEABILITY.md was regenerated, not hand-edited.
- [ ] No invented approvals, dates, endpoints or research.
