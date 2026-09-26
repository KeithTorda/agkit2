---
part: 27
title: Accessibility
covers: div buttons, ARIA misuse, role soup, missing labels, focus outlines, focus order, focus traps, colour-only meaning, contrast, target sizes, heading order, landmarks, skip links, alt text, motion, keyboard navigation, screen reader text, form error announcement, live regions, language attribute, zoom, tables, dialogs, testing
---

# 27 — Accessibility

Read when: building or reviewing any interactive component, form, page layout, colour choice, or content that must work with keyboard, screen reader, zoom, or touch. Government and school sites must meet WCAG 2.1 AA at minimum; target WCAG 2.2 AA.

## 27.1 The AI accessibility signature

Generated code tends to fail accessibility in two opposite ways at once: native elements replaced with `div`s, and ARIA sprayed on top to compensate. Both are tells.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `aria-*` on nearly every element | Added to "look accessible"; most of it is wrong or redundant | Native HTML first. Add ARIA only where no native element exists (tabs, combobox, tree) |
| `role="button"` on a `div` | Missing keyboard support (Enter, Space), focus and disabled state | `<button type="button">` |
| `role="navigation"` on `<nav>`, `role="main"` on `<main>`, `role="banner"` on `<header>` | Redundant; the element already has the role | Drop the role attribute |
| `role="list"` on a `<ul>` without reason | Redundant (except to restore semantics after `list-style: none` in Safari, which is the one valid case) | Keep only when Safari VoiceOver drops list semantics and the list count matters |
| `aria-label` on a `div` or `span` with no role | Ignored by most screen readers | Put the text in the element, or use a real element that accepts a name |
| `aria-label` that repeats the visible text | Noise; risks drift from visible text | Remove. Visible text is the name |
| `aria-label` that differs from the visible label ("Submit form" on a button reading "Send") | Voice-control users say "click Send" and nothing happens (WCAG 2.5.3) | Accessible name starts with the visible text |
| `tabindex="0"` on non-interactive text, cards, headings | Adds useless tab stops | Remove. Only interactive elements are focusable |
| `tabindex="1"` or higher | Breaks the natural tab order | Never positive `tabindex`. Fix DOM order |
| `aria-hidden="true"` on a focusable element | Focus lands on something the screen reader cannot see | Remove `aria-hidden`, or make the element non-focusable too (`inert`) |
| "Accessibility widget" overlay (accessiBe, UserWay, floating wheelchair button) | Does not fix the code; often breaks screen readers | Remove. Fix the HTML |
| `alt`, `aria-label` and `title` all set to the same text | Belt-and-braces spam | One accessible name, one mechanism |

## 27.2 Interactive elements

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `<div onclick>` / `<span onclick>` as a button | No keyboard, no focus, no role | `<button type="button">` |
| `<a>` without `href` used as a button (`<a onclick>`, `<a href="#">`, `<a href="javascript:void(0)">`) | Not a link, not a button; `#` jumps to top | `<button>` for actions; `<a href="/path">` for navigation |
| `<button>` used to navigate (`onclick="location.href=…"`) | Loses open-in-new-tab, middle-click, link semantics | `<a href>` |
| Clickable table row (`<tr onclick>`) with no link inside | Keyboard users cannot open the row | Put an `<a>` in the primary cell; optionally stretch its hit area with a pseudo-element |
| Whole card clickable via JS with nested buttons inside | Nested interactive content; unpredictable click targets | One link on the card title with a stretched `::after`; secondary buttons positioned above it with `position: relative; z-index: 1` |
| Button inside a link or link inside a button | Invalid HTML; screen readers get confused | One interactive element per target |
| `<button>` without `type` inside a form | Defaults to `submit`; "Cancel" submits the form | `type="button"` for non-submit buttons |
| Disabled buttons with no explanation | Users cannot tell why | Keep enabled and show the error on click, or show the reason next to it. See part 18 |
| Custom dropdown built from `div`s | No keyboard, no screen reader support | Native `<select>`; for searchable, a tested combobox (Headless UI, Radix, React Aria, or the WAI-ARIA combobox pattern) |
| Custom checkbox/radio hiding the native input with `display: none` | Input removed from the accessibility tree | Keep the native input; style it with `appearance: none` and pseudo-elements, or visually hide it with a `.sr-only` class and style the label |
| Toggle switch as a `div` | No state, no keyboard | `<button role="switch" aria-checked="true">` or `<input type="checkbox" role="switch">` |
| Accordion headers as `div`s with click handlers | No keyboard | `<details><summary>`, or `<button aria-expanded aria-controls>` inside a heading |
| Tabs as `div`s | No arrow-key support, no state | WAI-ARIA tabs pattern (`role="tablist"`, `role="tab"`, `aria-selected`, arrow keys) or a library that implements it; for 2 sections, just use headings |
| Drag-and-drop as the only way to reorder or upload | Keyboard and switch users blocked (WCAG 2.5.7) | Also offer "Move up/Move down" buttons or a file input |
| Hover-only menus or actions | Unreachable by keyboard and touch | Reveal on `:focus-within` too, or always visible |
| Swipe-only gestures (swipe to delete) | Unreachable without touch | Visible button alternative |
| Long-press or double-click as the only trigger | Hidden and hard to perform | Single click/tap on a visible control |

