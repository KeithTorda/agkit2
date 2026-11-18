# 00 — Master Screen & Component Type Catalog (Stack-Agnostic)

First-party design and component taxonomy for **any UI stack** (Tailwind CSS + shadcn/ui, React / Next.js, Laravel Blade / Livewire, Vue / Svelte, Vanilla CSS + `ui-kit/keith-ui-tokens.css`, or Bootstrap 5).

---

## 1. Domain-to-Screen Archetype Map (18 Screen Types)

| # | Screen Archetype | Core Component Types Combined |
|---|---|---|
| 1 | **Overview Dashboard** | `AppShell` + 4 `StatCard` KPIs + `ChartCard` (Trend/Bar) + `ActivityTimeline` + Recent `CrudTable` |
| 2 | **KPI & Analytics Workspace** | `FilterToolbar` (Date Range) + `StatCard` variants (Solid, Tinted, Sparkline, Progress) + Multi-Series `ChartCard` |
| 3 | **Tabbed Status Ledger / Queue** | `SegmentedStatusTabs` (`All / Ready / Pending / Voided`) + `SearchInput` + `FloatingRowTable` + `Pagination` |
| 4 | **Standard CRUD Directory** | Header CTA (`Add Record`) + `CrudTable` + `StatusBadge` + `IconActionButtons` + `FormModal` + `ConfirmDeleteDialog` |
| 5 | **Record / Transaction Detail** | Breadcrumb + Summary Header (`StatusBadge` + Primary Actions) + 2-Column Key-Value `SurfaceCard` + `ActivityTimeline` |
| 6 | **Wallet / Payout / Treasury** | `BalanceHeroCard` + Payout Breakdown `StatCard`s + Payment History `FinancialLedgerTable` |
| 7 | **Product / Item Catalog Grid** | Category/Search `FilterToolbar` + Responsive 3–4 Column `ProductCard` Grid (or Horizontal `ProductListRow`) |
| 8 | **Product / Asset Detail** | Media Preview Gallery + Variant/Option Selector + Price (`tabular-nums`) + Primary Action + Tabbed Specs/Reviews |
| 9 | **Order & Checkout Split View** | Left: Customer/Billing Form + Payment Method `RadioCardGroup`; Right: Sticky Itemized Summary + Subtotal/VAT/Total |
| 10 | **Printable Official Invoice / Receipt** | `@media print` A4/Letter `InvoiceSheet`: Brand/Seal Header, From/To Blocks, Line-Item Table, Server-Computed Totals, Signature/Reference Footer |
| 11 | **Structured Data Entry Form** | Sectioned `SurfaceCard` + Labeled Inputs (`InputField`, `CurrencyInput`, `SearchableSelect`, `UploadDropzone`) + Sticky/Footer Submit |
| 12 | **Multi-Step Onboarding / Wizard** | `StepProgressHeader` (`1 → 2 → 3 → 4`) + Step Validation + `Back / Continue / Finish` Controls |
| 13 | **Studio / Media Workspace** | Split 2-Pane Layout: Left Controls/Timeline/Rules Form + Right Live Preview Frame (`aspect-ratio`) & Rule Checklist |
| 14 | **User Profile & Account Settings** | Profile Header (`AvatarUpload` + Role Badge) + `UnderlineTabs` (`Overview`, `Security`, `Preferences`) |
| 15 | **Split Inbox / Support Tickets** | Left Folder/Status Rail + Middle Filterable Thread List + Right Conversation View & Attachment Reply Box |
| 16 | **Schedule / Appointment Calendar** | Month/Week/Day `CalendarGrid` + Category Legend + `EventFormModal` |
| 17 | **Authentication Screens** | Centered `AuthCard`: Sign In, Register, Forgot Password, Reset Password, Session Lock, OTP Verification |
| 18 | **System & HTTP Error Screens** | Clean Centered Status View (`400`, `403`, `404`, `500`, `503 Maintenance`) with Plain Message + Single Return CTA |

---

## 2. Catalog Directory Index

- [01-DESIGN-TOKENS-CONTRAST-AND-THEMES.md](./01-DESIGN-TOKENS-CONTRAST-AND-THEMES.md) — Semantic CSS variables, 15 WCAG AA color presets, Light/Dark modes, and `@layer` conflict-free setup across Tailwind, Vanilla CSS, and Bootstrap.
- [02-APP-SHELLS-SIDEBARS-AND-SETTINGS-PANEL.md](./02-APP-SHELLS-SIDEBARS-AND-SETTINGS-PANEL.md) — Vertical/Horizontal shells, 5 sidebar modes, sticky viewport rules, top header bar, and the Right-Side Theme Settings Drawer.
- [03-CARDS-KPIS-CHARTS-AND-WIDGETS.md](./03-CARDS-KPIS-CHARTS-AND-WIDGETS.md) — 16 surface card, KPI metric, timeline, user list, checklist, and chart container types.
- [04-DATA-TABLES-LEDGERS-AND-FILTERS.md](./04-DATA-TABLES-LEDGERS-AND-FILTERS.md) — 12 CRUD table, status ledger, financial table, filter toolbar, upward-safe row menu, and pagination types.
- [05-FORMS-INPUTS-PICKERS-AND-WIZARDS.md](./05-FORMS-INPUTS-PICKERS-AND-WIZARDS.md) — 18 input, currency group, combobox, radio card, dropzone, date picker, stepper wizard, and validation types.
- [06-BUTTONS-BADGES-MODALS-ALERTS-AND-NAVS.md](./06-BUTTONS-BADGES-MODALS-ALERTS-AND-NAVS.md) — 16 button, soft status badge, modal/dialog, alert/toast, accordion, tab, dropdown, and progress bar types.
- [07-AUTH-INVOICE-POS-INBOX-AND-SYSTEM-PAGES.md](./07-AUTH-INVOICE-POS-INBOX-AND-SYSTEM-PAGES.md) — 14 auth, POS/catalog, checkout, printable invoice, profile, split inbox, calendar, and error page blueprints.
