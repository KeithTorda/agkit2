---
part: 15
title: Responsive and mobile
covers: breakpoints, test widths, touch targets, hover-only interactions, horizontal overflow, viewport units, mobile nav behaviour, bottom sheets, tables on mobile, mobile font sizes, iOS input zoom, safe areas, orientation, low-end Android, slow networks, in-app browsers, image sizes, desktop-only features
---

# 15 — Responsive and mobile

Read when: building any page that phones will open. In the Philippines that is almost every page: most visitors to LGU, school, election and small-business sites arrive on a mid-range or low-end Android phone, often from a Facebook or Messenger link.

## 15.1 Breakpoints

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Desktop-first CSS with `max-width` overrides stacked for each device | Mobile gets leftover styles and patches. | Mobile-first: base styles for small screens, `min-width` queries to add columns. |
| Breakpoints named after devices (`iphone`, `ipad`, `macbook`) | Device list goes stale. Android sizes ignored. | Breakpoints where the layout breaks: typical tokens `40rem` (640px), `48rem` (768px), `64rem` (1024px), `80rem` (1280px). From DESIGN.md. |
| 6–8 breakpoints, each with small tweaks | Hard to test. Layout jumps at many widths. | 3–4 breakpoints. Use fluid layout (`minmax`, `auto-fill`, `clamp` on headings) between them. |
| Breakpoints in px in some files, rem in others, different values per component | No system. | One set of breakpoint tokens. Same values in CSS and JS. |
| `@media (max-width: 768px)` and `@media (min-width: 768px)` both matching at 768px | Overlap bug at exactly 768px. | Mobile-first `min-width` only, or use range syntax `(width < 48rem)` / `(width >= 48rem)`. |
| Layout switch driven by JS `window.innerWidth` | Flash of wrong layout. Breaks with SSR. | CSS media queries. JS `matchMedia` only when behaviour, not layout, must change. |
| Viewport-based layout for a component that sits in different widths (card in sidebar vs main) | Component breaks in narrow containers on wide screens. | Container queries (`@container`) for reusable components. |
| Hiding content on mobile with `hidden md:block` to "simplify" | Mobile users lose information, often the key info (price, date, status). | Reflow content. Hide only decoration. |
| Separate mobile and desktop markup rendered twice (`md:hidden` + `hidden md:flex`) for the same content | Duplicate DOM, duplicate IDs, screen readers read both in some cases. | One markup that reflows. Duplicate only nav shells if needed, with the hidden copy truly `display: none`. |

## 15.2 Test widths

Generated UIs are checked at one desktop width. Check these every time.

| Width | What it represents | Check |
|---|---|---|
| 320px | Small Android, zoomed text, split-screen | Nothing overflows horizontally. Buttons still fit. |
| 360px | Most common low-end and mid-range Android width in PH | Primary layout target. Forms, tables, nav usable. |
| 390px | Current iPhone standard width | Same as 360 with slightly more room. |
| 768px | Tablet portrait, small laptops zoomed | Two-column switch looks right. Nav mode correct. |
| 1024px | Tablet landscape, small laptops, school and LGU office desktops at 1366x768 with browser chrome | Sidebar + content fit without horizontal scroll. |
| 1440px | Common desktop | Containers capped, text not too wide. |
| 1920px+ | Large monitors, projectors in barangay halls and classrooms | Content does not stretch. Max-width holds. |

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Only tested at 1440px | Mobile issues missed. | Check all widths above before reporting done. |
| Only tested in Chrome DevTools device mode | Misses address bar behaviour, keyboard, real touch. | Also open on a real Android phone or an emulator when possible. Say which in the report. |
| Test at 390px only | 360px is common in PH. 30px less width breaks many layouts. | 360px is the base target. |
| Height ignored (only widths tested) | Landscape phones are about 360px tall. Modals and sticky bars cover everything. | Test 740x360 landscape. |
| Tested only with short English copy | Filipino strings and long names overflow. | Test with the longest real strings: full names with suffixes ("Ma. Cristina Dela Cruz-Santos Jr."), Filipino labels, long barangay names. |

