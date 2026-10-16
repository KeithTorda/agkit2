# AG Kit scripts

Python 3.10+, standard library only (`doc_verify.py` uses optional PDF libraries). Every script resolves the kit from its own location, takes `--help`, and runs on Windows (PowerShell) and POSIX. `KIT` is the kit root defined in `core-protocol`; quote it in commands:

```powershell
python "KIT/scripts/checklist.py" .
```

Read each script's `--help` for exit-code details. In the project runners, `0` means no blocking finding was reported; it can also accompany incomplete or skipped evidence. JSON `outcome` (`PASS`, `FAIL`, `INCOMPLETE`, `SKIPPED`) and `verified` distinguish those cases. Never use exit 0 or legacy `success: true` alone as proof that checks ran. Other focused tools have their own contracts.

## Project checks (choose by changed behavior and consequences)

| Script | Mode | What it runs |
|---|---|---|
| `checklist.py . [--quick]` | Focused | Detects the stack (Node/TS, Python, PHP/Laravel) and runs the project's own lint, type check and tests, scoped to git-changed files where the tool supports it (eslint/biome/ruff/pint on the files; `vitest related`, `jest --findRelatedTests`). Types use the project's `typecheck`-style script, else `vue-tsc`, `svelte-check` or the local `node_modules/.bin/tsc --noEmit`; mypy (or pyright) for Python; PHPStan for PHP. No changed files: nothing runs. No git: whole project. `--since origin/main` adds committed changes; `--all-files` drops the scoping. No security scan or audits. |
| `checklist.py . --full` | Broad static/test | Whole project: the kit security scan (high+), lint, types, tests, and the advisory audits (CSS, naming, UX, accessibility, SEO, i18n, schema). |
| `verify_all.py . [--url URL]` | Release-oriented | Everything in `--full`, plus the production build (`<pm> run build`), dependency analysis, GEO, React performance, mobile, API and bundle size checks. `--no-build`, `--no-e2e`, `--no-runtime`. |

`--url URL` (either script, any tier) adds Lighthouse and a Playwright smoke test against the running app; without it they are skipped. checklist.py runs its own lint, type and test steps; it does not call `lint_runner.py`, `type_coverage.py` or `test_runner.py`.

Required findings (fail the run): security high or above, type errors, failing tests, and in `verify_all.py` a failing build. The lint step and heuristic audits are advisory by default because the runner cannot classify each project's rules; inspect findings for real bugs and honor the project's CI. `--strict` makes advisory findings block. A missing/broken required tool produces `INCOMPLETE` and `verified: false`, with the check in `not_verified`. Genuinely inapplicable checks are skipped; an all-skipped run produces `SKIPPED`. Explicitly deferred required checks remain unverified. Each step is timed; `--json` prints the report to stdout (progress to stderr), and `--report FILE` saves it. `--stop-on-fail` leaves later checks recorded as not run. `checklist.py --timeout SECONDS` overrides each timeout.

These scripts do not judge visual quality. Use `browser-verification` for visible changes, including copy/style edits that affect wrapping, contrast or layout. Reuse or start the correct dev server, inspect screenshots and interactions, refine the draft and report only observed evidence.

## Focused tools

| Script | Use |
|---|---|
| `css_audit.py . [--strict] [--json] [--report FILE] [--limit N]` | Why a colour is wrong, with file:line: token defined twice outside a theme scope, `var()` nothing defines, unreadable colour pairs, inline colour styles, one selector coloured in several files, and `!important` overrides (warning with location; a note when a comment on the line explains it; the reduced-motion reset is ignored). Ignores `node_modules`, `vendor`, `dist`, `build`, `*.min.css` and bannered vendor bundles; understands Tailwind v4 `@theme`, CSS modules and scoped component styles. Advisory; `--strict` makes errors (and uncommented `!important`) fail. |
| `naming_check.py . [--strict] [--json]` | Generic file names in generic folders (`src/utils.ts`), duplicate source basenames, a class defined in several global stylesheets, generic exported names, un-namespaced custom properties. Framework conventions, tests, CSS modules, `@theme` and the shadcn/ui token set are excluded. Advisory; `--strict` makes errors fail. |
| `ui_verify.py .agents/verify/<slug> [--widths 390,1440] [--require-before] [--require-visual-review] [--json] [--report FILE]` | Checks evidence-file consistency: screenshot dimensions, distinct views and a known `pass`/`fail`/`skipped` verdict. A passing verdict must name route/widths, record console/network counts, a passed or justified inapplicable interaction, and an empty `notVerified` list. Optional `visualReview` records can document observations per width; `--require-visual-review` requires passing recorded coverage for the requested widths. `visualReviewStatus` and `verificationScope` distinguish record completeness from perception. It cannot inspect the live page, establish observer truth or judge aesthetics. An honest skip with reason exits 0 and remains skipped. |
| `doc_verify.py out.pdf --outdir DIR [--page-size a4\|a5\|folio\|legal\|letter] [--glyphs "₱,ñ"] [--margin-mm N] [--dpi N] [--reference form.pdf] [--json]` | Renders a generated PDF to PNGs to look at, and checks page size, embedded fonts, extractable text, glyphs and content near the edge; with `--reference`, a per-page diff against the official form. Needs `pypdf pdfplumber` for checks and `pypdfium2 pillow` (or poppler) for rendering; a missing library becomes a note. Writes `doc-verdict.json` to the outdir (`--report` to change). Exit 1 on issues, 2 when nothing could be checked. |
| `session_manager.py status . [--json]` | Read-only snapshot for `/status`: stack, scripts, feature folders, file counts, git branch and recent commits, open plan tasks, memory and `DESIGN.md` presence. Malformed manifests and failed Git queries are reported as unknown/incomplete evidence. `info` prints package metadata. |

