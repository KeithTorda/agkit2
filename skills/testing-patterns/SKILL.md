---
name: testing-patterns
description: Testing strategy and practice - which changes need tests, the test pyramid, AAA, the TDD loop, mocking at boundaries, Vitest and node:test, pytest, Pest for Laravel, and Playwright end-to-end tests, with the kit's test and smoke runners. Use when writing or reviewing tests, choosing a framework, practising red-green-refactor, or deciding whether a change needs tests.
version: 2.5.0
---

# Testing Patterns

Tests are the executable specification for logic that matters. When to write them follows `code-rules`: write or update tests for logic that money, auth, permissions or data integrity depend on, and when the user asks; otherwise judge whether a test would catch a real regression. A static component or a copy change usually does not need one.

## 1. Pyramid

| Level | Share | Covers | Speed |
|-------|-------|--------|-------|
| Unit | Most | Pure functions, validation, business rules (totals, VAT, stock, grading), reducers, isolated components | Milliseconds |
| Integration | Some | Route handlers, Server Actions and controllers, queries against a real test database, component + provider trees | Seconds |
| E2E | Few | Critical journeys in a real browser: log in, make a sale, submit a registration, the flow the client cannot lose | Slow; run before release and on CI |

Choose a test's level by the boundaries it crosses: pure logic → unit; one real boundary you own (a route, a query) → integration; a whole journey → E2E. Write each behaviour at the lowest level that still exercises the real risk. High unit coverage with no E2E can still ship a broken checkout; an all-E2E suite is too slow to run on every change.

## 2. AAA structure

| Step | Purpose |
|------|---------|
| Arrange | Build the input and dependencies (factories, fixtures, fakes) |
| Act | Call the one thing under test |
| Assert | Verify the observable outcome, ideally one behaviour per test |

Name tests by behaviour: `returns 404 when the user does not exist`, `rejects a sale when stock is insufficient`.

## 3. TDD loop

1. Red: write the smallest test that fails for the right reason, and watch it fail. A test that passes immediately may be testing nothing.
2. Green: the minimum code that makes it pass.
3. Refactor: improve names and structure with the tests green.

TDD pays off for bug fixes (reproduce the bug in a test first), business rules and new modules with clear inputs and outputs. For spikes and layout work, write the code first and add tests for the logic that emerged.

## 4. What to cover

