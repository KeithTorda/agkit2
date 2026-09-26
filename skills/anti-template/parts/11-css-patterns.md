---
part: 11
title: CSS Patterns
covers: box-shadow, border-radius, gradients, border-image, animated backgrounds, backdrop-filter, filter, text-shadow, blend modes, transforms on hover, transition all, will-change, 100vh and 100vw, fixed heights, overflow hidden, absolute layouts, magic numbers, z-index, !important, inline styles, vendor prefixes, px vs rem, clamp, focus and outline, cursor, user-select, scrollbar and selection styling, CSS custom properties misuse, Tailwind class soup, arbitrary values, Bootstrap overrides, replacement token block
---

# 11 — CSS Patterns

Read when: writing or reviewing any CSS, Tailwind classes, Bootstrap markup or inline styles. Part 10 names the visual tropes; this part names the code that produces them and the code to write instead. File structure and naming live in part 29. Colour values live in part 12.

Guidance: DESIGN.md and the brief override this part.

All replacement values are tokens defined in DESIGN.md. Where this part shows a neutral default (for example a shadow in `rgba(0,0,0,…)`), it is a fallback for a missing token, not a brand colour.

## 11.1 The banned list from v3.0.0

These lines were in the original rulebook. They stay banned.

```css
/* Banned: glow shadows */
box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
box-shadow: inset 0 0 30px rgba(59, 130, 246, 0.2);

/* Banned: gradient text */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;

/* Banned: glassmorphism */
background: rgba(255, 255, 255, 0.05);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.1);

/* Banned: bubbly radius on data, and blobs */
.thread-list { border-radius: 24px; }
.blob { position: absolute; border-radius: 50%; filter: blur(80px); }

/* Banned: rainbow border */
border-image: linear-gradient(to right, #f00, #0f0, #00f) 1;

/* Banned: hover transforms on cards and rows */
.card:hover { transform: scale(1.05); }
.row:hover  { transform: translateY(-4px); }

/* Banned: gradient buttons */
.btn { background: linear-gradient(135deg, #6366f1, #8b5cf6); }

/* Banned: frosted nav */
nav { backdrop-filter: blur(12px); background: rgba(0, 0, 0, 0.5); }

/* Banned: glow text */
text-shadow: 0 0 10px rgba(99, 102, 241, 0.5);

/* Banned: animated gradient background */
background-size: 400% 400%;
animation: gradient-shift 15s ease infinite;
```

Decorative underline animations on every nav link are also banned. One or two animated underlines on a marketing page are fine; nav links get a plain underline or active state.

## 11.2 Shadows

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `box-shadow: 0 0 20px <colour>` (zero offset, big blur, coloured) | Glow. Means nothing | `box-shadow: var(--shadow-1)` or none |
| `box-shadow: 0 25px 50px -12px rgba(0,0,0,.25)` on cards (Tailwind `shadow-2xl`) | Heavy float on static content | `var(--shadow-1)` on cards if DESIGN.md wants shadows; otherwise a 1px border |
| Two to four stacked shadows on one element for "depth" | Copy-paste from shadow generators | One or two layers, defined once as tokens |
| Coloured shadow under a coloured button | Tailwind `shadow-indigo-500/50` look | Neutral shadow or none on buttons |
| Shadow + border + background tint on the same card | Three ways to say "container" | Pick one: border or shadow |
| Shadow on table rows, list items, table wrappers | Elevation on content that sits on the page | No shadow. Dividers between rows |
| Shadow growing on hover (`shadow-md` → `shadow-xl`) | Lift effect | Background change on hover |
| `inset` shadows to fake depth on inputs | Neumorphic | 1px border; border colour change on focus |
| Arbitrary shadows scattered in files (`0 3px 7px rgba(0,0,0,.13)`) | Magic values, no scale | Shadow scale of 2–3 tokens: `--shadow-1` (cards, optional), `--shadow-2` (menus, popovers), `--shadow-3` (dialogs) |
| `filter: drop-shadow()` on text or icons | Blurry glyphs | None |

