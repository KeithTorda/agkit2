---
name: api-patterns
description: Design or review API contracts, errors, pagination, authorization, retries and compatibility. Use for HTTP endpoints, GraphQL schemas, RPC routers and webhook contracts; preserve the project's protocol and framework unless a change is justified.
version: 2.8.2
---

# API Patterns

Make the client-visible contract explicit, then implement it with the installed stack. Inspect consumers, routes, schemas and authentication before selecting an API style. A framework's server function may serve its own UI; an HTTP API is useful when consumers need that boundary. Neither is mandatory.

## Boundaries and observable behavior

REST suits resource-oriented contracts and broad compatibility. GraphQL lets clients select connected data but adds authorization and query-cost concerns. Typed RPC suits coordinated consumers; shared types do not validate runtime data or prevent deployed-version drift. SSE, WebSocket and streaming HTTP suit different push requirements. Preserve a working protocol unless the outcome needs another.

- Methods/statuses reflect the operation. GET does not cause business mutations. PUT and DELETE have idempotent intended effects; repeated responses need not have identical statuses. PATCH idempotency depends on the patch operation.
- Preserve established names and shapes. For new APIs, choose a consistent success shape and structured errors, such as a project envelope or Problem Details.
- Errors have a stable machine code and user-safe detail; field issues and correlation IDs help recovery. Keep internal traces/secrets out. Do not reveal existence where access policy conceals it.
- Validate query/path/body data at the boundary, including size, allowed fields and coercion. Enforce identity, role, ownership and tenant scope on the server. Return only permitted fields.

For a small endpoint, a concise contract and focused test suffice. Shared/public APIs need schemas, authentication, examples, errors and evolution rules in the project's API docs.

## Lists and compatibility

Bound page sizes and define deterministic ordering. Offset pagination suits page navigation when its consistency/cost trade-offs are acceptable. Cursor/keyset pagination needs stable ordering and a unique tie-breaker; validate cursors and bind them to relevant filters. Explain behavior when records change between pages.

Additive fields can still break strict consumers. Check schemas and deployed clients before changing responses, enums, defaults or nullability. Version a breaking external contract when consumers cannot migrate together; document migration/deprecation. Coordinated internal changes may update callers directly.

## Retries, idempotency and webhooks

Classify whether a retry is safe. For repeat-sensitive writes, use an idempotency key or business uniqueness constraint. Scope keys to actor/tenant and operation, bind them to a request fingerprint, reject conflicting reuse, and make deduplication atomic with the effect. Persist status/results for the actual retry window. Test concurrent duplicates and crashes after commit.

Verify webhook signatures using the provider's documented raw-body, timestamp and replay rules. Record event identity atomically with processing or durable enqueue. Acknowledge acceptance only after required work is durably committed; make asynchronous consumers idempotent. Test duplicate, out-of-order and retried events.

## Capacity and security

Apply body, upload, time and query-cost bounds appropriate to the endpoint. Rate limits need a trustworthy identity/proxy model and shared accounting when instances share a budget. Use header/status syntax supported by the actual server and clients; do not assume a draft syntax is universal. Retry eligible failures with deadlines and bounded backoff.

Cookies, bearer tokens, keys and delegated identity solve different problems. Follow existing authentication; verify issuer/audience/lifetime where relevant. Check CSRF for cookie-authenticated writes, CORS for browser access, and authorization independently of either. Read [security-testing.md](security-testing.md) for a focused access/failure matrix.

## Verification and helper

Exercise success, invalid input, denied access, empty results and important dependency/retry failures. Check a real consumer when shared shapes change. Keep generated API schemas consistent with runtime behavior using existing tooling.

`python "KIT/skills/api-patterns/scripts/api_validator.py" .` checks route/spec patterns. Supports `--json`, `--verbose`, `--fail-on error|warning|never`. Expand `KIT` to the active path. It is heuristic: investigate warnings; a clean scan does not prove contract correctness.
