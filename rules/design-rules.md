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
The anti-default list (what not to reach for unexamined, and when it is fine) is defined once in `frontend-design` §0.E and §4.8; mobile equivalents in `mobile-design`. Every UI build starts with a named reference and a screen read (`frontend-design` §0.C, §0.F): a target to aim at and a job the screen must do, before any layout. Scripts (`ux_audit.py`, `accessibility_checker.py`, `mobile_audit.py`) are advisory and never block; an agent's own draft UI is refined against the render, not escalated (`code-rules` auto-fix policy).

## Always
Accessible by default (labels, focus-visible, contrast, `prefers-reduced-motion`), responsive, no layout-property animations, no fake screenshots built from divs, and one design system per project.

### Ultra High-Contrast Typography & Badges (Anti-Blur Invariant)
- **Pure Contrast Standard**: Never use washed-out/faded grays (e.g. `#94A3B8`, `#64748B`) or muddy low-contrast text on dark surfaces. In dark themes, primary text must be Pure White (`#FFFFFF`) and secondary/table text must be bright high-contrast (`#F1F5F9` / `#E2E8F0` with 10:1+ contrast) so content is 100% sharp and readable even for visually impaired or elderly users. In light themes, use Pure Black (`#000000`) / Slate-900.
- **Radiant Status Badges**: Never place dark colored text on dark backgrounds (e.g. dark green on navy). Status pills on dark surfaces must use luminous foregrounds with semi-transparent tinted backgrounds and borders (e.g. Emerald `#34D399` text + border with subtle glow).
- **CSS Architecture Layering**: Encapsulate reusable card, button, and surface styles within `@layer components { ... }` in CSS to prevent specificity collisions with utility classes.

