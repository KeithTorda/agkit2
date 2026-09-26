---
adr: ADR-001
title: Offline-capable PWA on the counter tablet with a cloud Laravel API
status: accepted
date: 2026-09-27
deciders: Liza Dela Cruz (owner), developer
---

# ADR-001: Offline-capable PWA on the counter tablet with a cloud Laravel API

## Status

Accepted on 2026-09-27 at the architecture checkpoint.

## Context

The café's internet drops several times a week, sometimes for hours, and selling must not stop (NFR-02). The owner wants reports on her phone from home (R-009). There is one developer and no IT staff on site, and the budget allows about ₱600 a month for hosting. Money must be exact and receipts must not skip numbers (NFR-06).

## Options

### Option A: Offline-capable PWA + cloud API (chosen)

- Tablet stores the menu and queues orders in IndexedDB; the Laravel API on a VPS is the system of record.
- Pros: owner reports from anywhere; no hardware to maintain in the café beyond the tablet and printer; one codebase for cashier and owner screens.
- Cons: offline sync, idempotency and device receipt series must be built and tested; printing depends on Web Bluetooth, so the tablet must run Chrome on Android.
- Cost: VPS about ₱600 a month; about 5 extra development days for the sync layer.

### Option B: Laravel server on a mini PC in the café (LAN only)

- Pros: internet outages do not matter for selling; printing from the server over USB or LAN is simple.
- Cons: the owner cannot see reports from home without a tunnel or a second cloud copy; hardware in a hot café with brownouts needs a UPS and someone to restart it; backups depend on the mini PC being healthy.
- Cost: about ₱18,000 hardware + UPS; less sync code but more on-site support.

### Option C: Subscription POS app (off the shelf)

- Pros: ready in days; offline mode and receipts included.
- Cons: SC/PWD computation and receipt wording are not under our control; per-device monthly fee in foreign currency; exporting data for the accountant depends on the vendor; does not meet the owner's wish to own her data.
- Cost: subscription per device per month; no development.

## Decision

Option A. It is the only option that meets both "selling never stops" and "reports from home" without on-site hardware to maintain. The sync risk is contained by client UUIDs as idempotency keys, a per-device receipt series, and a Playwright test that runs a full checkout with the network disabled.

## Consequences

- The counter tablet must be Android with Chrome (Web Bluetooth); the owner buys a supported printer before M2 (RK-02).
- Sync, idempotency and the device receipt series become Must work in M2 (T-008, T-009).
- Total and discount rules exist in two places (PHP and TypeScript); both run the same JSON fixtures in CI (T-006).
- If the café later adds a second counter, each device gets its own receipt series; no redesign needed.
- Revisit if the owner wants a kitchen display or a second branch; Option B's LAN server might then be added as a local relay.
