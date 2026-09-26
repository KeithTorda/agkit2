---
name: proplan
description: "/proplan - Professional system planning: business and development goals, requirements, architecture with an ADR checkpoint, data, API, UX, security, quality, operations, roadmap and documentation plan, written by native planning subagents into docs/proplan/<slug>/ and checked end to end by proplan_check.py. Use for a new client system or a large feature; --lite for small systems; '/proplan update <slug>' to change an existing plan."
version: 2.5.0
---

# /proplan

Plans a system the way a small professional team would before building it: what the client needs and why, what "good" means in numbers, how it is built and why that way, how it is tested, deployed and documented, and in what order the work happens. The output is a folder of short, linked documents that `/orchestrate` executes milestone by milestone.

The coordinator (you, the main agent) runs the phases, briefs the subagents, holds the one checkpoint with the user, reconciles the documents, and reports. Subagents write documents; they do not talk to the user.

## Usage

```text
/proplan <system idea>                  full set (client systems, anything with money, personal data or several roles)
/proplan --lite <system idea>           lite set (small systems, internal tools, one or two roles, one developer)
/proplan update <slug> <change>         change request against an existing plan
```

"Proceed", "no questions" or "just decide" in the request means: skip the intake questions and the architecture checkpoint, choose the recommended option, and record that you did.

| Need | Use |
|---|---|
| A feature or fix in an existing app, a few days of work | `/plan` (one file in `docs/plans/`) |
| A small system: few roles, one developer, weeks of work | `/proplan --lite` |
| A client system, several roles, money, personal data, integrations, or a team | `/proplan` |

If the request is clearly `/plan`-sized, say so in one line and offer it; do what the user chooses.

## Output

Exactly this layout, in the project root (monorepo: repository root):

```text
docs/proplan/<slug>/
  00-overview.md        coordinator          summary, doc index, decisions, assumptions, checkpoint record, version + changelog
  01-goals.md           product-manager      business goals G-01.. (SMART), development goals DG-01.., KPIs KPI-01..
  02-requirements.md    product-manager      stakeholders, personas, scope in/out, R-001.. (story, Given/When/Then, MoSCoW), NFR-01..
  03-architecture.md    solution-architect   context, C4 level 1-2 (mermaid), components, integrations, stack with reasons
  04-data-model.md      database-architect   entities, erDiagram, tables/columns/indexes/constraints, retention
  05-api.md             backend-specialist   endpoints API-01.., request/response, auth, errors, versioning
  06-ux.md              ux-architect         journeys, sitemap/IA, screen inventory S-01.., key flows, wireframe specs, DESIGN.md direction
  07-security.md        security-auditor     STRIDE threats TH-01.., roles x actions matrix, privacy (RA 10173), secrets, audit log
  08-quality.md         test-engineer        test pyramid, test cases TC-001.. mapped to R-ids, budgets, a11y target, definition of done
  09-operations.md      devops-engineer      environments, CI/CD, deploy, backups, monitoring, rollback
  10-roadmap.md         project-planner      milestones M1.., tasks T-001.. (owner, estimate, depends, covers, verify), critical path, gantt
  11-risks.md           project-planner      risk register RK-01.. (likelihood, impact, mitigation, owner)
  12-documentation.md   documentation-writer docs to produce during the build DOC-01.., owners, due points
  13-glossary.md        coordinator          terms and acronyms (product-manager seeds them in its return)
  adr/ADR-001-<slug>.md solution-architect   Context / Options / Decision / Consequences
  TRACEABILITY.md       generated            G -> R -> S/API -> T -> TC matrix (proplan_check.py --write-traceability)
  REVIEW.md             plan-reviewer        red-team findings RV-01..; coordinator fills Status and Checker output
  notes/codebase-map.md coordinator          brownfield only: the map explorer-agent returns, saved verbatim
```

Lite set: `00`, `01`, `02`, `03` (with "Data model summary" and "API summary" sections; API-01.. defined there), `10` (with a short risks table, RK-01..), `TRACEABILITY.md`. One ADR for the main decision is recommended; `adr/` is optional in lite.

Templates for every file: `KIT/skills/proplan/templates/` (`00-overview.md` ... `13-glossary.md`, `adr-template.md`, `traceability-template.md`, `review-template.md`). Each has the section headings, the ID rules and guidance in `<!-- -->` comments. A complete lite example that passes the checker: `KIT/skills/proplan/example/pos-lite/`. Before the first `/proplan` in a session, read only its `00-overview.md` and `10-roadmap.md` for the level of detail; each brief points a subagent to the one example file closest to its own document.

## IDs and checker

IDs link the documents end to end (G-01, R-001, API-01, S-01, TC-001, M1, T-001, RK-01 ...). Define an ID once, in its home document; cite it anywhere; never renumber or reuse one; widths are fixed (R-001, not R-1). The ID table, what counts as a definition, and the full list of checks: `KIT/skills/proplan/reference.md`.

