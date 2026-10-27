# Updating a proplan

Use this procedure for `/proplan update <slug> <change>`. Preserve the record of decisions and completed work while keeping the remaining plan executable.

## Trace the requested change

Read 00, the relevant source/plan sections and TRACEABILITY. A baseline checker run can separate existing structural problems from new ones. Identify affected goals, requirements, screen/API contracts, tasks/tests, threats, risks and ADRs.

For a material change, explain the impact concisely: what behavior changes, affected IDs/contracts, delivery effect and any consequential decision still open. Do not require a new approval checkpoint when the user already authorized the concrete change. Ask only for a missing product commitment, permission boundary or other decision the user must own.

## Edit without losing history

Keep existing IDs and allocate the next unused ID for new items. Removed requirements can remain `Priority: Won't` with the removal reason/version. Preserve completed tasks and their evidence; append replacement work instead of rewriting completion history. Use a superseding ADR for a materially changed accepted architecture decision and cross-link the two.

Update contracts in dependency order and assign disjoint paths when delegating. A changed visual direction keeps theme structure under rule-01-unified-theme-system; routine updates within that system need no new intake.

Use the plan's version convention consistently: major for incompatible architecture/Must-scope changes, minor for compatible requirements/tasks/estimates, patch for clarifications. Update changed document metadata and 00's changelog with affected IDs and rationale; project plan versions are distinct from the kit version.

## Validate the delta

Regenerate traceability with `python "KIT/scripts/proplan_check.py" docs/proplan/<slug> --write-traceability`. Resolve structural errors and assess warnings rather than inventing filler. Review changed assumptions, dependency cycles, criteria and cross-document names/roles. Use an independent review when its value warrants it and tools are available; otherwise state the review scope honestly.

Report the changed behavior/IDs, schedule or contingency effect, actual checker result and remaining decisions/evidence. Continue implementation if the active request already includes it; a plan-only update ends with the updated plan.

## Grow lite into full

For `/proplan update <slug> --full`, check the existing lite set, create missing 04–09 and 11–13 plus REVIEW from their templates, and ensure an ADR exists. Preserve identity while moving definitions to their full-set home:

- API definitions move from the 03 summary to headings in 05; 03 keeps references without redefining them.
- Risk definitions move from the 10 lite table to the 11 register; 10 links to them.
- Screen definitions, if present in a lite summary, move to 06 without changing numbers.
- The 03 data summary supplies 04; actual constraints and lifecycle detail are completed there.

Add full-set Must-requirement test coverage and domain detail, reconcile names/contracts, switch `set: lite` to `set: full` in 00 and record the version/change. Run `proplan_check.py docs/proplan/<slug> --full --write-traceability` and review the resulting set. More documents do not justify invented requirements or presumed legal obligations.
