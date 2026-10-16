# Proplan IDs and checker reference

Use this for machine-readable document contracts. The workflow in [SKILL.md](./SKILL.md) governs planning depth and decision handling; the checker validates structure and links rather than the quality of the product decision.

## Stable identifiers

| ID | Meaning | Home | Definition |
|---|---|---|---|
| G-01 | Business goal | 01 | Heading beginning with the ID |
| DG-01 | Development/quality goal | 01 | Heading beginning with the ID |
| KPI-01 | Success metric | 01 | First cell of the metric table |
| R-001 | Functional requirement | 02 | Heading; Priority and Given/when/then acceptance line |
| NFR-01 | Quality requirement | 02 | Heading; measurable criterion and relevant DG link |
| API-01 | Endpoint/action contract | 05; lite 03 | Heading with Serves line; lite API table row |
| S-01 | Screen/view | 06 | First cell of screen inventory |
| TH-01 | Threat | 07 | First cell of threat table |
| TC-001 | Acceptance test case | 08 | First cell of case table, Covers links R/NFR |
| M1 | Milestone | 10 | Heading beginning with the ID |
| T-001 | Task | 10 | Checkbox `- [ ] **T-001**` with owner, covers and verify |
| RK-01 | Risk | 11; lite 10 | First cell of risk register |
| DOC-01 | Documentation deliverable | 12 | First cell of document table |
| ADR-001 | Architecture decision | adr/ADR-001-<slug>.md | Numbered file with matching H1/frontmatter |
| RV-01 | Review finding | REVIEW.md | First cell of findings table |

Define each ID once in its home; references may appear elsewhere. Preserve fixed widths and never renumber/reuse identities during an update. Keep removed work as a truthful historical item when needed.

Headings define an ID only when it is the first token. Thus `### Wireframe: S-01 ...` references a screen already defined in the inventory. A table's first cell defines an ID when its first header is `ID`, or in the ID's home document when not already defined as a heading. Use other column orders or non-ID headers for summary/reference tables to avoid duplicate definitions.

Milestone references are recognized in headings, whole table cells or next to “milestone”; ordinary prose such as a device model is not automatically a milestone. Generated TRACEABILITY uses the stable markers `<!-- proplan:traceability:start -->` and `<!-- proplan:traceability:end -->`; do not edit their contents by hand.

## Task contract

```markdown
- [ ] **T-001** Implement the stated outcome
  - owner: backend-specialist · estimate: 1d · depends: - · covers: R-001
  - verify: <specific command or observation and expected result>
```

Use real IDs and an existing kit agent, or `Name (human)`, as owner. Dependencies must exist and be acyclic. Estimates are useful only with a basis; the checker warning does not justify invented precision. `[x]` requires actual completion evidence. A roadmap states contingency/buffer explicitly, including a justified zero if appropriate; no fixed percentage is policy.

## Run the checker

```powershell
python "KIT/scripts/proplan_check.py" docs/proplan/<slug>
python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --write-traceability
python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --stage design
python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --lite --json
```

The overview's `set:` selects full/lite unless explicitly overridden. Design stage omits later delivery/review files and task/test coverage checks; it ignores references to T-, RK- and milestones not yet defined. Final stage checks the complete selected set. `--strict` also fails on warnings.

Errors include missing set files/frontmatter/H1, invalid or duplicate/wrong-home IDs, dangling links, requirements without priority or Given/when/then criteria, Must requirements without tasks (and without cases in full mode), invalid task contracts/cycles, unserved goals, malformed ADRs, stale traceability and open blocker findings. Warnings include empty sections/placeholders, NFRs without numbers, requirements without goals, missing estimates, unknown owner names and missing buffer.

Exit 0 means no checker errors, not validated architecture, executed tasks or user approval. Exit 1 means errors (or warnings under strict); exit 2 means usage failure. Report the actual result and assess warnings in context. Qualitative criteria can be useful even if a numeric heuristic warns; never insert arbitrary numbers merely to obtain green.

## The bundled example

`example/pos-lite/` demonstrates linked IDs and parseable formats with a fictional cafe system. Its names, dates, signoffs, pricing, hardware assumptions and regulatory/tax rules are illustrative; they are not current verified advice. Use the checker to inspect structure and choose current project decisions from the actual brief/evidence.

At handoff describe the plan path/set/version, expected outcome, significant decisions, readiness, actual checker evidence and outstanding limits. A planning-only request can name `/orchestrate docs/proplan/<slug> M1` as the next step; a request that already includes building can continue without redundant approval.
