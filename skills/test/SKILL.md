---
name: test
description: "/test - Runs the project's tests, writes tests for a file or feature, reports coverage, or fixes failing tests. Use when the user asks to test, add tests, check coverage or make the suite pass, and for logic that money, auth, permissions or data integrity depend on."
version: 2.5.0
---

# /test

**Input:** `/test` runs everything; `/test <file|feature>` writes tests for that target; `/test coverage` reports coverage; `/test fix` repairs failing tests.
**Agent:** `KIT/agents/test-engineer.md`.
**Read now:** `KIT/skills/testing-patterns/SKILL.md` (structure, mocking, e2e).

## Run
1. Detect the runner from the project (`package.json` scripts, `pytest.ini`/`pyproject.toml`, `composer.json` → `php artisan test` or `vendor/bin/pest`) and run it. Never invent a runner.
2. Report pass/fail counts and each failure with expected vs received.

## Generate
1. Read the target; list public behaviour, error paths, edge cases, and external dependencies to mock.
2. Write tests in the project's framework and folder convention: arrange-act-assert, behaviour over implementation, one behaviour per test, descriptive names.
3. Prioritise tests that would catch a real regression (money, auth, permissions, data integrity, tricky logic). A test of a static component usually is not worth it.
4. Run them. When one fails, decide whether the test or the code is wrong, fix that one, and say which.
5. Check that a new test can fail: break the behaviour briefly or state why it would catch the bug.

## Coverage
Run with the coverage flag (`vitest run --coverage`, `pytest --cov`, `pest --coverage`) and report the uncovered branches worth testing, not only the percentage.

## Fix
Read the failure, reproduce it alone (`npx vitest run path/to/file.test.ts`), find whether the code or the test drifted, fix the one that is wrong. Never delete or skip a failing test to get green without saying so.

## Output

```markdown
## Tests: <target>
| Case | Type | Covers |
|---|---|---|
| rejects invalid email | unit | validation |
Files: tests/<file>.test.ts
Run: `<command>` → <passed>/<total> passed
Failed: <test> - expected <x>, received <y> → <fix applied or proposed>
```

Every number comes from a run in this session.
