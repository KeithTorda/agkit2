# 00 — Master Component Index & 67-Page Template Map

Source repository downloaded locally at:
`c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit/reference-template/bootstrap-5-dashboard-pro/`
Upstream URL: `https://starcodekh.github.io/Bootstrap-5-Dashboard-Template-Pro/`

---

## 1. Quick Domain-to-Template Reuse Matrix

Whenever you build any project, pick its screens directly from this table instead of designing from scratch:

| Project / Module Need | Primary Template Page(s) to Reuse | Key Reusable Classes |
|---|---|---|
| **Executive / Admin Overview Dashboard** | `index.html` (Light), `index-2.html` (Dark) | `.invoice-card-row`, `.invoice-card`, `.card`, ApexCharts / Chart.js |
| **KPI Summary & Stat Strip** | `index.html`, `widget-basic.html`, `cards-center.html` | `.invoice-card`, `.widget-stat`, `.bgl-primary`, `.media` |
| **Ledger / Queue / Transaction Table + Status Tabs** | `page-transaction.html`, `page-invoices.html` | `.card-tabs.style-1`, `.table.card-table.dataTablesCard`, `.badge.light` |
| **Standard CRUD Table (Patients, Students, Staff, Stock)** | `table-datatable-basic.html`, `table-bootstrap-basic.html` | `.table-responsive`, `.display`, `.btn.btn-xs.sharp`, `.custom-checkbox` |
| **Transaction / Record Detail View** | `transaction-details.html` | `.card`, detail key-value grid, activity chart |
| **Wallet / Treasury / Cashflow Screen** | `my-wallet.html`, `cards-center.html` | `.card-bx`, `.nouislider`, payment history list |
| **POS / Storefront / Product Catalog** | `ecom-product-grid.html`, `ecom-product-list.html`, `ecom-product-detail.html` | `.new-arrival-product`, `.new-arrivals-img-contnent`, `.price` |
| **Order Management & Checkout** | `ecom-product-order.html`, `ecom-checkout.html`, `ecom-customers.html` | Order status badges, billing form, cart summary list |
| **Printable Invoice / Official Receipt / RHU Form** | `ecom-invoice.html`, `page-invoices.html` | `.card`, From/To header blocks, line-item table, subtotal/VAT summary |
| **Data Entry Forms & Validation** | `form-element.html`, `form-validation.html`, `form-pickers.html` | `.basic-form`, `.form-control`, `.input-default`, `.needs-validation` |
| **Multi-Step Registration / Onboarding Wizard** | `form-wizard.html` | `.form-wizard`, SmartWizard step indicators |
| **Rich Text / Announcements / Document Editor** | `form-ckeditor.html`, `email-compose.html` | CKEditor card, Dropzone file attachment area |
| **Staff / User Profile & Account Settings** | `app-profile.html`, `post-details.html` | `.profile-card`, `.profile-info`, `.custom-tab-1` |
| **Support Tickets / Internal Inbox / Notifications** | `email-inbox.html`, `email-read.html`, `email-compose.html`, `widget-basic.html` | `.email-left-box`, `.email-right-box`, `.widget-timeline`, `.widget-media` |
| **Appointment / Schedule Calendar** | `app-calender.html` | FullCalendar card + external event category badges |
| **Login / Register / Forgot Password / Lock Screen** | `page-login.html`, `page-register.html`, `page-forgot-password.html`, `page-lock-screen.html` | `.authincation`, `.authincation-content`, `.auth-form` |
| **Error Pages & Starter Shell** | `page-error-400..503.html`, `empty-page.html` | `.error-page`, `.error-text`, clean `#main-wrapper` shell |

---

## 2. Complete Inventory of All 67 HTML Files

