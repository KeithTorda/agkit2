---
name: test
description: "Run, add or diagnose meaningful project tests and report actual outcomes. Use /test with a target, coverage or fix; choose the established runner and valuable behavior."
version: 2.8.2
---

# /test

Use `KIT/agents/test-engineer.md` and `KIT/skills/testing-patterns/SKILL.md`. Infer the intended mode from context: run, add tests for a target, inspect coverage or repair failures. Read the project scripts/configuration; do not invent a test runner or install one without a reason.

For a run, choose the requested scope or the project's established suite and capture actual results. For new tests, identify valuable public behavior and likely regressions, then use the project's conventions and suitable test level. Cover important boundaries and denial/failure cases; avoid assertions that only mirror private implementation or static trivia.

For a failure, reproduce it in isolation, compare expectation with the requirement and fix the faulty product/test/fixture/environment within scope. Do not skip or weaken a valid test to manufacture success. Check flakes for shared state and timing before adding retries.

Use coverage to find meaningful uncovered branches, not as proof of correctness or a universal target. Run changed tests and verify they observe the intended behavior; mutation checks are optional when they provide real confidence, not a mandatory temporary break of working code.

Report commands, target, pass/fail/skip counts actually produced, important behavior covered and unresolved limitations. Follow verify-changes for interpreting incomplete or skipped runs.
