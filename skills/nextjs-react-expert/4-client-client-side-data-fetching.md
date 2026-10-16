# Client data, subscriptions and storage

Use client fetching when the product or existing architecture needs browser-owned freshness, interaction or offline behavior. Keep an adequate adopted query/store library; adding one is a trade-off, not a universal requirement.

## Rule 4.1: Own subscriptions and cleanup

A subscription needs a stable source, correct snapshot, unsubscribe and reconnect behavior. Multiple component listeners may be acceptable; consolidate when duplication creates a measured cost or correctness issue. React `useSyncExternalStore` can integrate an external store when supported, but it does not automatically deduplicate arbitrary listeners.

Keep server snapshots consistent with initial client rendering. Avoid module-global mutable user data on the server and clear identity-specific subscriptions/state on account changes.

## Rule 4.2: Listeners match their purpose

Use passive listeners when supported and the handler never cancels the event. A gesture handler that needs `preventDefault` cannot be made passive without changing behavior. Scope listeners to the relevant element and clean them up. Throttle/defer work from a measured input cost while preserving responsiveness; passive does not make expensive JavaScript free.

## Rule 4.3: One coherent server-data owner

Query libraries can provide deduplication, retries, invalidation, pagination and optimistic state. Their defaults vary: configure freshness/retry behavior from the endpoint contract and product needs. An infinite stale time or retention is appropriate only when updates/memory are understood.

Keys include dimensions affecting results: resource ID, tenant/actor scope, filters, cursor and locale where relevant. Keep query clients request-scoped on the server and appropriately shared in the browser. Hydration must not serialize data to an unauthorized client.

For a mutation, define pending/duplicate handling, expected errors and the successful read update. Optimistic updates need rollback/reconciliation, especially for concurrent edits. Invalidate or update the actual owner; calling a server action alone does not necessarily refresh every browser cache.

If using plain effects/fetch, guard against stale completion after navigation/input changes. Abort supported work and/or ignore obsolete responses. A cancelled await is not proof the server stopped a write. Pagination must not mix pages from different filter identities.

## Rule 4.4: Browser storage is bounded untrusted state

Store minimal preferences/drafts with a version and recovery policy. Parse stored data defensively; it may be malformed, old, manually edited, unavailable or over quota. Treat storage failure as an expected branch where the experience can recover.

Avoid persisting sensitive credentials by convenience. Follow the adopted identity design: HttpOnly cookies reduce JavaScript token exposure but require appropriate CSRF/session controls; they are not a universal replacement for every token flow. Never assume browser storage is private, authoritative or synchronized across devices.

## Verification

Exercise duplicate views, filter changes during an in-flight request, logout/tenant switch, network failure, retry and stale/empty data. Confirm listeners release and cache/storage do not leak identity-specific data. Measure actual request/render behavior instead of inferring it from a hook name.
