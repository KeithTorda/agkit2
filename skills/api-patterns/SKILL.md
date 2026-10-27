---
name: api-patterns
description: Use when designing, building or reviewing an HTTP API, webhook or integration endpoint - routes, payloads, errors, pagination, auth and retries.
version: 3.2.0
---

# API Patterns

Write the contract first, then implement it in the project's existing framework. Integration endpoints follow rule-04-system-integration (Option B); security follows rule-06-security-baseline.

## Steps

1. Read the existing routes, controllers, validators, auth middleware and API docs. Keep the protocol and response shape the project already uses.
2. Write the contract in the project docs before coding: method, path, request body, success response, error codes, auth, example. New endpoints go under `/api/v1/...`; ship a breaking change as `/api/v2/...` and keep v1 running until consumers move.
3. Use methods honestly: GET reads, POST creates or triggers, PUT/PATCH updates, DELETE removes (or voids, for money records).
4. Return errors in one JSON shape with a stable machine `code`, a user-safe `message` and optional per-field `errors`. Map statuses: 400/422 invalid input, 401 not signed in, 403 not allowed, 404 not found, 409 conflict, 429 rate limited.
5. Validate every input at the boundary (Laravel Form Request, Zod). Check permission for the specific record on the server and return only fields the caller may see.
6. Lists: cap the page size, sort deterministically (add `id` as a tie-breaker), and use cursor pagination for large or fast-changing tables.
7. Writes that a client or worker may repeat: accept an `Idempotency-Key` header, store key + request hash + response atomically with the write, return the stored response on a repeat, and return 409 when the same key arrives with a different body.
8. Add-on to ERP sync: save the record and its `outbox` row in one transaction; the middleman worker sends it later with the idempotency key. The user's request does not wait on the ERP.
9. Incoming webhooks: verify the HMAC signature on the raw body, record the event ID, queue heavy work, reply fast, and handle duplicates and out-of-order events.
10. Update the API doc (`docs/api/` or `05-api.md`) in the same change.

## Stack notes

- Laravel specifics (Form Requests, API Resources, Sanctum, route versioning, queued jobs) live in the `laravel-patterns` skill.
- Next.js: Route Handlers under `app/api/v1/`; validate with Zod; server actions are fine for the app's own UI and do not replace a versioned API for other systems.
- Security cases to test (ownership, tenant scope, CSRF, expired tokens): [security-testing.md](security-testing.md).

## Helper

`python "KIT/skills/api-patterns/scripts/api_validator.py" .` scans routes and specs for common pattern issues (`--json`, `--verbose`, `--fail-on error|warning|never`). Run it when the user asks for a check; treat its output as hints.

## Before you finish, check

- [ ] The contract (paths, payloads, error codes) is written in the project docs and versioned under `/api/v1`.
- [ ] Every write that can be retried has an idempotency key or a unique constraint.
- [ ] Cross-system writes go through the outbox, and webhooks are signature-checked and idempotent.
- [ ] Permission is checked per record on the server, and errors use the shared JSON shape.