```html
<!-- Banned -->
<div class="btn btn-primary" onclick="save()" role="button" aria-label="Save button">Save</div>

<!-- Use -->
<button type="button" class="btn btn-primary" onclick="save()">Save</button>
```

## 27.3 Focus

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `outline: none` / `outline: 0` with no replacement | Keyboard users lose their place; the most common generated CSS failure | `:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }` |
| Tailwind `focus:outline-none` with no `focus-visible:ring` | shadcn/Tailwind habit, ring removed when restyling | `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[color:var(--color-focus)]`, or keep the ring classes |
| Bootstrap `.btn:focus { box-shadow: none }` override | Removes Bootstrap's only focus indicator | Keep it, or set `$btn-focus-box-shadow` in Sass to a token-based ring |
| Focus ring using `box-shadow` only | Hidden in Windows High Contrast / forced colours | `outline` (can be transparent plus `box-shadow`, so forced colours still draw it) |
| Focus ring colour below 3:1 against the background | Invisible indicator (WCAG 1.4.11, 2.4.13) | Focus token checked at 3:1 against every surface it appears on |
| Focus ring clipped by `overflow: hidden` on a parent | Ring cut off | `outline-offset: -2px` inside clipped containers, or remove the overflow clip |
| `:focus` styles that also show on mouse click | Designers then remove focus styles entirely | Style `:focus-visible`, not `:focus` |
| Focused element hidden under a sticky header | Fails WCAG 2.4.11 | `scroll-padding-top` equal to the header height on `html` |
| Focus lost after an action (row deleted, modal closed, item added) | Focus drops to `<body>`; keyboard user restarts from top | Move focus to a sensible target: the next row, the trigger button, the new item's heading |
| Focus not moved on client-side route change | Screen reader users are not told the page changed | On route change, focus the new page `<h1>` (with `tabindex="-1"`) or a route announcer |
| Visual order differs from DOM order (CSS `order`, `flex-direction: row-reverse`, grid placement) | Tab order jumps around | Change the DOM order to match the visual order |
| Off-screen menus still focusable when closed | Tab disappears into hidden content | `hidden`, `display: none`, or `inert` on closed panels |

```css
/* Banned */
*:focus { outline: none; }
button:focus { outline: 0; box-shadow: none; }

/* Use */
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
html { scroll-padding-top: var(--header-height); }
```

## 27.4 Dialogs, drawers and focus traps

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Modal built as a `div` with a backdrop and no focus handling | Tab walks behind the modal | Native `<dialog>` with `showModal()`; it handles focus containment, Escape and `inert` background |
| No Escape to close | Keyboard users are stuck | Escape closes every non-critical dialog |
| Focus not moved into the dialog on open | Screen reader keeps reading the page | Focus the first field, or the dialog heading for read-only dialogs; for destructive confirm, focus Cancel |
| Focus not returned to the trigger on close | User loses place | Store the trigger and call `.focus()` on close (native `<dialog>` does this) |
| Focus trap in a non-modal element (a trap in a sidebar, a cookie banner) | Keyboard user cannot leave | Trap focus only in modal dialogs. Banners and drawers that are not modal do not trap |
| No accessible name on the dialog | Screen reader says "dialog" only | `aria-labelledby` pointing to the dialog heading |
| Background still scrollable and readable by screen reader | Content behind leaks through | `<dialog>` modal, or `inert` on the rest of the page plus `overflow: hidden` on body |
| Close button is an unlabeled "×" character | Read as "times" or "multiplication" | `<button aria-label="Close">` with an SVG icon, plus a visible "Cancel" button. See part 21 |
| Toast that steals focus | Interrupts typing | Toasts never take focus; announce via a live region |
| Toast with an action (Undo) that disappears before a keyboard user reaches it | Unreachable action (WCAG 2.2.1) | Keep action toasts for 8 s minimum; pause on hover and focus; or no timeout for toasts with actions |

