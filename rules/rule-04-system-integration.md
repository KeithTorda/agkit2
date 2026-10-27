---
name: rule-04-system-integration
version: 3.0.0
priority: P0
trigger: glob
globs: "**/app/Http/**, **/app/Models/**, **/app/Services/**, **/app/Jobs/**, **/app/Actions/**, **/database/**, **/migrations/**, **/routes/**, **/api/**, **/server/**, **/prisma/**, **/drizzle/**, **/*.sql, **/docs/plans/**, **/proplan/**, **/outbox*, **/sync*, **/webhook*"
description: Rule 04 - apply when designing or building a new system, an add-on module (POS, SFA, HRIS, inventory, e-invoicing), an API between systems, database ownership, sync jobs, webhooks or reconciliation. ERP <-> add-on integration pattern (Option B).
---

# RULE 04 — SYSTEM INTEGRATION (OPTION B)

Every new system is designed as an **add-on** that integrates with a **core system of record** (for MyBizMate: the core ERP). This applies to POS, SFA, HRIS and every other new system.

If no core system exists yet, still use a separate database, an outbox table and a versioned API so the system can plug into one later. Do not invent ERP endpoints; mark them as "to be confirmed with the ERP owner".

## 1. Separate databases

- Each system has its own database. No system reads or writes another system's tables directly.
- No shared database users across systems. No cross-database joins.

## 2. One owner per table

| Data | Owner | Others |
|---|---|---|
| Master data: customers, items/products, prices, branches, users, chart of accounts, tax settings | Core ERP | Read-only local copy, updated by sync |
| Transactions created in the add-on: sales, receipts, orders, attendance, visits | The add-on | ERP receives them through sync |

- Only the owner creates, updates or deletes its records. A non-owner that needs a change calls the owner's API.
- Local copies of master data store the owner's ID (`erp_item_id`) and a `synced_at` timestamp.

## 3. Add-on → ERP: outbox + middleman (realtime)

1. In the same database transaction that saves the business record, insert a row into the add-on's `outbox` table (`id`, `event_type`, `aggregate_id`, `payload` JSON, `idempotency_key`, `status`, `attempts`, `next_attempt_at`, `last_error`, `created_at`).
2. A middleman worker reads pending outbox rows in order per `aggregate_id`, calls the ERP API, and marks them `sent` on success.
3. Retries use exponential backoff with a max attempt count; after that the row becomes `failed` and is visible on an admin screen for manual retry.
4. Every call sends an `Idempotency-Key` header. The ERP stores processed keys and returns the original result for a repeated key, so retries never create duplicates.
5. Never call the ERP directly inside the user's request and fail the sale because the ERP is down. The add-on keeps working offline-from-ERP and syncs later.

## 4. ERP → add-on: webhooks + nightly reconciliation

- The ERP sends webhooks for master-data changes (`item.updated`, `price.updated`, `branch.created`...). Webhooks are signed (HMAC with a shared secret) and verified before processing.
- Webhook handlers are idempotent (same event twice = same result) and respond fast; heavy work goes to a queue.
- A nightly reconciliation job compares master data (counts + updated_at or checksums) and fixes drift. It logs what it changed.

## 5. Versioned API contract

- All integration endpoints are versioned: `/api/v1/...`. A breaking change ships as `/api/v2/...`; the old version stays until every consumer has moved.
- The contract (endpoints, payloads, error codes, webhook events) is written in the project docs (`/proplan` `05-api.md`, `docs/api/`, or the API summary in `03-architecture.md` for lite plans).
- Errors use one consistent JSON shape with a machine-readable `code`.

## 6. Checklist for any integration design

- [ ] Which system owns each table?
- [ ] Which events go add-on → ERP (outbox) and ERP → add-on (webhook)?
- [ ] What is the idempotency key for each event?
- [ ] What happens when the other system is down for an hour? For a day?
- [ ] What does nightly reconciliation compare and fix?
- [ ] Is the API versioned and documented?

## Before you answer, check

- [ ] Each table has one owning system; the add-on writes only its own tables.
- [ ] Add-on → ERP changes go through the outbox with an idempotency key.
- [ ] ERP → add-on changes come by signed webhook plus nightly reconciliation.
- [ ] Endpoints are under `/api/v1/...` and documented.
