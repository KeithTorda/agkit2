---
name: testing-patterns
description: Select and write tests that protect changed behavior and important failure paths using the project's tools. Use for test implementation, regression coverage or test strategy; avoid implementation-mirroring tests and fixed coverage quotas.
version: 2.8.2
---

# Behavioral Testing

Choose the cheapest reliable observation of the contract at risk. Inspect existing tests, environment, data isolation and CI before selecting a framework. Keep working tools; a reversible low-impact edit rarely warrants new tests or framework installation.

## Match test level to uncertainty

| Contract | Useful evidence |
|---|---|
| Pure calculation, parsing or transition | Focused unit test over meaningful inputs/boundaries |
| Database query, auth boundary, API serialization | Integration test across the real boundary or a faithful test service |
| Form/component interaction | Accessible role-based interaction and observable state/result |
| Critical cross-system user flow | A small deterministic browser/end-to-end journey |
| Styling/layout | Rendered inspection at relevant widths, with focused visual regression only when maintainable |

No fixed pyramid percentages apply to every project. Use real database engines for engine-specific SQL/isolation when it matters. Mock a boundary only when the behavior being tested is not that boundary; an always-successful ORM mock cannot prove transactions or authorization queries.

## Design meaningful cases

Arrange only needed state, perform an operation and assert the result users/consumers rely on. Cover important success and failure paths: invalid input, denied access, empty/duplicate results, partial failure, retries or concurrency when relevant. Do not reproduce every implementation branch or assert private helper names/call order without a contract reason.

Keep state isolated with test-specific data and deliberate cleanup. Use deterministic clocks/seeds where needed; do not make production behavior depend on test-only assumptions. Avoid real credentials, customer data, uncontrolled external writes and sleep-based timing.

TDD can help uncertain behavior: watch a new test fail for the intended reason, implement, then simplify. It is a useful technique rather than a mandatory ceremony for every edit. Regression tests should fail on the original defect when practical.

## Browser testing

Use stable accessible locators and retrying assertions tied to real readiness. Avoid fixed delays and arbitrary retries that hide races. Handle test authentication, server startup, isolated data and cleanup through existing fixtures. Review console/runtime errors and expected failure states; a screenshot alone cannot prove an interaction works.

Test the promised interaction contract, not only its opening toggle. For an overlay that blocks the page, exercise keyboard focus while open, dismissal and return to the opener; a visible backdrop and correct expanded state do not prove covered controls are unreachable. Keep nonmodal disclosures in ordinary page navigation rather than testing every menu as a modal.

Start independent cases from a saved clean URL or an appropriately isolated browser context. Reloading the current page can preserve query-string filters or other persisted state, leaking one test's state into the next. Reset only the state the case owns and verify its starting conditions before asserting results.

Scope table locators to the semantic task region and intended table or `tbody`, then verify identifying headers or representative row data before checking geometry, row counts, sorting, or last-column access. The first table in a document may be a visually hidden accessible chart-data table rather than the orders table under test.

Investigate failures as uncertain product/test evidence. Preserve the original report and useful traces/screenshots, identify whether the cause belongs to the app, harness, or environment, and repair that layer. For example, confirm expected local-server favicon noise separately from application request failures; correct leaked test state or a wrong table locator in the harness. Rerun all affected conditions with the same corrected checks and explain the correction. Retry may collect diagnostics, but repeated pass-on-retry is not a clean guarantee.

Use [browser-verification](../browser-verification/SKILL.md) for actual-size legibility, responsive layout, and scroll usability. Passing controls and contained overflow do not establish visual quality. Requested paired output comparisons have an optional [comparison workflow](../browser-verification/comparison-testing.md); they are not required for routine changes.

## Existing helpers

```powershell
python "KIT/skills/testing-patterns/scripts/test_runner.py" .
python "KIT/skills/testing-patterns/scripts/playwright_runner.py" http://localhost:3000 --screenshot
```

`test_runner.py` detects supported installed Node, Python and PHP suites. Supports `--coverage`, `--json`, `--timeout`. Inspect which suites actually ran: JSON distinguishes PASS, FAIL, INCOMPLETE and SKIPPED with a verified flag. Missing dependencies, absent suites or a known zero-test run do not establish a pass; a suite failure or timeout is failure. The kit checklist also runs tests, so avoid duplicate runs without a reason.

`playwright_runner.py` is a smoke/quick-accessibility helper, not a complete accessibility or browser suite. Supports `--mobile`, `--a11y`, `--screenshot`, `--screenshot-dir`, `--timeout-ms`, `--json`. It flags page-load/runtime/basic semantic issues. Missing Playwright/browser produces SKIPPED/NOT VERIFIED even with exit zero. Existing suite commands, such as configured Playwright/Vitest/pytest/Pest scripts, remain authoritative for their scope.

Report passed/failed/skipped scopes honestly. After relevant checks pass, broaden only for new changes, failures or unresolved risks. Use `systematic-debugging` for unclear failures and `adversarial-review` for an independent contract review.