## 27.5 Keyboard navigation

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Feature works only with a mouse (drag, hover, click on canvas) | Mouse-first generation | Every action reachable with Tab, Enter, Space, Escape, arrow keys where the pattern needs them |
| Custom keyboard shortcuts on single letters with no way to turn off | Conflicts with screen reader keys (WCAG 2.1.4) | Modifier-based shortcuts (Ctrl/Cmd + key), or a setting to disable them |
| Keyboard shortcuts not listed anywhere | Hidden feature | A "Keyboard shortcuts" list reachable from the help menu or `?` |
| Keyboard trap in embedded widget (map, rich text editor, video player) | Tab cannot leave | Test Tab and Shift+Tab through every embed; document the escape key if the widget needs Tab internally |
| POS screen that requires a mouse for every sale | Cashiers use keyboards and barcode scanners | Keyboard flow: scan or type SKU, Enter to add, a key to pay, Enter to confirm |
| Arrow keys scroll the page inside a menu | Menu pattern not implemented | Arrow keys move between menu items; Home/End jump to first/last |
| Map (Leaflet, Google Maps) with no keyboard or list alternative | Precinct or office locations unreachable | Provide a text list of locations with addresses next to or below the map. See part 20 |

## 27.6 Skip links and landmarks

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| No skip link on a site with a long header nav | Keyboard users tab through 20+ links on every page | `<a class="skip-link" href="#main">Skip to content</a>` as the first focusable element, visible on focus |
| Skip link that is permanently invisible (`display: none`) | Never usable | Visually hidden until `:focus`, then shown at top left |
| Skip link target without `id` or not focusable | Link does nothing | `<main id="main" tabindex="-1">` |
| No `<main>` | Screen reader landmark navigation fails | One `<main>` per page |
| Everything inside `<div id="app">` with no landmarks | Framework root with no structure | `<header>`, `<nav>`, `<main>`, `<footer>` inside the root. See part 28 |
| Multiple `<nav>` elements with no names | "navigation, navigation, navigation" | `aria-label="Primary"`, `aria-label="Breadcrumb"`, `aria-label="Footer"` |
| Several `<main>` elements, or `<main>` inside `<article>` | Invalid landmark structure | Exactly one visible `<main>` |
| `<section>` used as a generic wrapper everywhere | Unnamed sections are not landmarks and add noise | `<section>` only with a heading; otherwise `<div>` |
| `<aside>` used for a layout column that is the main content | Wrong landmark | `<aside>` only for complementary content |

```html
<!-- Use -->
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header>…<nav aria-label="Primary">…</nav></header>
  <main id="main" tabindex="-1">…</main>
  <footer>…</footer>
</body>
```

```css
.skip-link { position: absolute; left: 0.5rem; top: -3rem; padding: 0.5rem 0.75rem;
  background: var(--color-surface); color: var(--color-text); z-index: var(--z-skip); }
.skip-link:focus { top: 0.5rem; }
```

## 27.7 Headings

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Multiple `<h1>` per page (logo is `h1`, hero is `h1`, section titles are `h1`) | Heading picked by visual size | One `<h1>` naming the page |
| Skipped levels (`h1` then `h4`) | Heading chosen for font size | Levels follow structure (h1, h2, h3); size set by CSS classes |
| Headings used for styling non-headings (a price or a tagline in `<h2>`) | Pollutes the heading outline | `<p>` with a class |
| Section titles styled as headings but coded as `<div class="title">` or `<p class="font-bold text-xl">` | Invisible to heading navigation | Real `<h2>`/`<h3>` |
| Card titles all `<h3>` with no `<h2>` above them | Broken outline | `<h2>` for the section, `<h3>` for cards inside it |
| Empty headings or headings containing only an icon | Screen reader reads nothing | Text in every heading |
| Visually hidden `<h1>` stuffed with keywords | SEO trick | A real, visible `<h1>` that names the page |
| Dashboard with no headings, only cards | Screen reader users cannot jump between regions | `<h2>` per region (can be visually small) |

