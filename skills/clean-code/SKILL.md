---
name: clean-code
description: Make code easier to understand and change while preserving required behavior and project conventions. Use for implementation, simplification and refactoring; focus on the touched code and the real maintenance problem.
version: 2.8.2
---

# Clean Code

Readable code makes the domain, effects and failure paths visible. Begin with what the code must preserve, then simplify the shortest route to the user's outcome. An existing convention is usually more valuable than a competing style.

## Understand before reorganizing

Read affected callers, configuration and tests. Identify the observable contract: input, returned data, errors, ordering, mutations and compatibility. Separate requested behavior changes from behavior-preserving refactors. Characterize risky legacy behavior with a focused test or repeatable observation when suitable coverage is absent.

## Shape code around meaning

- Name domain operations precisely: `reserveStock` explains more than `processData`. Short local names are fine when immediately clear.
- Keep a function cohesive. Split when distinct responsibilities/effects obscure behavior, not because of a line count or the word "and".
- Make invalid states harder to construct with types, schemas, constraints or explicit transitions. Runtime input still needs runtime validation.
- Use guard clauses when they clarify the main path. Preserve cleanup, transaction and resource lifetime when rearranging control flow.
- Keep effects visible. Do not hide writes, destructive actions or retries behind a harmless-looking getter.
- Comments explain constraints, surprising choices or workarounds. Update them when the code changes.

## Choose abstraction by evidence

Similar syntax alone does not justify sharing. Extract when callers share meaning and must evolve together, or when a stable boundary clarifies testing/integration. There is no required second/third-use threshold. Deliberate duplication can beat a configurable component with unrelated branches; a one-use function can usefully name a business rule.

Avoid speculative extensibility, but retain interfaces that enforce real boundaries. Use direct dependencies when sufficient and injection when replacement, isolation or lifecycle control has a purpose. Do not replace clear loops, classes or concrete code solely to impose a style.

## Change shared code carefully

Search exports, imports, dynamic registration and persisted shapes before renaming public contracts. Update consumers together or provide compatibility. Keep unrelated cleanup out of the diff. Generated/vendor code follows its owning workflow.

Before deleting apparent dead code, check framework discovery, reflection, runtime registration and external consumers. No textual references is evidence, not proof.

## Verify meaning and readability

Use focused existing checks for touched behavior; broaden when a shared contract changes. Tests should protect outcomes, not count functions, assert helper names or duplicate implementation. A formatting-only change usually needs a static check, not a new test suite.

Review the diff for accidental behavior changes, swallowed errors, weaker types, broken callers and unrelated churn. Explain improvements and intentional behavior changes. Use `systematic-debugging` for unclear behavior and `adversarial-review` when independent defect review adds confidence.

`python "KIT/scripts/naming_check.py" .` gives advisory naming observations. Heuristics do not override the language, framework or repository convention.
