---
part: 14
title: Layout and spacing
covers: cards everywhere, equal grids, centering, max-widths, spacing scale, gaps, section padding, alignment, grid systems, whitespace, density, sticky elements, scroll contexts, sidebar and main shell, above the fold, visual hierarchy, symmetry, template rhythms
---

# 14 — Layout and spacing

Read when: building any page shell, section, grid, dashboard layout, form layout, or setting spacing tokens.

Guidance: DESIGN.md and the brief override this part.

## 14.1 Cards everywhere

The most common generated layout wraps every piece of content in a white box with a shadow and a radius. Cards are for items a user can pick up as a unit: a product, a person, a file. Not for sections.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Everything in a card with shadow (original 3.1) | No hierarchy. Page becomes a grid of identical boxes. | Content on the page surface. Separate sections with headings and spacing. Dividers (1px border token) between list items. Cards only for repeatable, self-contained items. |
| Cards inside cards (original 2.1) | Nesting destroys hierarchy. Double borders, double padding. | Single level. Inner groups become a heading plus a list, or a `<dl>`, inside the one card. |
| Every section of a settings page in its own card | Admin template look. Padding doubles. | One column of sections with `h2` headings and a 1px divider between them. |
| Form inside a card inside a page with a gray background | Three nested surfaces for one form. | Form on the page surface, max 640px wide. See part 17. |
| Table inside a card with shadow (original 3.4) | Adds a frame and padding that steals width. | Table directly on the surface with a 1px border or no border. See part 19. |
| Every section wrapped in `div.card` (original 7.1) | Code-level version of the same tell. | Semantic `<section>` on the surface. HTML: see part 28. |
| Identical card grid for everything (original 2.1): stats, feeds, profiles, settings | One component used for all content types. | Table for tabular data, list for feeds, `<dl>` for metadata, cards only for browsable items. |
| Icon + title + vague sentence cards (original 3.1) | Feature-card template. Says nothing. | For tools: skip. For marketing: screenshot or real data with one factual line. Copy: see part 05. |
| Cards with 32px padding showing one line of text | Box is bigger than its content. | Padding 12–16px for compact cards, 20–24px for content cards. Or no card. |
| Cards with equal height forced by `h-full`, leaving large blank areas | Grid looks tidy but cards are half empty. | Let height follow content in lists. Equal height only for product grids where images align. |
| Card for a single number | See part 19 and part 22. | Inline stat row or `<dl>`. |
| Shadow + border + radius + background tint on the same card | Four surface signals. | One: border or subtle shadow. Radius from tokens. CSS: see part 11. |
| Hover lift on cards | See part 25. | Background change or none. |
| Masonry for non-image content (original 3.1) | Pinterest layout for text. Reading order unclear. | List or table. Masonry only for image galleries. |

## 14.2 Grids and columns

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| 3-column equal card grid for stats (original 3.1) | Default template row. | Inline stat row, `<dl>`, or compact table. |
| `grid-cols-3` for every set of items, regardless of count | 4 items leave one orphan. 5 items leave two. | Pick columns from item count and content width. `repeat(auto-fill, minmax(16rem, 1fr))` for browsable items. |
| Always 3 features, 3 plans, 3 testimonials, 3 steps | Rule-of-three layout. Real content rarely comes in threes. | Show the actual number of items. 2 or 5 is fine. |
| Bento grid on a site with no visual content | Trend layout. See part 10. | Plain list or two-column grid. |
| 12-column grid system imported to lay out a 3-page site | Bootstrap reflex. `col-md-4` everywhere. | CSS grid with named areas or 2–3 explicit columns. |
| Nested `.row > .col > .row > .col` 4 levels deep | Bootstrap nesting. Hard to change. | Flatten. One grid per layout region. Use `gap`. |
| Two-column layout forced on mobile (original 3.1) | Squeezed columns at 390px. | Single column under about 640px. See part 15. |
| Uneven column gutters because of margin on children | Gaps drift. Last item has an extra margin. | `gap` on the grid or flex container. No margins on children for spacing. |
| Sidebar content column at 50/50 with main | Secondary info gets equal weight. | Main 2/3 or more. Aside 280–320px fixed. |
| Grid that stretches cards to 600px wide on 1920px screens | `1fr` columns with no max. | Container max-width (14.4) or `minmax(16rem, 22rem)` tracks. |
| Image left / text right, then text left / image right, repeated 4 times (z-pattern) | Marketing template rhythm. See part 10. | One layout for all feature rows, or a list. Alternate only if the content requires it. |
| Grid-template-areas that reorder content visually but not in DOM | Tab order and reading order differ. | Keep DOM order equal to visual order. See part 27. |