### A. Dashboards & Finance (7 Pages)
1. `index.html` — Main Dashboard (Light): 4 colored `.invoice-card` KPIs, Wallet card overview, Activity spline chart, Quick Transfer form, Spendings progress, Transaction Overview bar chart, Previous Transactions table.
2. `index-2.html` — Main Dashboard (Dark): Full dark-theme counterpart (`data-theme-version="dark"`).
3. `my-wallet.html` — Wallet balance cards, Weekly Summary chart, Payment History feed, Invoices Sent list.
4. `page-invoices.html` — Filterable Invoices DataTable with status pills and recipient avatars.
5. `cards-center.html` — Owl-Carousel card deck, Card Statistic donut chart, Card List management table.
6. `page-transaction.html` — Tabbed Transaction Ledger (`All`, `Completed`, `Pending`, `Canceled`) with `.card-tabs.style-1`, date filter button, and `.dataTablesCard` floating row table.
7. `transaction-details.html` — Single transaction breakdown (ID, amount, party info, status, description, activity chart).

### B. Apps, E-Commerce & Operations (13 Pages)
8. `app-profile.html` — Cover banner, avatar, user stats, tabbed Posts / About Me / Account Settings form, photo gallery.
9. `post-details.html` — Article/announcement view with comments and sidebar widgets.
10. `app-calender.html` — Interactive FullCalendar month/week/day scheduler with modal event creation.
11. `email-inbox.html` — Folder sidebar (`Inbox`, `Sent`, `Important`, `Trash`) + selectable message list with star/pagination.
12. `email-read.html` — Message thread view, sender metadata, attachment cards, quick reply box.
13. `email-compose.html` — Recipient/subject form + Dropzone drag-and-drop multi-file uploader.
14. `ecom-product-grid.html` — 4-column responsive product card grid with ratings and prices.
15. `ecom-product-list.html` — Horizontal product list cards with stock status badge and review count.
16. `ecom-product-detail.html` — Tabbed product image preview, size/variant selector, quantity input, Add to Cart CTA, review modal.
17. `ecom-product-order.html` — Orders table with bulk checkbox, customer info, delivery address, status badge (`Completed`, `Processing`, `On Hold`, `Pending`), and row action dropdown.
18. `ecom-checkout.html` — 2-column Checkout: Billing address + payment method form on left, itemized cart summary + promo code on right.
19. `ecom-invoice.html` — Clean printable Invoice/Receipt card (`From`, `To`, QR/reference block, itemized table, Subtotal/VAT/Total).
20. `ecom-customers.html` — Customer directory table with avatar, phone, joined date, and billing address.

### C. Bootstrap 5 Core UI Primitives (16 Pages)
21. `ui-accordion.html` — 12 accordion variants (default, bordered, flush, left-indicator, icon header, solid/tinted header).
22. `ui-alert.html` — 17 alert styles (soft, solid, alt left-border, icon alerts, dismissible, rich message alerts).
23. `ui-badge.html` — 12 badge styles (`.badge.light.badge-*`, solid, pill, outline, rounded, circle counters, `xs`/`sm`/`lg`/`xl`).
24. `ui-button.html` — 16 button groups (solid, `.light` tinted, outline, `.btn-rounded`, `.sharp` square icon buttons, icon-start/end, loading/disabled).
25. `ui-button-group.html` — Segmented button groups, toolbars, vertical stacks, split dropdown groups.
26. `ui-card.html` — 11 card variants (header + subtitle + footer, solid contextual cards, image cards, nav-tab cards).
27. `ui-carousel.html` — Slideshow carousels with indicators, controls, captions, and crossfade.
28. `ui-dropdown.html` — Basic dropdowns, headers, dividers, right-aligned, `dropup`, split button menus.
29. `ui-grid.html` — Responsive 12-column Bootstrap 5 breakpoint reference (`col-sm`, `col-md`, `col-lg`, `col-xl`, `col-xxl`).
30. `ui-list-group.html` — Basic, active/disabled, action links, flush, badge-counter lists, rich media list groups.
31. `ui-modal.html` — Basic modal, scrollable long-content modal, vertically centered modal, `modal-sm` / `modal-lg` / `modal-xl`, grid modal.
32. `ui-pagination.html` — Default, `.pagination-gutter`, contextual colors, `.pagination-circle`, `sm`/`xs` sizes.
33. `ui-popover.html` — Top/bottom/left/right popovers and tooltips.
34. `ui-progressbar.html` — Default, striped, animated, stacked, vertical, and thickness variants.
35. `ui-tab.html` — Default tabs, `.custom-tab-1` underline tabs, `.nav-pills`, vertical pills, icon tabs.
36. `ui-typography.html` — Heading scale (`h1`–`h6`), lead text, muted/contextual text colors, lists, blockquotes.

