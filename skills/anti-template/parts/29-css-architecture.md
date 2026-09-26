---
part: 29
title: CSS Architecture
covers: file organisation, naming, BEM and prefixes, generic class names, specificity, nesting depth, tokens, utility vs component, duplication, dead CSS, global overrides, inline styles, media query placement, container queries, cascade layers, Tailwind config and @apply, Bootstrap Sass customisation, CSS resets, rule and property ordering, state classes, theming structure
---

# 29 — CSS Architecture

Read when: creating or restructuring stylesheets, adding a component's CSS, setting up Tailwind or Bootstrap config, reviewing a CSS diff, or cleaning a project that grew one giant stylesheet.

Guidance: DESIGN.md and the brief override this part.

This part covers how CSS is organised, named and layered. Individual banned declarations (glow shadows, `transition: all`, `z-index: 9999`, `100vh`) live in part 11. Colour values live in part 12. Type scale lives in part 13.

## 29.1 File organisation

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| One `style.css` or `styles.css` with 500+ lines covering every page | Agent appends to the end of one file each turn. Nobody can find a rule. | One file per component or page section. Split at about 200–300 lines. `components/thread-list.css`, `pages/checkout.css`. |
| `styles.css`, `style2.css`, `new-styles.css`, `custom.css`, `main-fixed.css` side by side | Each session added a file instead of editing the right one | One entry file that imports in a fixed order. Delete versioned duplicates after merging. |
| `global.css` holding 60% of all rules | Everything is "global" because the agent did not decide where it belongs | `global.css` holds reset, tokens, base element styles only. Component rules go in component files. |
| `custom.css` loaded after a framework to undo it | Override layer instead of configuring the framework | Configure the framework (Tailwind config, Bootstrap Sass variables). See 29.10 and 29.11. |
| Per-component CSS file that is 8 lines and only sets `margin-top` | Component explosion copied from a template | Keep tiny rules with the parent component. Create a file when the component has its own states or variants. |
| Folders named `css/`, `styles/`, `scss/`, `stylesheets/` all in one repo | Mixed templates pasted together | One styles root. Pick the name the framework expects and use it everywhere. |
| `components/Button/Button.module.css` plus `styles/button.css` plus Tailwind classes for the same button | Three systems styling one element | One source per component. If using CSS Modules, no global `.btn` rules for the same element. |
| Styles for one page scattered in 4 files | No ownership rule | A file owns a block. Rules for `.receipt-*` live only in `receipt.css`. |
| `animations.css` with 40 keyframes, 3 used | Library of effects pasted "in case" | Keyframes live next to the component that uses them. Delete unused keyframes. |
| `utilities.css` hand-written clone of Tailwind (`.mt-1` to `.mt-96`) in a non-Tailwind project | Rebuilding a framework by hand | Use a spacing token in component CSS, or adopt Tailwind properly. A handful of real utilities (`.visually-hidden`, `.stack`) is fine. |
| `print.css` absent on receipt, report or certificate pages | Agent never thinks of print | Add `@media print` rules in the page file for receipts, BIR invoices, barangay clearances, report cards. Hide nav, set black text, set page margins. |
| Vendor CSS copied into `src/` and edited | Upgrades now overwrite edits or are impossible | Import vendor CSS from `node_modules` or a pinned CDN URL. Put edits in your own file that loads after. |

Use a fixed import order in the entry file:

```css
/* Use */
@layer reset, tokens, base, layout, components, utilities, overrides;

@import "reset.css" layer(reset);
@import "tokens.css" layer(tokens);
@import "base.css" layer(base);
@import "layout.css" layer(layout);
@import "components/header.css" layer(components);
@import "components/thread-list.css" layer(components);
@import "components/receipt.css" layer(components);
@import "utilities.css" layer(utilities);
```