## 27.8 Forms

Form layout and copy are in part 17. This section covers what assistive technology needs.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Missing labels (input with only a placeholder) | Placeholder disappears on typing; not reliably read as a name | `<label for="id">` visible above the field |
| Floating labels built with `placeholder=" "` hacks | Fragile; label shrinks under the minimum size | Static label above. See part 17 |
| Label not connected (`<label>Name</label><input>` with no `for`/`id`) | Clicking the label does nothing; no name | `for` matches `id`, or wrap the input in the `<label>` |
| Asterisk without legend | "star" read aloud, meaning unclear | "* Required" legend at the top of the form, plus `required` on the input; or mark optional fields "(optional)" instead |
| Required fields marked only in red | Colour-only meaning | Text marker and `required` attribute |
| Help text not connected | Screen reader misses format hints | `aria-describedby="field-hint"` on the input |
| Errors shown only as a red border | Colour-only; not announced | Text error below the field, `aria-invalid="true"`, and `aria-describedby` pointing to the error |
| Errors not announced on submit | Screen reader user hears nothing | On submit failure: focus an error summary at the top (`role="alert"` or focused heading) that links to each field; or focus the first invalid field |
| Error summary without links | User must hunt for fields | Each summary item is `<a href="#field-id">` |
| Inline validation announcing on every keystroke | Screen reader chatter | Validate on blur or submit; announce once |
| Radio group without `<fieldset>` and `<legend>` | Options read without the question | `<fieldset><legend>Sex</legend>…</fieldset>` |
| Date entered via three unlabeled selects | "combo box, combo box, combo box" | One labeled group with `<legend>Date of birth</legend>` and labels "Day", "Month", "Year"; or one text input with format hint |
| Missing `autocomplete` attributes | Users with motor or memory difficulties retype everything (WCAG 1.3.5) | `autocomplete="name"`, `email`, `tel`, `street-address`, `postal-code`, `one-time-code`, `current-password`, `new-password`. See part 17 |
| Session timeout on long forms with no warning | Data lost (WCAG 2.2.1) | Warn 2 minutes before timeout with an option to extend; save drafts |
| CAPTCHA with no alternative | Blocks blind users | Invisible or checkbox challenge with audio alternative, or rate limiting and a honeypot field |
| Paste blocked on password or OTP fields | Blocks password managers (WCAG 3.3.8) | Allow paste |
| OTP split into 6 separate inputs without labels | Six unlabeled boxes | One `<input inputmode="numeric" autocomplete="one-time-code" maxlength="6">` styled as boxes if needed |
| Asking for the same info twice in one flow | Fails WCAG 3.3.7 redundant entry | Pre-fill or offer "Same as above" |

```html
<!-- Use -->
<label for="mobile">Mobile number</label>
<p id="mobile-hint" class="hint">Format: 09XX XXX XXXX</p>
<input id="mobile" name="mobile" type="tel" inputmode="tel" autocomplete="tel"
  aria-describedby="mobile-hint mobile-error" aria-invalid="true" required>
<p id="mobile-error" class="error">Enter an 11-digit mobile number starting with 09.</p>
```

