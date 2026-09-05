# AG Kit v2 — Decisions (single source of truth for every edit)

Every editor (human or sub-agent) follows this file. When a file you edit disagrees with this
file, this file wins. Do not invent new policies; if something is unspecified, choose the
simplest option and note it in your summary.

## 1. Install layout (Antigravity IDE, Windows host, user Keith)

| Thing | Location |
|---|---|
| Kit root (`AG_KIT`) | `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2` |
| Global always-on entry (no frontmatter) | `C:/Users/Keith/.gemini/GEMINI.md` |
| Global rules with triggers (the ONLY copy) | `C:/Users/Keith/.gemini/config/rules/*.md` |
| Plugin manifest | `AG_KIT/plugin.json` |
| Agent persona docs (read on demand by path) | `AG_KIT/agents/<name>.md` |
| Skills (Antigravity skills; each is also a `/<name>` slash command) | `AG_KIT/skills/<name>/SKILL.md` |
| Kit runner scripts | `AG_KIT/scripts/*.py` |
| Skill scripts | `AG_KIT/skills/<skill>/scripts/*.py` |
| Project memory (per project, optional) | `<project>/.agents/memory/MEMORY.md` |
| Plan files (per project) | `<project>/docs/plans/{task-slug}.md` (create the folder; monorepo → repository root) |
| Design tokens (per project) | `<project>/DESIGN.md` |

- The plugin has **no** `rules/` directory (rules live only in `~/.gemini/config/rules/`) and **no** `workflows/` directory (workflows are deprecated in Antigravity; former workflows are now skills named after the slash command).
- Paths in markdown are either absolute with forward slashes under `AG_KIT`, or relative links inside a skill folder (`./scripts/x.py`, `./sub-file.md`). Never `.agents/agent/...`, `.agents/skills/...`, `.agents/scripts/...`.
- Commands must work in PowerShell: `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .`
- UTF-8, LF line endings, no trailing whitespace noise.

## 2. Frontmatter contracts

- `agents/*.md`: `name` (== filename), `description` (one paragraph; must end with `Triggers on: <keywords>.`), `skills` (comma list; every entry must exist in `skills/`), `version` (semver).
- `skills/*/SKILL.md`: `name` (== directory), `description` (what it does AND when to use it, third person — this is what Antigravity uses to decide activation), `version`. No `allowed-tools` (Claude Code field; Antigravity ignores it).
- Rules: `name`, `trigger` (`always_on` | `model_decision` | `glob`), `description` (required for `model_decision`), `globs` (for `glob`), `priority` (P0/P1/P2), `version`.

## 3. Canonical behavior rules (each has one home — see §4; elsewhere point, never paraphrase)

1. **Questions.** Ask only when the answer changes what you would build — scope, data model, security, architecture, or a design direction you cannot infer. New app or multi-file feature: ask 1–3 targeted questions in one message before planning. Bug fix, single-file change, UI tweak: proceed and state your assumptions. Never ask twice before starting; if the user says "proceed", proceed with stated defaults.
2. **Announcement.** At most one line at the top of a code or design response: `🤖 @<agent> · skills: <a>, <b>`. It is informational, never a gate. No other announcement formats exist.
3. **Phases.** One model, defined once in `code-rules.md`: ANALYZE → PLAN → BUILD → VERIFY. Every other file references it instead of redefining it. Antigravity's native Planning Mode is the PLAN phase.
4. **Plan file.** Required for NEW APP and COMPLEX tasks (multi-file or structural change): `docs/plans/{task-slug}.md`, kebab-case, never `plan.md`/`PLAN.md`. Simple tasks: a 1–3 line plan in the response is enough. A missing plan file never blocks a simple task. Format: `plan-writing` skill (checkbox tasks with owner and verify line).
5. **Auto-fix.** Failures of required checks (security high+, lint, type errors, failing tests) are fixed automatically. Advisory findings (UX, SEO, GEO, mobile, API heuristics) are reported; ask before making changes they suggest that touch design or scope.
6. **Design tokens.** `DESIGN.md` at the project root is the source of truth (format: `design-spec` skill). Required before building a new app or a new page-level UI. For components in an existing project without `DESIGN.md`: infer from existing styles, say so, and offer to create `DESIGN.md`. Bug fixes and trivial tweaks skip the gate.
7. **Anti-defaults, not bans.** Purple/violet primaries, Inter, shadcn/ui, glassmorphism, three equal cards, etc. are *anti-default heuristics*: don't reach for them unexamined; use them when the brief, brand, or `DESIGN.md` asks. Scripts may warn about them, never fail.
8. **Memory.** If `<project>/.agents/memory/MEMORY.md` exists, read it at session start. Otherwise do nothing. `/remember` creates it.
9. **Loading.** Read the agent file for the routed agent. Load a skill only when its description matches the task. Inside a skill, read `SKILL.md` first, then only the section files it points to for the current need. Never load every skill in an agent's list up front.
10. **Verification.** Fast gate: `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .` Release gate: `verify_all.py`. "Done" means required checks pass and logic changes have tests.
11. **Ownership (multi-agent).** The file-ownership table in `agents/orchestrator.md` is canonical: `backend-specialist` owns API/server, `database-architect` owns schema/migrations, `frontend-specialist` owns web UI, `mobile-developer` owns mobile UI/native layer only, `test-engineer` owns tests, `devops-engineer` owns CI/deploy. Mobile apps with a backend use `backend-specialist` for the backend.
12. **Agent count.** Use the minimum number of agents the task needs. A single specialist is a valid outcome of orchestration. If subagents are not available in the current Antigravity surface, execute the plan yourself acting as each specialist in turn (writers sequentially, in ownership order).
13. **Language.** Rule and skill files are English. Respond in the user's language; code, comments, identifiers, and commit messages in English.