## 29.2 Naming and generic class names

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `.container`, `.wrapper`, `.inner`, `.content`, `.box`, `.section`, `.item`, `.title`, `.text`, `.card` as the only class | Template names with no owner. They collide the moment a second component appears. | Name by component and part: `.thread-list`, `.thread-list__item`, `.thread-list__title`. |
| `.container > .wrapper > .inner` triple around one block | Wrapper stacking from boilerplate | One element with the layout rule. See part 28 for the markup side. |
| `.hero-section`, `.features-section`, `.cta-section`, `.testimonials-section` | Names the landing template, not the content | Name what the block holds: `.fee-schedule`, `.precinct-finder`, `.office-hours`. |
| `.card-1`, `.card-2`, `.box-blue`, `.text-big`, `.red-button` | Names describe appearance or order. They lie after the first redesign. | Name the role: `.stat--overdue`, `.button--danger`, `.notice--urgent`. |
| `.new-header`, `.header-v2`, `.header-fixed`, `.old-nav` | History encoded in the class | Rename to the current role. Delete the old one. |
| `.flex-center`, `.mt-20`, `.w-50` hand-rolled in a non-utility project | Utility names mixed into component CSS | Put the layout rule in the component class. |
| Mixed conventions: `.threadList`, `.thread-list`, `.thread_list`, `.ThreadList` in one project | Different sessions, different habits | One convention. Kebab-case for classes. Write it in DESIGN.md or the styles README line. |
| BEM chain four deep: `.card__header__title__icon` | BEM misunderstood as DOM path | One element level: `.card__icon`. Elements belong to the block, not to each other. |
| Modifier without base: `<div class="button--primary">` | Modifier copied without the block | Always pair: `class="button button--primary"`. |
| `.is-active`, `.active`, `.selected`, `.current`, `.on` all meaning the same | No state naming rule | One set of state classes: `.is-active`, `.is-open`, `.is-disabled`, `.is-loading`, `.has-error`. Prefer ARIA attributes where one exists (see 29.13). |
| Classes named after the agent's task: `.fix-mobile`, `.temp-style`, `.test`, `.debug-border` | Leftover scaffolding | Delete or rename to the role. |
| No prefix in a widget embedded on third-party pages (LGU site plugin, chat widget) | Collides with host page `.button` | Prefix every class: `.bm-widget__button`. Or use Shadow DOM. |
| Prefix on everything in a single-app project: `.app-header`, `.app-button`, `.app-text` | Prefix copied from library docs with no need | Prefix only when styles ship into someone else's page. |
| JS selecting styling classes: `document.querySelector('.card__title')` | Renaming a class now breaks JS | JS hooks use `data-*` attributes or `id`. Styling classes stay for CSS. |
| Tagalog, English and abbreviations mixed in class names: `.btn-bayad`, `.payment-btn`, `.pymnt` | Inconsistent vocabulary | English class names. Filipino words stay in content, not selectors. Or pick one language and document it. |

```css
/* Banned */
.container .wrapper .card .title { font-size: 18px; }
.card-2 .text-big { color: #6366f1; }

/* Use */
.thread-card__title { font-size: var(--text-lg); }
.thread-card--pinned .thread-card__title { color: var(--color-primary); }
```

## 29.3 Specificity

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `!important` to win a fight | Each fix raises the stakes. Next change needs another `!important`. | Find the rule it is fighting. Lower that selector or reorder layers. `!important` only in `.visually-hidden` and user-preference overrides. Pattern details in part 11. |
| ID selectors for styling: `#main-header .nav a` | Specificity 1-1-1 beats every class rule. Overrides become impossible. | Class selectors only. IDs are for anchors, labels and JS hooks. |
| Qualified selectors: `div.card`, `ul.nav-list`, `button.btn` | Adds specificity and ties style to one tag | `.card`, `.nav-list`, `.button`. |
| Doubled class hack: `.button.button` | Specificity hack pasted from a forum answer | Use `@layer` order or fix the source rule. |
| Overrides by repeating a longer path: `body .page .main .card .title` | Arms race copied into every new rule | Keep selectors at 1–2 classes. Use modifiers for variants. |
| `:not()` chains to exclude cases: `.item:not(.first):not(.last):not(.active)` | Patching around missing modifiers | Add a modifier class or use `:first-child` / `:last-child` directly. |
| Styling by attribute strings: `[class*="col-"]`, `[class^="icon-"]` | Brittle substring matches | Target a real class. |
| Inline `style=""` to win specificity | Highest specificity outside `!important`, invisible in CSS review | Move to the stylesheet. Allow inline only for runtime values set by JS, and set a custom property: `style="--progress: 42%"`. |
| `:where()` and `:is()` used at random | Specificity becomes unpredictable to readers | Use `:where()` in reset and base layers to keep them at zero specificity. Avoid `:is()` in component selectors unless it removes real duplication. |
| Framework override file with 200 `!important` lines | Fighting Bootstrap or a UI kit instead of configuring it | Configure through variables. Load your layer after the vendor layer. |

```css
/* Banned */
#sidebar ul li a.active { color: #fff !important; }

/* Use */
@layer components {
  .sidebar__link[aria-current="page"] { color: var(--color-on-primary); }
}
```

## 29.4 Nesting depth

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Sass or native CSS nesting 5–8 levels deep mirroring the DOM | Output selectors are long and specific. Moving one element breaks styles. | Max 2 levels of nesting. Nest only pseudo-classes, pseudo-elements, modifiers and media queries. |
| `&__title { &__icon { &--active { ... } } }` producing `.card__title__icon--active` | Nesting abused to generate names | Write the full class name flat. Searching the codebase for it then works. |
| Nesting every element under `.page` or `body` | Global scope wrapper added "for safety" | Scope with the component class only. |
| `& > div > span` child chains | Coupled to exact markup | Give the element a class. |
| Nested media queries repeated inside every nested child | Duplicate breakpoints at 5 depths | One media block per component, or nest the query inside the single rule that changes. |
| Using nesting in plain CSS without checking target browsers | Older Android WebViews common in PH budget phones may lack support | Check support for your browserslist. Use PostCSS nesting or Sass if older WebViews matter. |