## Kit maintenance

| Script | Use |
|---|---|
| `kit_doctor.py [--source DIR] [--config-root DIR] [--json]` | Read-only source validation, installed file/version/rule agreement, global entrypoint and local tool availability. Use `python -B` to avoid bytecode writes. It does not repair files, inspect an already-loaded chat or verify a generated app. |
| `validate_kit.py [path] [--rules DIR] [--json] [--strict] [--quiet]` | Validates structure and references: rule/agent/skill frontmatter, always-on size budget, native agent sections, routed commands and targets, numeric release version and manifest consistency, portable paths, Python syntax, obsolete files and size warnings. Historical notes are exempt from path hygiene. `--strict` makes warnings fail. This checks packaging, not generated design quality. |
| `build_quick_reference.py [--kit DIR] [--write \| --out PATH \| --check]` | Regenerates the `quick-reference` rule (trigger `model_decision`) from agent and skill frontmatter. `--write` targets `KIT/rules/quick-reference.md` in the source repo, else `~/.gemini/config/rules/`. `--check` exits 1 when the file is stale. |
| `proplan_check.py docs/proplan/<slug> [--lite \| --full] [--write-traceability] [--strict] [--json]` | Checks a `/proplan` document set: the documents for a full or lite set exist (`--lite`/`--full`, else the `set` in `00-overview`, else auto-detect), frontmatter and headings are sane, every ID has the right syntax and is defined once in its home document, and IDs trace end to end (goals, requirements, screens/APIs, tasks, test cases: G-, R-, NFR-, S-, API-, T-, TC-, ADR-, RK- and others). `--write-traceability` regenerates `TRACEABILITY.md` first. Exit 1 on errors; warnings fail only with `--strict`. |
| `validation_runner.py` | Shared step runner for `checklist.py` and `verify_all.py` (not an entry point). |
| `tests/` | Behavioral regression tests: `python -m unittest discover -s scripts/tests -v` from the kit root. Temporary fixtures exercise required/advisory results, incomplete/skipped evidence, failure retention, UI verdict consistency and other toolkit behavior. |

## Skill scripts

Each lives in `KIT/skills/<skill>/scripts/`, takes `--help` and `--json`, and is documented in its skill. The static auditors share `--fail-on error|warning|never` (default `error`) and `--verbose`.

| Script | Skill | Default exit 1 when |
|---|---|---|
| `security_scan.py`, `dependency_analyzer.py` | `vulnerability-scanner` | a finding is high or critical (`--fail-on`) |
| `lint_runner.py`, `type_coverage.py` | `lint-and-validate` | a lint/compiler/syntax command reports a failure (optional helpers); source heuristic counts are advisory |
| `test_runner.py`, `playwright_runner.py` | `testing-patterns` | a suite or the smoke test fails |
| `lighthouse_audit.py`, `bundle_analyzer.py` | `performance-profiling` | a score threshold is missed / an asset is over the high limit |
| `seo_checker.py`, `geo_checker.py` | `seo-fundamentals` | SEO errors / never, unless `--min-score` |
| `ux_audit.py`, `accessibility_checker.py` | `frontend-design` | never unless `--fail-on warning` / accessibility errors |
| `api_validator.py`, `schema_validator.py`, `i18n_checker.py`, `react_performance_checker.py`, `mobile_audit.py` | `api-patterns`, `database-design`, `i18n-localization`, `nextjs-react-expert`, `mobile-design` | error findings |

A missing tool, browser or build output is not evidence of success. Read each helper's status and missing-check notes; a nonblocking exit code can accompany incomplete work.

## Prerequisites

- The checks call the project's own tools (`node_modules/.bin/eslint`, `tsc`, `vitest`, `ruff`, `mypy`, `pytest`, `vendor/bin/pest`, ...) and never download them. Install project dependencies first; a missing tool is reported, not failed.
- `security_scan.py` runs `npm audit` / `composer audit` when installed (network); `--offline` skips them.
- Runtime audits require the corresponding installed tool/browser. Follow the project's tooling and the relevant skill rather than changing versions solely to run a check.
