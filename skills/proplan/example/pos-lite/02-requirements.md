---
doc: 02-requirements
project: cafe-pos
version: 1.0.0
status: approved
owner: product-manager
updated: 2026-09-27
---

# Requirements

## Stakeholders

| Stakeholder | Interest | Involvement |
|---|---|---|
| Liza Dela Cruz, owner | Sales visibility, cash control, correct discounts | Approves scope and the architecture checkpoint; UAT on reports |
| Cashiers (2 per shift) | Fast checkout, no arithmetic, clear errors | UAT on the order and payment screens |
| Supervisor (Mark) | Approves voids, counts cash at shift close | UAT on voids and shift close; part-time tester |
| Accountant (external) | Receipt wording, discount records, sales summary format | Reviews receipt wording and the CSV export |

## Personas

- **Cashier (Joy, 22).** Works the 6:00-14:00 shift, handles 120-180 orders, often with a queue of 8 people. Uses her own Android phone daily; has never used a POS. Needs large targets and no mental math.
- **Supervisor (Mark, 30).** Opens and closes shifts, approves voids and discounts, counts the drawer. Wants to find a variance in minutes, not hours.
- **Owner (Liza, 45).** Reads the report on her phone at night; edits prices a few times a year; not technical.

## Scope

In:
- Menu with categories, items, modifier groups (size, sugar level, add-ons), sold-out toggle.
- Orders at one counter, cash and GCash (static QR) payments, split between the two.
- Senior Citizen and PWD discounts with ID details recorded.
- Receipts on a 58 mm Bluetooth thermal printer; reprint.
- Voids with supervisor PIN; shift open and close with cash count.
- Daily report on the owner's phone and CSV export.
- Offline order taking with automatic sync.

Out (this version):
- Loyalty stamps and customer accounts (phase 2 if G-01 is met).
- Recipe-level inventory deduction (phase 2; the café tracks stock on a sheet today).
- GCash or card payment API integration (the static QR is enough for current volume).
- Kitchen display, table service, delivery-app integration, multiple branches.
- BIR accreditation of the POS as a CAS/CRM; the owner handles registration with her accountant.

## Functional requirements

<!-- Priorities use MoSCoW. Every requirement names the goal it serves and has Given/When/Then criteria. -->

### R-001 Cashier signs in with a PIN

- Priority: Must
- Goals: G-02
- Story: As a cashier, I want to sign in with a 4-6 digit PIN so that every order and cash movement is attributed to me.
- Acceptance:
  - AC1: Given an active cashier with PIN 4821, when she enters 4821 on the sign-in pad, then the order screen opens and her name shows in the header.
  - AC2: Given 5 wrong PIN attempts on one tablet within 10 minutes, when a 6th attempt is made, then sign-in is blocked for 5 minutes and the attempt is logged.
  - AC3: Given a signed-in cashier and 10 minutes without input, when the timer elapses, then the screen locks and the open order is kept.

### R-002 Build an order from the menu grid

- Priority: Must
- Goals: G-01
- Story: As a cashier, I want to tap items and pick modifiers from a grid so that I can build an order without typing.
- Acceptance:
  - AC1: Given the Coffee category is open, when the cashier taps "Spanish Latte" and picks size 16 oz and sugar 50%, then one line "Spanish Latte 16oz, 50% sugar" is added with the price of the 16 oz variant.
  - AC2: Given an item is marked sold out, when the cashier views the grid, then the item is shown as sold out and cannot be added.
  - AC3: Given an order with 3 lines, when the cashier changes the quantity of line 2 to 0, then the line is removed and the total is recomputed.

### R-003 Take a cash payment

- Priority: Must
- Goals: G-01, G-02
- Story: As a cashier, I want the POS to compute change so that I do not do arithmetic at the counter.
- Acceptance:
  - AC1: Given an order total of ₱185.00, when the cashier enters ₱500 tendered, then the screen shows change of ₱315.00 and the order is marked paid (cash).
  - AC2: Given an order total of ₱185.00, when the cashier enters ₱150 tendered, then the payment is refused with "Amount is less than the total".
  - AC3: Given quick-tender buttons, when the cashier taps "₱200", then tendered is set to ₱200.00 without typing.

### R-004 Take a GCash payment through the café's QR

- Priority: Must
- Goals: G-01, G-02
- Story: As a cashier, I want to record a GCash payment with its reference number so that the owner can match it against the GCash transaction history.
- Acceptance:
  - AC1: Given an order total of ₱185.00, when the cashier selects GCash, then the café's merchant QR is shown full-screen with the amount in large text.
  - AC2: Given the GCash screen, when the cashier enters a 13-digit reference number and confirms, then the order is marked paid (GCash) with that reference.
  - AC3: Given a reference number already used today, when the cashier enters it again, then the POS warns "Reference already used on order #0142" and does not save.
  - AC4: Given a split payment, when the cashier records ₱100 cash and ₱85 GCash for a ₱185 order, then the order is paid with two payment lines.

### R-005 Print a receipt

- Priority: Must
- Goals: G-01
- Story: As a cashier, I want a receipt printed automatically after payment so that the customer leaves with proof of purchase.
- Acceptance:
  - AC1: Given a paid order and a paired printer, when payment is confirmed, then a 58 mm receipt prints with the business details from settings, the receipt number, the lines, discounts, VAT breakdown, payment method and change.
  - AC2: Given the printer is off, when payment is confirmed, then the order is still saved, a "Receipt not printed" banner shows, and "Reprint" works once the printer is back.
  - AC3: Given the device is offline, when an order is paid, then the receipt number comes from the device series (for example T1-000123) and has no gaps in that series.

### R-006 Apply a Senior Citizen or PWD discount