```scss
/* Banned */
.dashboard {
  .main {
    .stats {
      .card {
        .header {
          .title { font-weight: 700; }
        }
      }
    }
  }
}

/* Use */
.stat-card__title { font-weight: var(--weight-semibold); }
.stat-card {
  &:hover { background: var(--color-surface-alt); }
  &--warning { border-color: var(--color-warning); }
}
```

## 29.5 Tokens

Tokens are named values for things that repeat: colour, spacing, radius, type, shadow, z-index, duration. Values come from DESIGN.md.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hard-coded hex in 40 places: `color: #6366f1` | Changing the brand means find-and-replace | Define once in `tokens.css`: `--color-primary`. Reference `var(--color-primary)`. |
| A variable for every single value: `--header-title-margin-left-mobile: 13px` | Token system that holds one-off values is a second stylesheet | Tokens for values used 3+ times or part of the scale. One-offs stay literal in the component. |
| Tokens named after appearance: `--blue`, `--purple-500`, `--light-gray-2` used directly in components | Rebrand or dark mode forces edits everywhere | Two layers. Primitives: `--gray-100`. Semantic: `--color-surface: var(--gray-100)`. Components use semantic only. |
| Token names like `--primary-color`, `--color-primary`, `--primaryColor`, `--brand` all present | Four sessions, four conventions | One naming pattern: `--{category}-{role}-{variant}`. `--color-text-muted`, `--space-4`, `--radius-sm`. |
| Spacing tokens `--spacing-xs` to `--spacing-9xl` with 14 steps, 5 used | Pasted scale | Keep the steps the design uses. A 4px base scale with 8–10 steps covers most apps. |
| Spacing values off-scale: `margin: 13px`, `padding: 17px 22px` | Pixel nudging each turn | Snap to the spacing scale tokens. See part 14 for the scale itself. |
| `--shadow-glow`, `--gradient-hero`, `--blur-glass` in tokens | Tokens encode banned tropes and invite reuse | Delete. Tokens for shadow are `--shadow-sm`, `--shadow-md` with subtle values. See part 11. |
| Dark mode done by overriding 60 component rules | No semantic tokens to switch | Redefine semantic tokens under `[data-theme="dark"]` and `prefers-color-scheme`. Components do not change. |
| Tokens defined inside a component and reused elsewhere | Hidden dependency | Global tokens in `tokens.css`. Component-scoped custom properties (`--button-bg`) only read inside that component. |
| Z-index values 1, 10, 99, 999, 9999 scattered | No stacking plan | A z-index scale: `--z-dropdown: 100; --z-sticky: 200; --z-modal: 300; --z-toast: 400`. See part 11. |
| Duration values 150ms, 200ms, 0.3s, 300ms, 350ms mixed | Motion drift | `--duration-fast: 120ms; --duration-base: 200ms`. See part 25. |
| Breakpoints as custom properties used inside `@media` | Custom properties do not work in media query conditions | Sass variables, PostCSS custom media, or literal values with a comment naming the token in DESIGN.md. |
| Tokens duplicated in `tailwind.config.js`, `tokens.css` and a TS `theme.ts` | Three sources drift | One source. Generate the others, or have Tailwind read the CSS variables. |
| Fallback values that differ from the token: `var(--color-primary, #8b5cf6)` | Fallback is the AI default purple and shows when the token fails | No fallback, or fallback equal to the DESIGN.md value. |
| Tokens with numbers that mean nothing: `--size-17`, `--gray-450` | Scale invented on the fly | Use a documented scale. Add a step only after checking DESIGN.md. |

```css
/* Use: tokens.css */
:root {
  /* primitives: values from DESIGN.md */
  --gray-50: /* DESIGN.md */;
  --gray-900: /* DESIGN.md */;

  /* semantic */
  --color-bg: var(--gray-50);
  --color-surface: var(--white);
  --color-surface-alt: var(--gray-100);
  --color-text: var(--gray-900);
  --color-text-muted: var(--gray-600);
  --color-border: var(--gray-200);
  --color-primary: /* DESIGN.md */;
  --color-danger: /* DESIGN.md */;

  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;

  --radius-sm: 4px;   /* inputs */
  --radius-md: 8px;   /* cards, modals */
  --radius-pill: 9999px; /* pills, avatars, chips only */

  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.06);
  --shadow-md: 0 1px 3px rgb(0 0 0 / 0.1), 0 1px 2px rgb(0 0 0 / 0.06);
}

[data-theme="dark"] {
  --color-bg: var(--gray-950);
  --color-surface: var(--gray-900);
  --color-text: var(--gray-100);
  --color-border: var(--gray-800);
}
```

