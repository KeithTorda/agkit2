---
name: ui-system-builder
description: Use this skill whenever designing, building, or refactoring any web UI, dashboard, admin panel, CRUD table, form, POS/storefront, printable invoice, or authentication screen across ANY UI stack (Tailwind CSS + shadcn/ui, React/Next.js, Laravel Blade, Vue/Svelte, Vanilla CSS, or Bootstrap) using Keith's first-party Component Type Catalog and Zero-Conflict Token System.
---

# UI System Builder — Stack-Agnostic Component & Token Skill

Kit root: `c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit`
- Component & Screen Type Catalog: `component-catalog/` (`00` through `07`)
- Portable Token & Theme Settings Engine: `ui-kit/keith-ui-tokens.css` + `ui-kit/keith-ui-settings.js`
- Automated Hygiene Guard: `python "c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit/scripts/audit_project_hygiene.py" <project_dir>`

## Workflow

1. **Choose or Match the Project UI Stack**
   - **Existing project:** Match its established stack (Tailwind/shadcn, React/Next.js, Blade, Vue, Vanilla CSS, or Bootstrap).
   - **New project:** Use the stack requested by the user (or modern Tailwind + semantic tokens / `ui-kit/keith-ui-tokens.css` when unspecified).

2. **Map Every Screen & Component Type Before Writing Markup**
   - Read [00-MASTER-SCREEN-AND-COMPONENT-TYPES.md](../../component-catalog/00-MASTER-SCREEN-AND-COMPONENT-TYPES.md) and the specific catalog guides needed (`01` tokens, `02` shells/sidebars/settings drawer, `03` cards/KPIs/charts, `04` tables/ledgers, `05` forms/wizards, `06` buttons/badges/modals, `07` auth/invoice/POS/errors).

3. **Enforce Zero-Conflict Token CSS**
   - Define colors, contrast, surfaces, and dark mode once in semantic CSS variables (`--ui-*` / `--on-*` / `--primary-ink` or Tailwind semantic tokens `bg-card`, `text-foreground`, `bg-primary`, `text-primary-foreground`).
   - Use `@layer tokens, base, components, utilities;` when writing custom CSS; scope custom classes to `.app-*` with **zero `!important` wars** and **zero raw `#hex` colors** outside token definitions.
   - **Include the Right-Side Theme Settings Drawer** (`ui-kit/keith-ui-settings.js` or `<ThemeSettingsDrawer />`) on admin dashboards and workspace shells using a single state store.

4. **Enforce Complete States, Accessibility & Zero Sample Data**
   - Never use hardcoded light-only classes (`bg-white text-black` / `text-dark bg-light`) that break Dark Mode, or `javascript:void(0)`.
   - Use `<button type="button">` for actions, `aria-label` on icon-only buttons, `<th scope="col">` on tables, `.tabular-nums` on numbers/amounts/dates, simple plain English words, zero sample data (`0` / `₱0.00` + `EmptyState`), and run `audit_project_hygiene.py` before finishing.
