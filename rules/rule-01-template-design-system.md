---
trigger: glob
globs: "**/*.html, **/*.css, **/*.scss, **/*.tsx, **/*.jsx, **/*.vue, **/*.svelte, **/*.blade.php, **/*.ejs, **/components/**, **/views/**, **/pages/**, **/app/**/page.*"
description: Enforces Zero-Conflict 3-Layer CSS architecture, semantic theme tokens, Bootstrap 5 Dashboard Pro reuse, premium component elevation, and WCAG AA accessibility.
---

# RULE 01 — ZERO-CONFLICT CSS, TEMPLATE REUSE & PREMIUM UI (BOOTSTRAP 5 PRO)

Catalog & Locked Theme Bridge: `c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit/component-catalog/`
Raw Template Source: `c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit/reference-template/bootstrap-5-dashboard-pro/`

## 1. Reuse Before Writing Markup

1. Map every screen from `component-catalog/00-INDEX-AND-PAGE-MAP.md`:
   - **Overview / KPIs:** `index.html`, `index-2.html`, `widget-basic.html`
   - **Tables / Ledgers:** `page-transaction.html`, `page-invoices.html`, `table-datatable-basic.html`
   - **Forms / Wizards:** `form-element.html`, `form-validation.html`, `form-wizard.html`
   - **POS / Orders / Printable Invoices:** `ecom-product-grid.html`, `ecom-product-order.html`, `ecom-invoice.html`
   - **Auth & Errors:** `page-login.html`, `page-register.html`, `page-error-404.html`, `empty-page.html`
2. **Mandatory Right-Side UI Kit Settings Panel:** Every dashboard/app shell must load `js/demo.js` and `js/styleSwitcher.js` (or an equivalent React `RightUiKitSettingsDrawer`) so Light/Dark mode, `color_1..15` swatches (`Primary`, `NavHeader`, `Header`, `Sidebar`), Layout, Sidebar Style, Container Width, Typography, and Quick Presets work out of the box.
3. **Single Theme State Store:** Any custom Light/Dark header button must read and write the `version` cookie from `demo.js` (`getCookie('version')` / `setCookie('version', ...)`), never a separate `localStorage` key that resets UI Kit settings on reload.

## 2. Locked 3-Layer Zero-Conflict CSS Architecture

Load stylesheets in this exact order:
1. **Layer 1 (`style.css` — READ-ONLY Vendor Base):** Never edit.
2. **Layer 2 (`08-COMPACT-PURE-CONTRAST-OVERRIDE.css` — LOCKED Kit Theme Bridge):** Copy untouched from `component-catalog/`. Scales `html { font-size: 13px }`, enforces pure `#000000` / `#ffffff` contrast, syncs Bootstrap components to `var(--primary)`, and defines WCAG AA semantic tokens across all 15 presets and Light/Dark modes:
   - Surfaces & ink: `--kit-canvas`, `--kit-surface`, `--kit-surface-subtle`, `--kit-border`, `--kit-ink`, `--kit-ink-muted`
   - Region auto-contrast: `--on-nav-header`, `--on-header`, `--on-sidebar` (handles both Light swatches and Dark Mode `color_1` `#212130`)
   - Accent auto-contrast: `--on-primary` (solid fills) and `--primary-ink` (readable links, outlines, and `.light` badges >= 4.5:1)
3. **Layer 3 (`app.css` — Scoped `.app-*` Domain Styles ONLY):**
   - **STRICTLY BANNED in `app.css`:** Bare HTML tags (`body`, `h1..h6`, `a`, `label`, `table`), Bootstrap/Dompet classes (`.card`, `.btn*`, `.badge*`, `.form-*`, `.dlabnav`, `.header`, `[data-*]`), raw `#hex` colors, and `!important`.
   - **ONLY ALLOWED in `app.css`:** Custom `.app-*` classes consuming `var(--kit-*)`, `var(--primary)`, `var(--on-primary)`, `var(--primary-ink)`, `var(--rgba-primary-*)`.

## 3. Markup & SVG Hygiene (Anti-Conflict Rules)

- **Banned Color Utilities in Markup:** Never use `text-dark`, `text-black`, `bg-white`, `bg-light`, or inline `style="color:...; background:..."` in HTML/EJS/Blade/JSX (Bootstrap's `!important` breaks Dark Mode and dark header/sidebar swatches). Use `.kit-subtle-box`, `.kit-muted`, or `.badge.light.badge-*`.
- **Protect Multi-Color SVGs:** Never write blanket `svg path { fill: ... !important }`; keep multi-tone brand marks intact and bind only monochrome title paths (`.svg-title-path`) or `stroke="currentColor"` icons.
- **Valid Semantic & Keyboard-Safe HTML:**
  - Replace every `href="javascript:void(0)"` with `<button type="button">`. Never nest `<button>` inside `<a>`.
  - Add `aria-label` on icon-only `.btn.sharp` controls, `aria-hidden="true"` on decorative icons, `<th scope="col">` on table headers, `aria-live="polite"` on dynamic status/toast alerts, and visible `:focus-visible` outlines.
  - Set explicit `width`/`height` or `aspect-ratio` on images/video frames to prevent layout shift (CLS).

## 4. Premium Component Elevation Standards

Keep authentic Bootstrap 5 Dashboard Pro structure while elevating visual craft:
- **Cards:** Clean `.card-header` with plain `.card-title`, soft layered elevation (handled by `08-COMPACT-PURE-CONTRAST-OVERRIDE.css`), zero stacked double borders.
- **KPI Cards (`.invoice-card`):** `tabular-nums` on every metric/amount/date, circular tinted icon container, concise 2–3 word plain label.
- **Data Tables:** Wrap in `.table-responsive`, uppercase small-caps headers, right-aligned `.btn.sharp.btn-xs` actions, upward-safe dropdowns (`dropup`) on bottom rows, and full-width `<td colspan="...">` empty state when zero rows exist.
- **Buttons & Badges:** One primary `.btn-primary` CTA per card/form, `.btn-outline-primary` or `.light.btn-primary` for secondary actions, `.badge.light.badge-*` for table status pills (`Ready`, `Pending`, `Paid`). Lock submit buttons (`disabled` + `aria-busy="true"` + spinner) during requests.
- **Forms, Modals & Empty States:** Plain `<label for="...">` on every field, logical field grouping on long forms, inline field-level `.text-danger.small` errors, centered `EmptyState` (muted 48–64px icon + plain message + single CTA button).

## 5. Motion & Automated Verification

- Standardize custom SVGs (`viewBox="0 0 24 24"`, `stroke-width="1.75"` or `2`). Animate only `transform` and `opacity` (`120ms–220ms` `cubic-bezier(0.23, 1, 0.32, 1)`) triggered by parent controls; always honor `@media (prefers-reduced-motion: reduce)`.
- Run `python "c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit/scripts/audit_project_hygiene.py" <project_dir>` after UI/CSS edits to guarantee zero violations.
