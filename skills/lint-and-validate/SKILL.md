---
name: lint-and-validate
description: Static checks after every code change - ESLint 9 flat config, TypeScript type checks, Ruff and mypy or pyright for Python, plus the kit's lint and type-coverage runners. Use after editing code, before declaring a task done, when setting up linting for a project, or when a lint or type error needs fixing.
version: 2.0.0
---

# Lint and Validate

Lint and type errors are required-check failures: fix them automatically before reporting a task as done (auto-fix policy: global `code-rules` rule). Run the project's own tools first; the kit scripts wrap them for the checklist.

Run only the tools the project actually has: Ruff, mypy, pyright, Pint, and Larastan run only when installed (mypy also needs a `[tool.mypy]` block); ESLint 9 needs a flat `eslint.config.*`. A missing tool is a note, not a failure — and not a pass either: do not call an unlinted project "clean".

## Commands by ecosystem

| Ecosystem | Lint | Types | Notes |
|-----------|------|-------|-------|
| Node / TypeScript | `npm run lint` if the script exists, else `npx eslint . --fix` | `npx tsc --noEmit` | ESLint 9+ uses flat config (`eslint.config.js` / `.mjs` / `.ts`); `.eslintrc*` is legacy and ignored by ESLint 9. Next.js 16 has no `next lint`; use `eslint-config-next` in the flat config |
| Python | `ruff check . --fix` and `ruff format .` | `mypy .` (when `[tool.mypy]` or `mypy.ini` exists) or `pyright` | Configure both in `pyproject.toml` |
| PHP / Laravel | `vendor/bin/pint --test` (fix: `vendor/bin/pint`) | `vendor/bin/phpstan analyse` (Larastan) | Config in `pint.json` and `phpstan.neon`; both installed as dev dependencies through Composer |
| Security (optional) | `npm audit --audit-level=high`; `bandit -r src -ll` and `pip-audit` for Python | | Bandit is optional; the required security gate is `@[skills/vulnerability-scanner]` |

Setting up a project that has none: add `eslint.config.js` with `@eslint/js` recommended, `typescript-eslint`, and the framework preset (`eslint-config-next`, `eslint-plugin-react-hooks` for the compiler rules); for Python add `[tool.ruff]` with `select = ["E", "F", "I", "UP", "B"]` and `[tool.mypy]` to `pyproject.toml`.

## The loop

1. Edit code.
2. Run lint and types for the touched ecosystem.
3. Fix every error at the source (see "What 'lint clean' means" below).
4. Re-run until clean, then run tests (`@[skills/testing-patterns]`).

## What "lint clean" means

Clean means the check passes because the code is right, not because the check was silenced. `as any` to dodge a type error, a file-level `/* eslint-disable */`, `# type: ignore` with no message, or a blanket `# noqa` are suppressions — they hide the finding from the next reader and from CI.

```ts
// Wrong — suppresses the check; the real bug (wrong shape) still ships.
const data = res.body as any;
data.usr.name;                 // typo survives

// Right — fix the type so the check protects you.
const data = res.body as UserResponse;
data.user.name;                // typo caught at compile time
```

The one legitimate disable is a single line a rule is genuinely wrong about, with the rule named and the reason inline: `// eslint-disable-next-line <rule> -- <why it is safe here>`. Warnings the project treats as errors count as errors.

## Kit scripts

`./scripts/lint_runner.py <project>` detects the project and runs what is configured: `npm run lint` (or `npx eslint .` when only the dependency exists) and `npx tsc --noEmit` when TypeScript is present; for Python, `ruff check .` only if Ruff is installed, then `mypy .` if mypy is installed and configured, otherwise `pyright` if installed. A missing tool is reported as a note, not a failure. Exit code 1 only when a linter that ran reported errors. Output is a per-check pass/fail summary plus JSON.

`./scripts/type_coverage.py <project>` uses real compiler output: it runs the project-local `tsc --noEmit` for every `tsconfig.json` it finds and fails when the compiler reports errors (skipped, not failed, when no local `tsc` is installed). Alongside that it counts explicit escape hatches (`: any`, `as any`, `@ts-ignore`, `@ts-nocheck`) and fails only above a project-size threshold; inferred return types are never counted against you. For Python it parses files with `ast` and reports functions missing parameter or return annotations.

```powershell
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/lint-and-validate/scripts/lint_runner.py .
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/lint-and-validate/scripts/type_coverage.py .
```

Both run inside the fast gate `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .` as required checks.
