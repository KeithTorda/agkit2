# Select boundaries and patterns

Choose a pattern because it resolves an observed or required problem. Compare with a simpler viable option; include ongoing failure/operating cost, not only a diagram's neatness. The same system may combine several patterns.

## Deployment boundary

A single deployment keeps coordination and transactions straightforward. Modules can provide ownership without introducing a network. Separate services may be justified by independent release, scaling, isolation, runtime or organizational requirements. Validate that the team can operate their authentication, tracing, rollout, retries and recovery.

A modular monolith is often a candidate, not a universal answer. Service extraction is easier only when data/contract boundaries are real; it can require substantial migration even with tidy folders.

## Data access boundary

Direct ORM/query usage can be the clearest option. Query objects help encapsulate complex/important reads. A repository/interface is useful when it expresses a domain boundary, multiple implementations or a genuine test seam. Wrapping every ORM method one-to-one often adds little, but a single implementation can still protect an important architectural boundary.

Use an actual transaction for state changes that must commit together. Avoid external calls inside a retriable transaction unless semantics are deliberately safe. An outbox/job system can bridge durable state and asynchronous work when the requirements justify it.

## Business logic boundary

A transaction script/action can express a straightforward use case. Richer domain objects or state machines help when multiple operations share invariants and transitions. Do not select full domain-driven design for prestige or reject a useful state machine because its state count is small. Choose the representation that makes valid transitions explicit and testable.

## Communication and asynchronous work

- Synchronous calls suit a result needed before responding; define latency/dependency failure behavior.
- Durable jobs suit work that must outlive a request; define delivery, duplicate handling, deadlines and visible failure state.
- Events suit independent consumers when eventual consistency is acceptable; define ownership, schema evolution and replay.
- SSE/WebSocket/polling are alternatives for UI freshness; compare directionality, update frequency, proxy support and cost. Real time does not require a broker by default.
- In-process post-response helpers may lose work; they are not equivalent to a durable queue.

## Offline and local state

Identify the operations available offline and their source of truth. Specify local storage, pending status, credentials, encryption/retention where needed, sync retry, deduplication and conflict resolution. "Use IndexedDB" does not settle conflicting sales or server validation.

## Decision test

State the problem, simpler option, evidence against that option, selected boundary, failure semantics and revisit signal. If no important difference supports a complex pattern, keep the simpler viable structure. See [patterns-reference.md](patterns-reference.md) for costs and [trade-off-analysis.md](trade-off-analysis.md) for documenting material decisions.
