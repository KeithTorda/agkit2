---
part: 19
title: Data Display
covers: tables, lists, cards, badges, chips, tags, avatars, stat and KPI tiles, key-value lists, timelines, activity feeds, trees, kanban, calendars, pagination vs infinite scroll, sorting, filtering, density, number alignment, truncation, row actions
---

# 19 — Data Display

Read when: rendering records of any kind: tables, lists, cards, feeds, stat tiles, detail views, badges, calendars, boards, or any screen in an admin, POS, inventory, school or LGU system that shows rows of data.

Number, date and currency formatting rules live in part 04. Charts live in part 20. Dashboard page composition lives in part 22. Row and bulk action buttons are in part 18.

## 19.1 Choosing the container

Match the container to the data. Tables for comparable records. Lists for feeds and single-column items. Key-value lists for one record's fields. Cards only for items that are visual or independent.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Identical card grid for everything: stats, feeds, users, orders | One component reused regardless of data | Table for records with 3+ comparable fields, list for feeds, inline text or `<dl>` for metadata |
| Orders, students or voters shown as cards, 3 per row | Cannot scan or compare columns | `<table>` with sortable columns |
| Cards inside cards (a card of cards of stats) | Nesting destroys hierarchy | Flat list with dividers, or one level of card |
| Masonry layout for non-image content | Reading order breaks | List or table. Masonry only for photo galleries |
| Table avoided; data laid out with divs and CSS grid | Loses semantics, sorting, screen reader headers | Real `<table>`, `<thead>`, `<th scope="col">` |
| Every record's detail page as a grid of 12 small cards | Card-everything | One `<dl>` key-value list grouped under headings |
| Carousel of records (products, announcements) | Hides most items | Show a list or grid; paginate if long |
| Accordion for every record in a list | Hides content that could be scanned | Show the summary fields in the row; open details on a detail page or expandable row |

## 19.2 Tables: structure and styling

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Zebra stripes plus hover plus row shadow plus rounded rows | Every effect stacked | Pick one: row dividers (default) or zebra. Hover background is fine on clickable rows |
| Table inside a card with shadow and 16px radius | Card habit | Table on the page surface, full width of the content column, 1px border token or no outer border |
| `border-radius: 24px` on a table | Bubbly look on data | 0 to 8px outer radius from DESIGN.md, or none |
| Header row with a gradient or saturated primary fill | Decoration | Header text in a muted token, weight 600, bottom border; background neutral or none |
| Uppercase tiny gray headers (11px, tracking-wider) everywhere | Tailwind UI default | Sentence case, 12 to 14px, weight 500 to 600, contrast 4.5:1 |
| Each cell with its own border (full grid lines) | Spreadsheet noise | Horizontal dividers only, unless it is an editable grid |
| Full-width table stretched on a 2560px screen with 4 columns | Huge gaps between values | `max-width` on the table or its container; or let the last column absorb width |
| Row height 72px for single-line text | Marketing spacing in data | 40 to 48px default row, 32 to 36px compact option for ops users |
| Row hover lifts with `translateY(-2px)` and shadow | Motion on data | Background change to `var(--surface-alt)` only |
| Nested tables | Unreadable, broken a11y | Expandable row with a sub-list, or a detail panel |
| Missing `<caption>` or heading for the table | Unlabelled region | A visible heading above the table, or `<caption>` |
| Sticky header missing on a 200-row table | Column meaning lost | `position: sticky; top: 0` on `<th>` for long tables |
| Sticky header, sticky first column, sticky action column, sticky footer all at once on mobile | Nothing scrolls | Sticky header plus first column at most |

