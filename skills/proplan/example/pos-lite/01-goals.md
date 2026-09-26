---
doc: 01-goals
project: cafe-pos
version: 1.0.0
status: approved
owner: product-manager
updated: 2026-09-27
---

# Goals

## Problem

Checkout is slow at the morning rush (about 90 seconds per order, measured over 20 orders on 2026-09-22), the end-of-day cash count is often off by several hundred pesos with no way to find why, SC/PWD discounts are computed by hand and sometimes wrongly, and the owner spends about an hour every night tallying paper slips.

## Business goals

### G-01 Faster checkout

- Target: median time from first item tapped to receipt printed is 45 seconds or less.
- Baseline: about 90 seconds (paper slip + mental change computation).
- Deadline: measured over the second full week after launch.
- Measured by: KPI-01.

### G-02 Cash that reconciles

- Target: shift-close cash variance within ₱50 on at least 90% of shifts.
- Baseline: owner estimates variance above ₱200 on about half of the days.
- Deadline: first full month after launch.
- Measured by: KPI-02.

### G-03 Owner sees the day without tallying

- Target: the daily sales report is available on the owner's phone by 21:00 every operating day, with no manual counting.
- Baseline: about 60 minutes of manual tallying each night.
- Deadline: from launch day.
- Measured by: KPI-03.

### G-04 Statutory discounts applied correctly

- Target: 100% of Senior Citizen and PWD discounts in the monthly sample are computed correctly (20% discount on the VAT-exempt price, with the ID details recorded).
- Baseline: owner found 3 wrong computations in a 30-slip sample in August.
- Deadline: first month-end after launch.
- Measured by: KPI-04.

## Development goals

### DG-01 Tested money paths

Automated tests cover at least 80% of lines in the order-total, discount, payment and shift-close modules, and every Must requirement has at least one feature test. Traced by NFR-05.

### DG-02 Fast at the counter

Adding an item to the order updates the screen in 100 ms or less (p95) on the counter tablet; the order screen is interactive within 2 seconds of opening the app. Traced by NFR-01.

### DG-03 Accessible cashier screens

Cashier screens meet WCAG 2.2 AA, with touch targets at least 44 by 44 CSS px and text contrast at least 4.5:1, so they stay usable under bright morning light. Traced by NFR-03.

### DG-04 Selling survives outages

The counter keeps taking orders for at least 8 hours without internet; no order is lost or duplicated when it syncs. Traced by NFR-02.

### DG-05 Maintainable by one developer

One repository, one-command local setup (`composer setup`), a README runbook for backup restore and printer pairing, and CI running tests on every push. Traced by NFR-05.

## Success metrics

| KPI | Metric | Source | Target | Review |
|---|---|---|---|---|
| KPI-01 | Median seconds from first item to receipt printed | order timestamps (created_at to printed_at) | 45 s or less (G-01) | weekly for the first month |
| KPI-02 | Share of shifts with cash variance within ₱50 | shift close records | 90% or more (G-02) | monthly |
| KPI-03 | Days the report was ready by 21:00 | report generation log | every operating day (G-03) | monthly |
| KPI-04 | Correct SC/PWD computations in a 30-order sample | discount records vs manual recomputation | 30 of 30 (G-04) | monthly |
