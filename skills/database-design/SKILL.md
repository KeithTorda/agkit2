---
name: database-design
description: Design schemas, queries, indexes, transactions and migrations around data invariants and workload. Use for database selection, modeling, persistence changes or slow queries; preserve the engine and ORM unless the task requires a change.
version: 2.8.2
---

# Database Design

Model facts that must remain true, then choose storage/access patterns that enforce them. Inspect the actual engine/ORM versions, migrations, workload and deployment. Do not upgrade storage or drivers to match a kit preference.

## Storage and schema

Relational engines suit joins, structured constraints and transactions. Embedded databases fit local tools and server workloads when concurrency/deployment limits fit. Document, key-value, search and vector stores solve specific access needs; compare source-of-truth ownership, hosting, backup/restore, write patterns, cost and team experience.

Keep an adequate existing ORM/query builder. Use parameterized SQL for complex or engine-specific operations. An ORM does not prevent unsafe transactions, N+1 queries or destructive migrations. Verify installed-version APIs before changing configuration.

- Choose identifiers for actual requirements: local identity, opaque public IDs, distributed generation, ordering and index behavior. Sequential IDs are not access control; time-ordered IDs may expose creation time. No UUID format is universal.
- Encode uniqueness, references, required fields and valid ranges with database constraints where possible. Include tenant scope in relevant unique/foreign-key contracts.
- Represent money with exact decimal or integer minor units and explicit currency/rounding rules. Precision varies by currency/use case; avoid binary floats for authoritative amounts.
- Distinguish instants, calendar dates and recurring local times. A birthday is not a UTC timestamp. Preserve the domain's time-zone interpretation.
- Normalize facts that must remain consistent. JSON/denormalized values need an ownership/update strategy and access patterns that justify them.

## Transactions and concurrency

Group changes that must commit together. Check isolation level and ORM semantics; atomicity alone does not eliminate every race. Scarce stock or balances may need an atomic conditional write, row lock, constraint or serializable transaction with bounded retry. A prior SELECT plus unguarded write is race-prone.

Keep external effects outside retriable transactions unless explicitly designed for it. For a database write plus durable event delivery, consider an outbox/idempotent consumer. Deduplication must survive concurrent requests and crashes after commit. Test the failure between steps.

## Query evidence

Capture representative parameters, row counts, latency distribution and query plans. EXPLAIN ANALYZE may execute writes/expensive work: use a suitable safe environment.

Index actual predicates, joins and ordering, accounting for composite order, selectivity and write cost. Fetch necessary columns, bound collections and batch/eager-load when it removes N+1. Cursor pagination needs deterministic ties and a matching index. Re-measure on representative data; an empty development database proves little.

## Migrations and recovery

Assess table size, locks, engine capabilities and overlap between old/new app versions. When rollout requires compatibility: expand schema, deploy compatible readers/writers, backfill in resumable batches, verify invariants, then remove old fields safely. A maintenance window may be simpler when acceptable.

Document data recovery and rollback limits. A down migration may destroy new data or be impossible. Verify backup restore for significant changes and use a dry run where useful. Do not claim zero downtime without lock/runtime evidence.

For `/proplan`, keep its data-model/template contract. Include entities, constraints, access patterns, transaction boundaries, retention, migrations and recovery assumptions.

## Helper

`python "KIT/skills/database-design/scripts/schema_validator.py" .` supports `--json`, `--verbose`, `--fail-on error|warning|never`. Its pattern scan cannot prove live constraints, performance, isolation or migration safety. Inspect actual migrations and database behavior.