## 14.3 Centering

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Centered everything: headings, text, buttons, forms, lists | Landing-page reflex. Every page looks like a hero. | Left-align content in apps. Center only short page-level heroes, auth card, empty state. Text alignment: see part 13. |
| `flex items-center justify-center min-h-screen` wrapper on every page | Content floats mid-screen with empty space above and below. | Content starts at the top below the header. Vertical centering only for auth and single-message pages. |
| Centered dashboard content with 300px empty on each side | Narrow content on wide screens for a data app. | Dashboards fill the available width up to 1440–1600px. |
| Centered table | Table floats. Hard to align with page title. | Table aligned to the content column's left edge. |
| Centered form fields with left-aligned labels outside them | Two alignment axes. | Labels and fields share a left edge. |
| Centered section headings above left-aligned content | Heading does not line up with what it labels. | Align heading with its content. |
| Centered buttons under a left-aligned form | Action detached from form. | Buttons aligned to the form's left edge (or right, one rule for the app). See part 17. |
| Icon centered above a centered heading above centered text, in every card | Feature-card template. | Icon inline with title, or no icon. Left-aligned. |

## 14.4 Max-widths and containers

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Fixed-width centered content under 600px on data apps (original 3.1) | Tables and dashboards cramped on desktop. | Text pages: about 720px (65ch). Forms: 560–640px. Dashboards and tables: 1200–1440px or full width with padding. |
| `max-w-7xl mx-auto` for every page type | One container for text, forms and dashboards. | Container width per page type: `--w-prose`, `--w-form`, `--w-page`, `--w-wide` from DESIGN.md. |
| No max-width at all: text lines 1800px on wide monitors | Unreadable. | Prose max 65ch. Page container max 1440px, centered, with side padding. |
| Full-width table stretched (original 3.4) | 3-column table spanning 1600px. Columns far apart. | Table width follows content. `width: auto` with a max, or container at form width for small tables. |
| Container padding 0 on mobile | Text touches screen edge. | Side padding 16px on mobile, 24px tablet, 32px desktop. Tokens. |
| Different container widths in header, body and footer | Edges do not line up. | Header, main and footer share one container width and padding. |
| Hero container at 1280px, next section at 1152px, next at 960px | Edges jump on scroll. | Two widths max per page: full page container and prose column. |
| Modal forms 900px wide for 3 fields | Wasted width. See part 21. | Modal width follows content: 400–560px for simple forms. |
| Login card 480px with 48px padding for 2 fields | Oversized. | 360–400px card, 24px padding. See part 23. |

