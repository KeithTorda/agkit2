---
name: tailwind-patterns
description: Tailwind CSS v4 mechanics - CSS-first configuration with @theme tokens, the @custom-variant dark setup, container queries, responsive and layout utilities, component extraction, and v3-to-v4 differences. Use when writing or reviewing Tailwind v4 code, wiring DESIGN.md tokens into @theme, setting up dark mode, or migrating a v3 config. Visual decisions live in frontend-design; this skill covers how Tailwind expresses them.
version: 2.0.0
---

# Tailwind CSS v4 Patterns

Tailwind v4 is CSS-first: configuration lives in the CSS entry file, tokens are CSS variables, the config file is optional. Design decisions (fonts, palette, radius) come from `DESIGN.md` (see `design-spec`); this file covers the mechanics.

## 1. Setup and entry file

```css
@import "tailwindcss";
@import "./theme.css";                      /* @theme block generated from DESIGN.md */
@plugin "@tailwindcss/typography";           /* plugins still exist; declared in CSS */
@custom-variant dark (&:where(.dark, .dark *));
@source "../node_modules/some-ui-lib";       /* extra content paths when auto-detection misses them */
```

- PostCSS: `@tailwindcss/postcss` in `postcss.config.mjs` (the old `tailwindcss` PostCSS plugin no longer works). Vite: `@tailwindcss/vite`. Both drive the same engine; PostCSS is not deprecated.
- `tailwind.config.js` is optional. Keep one only for a legacy plugin that needs it, loaded with `@config "./tailwind.config.js"`; do not split tokens between CSS and JS.
- Content detection is automatic; `@source` adds paths, `@source not` excludes them.

## 2. Tokens with `@theme`

```css
@theme {
  --color-primary: #1a1c1e;        /* colors.*          → bg-primary, text-primary, border-primary */
  --color-surface: #fbfaf7;
  --color-surface-dark: #131316;   /* DESIGN.md -dark counterpart, applied in §3 */
  --font-body-md: "Public Sans";   /* typography.*      → font-body-md */
  --text-headline-lg: 48px;        /* fontSize          → text-headline-lg */
  --radius-md: 8px;                /* rounded.*         → rounded-md */
  --spacing-md: 16px;              /* spacing.*         → p-md, gap-md */
  --breakpoint-3xl: 1920px;        /* adds 3xl: */
}
```

- Namespaces decide the utilities: `--color-*`, `--font-*`, `--text-*`, `--font-weight-*`, `--tracking-*`, `--leading-*`, `--radius-*`, `--shadow-*`, `--spacing-*`, `--breakpoint-*`, `--container-*`, `--animate-*`, `--ease-*`.
- Font family is whatever `DESIGN.md` specifies; do not hardcode a house font here.
- Reset a default scale before replacing it: `--color-*: initial;` then your own colors.
- `@theme inline` for values that reference other variables (`--color-brand: var(--brand)`); `@theme static` to emit every variable even when unused.
- OKLCH (`oklch(0.7 0.15 250)`) for hand-tuned palettes; `DESIGN.md` hex values are exported as-is, which is fine.
- Utilities compile to `var(--color-primary)`, so overriding a variable later in the cascade (`.dark`, a theme class) changes every utility that uses it.

**The round-trip, wrong vs right.** With each `DESIGN.md` token mapped once, components name it instead of re-typing the value:

```tsx
// v3 habit: tokens in JS config, arbitrary values in markup — hex drifts, no dark swap, invisible to the theme
<button className="bg-[#1a1c1e] text-[#fbfaf7] rounded-[8px] px-[16px]">Save</button>

// v4: DESIGN.md token → @theme (above) → semantic utility; overriding the variable once reskins every use
<button className="bg-primary text-surface rounded-md px-md">Save</button>
```

Reach for an arbitrary value (`p-[13px]`) only for a genuine one-off; a value used twice is a missing token — add it to `@theme`.

## 3. Dark mode

Default behaviour without any setup: `dark:` follows `prefers-color-scheme`. For a class-driven scheme (toggle, per-page lock), declare the variant once:

```css
@custom-variant dark (&:where(.dark, .dark *));
.dark { --color-surface: var(--color-surface-dark); --color-on-surface: var(--color-on-surface-dark); }
```

