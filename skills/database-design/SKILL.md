---
name: database-design
description: Use when designing tables, migrations, indexes or queries, deciding which system owns which data, or fixing a slow query, on MySQL or Postgres.
version: 3.2.0
---

# Database Design

Model the facts that must stay true, enforce them in the database, and keep each system's data in its own database per rule-04-system-integration.

## Steps

1. Read the current migrations, models and engine version. Keep the existing engine and ORM.
2. Write an ownership table: every table, its owner system, and whether it is master data (ERP-owned, local read-only copy) or a transaction (owned by this add-on). Only the owner writes it.
3. Local copies of ERP master data carry the ERP ID (`erp_item_id`, `erp_branch_id`) with a unique index, plus `synced_at`. Upserts match on that ERP ID.
4. Add an `outbox` table to every add-on, with the columns listed in rule-04-system-integration and an index on (`status`, `next_attempt_at`). Store processed incoming keys in an `idempotency_keys` or `processed_events` table with a unique key.
5. Enforce invariants with constraints: NOT NULL, foreign keys, unique keys (include `branch_id` or tenant in them where scoped), CHECK where the engine supports it.
6. Types: money as `DECIMAL(15,2)` or integer centavos with a currency column; instants as UTC timestamps; calendar dates as `DATE`. Avoid FLOAT for amounts.
7. Money and stock records are voided or reversed, with `voided_at`, `voided_by` and `void_reason`, per rule-06-security-baseline. Add an audit table for sensitive changes.
8. Wrap multi-step writes in a transaction. For stock or balances, use an atomic conditional update (`UPDATE ... SET qty = qty - ? WHERE id = ? AND qty >= ?`) or a row lock.
9. Index the real WHERE, JOIN and ORDER BY columns, composite in that order. Eager-load relations to remove N+1 queries. Read EXPLAIN on realistic data sizes.
10. Large-table changes: add the new column, deploy code that writes both, backfill in batches, then drop the old column in a later release. Note in the migration whether `down()` loses data.

## Stack notes

- Laravel specifics (migrations, Eloquent casts, `lockForUpdate`, soft deletes, seeders) live in the `laravel-patterns` skill.
- Postgres: use `jsonb`, partial indexes and `timestamptz`. MySQL 8: use InnoDB, `utf8mb4`, and generated columns to index JSON fields.
- `/proplan` data-model docs list entities, owner, constraints, indexes and retention.

## Helper

`python "KIT/skills/database-design/scripts/schema_validator.py" .` scans schema files for common issues (`--json`, `--verbose`, `--fail-on error|warning|never`). Run it on request; it cannot prove live constraints or performance.

## Before you finish, check

- [ ] Each table has exactly one owner system, and no query touches another system's database.
- [ ] The add-on has an `outbox` table and a unique store for processed idempotency keys.
- [ ] Money uses exact types, and money or stock rows are voided instead of deleted.
- [ ] Constraints and indexes match the real queries, and risky migrations note their rollback limits.
