---
name: design-rules
version: 2.0.0
priority: P0
trigger: glob
globs: "**/*.tsx, **/*.jsx, **/*.vue, **/*.svelte, **/*.astro, **/*.css, **/*.scss, **/*.blade.php, **/*.dart, **/components/**, **/resources/views/**"
description: Apply when touching UI files — the DESIGN.md gate, anti-default heuristics, and which skill owns design decisions.
---

# Design Rules

## DESIGN.md (single gate)
`DESIGN.md` at the project root is the source of truth (format: `design-spec` skill). Required before building a new app or a new page-level UI. For components in an existing project without `DESIGN.md`: infer from existing styles, say so, and offer to create `DESIGN.md`. Bug fixes and trivial tweaks skip the gate. When it exists, its tokens override any skill guidance.

## Ownership
- Web UI (React/Next.js, Vue/Nuxt, Blade/Livewire/Inertia): `frontend-specialist` agent → `frontend-design` skill (design read, dials, layout, motion, redesign protocol) + `tailwind-patterns`.
- Mobile UI: `mobile-developer` agent → `mobile-design` skill.
- Tokens and their format: `design-spec` skill. Live guideline checks: `web-design-guidelines`.
Design judgment lives in those skills, not in agent files or here.

## Anti-defaults, not bans
Purple/violet primaries, Inter, shadcn/ui, glassmorphism, three equal cards, centered hero over a dark mesh, and similar are anti-default heuristics: don't reach for them unexamined; use them when the brief, brand, or `DESIGN.md` asks. Scripts (`ux_audit.py`, `accessibility_checker.py`, `mobile_audit.py`) are advisory and never block.

## Always
Accessible by default (labels, focus-visible, contrast, `prefers-reduced-motion`), responsive, no layout-property animations, no fake screenshots built from divs, and one design system per project.