- Priority: Must
- Goals: G-04
- Story: As a cashier, I want the POS to compute the SC/PWD discount so that it is correct every time and the details the accountant needs are recorded.
- Acceptance:
  - AC1: Given a ₱168.00 VAT-inclusive item for the senior's own consumption, when the cashier applies the SC discount, then VAT is removed (₱150.00) and 20% is deducted, so the line total is ₱120.00.
  - AC2: Given the discount dialog, when the cashier tries to save without the ID number and name, then saving is refused with "ID number and name are required".
  - AC3: Given an order with an SC discount, when the receipt prints, then it shows the discount type, the ID number, the VAT-exempt sale and the discount amount as separate lines.

### R-007 Void a line or an order with supervisor approval

- Priority: Must
- Goals: G-02
- Story: As a supervisor, I want voids to need my PIN and a reason so that no money leaves the drawer unrecorded.
- Acceptance:
  - AC1: Given a paid order, when the cashier taps "Void order", then the POS asks for a supervisor PIN and a reason from a list.
  - AC2: Given a valid supervisor PIN and reason "wrong item", when confirmed, then the order is marked void, the receipt number stays used, and the void appears in the shift report with both names.
  - AC3: Given a cashier PIN is entered in the supervisor prompt, when confirmed, then the void is refused.

### R-008 Open and close a shift with a cash count

- Priority: Must
- Goals: G-02
- Story: As a supervisor, I want to count the drawer at shift close and see expected versus counted cash so that I find variances the same day.
- Acceptance:
  - AC1: Given no open shift, when the supervisor opens one with a ₱2,000 starting float, then orders can be taken and the float is recorded.
  - AC2: Given a shift with ₱8,450 cash sales and ₱2,000 float, when the supervisor enters counted cash ₱10,420 by denomination, then the POS shows expected ₱10,450 and variance -₱30.
  - AC3: Given unsynced orders on the tablet, when the supervisor tries to close the shift, then the POS says how many orders are waiting and closes only after they sync or the supervisor confirms closing offline.

### R-009 Owner reads the daily report on her phone

- Priority: Must
- Goals: G-03
- Story: As the owner, I want a daily report on my phone so that I know sales, payment mix and best sellers without counting slips.
- Acceptance:
  - AC1: Given a day with synced orders, when the owner opens Reports > Today, then she sees gross sales, discounts, net sales, cash vs GCash totals, voids, order count and the top 10 items.
  - AC2: Given the owner selects a past date, when the report loads, then the figures match the sum of that date's non-void orders to the centavo.
  - AC3: Given a cashier account, when it opens the reports URL, then access is refused (403).

### R-010 Owner manages the menu

- Priority: Must
- Goals: G-01, G-03
- Story: As the owner, I want to add items, change prices and mark items sold out so that the grid always matches what we sell.
- Acceptance:
  - AC1: Given the owner edits the 16 oz Spanish Latte price from ₱165 to ₱175, when she saves, then new orders use ₱175 and past orders keep ₱165.
  - AC2: Given the supervisor marks "Ube Cheesecake" sold out, when the tablet next syncs (within 60 seconds online), then the item shows as sold out on the grid.

### R-011 Keep selling offline

- Priority: Must
- Goals: G-01
- Story: As a cashier, I want to keep taking orders when the internet is down so that the queue does not stop.
- Acceptance:
  - AC1: Given the tablet is offline, when the cashier completes an order, then it is saved on the tablet and a counter shows "3 orders waiting to sync".
  - AC2: Given 40 queued orders, when the connection returns, then all 40 reach the server within 5 minutes and none is created twice.
  - AC3: Given the same order is sent twice because a response was lost, when the server receives the second copy, then it returns the existing order and creates nothing new.

### R-012 Export daily sales to CSV

- Priority: Should
- Goals: G-03
- Story: As the owner, I want to download a date range as CSV so that my accountant can prepare the monthly summaries.
- Acceptance:
  - AC1: Given the owner picks 2026-11-01 to 2026-11-30, when she taps Export, then a UTF-8 CSV downloads with one row per order line including discount type, ID number, VAT-exempt amount and payment method.

## Non-functional requirements

### NFR-01 Performance at the counter

Adding an item updates the order panel in 100 ms or less at p95 on the counter tablet (mid-range Android, 4 GB RAM); the order screen is interactive within 2 s of launch from the home screen. Serves DG-02.

### NFR-02 Offline and sync

Orders, payments and receipts work offline for at least 8 hours and 1,000 orders; queued orders sync within 5 minutes of reconnecting; every order carries a client-generated UUID used as an idempotency key. Serves DG-04.

### NFR-03 Accessibility

Cashier and supervisor screens meet WCAG 2.2 AA; touch targets at least 44 by 44 CSS px; money shown at least 20 px; nothing relies on colour alone. Serves DG-03.

### NFR-04 Security and privacy

PINs and passwords hashed with Argon2id; owner account requires a 12+ character password; roles cashier, supervisor, owner enforced on the server for every endpoint; SC/PWD names and ID numbers are personal information under the Data Privacy Act of 2012 (RA 10173): collected only for the discount record, visible only to supervisor and owner, kept as long as the tax records require, and never shown in logs.

### NFR-05 Maintainability and tests

At least 80% line coverage on the money modules (totals, discounts, payments, shift close); CI runs Pest and the Vitest suite on every push; one-command setup; README runbook. Serves DG-01 and DG-05.

### NFR-06 Money and data integrity

Money is stored as integer centavos; order totals are computed by one server-side function and the client mirror is tested against the same fixtures; receipt numbers are unique per device series with no gaps; daily backups kept 30 days and a restore is tested before launch.
