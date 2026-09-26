---
part: 22
title: Dashboards and Admin Panels
covers: dashboard home, greetings, stat cards, quick actions, recent activity, charts grid, CRUD pages, list/detail/edit, filter bars, bulk actions, settings, roles and permissions, audit logs, reports and export, POS screens, inventory screens, school and LGU admin
---

# 22 — Dashboards and Admin Panels

Read when: building an admin panel, back office, dashboard home, CRUD module, POS, inventory, school system, barangay or LGU records system.

Table, card and badge details are in part 19. Chart rules are in part 20. Modals and toasts are in part 21. Sidebar and nav are in part 16. This part covers how admin screens are put together.

## 22.1 Dashboard home

The dashboard home is where AI output looks most like a template. Build it from the questions the user opens the app to answer.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Good morning, Keith! 👋" greeting heading | Filler; every generated dashboard has it | No greeting. Page title "Dashboard" or the module name ("Today's sales") |
| "Welcome back! Here's what's happening today." subtext | Says nothing | Delete. Show the date range the numbers cover instead: "Today, 23 Sep 2026" |
| 4–6 stat cards with colored icon circles and trend arrows | The default admin template row | 1–2 key numbers the user acts on; the rest in a compact table or `<dl>` |
| 6+ metric cards | Wall of numbers nobody reads | Max 4 in the top row; move the rest into a report page |
| Different color per stat card (blue, green, orange, purple) | Color as decoration | Neutral cards; color only for status (below target, overdue) |
| KPI cards with no definition ("Engagement 87%") | Undefined metric, invented to fill space | Only metrics the business already tracks, labelled with their definition and period: "Paid enrollments, this SY" |
| Trend arrow "+12.5%" with no comparison period | Meaningless change | State the comparison: "+₱4,200 vs yesterday" or "+3 vs last week" |
| Green up arrow for every increase | Up is not always good (expenses, absences, complaints) | Color by good/bad for that metric, or neutral arrows with text |
| Sparkline inside every stat card | Decoration | Sparkline only when the trend matters and has 7+ points. See part 20 |
| Charts grid: 2x2 of line, bar, donut, area | "Analytics" template | One chart that answers a real question; other data in tables |
| Donut for 2 categories | A number does the job | Text: "62 paid, 38 unpaid" |
| Line chart with 3 points | Not a trend | Table or text |
| Full-width empty chart area with "No data" | Big hole on the page | Hide the chart until there is data; short text line instead |
| Quick Actions card with 6 big icon buttons | Duplicates the nav | Put actions where they belong: "New sale" on the sales page, a primary button in the page header |
| Recent Activity feed with identical entries ("Admin updated a record" x 20) | No information | Group by day, name the record and the change: "Maria Santos changed Grade 7-B adviser to Mr. Reyes" |
| Recent activity limited to 5 rows with no "View all" | Dead end | Link to the full audit log page |
| Calendar widget, weather widget, clock widget | Filler widgets | Remove unless the job needs them (a clinic schedule needs a calendar) |
| To-do list widget on an admin dashboard | Template leftover | Remove; tasks come from real records (pending approvals, overdue invoices) |
| Progress bars for "Storage used 67%" on apps with no storage limit | Invented metric | Remove |
| Onboarding tour overlay on first login | Covers the UI; users skip it | Self-explanatory labels; a short empty state on each page. See part 04 |
| Auto-refresh every 5s | Load on server, jumping numbers | Refresh on action, or every 60s+ with "Updated 2m ago". "Live" label only for push. See part 04 |
| Skeleton shimmer on a dashboard that loads in 200ms | Flash | Skeleton only when load is over 500ms. See part 21 |
| Same dashboard for every role | Cashier sees revenue charts, teacher sees system stats | One home per role: cashier sees today's sales and open shift; teacher sees their classes; admin sees approvals pending |
| Dashboard with no actions (numbers only) | Dead end | Each important number links to the filtered list behind it: "12 overdue" opens `/invoices?status=overdue` |
| "Upgrade to Pro" card in the sidebar of a client's internal tool | SaaS template leftover | Remove |