## 15.3 Touch targets

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Icon buttons at 24px or smaller with no padding | Hard to tap, frequent mis-taps. | Minimum 24x24 CSS px (WCAG 2.2 AA). Target 44x44 for primary touch actions. Extend hit area with padding, not icon size. |
| Links in a dense list with 4px vertical gap | Mis-taps on neighbours. | 8px+ spacing between adjacent targets, or rows 44px+ tall. |
| Table row actions as tiny icons in the last column | Unusable on phones. | Row tap opens detail. Actions on the detail view or in one overflow menu per row with a 44px trigger. |
| Close X at 16px in modal corner (original 3.5 "Tiny X") | Hard to hit. | 44x44 close target plus a visible Cancel button. See part 21. |
| Checkbox and radio at native 13px with label not clickable | Tiny target. | Wrap input in `<label>` so the text is tappable. Visual control 20–24px. Forms: see part 17. |
| Pagination numbers 28px wide, 2px apart | Mis-taps. | 44px targets, or Previous/Next only on mobile. |
| Slider/range inputs for exact values | Hard to set precisely by thumb. | Number input, with slider as optional helper. |
| Swipe-only actions (swipe to delete, swipe to archive) | Hidden, not discoverable, not accessible. | Visible button. Swipe only as a shortcut to an action also reachable by tap. |
| Long-press only actions | Hidden. | Visible menu button. |
| Double-tap actions | Conflicts with zoom. | Single tap. |
| Draggable sort with no alternative | Hard on touch. | Move up/down buttons or a position field as well. |
| POS product tiles at 64px on a tablet | Cashier mis-taps under speed. | Product tiles 88px+ tall on tablets, clear gaps. |

## 15.4 Hover-only interactions

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Actions shown only on row hover | Touch users never see them. | Actions visible or behind a visible menu button. Hover may reveal extras on pointer devices only: `@media (hover: hover)`. |
| Tooltip is the only place a label or value appears | No hover on touch. | Visible label. Tooltip only as extra detail, also opened by tap and focus. See part 21. |
| Mega menu or dropdown that opens on hover only | Touch cannot open it, or first tap follows the link. | Open on click/tap. Hover open on desktop is optional and must not replace click. See part 16. |
| Hover animations on mobile (original 5.3) | Sticky hover state after tap. | Wrap hover styles in `@media (hover: hover) and (pointer: fine)`. Use `:active` for touch feedback. |
| Image caption revealed on hover | Hidden on phones. | Caption always visible below the image. |
| Card flips on hover to show details | Touch cannot trigger it. | Show details on the card or on its page. |
| Password "hover to reveal" | Not usable on touch. | "Show password" toggle button. See part 23. |
| Chart values shown only on hover | Values hidden on phones. | Data labels or a table under the chart. See part 20. |
| `title` attribute as the only explanation | No touch support, not read reliably. | Visible text. |

## 15.5 Horizontal overflow

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Page scrolls sideways at 360px | Some element wider than viewport: fixed widths, long words, wide tables, `100vw` with scrollbar. | Find the element (outline all with `* { outline: 1px solid red }` temporarily). Fix its width. |
| `overflow-x: hidden` on `html`/`body` to hide the bug | Breaks `position: sticky`, hides content, still scrolls on iOS in some cases. | Fix the element. Use `overflow-x: clip` only on a specific decorative wrapper. |
| `width: 100vw` on full-bleed sections | Includes scrollbar width on desktop; overflows by 15–17px. | `width: 100%`, or full-bleed via grid (`grid-column: 1 / -1`). |
| Fixed `width: 500px` on cards, images, inputs | Wider than phone. | `max-width: 100%` and `width: 100%` or intrinsic sizes. |
| `min-width` on flex children stopping shrink | Flex items default `min-width: auto`; long content pushes out. | `min-width: 0` on flex/grid children that hold text. |
| Long unbroken strings (emails, URLs, reference numbers, Tagalog compounds) | Push layout wider. | `overflow-wrap: anywhere` on user content. See part 13. |
| Code blocks and pre without scroll | Page scrolls instead of the block. | `pre { overflow-x: auto; max-width: 100%; }` |
| Embedded maps, videos, iframes with fixed width | Overflow. | `width: 100%; aspect-ratio: 16/9;` on the iframe. |
| Absolutely positioned decorations off-screen (`right: -200px`) | Decorative blobs cause sideways scroll. See part 10. | Remove the decoration. |
| Button rows that do not wrap | Buttons pushed out of view. | `flex-wrap: wrap` or stack buttons full width on mobile. |
| Tabs row that overflows without cue | Hidden tabs. See part 16. | Scrollable tabs with visible partial tab and fade, or a select on mobile. |

