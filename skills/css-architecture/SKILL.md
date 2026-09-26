---
name: css-architecture
description: "How styles are organised so a change lands in one place: one token source, cascade layers, co-located component styles, fixing the owning rule instead of overriding it, naming, dead-CSS removal; Tailwind v4 and a plain CSS/SCSS mode for Laravel Blade. Use when adding, moving or fixing CSS, creating a stylesheet, or when a fix is about to become an override."
version: 2.5.0
---

# CSS Architecture

> Every style has exactly one home. If you cannot say where a rule belongs, you are about to create an override.

Before writing a rule, name its home: a token (`@theme`), base, a shared component class, this component, or this page. No home usually means the rule patches a symptom: find the rule that owns the behaviour and change that one. The policy is `code-rules` "Fix at the source"; this file is the method. The project's existing structure wins over this layout; follow it and improve it where you touch it.

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
- Avoid creating `overrides.css`, `fixes.css`, `custom.css`, `theme-overrides.css`. Such a file tends to grow into a second source of truth: nearly every rule in it has an owner that already exists. If the project already has one, move rules out of it as you touch them.

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

`!important` is a last resort, not a crime. The usual legitimate case: a third-party widget that ships unlayered CSS or sets inline styles you cannot configure. Use the narrowest form (a Tailwind v4 `!` utility such as `w-full!`, or one declaration on one selector) with a comment naming the source: `{/* react-datepicker sets inline widths */}`. Utilities meant to always win (`.u-hidden`) are the other accepted use.

## Naming (the CSS half; files and exports are in `clean-code`)

- Follow the project's naming. In new plain-CSS code, prefer component-prefixed BEM: `.invoice-table`, `.invoice-table__row`, `.invoice-table--compact`. Bare global names (`.container .wrapper .card .header .content .box .item .row`) tend to collide; avoid adding new ones (framework classes such as Bootstrap's `.container` are fine).
- Custom properties: `--<component>-<property>` for component-local values (`--invoice-table-gap`); `--color-* --space-* --radius-* --shadow-* --font-* --motion-*` for tokens, and only tokens `DESIGN.md` defines.
- No raw hex or px in a component when a token exists. A value used twice is a missing token (`tailwind-patterns` §2).
- Check (advisory; `--strict` to fail): `python "KIT/scripts/naming_check.py" .`

## Dead CSS

- Replace a rule or a class: delete the old one in the same change, and grep the markup for the old class name before closing the task.
- Run the project's unused-CSS check when one exists (PurgeCSS, `knip`, a DevTools coverage pass); report what it removed.
- A stylesheet that only grows is unmaintained. Aim for each fix to leave it the same size or smaller.

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
- **`!important` to beat a layer**: you found the layer order and fought it. Move the rule into the right layer; keep `!important` for sources you cannot change, with a comment.

## Boundaries

Tailwind mechanics and the `@theme` mapping → `tailwind-patterns`; fixing a broken layout → `ui-repair`; design token values → `design-spec`; file and export names → `clean-code`.

## Sub-files

| File | Read when |
|---|---|
| [plain-css.md](./plain-css.md) | The project is not Tailwind (Laravel Blade, legacy CSS/SCSS) |

## Check it before you look at it

The browser shows you that text is the wrong colour. This shows you *why*, with `file:line`,
before you render anything:

```bash
python "KIT/scripts/css_audit.py" .            # advisory report
python "KIT/scripts/css_audit.py" . --strict   # exit 1 on errors (uncommented !important counts), as a gate
```

It reads every `.css`/`.scss` plus `<style>` blocks and `style=""` attributes, and reports:

- **token-collision** — one custom property defined more than once with different values outside a
  theme selector. Whichever file loads last silently wins, so the colour changes with import order.
  This is the single most common cause of "the text colour keeps changing". One token, one definition;
  a theme (`.dark`, `[data-theme]`, `@media (prefers-color-scheme)`) is the only legitimate redefinition.
- **undefined-var** — `var(--x)` where nothing defines `--x` and there is no fallback. The
  declaration is dropped and the element inherits, which is how text becomes invisible.
- **contrast** — a rule setting both `color` and a background below 4.5:1 (3:1 counts as an error).
  Values resolve through `var()` when the token has one unambiguous definition.
- **important** — `!important` on a colour: check whether the owning rule should change instead; fine with a comment when the source is third-party.
- **inline-style** / **cross-file-override** — a colour set in a `style=""` attribute, or the same
  property on the same selector in more than one file. Both decide the rendered colour by load order
  rather than by ownership.

Useful before `/see`: a render tells you something is wrong, this tells you which line. It sees declared pairs only; colours over images or translucent layers need the rendered check.
