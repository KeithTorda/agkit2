---
part: 22
title: Dashboards and operational screens
covers: dashboard purpose, KPIs, CRUD, filters, bulk actions, settings, permissions, audit logs, exports, POS, inventory, institutions
---

# 22 - Dashboards and operational screens

Read when designing operational software. Efficiency, clear state, and correct data matter, but an admin interface does not have to be gray, plain, or devoid of brand. Follow the chosen direction and the work people actually do.

## Start with the workflow

Identify frequent tasks, decisions, user roles, data volume, and important exceptions. A dashboard should help a user orient or act. Some users need metrics and trends; others should land directly on a queue, table, editor, or sale screen. Do not require a greeting, chart, KPI row, or universal dashboard homepage.

Show meaningful metrics with period, unit, source, and comparison basis. Color, icons, charts, and cards can support scanning. Avoid fabricated counts, decorative charts unrelated to decisions, and trend arrows without calculations. Use useful empty, loading, stale, and error states.

## CRUD, filters, and bulk operations

A record screen needs a clear name, useful identifiers, search/filter behavior, relevant actions, and a detail or edit path. Choose table, list, cards, or another view from actual comparison and interaction needs. Preserve selection, sorting, filter state, and navigation context where useful.

Bulk actions must identify their scope, including selected page versus all filtered records. Confirm impact when warranted and report partial failures accurately. Avoid optimistic claims for irreversible or financial actions. Retry should not repeat already completed effects.

Forms and settings need clear save behavior: immediate updates and batched save are both valid when communicated consistently. Warn or preserve drafts when navigation would discard meaningful work. Settings groups should reflect the user's mental model rather than the database schema alone.

## Roles, audit, and exports

Permission UI should explain availability without suggesting that hiding a control enforces security. Authorize each server operation and resource access. Do not rely on a client-supplied role or tenant ID.

Audit history should record the actor, action, affected object, and time appropriate to the domain, with secure access and careful handling of sensitive data. A decorative activity feed is not an audit trail. Avoid exposing secrets or complete personal records in logs.

Exports should respect filters, permissions, currency, dates, and data volume. Show actual generation state, support useful errors, and protect downloads appropriately. Spreadsheet-formula injection can affect exported user-provided text; account for it in the chosen export format.

## POS, inventory, and institutional workflows

POS needs usable scan/keyboard/touch flow, clear line items, quantities, discounts, taxes where applicable, payment state, totals, and change. Keep critical values accessible during the transaction. Handle duplicate submission, offline constraints, reconciliation, refunds, and voids according to real business rules.

Inventory needs actual units, stock locations, movements, thresholds, reservations, and source of truth. Prevent lost updates and negative stock when the domain disallows it. Display stale data honestly rather than promising perfect real-time inventory from periodic polling.

School, barangay, and LGU administration should use real forms, service requirements, roles, and records. Protect personal and student information. Do not invent official receipt formats, legal obligations, or voter data; verify current authoritative requirements where needed.

## Visual craft and review

Choose density, typography, section hierarchy, persistent navigation, and visual emphasis for the operating environment. Rich branding, mixed surfaces, iconography, dark themes, and animation are valid if they preserve clarity and performance. Test representative data, long records, small screens where supported, keyboard operation, permission boundaries, and actual error paths. Do not label the whole app verified from a screenshot of the overview page.
