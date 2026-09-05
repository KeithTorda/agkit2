# AG Kit v2 Runtime Scripts

All scripts are Python 3 standard library only. Run them from any project with the absolute kit path (PowerShell or bash):

```powershell
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .
```

## Entry points

| Script | Purpose | Notes |
|---|---|---|
| `checklist.py <project> [--url URL] [--report file]` | Fast gate used at the end of every task. | Required checks: security scan (high+), lint, type check, tests. Everything else advisory. URL checks are skipped without `--url`. |
| `verify_all.py <project> [--url URL] [--no-runtime] [--no-e2e]` | Release gate: the fast gate plus dependency analysis, GEO, bundle, React performance, mobile, i18n, API checks, Lighthouse, Playwright smoke. | Same required/advisory split. |
| `validate_kit.py [--json]` | Self-check of the kit: frontmatter contracts, agent→skill references, absolute paths, markdown links, Python syntax, legacy patterns. | Run after editing agents/skills. Exit 1 on errors. |
| `build_quick_reference.py [--write \| --out PATH]` | Regenerates the `quick-reference` global rule from disk. | `--write` targets `~/.gemini/config/rules/quick-reference.md`. Run after adding or removing agents/skills. |
| `session_manager.py status\|info [project]` | Project snapshot: type, package metadata, feature hints, file counts. | Used by `/status`. |
| `validation_runner.py` | Shared runner (not an entry point). | `suite_success` gates on required checks only. |
| `tests/test_toolkit.py` | Regression tests for the kit and its scanners. | `python scripts/tests/test_toolkit.py` |

## Skill scripts

Each skill's `SKILL.md` documents its own scripts under `skills/<skill>/scripts/`. Advisory heuristics (UX, mobile, API, SEO/GEO, schema) produce warnings; only `security_scan.py`, `lint_runner.py`, `type_coverage.py`, and `test_runner.py` can block.

## Runtime prerequisites

- Lint/type/test scripts call the project's own tooling (`npm run lint`, `npx tsc --noEmit`, `ruff`, `mypy`/`pyright`, `pytest`, `vitest`, …). A missing tool is reported as a note, not a failure.
- `security_scan.py` runs `npm audit` when a `package.json` exists (network access).
- Lighthouse: `npm install -g lighthouse`. Playwright smoke: `pip install playwright && playwright install chromium`.
