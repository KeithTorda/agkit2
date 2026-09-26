---
doc: 00-overview
project: cafe-pos
title: Kape Norte Counter POS
set: lite
version: 1.0.0
status: approved
owner: coordinator
updated: 2026-09-27
---

# Kape Norte Counter POS - Plan Overview

## Summary

Kape Norte is a one-branch café in Tuguegarao City with two cashiers per shift and an owner who does the books at night. Orders are written on paper slips, change is computed in the cashier's head, and the owner rebuilds the day's sales from slips and a GCash screenshot folder. This plan covers a counter POS on one Android tablet: menu, orders with modifiers, cash and GCash payments, receipts on a Bluetooth thermal printer, Senior Citizen and PWD discounts, shift cash counts, and a daily report the owner reads from home.

The system keeps selling when the internet drops, which happens several times a week at this location.

| Item | Value |
|---|---|
| Client | Kape Norte (owner: Liza Dela Cruz) |
| Team | 1 developer, 1 part-time tester (the café supervisor) |
| Target launch | 2026-11-16, 7 weeks from plan approval, including 1 week of buffer |
| Plan set | lite (00, 01, 02, 03, 10, TRACEABILITY) |
| Architecture | Laravel 12 API on a small VPS + offline-capable PWA on the counter tablet (ADR-001) |

## Documents

| File | Contents | Owner |
|---|---|---|
| 01-goals.md | Business goals G-01..G-04, development goals DG-01..DG-05, KPIs | product-manager |
| 02-requirements.md | Stakeholders, personas, scope, R-001..R-012, NFR-01..NFR-06 | product-manager |
| 03-architecture.md | Context, containers, stack, data model summary, API summary | solution-architect |
| adr/ADR-001-offline-pwa-with-cloud-api.md | Why a PWA with an offline queue instead of a LAN server or a subscription POS | solution-architect |
| 10-roadmap.md | Milestones M1..M3, tasks T-001..T-019, critical path, risks | project-planner |
| TRACEABILITY.md | Goal to requirement to API to task matrix (generated) | proplan_check.py |

## Key decisions

- Offline-first PWA talking to a cloud API; orders queue in the tablet and sync with idempotency keys (ADR-001).
- GCash through the café's existing static merchant QR; the cashier types the reference number. No payment API integration in this version (R-004).
- Money is stored as integer centavos; totals are computed by one shared function on the server and mirrored in the client (NFR-06).
- Receipt wording and the registered business details are configurable. Whether the printed slip may serve as the official receipt depends on the café's own BIR registration; the owner confirms the wording with her accountant before launch (T-016).

## Assumptions

- One counter tablet (Android, Chrome) and one 58 mm Bluetooth ESC/POS printer; the owner buys both before M2.
- Menu has about 45 items and 6 modifier groups; prices change a few times a year.
- The owner uses her phone for reports; cashiers never need access outside the café.
- Laravel is the developer's strongest stack and the café pays for one small VPS (about ₱600 a month).

## Open questions

None blocking. Receipt wording (T-016) is confirmed with the accountant during M3.

## Next step

Run `/orchestrate docs/proplan/cafe-pos M1` to build milestone M1.

## Changelog

| Version | Date | Change | Affected IDs |
|---|---|---|---|
| 1.0.0 | 2026-09-27 | Plan approved by the owner after the architecture checkpoint | all |
