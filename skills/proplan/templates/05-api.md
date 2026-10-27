---
doc: 05-api
project: <slug>
version: 0.1.0
status: draft
owner: backend-engineer
updated: YYYY-MM-DD
---

<!-- AGKIT2 2.8.0 planning scaffold. Keep machine-readable IDs/fields and use only relevant content. Replace illustrative rows and examples with the actual brief. Do not invent evidence, approvals, dates or locale-specific obligations. Shared core/design/verification rules govern decisions and checks; this template adds no universal approval or task-count gate. -->


# API

## Conventions

<!-- Match actual consumers and framework conventions. Specify identifiers, dates, money, pagination and retry behavior where needed without forcing public versioning on an internal action. -->
## Authentication and authorization

<!-- Define identity and per-resource permission checks with role names aligned to 02/07. Authentication alone does not grant record access. -->
## Error model

<!-- Use a consistent actionable error contract suitable to the stack. The sample shape/statuses are examples; keep caller handling and observability coherent. -->
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

<!-- Bound expensive/abusable operations based on actual traffic and trust boundaries; explain proposed limits. -->
## Endpoint index

<!-- Reference endpoint IDs already defined below. Keep the ID out of the first column to avoid duplicate definitions. -->
| Method | Path | ID | Role |
|---|---|---|---|
| | | | |

## Endpoints

<!-- Define each API ID once with Serves, request/response, authorization and failure/side-effect behavior. Include idempotency/transactions for retried consequential writes. -->
### API-01 <METHOD /path>

- Serves: R-001
- Purpose:
- Auth and role:
- Request:
- Response:
- Errors:
- Notes:

## Webhooks and events

<!-- Document actual integrations, signature/identity validation, duplicate handling, retries and observability. Say inapplicable when none exist. -->
## Versioning and deprecation

<!-- Explain compatibility for real consumers. A coordinated internal deployment can be sufficient; do not add a public API lifecycle unnecessarily. -->