## 29.6 Utility vs component

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Utility classes for everything in a project that does not use Tailwind | Hand-written utility soup with no build purge | Component CSS with tokens. Keep a short utility list: `.visually-hidden`, `.stack`, `.cluster`, `.truncate`. |
| Tailwind project with a parallel `components.css` defining `.card`, `.btn` in plain CSS | Two systems for the same elements | Choose. Tailwind components live as framework components (partials, React components) that hold the class list. |
| Same 25-class Tailwind string pasted on 12 buttons | Copy-paste instead of a component | Extract a component (React, Blade, Twig partial, Astro component) that renders the button. One place to change. |
| Utilities and component classes on one element fighting: `class="card p-2"` where `.card` sets padding | Order of stylesheets decides the winner by accident | Put utilities in a later layer so they win on purpose, or do not mix on the same property. |
| Layout utilities inside a component's internals and component CSS on the page shell | Rules reversed | Component internals: component CSS or its own class list. Page placement (gap, grid position): utilities or layout classes on the parent. |
| Margin set by the component itself: `.card { margin-bottom: 24px; }` | Component cannot be reused in another context | Parent sets spacing: `.stack > * + * { margin-top: var(--space-4); }` or `gap`. |
| Component sets its own width: `.modal { width: 600px; }` fixed | Breaks on 360px phones | `width: min(100% - 2rem, 36rem)`. |

```css
/* Use: layout primitives instead of margins on components */
.stack { display: flex; flex-direction: column; gap: var(--stack-gap, var(--space-4)); }
.cluster { display: flex; flex-wrap: wrap; gap: var(--cluster-gap, var(--space-2)); align-items: center; }
```

## 29.7 Duplication and dead CSS

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Same rule block pasted for `.card`, `.panel`, `.box`, `.tile` | Four names for one thing | One component. Variants via modifiers. |
| Same value repeated 3+ times (colour, radius, shadow) | No token | Make it a token. |
| A new rule appended at the bottom instead of editing the existing one | Agent does not read the file first | Search for the selector before writing. Edit in place. |
| Two rules for the same selector in different files | Later one wins silently | One definition per selector. Grep before adding. |
| Unused classes from a template (`.testimonial-slider`, `.pricing-toggle`) shipped on an admin panel | Starter kit never trimmed | Delete classes with no match in templates. Run PurgeCSS or check coverage in DevTools. |
| Commented-out blocks of old CSS | Git already stores history | Delete. |
| Rules for elements removed from markup | Markup changed, CSS did not | When deleting markup, delete its CSS in the same change. |
| Declarations that repeat the default: `display: block` on a `div`, `font-weight: 400` on body text, `position: static` | Pasted boilerplate | Delete declarations equal to the default. |
| Same property twice in one rule: `padding: 16px; ... padding: 20px;` | Appended fix | Keep one. |
| Shorthand then longhand fight: `margin: 0 auto; margin-left: 12px;` without reason | Patch on patch | One declaration that states the intent. |
| Vendor prefixes for properties that no longer need them: `-webkit-border-radius`, `-moz-box-shadow` | Copied from 2012 snippets | Remove. Let Autoprefixer add what your browserslist needs. |
| Keyframes named `fadeIn`, `fade-in`, `fadein` all defined | Three turns, three names | One. Or none: see part 25. |
| Bootstrap and Tailwind both loaded | Two frameworks, one page | One framework. Remove the other and its classes. |
| Full Font Awesome CSS loaded for 4 icons | Dead weight | Inline SVG icons. See part 26 and part 34. |

## 29.8 Global overrides and inline styles

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `overrides.css` or `fixes.css` that grows every session | Bug fixes live far from the component | Fix the component file. If an override layer is needed for vendor CSS, keep it short and name what each block overrides. |
| Global element rules that restyle every instance: `button { background: #6366f1; border-radius: 24px; }` | Every button, including third-party widgets and date pickers, changes | Base layer sets only font inheritance and cursor. Styled buttons use `.button`. |
| `* { margin: 0; padding: 0; box-sizing: border-box; }` plus a second reset plus normalize | Stacked resets | One reset. See 29.12. |
| Global `a { text-decoration: none; }` | Removes link affordance everywhere | Keep underlines in body text. Remove only in nav and buttons by class. See part 13. |
| Global `img { width: 100%; }` | Stretches logos and icons | `img { max-width: 100%; height: auto; }`. |
| `html { overflow-x: hidden; }` to hide a layout bug | Masks the element that overflows | Find the overflowing element (`* { outline: 1px solid red }` locally) and fix it. See part 11. |
| `style="margin-top: 20px"` sprinkled in templates | Styling hidden from CSS review. Cannot respond to breakpoints. | Class in the stylesheet. |
| Inline styles for colour or theme: `style="color: #6366f1"` | Breaks dark mode and tokens | Use a modifier class tied to a token. |
| Inline style for runtime values (progress width, chart bar height) | This is the valid case | Set a custom property inline, style from CSS: `style="--value: 72%"` and `.meter__bar { width: var(--value); }`. |
| `<style>` blocks inside component templates on every page | Duplicate CSS per render, no caching | Move to the component stylesheet. Framework-scoped styles (Vue `<style scoped>`, Svelte) are fine. |
| Styles injected with JS `element.style.x = ...` for static appearance | Hard to find, fights CSS | Toggle a class or attribute. JS sets only values CSS cannot know. |

