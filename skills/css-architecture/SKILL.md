---
name: css-architecture
description: "How styles are organised so a change lands in one place — one token source, cascade layers, co-located component styles, the override ban as a method, naming, dead-CSS removal; the Tailwind v4 mapping and a plain CSS/SCSS mode for Laravel Blade. Use when adding, moving, or fixing CSS, creating a stylesheet, or when a fix would otherwise add an override."
version: 1.0.0
---

# CSS Architecture

> Every style has exactly one home. If you cannot say where a rule belongs, you are about to create an override.

Before writing a rule, name its home: a token (`@theme`), base, a shared component class, this component, or this page. No home means the rule patches a symptom — find the rule that owns the behaviour and change that one. The override ban is policy (`code-rules` "Fix at the source"); this file is the method.

## File structure (Tailwind v4 / Next.js)

```text
app/
  globals.css                  # @import "tailwindcss"; @theme; @layer base; @layer components — nothing else
  (dashboard)/invoices/
    page.tsx                   # page-specific rules stay in the page
components/
  invoice-table/
    invoice-table.tsx          # className on the element: the default home
    invoice-table.module.css   # only for what utilities cannot express
  app-shell/
    app-shell.tsx
```

- `globals.css` holds four things: `@import "tailwindcss"`, `@theme { tokens }` (values from `DESIGN.md`), `@layer base { resets, element defaults }`, `@layer components { the few real shared classes }`. Nothing else is global.
- Component styles live with the component: `className` first; a co-located `<component>.module.css` only for what Tailwind cannot express (complex keyframes, skinning a third-party widget).
- Page-specific rules live in the page file. A rule two pages need is a component or a token, not a page rule.
- Never create `overrides.css`, `fixes.css`, `custom.css`, `theme-overrides.css`. The file's existence is the smell: every rule in it has an owner that already exists.

## Cascade layers, not specificity wars

Tailwind v4 orders its layers `theme, base, components, utilities`. Put custom CSS in the layer that matches what it is; a later layer wins over an earlier one whatever the selector specificity.

- A utility beats a component class by layer order (`utilities` comes after `components`) — never by `!important`, never by a longer selector.
- Third-party CSS goes in its own layer, declared before `components`, so your rules win by order. Layer order is fixed by first mention, so declare it on line one:
  ```css
  @layer theme, base, vendor, components, utilities;
  @import "tailwindcss";
  @import "react-datepicker/dist/react-datepicker.css" layer(vendor);
  ```
- Unlayered CSS beats every layer. A custom rule outside `@layer` is the start of the next war.

## When a rule "does not take"

1. Find why it lost: layer order, a more specific selector, a later rule in the same layer, the wrong element (the child inherits from a parent you did not style), or a class the compiler never generated (a runtime string, a missing `@source`).
2. Fix that cause in the rule that owns the behaviour.
3. Delete the rule you were about to duplicate. One rule per behaviour.

`!important` has one allowed home: a Tailwind `!` utility (`w-full!` — v4 puts the mark at the end) on a third-party widget that ships unlayered CSS, with a comment naming the widget: `{/* react-datepicker sets inline widths */}`.

## Naming (the CSS half; files and exports are in `clean-code`)

- Classes are component-prefixed BEM: `.invoice-table`, `.invoice-table__row`, `.invoice-table--compact`. Global `.container .wrapper .card .header .content .box .item .row` are banned; they collide within a month.
- Custom properties: `--<component>-<property>` for component-local values (`--invoice-table-gap`); `--color-* --space-* --radius-* --shadow-* --font-* --motion-*` for tokens, and only tokens `DESIGN.md` defines.
- No raw hex or px in a component when a token exists. A value used twice is a missing token (`tailwind-patterns` §2).
- Check: `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/naming_check.py .`

## Dead CSS

- Replace a rule or a class: delete the old one in the same change, and grep the markup for the old class name before closing the task.
- Run the project's unused-CSS check when one exists (PurgeCSS, `knip`, a DevTools coverage pass); report what it removed.
- A stylesheet that only grows is unmaintained. Each change leaves it the same size or smaller.

## Plain CSS / SCSS mode (Laravel Blade, non-Tailwind)

One entry file (`resources/css/app.scss`) imports every partial once, in ITCSS order: settings (tokens) → tools (mixins) → generic (reset) → elements → objects (layout) → components → utilities. Each partial is `_<name>.scss`; each component is one file with its BEM prefix; no per-page override files. Full mode and the migration steps: [plain-css.md](./plain-css.md).

## Exemplar

```text
WRONG (apply and override)
  styles.css gets `.sidebar { width: 240px !important }` appended because the earlier
  `.sidebar { width: 240px }` "did not work". Two rules, one !important; the next
  width change edits the wrong one.

RIGHT (fix the one rule)
  The earlier rule lost to a later `.layout .sidebar { width: 200px }` in the layout
  file. Put the width in the sidebar component — `.app-sidebar { width: var(--app-sidebar-width) }`
  — delete the `.layout .sidebar` rule and the duplicate. One rule, no !important.
```

## Failure modes

- **Appending to `globals.css` because it is open** — the rule has an owner; put it there. Global is tokens, base, and shared components only.
- **A second token list** — values in `tailwind.config.js`, a `theme.ts`, or a components file beside `@theme`. One source; the others drift within a sprint.
- **Page-specific overrides of a shared component** — `.checkout .btn { }` is a variant in disguise; add `.btn--wide` or a `variant` prop to the component.
- **Inline `style=` for layout** — invisible to the theme, the layer order, and the next reader. Inline only for runtime values (`style={{ '--index': i }}`).
- **`!important` to beat a layer** — you found the layer order and fought it. Move the rule into the right layer.

## Boundaries

Tailwind mechanics and the `@theme` mapping → `tailwind-patterns`; fixing a broken layout → `ui-repair`; design token values → `design-spec`; file and export names → `clean-code`.

## Sub-files

| File | Read when |
|---|---|
| [plain-css.md](./plain-css.md) | The project is not Tailwind (Laravel Blade, legacy CSS/SCSS) |