```powershell
python "KIT/scripts/proplan_check.py" docs/proplan/<slug>                         # set from 00-overview 'set:', else auto-detect
python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --write-traceability    # regenerate TRACEABILITY.md, then check
python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --lite --json
python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --stage design          # end of Phase 3
```

Exit 0 = no errors (warnings allowed; `--strict` fails on them), 1 = errors, 2 = usage error. The checker verifies links, not judgment; plan-reviewer does the judging.

## Phases

```text
0 Intake -> 1 Discovery (parallel, read-only) -> 2 Architecture decision [CHECKPOINT] -> 3 Detailed design (parallel, disjoint docs)
  -> 4 Delivery plan -> 5 Review (adversarial) + checker -> 6 Handoff (/orchestrate ... M1)
```

Lite runs the same spine with fewer agents: see "Lite mode" below.

### Phase 0 - Intake (coordinator)

1. **Read first.** `.agents/memory/MEMORY.md`, `DESIGN.md`, `README`, and `docs/` if they exist. If `docs/proplan/<slug>/` already exists for this system, switch to update mode.
2. **Greenfield or brownfield.** Code in the workspace that the system will extend or replace = brownfield: Phase 1 adds `explorer-agent` (and `code-archaeologist` for legacy code without tests or docs), and every document describes current state and target state.
3. **Set.** `--lite` given, or the system is small (one or two roles, no integrations beyond one payment or email, one developer, under about 6 weeks): lite. Otherwise full. State the choice in one line; the user can override.
4. **Questions.** Ask only what changes the plan and cannot be inferred. One message, at most 5 questions (the intake is the one place the kit allows more than 3), each with your recommended default, so "defaults are fine" is a complete answer. Typical: primary users and roles; the must-have outcome and deadline; hosting and budget constraints; existing systems or data to import; integrations (GCash, SMS, government systems). If the request already answers them, or the user said "proceed", ask nothing: write the assumptions into 00 and continue.
5. **Slug and folder.** Slug: 2-4 words, kebab-case, at most 30 characters (`cafe-pos`, `barangay-portal`). Create `docs/proplan/<slug>/` and `adr/`. Copy the templates for the set; fill 00's frontmatter (`set`, `title`, `project`, `version: 0.1.0`, `status: draft`).
6. **Intake summary.** Write a 10-20 line intake summary (who, problem, users, constraints, deadline, budget, stack preference, integrations, set, greenfield/brownfield, assumptions). Every brief below includes it verbatim. It is the shared truth for all subagents.

### Phase 1 - Discovery (parallel, read-only except their own documents)

One parallel batch: `product-manager` (01, 02; returns glossary terms), `ux-architect` (discovery notes in 06), `security-auditor` (discovery notes in 07), and `explorer-agent` if code exists. explorer-agent stays read-only: it returns the codebase map in its reply and you save it to `docs/proplan/<slug>/notes/codebase-map.md`. Per-agent brief additions: `briefs.md`.

When they return: read 01 and 02 yourself, check that Must requirements match the intake, feed the UX and security findings back as requirements (a missing role, a missing NFR for privacy) through product-manager, or amend 02 yourself if the change is small. Settle open questions that block architecture: ask the user now only if the answer changes the architecture; otherwise record the assumption.

### Phase 2 - Architecture decision (checkpoint)

1. Brief `solution-architect` with the intake summary, 01, 02, the discovery notes and (brownfield) the codebase map. It writes `adr/ADR-001-<slug>.md` with status `proposed` and 2-3 real options, and a draft `03-architecture.md` for the recommended option.
2. **CHECKPOINT.** Present the options to the user in one compact message and wait for a choice:

   ```text
   Architecture for <system> - pick one (recommended: A)
   | Option | How it works | Good at | Costs you | Rough cost |
   |---|---|---|---|---|
   | A ... | ... | ... | ... | ... |
   | B ... | ... | ... | ... | ... |
   | C ... | ... | ... | ... | ... |
   Why A: <one or two sentences tied to the top NFRs>.
   Reply A, B, C, or "proceed" for A.
   ```

   If the user already said "proceed", choose the recommended option without waiting.
3. Record the choice: ADR status `accepted` with date and decider; 00 "Architecture checkpoint" section. If the user chose a non-recommended option, `solution-architect` revises 03 for it. Further hard-to-reverse decisions (auth model, multi-tenancy, offline strategy) get their own ADRs, numbered in order.

### Phase 3 - Detailed design (parallel, one document per agent)

Six agents in one parallel batch with `workspace: share` (the documents are disjoint files, so no worktrees are needed): database-architect 04, backend-specialist 05, ux-architect 06 (complete), security-auditor 07 (complete), test-engineer 08, devops-engineer 09. What each reads and adds: `briefs.md`. Each writes only its own document and reports cross-document needs as findings (for example, an `audit_events` table in 04 for the security auditor).

