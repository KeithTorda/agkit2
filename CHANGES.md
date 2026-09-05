# AG Kit v2 — What changed from the original ag-kit install (2026-09-05)

Based on vudovn/ag-kit. Rebuilt for a global Antigravity install on this machine. Full audit: `ag-kit-audit.md`; policies every file follows: `DECISIONS.md` (both next to this file).

## Layout
- Plugin renamed to `ag-kit-v2` (the old `ag-kit` plugin is disabled in `~/.gemini/config/config.json`; delete its folder when convenient).
- Rules live only in `~/.gemini/config/rules/` (6 files, same names as before, rewritten). The duplicate `rules/` inside the plugin is gone (it was injected twice).
- `~/.gemini/GEMINI.md` is a 1 KB entry file. Always-on context is now ~7 KB (was ~9–10 k tokens with pointers).
- `workflows/` removed (deprecated in Antigravity). The 13 workflows became 11 slash-command skills: `/brainstorm /create /plan /debug /test /verify /deploy /orchestrate /enhance /remember /status` (`/preview` dropped with its broken script; `/coordinate` merged into `/orchestrate`).
- Every `.agents/agent|skills|scripts/` path became an absolute `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/...` path (93 broken references before).
- All files LF, UTF-8.

## Policies (one definition each — see DECISIONS.md §3)
- Questions: ask only when the answer changes the build; 1–3 questions for new apps/multi-file work; proceed on simple tasks. No 3-question floor, no re-asking after "proceed".
- One announcement line (`🤖 @agent · skills: …`), informational only.
- One phase model: ANALYZE → PLAN → BUILD → VERIFY (defined in `code-rules`).
- Plan file: `docs/plans/{task-slug}.md`, required only for NEW APP / COMPLEX.
- Verification: `checklist.py` gates on required checks only (security high+, lint, type check, tests); everything else is advisory. Auto-fix required failures; report advisory ones.
- `DESIGN.md` is the single design gate and the token source of truth (`design-spec` owns the format; `frontend-design` consumes it).
- Purple / shadcn / Inter / glass etc. are anti-default heuristics, not bans; `DESIGN.md` overrides; scripts warn, never fail.
- Memory is per project (`<project>/.agents/memory/MEMORY.md`), read only if it exists.

## Agents (20 → 17)
- Deleted: `game-developer`; `product-owner` merged into `product-manager`; `qa-automation-engineer` merged into `test-engineer`.
- `frontend-specialist` 26 KB → 6 KB (design judgment moved to the `frontend-design` skill; contradictions removed). `project-planner` 15 KB → 5 KB. `mobile-developer` 13 KB → 5 KB.
- `orchestrator` holds the canonical file-ownership table for all 17 agents.
- Frontmatter: `name`, `description` (ending with `Triggers on: …`), `skills`, `version` — `tools`/`model` dropped (ignored by Antigravity).

## Skills (47 → 40)
- Deleted: game-development (10), rust-pro, intelligent-routing (→ `request-routing` rule), behavioral-modes (→ `core-protocol`), code-review-checklist, code-review-graph, documentation-templates, context-compression, batch-operations, skillify.
- Merged: simplify-code → clean-code; coordinator-mode → parallel-agents; tdd-workflow + webapp-testing → testing-patterns; geo-fundamentals → seo-fundamentals; bash-linux + powershell-windows + server-management → shell-ops; deployment-procedures → `/deploy`; api-patterns and database-design sub-files inlined.
- `frontend-design/SKILL.md` 89 KB → 35 KB; `redesign.md` folded into it; style files marked as explicit exceptions.
- Tech refresh to September 2026: Next.js 16 / React 19.2 compiler-first, Tailwind v4 (`@custom-variant dark`), `motion/react`, TanStack Query instead of SWR, Better Auth (Lucia deprecated), `redis.asyncio`, httpx `ASGITransport`, Prisma 7, UUIDv7, ESLint 9 flat config, Expo SDK 54+/Reanimated 4/FlashList v2, iOS 26 / Android 16 baselines, current AI-crawler names, IETF RateLimit headers.

## Scripts
- `validate_kit.py` rewritten for this layout (0 errors); manifest/lock/dependency-graph machinery removed; `auto_preview.py` (broken) and `convert_rules.py` (dead) deleted; `build_quick_reference.py` added.
- `validation_runner.py`: only required checks gate success. `lint_runner.py`: runs ruff/mypy only if installed. `test_runner.py`: `sys.executable`. `ux_audit.py`: purple is an advisory warning with a `DESIGN.md` override. `react_performance_checker.py`: memoization check removed. `lighthouse_audit.py`: no `--no-sandbox`.
- `tests/test_toolkit.py`: 12 tests, all passing.

## Maintaining the kit
1. Edit agents/skills.
2. `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/validate_kit.py`
3. `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/build_quick_reference.py --write`
4. `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/tests/test_toolkit.py`
