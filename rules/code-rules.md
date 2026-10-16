---
name: code-rules
version: 2.8.2
priority: P0
trigger: always_on
description: Implementation and evidence policy for any stack. Distinguishes defects, missing evidence and optional heuristics without style gates.
---

# Implementation and Evidence

## Establish the implementation contract

Inspect the actual manifest, lockfile, entrypoints, tests and neighboring code. Preserve existing stack and behavior unless the request changes them. Select new dependencies for a concrete capability and verify their supported API/version from primary documentation; examples in the kit are not an instruction to upgrade.

Fix the layer that owns the defect. A local adapter, vendor override, dynamic inline value or wrapper can be appropriate when its purpose is explicit. Avoid accumulating overrides or suppressions that hide a broken contract. Update necessary callers, remove code made obsolete and keep unrelated rewrites out of the change.

Use names that communicate domain meaning, while preserving valid framework conventions. Keep cohesive code together rather than splitting it to satisfy arbitrary function/file lengths. Validate untrusted input and server-side authorization; preserve data integrity with appropriate transaction/retry boundaries and parameterized queries. Do not expose secrets in clients, logs or generated artifacts.

## Match evidence to consequence

| What changed | Useful verification |
|---|---|
| A harmless nonvisual edit | Read the immediate effect and affected references |
| Appearance or content layout, even one value | Inspect the affected render, wrapping, contrast and responsive state at relevant widths |
| Ordinary code behavior | Existing focused checks, types/build or meaningful behavior tests for the changed contract |
| Money, access, permissions, deletion, migration or critical shared logic | Relevant regression and integration/error paths, review of the consequential diff and appropriate project checks |
| Release or production state | Project release/build checks, authorized deployment, health and rollback evidence appropriate to the environment |

`python "KIT/scripts/checklist.py" . --quick` runs configured project checks; `--full` broadens scope and adds advisory scans. `verify_all.py` supports release evidence. Use the project commands directly when that is clearer. Labels tier 0–3 in references map to harmless, normal, consequential and release work; the table above controls actual depth.

Reuse a local server, or start its documented preview when useful and practical. Confirm the route/build being inspected. Without browser/runtime access, use available evidence and name the unverified behavior. Do not download a large toolchain simply to tick a box for a low-impact edit.

## Interpret the evidence honestly

Actual compiler errors, failing relevant tests, broken interactions or confirmed security/data defects need repair or an explicit unresolved report. Naming, stylistic lint and source regex heuristics are investigation leads; inspect their consequence before treating them as defects. Never change accepted aesthetics merely to satisfy a scan.

Report `PASS`, `FAIL`, `INCOMPLETE` or `SKIPPED` according to what ran. Exit zero and legacy `success: true` alone can accompany missing evidence. `verified` does not establish untested features, full coverage or production readiness. A configured test command can pass while covering little; make the scope clear.

Report kit health, working behavior and rendered craft separately. Tests or a version number cannot supply a design score. Requested comparisons use equal inputs, a stated rubric and preserved outcomes; see `browser-verification/comparison-testing.md`. Check test setup and targets before blaming the app.

Test stable observable behavior and important failure paths. Do not mirror implementation details or static wording to inflate counts. Re-run focused checks after changes that can affect them, then move toward delivery instead of repeatedly testing unchanged work.