- Unit: business logic, edge cases (empty, zero, negative, very large, rounding), error handling. Skip framework code, third-party libraries and trivial getters.
- Integration: request and response shape, status codes (200, 400, 401, 403, 404, 422), authorisation (user A cannot read user B's record), transactions and rollbacks, external-service contracts. Reset state per test.
- E2E: happy-path journeys, login, payment, deep links. Role-based locators (`getByRole`, `getByLabel`) first, `data-testid` when no accessible name exists; rely on auto-waiting, not sleeps; give every test its own state.
- Visual regression: worth it for design systems and stable marketing pages; low value for dynamic content.

## 5. Mock at the boundary, not the code under test

Mock the seams your code talks to but does not own — third-party APIs, the network, the clock, randomness. Use a real test database in integration tests and an in-memory fake in unit tests. Wrap a third-party client in a thin adapter and fake the adapter, so a library upgrade does not rewrite your tests. Two failure modes: mocking the logic under test (the test proves nothing), and mocking your own code so deeply that tests assert call sequences instead of outcomes — green while the behaviour is wrong, broken on every refactor.

```ts
// Over-mocked: asserts calls, restates the implementation, stays green even if the total is wrong
const repo = { save: vi.fn() }, gateway = { charge: vi.fn() }
await createOrder({ items }, { repo, gateway })
expect(gateway.charge).toHaveBeenCalledWith(100)
expect(repo.save).toHaveBeenCalled()

// Mock only the external boundary, use a real fake for what you own, assert the outcome
const repo = new InMemoryOrderRepo()
const gateway = { charge: async () => ({ id: 'ch_1', status: 'paid' }) }
const order = await createOrder({ items }, { repo, gateway })
expect(order.total).toBe(100)
expect(await repo.findById(order.id)).toMatchObject({ status: 'paid' })
```

Vocabulary: stub = fixed return value; spy = records calls; mock = asserts expectations; fake = simplified working implementation. Reach for a fake before a mock.

## 6. Frameworks

| Stack | Default | Command |
|-------|---------|---------|
| Node / TypeScript | Vitest (3.x or later) or `node:test` (built in, Node 24) | `npx vitest run`, `node --test "src/**/*.test.ts"` |
| React / Next.js | Vitest + React Testing Library (jsdom, or Vitest browser mode for real-browser components); Playwright for E2E | `npx vitest run`, `npx playwright test` |
| Python | pytest (+ `pytest-asyncio`, httpx `ASGITransport` for FastAPI; details in `python-patterns`) | `uv run pytest` or `python -m pytest` |
| PHP / Laravel 12 | Pest (PHPUnit underneath; PHPUnit alone in older projects) | `php artisan test`, `vendor/bin/pest` |

Async Server Components are not supported by React Testing Library; cover them with E2E tests and unit-test the data functions they call.

`test_runner.py` detects every suite and runs the ones that can run: Node - `npm test` when `package.json` has a real test script (the npm-init placeholder is ignored), else local Vitest or Jest; PHP - `php artisan test`, `vendor/bin/pest` or `vendor/bin/phpunit`; Python - pytest when installed, else `python -m unittest discover` (only when test files exist). Suites run with `CI=true` so watch modes exit. A suite whose tool or dependencies are missing is reported as NOT RUN with the fix - a note for the report, not a pass. Flags: `--coverage`, `--json`, `--timeout SECONDS` (per suite, default 600). Exit 1 when a suite that ran failed or timed out. `KIT/scripts/checklist.py` runs tests itself; use this script to run the suites on their own.

```powershell
python "KIT/skills/testing-patterns/scripts/test_runner.py" .
```

## 7. Pest (Laravel)

- Run with `php artisan test` (`--parallel` for speed); one file or filter: `vendor/bin/pest tests/Feature/OrderTest.php --filter=refund`.
- Layout: `tests/Unit/` for pure classes and actions, `tests/Feature/` for HTTP and console tests through the framework (`$this->post('/orders', [...])->assertCreated()`).
- Database: `RefreshDatabase` (or `LazilyRefreshDatabase`) against SQLite in memory or a dedicated test database in `phpunit.xml`; model factories over hand-built rows; `Queue::fake()`, `Mail::fake()`, `Http::fake()`, `Storage::fake()` for side effects. When production runs MySQL or Postgres and the code uses engine-specific SQL, test against that engine.
- Style: `it('rejects an expired token', function () { ... })`, `expect($value)->toBe(...)`, datasets for table-driven cases. Pest 4 adds browser tests (Playwright-based) for projects that want E2E inside the PHP suite.
- Coverage: `php artisan test --coverage` (needs Xdebug or PCOV). Pint and Larastan run alongside (`lint-and-validate`).

## 8. Playwright

Two tools:

- **Smoke check of a running URL** (no project suite needed): `playwright_runner.py` loads the page in headless Chromium. It fails when the page does not load (network error, HTTP 4xx/5xx), on uncaught JS errors, or on accessibility errors (images without `alt`, unnamed buttons and links, unlabeled fields); it warns on console errors, a missing `<title>`, and zero or several `h1`s. Flags: `--screenshot` (full page; `--screenshot-dir`, default system temp `agkit_screenshots`), `--a11y` (accessibility checks only, skip timing), `--mobile` (390x844 touch viewport; default 1440x900), `--timeout-ms`, `--json`. When the Python package or its browser is missing the result is SKIPPED (NOT VERIFIED) and it exits 0; install with `pip install playwright` and `python -m playwright install chromium`.
  ```powershell
  python "KIT/skills/testing-patterns/scripts/playwright_runner.py" http://localhost:3000 --screenshot
  ```
- **The project's own E2E suite:** `npx playwright test`. Useful config: `retries: 2` on CI, `trace: 'on-first-retry'`, `screenshot: 'only-on-failure'`; a `webServer` entry so the suite starts the app; fixtures or `storageState` for login. Name files by feature (`checkout.spec.ts`) under `tests/e2e/`.

CI order when the project has CI: install dependencies and browsers (`npx playwright install --with-deps chromium`), unit and integration on every push, E2E on merge and before release, traces and screenshots uploaded as artifacts.

## 9. Anti-patterns

| Avoid | Do instead |
|-------|-----------|
| Testing implementation details | Test observable behaviour |
| Hard-coded waits (`sleep`, `waitForTimeout`) | Auto-waiting assertions (`await expect(locator).toBeVisible()`) |
| Shared mutable state between tests | Fresh state per test |
| Ignoring flaky tests | Quarantine and fix; delete only if the behaviour it covers is gone |
| Snapshotting everything | Snapshot only stable, meaningful output |
| No tests around money, auth or data rules because "no framework is set up" | Add Vitest, `node:test`, pytest or Pest; it takes minutes |

Related: `verify-changes` for release checks, `systematic-debugging` when a test fails and the cause is unclear.