## 4. Style rules for every file

- No "you have FAILED", "PROTOCOL VIOLATION", "VIOLATION", "🔴", "STOP →", "Maestro", "MANDATORY" in caps. Plain imperative sentences. Use "must" only for the rules in §3.
- No ASCII table-of-contents blocks; no "Spirit of the agent" closers; no restating a skill's content inside an agent file — point to the skill.
- No Claude/Cursor/Windsurf terms: never "Claude Write tool", "ask/edit mode", "Cursor", "Windsurf". Antigravity terms: Planning Mode, Fast Mode, Agent Manager, subagents, Artifacts.
- Each rule/protocol lives in exactly one file. Elsewhere write `See <file>` with the path.
- Prefer durable phrasing over version numbers; where a version matters, use the Sept 2026 baseline below.

## 5. Tech baseline (September 2026)

- **Web:** Next.js 16 (App Router; Turbopack default; `next lint` removed — use the project's ESLint script), React 19.2, compiler-first when the React Compiler is enabled (`reactCompiler: true` in next.config / babel-plugin-react-compiler in Expo — the kit's templates enable it; check the flag before removing manual memo), TypeScript 5.9+, Tailwind CSS v4 (`@import "tailwindcss"`, `@theme`, `@custom-variant dark (&:where(.dark, .dark *))`, `@plugin`), `motion/react` (not `framer-motion`), Lucide/Phosphor icons acceptable, shadcn/ui + Radix acceptable foundations.
- **Data layer default:** Server Components for reads; Server Actions + `useActionState` for mutations; TanStack Query only for client-interactive server state (polling, infinite lists, optimistic UI). Replace SWR references with TanStack Query.
- **Node/Python/PHP:** Node 24 LTS (`node:test` or Vitest); standalone APIs default to Hono (Fastify when Node-heavy; Express only in existing code; inside Next.js use Route Handlers + Server Actions); ESLint 9+ flat config (`eslint.config.js`; `.eslintrc` is legacy); Python 3.13+ (3.14 current) with Ruff + mypy/pyright, httpx `ASGITransport(app=app)`, `redis.asyncio` (not aioredis), Django 5.2 LTS / 6.x, FastAPI current; PHP 8.4 / Laravel 12 with Eloquent, Pest or PHPUnit, Pint, Larastan.
- **Auth:** Better Auth or Clerk; Auth.js for existing projects; Lucia is deprecated.
- **DB:** Postgres 17/18, Prisma 7 (edge-capable, Rust-free client) or Drizzle; UUIDv7 (RFC 9562) for sortable IDs; ULID only for legacy compatibility.
- **Mobile:** Expo SDK 54+ with Expo Router, React Native New Architecture, Reanimated 4, FlashList v2 (no `estimatedItemSize`), NativeWind 4+; Flutter 3.3x with Riverpod/Drift; iOS 26 (Liquid Glass) and Android 16+ (Material 3 Expressive) are the platform baselines.
- **Other:** Nuxt 4, Astro 5, current Vite / Playwright / Lighthouse, OWASP Top 10:2025, MCP specification 2026-07-28 (stateless, `server/discover`), WebGPU shipping in Chrome/Firefox/Safari.

## 6. Final inventory

**Agents (17):** backend-specialist, code-archaeologist, database-architect, debugger, devops-engineer, documentation-writer, explorer-agent, frontend-specialist, mobile-developer, orchestrator, penetration-tester, performance-optimizer, product-manager (absorbs product-owner), project-planner, security-auditor, seo-specialist, test-engineer (absorbs qa-automation-engineer).
Deleted: game-developer, product-owner, qa-automation-engineer.

**Skills kept (28):** api-patterns (sub-files inlined), app-builder (+templates), architecture, brainstorming, clean-code (absorbs simplify-code), database-design (thin sub-files inlined), design-spec, frontend-architecture, frontend-design, i18n-localization, lint-and-validate, mcp-builder, memory-system, mobile-design, nextjs-react-expert, nodejs-best-practices, parallel-agents (absorbs coordinator-mode), performance-profiling, plan-writing, python-patterns, red-team-tactics, seo-fundamentals (absorbs geo-fundamentals), systematic-debugging, tailwind-patterns, testing-patterns (absorbs tdd-workflow + webapp-testing), verify-changes, vulnerability-scanner, web-design-guidelines.
**New skill:** shell-ops (merges bash-linux + powershell-windows + server-management).
**Command skills (11, from former workflows):** brainstorm, create, plan, debug, test, verify, deploy (absorbs deployment-procedures), orchestrate (absorbs coordinate), enhance, remember, status.
**Deleted skills:** game-development/*, rust-pro, intelligent-routing (→ request-routing rule), behavioral-modes (→ core-protocol rule), code-review-checklist, code-review-graph, documentation-templates, context-compression, batch-operations, skillify, simplify-code, tdd-workflow, webapp-testing, geo-fundamentals, bash-linux, powershell-windows, server-management, coordinator-mode, deployment-procedures.
**Deleted scripts:** scripts/auto_preview.py, skills/nextjs-react-expert/scripts/convert_rules.py.
