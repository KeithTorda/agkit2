---
name: rule-01b-theme-quick
version: 3.2.0
priority: P0
trigger: glob
globs: "**/*.html, **/*.css, **/*.scss, **/*.tsx, **/*.jsx, **/*.vue, **/*.svelte, **/*.astro, **/*.blade.php, **/tailwind.config.*, **/components/**, **/resources/views/**"
description: Rule 01 quick card - the 12 must-dos of the Unified Theme System. Full text is rule-01-unified-theme-system.
---

# RULE 01 QUICK CARD — UNIFIED THEME SYSTEM

Full rule: `rule-01-unified-theme-system`. This card is the short version to apply on every UI change.

1. **One theme system.** Reuse the project's existing theme provider and tokens. Add a new provider only when none exists.
2. **Three modes.** Light, Dark, System. Store `themePreference` (`light|dark|system`) and derive `resolvedTheme` (`light|dark`). Default: System.
3. **Token chain.** Primitive palette → semantic tokens (`background`, `foreground`, `surface`, `surface-elevated`, `primary`, `muted`, `border`, `ring`, `success`, `warning`, `error`, `info`) → component tokens → components.
4. **Colors only from tokens.** Raw color values live only in the token files. Components use token names.
5. **No flash on load.** Set the resolved theme before first paint (inline head script or server-read preference). No hydration mismatch.
6. **Persist and follow the OS.** Save explicit choice; restore on reload; in System mode listen to `prefers-color-scheme` changes.
7. **Native controls match.** Set `color-scheme` so scrollbars, inputs, date pickers and selects follow the theme.
8. **Every component themed.** Sidebar, navbar, cards, tables, charts, forms, dropdowns, modals, toasts, tooltips, portals and third-party widgets.
9. **Charts and effects per theme.** Chart axes, grids, tooltips and series use chart tokens; glow, glass and shadows have separate light and dark intensity.
10. **Contrast.** WCAG 2.2 AA: text 4.5:1, large text and UI indicators 3:1. Visible focus ring in both themes.
11. **Motion.** Animate `transform` and `opacity`; 150–300 ms; respect `prefers-reduced-motion`.
12. **Switching keeps state.** Changing theme does not reset forms, navigation, selections or data.

## Stack mapping

- Bootstrap 5.3: `data-bs-theme` on `<html>`, tokens mapped to `--bs-*`, System mode resolved in a head script.
- Tailwind: tokens as CSS variables; dark variant bound to the same attribute the provider sets.
- Next.js: one provider (e.g. next-themes) with `suppressHydrationWarning` on `<html>`.

## Before you answer, check

- [ ] Every color I added is a token with a light and a dark value.
- [ ] Theme is set before first paint and persists.
- [ ] Focus, hover, disabled and error states work in both themes.
