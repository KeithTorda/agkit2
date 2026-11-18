---
trigger: glob
globs: "**/*.html, **/*.css, **/*.scss, **/*.tsx, **/*.jsx, **/*.vue, **/*.svelte, **/*.blade.php, **/*.ejs, **/components/**, **/views/**, **/pages/**, **/app/**/page.*"
description: Enforces stack-agnostic component catalog reuse, Zero-Conflict @layer & semantic token CSS, WCAG AA contrast across all 15 presets, responsive sidebars, and accessible UI states.
---

# RULE 01 — STACK-AGNOSTIC UI DESIGN, COMPONENT TYPES & ZERO-CONFLICT CSS

Component & Screen Type Catalog: `c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit/component-catalog/`
Portable Token & Settings Engine: `c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit/ui-kit/`

## 1. Build Cleanly in Any UI Stack

1. **Match or Choose the Right Stack:** Support Tailwind CSS + shadcn/ui, React/Next.js, Laravel Blade/Livewire, Vue/Svelte, Vanilla CSS (`ui-kit/keith-ui-tokens.css`), or Bootstrap 5 without forcing third-party template bloat.
2. **Map Component Types First:** Consult `component-catalog/00-MASTER-SCREEN-AND-COMPONENT-TYPES.md` (`01` tokens, `02` shells/sidebars, `03` KPIs/cards/charts, `04` tables/ledgers, `05` forms/wizards, `06` buttons/badges/modals, `07` auth/invoices/POS/errors) so every screen ships complete variants and states.
3. **Right-Side Live Theme Settings Drawer:** On admin dashboards and workspace shells, include the complete right-side customizer (`ui-kit/keith-ui-settings.js` or `<ThemeSettingsDrawer />`) supporting Light/Dark mode, 15 WCAG AA color presets, Vertical/Horizontal layout, Sidebar mode (`full`, `mini`, `compact`, `floating`), Font style, and Reset — persisted in **one single state store**.

## 2. Zero-Conflict Token & `@layer` CSS Architecture

1. **Semantic Tokens Only (Zero Raw Hex in Components):**
   - Bind all surfaces, borders, text, and accents to CSS variables (`--ui-canvas`, `--ui-surface`, `--ui-surface-subtle`, `--ui-border`, `--ui-ink`, `--ui-ink-muted`, `--ui-primary`, `--on-primary`, `--primary-ink`, `--on-sidebar`, `--on-header`) or Tailwind semantic tokens (`bg-background`, `bg-card`, `text-foreground`, `border-border`, `bg-primary`, `text-primary-foreground`).
   - Pair solid primary fills with `--on-primary` and text links/outlines/soft badges with `--primary-ink` so all 15 presets pass `>= 4.5:1` WCAG AA contrast in both Light and Dark modes.
2. **Layered & Scoped Custom CSS:**
   - Declare `@layer tokens, base, components, utilities;` when authoring custom CSS, and never edit vendor stylesheets directly.
   - Scope custom domain styles to `.app-*` (or CSS Modules) with **zero `!important`** and **zero raw `#hex` colors** outside `:root` / `@layer tokens`.
3. **Banned Dark-Mode Breakers in Markup:**
   - Never put unpaired light-only utilities (`text-dark`, `text-black`, `bg-white`, `bg-light`) or inline `style="color:...; background:..."` in markup.
   - Never write blanket `svg path { fill }` rules that overwrite multi-color brand marks.

## 3. Responsive Layout, Premium Craft & Accessibility

- **Responsive Parity (`<640px` Mobile, `768px–1024px` Tablet, `1280px+` Desktop):**
  - Centralize navigation items in one config; lock desktop sidebars to `100dvh` (`sticky top-0 h-screen flex flex-col shrink-0`), use explicit collapsed/expanded widths (`76px` vs `248px`), set `<nav>` to `overflow-visible` when collapsed so tooltips are never clipped, and synchronize mobile drawer breakpoints (`768px`).
  - Wrap all tables in `overflow-x-auto` / `.table-responsive` and configure bottom-row dropdowns to flip upward (`dropup`).
- **Visual & Semantic Precision:**
  - Pure `#000000` (Light) / `#ffffff` (Dark) primary text contrast; `tabular-nums` on all numbers, `₱` amounts, IDs, and dates.
  - One primary button CTA per card/form; soft tinted `StatusBadge` pills inside tables (`Ready`, `Pending`, `Paid`).
  - Replace every `javascript:void(0)` with `<button type="button">`, never nest `<button>` inside `<a>`, add `aria-label` on icon-only controls, `<th scope="col">` on table headers, `:focus-visible` outlines, `aria-live="polite"` on dynamic toasts/alerts, and explicit `width`/`height` or `aspect-ratio` on media.

## 4. Motion & Hygiene Check

- Uniform SVG grid (`viewBox="0 0 24 24"`, `stroke-width` `1.75` or `2`). Animate only `transform` and `opacity` (`120ms–220ms` `cubic-bezier(0.23, 1, 0.32, 1)`) bound to parent interactive controls; honor `@media (prefers-reduced-motion: reduce)`.
- Run `python "c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit/scripts/audit_project_hygiene.py" <project_dir>` after UI/CSS edits.
