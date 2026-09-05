---
name: test
description: "/test — Runs the project's tests, generates tests for a file or feature, reports coverage, or fixes failing tests. Use when the user asks to test, add tests, check coverage, or make the suite pass."
version: 2.0.0
---

# /test

**Input:** `/test` runs everything; `/test <file|feature>` generates tests for that target; `/test coverage` reports coverage; `/test fix` repairs failing tests.
**Agent:** read `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/test-engineer.md`.
**Skills:** `@[skills/testing-patterns]` (structure, mocking, e2e), `@[skills/verify-changes]`.

## Steps

### Run
1. Detect the runner from the project (`package.json` scripts, `pytest.ini`, `pyproject.toml`, `composer.json` → `php artisan test` or `vendor/bin/pest`) and run it. Never invent a runner.
2. Then run `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .`; tests are one of its required checks. The required-vs-advisory gate and the auto-fix policy are the global `code-rules` rule's — follow it, do not restate a different threshold here.

### Generate
1. Read the target; list public behavior, error paths, edge cases, and external dependencies to mock.
2. Write tests in the project's framework and folder convention (`*.test.ts`, `tests/`, `__tests__/`): arrange-act-assert, behavior over implementation, one behavior per test, descriptive names.
3. Run them. When one fails, decide whether the test or the code is wrong, fix that, and say which.

### Coverage
Run the runner with its coverage flag (`vitest run --coverage`, `pytest --cov`) and report the uncovered branches worth testing, not only the percentage.

## Output

```markdown
## Tests: <target>
| Case | Type | Covers |
|---|---|---|
| rejects invalid email | unit | validation |
Files: tests/<file>.test.ts
Run: `<command>` → <passed>/<total> passed, <failed> failed
Failed: <test> — expected <x>, received <y> → <fix applied or proposed>
```

## Verification

- Every number comes from a run in this session.
- New tests fail when the behavior is broken (check by temporarily reverting, or state the reasoning).
- Required checks pass.