## 29.9 Media queries and responsive structure

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| One `responsive.css` at the end with every breakpoint for every component | Component logic split across files | Keep a component's breakpoints in its own file, next to the base rule. |
| Desktop-first rules undone with `max-width` queries | Most PH users are on phones. Undoing is more code. | Mobile-first base rules. Add `min-width` queries for larger screens. |
| Breakpoints at random values: 767px, 768px, 800px, 991px, 1000px, 1024px in one project | Pasted from different frameworks | A fixed set from DESIGN.md or the framework (e.g. 640, 768, 1024, 1280). Use the same values everywhere. |
| Device names in queries or comments: `/* iPhone 12 */` | Targets devices, not layout needs | Break where the content breaks. Name breakpoints by size: `sm`, `md`, `lg`. |
| Media query per property scattered across the file: 15 `@media (min-width: 768px)` blocks | Hard to see the tablet layout | Group per component, or nest the query inside the rule it changes. Not both styles in one project. |
| Viewport media queries for a component that sits in sidebars and main areas | Card breaks in a narrow column on a wide screen | Container queries: `container-type: inline-size` on the parent, `@container (min-width: 30rem)` in the component. |
| `max-width` and `min-width` queries overlapping at the same pixel (768 and 768) | Both apply at exactly 768px | Use range syntax `@media (width >= 768px)` or offset by 0.02px in the max query. |
| `@media screen and (-webkit-min-device-pixel-ratio: 2)` blocks for every image | Pasted retina hacks | `srcset` and `sizes` on the image. See part 26. |
| No `prefers-reduced-motion` or `prefers-color-scheme` blocks | Preferences ignored | A reduced-motion block in base CSS. Dark tokens under `prefers-color-scheme`. See part 25 and part 34. |

## 29.10 Tailwind configuration and @apply

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Default `tailwind.config` untouched, so `indigo-600`, `violet-500`, `slate-900` everywhere | Default palette is the AI look | Add brand colours from DESIGN.md as semantic names: `primary`, `surface`, `muted`. Remove or restrict default colours you do not want used. |
| Arbitrary values all over: `mt-[13px]`, `text-[#6366f1]`, `w-[347px]`, `rounded-[22px]` | Bypasses the scale | Add the value to the theme if it repeats. Otherwise use the nearest scale step. See part 11. |
| `@apply` used to rebuild every Tailwind class as a semantic class: `.btn { @apply px-4 py-2 rounded-lg bg-indigo-600 ... }` for 50 classes | Writing CSS with extra steps. Loses the point of utilities. | Extract framework components for repeated markup. Use `@apply` only for a few base styles you cannot reach with components (third-party HTML, Markdown content). |
| `@apply` with `hover:`, `md:` and `dark:` variants inside dozens of rules | Hard to read, order bugs | Plain CSS with tokens for those rules, or keep the utilities in the markup. |
| `safelist` with regex patterns covering everything: `{ pattern: /.*/ }` | Kills purge, ships megabytes | Safelist only dynamic class names you build at runtime. Better: map values to full class names in code. |
| Dynamic class names built by string: `` `bg-${color}-500` `` | Tailwind cannot see them, so they are purged, then safelisted | Use a lookup object with full class names: `{ danger: "bg-danger", ok: "bg-success" }`. |
| `content` paths missing folders, then classes "randomly" disappear | Config copied from another project | List every template path, including `.blade.php`, `.twig`, `.php`, `.vue`, `.svelte`, `.astro`. |
| Plugins installed and unused: `@tailwindcss/typography`, `forms`, `aspect-ratio`, `line-clamp` all added | Starter template | Keep plugins you use. `aspect-ratio` and `line-clamp` are core in current versions. |
| `theme` overwritten instead of `extend`, deleting the spacing scale | Config mistake that forces arbitrary values | Use `extend` unless you replace the whole scale on purpose. |
| `darkMode: "class"` configured, no toggle, no `dark:` classes | Copied config | Remove, or implement dark tokens. |
| `important: true` in config | Global `!important` to fight a legacy stylesheet | Scope with `important: "#app"` if you must coexist, and plan removal of the legacy CSS. |
| Tailwind v3 config syntax in a v4 project, or `@tailwind base` directives with v4 `@import "tailwindcss"` | Mixed version knowledge | Check the installed version. v4 uses `@import "tailwindcss"` and `@theme` in CSS. |
| Theme tokens in `@theme` and a separate `:root` block with the same values | Two sources | In v4, `@theme` variables are already CSS variables. Use them. |
| Class order random in long strings | Hard to review diffs | Use `prettier-plugin-tailwindcss` for automatic ordering. |
| 40-class strings with conflicting utilities: `p-4 p-6`, `text-sm text-base` | Appended fixes | Remove the loser. `tailwind-merge` only where props merge classes at runtime. |