## 15.6 Viewport height and units

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `height: 100vh` on hero or app shell | On mobile, `100vh` is taller than the visible area when the address bar shows. Bottom content and buttons get hidden. | `min-height: 100dvh` with `100vh` fallback before it. Use `svh` when the element must never exceed the smallest visible area. |
| `h-screen` in Tailwind for full-height layouts | Same bug. | `min-h-dvh` (Tailwind 3.4+) or `min-h-[100dvh]` with a fallback. |
| Fixed bottom button hidden under the mobile browser bar or keyboard | Uses `bottom: 0` with `100vh` layout. | Use `dvh` layouts, `env(safe-area-inset-bottom)`, and test with the keyboard open. |
| JS that sets `--vh` on resize (old workaround) copied into new projects | Obsolete. Causes jank on scroll. | `dvh`/`svh`/`lvh` units. |
| Full-screen modals with `height: 100vh` | Bottom action buttons cut off. | `max-height: 100dvh` and a scrollable body with fixed footer. |
| Chat or POS layout with `height: 100vh` and inner scroll | Input box hidden under keyboard on Android. | `100dvh` and `interactive-widget=resizes-content` in the viewport meta if the layout depends on keyboard height. Test on Android Chrome. |

## 15.7 Mobile navigation behaviour

Navigation components and their rules are in part 16. This section covers only responsive behaviour.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hamburger on desktop (original 3.2) | Hides nav with room to show it. | Visible nav at `64rem`+. Hamburger at smaller widths only. See part 16. |
| Mobile menu that does not lock body scroll | Page scrolls behind the open menu. | Lock scroll while open (`overflow: hidden` on `html` only during open state, or `<dialog>`). Restore position on close. |
| Mobile menu taller than viewport with no scroll | Bottom links unreachable. | Menu panel `max-height: 100dvh; overflow-y: auto`. |
| Menu does not close after tapping a link in single-page apps | Menu covers the new page. | Close on route change. |
| Sidebar that shrinks to icons on mobile (original 3.7 icon-only collapse) | Icons without labels. | Off-canvas drawer with full labels on mobile. |
| Desktop sidebar still visible at 768px squeezing content to 400px | Breakpoint too low. | Sidebar collapses to drawer below `64rem` unless content still fits. |
| Tab bar with 6+ items on mobile (original 3.2) | Crowded, tiny labels. See part 16. | 4–5 items max, rest under "More". |
| Mobile header taller than 64px with logo, search, bell, avatar, menu | Crowded, eats screen. | 48–56px header: logo, one or two icons, menu. Search behind an icon or on its own row. |

## 15.8 Bottom sheets, drawers, mobile overlays

Overlay rules in general are in part 21.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Desktop centered modal shown unchanged on phones | Tiny modal with small text, or modal wider than screen. | On small screens, full-width sheet anchored to bottom or full-screen page for longer forms. |
| Bottom sheet with no visible close | Swipe-down only. | Close button and Cancel. Swipe as a shortcut. |
| Bottom sheet covering 100% height with a drag handle | Looks like a sheet, behaves like a page. | If content needs full height, open a page. Sheets for short choices (up to about 60% height). |
| Sheet content scroll fights sheet drag gesture | Custom gesture library clash. | Native `<dialog>` with CSS, no drag, or a tested library. |
| Filters panel as a modal with 20 inputs on mobile | Hard to use. | Full-screen filter page with Apply and Clear at the bottom, sticky. |
| Select opens a custom dropdown on mobile | Native pickers work better on phones. | Native `<select>` on mobile. See part 17. |