## 14.5 Spacing scale

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Random values: 13px, 18px, 22px, 37px margins | No system. | One spacing scale in tokens from DESIGN.md, 4px or 8px base: 4, 8, 12, 16, 24, 32, 48, 64. |
| Arbitrary Tailwind values `mt-[37px]`, `p-[18px]` | Magic numbers. See part 11. | Scale values only. Add a token to config if a new step is needed. |
| Same gap everywhere (`gap-6` on every stack) | No grouping. Related and unrelated items spaced equally. | Proximity: 4–8px within a group (label to input), 16–24px between groups, 32–64px between sections. |
| Inconsistent gaps between identical elements (list items at 12px, 16px, 14px) | Built one component at a time. | One gap token per component type. |
| Margin on both top and bottom of every element | Margins collapse unpredictably. Double gaps inside flex. | Stack with `gap` on the parent, or one-direction margin (`margin-block-start` via a stack/owl rule). |
| Spacing in `em` on components with different font sizes | Gaps change with font size. | `rem` tokens for layout spacing. |
| Padding inside buttons larger than gap between buttons | Buttons look glued yet bloated. | Button group gap 8px. Button padding from part 18. |
| Heading spacing equal above and below | Heading floats. See part 13. | Space above 2–3x space below. |
| Spacers `<div class="h-8"></div>` or `<br><br>` | Layout in markup. | `gap` or margins on the parent layout. |
| Negative margins to fix alignment (`-mt-4`, `-mx-2`) | Patches over a padding mistake. | Remove the extra padding at its source. |

## 14.6 Section padding bloat

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `py-24` / `py-32` on every section | Marketing rhythm. Each section fills a screen with little content. | Marketing sections 48–96px vertical. App sections 24–32px. Size the gap to the content. |
| `py-24` on app pages (settings, lists, dashboards) | User scrolls past empty space to reach data. | App page top padding 24px. Section gap 32px. |
| Same large padding on a section with one sentence and a section with a grid | Padding not linked to content. | Smaller sections get less padding. |
| Hero with `min-h-screen` or `h-screen` on a utility page (original 2.1 oversized hero) | First screen shows only a heading. Oversized hero trope: see part 10. | Content visible above the fold without scrolling. Hero height follows content. |
| 64px between page title and first content | Title detached from its content. | 16–24px below page title. |
| Footer with 96px top padding | Template footer. See part 16. | Footer padding 24–32px. |
| Empty states with 200px vertical padding | Oversized. See part 04. | 32–48px. |
| Mobile keeps desktop section padding | `py-24` on 390px screens = 192px of empty per section. | Reduce section padding by about half under 640px. |

## 14.7 Alignment

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Elements aligned by eye, off by 2–6px | Mixed padding values. | Shared left edge per column. Check with a vertical guide or outline. |
| Icon and text not vertically centered in a row | Baseline mismatch. | `display: flex; align-items: center; gap: 8px` or align icon to the first line's cap height. |
| Page title, table and filters each with different left padding | Three edges. | One content edge per column. |
| Card content aligned differently from section heading above it | Card padding adds an offset. | Align card edge to heading, or indent both consistently. |
| Numbers left-aligned in a column | See part 19. | Right-align numbers. |
| Labels and inputs with mismatched widths in a grid form | Ragged form. | Labels above inputs, single column. Multi-column forms: see part 17. |
| Buttons in dialogs and forms on different sides across the app | No rule. | One placement rule for primary actions app-wide. See part 18. |
| Header logo not aligned with main content edge | Header uses a different container. | Same container and padding as main. |
| Baseline misalignment between side-by-side text of different sizes | Headings and meta text in a row look off. | `align-items: baseline` for rows mixing sizes. |

## 14.8 Whitespace and density

Marketing pages and data apps need different density. Generated output uses marketing density everywhere.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Marketing density in admin tools and POS | Few rows per screen. More scrolling. Cashiers and encoders work fast. | Data apps: table rows 36–44px, cell padding 8–12px, section gap 24px. |
| Admin density on a public barangay or school homepage | Crowded for a general audience. | Public pages: body 16px+, 24–48px between groups, fewer items per row. |
| "Breathing room" around every element | Whitespace used as a style, not grouping. | Whitespace groups related items. Every gap has a purpose: within group small, between groups large. |
| Dashboard with 6+ metric cards (original 3.1) | Low data per pixel. See part 22. | 1–2 key metrics prominent. Rest in a table. |
| Offer a density toggle (compact/comfortable/spacious) nobody asked for | Template settings. | One density set for the app's use. Toggle only when users asked. |
| POS screen with small targets and lots of padding around the grid | Wasted space where the product grid needs it. | Maximise product grid and cart. Targets 44px+. See part 22. |
| Long government forms spread over wide whitespace | Scroll length doubles. | Single column, 16–24px between fields, section headings. See part 17. |
| Empty space filled with decoration (blobs, dots, gradients) | Filling space for its own sake. See part 10. | Leave the space empty or remove it. |