## 11.3 Border radius

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `border-radius: 24px` (or `rounded-3xl`) on cards, tables, inputs | Bubbly toy look | `var(--radius-card)`; common values 6–8px |
| `rounded-full` on primary buttons in a data app | Consumer-app style in admin tools | `var(--radius-control)`; common 4–6px. Full pill only if DESIGN.md chooses it |
| Different radius on every component (4, 6, 8, 10, 12, 16, 20) | No scale | 3 tokens: `--radius-control` (inputs, buttons), `--radius-card` (cards, dialogs, menus), `--radius-pill: 9999px` (chips, badges, avatars) |
| Inner and outer elements with the same radius (card 16px, image inside 16px with 8px padding) | Corners look wrong | Inner radius = outer radius − padding, or 0 on inner media |
| Radius on one side of a table and not the other; radius on a table cell | Clipped borders | Radius on the wrapper only, `overflow: clip` on that wrapper |
| `border-radius: 50%` on non-square elements to make "pills" | Makes ellipses | `9999px` for pills; `50%` only on squares (avatars) |
| Radius on full-bleed sections and page headers | Floating-card page layout | Full-bleed elements have no radius |

## 11.4 Gradients and backgrounds

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `linear-gradient(135deg, #667eea, #764ba2)` or indigo→violet anywhere | The best-known AI gradient | Solid `var(--color-primary)` |
| Gradient buttons | Decoration on a control | Solid fill token; hover to `var(--color-primary-hover)` |
| Gradient badges and tags | Decoration on metadata | Solid muted background token. See part 12 |
| Several `radial-gradient()` layers on a hero (mesh gradient) | Aurora trope | `background: var(--color-bg)` |
| `background-size: 400%` + keyframes moving `background-position` | Animated gradient; repaints every frame | Static background |
| `border-image: linear-gradient(...)` | Rainbow border; also kills `border-radius` | `border: 1px solid var(--color-border)` |
| Gradient border faked with a pseudo-element and `mask-composite` | Aceternity trick | Solid border |
| `background-clip: text` with a gradient | Gradient text | `color: var(--color-text)` |
| Gradient scrims (`linear-gradient(to top, rgba(0,0,0,.8), transparent)`) on every image | Muddy photos, text contrast varies | Text outside the image. If text must overlay, a flat scrim tested to 4.5:1 at the lightest part of the photo |
| `background-image` SVG noise data URIs | Grain overlay | Delete |
| `background-attachment: fixed` | Parallax on the cheap; broken on iOS; janky | Default scroll |
| Gradient `<hr>` | Decorative divider | `border-top: 1px solid var(--color-border)` |

## 11.5 Filters, blur and blend

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `backdrop-filter: blur()` on cards, dialogs, sidebars, headers | Glass; heavy on low-end Android; contrast varies | Opaque `var(--color-surface)`. Dialog backdrop: flat `var(--color-overlay)` without blur |
| `filter: blur(80px)` on absolutely positioned circles | Blobs | Delete the element |
| `text-shadow` for glow or "readability" | Glow type; blurred text | None. Fix contrast with background, not shadow |
| `mix-blend-mode: overlay/screen` on decorative layers | Effect demo | Delete |
| `filter: grayscale(100%)` on logos with colour on hover | Logo wall trope | Show logos as supplied, or monochrome versions from the brand kit |
| `filter: brightness(1.1)` for hover | Changes images and text unpredictably | Background token change |
| `opacity` animation on large blurred elements | Expensive compositing | Delete |