## 19.3 Columns, alignment and numbers

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Numbers left-aligned or centered | Digits do not line up | Right-align numbers and their headers. Left-align text. Center only short fixed-width icons or checkboxes |
| Proportional digits in price and quantity columns | Columns wobble | `font-variant-numeric: tabular-nums` on numeric cells |
| Mixed decimal places (₱1,250 / ₱980.5 / ₱12.00) | Unformatted data | Same decimals per column: `₱1,250.00` format. See part 04 |
| Currency symbol repeated in every cell with inconsistent spacing | Noise | "Amount (₱)" in the header and plain numbers in cells, or `₱` in every cell with one format |
| Dates as raw ISO `2025-03-04T08:15:00Z` | Unformatted | "Mar 4, 2025" or "04 Mar 2025, 8:15 AM" per app rule. See part 04 |
| Relative time only ("3 days ago") in audit tables | Cannot compare exactly | Absolute date in the cell, relative in a tooltip, or both |
| ID column (UUID) shown first and widest | DB dump | Hide internal IDs. Show human codes (OR-000123, LRN) where users use them |
| Every DB column shown (created_at, updated_at, deleted_at, uuid, id) | Schema dump | Show the 4 to 8 columns users act on. Offer column picker if more are needed |
| Column order random | Generated from object keys | Identifier first, then the fields users scan, then status, then amounts, then actions |
| Boolean columns as "true" / "false" | Raw values | "Yes" / "No", or a status word, or a check mark with text alternative |
| Empty cells blank with no marker | Unclear if missing or loading | En dash "–" or "None" in a muted token, with visually hidden "No value" if needed |
| Totals row missing on financial tables | Users add by hand | Footer row `<tfoot>` with totals, bold, right-aligned |

## 19.4 Status in tables and lists

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Icon-only status column (green dot, red dot) | Color-only meaning | Text status ("Paid", "Overdue") with optional dot or icon |
| Every status a different saturated pill color (8 colors) | Rainbow | 4 semantic tokens: neutral, info, success, warning, danger. Map each status to one |
| Status pill with gradient, glow or pulse animation | Decoration | Solid subtle background token plus text token; no animation |
| "Live" or "Real-time" badge on data refreshed by polling | False claim | "Updated 2m ago" for polling; "Live" only for push (WebSocket/SSE). Status words in part 04 |
| Pulsing green dot next to "Online" for a static field | Fake presence | Show presence only if the system tracks it; no pulse |
| Status words that differ across screens (Paid / Settled / Completed for the same state) | Generated per screen | One status vocabulary in a shared enum-to-label map |

## 19.5 Sorting, filtering and search in data views

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Sortable columns with no indication of current sort | User cannot tell order | Arrow on the sorted column, `aria-sort="ascending|descending"` on its `<th>` |
| Sort arrows shown on every column, including non-sortable ones | Misleading | Arrows only on sortable columns; sort control is a `<button>` inside `<th>` |
| Default sort is DB insertion order | Random-looking | Default to the most useful order (newest first for orders, alphabetical for names) and show it |
| Filter panel with 15 filters open by default | Wall of controls | 2 to 4 common filters visible; "More filters" for the rest |
| Filters applied with no visible summary | User forgets why rows are missing | Chips for active filters with remove buttons and "Clear all" |
| Filters and sort not in the URL | Lost on refresh, cannot share | Store in query params (`?status=paid&sort=-date`) |
| Filter results count missing | Unclear effect | "48 orders" near the table heading, updated on filter |
| Search that only matches from the start of a field or is case-sensitive | Frustrating | Case-insensitive, contains match; accent-insensitive where names have ñ |
| Filter dropdowns listing values that return 0 results | Dead ends | Show counts, or hide empty values |
| Date filter as two raw date pickers only | Slow for common ranges | Presets (Today, This week, This month, Custom) |

## 19.6 Pagination, infinite scroll and load more

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Pagination for fewer than 20 items | Needless clicks | Show all when under about 50 rows |
| "Showing 1-10 of 10" | States the obvious | Hide the range when everything fits on one page |
| Infinite scroll on admin tables and reports | Cannot reach footer, lose position, cannot reference a page | Numbered pagination or "Load more" for admin data |
| Infinite scroll with no end marker | Endless spinner | "End of list" text or disable loading when done |
| Page size fixed at 10 for ops users | Too many clicks | 25 or 50 default with a page-size select (25, 50, 100) |
| Pagination with 20 page-number buttons | Clutter | First, previous, current range (3 to 5 numbers), next, last; plus "Page 3 of 48" |
| Pagination that resets to page 1 after editing a record | Lost position | Return to the same page and scroll position |
| Pagination controls only at the bottom of a long table | Scroll to navigate | Top and bottom for long pages, or sticky bottom |
| Offset pagination on large, fast-changing tables (duplicates between pages) | Data shifts | Cursor pagination on the API. See part 32 |