## 14.9 Sticky and fixed elements

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Sticky everything (original 3.1): header, sub-nav, filters, sidebar, CTA bar | Stacked sticky bars eat half the viewport on phones. | Sticky header only. Add sticky table header or sticky action bar only when the content is long and the action is frequent. |
| Sticky header taller than 64px | Takes permanent space. | 56–64px desktop, 48–56px mobile. |
| Sticky header with blur (original 3.2) | See part 16 and part 10. | Solid header. |
| Floating CTA bar on every marketing section | Nagging. | One CTA at the end of the page, plus the header. |
| Floating chat bubble + cookie banner + back-to-top + promo bar | Four fixed elements covering content on mobile. | Max one floating element on mobile. Cookie text: see part 08. |
| Fixed position elements without offsetting anchors | Jump links land under the header. | `scroll-margin-top` equal to header height on anchored headings. |
| Sticky sidebar taller than viewport | Bottom items unreachable. | Sidebar scrolls within itself, or is not sticky. See 14.10. |
| Sticky table header without background | Rows show through the header. | Solid background token on sticky header cells. |
| Sticky "Save" bar on a page with 2 fields | Unneeded. | Normal button after the fields. Sticky save only for long forms. |
| `z-index: 9999` on sticky elements | Stacking wars. See part 11. | z-index scale in tokens (base, dropdown, sticky, overlay, modal, toast). |

## 14.10 Scroll contexts

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Sidebar and main both scrollable (original 3.1) | Two scrollbars. Scroll wheel moves the wrong one. | One scroll context: the page. Sidebar collapses on mobile. |
| Full-height sidebar with its own scroll (original 3.1) | Nested scroll on short lists. | Sidebar scrolls with page or collapses. Inner scroll only when the nav list is taller than the viewport. |
| `h-screen overflow-hidden` on body with inner `overflow-y-auto` main | Breaks browser find, pull-to-refresh, mobile address bar collapse. | Let the document scroll. Use `position: sticky` for the sidebar. |
| Scrollable card inside a scrollable page | Scroll traps. | Show all content, or paginate. Inner scroll only for chat logs and code. |
| Horizontal scroll containers with no visible cue | Users do not know more exists. | Visible partial item at the edge, scroll shadow, or arrows. Tables: see part 19. |
| Modal with its own scroll inside a scrolling page | Background scrolls behind. See part 21. | Lock body scroll while open. Long content goes to a page. |
| Tabs that reset scroll position to top on every switch | Loses place. | Keep scroll position per tab, or place tabs so the content starts in view. |
| `overflow: hidden` on body to fix horizontal scroll | Hides the bug. See part 11 and part 15. | Find the overflowing element. |
| Custom thin scrollbars that are hard to grab | 4px scrollbars on desktop. | Default scrollbars, or `scrollbar-width: thin` only on small inner panels. |
| Scroll snap on long content pages | Page jumps, fights the user. | No scroll snap on vertical page content. Only on carousels if at all. |

## 14.11 App shell: sidebar and main

