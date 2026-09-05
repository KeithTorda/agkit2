---
name: api-patterns
description: API design decisions - choosing REST, GraphQL, or tRPC, resource naming and status codes, response and error envelopes, pagination, idempotency for mutations and webhooks, versioning, authentication choices, rate limiting with IETF RateLimit headers, and OpenAPI documentation. Use when designing or reviewing an HTTP API, a Route Handler set, a GraphQL schema, or a tRPC router, and before writing endpoint code.
version: 2.0.0
---

# API Patterns

Decide the shape of the API before writing handlers: who consumes it, which style fits, what every response looks like, and how it evolves. Implementation guidance lives in `@[skills/nodejs-best-practices]` and `@[skills/python-patterns]`; data modelling in `@[skills/database-design]`; attack testing in `./security-testing.md`.

## 1. Choose the style

| Consumers | Pick | Why |
|-----------|------|-----|
| Public API, many platforms, third parties | REST + OpenAPI | Widest compatibility, HTTP caching, tooling |
| Complex, interconnected data; several frontends with different needs | GraphQL | Clients shape queries; no over/under-fetching |
| TypeScript on both ends in one repo, internal product | tRPC | End-to-end types with no schema file or codegen |
| Real-time, event streams | WebSocket / SSE (+ AsyncAPI) | Push, not poll |
| Internal service-to-service | gRPC (performance) or REST (simplicity) | |

Questions that settle it: Who calls this? Is the frontend TypeScript in the same repo? How deep are the data relationships? Does HTTP caching matter? Public or internal? Next.js apps usually need no separate API for their own UI (Server Components + Server Actions); add REST only for external consumers or mobile clients.

GraphQL fits poorly for simple CRUD, heavy file uploads, or teams new to it; guard it with max query depth, cost analysis, batch limits, and introspection off in production. tRPC fits poorly for non-TypeScript clients and public APIs; common hosts are Next.js, React Router 7 (framework mode), and any TS backend.

## 2. REST conventions

- Resources are plural nouns in lowercase-hyphen form: `/users/123/posts`, at most three levels deep; no verbs (`/getUsers`).
- Methods: `GET` read (idempotent), `POST` create, `PUT` replace, `PATCH` partial update, `DELETE` remove (idempotent).
- Status codes: 200 read/update, 201 created, 204 no content, 400 malformed, 401 unauthenticated, 403 forbidden, 404 not found, 409 conflict, 422 validation, 429 rate limited, 500 server fault.

## 3. Responses, errors, pagination

Pick one response shape and use it everywhere: an envelope `{ data, error, meta }` or bare resources with RFC 9457 problem details for errors (`application/problem+json` with `type`, `title`, `status`, `detail`, `instance`). Every error carries a machine code, a user-safe message, optional field-level details, and a request id; never internal stack traces. The failure mode to avoid is a different error shape per endpoint — the client then cannot handle errors generically.

```jsonc
// WRONG - three endpoints, three shapes, wrong statuses
POST /login   -> 200 { "success": false, "msg": "bad password" }   // 200 for a failure
GET  /users/9 -> 404 "Not found"                                    // bare string
POST /orders  -> 400 { "errors": ["qty must be > 0"] }             // 400 for a validation error

// RIGHT - one envelope everywhere; status matches semantics, code is stable, message is safe
POST /login   -> 401 { "error": { "code": "invalid_credentials", "message": "Email or password is incorrect", "request_id": "req_a1b2" } }
GET  /users/9 -> 404 { "error": { "code": "not_found",           "message": "User not found",                "request_id": "req_c3d4" } }
POST /orders  -> 422 { "error": { "code": "validation_failed",   "message": "Order is invalid", "fields": { "qty": "must be greater than 0" }, "request_id": "req_e5f6" } }
```