## 15.9 Tables on mobile

Table design in general is in part 19. This covers small screens.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Wide table shrunk with 10px font to fit 360px | Unreadable. | Keep text size. Allow horizontal scroll inside a wrapper, or change layout. |
| Horizontal scroll without indicator (original 3.4) | Users do not know columns exist. | Sticky first column plus scroll shadow or a partial column visible at the edge. |
| Every table converted to stacked cards on mobile | Loses comparison across rows. Works for records, fails for numbers. | Stacked cards for record lists (people, orders). Scrolling table for numeric comparisons (grades, sales, vote counts). |
| Stacked cards with labels missing (just values) | "12 / 45 / Active" with no meaning. | Each value with its label: `<dl>` per row or `data-label` rendered via `::before`. |
| All 12 columns kept on mobile | Scrolling far to find the one column needed. | Prioritise 3–4 columns. Other columns in the row's detail view. |
| Table wrapper with `overflow: auto` but the page also scrolls sideways | Two horizontal scrolls. | Only the wrapper scrolls. Check 15.5. |
| Sticky header in a horizontally scrolling table breaks | `overflow` on the wrapper kills `position: sticky` on page scroll. | Constrain wrapper height and use sticky header inside it, or accept non-sticky on mobile. |
| Row click targets smaller than row | Only the name is tappable. | Whole row tappable via a link in the first cell expanded with `::after` inset, keeping other controls above it. |

## 15.10 Text and input sizes on mobile

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Input font-size below 16px | iOS Safari zooms the page on focus and does not zoom back. | `font-size: 16px` (1rem) minimum on `input`, `select`, `textarea` on mobile. |
| Fixing the zoom with `maximum-scale=1` or `user-scalable=no` | Blocks pinch zoom. Fails WCAG 1.4.4. See part 27. | `<meta name="viewport" content="width=device-width, initial-scale=1">` only. Fix input size instead. |
| Body text 14px on mobile because it "looks cleaner" | Hard to read for older users and on low-DPI screens. | Body 16px on mobile. |
| Hero heading scaled with `vw` to 64px on phone | Wraps one word per line. | Mobile headings 24–32px. See part 13. |
| Headings that shrink below body size at small widths | `clamp()` minimum set too low. | Minimum heading size at least one step above body. |
| Line length on tablet 100+ characters | Prose container missing `max-width`. | `max-width: 65ch`. |
| `-webkit-text-size-adjust: none` | Prevents text scaling in landscape and some accessibility settings. | `text-size-adjust: 100%` (and `-webkit-` prefix) only. |
| Text in images (flyers, posters) as the only copy of an announcement | Unreadable on phones, not searchable. Common on LGU/school Facebook-style posts. | Post the text as HTML. Image is an extra. Alt text: see part 26. |

## 15.11 Safe areas and notches

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Fixed bottom bar under the iPhone home indicator | Buttons overlap system gesture area. | `padding-bottom: calc(var(--space-3) + env(safe-area-inset-bottom))`. |
| `viewport-fit=cover` added without safe-area padding | Content under the notch in landscape. | Add `viewport-fit=cover` only with `env(safe-area-inset-*)` padding on edges. |
| Safe-area padding added to every element | Doubles padding. | Apply only on the fixed edge elements (header, bottom bar, full-bleed sheet). |
| Full-screen PWA with status bar overlapping header | Missing top inset. | `padding-top: env(safe-area-inset-top)` on header in standalone mode. |

