---
name: design-rules
version: 2.5.0
priority: P0
trigger: glob
globs: "**/*.html, **/*.css, **/*.scss, **/*.tsx, **/*.jsx, **/*.vue, **/*.svelte, **/*.astro, **/*.blade.php, **/*.dart, **/components/**, **/resources/views/**"
description: UI work - DESIGN.md is the source of truth, accessibility is firm, anti-template guidance is judgment not bans. Colour values never come from this rule.
---

# Design Rules

1. **Brief first.** Before a new page or screen, state in one line who uses it, on what device, to do what. The layout follows that job.
2. **`DESIGN.md` is the truth.** Its colours, type, spacing, radii and style direction override every skill default. New app or new page-level UI without one: write a short one (`design-spec`). Existing project without one: infer tokens from the current CSS and match it. Bug fixes never need one.
3. **The client's taste wins.** If the brief or `DESIGN.md` asks for gradients, glass, glow, bold animation, dark neon, a 3D hero - build it well. The kit's anti-template guidance (`anti-template` skill) lists defaults that make work look generated; treat each as a question ("does this page need it?"), not a ban.
4. **Firm: accessibility.** Text contrast at least 4.5:1 (3:1 for large text and UI outlines), real `<button>`/`<a>`/`<label>`, visible focus, alt text, keyboard reachable, `prefers-reduced-motion` respected, usable at 390 px and 1440 px.
5. **Firm: honest copy.** No hype words or fake-excited microcopy in system text (`anti-template` part 01-04). Buttons say what they do.
6. **One system per project.** One CSS approach, one icon set, at most two font families, unless `DESIGN.md` says otherwise.
7. **Tokens, not magic values.** Colours, spacing and radii come from tokens (`:root` variables or Tailwind `@theme`). Component CSS lives with its component (`css-architecture`).
8. **Motion with purpose.** Animate `transform` and `opacity`; keep UI feedback 150-400 ms; larger motion only where the design calls for it.

Owners: web UI → `frontend-specialist` (`frontend-design`), mobile → `mobile-developer` (`mobile-design`), flows and screens in planning → `ux-architect`.