Navigation behaviour in the sidebar is in part 16. This section covers the shell geometry.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Sidebar wider than 280px (original 3.7) | Takes width from content. | 220–260px. |
| Sidebar + top header + sub-header + breadcrumb bar + page header | Five bands before content. | Sidebar + one header row. Page title and actions in the same row. |
| Header row with title on left and 5 buttons on right | Crowded. | One primary action. Others in a menu. See part 18. |
| Main area padding 48px on all sides | Marketing padding in an app. | 16–24px. |
| Right-side panel always open with nothing in it | Template three-panel layout. | Open detail panels on selection. Close by default. |
| Shell that differs page to page (sidebar on some, not others) | Built page by page. | One shell for the logged-in app. Auth pages without shell. |
| Content area background different from sidebar and header, plus card backgrounds | Three surface colors plus cards. | Two surfaces max: page and raised. Tokens from DESIGN.md. Color: see part 12. |
| Footer inside the app shell with copyright and links | Marketing footer in a tool. | No footer in logged-in app shells, or a single line in the sidebar. |

## 14.12 Above the fold and first screen

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Oversized hero on a utility tool (original 2.1) | 100vh hero before any function. | The first screen shows the tool: search, form, table, or key numbers. |
| Barangay/LGU homepage with a full-screen photo slider first | Services and notices pushed below. | First screen: office name, top 3–6 services (clearance, certificate request, permits), latest notice, contact number. Page type: see part 24. |
| School homepage hero image with "Welcome to our school" and no dates | No useful info in first screen. | Enrollment dates, announcements, contact, map link up top. |
| Dashboard first screen is a greeting and a chart | See part 22. | Items that need action first (pending approvals, low stock, failed payments). |
| Precinct finder with the search box below a hero | Main task hidden. | Search form in the first screen at 390px. |
| "Scroll down" chevron animation | Admits the first screen has nothing. | Remove. Put content in the first screen. |
| Carousel as the first element | Users see slide 1 only. Auto-rotation distracts. | One static message, or a list of the items. Motion: see part 25. |

## 14.13 Visual hierarchy

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Every element has equal visual weight (all cards, all bold, all accent) | No starting point. | One primary element per screen: the page title or the main task. Secondary items smaller and quieter. |
| Multiple primary buttons in one view | See part 18. | One primary per view. |
| Accent color on 5+ elements per screen | See part 12. | One accent use per viewport where possible. |
| Decorative elements heavier than content (icons, illustrations larger than text) | Decoration wins attention. | Content first. Icons at text size. See part 26. |
| Page title smaller than a card title | Scale mismatch. | Page title is the largest text on app pages. |
| Metadata (dates, authors, IDs) same weight as main text | Hard to scan. | Metadata smaller size, muted token. |
| Secondary actions styled as bright pills | Compete with primary. | Text links or subtle buttons. |
| Status shown only by a card's colored top border | Weak, color-only. See part 27. | Status text label plus color. |

## 14.14 Symmetry and template rhythm

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Perfectly symmetric pages: centered hero, 3 cards, centered CTA, 4-col footer | The default generated landing page. Hero + 3 features + CTA: see part 10. | Order sections by what the visitor needs. Allow uneven groupings. |
| Full-width alternating background sections (original 3.1, 2.1) | Marketing rhythm: white, gray, white, gray, dark. | One consistent background. Separate sections with headings and spacing. |
| Every section: centered heading + centered subhead + grid | Same section template repeated 6 times. | Vary structure by content: a table, a list, a paragraph, a form. |
| Decorative dividers between every section (wave SVG, gradient line) | See part 10. | Whitespace or a 1px border token. |
| Section order copied from a template: hero, logos, features, testimonials, pricing, FAQ, CTA | Not based on the client's content. | Sections the client has real content for. Remove sections filled with placeholder. |
| Every section exactly one screen tall | Slide-deck layout on the web. | Height follows content. |
| Mirror layout on about/team pages (photo left, text right, then flipped) | Z-pattern template. | Consistent layout. Grid of people or a list. |

## 14.15 Layout by page and component type