```html
<!-- Banned -->
<h1>Good morning, Keith! 👋</h1>
<p>Here's what's happening with your store today.</p>
<div class="grid grid-cols-4 gap-6">
  <div class="card"><div class="icon bg-indigo-100"><svg/></div>
    <p>Total Revenue</p><h3>$45,231.89</h3><span class="text-green-500">+20.1% from last month</span></div>
  <!-- x4 more -->
</div>

<!-- Use -->
<h1>Today</h1>
<p class="meta">Tue 23 Sep 2026 · Store: Poblacion branch</p>
<dl class="kpis">
  <div><dt>Sales</dt><dd>₱38,420.00</dd><dd class="delta">₱4,200 more than Tue last week</dd></div>
  <div><dt>Open orders</dt><dd><a href="/orders?status=open">7</a></dd></div>
</dl>
<h2>Low stock</h2>
<table>…</table>
```

## 22.2 Stat cards and KPI tiles

Visual detail for tiles is in part 19. Rules specific to dashboards:

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "$45,231.89" and "+20.1% from last month" (shadcn demo values) | Copied demo data | Real values from the database, or clearly marked sample data in dev only |
| USD `$` in a Philippine client's dashboard | Default locale | `₱` with `Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' })` |
| Numbers animated counting up from 0 | Motion for no reason | Render the final number. See part 25 |
| Huge 48px numbers with tiny 12px labels | Poster style on a work tool | Number about 24–32px, label 13–14px, same token scale as the rest of the app |
| Every tile clickable-looking but none link | False affordance | Link tiles that have a list behind them; plain text for the rest |
| Big number with no period ("Students: 1,204") | Ambiguous | Add scope: "Enrolled, SY 2026–2027" |
| Stat tiles showing zeros on a new install | Wall of zeros | Empty state that says what creates the first record |
| Percentages without the base ("Attendance 94%") | Cannot judge | "94% (451 of 480)" |

## 22.3 CRUD page structure

Most admin work is list, detail, create, edit. Keep one pattern across every module.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Each module built with a different layout (modal create here, page create there) | Generated per prompt, never unified | One pattern: list page, detail page, create/edit page. Same header, same button places |
| Create and edit in a modal for 10-field records | Cramped, lost on backdrop click | Create/edit pages with URLs (`/products/new`, `/products/42/edit`) |
| List page header: title, subtitle paragraph, 3 buttons, search, 4 filters, export, import, view toggle | Every feature on one bar | Title + one primary action ("Add product") on the header row; search and filters on the next row; export and import in an overflow menu |
| Page subtitle "Manage your products and inventory" | Restates the title | Delete, or show the count: "1,240 products" |
| Breadcrumbs "Dashboard / Products / List" on a 2-level app | Adds nothing | Breadcrumbs only 3+ levels deep. See part 16 |
| Detail page that is just the edit form with disabled inputs | Hard to read, looks broken | Read view as a key-value list; Edit button opens the form |
| Edit form with Save at the top only, or bottom only on a long form | Scrolling to save | Save/Cancel at the bottom; on long forms also a sticky footer bar |
| Save button always enabled with no dirty tracking | Pointless saves, no warning on leave | Track dirty state; warn on navigation away with unsaved changes |
| After Save, redirect to the list and lose context | User has to find the record again | Stay on the detail page with "Saved." or return to the list with the row highlighted |
| Delete button next to Save, same size | Misclicks | Delete at the bottom of the detail page or in an overflow menu, danger style |
| ID column shown to users as a UUID | Developer data | Human reference numbers (OR-2026-000123, LRN, Resident ID); UUID hidden |
| `created_at` / `updated_at` columns as raw ISO strings | Unformatted | "23 Sep 2026, 2:14 PM" in PHT, with relative time where useful. See part 04 |
| Status column with 6 pill colors | Rainbow table | 2–3 status colors max; neutral for normal states |
| "Actions" column with 3 icon buttons per row (eye, pencil, trash) | Template CRUD table | Row links to detail; bulk delete via checkbox; row menu for rare actions. See part 19 |
| No empty state on the list | Blank table with headers | "No products yet. Add product" |
| Pagination "Showing 1 to 10 of 10 entries" (DataTables default) | Default text left on | Hide pagination under 50 rows; custom text when shown: "1–50 of 1,240" |
| Page size selector 10/25/50/100 | Default | Pick one sensible size (50) and let search do the rest; keep the selector only when users asked |

## 22.4 Filter bar and search

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Filters inside a collapsible "Advanced filters" panel that everyone opens | Hidden main function | Show the 2–3 most used filters inline; the rest in "More filters" |
| Filters not reflected in the URL | Cannot share or refresh | Store filters in query params |
| Active filters not visible after closing the panel | User forgets list is filtered | Chips showing active filters with remove (x) and "Clear all" |
| Search that needs an exact full name | Frustrating | Case-insensitive partial match; for PH names match with and without "ñ" and middle initial |
| Search fires a request on every keystroke with no debounce | Server load, flicker | Debounce 250–300ms; min 2 characters |
| Date filter with a custom range picker only | Slow for common cases | Presets: Today, Yesterday, This week, This month, This SY / fiscal year, plus Custom |
| Filter dropdowns listing every value including typos | Dirty data exposed | Use normalized reference tables (barangays, sections, categories) |
| Filters reset when opening a record and coming back | Lost work | Preserve list state (query params, scroll position) on back |
| Result count missing | No feedback | "42 results" next to the filters |

## 22.5 Bulk actions

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Checkboxes on every table with no bulk actions defined | Unused affordance | Checkboxes only where bulk actions exist |
| Bulk action bar always visible | Clutter | Bar appears when 1+ rows are selected: "3 selected · Mark paid · Export · Delete" |
| "Select all" selects only the visible page with no notice | Surprise partial action | "All 50 on this page selected. Select all 1,240?" |
| Bulk delete with no count in the confirm | User cannot check scope | "Delete 37 records?" with the first names listed |
| Bulk action runs silently for 2,000 records | Looks stuck | Background job with progress and a result summary: "1,198 updated, 2 failed. View errors" |
| Partial failures hidden | Data silently wrong | List failed rows with the reason and a retry |

## 22.6 Settings pages

Account-level settings (profile, password, sessions) are in part 23.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Settings split into 8 tabs with 2 fields each | Tab bloat | One page with headings; tabs only when sections are large and unrelated |
| Toggle switches for every option | Toggle overuse | Checkbox for options saved with a Save button; toggle only for settings that apply instantly |
| Toggles that apply instantly mixed with fields that need Save | User cannot tell what is saved | Per section: either all instant with "Saved" feedback, or all behind one Save |
| Settings with no descriptions for unclear options | "Enable strict mode" means nothing | One line of helper text stating the effect: "Block sales when stock is 0" |
| "Danger Zone" red box with 4 destructive actions | GitHub copy | Destructive actions at the bottom of the relevant section, each with a clear confirm |
| Settings for features that do not exist (Integrations: Slack, Zapier, Stripe) | Template settings | Only settings the app actually reads |
| Theme picker with 10 themes and accent colors | Showcase feature | Light, dark, system. Or none. See part 34 |
| Business settings missing PH needs | Generic | TIN, BIR permit/ATP details, OR series start, VAT/non-VAT, branch code, business address with barangay |
| Save buttons per field | Many clicks | One Save per section or page |

## 22.7 Roles and permissions UI

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Permission matrix grid of 40 checkboxes per role | Unusable, copied from enterprise templates | A few named roles with a plain description: "Cashier — sell, void own sales with manager PIN, no reports" |
| Roles named "Super Admin", "Admin", "Moderator", "Editor", "Viewer" regardless of the business | Generic | Use the business's words: Principal, Registrar, Adviser, Teacher; Punong Barangay, Secretary, Treasurer, Kagawad; Owner, Manager, Cashier |
| Hidden menu items as the only access control | Backend still allows the action | Enforce on the server; UI hiding is secondary. See part 32 |
| Disabled buttons with no reason for users lacking permission | Confusing | Hide actions the role never has; if shown, say why: "Only the Treasurer can approve disbursements" |
| 403 page for normal navigation within a role | Links lead to walls | Do not render links to pages the role cannot open |
| Role changes take effect with no audit record | No accountability | Log who changed whose role, when, from what to what |
| Invite user form with a role dropdown defaulting to Admin | Unsafe default | Default to the least-privileged role |

## 22.8 Audit logs and activity history

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Activity" page with entries like "User performed an action" | No information | Who, what record, what changed (before → after), when, from where (IP/device where relevant) |
| Audit log editable or deletable by admins | Defeats the purpose | Append-only; no delete in the UI |
| Timestamps in UTC shown to PH users | 8 hours off | Show in Asia/Manila (PHT, UTC+8); store UTC |
| Relative times only ("3 hours ago") in logs | Useless for audits | Absolute date-time, relative as secondary |
| Log shown as a timeline with colored dots and icons per event | Decoration | Dense table: time, user, action, record, details; filter by user, record type, date |
| No export of logs | COA/auditors need them | CSV export with the current filters |
| Sensitive values in logs (passwords, full card numbers, OTPs) | Leak | Mask or omit sensitive fields |

## 22.9 Reports and export

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Reports" page of charts with no export | Admins need files, not pictures | Each report: filters, a table, Export CSV/XLSX, Print |
| Export button that exports only the current page | Silent partial data | Export all rows matching the filters; say the count: "Export 1,240 rows" |
| Export filename "export.csv" / "data (1).xlsx" | Useless on disk | `sales_poblacion_2026-09-01_to_2026-09-30.csv` |
| CSV with ISO dates and raw enums | Hard to use in Excel | Readable dates, labels not codes, peso amounts as numbers with 2 decimals, UTF-8 BOM so "ñ" opens correctly in Excel |
| Print view that prints the sidebar, nav and buttons | No print stylesheet | `@media print`: hide chrome, show header with org name, report title, filters and printed date/time and user |
| PDF generation for every report | Heavy and slow | Print stylesheet first; PDF only when a signed, fixed document is required |
| Government reports built as custom layouts | Must match official forms | Follow the required form layout exactly (DepEd SF1–SF10, BIR forms, barangay RBI, COA formats) and label the form number |
| Large reports generated synchronously | Times out | Background job, notify when ready, keep files for a stated period |

## 22.10 Page header and density

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hero-size page titles (36–48px) on admin pages | Marketing type in a tool | 20–28px page title. See part 13 |
| `py-24` section padding in admin | Wasted screen | Tight spacing scale for data apps (16–24px between blocks). See part 14 |
| Everything in cards with shadows | Card soup | Content on the page surface with dividers; cards only for grouped summaries |
| Content capped at 768px width on a data screen | Wide tables squeezed | Full available width up to about 1440px for tables; 720px for forms and text |
| Sticky header, sticky filter bar, sticky table header, sticky footer | Little room left for rows | Sticky app header and table header only |
| Dark sidebar, colored header, white content, gray cards | Four surface colors | Two surfaces: page and raised. See part 12 |
| "Admin Panel" / "Dashboard Pro" in the header instead of the client's name | Template branding | Client or system name: "Brgy. San Isidro Records", "Santos Hardware POS" |

## 22.11 POS screens

A cashier uses the POS for 8 hours a day on a touch screen, often on a slow shared connection. Speed and error-proofing beat looks.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| POS built like a dashboard with sidebar, stat cards and charts | Wrong job | Full-screen sell view: product search/grid on one side, cart and total on the other |
| Product grid of big cards with stock photos | Slow to scan, images load slowly | Text tiles with name, price and short code; images optional and small; barcode and search first |
| Search that needs a mouse click before typing | Slows every sale | Search/barcode input focused on load and after every sale; scanner input goes straight in |
| Total shown in 14px text | Customer and cashier cannot see it | Total is the largest text on the screen (32px+), `tabular-nums` |
| Prices without centavos or with inconsistent decimals | Rounding confusion | Always 2 decimals: ₱1,250.00 |
| Quantity edited through a modal | Extra taps | Inline +/- steppers (44x44 targets) and direct numeric entry |
| Payment step as a multi-page wizard | Slow checkout | One payment panel: method (Cash, GCash, Maya, Card), amount tendered, change due shown live |
| Change computation only after pressing Submit | Cashier cannot check | Change updates as the amount is typed |
| Quick cash buttons for USD-style amounts | Wrong denominations | ₱ denominations: 20, 50, 100, 200, 500, 1000, and "Exact" |
| Void and discount available to every cashier with no trace | Fraud risk | Manager PIN for void, refund, price override and discounts; log each with reason |
| Senior citizen / PWD discount as a generic "Discount %" field | Legal requirement handled loosely | Dedicated SC/PWD discount: 20% plus VAT exemption, capture ID number and name as required on the receipt |
| Receipt layout designed like an email | Not a BIR receipt | Follow the required receipt fields: registered name, TIN, address, OR/invoice number series, date/time, VAT breakdown (VATable, VAT-exempt, zero-rated, VAT amount), cashier, terminal/MIN where applicable. Wording rules in part 09 |
| No X-reading / Z-reading or end-of-shift flow | Store cannot close the day | Shift open with starting cash, X-reading anytime, Z-reading at close, cash count vs expected with variance |
| POS stops when internet drops | Store cannot sell | Offline queue with visible sync count; block only actions that need the server (GCash confirmation) |
| Hover-only states and small targets | Touch screen | 44x44 minimum targets, `:active` states, no hover-dependent menus |
| Animations on add-to-cart (fly-to-cart, bounce) | Slows repeated actions | Instant update; brief row highlight at most |
| Dark neon POS theme | Crypto look, eye strain in bright stores | High-contrast light theme by default from DESIGN.md tokens |
| Keyboard shortcuts missing on desktop POS | Slower than the old system | F-keys or letter shortcuts for Pay, Void line, Hold, Recall, Discount; shown on the buttons |
| Hold/park sale missing | Queue blocks when a customer steps away | Hold sale and recall list |

## 22.12 Inventory screens

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Stock shown as a single number with no unit | Pieces vs boxes vs kilos confusion | Show unit: "24 pcs", "3 boxes (12 pcs/box)", "12.5 kg" |
| Stock edited directly in a field | No history, easy theft | Stock changes only through movements: receive, sell, transfer, adjust (with reason), return |
| "Low stock" badges on every row in orange | Alert fatigue | Reorder point per item; low-stock list sorted by urgency |
| Product form with 30 fields on one screen including rarely used ones | Slow data entry | Required fields first (name, unit, price, cost, SKU/barcode); the rest under "More details" |
| Variants built as separate products | Messy counts | Variants (size, color) under one product with their own SKU and stock |
| Stock count screen without scanner support | Slow counts | Scan-to-count mode with running totals and variance review before posting |
| No branch/location dimension | Multi-branch stores need it | Stock per location; transfers between locations |
| Expiry dates ignored for food/pharmacy clients | Real risk | Batch/lot and expiry tracking where the client sells perishables; FEFO picking |
| Money values as floats | Rounding errors | Store centavos as integers or DECIMAL(12,2). See part 32 |
| Import from Excel with no preview | Bad data goes straight in | Upload, preview with row-level errors, then confirm import |

## 22.13 School admin

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Generic "Users" module for students, teachers and parents | Loses school structure | Separate records: learners (with LRN), teachers/staff, guardians; linked by section and school year |
| No school year dimension | Data mixes across years | School year selector in the header; every record scoped to a SY (e.g., SY 2026–2027) |
| Grade levels as free text | Typos, broken reports | Fixed list: Kinder, Grade 1–12, with strands/tracks for SHS (STEM, ABM, HUMSS, GAS, TVL) |
| Grades entered one student at a time in forms | Slow for teachers | Class record grid: learners as rows, components (Written Work, Performance Task, Quarterly Assessment) as columns, keyboard navigation, autosave |
| Grade computation hidden | Teachers cannot verify | Show the formula and weights used (per DepEd order the school follows), transmuted grade and remarks |
| Attendance as a checkbox per learner per day with no bulk | Slow | Default "Present" for all, mark exceptions; show monthly totals for SF2 |
| Report card designed as a modern card UI | Parents and DepEd expect the official format | Printable form matching the required layout (SF9) |
| Enrollment form asking for fields schools do not collect | Copied from generic templates | Fields from the actual enrollment form the school uses (LRN, PSA birth certificate number, 4Ps status, IP/Mother tongue, last school attended) |
| Parent portal with gamified badges for learners | Invented features | Grades, attendance, announcements, fees balance |
| Minors' data shown to any logged-in user | Privacy (Data Privacy Act) | Access by role and assignment: advisers see their section, subject teachers see their classes |

## 22.14 Barangay and LGU admin

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Resident records as a generic contacts list | Loses household and purok structure | Residents grouped by household, purok/sitio and barangay; head of household flag |
| Address as one free-text field | Cannot filter or report | Structured: house no., street, purok/sitio, barangay, city/municipality, province (PSGC codes where possible) |
| Clearance/certificate issuance as a form that emails a PDF | Office prints and signs | Queue: request, verify, pay fee (OR number), print on the official template, release; log each step |
| Certificate template with fake seal, "Hon." placeholder names | Invented officials | Officials pulled from a settings table the barangay maintains; real seal file uploaded by the client. See part 09 |
| Blotter module with open text and no case number | Hard to track | Case number series, parties, incident date/place, status (filed, mediated, settled, referred), hearing schedule |
| Dashboard showing "Total population" from records that are 40% complete | Misleading | Show the count with the basis: "3,412 residents recorded (RBI updated Aug 2026)" |
| Officials' term dates missing | Signatories wrong after elections | Term start/end; signatory resolves by document date |
| Disbursement/budget module with no approval chain | Accountability gap | Prepared by, reviewed by, approved by; each step logged with date |
| Election tools (COMELEC-style precinct finders, voter lists) editable by many users | Integrity risk | Read-only public lookups; edits by a small named role with full audit trail |
| Personal data exported freely | Data Privacy Act exposure | Export restricted by role, logged, with purpose noted |

## 22.15 Stack-specific tells

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| AdminLTE / CoreUI / Sneat / Materio demo pages left in (Charts, Icons, Typography, Buttons, "Pages > Error 404") | Template shipped as the product | Delete demo routes and menu items before first client review |
| Template footer "Copyright © 2026 AdminLTE.io. All rights reserved. Version 3.2.0" | Vendor branding left in | Client name and year, or no footer |
| shadcn dashboard example copied whole ("Overview", "Recent Sales" with Olivia Martin, "$45,231.89") | Demo names and numbers left in | Real modules and data; grep for "Olivia Martin", "Jackson Lee", "$45,231" |
| Tailwind: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6` stat row for 7 stats | Template row repeated | Fewer stats; a `<dl>` or table for the rest |
| Chart.js default blue/red datasets with legend at top | Library defaults | See part 20 |
| DataTables with default "Search:" label, "Show 10 entries", "Previous/Next" | Default plugin text | Configure labels and page size; hide controls not needed |
| Bootstrap: `.card.shadow` around every block, `.bg-gradient-primary` sidebar | SB Admin 2 look | Plain surfaces, solid sidebar token |
| React admin (react-admin, Refine) default theme unchanged | Recognizable framework look | Apply DESIGN.md tokens to the theme before the first screen |
| Filament / Laravel Nova / Django admin exposed as the client-facing app | Developer tool as product | Fine for internal staff; client-facing screens get their own UI |