## 27.9 Screen reader text and live regions

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| No `.sr-only` utility; hidden text done with `display: none` | Hidden from everyone, including screen readers | `.sr-only` class (clip pattern) for text that only screen readers need; Tailwind `sr-only`; Bootstrap `visually-hidden` |
| "Read more" / "Click here" / "View" links repeated 10 times | Link list reads "Read more, Read more…" (WCAG 2.4.4) | Specific text ("Read the 12 May advisory"), or add `.sr-only` context: `View<span class="sr-only"> receipt 000123</span>` |
| Status changes not announced (saved, item added to cart, filter results updated) | Silent UI for screen reader users | `role="status"` (polite) live region with short text: "Saved.", "3 results." |
| `aria-live="assertive"` on everything | Interrupts constantly | `polite` for status; `assertive` / `role="alert"` only for errors that block the task |
| Live region added to the DOM at the same time as its text | Many screen readers miss it | Render the empty live region on page load; change its text later |
| Toast library with no live region | Toast is visual only | Toast container is a `role="status"` region; error toasts `role="alert"` |
| Loading spinner with no text | Screen reader users do not know it is loading | `<span class="sr-only">Loading</span>` inside the spinner, or `aria-busy="true"` on the region being loaded |
| Icon with visible meaning but no text alternative (warning triangle next to a field) | Meaning lost | `.sr-only` text ("Warning:") or `aria-label` on the icon's wrapper; decorative duplicates get `aria-hidden` |
| Decorative icons and emoji read aloud ("rocket, sparkles") | Noise | `aria-hidden="true"` on decorative SVG; no emoji in UI. See part 26 |
| Price or peso amounts read incorrectly (₱1.2k read as "peso one point two k") | Shorthand confuses | Full amount in text, or `.sr-only` full value next to the abbreviation |
| Dates like "05/06/2025" | Ambiguous DD/MM vs MM/DD, spoken as numbers | Write "5 June 2025" or use `<time datetime="2025-06-05">5 June 2025</time>`. See part 04 |

```css
/* Use */
.sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}
```

## 27.10 Colour and contrast

Palette rules are in part 12. These are the pass/fail numbers.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Grey body text on white (`text-gray-400`, `#9ca3af` on `#fff`, about 2.5:1) | "Subtle" AI styling fails | Body and small text at 4.5:1 or more |
| Grey text on grey card (`text-slate-500` on `bg-slate-100`) | Double-muted | Check the actual pair; use the muted-text token that passes 4.5:1 on that surface |
| Placeholder text below 4.5:1 carrying needed info | Hint unreadable | Put hints in helper text, not placeholders |
| White text on a mid-tone brand button (white on light green/orange/sky) | Brand colour chosen without checking | Button text/background pair from DESIGN.md checked at 4.5:1 |
| Text on images or gradients | Contrast varies across the image | Solid background behind text; if on a photo, a solid scrim token checked at the worst point |
| Input borders and icons below 3:1 | Fields invisible to low-vision users (WCAG 1.4.11) | Field borders, focus rings, icons that carry meaning at 3:1 or more |
| Disabled text used for normal content | Disabled colour is exempt only for disabled controls | Normal text token |
| Colour-only meaning (red/green for paid/unpaid, coloured dots only, red border only) | Colour-blind users miss it (WCAG 1.4.1) | Text label or icon plus colour: "Paid", "Unpaid" |
| Links in body text distinguished only by colour | Fails 1.4.1 unless 3:1 against surrounding text plus a non-colour cue on hover/focus | Underline links in body text. See part 13 |
| Charts that rely on colour alone | Series indistinguishable | Direct labels, patterns or markers, plus a data table. See part 20 |
| Dark mode with the same accent colour as light mode | Accent fails on dark surfaces | Separate dark-mode token values, each checked |
| No support for forced colours (Windows High Contrast) | Custom controls disappear | Use real borders/outlines (not only backgrounds/shadows); test with `forced-colors: active` |

## 27.11 Target size and touch

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Tiny icon buttons (16x16 close X, 20x20 row actions) | Fails WCAG 2.5.8 (24x24 minimum) | 24x24 CSS px minimum on desktop; 44x44 on touch layouts |
| Tiny gray "Forgot password?" link | Hard to hit and read | Normal-size link, 44 px tall hit area on mobile. See part 23 |
| Adjacent small targets with no spacing (edit and delete icons touching) | Mis-taps, especially on delete | 8 px gap minimum; destructive action separated or in a menu |
| Checkbox and radio only 12–14 px with no clickable label | Hard to tap | Label wraps the input so the whole row is the target |
| Links in dense text on mobile with no line spacing | Mis-taps | Line-height 1.5 or more; lists for link groups |
| Pagination numbers 24 px wide on mobile | Hard to tap | 44x44 on mobile, or Previous/Next buttons only |

## 27.12 Motion, time and flashing

Motion rules are in part 25.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| No `prefers-reduced-motion` support | Vestibular triggers | Global reduced-motion block. See part 25 |
| Autoplay carousel, marquee or video with no pause | Fails WCAG 2.2.2 | No autoplay, or a keyboard-reachable pause control |
| Anything flashing more than 3 times per second | Seizure risk (WCAG 2.3.1) | Never |
| Auto-refreshing page that resets scroll and focus | Screen reader loses place | Update data in place; announce "Updated" politely; never reload the page |
| Timed OTP with no resend or extension | Users with slower input fail | Show the time left in text, allow resend after 30–60 s |
| Auto-logout without warning | Data loss | Warning dialog 2 minutes before, with "Stay signed in" |

