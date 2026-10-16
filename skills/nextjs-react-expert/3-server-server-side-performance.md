# Server correctness, data cost and lifetimes

Use server traces and real data before changing caches or request structure. Server rendering can still issue N+1 queries, expose fields, block on unrelated dependencies or share state across users.

## Rule 3.1: Treat every mutation as an entry point

Server actions, handlers and resolvers require boundary validation plus authentication and operation/resource/tenant authorization. Middleware or hidden buttons alone are insufficient. The safe order depends on information-leak policy and validation cost; do not mandate expensive body parsing before authentication for every endpoint.

A conceptual mutation sequence is: establish actor, parse allowed input, authorize access/transition, perform the coherent transaction, then invalidate relevant read state. Validate again at authoritative boundaries where needed. Return expected domain errors in the project's supported shape and keep internal exceptions secret-safe.

## Rule 3.2: Send an explicit client contract

Pass the fields the client is allowed to receive. Large ORM objects may contain secrets, unsupported values or lazy relations. Projection improves security/clarity and may reduce serialization; verify the actual RSC payload rather than assuming object identity deduplicates all copies.

Do not over-fragment props merely to save a few bytes while making the component contract unclear. Check which serialization types the installed framework supports.

## Rule 3.3: Choose cache scope deliberately

Request memoization deduplicates work within a supported request/render boundary. Process-local caches can span requests, be duplicated across workers or disappear after redeploy/cold start. Distributed/framework caches have different invalidation, consistency and cost. None is automatically suitable for current-user state.

Keys must include relevant actor/tenant/permission/locale dimensions or the cached function must be genuinely public. Bound memory, expiry and negative results. Consider concurrent misses, outages and permission changes. An LRU cache is not a durable store or guaranteed cross-instance cache.

## Rule 3.4: Reduce actual data work

Project required fields, bound lists and remove measured N+1. Inspect query plans and transaction/isolation semantics. A server component querying the database directly can be appropriate; an internal HTTP hop is not mandatory. Preserve a real API boundary when multiple clients or architecture requires it.

## Rule 3.5: Compose independent work

Components/loaders can start independent authorized reads concurrently when framework semantics allow it. Confirm the actual waterfall; wrappers, session reads and nested loaders may still serialize. Balance concurrency with connection-pool/upstream capacity. See [1-async-eliminating-waterfalls.md](1-async-eliminating-waterfalls.md).

## Rule 3.6: Verify memoization semantics

APIs such as React `cache` have environment-specific lifetime and key behavior. Check installed documentation and whether callers share the same wrapper/function identity. Stable primitive arguments may make keys easier to reason about; object inputs are not inherently wrong when the actual key semantics support them.

Do not assume request memoization persists across requests or that persistent caches handle private data safely. Cache failure behavior and invalidation matter as much as hit rate.

## Rule 3.7: Separate optional from durable effects

A supported post-response callback may be suitable for best-effort telemetry. Check host lifetime/error handling; work may be lost and request data access may be constrained. Payments, required notifications and state transitions need a durable workflow/outbox when loss is unacceptable.

See [9-cache-components.md](9-cache-components.md) before adopting framework caching. Verify access isolation, fresh reads after mutation, timeout behavior and comparable server latency after changes.