## 11.6 Transitions, transforms and hover

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `transition: all 0.3s ease` (Tailwind `transition-all duration-300`) | Animates layout properties, causes jank, animates things you did not intend | List properties: `transition: background-color 150ms, border-color 150ms, color 150ms` |
| `* { transition: ... }` global | Everything animates, including theme switches and page load | Transitions per component |
| `transform: scale(1.05)` on hover for cards, images, buttons | Hover zoom | Background or border colour change |
| `transform: translateY(-4px)` on hover | Hover lift | Same |
| `transform: translateX(4px)` arrow nudge on every link | Micro-animation on repeat | Static arrow or no arrow |
| Durations 300–700ms on hover | Sluggish | 100–150ms for colour; see part 25 |
| `cubic-bezier(0.68, -0.55, 0.265, 1.55)` bounce on UI | Cartoon feel | `ease-out` or the easing token from part 25 |
| `will-change: transform` on many elements | Memory cost; no benefit without animation | Remove. Add only to an element during a known animation |
| Hover styles with no `:focus-visible` equivalent | Keyboard users get nothing | Every `:hover` rule on a control has a matching `:focus-visible` rule |
| Hover-only effects on touch screens | Sticky hover on tap | Wrap in `@media (hover: hover)`; use `:active` for touch feedback |
| `@keyframes` for spinners, pulses, bounces, floats defined per file | Animation sprawl | One motion file; reduced-motion guard. See part 25 |

## 11.7 Layout mechanics

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `height: 100vh` on heroes and full-screen layouts | On mobile the address bar changes the viewport; content is cut off | `min-height: 100svh` for full-screen shells, `100dvh` if the layout must follow the bar. Most sections need no height at all |
| `min-h-screen` on every page wrapper | Forces full height where content decides | Only on the app shell |
| `width: 100vw` | Includes scrollbar width; causes horizontal scroll | `width: 100%` |
| Fixed `height` on text containers (cards, buttons, table cells) | Text overflows or clips when translated, zoomed or longer | `min-height` if needed; let content set height |
| Fixed `width` on buttons | Filipino and longer strings clip | Padding sets width; `min-width` if equal sizes are needed |
| `overflow: hidden` to hide a horizontal scroll bug | Masks the real overflow; also clips focus outlines and dropdowns | Find the overflowing element (often `100vw`, negative margins or wide images) and fix it. Use `overflow: clip` only on a known decorative wrapper |
| `overflow-x: hidden` on `body` | Same, and breaks `position: sticky` | Fix the element |
| `position: absolute` to lay out normal content | Breaks on other screen sizes and zoom | Flexbox or grid |
| Negative margins to line things up (`margin-top: -37px`) | Patching a wrong layout | Fix alignment in the parent grid or flex |
| Magic numbers (`top: 73px`, `padding: 13px 17px`, `margin-left: 3.2rem`) | Values tuned by eye for one screen | Spacing scale tokens (`var(--space-3)`). Header offsets from a token (`--header-h`) |
| `display: flex; justify-content: center; align-items: center` on every wrapper | Centering everything; reading lines lose left edge | Left-align text blocks. Centre only small items (icon in a button, empty state) |
| Margins on children for gaps inside flex/grid | Double spacing at the edges | `gap: var(--space-3)` |
| Mixing `space-y-*`, margins and `gap` in one component | Three spacing systems | `gap` for flex and grid children |
| `max-width: 1280px` hard-coded in ten places | Repeated magic value | `--content-max` token. Text measure `max-width: 70ch`. See part 14 |
| `float` for layout | Pre-2017 technique | Grid or flex |
| Padding-top percentage hack for aspect ratio | Old technique | `aspect-ratio: 16 / 9` |
| `line-clamp` with no way to read the rest | Hidden content | Clamp only in lists where the full text is one click away; see part 19 |
| `calc()` chains with magic numbers (`calc(100% - 347px)`) | Layout by arithmetic | Grid with `minmax()` and `fr` |

## 11.8 Stacking and z-index

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `z-index: 9999`, `99999`, `2147483647` | Escalation war | z-index scale tokens: `--z-dropdown: 10`, `--z-sticky: 20`, `--z-overlay: 30`, `--z-dialog: 40`, `--z-toast: 50` |
| `z-[9999]` in Tailwind | Same | Theme `zIndex` scale mapped to the tokens |
| `-z-10` on decorative elements behind content | Usually a blob or glow | Delete the element |
| z-index on elements that are not positioned | Does nothing; noise | Remove, or add `position: relative` if needed |
| z-index fights caused by `transform` or `filter` creating stacking contexts | Symptom of decorative effects | Remove the decorative transform; use `isolation: isolate` on the component root |