### D. Widgets, Forms, Tables, Charts & Plugins (21 Pages)
37. `widget-basic.html` — 22 ready-made widgets: `.widget-stat` KPI cards (icon circle + counter + progress bar), `.widget-timeline` activity feeds, `.widget-media` user lists, To-Do checklist, sparkline stat cards, social/profile cards.
38. `form-element.html` — 31 form card patterns: `.input-default`, `.input-rounded`, checkboxes (`.custom-checkbox`), radios, selects, file inputs, input groups, horizontal/vertical/inline forms.
39. `form-validation.html` — Client/server `.is-valid` / `.is-invalid` feedback + icon-prefixed vertical validation form.
40. `form-wizard.html` — 4-step SmartWizard onboarding/checkout stepper.
41. `form-pickers.html` — DateRangePicker, Material DateTimePicker, Pickadate, ClockPicker, ColorPicker.
42. `form-ckeditor.html` — Rich-text WYSIWYG editor card.
43. `table-bootstrap-basic.html` — 14 clean Bootstrap tables: Recent Payments Queue, Exam Toppers (with progress bars + sharp action buttons), striped, bordered, hover, primary/dark headers, contextual rows.
44. `table-datatable-basic.html` — 5 DataTables setups: Basic, Complex Header, Profile Datatable (avatar + contact + sharp edit/delete buttons), Fees Collection (status pills + currency), Patient Records table (check-all + status + action icons).
45–50. **Charts (6 Pages):** `chart-chartjs.html` (13 charts), `chart-chartist.html` (21 charts), `chart-flot.html`, `chart-morris.html`, `chart-sparkline.html`, `chart-peity.html` (+ `apexchart` in dashboards/widgets).
51–57. **Plugins (`uc-*` & Map, 7 Pages):** `uc-select2.html` (searchable single/multi selects), `uc-sweetalert.html` (confirmation/alert dialogs), `uc-toastr.html` (toast notifications), `uc-noui-slider.html` (range sliders), `uc-nestable.html` (drag-sort hierarchy tree), `uc-lightgallery.html` (lightbox gallery), `map-jqvmap.html` (vector maps).

### E. Standalone Auth, Error & Blank Shell Pages (10 Pages)
58. `page-login.html` — Centered `.authincation` sign-in card.
59. `page-register.html` — Centered registration card.
60. `page-forgot-password.html` — Password reset request card.
61. `page-lock-screen.html` — Session lock screen with password unlock.
62–66. `page-error-400.html`, `page-error-403.html`, `page-error-404.html`, `page-error-500.html`, `page-error-503.html` — Clean HTTP status screens with primary return button.
67. `empty-page.html` — Clean master `#main-wrapper` layout shell ready for any new page.

---

## 3. Bundled Icon Packs (`icons/`) & Vendor Libraries (`vendor/`)

- **10 Icon Packs in `icons/`:**
  - `flaticon` / `flaticon_1` (Primary sidebar & search icons: `flaticon-025-dashboard`, `flaticon-381-search-2`, etc.)
  - `line-awesome` (`las la-*`, `lab la-*` — crisp stroke icons used in buttons/headers)
  - `font-awesome` (`fas fa-*`, `far fa-*` — used in sharp table action buttons)
  - `bootstrap-icons` (`bi bi-*`)
  - `themify-icons` (`ti-*`), `simple-line-icons`, `material-design-iconic-font`, `icomoon`, `avasta`
- **Core Vendors & Scripts Required by Every Shell Page:**
  - `vendor/global/global.min.js` (Bootstrap 5 bundle + jQuery + MetisMenu + PerfectScrollbar)
  - `vendor/jquery-nice-select/js/jquery.nice-select.min.js` + `css/nice-select.css`
  - `js/custom.min.js` + `js/dlabnav-init.js`
  - **Mandatory Right-Side UI Kit Settings Panel:** Always include `js/demo.js` and `js/styleSwitcher.js` so every dashboard has the complete floating `.sidebar-right` Theme/Header/Layout/Font customizer and `.dlab-demo-panel` preset switcher on the right edge.
