---
name: proplan
description: "Plan a system as linked goals, requirements, architecture, domain contracts and delivery milestones in docs/proplan/<slug>. Supports full, --lite and update modes with stable IDs and a structural checker."
version: 2.8.2
---

# /proplan

Create a coherent system specification builders can execute and reviewers can challenge. Use full mode for a requested comprehensive plan or substantial cross-domain decisions. Use `--lite` for a compact linked plan. A bounded feature can use plan-writing without a mandatory switch or approval ceremony.

```text
/proplan <system brief>
/proplan --lite <system brief>
/proplan update <slug> <change>
```

## Documents and contracts

Write to `docs/proplan/<slug>/` at the project root. Preserve these filenames and checker contracts; content depth follows the actual system.

| File | Owner | Purpose |
|---|---|---|
| 00-overview.md | coordinator | Summary, set/version, decisions, assumptions, index and changes |
| 01-goals.md | product-manager | G- business goals, DG- development goals, KPI- measures |
| 02-requirements.md | product-manager | R- requirements/acceptance, NFR- quality needs, scope |
| 03-architecture.md | solution-architect | Boundaries, quality drivers, integrations, rationale |
| 04-data-model.md | database-architect | Entities, constraints, queries and lifecycle |
| 05-api.md | backend-specialist | API- contracts, authorization, failure and retry behavior |
| 06-ux.md | ux-architect | S- screens/states, journeys and accepted design direction |
| 07-security.md | security-auditor | TH- threats, permissions, data handling and controls |
| 08-quality.md | test-engineer | TC- acceptance coverage and verification approach |
| 09-operations.md | devops-engineer | Release, configuration, recovery and observability |
| 10-roadmap.md | project-planner | M milestones and T- tasks with ownership/dependencies/verify |
| 11-risks.md | project-planner | RK- risks, triggers, mitigations and owners |
| 12-documentation.md | documentation-writer | DOC- deliverables needed by actual readers |
| 13-glossary.md | coordinator | Consistent product vocabulary |
| adr/ADR-001-<decision>.md | solution-architect | Durable architecture decision and consequences |
| TRACEABILITY.md | generated | Goal/requirement/contract/task/test coverage |
| REVIEW.md | plan-reviewer | RV- findings and their resolution |

Full mode uses the complete set. Lite mode uses 00, 01, 02, 03, 10 and TRACEABILITY; 03 includes **Data model summary** and **API summary**, with API IDs defined in its table, and 10 holds a short RK- risks table. An ADR and review artifact can still be useful in lite mode. Do not invent endpoints or screens for a system that does not have them; state why a domain is inapplicable in its full-set document.

Read [reference.md](./reference.md) for exact IDs, definitions and checker behavior. Templates in `templates/` preserve parseable headings and fields. `example/pos-lite/` is an illustrative checker fixture, not an assumed domain, legal policy, stack recommendation or real release report.

## Establish the brief

Read the request, relevant repository/docs and accepted decisions. Identify greenfield versus brownfield, audience, core outcomes and material constraints. In brownfield work map the actual system before proposing replacements; explorer-agent can return a map for `notes/codebase-map.md`.

Ask only for missing decisions that change the promised outcome or a consequential commitment. Before a new visual design ask one conversational style/reference question and wait unless answered or explicitly delegated. Carry the accepted answer into 06 and all worker briefs; do not repeat it per role. An unresolved visual choice need not block independent nonvisual discovery.

State the selected set and material assumptions, then create only its needed files from templates. Use a concise shared brief carrying goals, constraints, evidence, accepted decisions and open dependencies; no questionnaire, line count or persona/goal quota is required.

## Develop in dependency order

1. Establish goals, requirements and important UX/security constraints. Explore current code when present; distinguish observed facts, proposed targets and unresolved evidence.
2. Define architecture and cross-domain contracts. Compare credible alternatives when an actual choice is open. Ask the user for unresolved product commitments or consequential choices they must own; do not require a universal architecture approval. Record routine delegated technical decisions and rationale.
3. Detail the schema, API, UX, security, quality and operations appropriate to the selected set. Parallelize only independent questions/disjoint files with settled inputs; otherwise sequence them. The schema/API/security matrix and role names must agree before calling contracts ready.
4. Plan usable milestones and tasks from the completed contracts. Include real migration, recovery, docs and verification work, estimates with uncertainty when useful, and contingency tied to risks. Preserve stable IDs and checkable criteria.
5. Reconcile the whole set, then review it for realistic failure scenarios. Fix material contradictions and keep unresolved decisions visible. An independent reviewer is useful when available; sequential review is valid and must not be described as independent.

Read [briefs.md](./briefs.md) for domain inputs and safe delegation/fallback. Shared ownership has one writer per file; the coordinator reconciles small inconsistencies and records material changes. Avoid blanket phase concurrency when one document consumes another's unfinished contract.

## Validate structure and judgment

```powershell
python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --stage design
python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --write-traceability
python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --lite --json
```

Use design stage while detailed contracts exist but delivery/review files are unfinished. Regenerate traceability for the final set and resolve errors. Review warnings for actual meaning; do not invent numbers or irrelevant content merely to silence a heuristic. Structural consistency is not product correctness, legal compliance, cost verification or user acceptance.

Keep `status: draft` while unsettled; use a truthful review/ready status per project practice. `approved` requires actual approval. Do not fabricate user decisions, signoffs, research, dates or estimates.

## Handoff and updates

Report the path/set/version, intended outcome, major decisions, scope, delivery sequence, important risks, checker result and outstanding decisions/evidence. Keep the report proportional rather than requiring a fixed script. For a planning-only request, end with the next executable milestone. If the user authorized implementation as well, continue through orchestrate once genuine blocking decisions are settled.

For changes, read [update.md](./update.md). Preserve IDs, update affected contracts and changelog, regenerate traceability and review the delta. A plan task does not authorize unrelated live deployment or destructive data operations.