## 11.9 Specificity and overrides

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `!important` to win a fight | Specificity debt | Lower the other selector's specificity, or use `@layer`. `!important` only in utility classes that must always win (for example `.visually-hidden`) and in reduced-motion overrides |
| Tailwind `!` modifier (`!p-4`, `!bg-white`) | Same problem | Remove the conflicting class |
| `style=""` inline overrides in templates | Uneditable, untokened | Class in the stylesheet using tokens |
| React `style={{ marginTop: 13 }}` | Same | Class or CSS module with tokens |
| ID selectors for styling (`#main-header .nav a`) | High specificity | Class selectors. See part 29 |
| Selector chains 4+ deep (`.page .content .card .body p`) | Fragile and specific | One class on the element. See part 29 |
| Resetting library styles property by property with `!important` | Override hell | Configure the library (Sass variables, theme config) instead |

## 11.10 Units and sizing

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `font-size` in px everywhere | Ignores the user's browser font setting | `rem` for font sizes |
| `html { font-size: 62.5%; }` | Old trick; breaks third-party components | Leave root at 100%; use rem values directly (0.875rem = 14px) |
| Spacing in `em` inside components with changing font size | Compounding sizes | `rem` or spacing tokens |
| `clamp()` on every font size and padding | Fluid everything; hard to predict | `clamp()` on display headings only; fixed rem for body and UI |
| Unitless magic line-heights per element (1.37, 1.42) | No scale | Line-height tokens: body 1.5, headings 1.2, UI 1.25. See part 13 |
| Media queries in px mixed with em | Inconsistent | One unit for breakpoints, from DESIGN.md. See part 15 |
| Border widths in rem (`0.0625rem`) | Scales with zoom unevenly | `1px` for hairlines |
| Input `font-size` under 16px on mobile | iOS zooms the page | 16px minimum on inputs at mobile widths. See part 15 |

## 11.11 Vendor prefixes and legacy junk

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `-webkit-`, `-moz-`, `-ms-`, `-o-` prefixes hand-written for `transition`, `transform`, `border-radius`, `box-shadow`, `flex` | Copied from 2013 snippets | Unprefixed properties. Let Autoprefixer or Lightning CSS add what the browserslist needs |
| `filter: progid:DXImageTransform…`, `zoom: 1`, `*display: inline` | IE hacks | Delete |
| `-webkit-font-smoothing: antialiased` everywhere by habit | Thins text on macOS; ignored elsewhere | Leave default unless DESIGN.md chooses it for dark surfaces |
| `-webkit-tap-highlight-color: transparent` with no replacement | Removes tap feedback | Keep it only with an `:active` style |
| `text-rendering: optimizeLegibility` on body | Slows long pages on some devices | Remove |
| `-webkit-appearance: none` on everything | Strips native controls including focus | Apply `appearance: none` only to controls you restyle fully, and restyle focus |
| CSS reset of 300 lines pasted on top of a framework that already resets | Duplicate reset | One reset. See part 29 |

## 11.12 Focus, cursor and selection

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `outline: none` / `outline: 0` / `focus:outline-none` with no replacement | Keyboard users lose their place | `:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }` |
| Focus shown as glow `box-shadow` only | Disappears in forced-colours mode | Outline, optionally plus a shadow |
| `cursor: pointer` on non-interactive cards and text | Promises a click that does nothing | Pointer only on links and controls (and cards that are one link) |
| `cursor: not-allowed` with `pointer-events: none` | The cursor never shows | Keep pointer events; block the action in code |
| `pointer-events: none` to hide broken clicks | Hides bugs | Fix the overlapping element |
| `user-select: none` on body or text | Users cannot copy reference numbers, addresses, amounts | Default selection. `user-select: none` only on drag handles |
| Custom thin purple `::-webkit-scrollbar` | Template flourish; hurts usability | Default scrollbars. If needed: `scrollbar-width: thin; scrollbar-color: var(--color-border-strong) transparent` |
| Hidden scrollbars on scrollable areas | Users cannot tell the area scrolls | Visible scrollbar or a scroll shadow cue |
| Brand-coloured `::selection` in purple | Decoration | Default selection, or selection token from DESIGN.md with checked contrast |
| `scroll-behavior: smooth` on `html` | Forced motion | See part 25. Leave default, or wrap in `prefers-reduced-motion: no-preference` |
| `caret-color` in brand colour with glow | Decoration | Default |