```html
<!-- Banned -->
<button class="bg-gradient-to-r from-indigo-500 to-violet-500 px-[22px] py-[11px] rounded-[14px] text-[15px] shadow-2xl hover:scale-105">Pay</button>

<!-- Use: config maps DESIGN.md tokens to 'primary', component holds the classes -->
<button class="bg-primary text-on-primary px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-hover">Pay ₱1,250.00</button>
```

## 29.11 Bootstrap customisation

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Compiled `bootstrap.min.css` from CDN plus `custom.css` overriding `.btn-primary` with `!important` | Fighting the framework | Install Bootstrap Sass. Set variables before import: `$primary`, `$border-radius`, `$font-family-base`. |
| Overriding `.btn`, `.card`, `.navbar` by class after compile | Every component state needs its own override | Set `$btn-padding-y`, `$card-border-radius`, `$navbar-padding-y` variables. Bootstrap generates states. |
| Importing all of Bootstrap for grid and buttons | Ships 200+ KB of unused CSS | Import only needed partials: functions, variables, maps, mixins, root, reboot, grid, buttons, forms, utilities. |
| Default Bootstrap blue `#0d6efd` left as primary on a client site | Instantly recognisable template | `$primary` from DESIGN.md. Also set `$link-color`. |
| Bootstrap utility pileup: `d-flex justify-content-between align-items-center mb-3 mt-2 px-3 py-2 shadow-sm rounded-3 bg-white border` | Utility override hell on every element | Component class in Sass that uses Bootstrap mixins and variables. |
| Overriding CSS variables `--bs-*` inline on elements everywhere | Local patches | Set `--bs-*` values in one place, or set Sass variables before compile. |
| Mixing Bootstrap 4 and 5 class names: `ml-2` with `ms-2`, `float-right` with `float-end`, `data-toggle` with `data-bs-toggle` | Training data from both versions | Check the installed version. Use v5 names in v5. |
| jQuery loaded only for Bootstrap 5 | v5 does not need jQuery | Remove jQuery unless other code uses it. |
| Admin template (AdminLTE, SB Admin, CoreUI) used with its demo colour, fonts and sidebar untouched | Every LGU or school admin looks like the demo | Change theme variables, remove demo widgets, charts and pages you do not use. See part 22. |
| Custom Sass that redefines Bootstrap mixins with the same name | Silent override, breaks on upgrade | Name your mixins with a project prefix. |

```scss
// Banned: custom.css after CDN bootstrap
.btn-primary { background: #6366f1 !important; border-radius: 24px !important; }

// Use: _variables.scss, then import
$primary: /* from DESIGN.md */;
$border-radius: .5rem;
$btn-border-radius: .25rem;
$enable-shadows: false;
$enable-gradients: false;
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/maps";
@import "bootstrap/scss/mixins";
@import "bootstrap/scss/root";
@import "bootstrap/scss/reboot";
@import "bootstrap/scss/grid";
@import "bootstrap/scss/buttons";
@import "bootstrap/scss/forms";
@import "bootstrap/scss/utilities/api";
```

