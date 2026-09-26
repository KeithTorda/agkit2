# AG Kit scripts

Python 3.10+, standard library only (`doc_verify.py` uses optional PDF libraries). Every script resolves the kit from its own location, takes `--help`, and runs on Windows (PowerShell) and POSIX. `KIT` is the kit root defined in `core-protocol`; quote it in commands:

```powershell
python "KIT/scripts/checklist.py" .
```

Exit codes everywhere: `0` ok, `1` a required failure (or findings with `--strict`), `2` usage error or nothing could be checked.

## Project checks (by `code-rules` tier)

| Script | Tier | What it runs |
|---|---|---|
| `checklist.py . [--quick]` | 1 | Detects the stack (Node/TS, Python, PHP/Laravel) and runs the project's own lint, type check and tests, scoped to git-changed files where the tool supports it (eslint/biome/ruff/pint on the files; `vitest related`, `jest --findRelatedTests`). Types use the project's `typecheck`-style script, else `vue-tsc`, `svelte-check` or the local `node_modules/.bin/tsc --noEmit`; mypy (or pyright) for Python; PHPStan for PHP. No changed files: nothing runs. No git: whole project. `--since origin/main` adds committed changes; `--all-files` drops the scoping. No security scan or audits. |
| `checklist.py . --full` | 2 | Whole project: the kit security scan (high+), lint, types, tests, and the advisory audits (CSS, naming, UX, accessibility, SEO, i18n, schema). |
| `verify_all.py . [--url URL]` | 3 | Everything in `--full`, plus the production build (`<pm> run build`), dependency analysis, GEO, React performance, mobile, API and bundle size checks. `--no-build`, `--no-e2e`, `--no-runtime`. |

`--url URL` (either script, any tier) adds Lighthouse and a Playwright smoke test against the running app; without it they are skipped. checklist.py runs its own lint, type and test steps; it does not call `lint_runner.py`, `type_coverage.py` or `test_runner.py`.

Required (fail the run): security findings high or above, type errors, failing tests, and in `verify_all.py` a failing build. Advisory (reported, never fail unless `--strict`): lint style, naming, CSS audit, UX/accessibility/SEO/i18n/schema heuristics, and the tier 3 extras. A tool that is not installed or configured is a note and appears under "not verified". Each step is timed; the run ends with a summary table and a `Result:` line. `--json` prints a machine-readable report to stdout (progress goes to stderr); `--report FILE` also writes it. `--stop-on-fail` stops after the first required failure; `checklist.py --timeout SECONDS` overrides every step's timeout.

## Focused tools

| Script | Use |
|---|---|
| `css_audit.py . [--strict] [--json] [--report FILE] [--limit N]` | Why a colour is wrong, with file:line: token defined twice outside a theme scope, `var()` nothing defines, unreadable colour pairs, inline colour styles, one selector coloured in several files, and `!important` overrides (warning with location; a note when a comment on the line explains it; the reduced-motion reset is ignored). Ignores `node_modules`, `vendor`, `dist`, `build`, `*.min.css` and bannered vendor bundles; understands Tailwind v4 `@theme`, CSS modules and scoped component styles. Advisory; `--strict` makes errors (and uncommented `!important`) fail. |
| `naming_check.py . [--strict] [--json]` | Generic file names in generic folders (`src/utils.ts`), duplicate source basenames, a class defined in several global stylesheets, generic exported names, un-namespaced custom properties. Framework conventions, tests, CSS modules, `@theme` and the shadcn/ui token set are excluded. Advisory; `--strict` makes errors fail. |
| `ui_verify.py .agents/verify/<slug> [--widths 390,1440] [--require-before] [--json] [--report FILE]` | Checks the evidence behind a `/see` claim: a screenshot per width, pixel width matching the name (1x to 3x, Windows 125/150 % scaling included), no screenshot reused as another width, `verdict.json` consistent. Widths default to those in `verdict.json`, else 390 and 1440. A verdict of `skipped` with a reason (no dev server) exits 0. |
| `doc_verify.py out.pdf --outdir DIR [--page-size a4\|a5\|folio\|legal\|letter] [--glyphs "₱,ñ"] [--margin-mm N] [--dpi N] [--reference form.pdf] [--json]` | Renders a generated PDF to PNGs to look at, and checks page size, embedded fonts, extractable text, glyphs and content near the edge; with `--reference`, a per-page diff against the official form. Needs `pypdf pdfplumber` for checks and `pypdfium2 pillow` (or poppler) for rendering; a missing library becomes a note. Writes `doc-verdict.json` to the outdir (`--report` to change). Exit 1 on issues, 2 when nothing could be checked. |
| `session_manager.py status . [--json]` | Read-only snapshot for `/status`: stack, scripts, feature folders, file counts, git branch and recent commits, open plan tasks, memory and `DESIGN.md` presence. `info` prints package metadata. |