- Put `.dark` on `<html>`; set it from `prefers-color-scheme` on load and from the toggle afterwards.
- Swap semantic token values under `.dark` (above) and write components once (`bg-surface text-on-surface`); use `dark:` utilities only for one-off exceptions. One mechanism per project.
- A `data-theme` attribute works the same way: `@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));`.
- Which schemes ship (light, dark, both) is decided by `DESIGN.md` `colorScheme`, not here.

## 4. Responsive, container queries, layout

- Mobile-first: unprefixed = base, `sm 640 / md 768 / lg 1024 / xl 1280 / 2xl 1536`. Ranges: `md:max-lg:hidden`.
- Container queries are built in: `@container` on the parent, `@sm:` / `@md:` / `@lg:` on children, `@container/card` + `@md/card:` for named containers, `@max-md:` for max-width queries. Use viewport breakpoints for page layout, container queries for components that must work in any column.
- Grid: `grid-cols-[repeat(auto-fit,minmax(16rem,1fr))]` for fluid card grids, `grid-cols-[2fr_1fr]` / `col-span-*` for asymmetric and bento layouts, `grid-cols-[auto_1fr]` for sidebars, `grid gap-px bg-border` for hairline-divided cells. Grid over percentage flex math; flex for one-axis rows and stacks.
- Full-height sections: `min-h-dvh` (v4 ships `dvh` / `svh` / `lvh` utilities), never `h-screen`.

## 5. v4 utility changes worth knowing

- Renames: `shadow-sm` → `shadow-xs`, `shadow` → `shadow-sm`, `rounded-sm` → `rounded-xs`, `rounded` → `rounded-sm`, `outline-none` → `outline-hidden`, `ring` is 1px (`ring-3` for the old look), `bg-opacity-*` → `bg-black/50`.
- Variants stack left to right; `hover:` applies only on hover-capable devices. New: `not-*`, `starting:` (`@starting-style` entry transitions), `inert:`, `in-*`, `nth-*`, arbitrary variants `[&>*]:p-4`.
- New utilities: 3D transforms (`rotate-x-*`, `perspective-*`), gradient angles and interpolation (`bg-linear-45`, `bg-linear-to-r/oklch`), `field-sizing-content`, `text-balance` / `text-pretty`.
- `@keyframes` inside `@theme` register `animate-*` utilities; `motion-safe:` / `motion-reduce:` gate them.

## 6. Component extraction

- Same class combination 3+ times, complex state variants, or a design-system atom → extract a component (React / Vue), not a CSS class.
- `@apply` still works and is the last resort (framework-less projects, third-party markup you cannot template). `@utility` defines a real utility with variant support: `@utility scrollbar-hidden { scrollbar-width: none; }`.
- Class lists: merge conditionally with `cn()` / `clsx`; never build class names at runtime (`bg-${color}-500` is invisible to the compiler; map to full class names). `cva` / `tailwind-variants` for size and intent props.

## 7. Migrating from v3

`npx @tailwindcss/upgrade` handles most of it (config → `@theme`, renamed utilities, `@tailwind base/components/utilities` → `@import "tailwindcss"`, PostCSS plugin swap). Then replace the old `darkMode` config key with `@custom-variant dark`, and check `border-*` defaults (now `currentColor`) and `ring` widths. Never mix a v3 config token set with `@theme`.

## 8. Anti-patterns

| Avoid | Do instead |
|---|---|
| Arbitrary values everywhere (`p-[13px]`) | The `@theme` scale; add a token if one is missing |
| `!important` / `!` modifiers | Fix the layer order; the one allowed case (a `!` utility on a third-party widget) is in `css-architecture` |
| Inline `style=` for static values | Utilities; inline only for runtime values (`style={{ '--index': i }}`) |
| Two token sources (JS config + `@theme`) | `@theme` only, generated from `DESIGN.md` |
| `h-screen` heroes | `min-h-dvh` |

## Organisation

Where CSS lives is decided by `css-architecture`, not here: what `globals.css` may contain, co-located component files, custom CSS in the right `@layer` (a `vendor` layer for third-party CSS) instead of `!important`, BEM class and custom-property naming, and deleting the rule you replace. This file covers how Tailwind expresses a style; that one covers where it goes.