## 27.13 Zoom, reflow and text spacing

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `<meta name="viewport" content="…, maximum-scale=1, user-scalable=no">` | Blocks pinch zoom (WCAG 1.4.4); copied from app templates | `<meta name="viewport" content="width=device-width, initial-scale=1">` |
| `maximum-scale=1` added to stop iOS input zoom | Wrong fix | Use 16 px (1rem) input font size instead. See part 15 |
| Font sizes in `px` locked on `html` (`html { font-size: 14px }`) | Ignores user browser font settings | `html` font size left at 100%; sizes in `rem` |
| Layout breaks at 200% zoom or 320 px width | Fails WCAG 1.4.10 reflow | Test at 320 px wide and 400% zoom on 1280 px; no horizontal scroll except data tables and maps |
| Fixed-height text containers | Text clips when users increase spacing (WCAG 1.4.12) | `min-height`, not `height`, on anything holding text |
| Text in images (banners, announcements as JPEG) | Cannot zoom cleanly or be read aloud | Real text in HTML. See part 26 |
| Truncated labels with no way to see the full text | Zoomed users lose content | Wrap text; if truncating, full text available via `title` plus an accessible expanded view |

## 27.14 Language

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `<html>` with no `lang` | Screen reader guesses pronunciation | `<html lang="en">` for English pages |
| `lang="en"` on a page written in Filipino | Screen reader reads Tagalog with English phonetics | `<html lang="fil">` for Filipino pages (`tl` is also valid; pick one and stay consistent) |
| Mixed English and Filipino paragraphs with no `lang` switch | Wrong pronunciation for whole paragraphs | `lang="fil"` on Filipino blocks inside an English page, and the reverse. Do not tag single Taglish words |
| Ilocano, Cebuano or other regional content untagged | Same issue | `lang="ilo"` (Ilocano), `lang="ceb"` (Cebuano), `lang="hil"` (Hiligaynon) on those blocks |
| Language switcher using flags | Flags are countries, not languages; Windows shows letters | Language names in their own language: "English", "Filipino", "Ilokano" |
| `lang` left as `en` in a Next.js/Vite template after translating | Template default | Set `lang` in the root layout from the page locale |

## 27.15 Tables

Table design is in part 19. These rules keep tables readable by assistive technology.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Data table built from `div` grid | No row/column relationships for screen readers | `<table>` with `<thead>`, `<tbody>`, `<th scope="col">` |
| No row headers in a record table | Cells read without context | First cell as `<th scope="row">` when it identifies the row |
| No `<caption>` | Table purpose unannounced | `<caption>` naming the table (can be visually hidden) |
| Sortable columns with no state | Sort direction unknown | `aria-sort="ascending"` on the sorted `<th>`; sort control is a `<button>` inside the `<th>` |
| Layout tables for page structure | Screen readers announce rows and columns of layout | CSS grid/flex. Tables for data only |
| Checkbox column with no labels | "checkbox, checkbox" | `aria-label="Select receipt 000123"` on each; header checkbox `aria-label="Select all"` |
| Horizontal scroll container not focusable | Keyboard users cannot scroll it | `tabindex="0"`, `role="region"` and `aria-label` on the scroll wrapper |

## 27.16 Images and media

What to write in alt text is in part 26.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `img` without `alt` | File name read aloud | Descriptive `alt`, or `alt=""` for decoration |
| Decorative image with descriptive alt | Clutter | `alt=""` (not missing, empty) |
| CSS background image carrying content (a photo of the official, a map) | Invisible to screen readers | `<img>` with alt |
| Inline SVG with meaning but no name | Silent | `role="img"` plus `aria-label`, or `<title>` referenced by `aria-labelledby` |
| Complex image (infographic, org chart, flowchart) with one-line alt | Content lost | Short alt plus the full content as HTML text or list nearby |
| Video with no captions; audio with no transcript | Deaf and hard-of-hearing users excluded | Captions (`<track kind="captions">`) and a transcript link |
| PDF-only announcements, forms and memos on LGU/school sites | Scanned PDFs are images; unreadable | HTML page with the content; tagged PDF as the download |