## 11.13 CSS custom properties misuse

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Variables named by value (`--purple-500`, `--blue`, `--shadow-big`) used directly in components | Components tied to a colour; theme change means find-and-replace | Two layers: primitives (`--gray-100`) defined once, semantic tokens (`--color-surface`, `--color-text-muted`) used by components. See part 12 |
| A variable for every single value (`--card-padding-left-mobile`) | Token sprawl | Tokens for values used 3+ times or that define the system. One-off values stay local |
| Variables defined inside components and redefined in five places | No source of truth | Global tokens in one `tokens.css` generated from DESIGN.md |
| `var(--primary)` with no fallback in third-party embeds | Breaks outside the app | Fallback only where the variable may be missing: `var(--color-primary, CanvasText)` |
| Colours stored as partial RGB channels (`--primary-rgb: 99,102,241`) for opacity tricks | Opacity-based colour system | Explicit semantic tokens for each tint. Or `color-mix(in oklab, var(--color-primary) 12%, transparent)` defined once as a token |
| Dark mode via `filter: invert(1)` on `html` | Inverts images and brand colours | Redefine semantic tokens under the dark theme selector. See part 12 |
| Tokens defined but hard-coded hex used next to them | Half-migrated | Grep for `#[0-9a-f]{3,8}` and `rgb(` outside `tokens.css`. Replace with tokens |
| JS writing CSS variables every frame for effects | Spotlight cursor, tilt cards | Delete the effect |

## 11.14 Tailwind class soup and arbitrary values

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| 25+ classes on one element, repeated across 12 cards | Unreadable; edits need 12 changes | Extract a component (React/Vue/Blade partial) and keep classes in one place. `@apply` rules in part 29 |
| Arbitrary values: `w-[347px]`, `text-[13px]`, `mt-[37px]`, `rounded-[20px]`, `bg-[#6366f1]` | Bypasses the scale; magic numbers inside classes | Extend the theme with DESIGN.md tokens; use scale classes |
| `bg-[#hex]` colours inline in JSX | Hard-coded palette | Theme colours mapped to CSS variables: `bg-surface`, `text-muted` |
| `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8` copied into every section | Tailwind UI fingerprint, repeated | One layout container component |
| `dark:` variants duplicated for every colour class | Double the classes; drift between themes | Semantic colours backed by CSS variables that switch per theme; no `dark:` on most elements |
| Conflicting classes (`p-4 p-6`, `text-sm text-base`) left in | Order-dependent bugs | `tailwind-merge` in the `cn()` helper, or remove the duplicate |
| `cn()` calls with 10 conditional branches | Styling logic sprawl | Variants with `cva` or a small map of variant → classes |
| `transition-all duration-300 ease-in-out` on everything | See 11.6 | `transition-colors duration-150` where hover exists |
| `hover:scale-105`, `hover:-translate-y-1`, `hover:shadow-2xl` | Hover tropes | `hover:bg-surface-alt` |
| `backdrop-blur-*`, `bg-white/5`, `ring-white/10` | Glass | `bg-surface border-border` |
| `animate-pulse`, `animate-bounce`, `animate-ping` on content | Decorative motion | Only `animate-pulse` on skeletons; see part 25 |
| `shadow-2xl`, `shadow-xl` on static cards | Heavy float | `shadow-sm` or border |
| `rounded-3xl`, `rounded-2xl` on data UI | Bubbly | Theme radius mapped to DESIGN.md |
| `bg-gradient-to-r from-* via-* to-*` | Gradient default | Solid theme colour |
| `text-transparent bg-clip-text` | Gradient text | Solid text colour |
| `tracking-tight` + `font-extrabold` + `text-6xl` on every heading | Hero type everywhere | See part 13 |
| `grid-cols-3` forced on all sizes | Breaks on phones | `grid-cols-1 md:grid-cols-3` or auto-fit with `minmax()` |
| Tailwind default palette (`indigo-600`, `slate-900`) used directly | Default look | Theme colours named by role, mapped to DESIGN.md |
| `className` strings built with template literals from user data | Purged classes vanish in production | Full class names in source; variants via map |

