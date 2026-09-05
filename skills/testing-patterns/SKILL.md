---
name: testing-patterns
description: Testing strategy for web and API projects - the test pyramid, AAA structure, the TDD loop, mocking rules, Pest/PHPUnit for Laravel, and Playwright end-to-end testing with the kit's test and smoke runners. Use when writing or reviewing unit, integration, or E2E tests, choosing a test framework, practising red-green-refactor, or deciding whether a change needs tests.
version: 2.0.0
---

# Testing Patterns

Tests are the executable specification. "Done" in this kit means required checks pass and every logic change has a test (see the VERIFY phase in `code-rules.md`).

## 1. Pyramid

| Level | Share | Covers | Speed |
|-------|-------|--------|-------|
| Unit (base) | Most | Pure functions, reducers, validation, business rules, and isolated UI components (component tests are unit tests with a render step) | < 100 ms each |
| Integration | Some | Route handlers and Server Actions, DB queries against a real test database, service contracts, component + provider trees | Seconds |
| E2E | Few | Critical user journeys in a real browser: sign-up, checkout, the one flow the business cannot lose | Slow, run on CI and before release |

Choose a test's level by the boundaries it crosses: no I/O, pure logic → unit; one real boundary you own (a route handler, a query against the test database) → integration; a whole journey through the browser → E2E. Write each behaviour at the lowest level that still exercises the real risk. More unit than integration, more integration than E2E: a suite with 90 % unit coverage and no E2E still ships a broken checkout; a suite that is all E2E is too slow to run on every change.

## 2. AAA structure

| Step | Purpose |
|------|---------|
| Arrange | Build the input and dependencies (factories, fixtures, fakes) |
| Act | Call the one thing under test |
| Assert | Verify the observable outcome, ideally one behaviour per test |

Name tests by behaviour: `returns 404 when the user does not exist`, `disables submit while pending`.

## 3. TDD loop

1. Red: write the smallest test that fails for the right reason. Watch it fail; a test that passes immediately is testing nothing.
2. Green: write the minimum code that makes it pass. No optimisation, no extra features.
3. Refactor: improve names, remove duplication, keep every test green. Commit.
4. Repeat. Priority order for new tests: happy path, error cases, edge cases, then performance.

TDD pays off most for new features, bug fixes (reproduce the bug in a test first), and complex logic. For exploratory spikes and pure layout work, write the code first, then add tests for the logic that emerged.

## 4. Test types and what to cover

- Unit: business logic, edge cases, error handling. Do not test framework code, third-party libraries, or trivial getters.
- Integration: request and response shape, status codes (200, 400, 401, 403, 404, 422), transactions and rollbacks, external-service contracts. Reset state in `beforeEach`; connect and disconnect in `beforeAll`/`afterAll`.
- E2E: happy-path journeys, authentication, payment, deep links. Use `data-testid` or role-based selectors, rely on Playwright's auto-waiting instead of sleeps, and give every test its own state.
- Visual regression: worth it for design systems and marketing pages; low value for dynamic content.

## 5. Mock at the boundary, not the code under test

Mock the seams your code talks to but does not own — third-party APIs, the network, the clock, randomness. Real test database in integration tests, in-memory fake in unit tests. Wrap a third-party client in a thin adapter and fake the adapter, so a library upgrade does not rewrite your tests. Two failure modes: mocking the logic under test (the test proves nothing), and mocking a dependency you own so deeply that you assert call sequences instead of outcomes — green while the behaviour is wrong, and broken on every refactor.

```ts
// Wrong — over-mocked: asserts calls, re-states the implementation, stays green even if the total is wrong.
const repo = { save: vi.fn() }, gateway = { charge: vi.fn() };
await createOrder({ items }, { repo, gateway });
expect(gateway.charge).toHaveBeenCalledWith(100);
expect(repo.save).toHaveBeenCalled();

// Right — mock only the external boundary, use a real fake for what you own, assert the outcome.
const repo = new InMemoryOrderRepo();
const gateway = { charge: async () => ({ id: "ch_1", status: "paid" }) };
const order = await createOrder({ items }, { repo, gateway });
expect(order.total).toBe(100);
expect(await repo.findById(order.id)).toMatchObject({ status: "paid" });
```

Vocabulary: stub = fixed return value; spy = records calls; mock = asserts expectations; fake = simplified working implementation. Reach for a fake before a mock.