Specific page-type layouts live in part 24. These rows cover shared structure.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| List page with filters in a left sidebar card, table in a right card, pagination in a third card | Card nesting for a standard list. | Filter bar above the table in one row. Table on surface. Pagination below. |
| Detail page as a grid of small cards (one per field) | Card per field. | Two-column `<dl>` for fields, sections with headings. |
| Edit page in a modal (original 3.1 modal for everything) | Cramped. No URL. See part 21. | Dedicated edit page or inline editing. Modals for destructive confirms only. |
| Settings split into 8 tabs with 2 fields each | Tabs for small content. See part 16. | One page with section headings. |
| Profile page with cover photo, avatar overlap, stats row, tabs | Social-network template for a school or admin profile. | Name, role, contact fields, recent items. See part 23. |
| Report page with charts in a 2x2 grid of equal cards | Charts sized by grid, not data. | Charts sized to their data. Table below for exact values. See part 20. |
| Receipt/invoice layout copied from a dashboard card | Receipts need print layout. | Single column, fixed widths for 58mm/80mm thermal or A4 print. `@media print` styles. BIR wording: see part 09. |
| Public notice pages with sidebar widgets (calendar, weather, social feed) | Portal-template clutter. | Notice text in a prose column. Related notices listed below. |
| Official directory as cards with large photos and hover effects | Template team grid. | Table or list: name, position, office, contact. Photo optional and small. |

## 14.16 Tailwind and Bootstrap specifics

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `container mx-auto px-4 py-24` on every section | Template section wrapper. | Section padding from tokens, sized to content (14.6). |
| `grid grid-cols-1 md:grid-cols-3 gap-8` for every group | Default 3-col grid. | Columns chosen by content count and width. `auto-fill` with `minmax`. |
| `min-h-screen flex items-center justify-center` on app pages | Centered floating content. | Normal flow from top. |
| `space-y-8` on every stack | Equal spacing everywhere. | Varied gaps for grouping (14.5). |
| `rounded-2xl shadow-xl p-8 bg-white` card on every block | Card-everything. | Surface layout. Card class used only for items. |
| `max-w-7xl` on prose pages | Wide text. | `max-w-prose` for reading. |
| `sticky top-0 z-50 backdrop-blur` header | Frosted sticky header. | `sticky top-0` with solid surface token, z-index from scale. |
| Bootstrap `container` > `row` > `col-md-4` x3 cards with `shadow-lg` | Bootstrap feature-card template. | CSS grid or `row-cols-*` with plain content. Shadows from part 11. |
| Bootstrap `py-5` on every section and `my-5` on every heading | Double vertical space. | Set `$spacer` scale in Sass. Section spacing once on the section. |
| Bootstrap `card` used for every panel in an admin template (AdminLTE look) | Card-everything, template recognisable. | Panels without card chrome. Keep `card` for items. |
| Bootstrap `vh-100` on sections | Full-height sections. | Height follows content. |
| `gap-x-8 gap-y-12` arbitrary combos per grid | Random gaps. | Gap tokens by level (14.5). |

## 14.17 Code: banned vs use

```html
<!-- Banned: card-everything, centered, 3-col equal grid, py-24 on an app page -->
<main class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-indigo-50">
  <div class="container mx-auto px-4 py-24">
    <div class="text-center mb-16">
      <span class="uppercase tracking-widest text-xs text-indigo-600">Overview</span>
      <h1 class="text-6xl font-extrabold">Your Dashboard</h1>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div class="rounded-2xl shadow-xl p-8 bg-white">
        <div class="rounded-2xl shadow p-6 bg-white">
          <p class="text-sm">Total sales</p>
          <p class="text-5xl font-bold">₱128,450</p>
        </div>
      </div>
      <!-- two more identical cards -->
    </div>
  </div>
</main>
```

```html
<!-- Use: page surface, header row, inline stats, table on surface -->
<main class="page">
  <header class="page-header">
    <h1>Sales</h1>
    <a class="btn btn-primary" href="/sales/new">New sale</a>
  </header>

  <dl class="stat-row">
    <div><dt>Today</dt><dd>₱128,450.00</dd></div>
    <div><dt>Transactions</dt><dd>214</dd></div>
  </dl>

  <section>
    <h2>Recent sales</h2>
    <table>…</table>
  </section>
</main>
```