## 15.12 Orientation

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Please rotate your device" screens | Blocks use. Fails WCAG 1.3.4. | Support both orientations. |
| Landscape phone: sticky header + sticky footer + keyboard leave 80px of content | Only portrait tested. | Reduce or un-stick bars when viewport height is under about 500px: `@media (max-height: 31rem)`. |
| Tablet POS layout only works landscape | Tablets on stands get rotated. | Portrait layout: product grid above, cart below or in a drawer. |
| Video or map locked to portrait size | Poor use of landscape. | `aspect-ratio` and max-height so media fits both. |

## 15.13 Low-end Android, slow networks, in-app browsers

Performance budgets and SEO are in part 34. These rows cover what breaks on the devices PH users hold.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Built and tested on a fast laptop on fibre | PH users often on 2–4 GB RAM phones, prepaid mobile data, weak signal in provinces. | Test with DevTools CPU 4x slowdown and "Slow 4G" or "3G" throttling. Page must be usable within a few seconds. |
| Heavy JS for static pages (full SPA for a barangay notice board) | Slow first load, drains data. | Server-rendered HTML. JS only where interaction needs it. |
| `backdrop-filter: blur()` and large box-shadows on scroll | Janky scroll on low-end GPUs. See part 10 and 11. | Solid backgrounds. |
| Autoplay background video | Burns prepaid data. Stutters. See part 26. | Static image or none. |
| Heavy animations and scroll listeners | Jank on low-end devices. See part 25. | No scroll-triggered animation. `prefers-reduced-motion` respected. |
| Page breaks in Facebook/Messenger in-app browser | Most PH traffic from shared links opens there. Downloads, file inputs, popups, OAuth redirects and `window.open` often fail. | Test links from Messenger. Avoid popup-based login. Offer "Open in browser" hint only where a feature truly fails (file download, Google sign-in). |
| Google sign-in as the only login inside in-app browsers | Google blocks OAuth in embedded webviews. | Email/phone login available too. See part 23. |
| Downloads (PDF certificates, forms) that only work via `blob:` links | Fail in in-app browsers. | Direct `https` link to the file with `Content-Disposition`. State file type and size in link text. |
| Loading 4 MB hero image on mobile | Data cost, slow. | Responsive images (15.14). Budget: see part 34. |
| Offline or weak-signal state not handled for forms | User loses a long form when signal drops. | Keep form data on failed submit. Show a retry. Save drafts locally for long forms (e.g. registration). Copy: see part 04. |
| Requires the latest Chrome features without fallback | Older Android WebView and Samsung Internet lag. | Check support for `:has()`, `dvh`, container queries, `text-wrap`. Provide simple fallbacks. |
| Lite/data-saver mode breaks the page | Images removed, fonts blocked. | Page readable with images and web fonts off. |
| Fonts load late, text invisible | See part 13. | `font-display: swap`. |

## 15.14 Images on mobile