## 11.15 Bootstrap patterns

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Overriding `.btn-primary`, `.card`, `.navbar` in a `custom.css` with `!important` | Override hell | Set Sass variables (`$primary`, `$border-radius`, `$box-shadow`) before importing Bootstrap. See part 29 |
| `.shadow-lg` on every card | Heavy default | `.shadow-sm` or `.border` only |
| `.rounded-pill` on cards and inputs | Bubbly | Default radius from `$border-radius` |
| `.bg-primary.text-white` sections alternating with `.bg-light` | Alternating band template | One background |
| `.display-1` / `.display-4` headings on app pages | Marketing type in tools | `h1`–`h3` scale set in Sass |
| `.jumbotron` (or recreated in v5) on every page | Hero everywhere | Page heading and content |
| `.text-muted.small` on half the page | Low contrast, tiny text | Muted only for secondary metadata; check 4.5:1. See part 12 |
| `.bg-gradient` utility | Gradient default | Flat colours |
| Utility soup (`.d-flex.justify-content-between.align-items-center.mb-3.p-3.border.rounded.shadow-sm`) on every row | Same problem as Tailwind soup | Component class in the Sass build |
| Mixing Bootstrap and Tailwind in one project | Two systems, conflicting resets | Pick one |
| Bootstrap loaded from a CDN at `@latest` plus a local copy | Duplicate and unpinned | One pinned version. See part 34 |
| Bootstrap Icons, Font Awesome and Material Icons all loaded | Three icon fonts | One icon set. See part 26 |

## 11.16 What to use instead: token block

This replaces section 2.3 of v3.0.0. Values come from DESIGN.md. The neutral fallbacks shown are for missing tokens only.

```css
/* Use: tokens.css (generated from DESIGN.md) */
:root {
  /* Surfaces and lines: values from DESIGN.md */
  --color-bg:            /* page */;
  --color-surface:       /* cards, header, dialogs */;
  --color-surface-alt:   /* hover rows, subtle panels */;
  --color-border:        /* 1px dividers */;
  --color-border-strong: /* inputs */;
  --color-text:          /* body text */;
  --color-text-muted:    /* secondary text, 4.5:1 checked */;
  --color-primary:       /* one accent */;
  --color-primary-hover: /* accent hover */;
  --color-focus:         /* focus outline, 3:1 checked */;
  --color-overlay:       /* dialog backdrop */;

  /* Radius: 3 steps */
  --radius-control: 4px;   /* inputs, buttons */
  --radius-card:    8px;   /* cards, dialogs, menus */
  --radius-pill:    9999px;/* chips, badges, avatars only */

  /* Shadow: neutral, 3 steps, floating layers only */
  --shadow-1: 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-2: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-3: 0 8px 24px rgba(0, 0, 0, 0.12);

  /* Spacing scale (4px base) */
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem; --space-4: 1rem;
  --space-6: 1.5rem;  --space-8: 2rem;   --space-12: 3rem;  --space-16: 4rem;

  /* Stacking */
  --z-dropdown: 10; --z-sticky: 20; --z-overlay: 30; --z-dialog: 40; --z-toast: 50;

  /* Motion */
  --dur-fast: 150ms;
  --ease-out: cubic-bezier(0.2, 0, 0, 1);
}
```

```css
/* Use: components built on the tokens */
.card {
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
}

.row:hover { background-color: var(--color-surface-alt); }

.btn {
  background-color: var(--color-primary);
  border-radius: var(--radius-control);
  transition: background-color var(--dur-fast) var(--ease-out);
}
@media (hover: hover) {
  .btn:hover { background-color: var(--color-primary-hover); }
}

.menu, .popover { box-shadow: var(--shadow-2); z-index: var(--z-dropdown); }
.dialog         { box-shadow: var(--shadow-3); z-index: var(--z-dialog); }
.dialog-backdrop { background: var(--color-overlay); }  /* no blur */

.site-header {
  position: sticky; top: 0; z-index: var(--z-sticky);
  background-color: var(--color-surface);            /* opaque, no blur */
  border-bottom: 1px solid var(--color-border);
}

:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
```