## 19.7 Density and mobile tables

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Marketing-level spacing in data apps (24px cell padding) | Low information density | 8 to 12px vertical, 12 to 16px horizontal cell padding. Offer a compact toggle for heavy users |
| Horizontal scroll with no indicator | Users miss columns | Fixed first column, scroll shadow on the edge, or visible scrollbar |
| Table squeezed to 390px with 8 columns and 10px text | Unreadable | On mobile: convert rows to stacked key-value blocks, or show 2 to 3 key columns with a link to detail |
| Stacked mobile rows that repeat every label in bold caps | Heavy | Primary field as the title, 2 to 3 secondary fields as muted text, status on the right |
| Hiding columns on mobile without a way to see them | Data loss | Detail page or expandable row shows all fields |

## 19.8 Truncation and overflow

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `text-overflow: ellipsis` on names and IDs with no way to see the full value | Information hidden | Allow wrapping for names; truncate only long descriptions, with full text in `title` or a tooltip, and on the detail page |
| Truncating numbers or amounts | Wrong value read | Never truncate numbers; widen the column or wrap the header |
| `line-clamp-3` on every description in a list, even 1-line ones | Applied blindly | Clamp only fields known to be long; add "Show more" for content users need |
| Middle truncation missing for file names and paths | End of name lost ("Report_2025_...") | Middle truncation keeping the extension: "Barangay_Report…_Q3.xlsx" |
| Long Filipino names cut to "Ma. Concepcion Dela Cr..." | 20-char limit | Let names wrap to 2 lines |

## 19.9 Lists

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Every list item is a card with shadow and 16px gap | Card-everything | One surface, 1px dividers between items |
| Avatar, title, subtitle, 3 badges, timestamp and 2 icon buttons per item | Everything at once | Title, one line of meta, one status. Actions on hover-plus-focus or in a menu |
| Icon before every list item for decoration | Noise | Icons only when they tell item types apart |
| `<div>` stacks for lists | No list semantics | `<ul>` / `<ol>` with `<li>` |
| Chevron on every row including non-clickable ones | False affordance | Chevron only on rows that navigate |
| Whole row clickable but only the title is a link, and the row hover suggests otherwise | Unclear target | Make the title a link and extend its hit area with a pseudo-element over the row, keeping nested buttons above it |

## 19.10 Cards (when cards are right)

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Icon + Title + Vague Sentence cards | Template filler | For tools, show real data or a screenshot. Skip the card row |
| Card hover lifts with `translateY(-4px)` and bigger shadow | Motion trope | Border or background token change; or none |
| Cards with a colored top border in a different color each | Rainbow | Neutral cards; color only for status |
| Card heights forced equal with large empty areas | Grid obsession | Allow natural height, or align content to top |
| Product card with image, name, price, rating, 3 badges, 2 buttons and wishlist heart | Everything at once | Image, name, price in ₱, one action. Extras on the product page |
| Cards with `shadow-2xl rounded-3xl` | Tailwind trope | Border token, radius token (commonly 8px), small or no shadow |
| Entire card wrapped in `<a>` containing buttons | Nested interactive elements | Title link with stretched hit area; buttons outside or above the link layer |