## 27.17 Testing that an agent can run

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Ensured accessibility" claimed in the report with no test | False claim. See part 07 | Report the checks run and their results |
| Only Lighthouse score quoted | Automated tools catch a fraction of issues | Automated scan plus the manual keyboard pass below |
| No automated check in the project | Regressions ship | `axe-core` via `@axe-core/playwright` or `jest-axe` on key pages; `eslint-plugin-jsx-a11y` for React |
| Keyboard not tested | Most generated failures are keyboard failures | Unplug the mouse: Tab through the page, open and close every menu and dialog, submit every form |
| Screen reader not tested | ARIA errors go unnoticed | Quick pass with NVDA (Windows), VoiceOver (macOS/iOS) or TalkBack (Android): headings list, landmarks list, one form |
| Zoom not tested | Reflow bugs | Browser zoom 200% and 400%; viewport 320 px |
| Contrast not measured | "Looks fine" on a bright monitor | Measure each text/background token pair; record ratios in DESIGN.md |

## 27.18 Check
- [ ] Every clickable thing is a `<button>` or `<a href>`; no `div`/`span` click handlers, no `href="#"`.
- [ ] No redundant roles on native landmarks; no `role="button"` on non-buttons.
- [ ] No positive `tabindex`; `tabindex="0"` only on custom widgets and scroll regions.
- [ ] No `aria-hidden` on focusable elements.
- [ ] Accessible names start with the visible label text.
- [ ] No accessibility overlay widget.
- [ ] `:focus-visible` outline present on every interactive element, 3:1 contrast, not clipped.
- [ ] No `outline: none` / `focus:outline-none` without a replacement.
- [ ] `scroll-padding-top` set when the header is sticky.
- [ ] Focus moves correctly after delete, close, add and route change.
- [ ] DOM order matches visual order.
- [ ] Modals use `<dialog>` or an equivalent: focus in, Escape closes, focus returns, background inert.
- [ ] Focus traps only in modal dialogs.
- [ ] Toasts do not take focus; action toasts stay 8 s+ and pause on hover/focus.
- [ ] Every action works with keyboard alone; no hover-only, drag-only, or swipe-only actions.
- [ ] Single-key shortcuts can be turned off or use a modifier.
- [ ] Skip link is the first focusable element and becomes visible on focus.
- [ ] One `<main>`; `<header>`, `<nav>`, `<footer>` present; multiple navs named.
- [ ] One `<h1>`; heading levels do not skip; visual titles are real headings.
- [ ] Every input has a connected `<label>`; placeholders are not labels.
- [ ] Hints and errors linked with `aria-describedby`; invalid fields have `aria-invalid="true"`.
- [ ] Submit errors produce a focused, linked error summary or focus the first invalid field.
- [ ] Radio and checkbox groups use `<fieldset>` and `<legend>`.
- [ ] `autocomplete` set on personal-data fields; paste allowed on password and OTP.
- [ ] Status messages use a pre-rendered `role="status"` region; errors use `role="alert"`.
- [ ] Link text makes sense out of context.
- [ ] Body text 4.5:1; large text and UI graphics 3:1; checked in light and dark.
- [ ] No colour-only meaning in status, required fields, errors, links or charts.
- [ ] Targets 24x24 minimum, 44x44 on touch; 8 px between adjacent small targets.
- [ ] Reduced motion respected; no autoplay without pause; nothing flashes.
- [ ] Viewport meta allows zoom; no `maximum-scale` or `user-scalable=no`.
- [ ] Layout reflows at 320 px and 400% zoom; text containers use `min-height`.
- [ ] `<html lang>` matches the page language (`en` or `fil`); mixed blocks tagged.
- [ ] Language switcher shows language names, not flags.
- [ ] Data tables use `<table>`, `<th scope>`, `<caption>`, and `aria-sort` when sortable.
- [ ] All images have `alt`; meaningful SVGs have a name; decorative ones are hidden.
- [ ] Videos have captions; announcements exist as HTML, not only as PDF or image.
- [ ] Session timeouts warn 2 minutes ahead and can be extended.
- [ ] axe (or equivalent) runs with zero violations on key pages.
- [ ] Manual keyboard pass and one screen reader pass done, and the report says which.