`.btn:hover { opacity: 0.9; }` from v3.0.0 is still acceptable where no hover token exists. Prefer the hover token: opacity also fades the text and can drop it below 4.5:1.

## 11.17 Banned and replacement pairs

```css
/* Banned */
.hero { height: 100vh; width: 100vw; overflow: hidden; }
/* Use */
.hero { padding-block: var(--space-12); }
```

```css
/* Banned */
.modal { z-index: 99999 !important; }
/* Use */
.modal { z-index: var(--z-dialog); }
```

```css
/* Banned */
.card-title { height: 48px; overflow: hidden; }
/* Use */
.card-title { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
/* only where the full title is one click away */
```

```css
/* Banned */
a, button, .card, .row, img { transition: all .3s ease-in-out; }
/* Use */
.btn, .nav-link { transition: background-color var(--dur-fast), color var(--dur-fast); }
```

```html
<!-- Banned -->
<div class="w-[347px] mt-[37px] p-[13px] rounded-[20px] bg-[#1e1b4b] shadow-2xl shadow-indigo-500/40 hover:scale-105 transition-all duration-300">

<!-- Use -->
<div class="w-full max-w-sm mt-8 p-4 rounded-lg bg-surface border border-border">
```

## 11.18 Check

- [ ] No coloured or zero-offset glow `box-shadow`.
- [ ] Shadows come from 2–3 tokens and appear only on menus, popovers, dialogs, toasts (and cards if DESIGN.md says so).
- [ ] Radius comes from 3 tokens; nothing at 20px+ on data UI.
- [ ] No `linear-gradient` or `radial-gradient` on buttons, badges, text or content areas.
- [ ] No `border-image` gradients.
- [ ] No animated `background-position` or `background-size: 400%`.
- [ ] No `backdrop-filter` except where DESIGN.md defines glass.
- [ ] No `filter: blur()` blobs, no `text-shadow`, no decorative `mix-blend-mode`.
- [ ] No `transition: all`; no global `*` transitions.
- [ ] No `scale` or `translate` on hover for cards, rows, images.
- [ ] Hover rules wrapped in `@media (hover: hover)`; each has a `:focus-visible` match.
- [ ] No `will-change` left on static elements.
- [ ] No `100vh` on sections; app shell uses `svh`/`dvh`.
- [ ] No `100vw` widths.
- [ ] No fixed heights or widths on text containers and buttons.
- [ ] No `overflow: hidden` on `body` or used to hide a scroll bug.
- [ ] No absolute positioning for normal layout; no negative-margin patches.
- [ ] No magic pixel values outside `tokens.css`.
- [ ] Gaps use `gap`, not child margins.
- [ ] z-index values come from the 5-step scale. No 999+.
- [ ] `!important` only in utilities and the reduced-motion block.
- [ ] No inline `style=` overrides in templates or JSX.
- [ ] Font sizes in rem; root font size left at 100%.
- [ ] Inputs 16px or larger on mobile.
- [ ] No hand-written vendor prefixes; build tool handles them.
- [ ] No `outline: none` without a `:focus-visible` outline.
- [ ] `cursor: pointer` only on clickable elements.
- [ ] No `user-select: none` on text.
- [ ] No custom purple scrollbars or hidden scrollbars on scroll areas.
- [ ] Components use semantic tokens, not primitive colour names.
- [ ] No hex or `rgb()` outside `tokens.css` (grep `#[0-9a-fA-F]{3,8}\b`).
- [ ] Dark mode redefines tokens; no `filter: invert()`.
- [ ] No Tailwind arbitrary values for colour, spacing or radius.
- [ ] No 25+ class strings repeated; repeated patterns extracted to components.
- [ ] No duplicated `dark:` classes where semantic colours can switch.
- [ ] No Tailwind default palette names in markup.
- [ ] Bootstrap themed with Sass variables, not `!important` overrides.
- [ ] One CSS framework and one icon set per project.