Pagination: offset (`?page=2&limit=20`) only when users jump to arbitrary pages and the set is small — it drifts when rows are inserted or deleted between requests, skipping or repeating items. Cursor (`?after=<opaque>&limit=20`) for large or frequently changing lists and for mobile clients; keyset when a sortable unique key exists and performance is critical. Return `next_cursor` (null at the end) and a stable sort.

## 4. Idempotency and retries

Networks retry. Any non-idempotent mutation (`POST`, and `PATCH` that is not naturally idempotent) needs a dedupe key so a retry does not charge the card or create the order twice.

- **Client-driven mutations:** accept an `Idempotency-Key` request header (a client-generated UUID). Store `key -> {status, response}` for a window (24h is typical). On a repeat key, return the stored response instead of re-executing; if the first request is still in flight, return `409`. Scope keys per user and endpoint.
- **Inbound webhooks:** dedupe on the provider's event id (Stripe `event.id`, etc.), never on receipt time — providers redeliver. Verify the signature first, record the event id, ignore ids already seen, return `2xx` fast, and process asynchronously (queue guidance in `@[skills/nodejs-best-practices]`).
- `GET`, `PUT`, and `DELETE` are idempotent by definition — keep them so. A `DELETE` on an already-deleted resource returns `204`/`404`, not an error that breaks the caller's retry.

## 5. Versioning

| Strategy | Form | Use |
|----------|------|-----|
| URI | `/v1/users` | Public APIs; explicit and cacheable |
| Header | `Accept: application/vnd.acme.v2+json` | Cleaner URLs, harder to discover |
| None, additive changes only | | Internal APIs, GraphQL (evolve the schema, deprecate fields), tRPC (types enforce compatibility) |

Never remove or rename a field in place; add the new one, deprecate the old, remove after consumers migrate.

## 6. Authentication

| Pattern | Use |
|---------|-----|
| Session cookie (httpOnly, SameSite) | Browser apps on the same site; the default for Next.js with Better Auth or Clerk (Auth.js in existing projects) |
| JWT access + refresh | Mobile clients, separate API domains, microservices; short expiry, verify signature and `exp`/`iss`/`aud`, minimal claims, rotate refresh tokens |
| OAuth 2.0 / OIDC (with PKCE) | Third-party login and delegated access |
| API keys | Server-to-server and public API tenants; hash at rest, scope, and rotate |
| Passkeys (WebAuthn) | Passwordless user login |

Authorize on every request inside the handler (Route Handler, Server Action, resolver), not only in middleware; check ownership, not just identity.

## 7. Rate limiting

Token bucket for most APIs (allows bursts), sliding window for strict limits, fixed window for simple cases. Limit per API key or user after auth and per IP before; stricter limits on auth and expensive endpoints. Return 429 with `Retry-After`.

Headers: the IETF draft standard `RateLimit-Policy` (the policy, for example `"default";q=100;w=60`) and `RateLimit` (current state: `limit`, `remaining`, `reset` in seconds). Many providers still send the legacy `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`; emit those too if existing clients read them.

## 8. Documentation

Generate OpenAPI 3.1 from code or schemas (Zod/Pydantic) rather than by hand; include auth requirements, request and response examples, error formats, and rate-limit rules. A good developer page has a quick start, an auth guide, the reference, an error guide, and a changelog.

## 9. Checklist before coding

- Consumers named; style chosen for this context.
- Response and error shape fixed; pagination type chosen.
- Mutations accept an idempotency key; webhooks dedupe on event id.
- Versioning and deprecation policy written down.
- Auth pattern chosen; authorization inside every handler.
- Rate limits and headers defined.
- OpenAPI (or schema) is the source of truth for docs.

## 10. Script (advisory)

`./scripts/api_validator.py <project>` finds route, controller, and OpenAPI files and reports missing error handling, status codes, input validation, auth, rate limiting, and logging by keyword search. It is heuristic (it matches file names containing `api` and detects auth by words like `token`); use its report as a review prompt, not a verdict.

```powershell
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/api-patterns/scripts/api_validator.py .
```