## 19.11 Stat and KPI tiles

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| 4 to 6 stat cards in a row, each with a colored icon circle and a trend arrow | The AI dashboard header | 1 to 2 key numbers prominent; the rest in a compact inline stat row, `<dl>` or table. See part 22 |
| 3-column equal card grid for stats | Card habit | Inline stat row: label and value pairs separated by dividers |
| Each stat card a different accent color | Decoration | Neutral tiles. Color only for status (over budget, overdue) |
| Stat value with no period ("Revenue ₱1.2M") | Meaningless | Name the period: "Sales this month", "Enrolled, SY 2025–2026" |
| "+12.5%" green arrow with no comparison base | Unclear | "+12% vs last month" in text. Arrow optional; color follows meaning (a rise in expenses is not good). See part 20 |
| Invented KPI tiles (Engagement Score, Health Index) with no definition | Undefined metrics | Only metrics the client tracks, with a definition in a tooltip or help text |
| Counters animating from 0 to the value | Motion trope | Render the number. See part 25 |
| Stat values in 48px extrabold gradient text | Hero styling in a tile | 24 to 32px, weight 600, solid text token, `tabular-nums` |
| Abbreviated numbers without precision rules ("1.2k" for 1,249 in a finance app) | Hides exact values | Full values in finance and government reports; abbreviate only in space-limited tiles, with exact value on hover and in the detail |
| Sparkline in every tile | Decoration | Sparkline only where the trend matters and has 7+ points. See part 20 |
| Stat tiles showing "0" everywhere for a new account | Dead dashboard | Empty state with the first action. See part 04 |

```html
<!-- Banned -->
<div class="grid grid-cols-4 gap-6">
  <div class="rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 p-6 shadow-xl">
    <div class="h-12 w-12 rounded-full bg-white/20"><svg>...</svg></div>
    <p class="text-4xl font-extrabold">12,543</p>
    <p class="text-sm">Total Users <span class="text-green-300">↑ 12.5%</span></p>
  </div>
  <!-- x3 more, each a different gradient -->
</div>

<!-- Use -->
<dl class="stat-row">
  <div><dt>Sales this month</dt><dd>₱482,310.00</dd></div>
  <div><dt>Orders</dt><dd>1,204</dd></div>
  <div><dt>Unpaid invoices</dt><dd>17</dd></div>
</dl>
```

## 19.12 Key-value and detail views

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Record detail as a grid of mini cards (one per field) | Card-everything | `<dl>` with `<dt>`/`<dd>`, two columns on desktop (label left, value right) |
| Labels in bold and values in gray | Hierarchy inverted | Labels muted, values in the main text token |
| Every field shown even when empty | Noise | Hide empty optional fields, or show "None" for fields users expect to see |
| Edit icon next to every value | Inline-edit sprinkle | One Edit button for the section; inline edit only for high-frequency single fields |
| Copy-to-clipboard icon on every value | Clutter | Copy only on values people paste elsewhere: reference numbers, account numbers, URLs, API keys |
| Metadata (created by, updated at) given the same weight as main fields | Flat hierarchy | Metadata in a muted line at the bottom or side |

## 19.13 Badges, chips and tags

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Badges on everything (every nav item, every card, every row) | Noise | Badges only for real counts (unread, pending) or status |
| "New" badge glowing or pulsing | Trope | Plain text badge, removed after the user sees the item or after a set number of days. See part 10 for the hero pill |
| Gradient badges | Decoration | Solid subtle background token plus text token |
| Badge color picked per tag name by hash, giving 20 colors | Rainbow | Neutral tags; color only for status tags |
| Count badge showing "99+" on a sidebar item for items that are not actionable | False urgency | Count only items that need action |
| Chips that look clickable but are static, or clickable but look static | Unclear affordance | Static tags: no hover, no pointer. Interactive chips: border, hover state, remove button with `aria-label` |
| Fantasy rank badges (Elite Vanguard, Code Wizard, Diamond Tier) | Gamification trope | Plain roles and levels: Admin, Mod, Member, Level 12. Requirements stated plainly ("50 posts") |
| Emoji inside badges ("🔥 Hot", "⚡ Pro") | Chat tone | Text only |
| Badge text 10px uppercase at low contrast | Unreadable | 12px minimum, sentence case, 4.5:1 |

## 19.14 Avatars

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| pravatar.cc or randomuser.me photos in production or demo screenshots | Placeholder people | Initials on a neutral token background, or the user's uploaded photo. See part 26 |
| Avatar stack "+12" on every card | Decoration | Avatar stacks only where membership matters (project team); otherwise a count in text |
| Online status dot on every avatar with no presence system | Fake | Show only with real presence data |
| Initials background color random per render | Flicker | Deterministic color from user ID within a small neutral set, or one neutral token |
| Gradient ring around avatars (story style) | Social app trope | No ring; 1px border token if needed on busy backgrounds |
| Avatar with no name nearby, alt text "avatar" | Unlabelled person | Name next to it; `alt=""` if the name is adjacent, otherwise `alt="Maria Santos"` |

