---
name: lint-and-validate
description: Static checks - ESLint flat config and TypeScript for JS/TS, Ruff and mypy or pyright for Python, Pint and Larastan for Laravel, what "clean" means, and the kit's lint and type-coverage runners. Use when running checks for a change per the code-rules tier, setting up linting for a project, or fixing a lint or type error.
version: 2.5.0
---

# Lint and Validate

Run the project's own tools first; the kit scripts wrap them. How much to run follows the `code-rules` tier: nothing for tier 0, the project's lint and types on touched files for tier 1, the full set for tier 2-3. Type errors are required failures at tier 2-3; lint style findings are advisory unless the project's CI treats them as errors. Either way, fix errors your change introduced.

Run only the tools the project has. A missing tool is a note, not a failure, and not a pass: do not call an unlinted project "clean"; write it under `Not verified:`.

## Commands by ecosystem

| Ecosystem | Lint / format | Types | Notes |
|-----------|------|-------|-------|
| Node / TypeScript | `npm run lint` if the script exists, else `npx eslint .` (add `--fix` for safe fixes); Prettier or Biome for formatting | `npx tsc --noEmit` | ESLint flat config (`eslint.config.js` / `.mjs` / `.ts`); `.eslintrc*` is legacy and not read by current ESLint. Next.js 16 has no `next lint`; use `eslint-config-next` in the flat config. Biome projects: `npx biome check .` |
| Python | `ruff check . --fix` and `ruff format .` (or `uv run ruff ...`) | `mypy .` when configured (`[tool.mypy]` or `mypy.ini`), else `pyright` | Configure both in `pyproject.toml` |
| PHP / Laravel | `vendor/bin/pint --test` (fix: `vendor/bin/pint`) | `vendor/bin/phpstan analyse` (Larastan) | Config in `pint.json` and `phpstan.neon`; Composer dev dependencies |
| Dependencies and security | `npm audit --audit-level=high`; `pip-audit`; `composer audit` | | Security review and scanning: `vulnerability-scanner` |

TypeScript: 5.9+ is the baseline. The native compiler preview (`tsgo`, TypeScript 7) is much faster; use it only when the project has adopted it, and keep `tsc` as the reference when results differ.

Setting up a project that has none (ask or state it, since it adds files): `eslint.config.js` with `@eslint/js` recommended, `typescript-eslint`, and the framework preset (`eslint-config-next`; current `eslint-plugin-react-hooks` with its `recommended` preset, which carries the React Compiler diagnostics). Python: `[tool.ruff]` with `lint.select = ["E", "F", "I", "UP", "B"]` and `[tool.mypy]` in `pyproject.toml`. Laravel: `laravel/pint` ships with new apps; add `larastan/larastan` for types.

## The loop

1. Edit code.
2. Run lint and types for the touched ecosystem (scope to changed files when the tool allows).
3. Fix what your change broke at the source.
4. Re-run; then run tests if the tier asks for them (`testing-patterns`).

Pre-existing errors in files you did not touch: mention the count, do not silently fix a hundred unrelated lines in the same change unless asked.

## What "clean" means

Clean means the check passes because the code is right, not because the check was silenced. `as any` to dodge a type error, a file-level `/* eslint-disable */`, a bare `# type: ignore`, or a blanket `# noqa` hide the finding from the next reader and from CI.

```ts
// Hides the problem: the typo still ships
const data = res.body as any
data.usr.name

// Fixes it: parse (or at least type) the response so the checker protects you
const data = UserResponse.parse(res.body)
data.user.name                 // a typo here is caught at compile time
```

A justified disable is fine: one line, the rule named, the reason inline — `// eslint-disable-next-line <rule> -- <why it is safe here>`, `# type: ignore[<code>]  # <why>`.

## Kit scripts

`python "KIT/scripts/checklist.py" .` is the normal entry point: it runs its own lint, type and test steps (`--quick`, tier 1, scoped to git-changed files; `--full`, tier 2, whole project plus security and advisory audits). It does not call the two scripts below. In checklist.py, type errors and failing tests are required failures; lint style is advisory unless `--strict`.

The two scripts here are optional helpers for running one check on its own. Neither downloads anything (no bare `npx`): binaries come from `node_modules/.bin` or `vendor/bin`, then `PATH`. A missing tool, `node_modules` or `vendor` is a SKIP with a note, never a failure.

- `lint_runner.py` runs the linters the project has: Node - `npm run lint` when the script exists, else local ESLint or Biome, plus local `tsc --noEmit` when TypeScript is present; PHP - `vendor/bin/pint --test` and `vendor/bin/phpstan`, else `php -l`; Python - `ruff check`, then mypy when configured, else pyright. Flags: `--json`, `--no-types` (skip tsc/mypy/pyright), `--timeout SECONDS` (per linter, default 300). Exit 1 when a linter reports errors or times out.
- `type_coverage.py` runs the project-local `tsc --noEmit` for every `tsconfig.json` (solution-style configs run their references; skipped when `node_modules/.bin/tsc` is missing) and counts escape hatches (`: any`, `as any`, `<any>`, `@ts-ignore`, `@ts-nocheck`); above a project-size threshold they fail, below it they are warnings. Python: syntax errors fail; annotation coverage and `Any` use are warnings only. Flags: `--json`, `--skip-compiler` (source scan only), `--timeout SECONDS` (per tsc run, default 300). Exit 1 on compiler or syntax errors or escape hatches above the threshold.

```powershell
python "KIT/skills/lint-and-validate/scripts/lint_runner.py" . --no-types
python "KIT/skills/lint-and-validate/scripts/type_coverage.py" .
```