## 29.12 CSS resets

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Eric Meyer reset plus normalize.css plus a `*` reset in one project | Three resets pasted by three sessions | One reset. A short modern reset or the framework's (Tailwind preflight, Bootstrap reboot). Not both. |
| Custom reset added on top of Tailwind preflight | Preflight already resets | Delete the extra reset. |
| `* { outline: none; }` or `*:focus { outline: 0; }` in the reset | Removes keyboard focus for everyone | Never remove outlines globally. Style `:focus-visible` with a token. See part 27. |
| `* { user-select: none; }` | Users cannot copy reference numbers, OR numbers, tracking codes | Remove. Disable selection only on drag handles. |
| `html { scroll-behavior: smooth; }` in every reset | Forced motion, ignores preferences | Wrap in `@media (prefers-reduced-motion: no-preference)` or remove. See part 25. |
| `html { font-size: 62.5%; }` to make rem math easy | Breaks user font settings in some components, and every third-party widget renders small | Keep root at 100%. Use rem tokens. |
| `body { overflow-x: hidden; }` in the reset | Hides overflow bugs and breaks `position: sticky` | Remove. Fix the overflow. |
| `ul { list-style: none; }` globally | Lists in content lose bullets. Safari also drops list semantics. | Remove bullets only on nav and component lists by class. Add `role="list"` where Safari semantics matter. |
| `button { all: unset; }` | Removes focus styles and display behaviour | Reset only font, colour, background, border, padding on `.button` classes. |
| Reset copied with IE hacks: `*zoom: 1`, `filter: progid:...`, `-ms-` rules | 2012 snippet | Delete. |

```css
/* Use: a short base that respects users */
*, *::before, *::after { box-sizing: border-box; }
body { margin: 0; font-family: var(--font-body); line-height: 1.5; color: var(--color-text); background: var(--color-bg); }
img, svg, video { display: block; max-width: 100%; height: auto; }
input, button, textarea, select { font: inherit; }
:where(h1, h2, h3, h4, p) { margin-block: 0 var(--space-3); }
:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }
@media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth; } }
```

## 29.13 State, variants and JS hooks

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `.active` class toggled by JS when an ARIA state exists | Two sources of truth that drift | Style the ARIA state: `[aria-current="page"]`, `[aria-expanded="true"]`, `[aria-selected="true"]`, `[aria-invalid="true"]`, `:disabled`. |
| `.disabled` class on a button that is still clickable | Looks disabled, still submits | Use the `disabled` attribute or `aria-disabled="true"` plus a handler guard. Style `:disabled`. |
| `.hidden` class plus `display: none !important` plus `hidden` attribute | Three ways to hide | Use the `hidden` attribute. Style `[hidden] { display: none; }` once. |
| One variant class per combination: `.button-primary-large-outline-disabled` | Combinatorial explosion | Orthogonal modifiers: `.button--primary .button--lg`. |
| Variants that repeat all base properties | Copy of the base rule with one change | Variant sets only what differs. Better: variant changes component custom properties. |
| Status colours by class name per status in 5 components: `.badge-paid`, `.row-paid`, `.chip-paid` | Status meaning copied everywhere | One status mapping: `[data-status="paid"] { --status-color: var(--color-success); }`. Components read `--status-color`. |
| Theme classes on `body` (`.theme-purple`, `.theme-ocean`, `.theme-sunset`) for 6 themes | Theme picker nobody asked for | Light and dark only, via tokens. See part 34. |

```css
/* Use: component custom properties for variants */
.button {
  --button-bg: var(--color-surface);
  --button-fg: var(--color-text);
  background: var(--button-bg);
  color: var(--button-fg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: var(--space-2) var(--space-4);
}
.button--primary { --button-bg: var(--color-primary); --button-fg: var(--color-on-primary); border-color: transparent; }
.button--danger  { --button-bg: var(--color-danger);  --button-fg: var(--color-on-danger);  border-color: transparent; }
.button:disabled { opacity: 0.5; cursor: not-allowed; }
```

## 29.14 Rule and property ordering

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Rules in the order the agent wrote them: footer, then button, then header, then button hover 300 lines later | Append-only file | Order in the file: block, elements, modifiers, states, media queries. |
| `:hover` defined before base, `:focus` missing, `:active` after media queries | State order bugs | Base, `:hover`, `:focus-visible`, `:active`, `:disabled`, then modifiers. |
| Properties in random order in each rule | Slow to scan | Pick one order and enforce it with Stylelint (`stylelint-order`): position, display and box model, typography, visual, misc. Or alphabetical. Pick one. |
| Layers undeclared, so import order decides everything | Moving an import changes the design | Declare `@layer` order once at the top of the entry file. |
| Third-party CSS loaded after component CSS | Vendor rules win | Load vendor CSS in an earlier layer: `@import url("vendor.css") layer(vendor);`. |
| No linter on a project with 3,000+ lines of CSS | Drift goes unnoticed | Add Stylelint with `stylelint-config-standard`. Add rules: `declaration-no-important`, `selector-max-id: 0`, `selector-max-compound-selectors: 3`, `color-no-hex` in component files, `max-nesting-depth: 2`. |