## 19.15 Activity feeds and timelines

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Recent Activity with identical entries ("Order updated" x10) | No information | Group by day and by object; collapse repeats: "Order OR-1203 updated 4 times" |
| Vertical timeline with colored dots, connecting gradient line and icons in circles for a simple log | UI-kit showcase | Plain list grouped by date headings, time on the left in `tabular-nums` |
| Relative times only ("2 hours ago") in logs | Not auditable | Absolute time with relative in tooltip, or both |
| Activity items missing actor or object | "Something changed" | "Juan Dela Cruz changed status of OR-1203 from Unpaid to Paid" |
| Audit log with no filter by user, action or date | Unusable | Filters for user, action type, date range; export. See part 22 |
| Feed that auto-inserts new items and shifts what the user is reading | Reading jump | "3 new items" button at the top that loads them on click |

## 19.16 Trees and hierarchies

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Tree with 5+ nested levels shown fully expanded | Wall of indentation | Expand to level 1 or 2 by default; remember expansion state |
| Expand toggle is only a 10px caret | Small target | Whole row toggles, or a 24px+ button with `aria-expanded` |
| Custom tree without keyboard arrows | Mouse-only | ARIA tree pattern with arrow keys, or nested lists with disclosure buttons |
| Org chart graphic for a 6-person barangay council | Heavy | Simple list: position, name, contact. See part 09 for official listings |
| Indentation only by 8px per level | Levels indistinct | 16 to 24px per level plus guide lines if deep |

## 19.17 Kanban boards

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Kanban for data that has no workflow stages | Board because it looks busy | Table with a status column |
| Drag-and-drop only for moving cards | Mouse-only; fails on touch and keyboard | Status select or "Move to" menu on each card, drag as extra |
| Column headers in different bright colors | Rainbow | Neutral headers with counts ("Pending 12") |
| Cards with avatars, tags, progress bars, due dates, comments count and attachment count all visible | Overloaded | Title, assignee, due date; rest on open |
| Columns with no WIP counts or limits when the team uses them | Missing function | Count in each header; limit shown if the team uses one |
| Horizontal scroll board on mobile with 6 columns | Hard to use | Mobile: one column at a time with a stage switcher, or a list grouped by status |

## 19.18 Calendars and schedules

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Month grid as the default view for a schedule list | Events truncate to dots | Agenda (list by date) as default; month view as an option |
| Week starts on Monday or Sunday inconsistently | Library default | Pick one per app (Sunday is common in PH calendars; follow the client) and set it in the library config |
| Event colors random per event | Rainbow | Color by category with a legend, max 5 categories, plus text labels |
| Times without AM/PM or timezone for public schedules | Ambiguous | "9:00 AM" with "Philippine time" noted once |
| PH holidays missing in a school or LGU calendar | Generic data | Include national and local holidays from an official list the client provides |
| Calendar cells 20px tall on mobile | Unusable | Agenda view on mobile |

## 19.19 Empty, loading and error states inside data views

Copy for these states is in part 04. This section is about layout.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Empty table with a large illustration | Filler art | "No records." plus an action link ("Add product") inside the table area |
| Empty state that hides the filters, so users cannot clear a filter that caused zero rows | Trap | Keep filters visible; add "Clear filters" link in the empty message |
| Skeleton rows for data that loads in 200ms | Flash | Skeleton only when load exceeds about 500ms. See part 21 |
| Skeleton with a different layout from the loaded table | Jump on load | Skeleton matches row height and column count |
| Table error replaces the whole page | Overreach | Error message in the table area with a Retry button; rest of the page stays |
| Loaded data flashes empty state first, then rows | Race condition | Show loading until the first response resolves |

