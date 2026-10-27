---
name: testing-patterns
description: Use when the user asks to write tests, plan test coverage or fix failing or flaky tests, in Pest/PHPUnit, Vitest/Jest or Playwright.
version: 3.2.0
---

# Testing Patterns

Write the smallest set of tests that proves the behavior users and money depend on. Tests are written and run when the user asks (kit-core).

## Steps

1. Read the existing test setup: framework, folders, factories, database reset method and the test script in `package.json` or `composer.json`. Use that setup.
2. List cases per requirement: success, invalid input, permission denied, empty result, boundary values (zero, max, negative), duplicate submit, and the other system being down.
3. Pick the lowest level that proves each case:
   - Pure logic (VAT, discounts, status changes): unit test.
   - Endpoint with database and auth: feature/integration test on a real test database.
   - Component behavior: Testing Library, query by role and label.
   - A few critical journeys (login, sale, receipt): Playwright.
4. Arrange data with factories inside each test. Each test runs alone and in any order.
5. Assert what users and other systems see: status code, response fields, database rows, the `outbox` row created, visible text.
6. For integrations (rule-04-system-integration), test that a repeated idempotency key returns the first result without a second record, and that a duplicate webhook changes nothing.
7. Mock only external boundaries (ERP API, payment gateway, mail). Keep the code under test real.
8. For a regression, write the test so it fails on the original bug first, then fix.
9. Flaky test: look for shared state, order dependence and timing. Replace fixed sleeps with waits on real readiness.

## Stack notes

- Laravel: Pest or PHPUnit with `RefreshDatabase`, `actingAs()`, `assertDatabaseHas`, `Http::fake()`, `Queue::fake()`.
- JS/TS: Vitest or Jest; MSW for HTTP mocks.
- Playwright: `getByRole` locators, isolated test data, a fresh context per test; scope table locators to the intended table.
- Visual or responsive checks on request: [browser-verification](../browser-verification/SKILL.md).

## Helpers

```powershell
python "KIT/skills/testing-patterns/scripts/test_runner.py" .
python "KIT/skills/testing-patterns/scripts/playwright_runner.py" http://localhost:3000 --screenshot
```

`test_runner.py` detects Node, Python and PHP suites (`--coverage`, `--json`, `--timeout`); its JSON marks each suite PASS, FAIL, INCOMPLETE or SKIPPED. `playwright_runner.py` is a smoke and basic accessibility check (`--mobile`, `--a11y`, `--json`). SKIPPED or a zero-test run counts as not verified.

## Before you finish, check

- [ ] Money, permissions and sync idempotency have tests where they are in scope.
- [ ] Each test builds its own data and passes when run alone.
- [ ] Assertions check observable results, not private methods or CSS classes.
- [ ] The report lists only what actually ran, with pass, fail and skip counts.
