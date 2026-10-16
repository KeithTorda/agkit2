---
name: verify-changes
description: "Match completion claims to meaningful execution evidence proportional to the changed behavior and consequence. Use before saying work functions or a bug is fixed, and for /verify."
version: 2.8.2
---

# Verify Changes

Evidence must support the actual claim. A successful build proves buildability; it does not prove a payment is correct, permissions hold or a page looks right. Use code-rules for shared policy and project requirements rather than duplicating a separate gate here.

## Choose evidence that matters

| Change | Useful evidence |
|---|---|
| Nonfunctional prose/comments | Read changed text and relevant links/contracts |
| Visible copy/style/layout | Render the affected screen/state and inspect readability, wrapping and fit |
| Bug repair | Reproduce the failing input, then observe the corrected and relevant neighboring behavior |
| Logic or feature | Relevant tests and important success/error behavior |
| API or integration | Appropriate real request and response/denial; identify mocked/external boundaries |
| Config/build | Load/build with the changed configuration |
| Refactor | Existing relevant tests and affected behavior/compatibility |
| Auth/money/data migration | Targeted boundary/integrity tests and suitable broader checks/review |
| Generated document | Render and inspect with see-doc |

Use existing project commands where they provide real confidence. Add tests for meaningful behavior, not to mirror an obvious reversible edit. Scope by consequence and affected paths; a tiny diff can affect global typography or authorization.

## Execute and interpret

```powershell
python "KIT/scripts/checklist.py" . --quick
python "KIT/scripts/checklist.py" . --full
```

The quick runner scopes appropriate tools to changed files; an empty diff can result in no work. Use `--all-files` when appropriate to include already-committed relevant code. Broader checks and `verify_all.py . --url <running-url>` can support substantial work/releases when they fit the project and prerequisites.

Read individual results and `outcome` (`PASS`, `FAIL`, `INCOMPLETE`, `SKIPPED`), `verified` and `not_verified`. Legacy `success` or exit zero can mean no blocking finding despite incomplete/skipped evidence. Missing tools, unapplied checks and all-inapplicable runs are not passes.

Fix introduced defects within scope and rerun affected checks. Investigate correctness, type/build, security/data-boundary and test failures before claiming completion. Judge heuristic style warnings against the approved design; do not reshape the user's work simply to silence a cosmetic rule. Identify pre-existing failures and keep independent progress moving.

## Render and report

For visible work use browser-verification: reuse/start the appropriate server, render relevant widths/states, inspect against the accepted brief and exercise changed interactions. Refine observed defects and inspect again. An unavailable runtime/browser limits the visual claim; diagnose the precondition and state it explicitly.

Report what changed, what actually ran/was observed, its result and material limits. Never invent counts, screenshots, requests or interactions; never promise zero future errors.
