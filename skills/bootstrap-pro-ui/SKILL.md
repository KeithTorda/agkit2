---
name: bootstrap-pro-ui
description: Use this skill whenever designing, building, or refactoring any web dashboard, admin panel, CRUD table, form, POS/e-commerce view, printable invoice, or authentication page using the downloaded Bootstrap 5 Dashboard Template Pro component library.
---

# Bootstrap 5 Dashboard Pro — Zero-Conflict Reusable UI Assembly Skill

Kit root: `c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit`
- Catalog & copy-ready snippets: `component-catalog/` (`00` through `07` + `08-COMPACT-PURE-CONTRAST-OVERRIDE.css`)
- Full source files: `reference-template/bootstrap-5-dashboard-pro/`
- Automated Hygiene Guard: `python "c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit/scripts/audit_project_hygiene.py" <project_dir>`

## Workflow

1. **Map Every Screen Before Writing Markup**
   - Read [00-INDEX-AND-PAGE-MAP.md](../../component-catalog/00-INDEX-AND-PAGE-MAP.md) and only the specific catalog guides needed (`01`–`07`).

2. **Enforce the 3-Layer Zero-Conflict CSS Load Order**
   - **Layer 1 (`style.css`):** Copy untouched from `reference-template/bootstrap-5-dashboard-pro/css/style.css`. Never edit.
   - **Layer 2 (`08-COMPACT-PURE-CONTRAST-OVERRIDE.css`):** Copy untouched from `component-catalog/08-COMPACT-PURE-CONTRAST-OVERRIDE.css`. Never edit per project — it already handles `13px` scaling, pure `#000000`/`#ffffff` contrast, Dark Mode `color_1`, and WCAG AA `--on-*` / `--primary-ink` tokens for all 15 color presets.
   - **Layer 3 (`app.css`):** Optional project-specific stylesheet strictly scoped to `.app-*` classes using `var(--kit-*)` and `var(--primary)` tokens. **Zero `!important`, zero raw `#hex` colors, zero global tag or Bootstrap/Dompet selectors.**
   - **Mandatory Right-Side UI Kit Settings Panel:** Always load `js/demo.js` and `js/styleSwitcher.js` at the bottom of the app shell, and bind any header theme toggle to `demo.js`'s `version` cookie (`getCookie('version')` / `setCookie('version', ...)`).

3. **Sanitize Markup & Prevent Theme Conflicts**
   - **Never** use `text-dark`, `text-black`, `bg-white`, `bg-light`, or inline color `style="..."` in HTML/EJS/Blade/JSX — use `.kit-subtle-box`, `.kit-muted`, or `.badge.light.badge-*`.
   - Replace every `href="javascript:void(0);"` with `<button type="button">`, add `aria-label` on icon-only `.btn.sharp` buttons, `<th scope="col">` on table headers, and `.tabular-nums` on numbers/amounts/dates.
   - Strip all template placeholder text (`Dompet`, `DexignLab`, `Lorem ipsum`) and start **100% empty of sample data** (`0` / `₱0.00` + clean `EmptyState`) using simple everyday English words.

4. **Verify Zero Violations Before Finishing**
   - Run `python "c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit/scripts/audit_project_hygiene.py" <project_dir>` and resolve any CSS/markup flags before reporting completion.