```css
/* Banned: random spacing, margins on children, sticky stack */
.card { margin: 22px 13px 37px; padding: 32px; }
.section { padding: 96px 0; }
.header, .subnav, .filters { position: sticky; top: 0; z-index: 9999; }

/* Use: spacing and width tokens from DESIGN.md */
:root {
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem; --space-4: 1rem;
  --space-6: 1.5rem;  --space-8: 2rem;   --space-12: 3rem;   --space-16: 4rem;
  --w-prose: 65ch; --w-form: 40rem; --w-page: 75rem; --w-wide: 90rem;
  --z-sticky: 10; --z-dropdown: 20; --z-overlay: 30; --z-modal: 40; --z-toast: 50;
}
.page { max-width: var(--w-page); margin-inline: auto; padding: var(--space-6) var(--space-4); display: grid; gap: var(--space-8); }
.page-header { display: flex; align-items: center; justify-content: space-between; gap: var(--space-4); }
.stat-row { display: flex; flex-wrap: wrap; gap: var(--space-8); }
.site-header { position: sticky; top: 0; z-index: var(--z-sticky); background: var(--color-surface); border-bottom: 1px solid var(--color-border); }
h2[id] { scroll-margin-top: 4rem; }
@media (min-width: 64rem) { .page { padding-inline: var(--space-8); } }
```

## 14.18 Check

- [ ] Cards used only for self-contained, repeatable items. No card per section.
- [ ] No cards inside cards.
- [ ] Tables and forms sit on the page surface, not inside shadowed cards.
- [ ] Data shown as table, list or `<dl>` according to its shape, not as identical cards.
- [ ] No 3-column equal grid used by default. Column count follows item count and width.
- [ ] Item counts are real, not padded to 3.
- [ ] No masonry for text content.
- [ ] Single column under about 640px.
- [ ] Grids use `gap`, not child margins.
- [ ] Content left-aligned in apps. Centering limited to auth, empty states, short heroes.
- [ ] No `min-h-screen` centering wrapper on app pages.
- [ ] Container widths set per page type: prose about 65ch, forms 560–640px, dashboards 1200–1440px.
- [ ] Header, main and footer share one container edge.
- [ ] Side padding 16px on mobile at minimum.
- [ ] One spacing scale in tokens. No arbitrary spacing values.
- [ ] Small gaps within groups, larger between groups, largest between sections.
- [ ] No spacer divs or `<br>` for layout. No negative-margin patches.
- [ ] App section padding 24–32px. No `py-24` on app pages.
- [ ] Marketing section padding sized to content, halved on mobile.
- [ ] First screen shows the main task or content, not a greeting or empty hero.
- [ ] No "scroll down" indicators.
- [ ] Density matches use: compact for admin/POS, relaxed for public pages.
- [ ] Max 2 prominent metrics on dashboards. Rest in a table.
- [ ] Only the header is sticky, unless a long table or long form needs one more.
- [ ] Max one floating element on mobile.
- [ ] Anchored headings have `scroll-margin-top`.
- [ ] z-index values come from a token scale. No 9999.
- [ ] One scroll context. Sidebar and main do not both scroll on short content.
- [ ] No `h-screen overflow-hidden` body.
- [ ] Horizontal scroll areas show a visible cue.
- [ ] Sidebar 220–260px. Shell identical across logged-in pages.
- [ ] Max two surface levels: page and raised.
- [ ] One primary element per screen.
- [ ] No alternating full-width background sections.
- [ ] No wave or gradient dividers between sections.
- [ ] Sections exist only where the client has real content.
- [ ] Edit forms on pages or inline, not in modals.
- [ ] Settings on one page with headings unless there are many sections.
- [ ] Receipts and printable pages have print layout.
- [ ] DOM order matches visual order.