## 6. Frameworks and detection

| Stack | Default | Command |
|-------|---------|---------|
| Node / TypeScript | `node:test` (built in, Node 24 LTS) or Vitest | `node --test` or `npx vitest run` |
| React / Next.js | Vitest + React Testing Library; Playwright for E2E | `npx vitest run`, `npx playwright test` |
| Python | pytest (+ `pytest-asyncio`, httpx `ASGITransport` for FastAPI) | `python -m pytest` |
| PHP / Laravel | Pest (PHPUnit underneath; PHPUnit alone in older projects) | `php artisan test` or `vendor/bin/pest` (`vendor/bin/phpunit`) |

`./scripts/test_runner.py <project>` detects the project's runner: the `test` script in `package.json` (covers `node --test`, Vitest, and Jest), Vitest or Jest from `devDependencies`, pytest when `pyproject.toml` or `requirements.txt` exists, and Pest/PHPUnit when `composer.json` exists (`php artisan test` in a Laravel project, `vendor/bin/pest` or `vendor/bin/phpunit` otherwise). Add `--coverage` for a coverage run. When nothing is configured the runner exits 0 with the message `No tests configured` and a warning: that is a warning, not a pass. Logic changes still need tests, so add the framework above and write them before calling the task done.

```powershell
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/testing-patterns/scripts/test_runner.py .
```

## 7. Pest / PHPUnit (Laravel)

- Run the suite with `php artisan test` (parallel: `php artisan test --parallel`); a single file or filter with `vendor/bin/pest tests/Feature/OrderTest.php` or `--filter=name`. Plain PHP packages: `vendor/bin/phpunit`.
- Layout: `tests/Unit/` for pure classes and actions, `tests/Feature/` for HTTP and console tests through the framework (`$this->get('/orders')`, `->assertStatus(201)`, `->assertJson([...])`).
- Database: `RefreshDatabase` (or `LazilyRefreshDatabase`) with an SQLite in-memory or a dedicated test database in `phpunit.xml`; model factories over hand-built rows; `Queue::fake()`, `Mail::fake()`, `Http::fake()` for side effects.
- Pest style: `it('rejects an expired token', function () { ... })`, `expect($value)->toBe(...)`, datasets for table-driven cases, `beforeEach` for shared arrangement. Coverage: `php artisan test --coverage` (needs Xdebug or PCOV).
- Static checks that run alongside the tests: Pint and Larastan (`@[skills/lint-and-validate]`).

## 8. Playwright

Two different tools:

- Smoke check of a running URL: loads the page in headless Chromium, records the status code, title, console and page errors, load timings, and basic accessibility counts (images without `alt`, unnamed buttons and links, unlabeled inputs). It fails on HTTP 4xx/5xx, a missing title, a page error, or any of those accessibility misses. No project test suite needed:
  `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/testing-patterns/scripts/playwright_runner.py http://localhost:3000 --screenshot` (add `--a11y` for the accessibility-only pass). Requires `pip install playwright && playwright install chromium`.
- The project's own E2E suite: `npx playwright test`. Configure `retries: 2` on CI, `trace: 'on-first-retry'`, `screenshot: 'only-on-failure'`, `video: 'retain-on-failure'`; use the Page Object pattern and fixtures for login. Organise as `tests/e2e/`, `tests/integration/`, `tests/component/`, `tests/fixtures/`; name files by feature (`checkout.spec.ts`).

CI order: install dependencies, install browsers (`npx playwright install --with-deps chromium`), run unit and integration on every PR, run E2E on merge and before release, upload traces and screenshots as artifacts. Shard large suites.

## 9. Anti-patterns

| Avoid | Do instead |
|-------|-----------|
| Testing implementation details | Test observable behaviour |
| Hard-coded waits (`sleep`, `waitForTimeout`) | Auto-waiting assertions (`expect(locator).toBeVisible()`) |
| Shared mutable state between tests | Fresh state per test, cleanup in `afterEach` |
| Ignoring flaky tests | Quarantine and fix; delete only if the behavior it covers no longer exists |
| Snapshot everything | Snapshot only stable, meaningful output |
| Skipping tests because "no framework is set up" | Add Vitest, `node:test`, or pytest; it takes minutes |

Related: `@[skills/verify-changes]` for the release gate, `@[skills/systematic-debugging]` when a test fails and the cause is unclear.