## 19.20 Philippine context

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Amount columns with "$" or "PHP 1250" unformatted | Wrong locale | `₱1,250.00` via `Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' })` |
| Student lists sorted by first name | Schools sort by surname | Sort by last name, then first name; show "Dela Cruz, Juan M." format where the school uses it |
| Voter or resident lists showing full birth dates, addresses and phone numbers to all roles | Data Privacy Act exposure | Show only fields each role needs; mask phone as "0917 *** 4567"; log access |
| Precinct or barangay lists without codes | Hard to match with official records | Show the official code (PSGC, precinct number) as a column |
| Receipts list without OR/SI number column | BIR reference missing | OR or SI number as the first column in sales tables |
| School year shown as a calendar year | Mismatch | "SY 2025–2026" |
| Grades shown as bars or badges only | Official records need numbers | Numeric grade plus descriptor used by DepEd or the school |

## 19.21 Stack-specific tells

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Tailwind UI table copy with `ring-1 ring-black ring-opacity-5 shadow sm:rounded-lg` wrapper on every table | Template signature | Table on surface; one border token if needed |
| DataTables.js default look (blue sort arrows, "Show 10 entries", "Search:" label) unchanged | Plugin default | Style to DESIGN.md tokens; rename labels; set page size 25 |
| Bootstrap `.table .table-striped .table-hover .table-bordered .shadow` all at once | Effects stacked | `.table` plus one of striped or hover |
| TanStack Table / AG Grid default theme with alpine blue left in | Library default | Theme via tokens |
| React list with `key={index}` | Reorder bugs | Stable IDs as keys. See part 31 |
| Rendering 5,000 rows without virtualisation or pagination | Freezes low-end Android | Paginate server-side, or virtualise lists over about 500 rows |
| `toLocaleString()` without a locale | Output differs per device | Pass `'en-PH'` (or the app locale) explicitly |

## 19.22 Check
- [ ] Records with 3+ comparable fields use `<table>`, not cards.
- [ ] No cards inside cards; no masonry for non-image content.
- [ ] Tables use one of zebra or dividers; hover only on clickable rows; no shadow or large radius.
- [ ] Table sits on the page surface with a heading or `<caption>`.
- [ ] Header cells use `<th scope="col">`; sorted column has `aria-sort` and a visible arrow.
- [ ] Numbers are right-aligned with `tabular-nums` and consistent decimals.
- [ ] Currency shows as `₱1,250.00`; dates follow the app format.
- [ ] Internal IDs and timestamps columns are hidden unless users need them.
- [ ] Empty cells show "–" or "None".
- [ ] Financial tables have a totals row.
- [ ] Status is text, optionally with a dot; 4 to 5 semantic colors max.
- [ ] "Live" appears only for push data; polling shows "Updated X ago".
- [ ] Filters, sort and page are in the URL; active filters show as removable chips.
- [ ] Result count shown near the table heading.
- [ ] No pagination under about 50 rows; no "Showing 1-10 of 10".
- [ ] Admin tables use pagination or Load more, not infinite scroll.
- [ ] Page size default 25 or 50 with a selector.
- [ ] Wide tables show a scroll hint or fixed first column; mobile shows stacked rows or key columns.
- [ ] Names wrap instead of truncating; numbers never truncate.
- [ ] Lists use `<ul>`/`<ol>` with dividers, not card stacks.
- [ ] Cards have no hover lift; one link per card with a stretched hit area.
- [ ] Stat row shows 1 to 2 prominent numbers; others compact; each names its period.
- [ ] Trend deltas state the comparison base in text.
- [ ] No counter animation, gradient stat text or colored icon circles.
- [ ] Detail views use `<dl>`, labels muted, values primary.
- [ ] Badges only for real counts or status; no pulse, gradient or emoji.
- [ ] No fantasy rank names.
- [ ] Avatars use initials or real uploads; no placeholder photo services.
- [ ] Activity feeds are grouped by day with actor and object named; repeats collapsed.
- [ ] Trees and kanban are keyboard usable with non-drag alternatives.
- [ ] Calendars default to an agenda list on mobile; times show AM/PM.
- [ ] Empty tables show a line of text and an action, filters stay visible.
- [ ] Skeletons only for loads over about 500ms and match the final layout.
- [ ] Personal data columns are limited by role and masked where not needed.
- [ ] Student and resident lists sort by surname.
- [ ] Rows use stable keys; large lists are paginated or virtualised.