Image content rules (stock, AI images, alt text) are in part 26.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| One large image file for all screen sizes | Phones download desktop-size files. | `srcset` with widths (e.g. 480, 800, 1200, 1600) and a correct `sizes` attribute. |
| `sizes` missing or set to `100vw` for an image in a 3-col grid | Browser picks a file 3x too large. | `sizes="(min-width: 64rem) 33vw, 100vw"` matching the layout. |
| Images without `width` and `height` | Layout shift as images load. | Always set `width`/`height` or `aspect-ratio`. |
| `loading="lazy"` on the hero/LCP image | Delays the main image. See part 34. | `loading="eager"` and `fetchpriority="high"` on the LCP image. Lazy for below-fold. |
| Art-direction ignored: wide banner cropped to a thin strip on phones | Key subject cut off. | `<picture>` with a mobile crop, or `object-position` on the subject. |
| PNG photos | Large. | WebP or AVIF with JPEG fallback. |
| Background images via CSS for content images (officials' photos, products) | No alt, no `srcset` control, no lazy loading. | `<img>` for content. CSS backgrounds only for decoration. |
| Logo walls and galleries with 30 full-size images on mobile | Heavy scroll. | Fewer items on mobile, or a "View all" page. |

## 15.15 Desktop-only features

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Drag-and-drop file upload with no button | No drag on phones. | Visible "Choose file" button. Drag area as extra on desktop. See part 17. |
| Right-click context menus as the only way to act | Not available on touch. | Visible menu button per item. |
| Keyboard shortcuts as the only way to trigger an action | Phones lack them. | Shortcuts only as accelerators for visible controls. See part 18. |
| Features that require a wide screen (side-by-side compare, spreadsheet editing) with no mobile path | Mobile users stuck. | Mobile path: one-at-a-time view, or a clear note "Editing is available on desktop" with read access on mobile. |
| Print-only outputs (certificates, receipts) with no mobile save | Many users have no printer. | "Download PDF" plus print. PDF readable on phone. |
| Hover preview of links, images, users | Absent on touch. See 15.4. | Tap opens the item. |
| Multi-select with Shift/Ctrl-click only | No modifier keys on touch. | Checkboxes per row. |
| Tooltips on disabled buttons to explain why | Touch cannot see them. See part 18. | Explanation text next to the button. |
| Webcam QR scanning without file-upload fallback | Some in-app browsers block camera. | Offer image upload or manual code entry. |

## 15.16 Tailwind and Bootstrap specifics

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `h-screen` / `min-h-screen` on shells and heroes | `100vh` bug. | `min-h-dvh` with fallback, or content height. |
| `hidden md:block` on important content | Mobile loses info. | Reflow instead of hide. |
| `text-xs` or `text-sm` on inputs | iOS zoom. | `text-base` on inputs at mobile sizes. |
| `hover:` utilities for key actions (`opacity-0 group-hover:opacity-100` on row actions) | Invisible on touch. | Visible by default. Hover styles only change emphasis. Tailwind v4 wraps `hover:` in `@media (hover: hover)`; v3 does not, so add a custom variant. |
| `w-[500px]`, `min-w-[600px]` on content blocks | Overflow at 360px. | `w-full max-w-*`. |
| `overflow-x-hidden` on the root layout | Hides overflow bug. | Find the element (15.5). |
| `grid-cols-2` without a mobile base | Two columns at 360px. | `grid-cols-1 sm:grid-cols-2`. |
| Bootstrap `col-6` without `col-12` base | Two squeezed columns on phones. | `col-12 col-md-6`. |
| Bootstrap `table-responsive` wrapper missing on wide tables | Page scrolls sideways. | Wrap every wide table in `.table-responsive`. |
| Bootstrap `navbar-expand` with no breakpoint (always expanded) | Nav overflows on phones. | `navbar-expand-lg` so it collapses under 992px. |
| Bootstrap modal without `modal-fullscreen-sm-down` for long forms | Cramped modal on phones. | `modal-fullscreen-sm-down` or a page. |
| Bootstrap `d-none d-md-block` on the only copy of a price or status | Hidden on mobile. | Reflow the layout. |

## 15.17 Code: banned vs use

```html
<!-- Banned: disables zoom -->
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">

<!-- Use -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```

```css
/* Banned: desktop-first, 100vh, hover-only actions, overflow hidden patch */
html, body { overflow-x: hidden; }
.hero { height: 100vh; }
.row-actions { opacity: 0; }
tr:hover .row-actions { opacity: 1; }
input { font-size: 14px; }
@media (max-width: 767px) { .grid { grid-template-columns: 1fr 1fr; } }

/* Use: mobile-first, dynamic viewport, visible actions, 16px inputs */
.shell { min-height: 100vh; min-height: 100dvh; }
.row-actions { opacity: 1; }
@media (hover: hover) and (pointer: fine) {
  .row-actions { opacity: 0.6; }
  tr:hover .row-actions, tr:focus-within .row-actions { opacity: 1; }
}
input, select, textarea { font-size: 1rem; }
.grid { display: grid; gap: var(--space-4); grid-template-columns: 1fr; }
@media (min-width: 40rem) { .grid { grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr)); } }

.icon-btn { min-width: 44px; min-height: 44px; display: inline-grid; place-items: center; }

.bottom-bar {
  position: sticky; bottom: 0;
  padding: var(--space-3) var(--space-4) calc(var(--space-3) + env(safe-area-inset-bottom));
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
}
@media (max-height: 31rem) { .bottom-bar { position: static; } }

.table-scroll { overflow-x: auto; max-width: 100%; }
.table-scroll th:first-child, .table-scroll td:first-child { position: sticky; left: 0; background: var(--color-surface); }

.flex-row > * { min-width: 0; }
.user-content { overflow-wrap: anywhere; }
```

```html
<!-- Banned: one big file, no dimensions, lazy hero -->
<img src="/img/barangay-hall.jpg" loading="lazy" class="w-full">

<!-- Use: responsive sizes, dimensions, eager LCP -->
<img
  src="/img/barangay-hall-800.webp"
  srcset="/img/barangay-hall-480.webp 480w, /img/barangay-hall-800.webp 800w, /img/barangay-hall-1200.webp 1200w"
  sizes="(min-width: 64rem) 50vw, 100vw"
  width="1200" height="675"
  alt="Barangay San Isidro hall, front entrance"
  fetchpriority="high">
```

## 15.18 Check

- [ ] CSS is mobile-first with `min-width` queries.
- [ ] 3–4 breakpoints from tokens. Same values in CSS and JS.
- [ ] No overlap bug at exact breakpoint widths.
- [ ] Reusable components use container queries where they sit in different widths.
- [ ] Checked at 320, 360, 390, 768, 1024, 1440 and 1920px.
- [ ] Checked in landscape at about 740x360.
- [ ] Tested with the longest real strings, including Filipino labels and long names.
- [ ] No horizontal page scroll at 320px.
- [ ] No `overflow-x: hidden` on `html`/`body` hiding a bug.
- [ ] No `100vw` full-bleed widths.
- [ ] Flex/grid text children have `min-width: 0` where needed.
- [ ] Touch targets 24x24 minimum, 44x44 for primary actions.
- [ ] 8px+ between adjacent tap targets.
- [ ] No action or information available only on hover.
- [ ] Hover styles wrapped in `@media (hover: hover)`. `:active` feedback for touch.
- [ ] No swipe-only, long-press-only or drag-only actions.
- [ ] No `100vh` for full-height layouts. `dvh` with fallback.
- [ ] Fixed bottom elements respect `env(safe-area-inset-bottom)`.
- [ ] Sticky bars relax on short (landscape) viewports.
- [ ] No "rotate your device" screen.
- [ ] Hamburger only below the desktop breakpoint.
- [ ] Mobile menu locks body scroll, scrolls itself, closes on navigation.
- [ ] Mobile tab bar has 5 items or fewer.
- [ ] Modals become sheets or pages on small screens.
- [ ] Wide tables scroll inside a wrapper with a visible cue, or become labelled stacked rows.
- [ ] Inputs are 16px on mobile.
- [ ] Viewport meta allows zoom. No `maximum-scale=1`, no `user-scalable=no`.
- [ ] Body text 16px on mobile.
- [ ] Announcements exist as HTML text, not only as images.
- [ ] Tested with CPU 4x slowdown and slow network throttling.
- [ ] Tested inside the Facebook/Messenger in-app browser for shared-link pages.
- [ ] Login does not depend only on Google sign-in or popups.
- [ ] File downloads use direct links with type and size stated.
- [ ] Long forms keep data after a failed submit.
- [ ] Images use `srcset`, correct `sizes`, `width`/`height`, WebP/AVIF.
- [ ] LCP image is not lazy-loaded.
- [ ] File upload has a visible button, not only drag-and-drop.
- [ ] Every desktop-only feature has a mobile path or a stated limit.
- [ ] Bootstrap: `col-12` base, `table-responsive`, `navbar-expand-lg`.