## 29.15 Scoping by stack

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| CSS Modules plus global class names inside the module (`:global(.card)`) everywhere | Scoping turned off by habit | Use local names. `:global` only for third-party markup. |
| Vue `<style>` without `scoped` in every component | Every component leaks global styles | `<style scoped>` or CSS Modules in Vue. |
| `::v-deep` / `:deep()` in most components | Reaching into children breaks encapsulation | Pass a class or custom property to the child. |
| CSS-in-JS (styled-components, Emotion) with runtime styles in a Next.js App Router project | Runtime cost and server component issues | CSS Modules, Tailwind, or zero-runtime options. Keep one approach. |
| styled-components with a `theme` object that duplicates CSS variables | Two token systems | Theme object references CSS variables, or drop the theme object. |
| Laravel Blade or PHP templates with `<style>` in each view | No caching, no reuse | Vite or Mix entry with component files. Include page CSS through the layout. |
| WordPress theme with styles in `functions.php` via `wp_add_inline_style` for large blocks | Hidden from editors and caches | Enqueue a stylesheet file. Use `theme.json` for tokens in block themes. |

## 29.16 Philippines project specifics

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| LGU or school site with a separate stylesheet per office page (`mayor.css`, `treasury.css`) that copy each other | Pages made one by one | Shared components (`.office-card`, `.notice`, `.fee-table`). Page files only for layout differences. |
| Print styles missing on barangay clearance, cedula request, report card, BIR-compliant receipt pages | These pages get printed on A4, Letter, Long (8.5x13) and 58/80mm thermal paper | `@page { size: A4; margin: 12mm; }` or the paper size the office uses. Separate `receipt-80mm.css` for POS thermal printers with `@page { size: 80mm auto; margin: 0; }`. |
| POS screen CSS written for a 1440px monitor only | POS runs on 1024x768 terminals and tablets | Layout tokens and container queries tested at 1024x768 and 800x1280. |
| Styles depending on a web font from Google Fonts with no fallback stack | Slow 3G and offline POS fall back to Times | Fallback stack in the token: `--font-body: "Chosen Font", system-ui, sans-serif;`. See part 13. |
| Election or precinct finder with heavy CSS framework for one search box | Traffic spikes on election day on mobile data | Small hand-written CSS or a trimmed framework build. Target under 30 KB CSS for single-purpose pages. |

## 29.17 Check

- [ ] Stylesheets split by component or page section. No file over about 300 lines without a reason.
- [ ] One entry file with a declared `@layer` order.
- [ ] No `style2.css`, `new.css`, `custom-fixed.css` or other versioned duplicates.
- [ ] Only one styling system per element (not Tailwind plus Bootstrap plus custom `.btn`).
- [ ] No generic class names used alone: `.container`, `.wrapper`, `.card`, `.title`, `.item`, `.box`.
- [ ] Class names describe role, not colour, size or order.
- [ ] One naming convention across the project. BEM elements one level deep.
- [ ] Modifiers always paired with their base class.
- [ ] No ID selectors in CSS.
- [ ] No qualified selectors like `div.card`.
- [ ] Selectors at most 3 compound parts. Nesting at most 2 levels.
- [ ] No `!important` outside `.visually-hidden` and preference overrides.
- [ ] Every repeated colour, spacing, radius, shadow, duration and z-index comes from a token.
- [ ] Tokens have a primitive and a semantic layer. Components use semantic tokens only.
- [ ] Token values come from DESIGN.md. No AI default purple in fallbacks.
- [ ] No tokens for banned tropes (glow, glass, hero gradient).
- [ ] Tokens defined in one source, not duplicated across CSS, Tailwind config and TS.
- [ ] Dark mode switches tokens, not component rules.
- [ ] Components do not set their own outer margin. Parents set spacing with `gap` or stack rules.
- [ ] No duplicated rule blocks under different names.
- [ ] No commented-out CSS. No rules for deleted markup.
- [ ] No obsolete vendor prefixes. Autoprefixer handles prefixes.
- [ ] No global overrides file that keeps growing.
- [ ] No global restyling of `button`, `a`, `img` beyond base resets.
- [ ] No inline `style=""` except custom properties for runtime values.
- [ ] Media queries live with their component, mobile-first, from one breakpoint set.
- [ ] Container queries for components that appear in columns of different widths.
- [ ] Tailwind config holds brand tokens. Default indigo/violet not used.
- [ ] No arbitrary Tailwind values that repeat. `@apply` limited to a few base cases.
- [ ] No dynamic Tailwind class strings built by interpolation.
- [ ] Bootstrap customised through Sass variables, only needed partials imported.
- [ ] Bootstrap version-correct classes and attributes (v5: `ms-*`, `data-bs-*`).
- [ ] Exactly one reset. No global outline removal, no `user-select: none`, no `font-size: 62.5%`.
- [ ] States styled through ARIA attributes and native pseudo-classes where they exist.
- [ ] JS hooks use `data-*` attributes, not styling classes.
- [ ] Rules ordered: base, elements, modifiers, states, media queries.
- [ ] Stylelint configured with limits on IDs, nesting, `!important`.
- [ ] Print styles exist for receipts, clearances, certificates and reports.
