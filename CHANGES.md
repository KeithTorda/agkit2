# Changes

## 4.0.0 - 2026-11-18

- **Zero-Conflict 3-Layer CSS Architecture:** Locked separation of `style.css` (Layer 1 vendor read-only), `component-catalog/08-COMPACT-PURE-CONTRAST-OVERRIDE.css` (Layer 2 semantic token bridge `--kit-*`, `--on-*`, `--primary-ink` verified WCAG AA >= 4.5:1 across all 15 presets and Light/Dark modes), and project `app.css` (Layer 3 `.app-*` namespace only, zero `!important`, zero raw `#hex`).
- **Automated Hygiene & Validator Guards:** Added `scripts/audit_project_hygiene.py` (blocks `!important`/hex/global selectors in `app.css`, `text-dark`/`bg-white`/`bg-light`/`javascript:void(0)` in templates, and template placeholder leftovers) and `scripts/validate_keith_kit.py`.
- **Unified Master Rules & 24-Point Anti-AI-Error Registry:** Rebuilt `rules/AGENTS.md` + `rule-01`..`rule-04` (all `< 11 KB`, `0 warnings`), synced `docs/GEMINI.md` (`v2.5.0`) and `docs/AI-ERROR-REGISTRY.md`, and mandated simple plain English copy, zero sample data, server-side integer/decimal money precision, fail-fast `.env` validation, and Contabo VPS backup checks.
- **Complete Bootstrap 5 Dashboard Pro Library:** Bundled all 67 reference HTML pages, 8 itemized `component-catalog/` guides, mandatory Right-Side UI Kit Settings Panel rule (`demo.js` + `styleSwitcher.js` single cookie store), 3 focused skills (`bootstrap-pro-ui`, `laravel-fullstack`, `vps-safe-deploy`), and 4 write-enabled subagents.

## 3.3.0 - 2026-11-04

- Creative freedom in UI: rewrote `rule-07` from a strict template checklist into a flexible design guide; moved full `rule-01` and `rule-04` to `model_decision` triggers so they load only when needed.
- Removed Bootstrap defaults: deleted `bootstrap-patterns` and Bootstrap block templates; agents and skills now adapt to whatever CSS stack a project uses.

## 3.2.0 — 2026-10-27

- Gemini fit: Rule 01b quick card; "Before you answer, check" recap on every rule; "Do not" lists rewritten as positive instructions; proof-of-work (pasted output) and `Rules applied` line in reports; session discipline in kit-core; Rule 04 now loads by glob on backend/db paths and Rule 05 is always on; validator flags rule files over 12,000 characters (info) and 24,000 bytes (error).
- New skills: `template-ui-blocks` (Bootstrap 5.3 + Tailwind copy-ready blocks for every Rule 07 recipe), `laravel-patterns`, `bootstrap-patterns`, `ph-business-compliance`, `init-project` (`/init-project` + AGENTS.md template).
- Rewritten short and direct: create, enhance, plan, proplan, orchestrate, debug, fix-ui, frontend-design, see, review, api-patterns, database-design, testing-patterns, deploy, verify.
- Cleanup: removed `anti-template` (252 KB, conflicted with Rule 07), `docs/history`, `docs/reviews`, `AG_KIT_SLASH_COMMANDS.md`, one-off install scripts; plans moved to `docs/plans/`; CHANGES and DECISIONS rewritten.
- Eval set: `docs/eval/` prompts with pass checklists to test the kit in Antigravity.

## 3.1.0 — 2026-10-27

- Rule 07 Template-Grade Design; design agents and skills default to template-grade; README rewritten.

## 3.0.0 — 2026-10-27

- Own rule set (Rules 02–06 + kit-core); 20 agents rebuilt as 14 on one template; skills, validator, tests and installer updated.

## 2.9.0 — 2026-10-27

- Old rules removed; Rule 01 Unified Theme System added; `/motionv` and mandatory browser checks removed.

Older history (2.x) is in the git log.
