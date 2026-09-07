# Plain CSS / SCSS mode

Read when the project is not Tailwind: Laravel Blade, a legacy CSS or SCSS codebase, a static site. Everything in `SKILL.md` still holds (one home per style, layers over specificity, no override files); this file gives the file order, the naming, and the migration.

## Entry file order (ITCSS)

One entry file imports every partial once, lowest specificity first. No other file imports CSS.

```scss
// resources/css/app.scss — the only file that imports
@use "settings/tokens";            // 1 settings: custom properties only, no selectors
@use "tools/mixins";               // 2 tools: mixins and functions, no output
@use "generic/reset";              // 3 generic: reset, box-sizing, base font
@use "elements/typography";        // 4 elements: bare h1, p, a, table — no classes
@use "elements/forms";
@use "objects/layout";             // 5 objects: .o-stack, .o-grid, .o-container — layout only
@use "components/invoice-table";   // 6 components: one file per block, BEM
@use "components/app-sidebar";
@use "components/order-form";
@use "utilities/spacing";          // 7 utilities: single-purpose .u-*, last so they win
@use "utilities/visibility";
```

Partials are `_<name>.scss` inside their layer folder: `settings/_tokens.scss`, `components/_invoice-table.scss`. One component per file, named after its block. Adding a partial means adding one `@use` line in order; a partial imported twice or out of order is a bug.

## BEM

Block = the component, element = a part of it (`__`), modifier = a variant or state (`--`). The block name is the file name.

| Rule | Example |
|---|---|
| Block is a component name; two words when one word is generic | `.invoice-table`, `.app-sidebar` — not `.table`, `.sidebar` |
| Element belongs to its block, never nested twice | `.invoice-table__row`, `.invoice-table__total` — not `.invoice-table__row__cell` |
| Modifier changes one thing and sits beside the block or element class | `.invoice-table--compact`, `.invoice-table__row--overdue` |
| JS state is a modifier or `is-*` on the block only | `.order-form--submitting` or `.order-form.is-submitting` |
| Space between components is an object, not a component rule | `.o-stack > * + * { margin-top: var(--space-md) }` — never `.invoice-table { margin-top }` |
| A component never styles another component's elements | `.app-sidebar .invoice-table__row` is banned; add a modifier to `invoice-table` |

Selectors stay flat: one class, at most one combinator. Specificity is (0,1,0) almost everywhere, so order decides and the layers stay meaningful.

## Cascade layers in plain CSS

Declare the order once, on the first line of the entry file, and wrap every partial's rules in its layer:

```css
@layer settings, base, layout, components, utilities;

@layer base { *, *::before, *::after { box-sizing: border-box; } body { margin: 0; font: var(--font-body); } }
@layer components { .invoice-table { display: grid; gap: var(--invoice-table-gap, var(--space-sm)); } }
@layer utilities { .u-hidden { display: none; } }
```

With SCSS, each partial wraps its own body in `@layer components { ... }` (Sass emits it where the `@use` sits; `@use` itself cannot be nested in a layer). Third-party CSS goes into `@layer vendor`, declared before `components`. Unlayered rules beat every layer — a rule outside `@layer` is the next override.

## Migrating an override-heavy stylesheet

1. **Inventory** — list every selector with file and line (`grep -n "{" resources/css`), count `!important` and duplicate selectors (`python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/naming_check.py .`). Screenshot the affected routes at 390 / 768 / 1440 through `/see`.
2. **Group by component** — assign each rule to a block (`invoice-table`, `app-sidebar`), an object, a token, or "dead". A rule with no owner is dead or belongs to a page-level object.
3. **Move into layers** — create one partial per block with the BEM names; move the rules in, replacing raw values with tokens; wrap each partial in its `@layer`.
4. **Delete duplicates** — where two rules set the same property on the same block, keep the one the markup needs and delete the other; remove every `!important` (order makes it unnecessary); delete the override files.
5. **Verify with `/see`** — the same routes at the same widths, compared with the step-1 screenshots; the unused-CSS check; `naming_check.py` reports zero duplicate classes.

## Laravel notes

- Vite entry: `resources/css/app.css` (or `app.scss` with `sass` installed) is the only stylesheet in the `vite.config.js` `input` list; Blade layouts load it with `@vite(['resources/css/app.css', 'resources/js/app.js'])`.
- Blade components map to BEM blocks: `<x-invoice-table>` is `resources/views/components/invoice-table.blade.php` plus `resources/css/components/_invoice-table.scss`, block `.invoice-table`. Props map to modifiers (`compact` → `.invoice-table--compact`).
- Page views (`resources/views/invoices/index.blade.php`) hold no `<style>` blocks and no `@push('styles')`; a page-only rule is an object or a modifier.
- Tokens: `resources/css/settings/_tokens.scss` holds `:root { --color-*; --space-*; --radius-*; ... }` from `DESIGN.md`. No `$scss-variables` for values the browser should own at runtime (theme swaps, dark mode).