Then run a **consistency sweep** yourself: entity and field names match across 04, 05, 06; role names match across 02, 05, 06 and the 07 matrix; every Must R-id has an endpoint or screen and a TC; threats in 07 point to an NFR, R or planned mitigation, and 07's privacy NFRs exist in 02; 09's backup and rollback cover the migrations 04 implies. Fix small mismatches yourself; send larger ones back to the owner with the exact conflict (doc, ID, both versions). Then run `python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --stage design` and fix every error (it skips what Phase 4 writes: 10-13, TRACEABILITY, REVIEW, task coverage, T-/RK-/milestone references).

### Phase 4 - Delivery plan

1. `project-planner` writes 10-roadmap and 11-risks from all documents, in the formats of `templates/10-roadmap.md` and `templates/11-risks.md` (task line, sizing, buffer, register columns). Milestones end in something the client can use; DESIGN.md, CI, backup and documentation work are real tasks.
2. Then `documentation-writer` writes 12-documentation against the milestones in 10.
3. You write 13-glossary from the terms the agents reported, write 00-overview (summary, key decisions, assumptions, open questions, next step, changelog), then run `python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --write-traceability` and fix every error.

### Phase 5 - Review

1. Brief `plan-reviewer` (it wrote none of the documents). It red-teams the set with the failure checks in its agent file and writes the findings in `REVIEW.md` from the template.
2. Fix the findings: small ones yourself, larger ones through the owning agent with the finding as the brief. You set each finding's Status: `fixed` (with the plan version) or `accepted` (who accepted it and why). Findings that need the user's call go to "Decisions for the user"; ask them in the handoff, at most 3.
3. Run `python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --write-traceability` until it passes; fix each warning or list it as accepted in REVIEW.md "Checker output" (yours to fill).
4. Set every document's `status: in-review` (the user approves; then `approved`).

### Phase 6 - Handoff (to the user)

Reply with the summary below; do not paste documents into the chat. Then stop; the build starts when the user runs `/orchestrate docs/proplan/<slug> M1`. After the user approves, set statuses to `approved`.

Use exactly these lines: plan path with set, version and checker result; What it delivers; Architecture; Scope; Development goals; Schedule; Top risks; Review; Decisions for you (at most 3, each with a recommended answer, or "none"); Next; Not verified.

A filled example of the summary: `KIT/skills/proplan/reference.md` ("Handoff summary example").

## Subagent briefs and fallback

Every subagent gets a complete brief: the intake summary verbatim, decisions so far, what to read, the one file it may write, the IDs it defines, what is untrusted, and a return format under 300 words. The skeleton, the per-phase additions and inputs for each agent run, workspace modes, and the order to play the roles yourself when `invoke_subagent` is not available are in `KIT/skills/proplan/briefs.md`. Read it before Phase 1.

## Lite mode

| Phase | Lite |
|---|---|
| 0 | Same; questions usually 0-3 |
| 1 | product-manager (01, 02) + explorer-agent if code exists; UX and security concerns go into 02 as NFRs and requirements |
| 2 | solution-architect: 03 with data model summary and API summary; one ADR for the main decision; checkpoint as normal (two options are enough) |
| 3 | skipped |
| 4 | project-planner: 10 with a short risks table (RK-01..); no 11, 12, 13 |
| 5 | plan-reviewer reviews and returns findings in its reply (REVIEW.md optional); you fix; `proplan_check.py docs/proplan/<slug> --lite --write-traceability` passes |
| 6 | Same summary |

A lite plan can grow into a full one later: `/proplan update <slug> --full` (procedure in `update.md`).

## Updating a plan

`/proplan update <slug> <change>`: show the impact on IDs as a table, edit through the owners without renumbering, bump the version with a changelog row, regenerate traceability, review the delta. Procedure: `KIT/skills/proplan/update.md`.

## Rules

- Plans are files. The chat carries the checkpoint, the questions and the summary, never the documents.
- The coordinator owns consistency. Subagents write one document each; two subagents never write the same file. During reconciliation (the Phase 3 sweep, Phase 4 wrap-up, Phase 5 fixes) the coordinator may edit any proplan document for small fixes and says which in 00's changelog; larger changes go back to the owner.
- Numbers over adjectives in every document: a requirement, NFR or goal without a checkable value is a finding.
- Design direction in 06 is guidance agreed with the client; accessibility targets are firm (`design-rules`).
- Security and privacy are planned, not bolted on: every Must flow involving money, personal data or authorization has a threat, a matrix row and a test case in the full set.
- Keep it proportional: a 3-week internal tool does not need a 12-page security document. Short, specific sections beat long generic ones; delete template sections that do not apply and say why in one line.
- Never claim the checker passed without running it; paste its result line in the summary.
