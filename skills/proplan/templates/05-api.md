---
doc: 05-api
project: <slug>
version: 0.1.0
status: draft
owner: backend-specialist
updated: YYYY-MM-DD
---

<!--
Owner: backend-specialist (Phase 3). Input: 02-requirements, 03-architecture, 04-data-model, 07 authorization matrix when available.
IDs defined here:
  API-01 ...  one heading per endpoint (or per closely related pair): "### API-04 PUT /orders/{uuid}".
Each API section names the R-ids it serves on a "Serves:" line; the traceability matrix reads them.
Do not define API ids in a summary table as well (the checker reports duplicates). The index table below puts the ID in the third column for that reason.
For a server-rendered app with few JSON endpoints (Laravel Blade, Livewire), list the routes and form posts that change data; the same fields apply.
-->

# API

## Conventions

<!--
- Base URL and versioning (/api/v1; how breaking changes are introduced).
- Format: JSON, UTF-8, field naming (snake_case or camelCase; pick one).
- Dates in ISO 8601 with offset; money as integer centavos or string decimals; never floats.
- Pagination (cursor or page/per_page), filtering and sorting parameters.
- Idempotency for retried writes (Idempotency-Key header or client UUIDs).
-->

## Authentication and authorization

<!-- Mechanism (session cookie, Sanctum or JWT bearer token, API key for machines), token lifetime and refresh, where roles are checked (server, every endpoint), how the matrix in 07 maps to endpoints. -->

## Error model

<!-- One shape for all errors, and the codes the client must handle. -->

```json
{ "error": { "code": "validation_failed", "message": "Readable message", "fields": { "amount": ["Must be at least 1"] } } }
```

| HTTP | Code | When |
|---|---|---|
| 400 | bad_request | malformed JSON or parameters |
| 401 | unauthenticated | missing or expired credentials |
| 403 | forbidden | authenticated but role not allowed |
| 404 | not_found | resource does not exist or is not visible to this user |
| 409 | conflict | state conflict (already closed, duplicate) |
| 422 | validation_failed | field validation errors |
| 429 | rate_limited | too many requests; Retry-After header |
| 500 | server_error | unexpected; logged with a request id |

## Rate limits

<!-- Per route group: sign-in, public forms, exports. -->

## Endpoint index

| Method | Path | ID | Role |
|---|---|---|---|
| | | | |

## Endpoints

### API-01 <METHOD /path>

- Serves: R-001
- Purpose:
- Auth and role:
- Request:
- Response:
- Errors:
- Notes: <!-- idempotency, side effects (emails, jobs), audit events written, performance expectation -->

## Webhooks and events

<!-- Incoming webhooks (payment provider callbacks: signature check, replay protection, idempotent handling) and outgoing events. -->

## Versioning and deprecation

<!-- How long old versions live, how clients are told. For an internal app with one client, "breaking changes ship with the client in the same deploy" is a valid policy; say so. -->