## 22.16 Check
- [ ] No greeting heading or "Here's what's happening" subtext.
- [ ] Dashboard shows 1–4 key numbers, each with a period, definition and link to the list behind it.
- [ ] Trend deltas name the comparison period; color follows good/bad for that metric.
- [ ] No stat card colors, icon circles or sparklines added for decoration.
- [ ] No undefined or invented KPIs. No demo values ($45,231.89, Olivia Martin) anywhere.
- [ ] Currency is ₱ with 2 decimals; dates and times are in PHT.
- [ ] No charts with 2–3 points, no donut for 2 categories, no empty full-width chart boxes.
- [ ] No Quick Actions card, weather, clock or to-do widgets unless the job needs them.
- [ ] Recent activity names who, what record and what changed, grouped by day, with "View all".
- [ ] Each role has its own home screen.
- [ ] Refresh is on action or 60s+ with "Updated X ago". No "Live" label on polling.
- [ ] Every module follows the same list / detail / create / edit pattern with URLs.
- [ ] Records with more than 3 fields are edited on a page, not in a modal.
- [ ] Page header has one primary action; secondary actions go in an overflow menu.
- [ ] Filters live in the URL, show as removable chips, and survive back navigation.
- [ ] Search is debounced, partial, case-insensitive and handles "ñ".
- [ ] Bulk bar appears only on selection and states counts; select-all across pages is explicit.
- [ ] Long bulk jobs run in the background and report failures per row.
- [ ] Settings use one page with headings; toggles only for instant-apply settings.
- [ ] Roles use the client's own titles and have plain descriptions; permissions are enforced on the server.
- [ ] Audit log is append-only, dense, filterable, exportable, and shows before and after values.
- [ ] Reports have Export (all matching rows, named file, UTF-8 BOM) and a print stylesheet.
- [ ] Official forms (DepEd SF, BIR, COA, barangay) follow the required layout.
- [ ] POS: search focused, total is the largest text, live change due, ₱ denomination buttons, manager PIN for voids and discounts.
- [ ] POS: SC/PWD discount handled as its own flow; receipt has the required BIR fields.
- [ ] POS works offline with a visible sync queue, and has X/Z-reading and shift close.
- [ ] Inventory changes only through logged movements with units and locations.
- [ ] School data is scoped by school year, section and role; class records use a grid.
- [ ] Barangay records use households, purok and structured PSGC addresses; certificates print on the official template with officials from settings.
- [ ] Template demo pages, vendor footers and "Upgrade to Pro" cards are removed.
- [ ] Header shows the client's system name, not "Admin Panel".
