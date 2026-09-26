# /proplan update <slug> <change>

Part of `KIT/skills/proplan/SKILL.md`. A plan is a living document: change it through this procedure so IDs, traceability and the changelog stay true.

## Steps

1. **Read** 00 (version, changelog), TRACEABILITY.md, and the documents the change names. Run the checker first so you start from a known state.
2. **Classify** the change: new requirement, changed requirement, removed requirement, new constraint or NFR, architecture change, schedule or resource change.
3. **Impact.** Walk the traceability chain from the entry point (G → R → S/API → T → TC, plus ADRs, TH and RK that cite the ids). Show the user a short table before editing:

   ```text
   | ID | Doc | Effect |
   | R-013 (new) | 02 | add: loyalty stamps, Should, G-01 |
   | S-07 (new), API-09 (new) | 06, 05 | add |
   | T-020..T-022 (new) | 10 | add to M3; M3 +3 d, buffer 5 d -> 2 d |
   | TC-031 (new) | 08 | add |
   | RK-06 (new) | 11 | buffer below 10% |
   ```

   An architecture change needs a new ADR that supersedes the old one, and the checkpoint again.
4. **Edit** through the owning agents (subagents for large changes, yourself for small ones). Never renumber; new ids take the next free number; a removed requirement becomes `Priority: Won't` with "Removed in vX.Y.Z: reason"; completed tasks (`[x]`) are never deleted.
5. **Version.** MAJOR: architecture or Must scope changed. MINOR: requirements, tasks or estimates changed. PATCH: wording. Bump 00's `version` and add a changelog row with the affected ids; bump `version` and `updated` on each changed document.
6. **Check.** `--write-traceability`, fix errors. MINOR or MAJOR changes get a plan-reviewer pass on the delta (findings appended to REVIEW.md).
7. **Report**: what changed, the impact on dates and buffer, new decisions for the user, next step.

## Upgrading lite to full: `/proplan update <slug> --full`

Use when a lite plan outgrows its set (more roles, money or personal data, an integration, a second developer).

1. **Check first.** Run `python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --lite`; start from a passing lite set.
2. **Create the missing documents** from the templates: `04-data-model`, `05-api`, `06-ux`, `07-security`, `08-quality`, `09-operations` (Phase 3 agents, one document each, `workspace: share`), then `11-risks`, `12-documentation` (Phase 4 agents), `13-glossary` and `REVIEW.md` (coordinator and plan-reviewer). `adr/` becomes required: make sure ADR-001 exists.
3. **Move IDs to their home documents without renumbering.**
   - API rows: each `API-xx` row in 03 "API summary" becomes a `### API-xx` heading in 05 with the same number and its `Serves:` R-ids; 03 keeps a one-line pointer to 05 and cites the ids without defining them (no table whose first column is `ID`).
   - Risk rows: each `RK-xx` row in 10's risks table moves to the register in 11 with the same number (add category, score, trigger and status); 10 keeps a pointer to 11.
   - Screens: if 03 defined `S-xx`, move them to 06's screen inventory the same way.
   - The "Data model summary" in 03 is the input for 04; 03 keeps the summary or a pointer.
4. **Fill the full-set gaps**: a test case (TC-) for every Must requirement in 08, a threat and matrix row for every Must flow with money, personal data or authorization in 07.
5. **Switch the set.** Change `set: lite` to `set: full` in 00, bump the MAJOR version, add a changelog row ("upgraded to full set; API-01..API-08 moved to 05, RK-01..RK-04 moved to 11").
6. **Check.** `python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --full --write-traceability` until it passes (the full set also requires a TC for every Must R and a REVIEW.md), then a plan-reviewer pass on the new documents.
