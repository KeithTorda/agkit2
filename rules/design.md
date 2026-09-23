---
name: design
version: 3.0.0
priority: P0
trigger: glob
globs: "**/*.html, **/*.css, **/*.scss, **/*.tsx, **/*.jsx, **/*.vue, **/*.svelte, **/*.astro, **/*.blade.php"
description: UI rules. DESIGN.md is the source of truth; contrast is a principle, not a hex value.
---

# Design

1. **`DESIGN.md` is the truth.** If the project has one, its colours, fonts, spacing and radii override every skill and every default. If it does not and you are building a new page or app, create one with the `design-spec` skill (10 lines is enough) before building. A bug fix or small tweak never needs one.
2. **Contrast is a principle.** Body text ≥ 4.5:1 against its background, large text ≥ 3:1. No dark-on-dark, no light-on-light. The actual colours come from `DESIGN.md`; this rule never dictates a hex value.
3. **One design system per project.** No mixing Tailwind and Bootstrap, no second icon set, no third font.
4. **Not a template (Anti-AI Design & Copy).** Before building a page, say in one line what it is for and who reads it, then choose layout for that. Strictly avoid tropes that look AI-generated:
   - *Visual:* Grid of identical cards for everything, hero + three features + CTA, gradient text, neon/glow shadows, frosted glass (glassmorphism), cards inside cards, decorative gradients in content areas.
   - *Copy & Voice:* Follow `copy.md`. Ban hype adjectives (`seamless`, `robust`, `blazing`, `delightful`), hype verbs (`unlock`, `empower`, `supercharge`), and fake-excited microcopy (`Nothing here yet! Your journey starts soon ✨`). Use plain, direct, functional words (`No threads yet.`, `Saved.`, `Search threads`).
5. **Accessible by default.** Real `<button>`/`<a>`/`<label>`, visible focus, alt text, `prefers-reduced-motion`, works at 390 px and 1440 px.
6. **CSS organisation.** Tokens in `:root` (or Tailwind `@theme`), one file per component, no global override file. Plain-CSS and Tailwind projects follow the `html-css-js` and `react` skills respectively.
7. **Motion is small.** 150–400 ms, opacity/transform only, never animate layout properties.
8. **Existing project without `DESIGN.md`:** infer tokens from the current CSS, say so in one line, and match it.
