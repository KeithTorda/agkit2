---
name: lint-and-validate
description: Run and repair configured syntax, lint, formatting and type checks with scope appropriate to a change. Use for static-check failures or relevant verification; reuse installed tools and distinguish tool failure from application defects.
version: 2.8.2
---

# Lint and Validate

Static checks test specific contracts: parseability, configured rules or type consistency. They do not prove behavior, design quality or security. Select checks from changed files and affected consumers; shared verification policy stays in core rules.

## Discover the real toolchain

Inspect manifests, lockfiles, scripts, language configuration, workspace boundaries and CI. Use the project's package manager/environment. Prefer an existing script to a guessed command. Use installed binaries; avoid an unpinned executor that silently downloads another version.

Examples when configured: JS/TS lint/typecheck scripts; Python Ruff/mypy/pyright through its environment; PHP Pint and PHPStan/Larastan. Framework checkers may cover contracts a bare compiler cannot. Verify installed-version command support; do not replace a working stack.

## Diagnose and repair

Read the first useful error and location. Distinguish source defects, generated-file mismatch, wrong directory, dependency state, version incompatibility and unavailable tooling. A pre-existing failure differs from a regression but can still limit verification.

Fix causes rather than broadly disabling rules, adding `any`, ignoring errors or weakening compiler settings. A justified suppression is narrow and explains the invariant/third-party limitation. Review autofixes, especially import changes and files outside scope. Apply formatting to the relevant scope using the configured formatter.

For a type change, inspect affected consumers: a local assertion can hide an incorrect boundary.

## Report what was checked

Capture command, scope and result. Separate passed, failed, timed out, unavailable and skipped. A zero-exit wrapper may mean no tool ran; inspect its summary. Rerun the relevant check after a repair. Broaden for shared contracts or unresolved evidence, not a fixed all-tools ritual.

Use behavioral tests for logic; browser verification for rendering runs only when the user asks. Static checks cannot validate either alone.

## Existing helpers

Expand `KIT` to the active installation:

```powershell
python "KIT/scripts/checklist.py" . --quick
python "KIT/skills/lint-and-validate/scripts/lint_runner.py" . --no-types
python "KIT/skills/lint-and-validate/scripts/type_coverage.py" .
```

`checklist.py --quick` orchestrates available relevant checks; `--full` adds security/advisory checks. Inspect actual execution. `lint_runner.py` supports `--json`, `--no-types`, `--timeout`; it never downloads missing tools. `type_coverage.py` supports `--json`, `--skip-compiler`, `--timeout`. Source annotation/escape-hatch counts are advisory, not proof of runtime correctness or comprehensive type coverage.
