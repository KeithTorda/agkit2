---
part: 32
title: Backend, API, and data integrity
covers: architecture, contracts, validation, authorization, secrets, logging, SQL, schema, transactions, payments, jobs, BaaS, privacy
---

# 32 - Backend, API, and data integrity

Read for server handlers, APIs, schemas, migrations, payments, background work, and access control. These concerns are correctness boundaries, not aesthetic preferences. Adapt details to the real stack and risk.

## Structure and API contracts

Use layers that clarify actual responsibilities. A small route can call a data function directly; complex business rules or multiple callers may justify a service/repository boundary. Follow framework conventions and avoid forwarding layers that add no useful contract. Do not ban a conventional class or envelope simply because it appears in boilerplate.

Keep request/response shapes, status codes, names, and pagination consistent with the API's actual contract. Use HTTP semantics appropriately and distinguish invalid input, unauthenticated, unauthorized, missing, conflict, rate-limited, and server failures. Nested routes and envelopes can be valid; avoid arbitrary depth restrictions and unexplained duplicate wrapping. Document errors and compatibility changes.

## Validate and authorize

Validate external input at server boundaries with appropriate types, ranges, size limits, formats, and allowed fields. Client validation is a usability aid, not enforcement. Prevent mass assignment. Derive user, role, tenant, and authoritative prices from trusted state rather than accepting them from the request body.

Authorize every sensitive operation and resource access, including exports, background jobs, uploads, and object storage. Test cross-user and cross-tenant access. UI hiding and CORS do not enforce authorization. Use secure session/token handling, appropriate cookie settings, CSRF protection where the architecture needs it, and abuse limits proportionate to the endpoint. Use the identity system's supported reset and recovery mechanisms.

## Secrets, errors, and logs

Keep private credentials in server-side secret/configuration mechanisms. Client-exposed environment prefixes are public. Do not commit real secrets, print environment dumps, or log passwords, tokens, OTPs, authorization headers, or unnecessary personal records. A variable existing is not proof that its value is valid or authorized for the task.

Return safe, actionable errors and preserve diagnostic cause/context internally. Use correlation IDs where useful. Limit request-body logging and centralize redaction. Avoid exposing stack traces or database internals to public clients.

## Database design and concurrency

Parameterize queries rather than concatenating untrusted input. Validate dynamic identifiers against an allowlist when parameterization cannot represent them. Use constraints, foreign keys, unique indexes, and transactions to protect invariants rather than relying solely on UI checks.

Choose indexes from query patterns and measured plans. Avoid N+1 loading, unbounded result sets, and fetching every column by reflex. Keep pagination stable enough for the workflow. Handle concurrent edits, inventory changes, uniqueness races, and partial failure with appropriate transactions, locking, version checks, or idempotency.

Use an exact financial representation such as integer minor units or suitable decimal types. Treat identifiers as strings when leading zeros matter. Keep instants, local schedules, and date-only values distinct. Schema and retention choices such as soft deletion should follow the domain, audit, and legal requirements rather than a universal template rule.

Use a forward migration for applied shared schema changes. Plan data migration and rollback/recovery where risk warrants it. Seed data should be intentionally scoped; development fixtures must not silently create realistic production identities or financial records. Some production reference-data migrations are legitimate and should be handled as explicit operations.

## Payments, webhooks, and background jobs

Verify webhook authenticity and authoritative payment status. Deduplicate repeated callbacks and requests; a timeout may mean an operation completed but its response was lost. Use idempotency keys, transactions, and reconciliation as the provider/domain requires. Do not trust client totals or a payment screenshot as settlement proof.

Preserve appropriate financial/audit history. Refund, void, cancellation, and deletion have different meanings; implement the actual business rules and current requirements. Do not invent universal receipt numbering, tax, or retention rules.

Background email/SMS/jobs need bounded retries, appropriate backoff, duplicate prevention, observable failure, and protection of personal data. Drafting a message does not itself authorize sending it.

## Managed backends and review

For Supabase, Firebase, or another managed backend, inspect real policies, storage rules, server credentials, and client privileges. Use the relevant available platform workflow. A configured SDK does not prove row-level authorization is correct.

Verify the changed contract and sensitive boundaries, including failure, duplicate delivery, concurrency, and unauthorized access where relevant. Report what was exercised and what remains untested. No checklist can guarantee a system has no errors or security weaknesses.