## Kit maintenance

| Script | Use |
|---|---|
| `validate_kit.py [path] [--rules DIR] [--json] [--strict] [--quiet]` | Validates the v2.5 structure: rule frontmatter, no hex colours in rules, always-on rules within 15000 bytes, agent native frontmatter and section order, skill frontmatter, every `KIT/...` reference, routed commands and agents, no hardcoded user path outside `rules/core-protocol.md`, size warnings (skill `parts/` and templates exempt), obsolete files. `--quiet` prints errors and the summary only; `--strict` makes warnings fail. Run after editing agents, skills or rules. |
| `build_quick_reference.py [--kit DIR] [--write \| --out PATH \| --check]` | Regenerates the `quick-reference` rule (trigger `model_decision`) from agent and skill frontmatter. `--write` targets `KIT/rules/quick-reference.md` in the source repo, else `~/.gemini/config/rules/`. `--check` exits 1 when the file is stale. |
| `proplan_check.py docs/proplan/<slug> [--lite \| --full] [--write-traceability] [--strict] [--json]` | Checks a `/proplan` document set: the documents for a full or lite set exist (`--lite`/`--full`, else the `set` in `00-overview`, else auto-detect), frontmatter and headings are sane, every ID has the right syntax and is defined once in its home document, and IDs trace end to end (goals, requirements, screens/APIs, tasks, test cases: G-, R-, NFR-, S-, API-, T-, TC-, ADR-, RK- and others). `--write-traceability` regenerates `TRACEABILITY.md` first. Exit 1 on errors; warnings fail only with `--strict`. |
| `validation_runner.py` | Shared step runner for `checklist.py` and `verify_all.py` (not an entry point). |
| `tests/test_toolkit.py` | Regression tests: `python -m unittest scripts/tests/test_toolkit.py -v` from the kit root. |

## Skill scripts

Each lives in `KIT/skills/<skill>/scripts/`, takes `--help` and `--json`, and is documented in its skill. The static auditors share `--fail-on error|warning|never` (default `error`) and `--verbose`.

| Script | Skill | Default exit 1 when |
|---|---|---|
| `security_scan.py`, `dependency_analyzer.py` | `vulnerability-scanner` | a finding is high or critical (`--fail-on`) |
| `lint_runner.py`, `type_coverage.py` | `lint-and-validate` | a linter or the compiler reports errors (optional helpers) |
| `test_runner.py`, `playwright_runner.py` | `testing-patterns` | a suite or the smoke test fails |
| `lighthouse_audit.py`, `bundle_analyzer.py` | `performance-profiling` | a score threshold is missed / an asset is over the high limit |
| `seo_checker.py`, `geo_checker.py` | `seo-fundamentals` | SEO errors / never, unless `--min-score` |
| `ux_audit.py`, `accessibility_checker.py` | `frontend-design` | never unless `--fail-on warning` / accessibility errors |
| `api_validator.py`, `schema_validator.py`, `i18n_checker.py`, `react_performance_checker.py`, `mobile_audit.py` | `api-patterns`, `database-design`, `i18n-localization`, `nextjs-react-expert`, `mobile-design` | error findings |

A missing tool, browser or build output is reported as SKIP / NOT RUN / NOT VERIFIED with exit 0: never a pass.

## Prerequisites

- The checks call the project's own tools (`node_modules/.bin/eslint`, `tsc`, `vitest`, `ruff`, `mypy`, `pytest`, `vendor/bin/pest`, ...) and never download them. Install project dependencies first; a missing tool is reported, not failed.
- `security_scan.py` runs `npm audit` / `composer audit` when installed (network); `--offline` skips them.
- Lighthouse: `npm install -g lighthouse@12` (needs Chrome). Playwright smoke: `pip install playwright` then `python -m playwright install chromium`.
