---
name: bootstrap-patterns
description: "Bootstrap 5.3 setup and patterns: Rule 01 tokens mapped to --bs-* variables, data-bs-theme Light/Dark/System, Sass/CSS customization, components, React-Bootstrap usage and admin layouts. Use for any Bootstrap or React-Bootstrap UI."
version: 3.2.0
---

# Bootstrap 5.3 patterns

Make Bootstrap look like a premium template (rule-07) while keeping one token system (rule-01).

## Steps

1. **Check the version.** `data-bs-theme` color modes need Bootstrap 5.3+. Upgrade only if the user agrees.
2. **One theme attribute.** Set `data-bs-theme="light|dark"` on `<html>`. Bootstrap has no System mode: resolve `prefers-color-scheme` in an inline head script before paint, store the user's choice, and listen for OS changes (full script in `template-ui-blocks`).
3. **Map tokens to Bootstrap.** In one `theme.css` (or `_variables.scss`), set `--bs-body-bg`, `--bs-body-color`, `--bs-primary`, `--bs-primary-rgb`, `--bs-secondary-bg`, `--bs-tertiary-bg`, `--bs-border-color`, `--bs-emphasis-color`, `--bs-link-color`, `--bs-focus-ring-color` from your semantic tokens for `:root` and `[data-bs-theme="dark"]`.
4. **Sass projects.** Override `$primary`, `$font-family-sans-serif`, `$border-radius`, `$box-shadow*`, `$enable-shadows: true` before importing Bootstrap. Add custom colors to `$theme-colors` so utilities like `.text-bg-brand` exist.
5. **Components first.** Use Bootstrap components (navbar, offcanvas sidebar, dropdown, modal, toast, accordion, nav-tabs, pagination, badge, progress, placeholder for skeletons) with project classes for polish: soft shadows, larger radius, icon chips, hover lift.
6. **Forms.** `.form-control`, `.form-select`, `.form-check form-switch`, `.input-group` with icons, `.invalid-feedback` + `.is-invalid`. Style file inputs and date pickers to match.
7. **Icons.** One set: Bootstrap Icons (`bi-*`) unless the project uses another.
8. **React-Bootstrap.** Use `react-bootstrap` components (`<Offcanvas>`, `<Dropdown>`, `<Modal>`, `<Toast>`) instead of raw data attributes; keep one ThemeProvider/context that sets `data-bs-theme`.
9. **Charts.** Read colors with `getComputedStyle(document.documentElement).getPropertyValue('--bs-primary')` and re-render when the theme attribute changes.
10. **Layout.** Admin shell = fixed sidebar (`offcanvas-lg` on mobile) + sticky topbar + `container-fluid` content with `row g-3/g-4` card grids.

## Avoid

Mixing a second UI kit, raw hex colors in components, and overriding `.btn` with `!important`; extend with variant classes instead.

## Before you finish, check

- [ ] `data-bs-theme` set before paint; System mode works; choice persists.
- [ ] All colors come from `--bs-*` / semantic tokens.
- [ ] Selects, switches, file inputs and dropdowns are styled in both themes.
- [ ] Sidebar collapses to offcanvas on mobile.
