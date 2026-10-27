# AGKIT2 v2.9 — Rule reset plan

Date: 2026-10-27
Requested by: Keith (Nikko)

## Goal

Remove the old rule set, keep agents/skills/scripts working, make Rule 01 (Unified Theme System) the rule the kit is built on, and strip the motion-video feature and every place where a browser check was effectively mandatory.

## Decisions

| Item | Decision |
|---|---|
| Old rules (`core-protocol`, `code-rules`, `design-rules`, `engineering-excellence`, `request-routing`, `universal-rules`) | Deleted. |
| New rules | `kit-core.md` (always on, small: kit path + agent/command routing + "checks only when asked") and `rule-01-unified-theme-system.md` (Keith's Rule 01, verbatim, loads for UI files). `quick-reference.md` stays as the generated catalog. |
| Why `kit-core` exists | Agents and skills locate their files through the `KIT` path, and the AI picks agents/commands from the routing table. Without it the kit stops working. It contains no style or design policy. |
| Motion | `/motionv` skill, its scripts, and the `videos/` folder removed. UI animation guidance (`frontend-design/motion.md`) stays because Rule 01 §10/§14 relies on it. |
| Browser checks | No skill or agent runs a browser, screenshot or `/see` pass automatically. `/see`, `/verify`, `/fix-ui` re-check and `browser-verification` run only when Keith asks. |
| Design intake question | No longer mandatory. Agents ask about style only when the direction is genuinely unclear. |
| Version | 2.9.0 |

## Steps

1. Write new `rules/kit-core.md` and `rules/rule-01-unified-theme-system.md`.
2. Update agents (frontend, mobile, ux, backend, devops, performance) — drop old-rule references and mandatory browser steps.
3. Update skills that referenced old rules or forced a browser check (css-architecture, tailwind-patterns, ui-repair, fix-ui, lint-and-validate, testing-patterns, frontend-design, design-spec, anti-template, brainstorm(ing), enhance, create, plan, orchestrate, parallel-agents, app-builder, verify-changes, browser-verification, proplan).
4. Update `validate_kit.py`, `build_quick_reference.py`, `kit_doctor.py`, `install.ps1` and tests to the new rule names; regenerate `quick-reference.md`.
5. Delete old rule files, `skills/motionv/`, `videos/` (script `cleanup-v2.9.ps1`, backs up first).
6. Run `install.ps1` so Antigravity's active copy (`~/.gemini/config/rules`, plugin, GEMINI.md block) matches. The installer moves the old active rules to `agkit-backups`.

## Rollback

`Desktop/agkit2-backup-v2.8.3/` (full copy made by the cleanup script) and `~/.gemini/config/agkit-backups/<timestamp>/` (made by the installer).
