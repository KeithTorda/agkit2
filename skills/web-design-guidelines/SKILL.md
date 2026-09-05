---
name: web-design-guidelines
description: Reviews built web UI code against Vercel's Web Interface Guidelines (accessibility, interaction, forms, performance, copy) by fetching the current rule set live, with a local fallback floor when the fetch is unavailable, and reporting file:line findings. Use after UI code exists, when asked to review UI, check accessibility, audit design or UX, or check a site against best practices. Not for designing new UI (frontend-design).
version: 2.0.0
---

# Web Interface Guidelines review

Audit-only skill. It fetches the live rule set and applies it to the files under review; it carries no full copy of the rules, only the short fallback floor below for when the fetch is unavailable.

## Procedure

1. **Fetch the current guidelines** with the session's fetch or browsing tool: `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` (last verified 2026-09-05). This is a live external dependency and can move: if it 404s, returns non-markdown, or no fetch tool is available, say so and fall back to the floor below plus `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/frontend-design/scripts/accessibility_checker.py <dir>` and `frontend-design` §10. Do not reconstruct the guideline text from memory — audit against the floor and say which source you used.
2. Read the files or pattern the user named; if none, ask which files to review (one question).
3. Apply every rule in the fetched document (or the floor, on fallback) to those files, leading with the highest-value checks below.
4. Report findings in the terse `file:line` format the fetched document specifies. Findings are advisory (see the auto-fix policy in the global `code-rules` rule): report them, ask before changing design or scope.

## Highest-value checks (lead with these; the floor when the live doc is unavailable)

The live guidelines are broad; these catch the most real defects. Thresholds and the full pre-flight live in `frontend-design` §4.4 (states, forms) and §10.

- **Accessibility** — keyboard-reachable and operable with a visible `focus-visible` ring; focus moved into an opened dialog and returned on close; real `<button>` / `<a>` / `<label>`, never `onClick` on a `<div>`; every control labelled and every image given `alt` (or `alt=""`); WCAG AA contrast in each shipped color scheme. Mechanical subset: `accessibility_checker.py`.
- **Responsive** — no horizontal scroll or clipped content at 320px; primary tap targets comfortably sized; every multi-column block collapses below `md`; `min-h-dvh`, not `h-screen`, on full-height sections.
- **States** — every async view ships loading (skeleton), empty, and error; forms validate inline with a pending/disabled submit, never `alert()`; interactive elements cover hover, `:active`, disabled, and focus.

## Where this sits

| Skill | Role |
|---|---|
| `design-spec` | Before coding: the project's `DESIGN.md` tokens |
| `frontend-design` | Before and during coding: design read, dials, layout / motion / copy defaults, anti-default heuristics, mechanical pre-flight |
| `web-design-guidelines` (this) | After coding: audit against the live Web Interface Guidelines |
