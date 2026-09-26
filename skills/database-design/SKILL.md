---
name: database-design
description: Database decisions and schema design - Postgres, MySQL, SQLite or a serverless option, Prisma 7, Drizzle or Eloquent, keys, money and timestamps, relationships, indexing, transactions, N+1 fixes and zero-downtime migrations. Use when designing or reviewing a schema, choosing a database or ORM, writing migrations, fixing slow queries, or writing a /proplan data model.
version: 2.5.0
---

# Database Design

Choose the database and ORM for the deployment target, then design the schema for the queries the app will actually run. The project's existing database and ORM win. When the choice is open and changes the architecture, it is a question worth asking (`core-protocol`); otherwise pick the default below and state it.

Firm in this skill: data integrity (constraints, transactions, money types, migrations that do not lose data) and parameterised queries. Everything else is a default.

## 1. Database selection

| Requirement | Choice |
|-------------|--------|
| Full relational features, self-hosted or managed | PostgreSQL 17/18 (default for new apps with a backend) |
| Laravel on shared or budget hosting, or the client already runs MySQL | MySQL 8.4 LTS or MariaDB 11 LTS |
| Serverless Postgres, branching for previews, scale to zero | Neon, Supabase |
| Edge or ultra-low latency reads, SQLite-compatible | Turso |
| Embedded, local, single-writer, simple app | SQLite (also fine for small production apps) |
| Vector search for AI features | Postgres + pgvector |
| Global distribution, MySQL compatibility | PlanetScale, CockroachDB |

A personal tool or a single-machine app can live in SQLite; a multi-writer service over the network should not.

## 2. ORM selection

| Context | Choice |
|---------|--------|
| TypeScript, schema-first DX, migrations, Studio | Prisma 7 (TypeScript client without the Rust engine, driver adapters, `prisma.config.ts`; runs on Node, serverless and edge) |
| TypeScript, SQL-like API, smallest bundle, maximum control | Drizzle |
| TypeScript, query builder without an ORM | Kysely |
| PHP / Laravel | Eloquent + Laravel migrations |
| Python | SQLAlchemy 2.0 (async) or Django ORM |
| Complex reporting queries, any stack | Raw SQL with typed results (parameterised) |

Prisma 7 and Drizzle are both good choices; choose by whether you want schema-first (Prisma) or SQL-first (Drizzle). When upgrading an older Prisma project, follow the Prisma 7 upgrade guide rather than assuming v5/v6 setup still applies.

## 3. Schema design

Normalise when data repeats across rows, updates would touch many places, or relationships are clear; denormalise (embed or duplicate) when reads dominate, data rarely changes, and it is always fetched together.

Primary keys:

| Type | Use when |
|------|----------|
| UUIDv7 (RFC 9562) | Default for new tables: globally unique and time-ordered, so B-tree inserts stay fast. Postgres 18 has `uuidv7()`; on older Postgres generate in the app (`uuid` npm package `v7()`, Python `uuid6`/`uuid_utils`) |
| Auto-increment / identity | Simple single-database apps where ids may be visible and guessable is acceptable |
| UUIDv4 | Only when random, non-sortable ids are specifically wanted |
| ULID | Legacy compatibility only; prefer UUIDv7 for anything new |
| Natural key | Rarely; only for stable business identifiers |

Every table: `created_at`, `updated_at` as `TIMESTAMPTZ` in Postgres (MySQL: `TIMESTAMP`/`DATETIME` stored in UTC, app timezone `Asia/Manila` for display), and `deleted_at` if soft delete is needed.

Money: integer minor units (centavos) or `NUMERIC(12,2)` / `DECIMAL(12,2)`; **never** `FLOAT`/`DOUBLE`. Store the currency when more than one is possible, and store computed totals, VAT and discounts on the sale row as they were at the time (prices change; receipts must not).

Integrity belongs in the database, not only in the app: `NOT NULL` where a value is required, `UNIQUE` for business identifiers (receipt number, student ID, precinct code), foreign keys, and `CHECK` constraints for invariants (`quantity >= 0`). Relationships: one-to-one as a separate table with a unique FK; one-to-many with the FK on the child; many-to-many through a junction table with a composite primary key. Choose `ON DELETE` deliberately: `CASCADE` for owned children, `RESTRICT` to protect referenced rows, `SET NULL` for optional links. Use `JSONB` for genuinely schemaless data only; structured data belongs in columns.

## 4. Indexing

Index columns used in `WHERE`, `JOIN`, and `ORDER BY`, every foreign key, and unique constraints. Every index is a second structure the database must update on every `INSERT`/`UPDATE`/`DELETE` that touches its columns, plus storage and planner cost — so index for the read patterns you actually run, not speculatively. An unused index is pure write tax; find them (`pg_stat_user_indexes`, `idx_scan = 0`) and drop them. Skip indexes on low-cardinality columns (a boolean rarely beats a scan) and on hot write paths not queried by that column.

| Index | Use |
|-------|-----|
| B-tree | Default: equality and ranges |
| Hash | Equality only |
| GIN | JSONB, arrays, full-text search |
| GiST | Geometry, ranges |
| HNSW / IVFFlat | pgvector similarity |

Composite indexes: equality columns first, range columns last, order matched to the query; a composite on `(a, b)` also serves queries on `a` alone. Partial indexes (`WHERE deleted_at IS NULL`) keep hot indexes small.

## 5. Query optimisation

- **N+1** — one query for parents plus one per child, the most common ORM performance bug. Eager-load instead: Prisma `include`/`select`, Drizzle `with`, Eloquent `with()` / `load()` (and `Model::preventLazyLoading(! app()->isProduction())` in `AppServiceProvider` to catch it in development), SQLAlchemy `selectinload()` (batched `IN` query) or `joinedload()` (single join), Django `select_related()` (FK, join) / `prefetch_related()` (M2M and reverse, second query). In GraphQL, batch per-field resolvers with DataLoader.

```ts
// WRONG - 1 query for posts, then N more (one per post) = N+1 round trips
const posts = await db.post.findMany();
for (const post of posts) {
  post.author = await db.user.findUnique({ where: { id: post.authorId } });
}

// RIGHT - eager-loaded in one round trip; select only the columns you read
const posts = await db.post.findMany({
  select: { id: true, title: true, author: { select: { id: true, name: true } } },
});
```

- Run `EXPLAIN (ANALYZE, BUFFERS)` on slow queries; watch for sequential scans on large tables, row estimates far from actuals, and sorts spilling to disk.
- Select only needed columns, paginate at the database (`LIMIT` with keyset conditions), push filters into SQL, and cache read-heavy results with explicit invalidation.
- Pool connections (PgBouncer, Neon pooler, Prisma Accelerate, or Drizzle with a pooled driver) in serverless environments.

### Transaction boundaries

Wrap writes that must succeed all-or-nothing in one transaction (create order + decrement stock + write ledger): Prisma `$transaction`, Drizzle `db.transaction`, Laravel `DB::transaction(fn () => ...)`. Keep transactions short and free of I/O: never make an HTTP call or wait on user input inside one — you hold locks for its whole duration. A plain transaction does not stop a read-modify-write race (check-then-update on a balance or inventory); for those use row locks (`SELECT ... FOR UPDATE`), an atomic write (`UPDATE ... SET qty = qty - 1 WHERE qty >= 1`), or `SERIALIZABLE` isolation with retry on serialization failure.

## 6. Migrations

Once a database holds production data, schema changes ship **expand then contract**: deploy the additive change first, migrate data and switch the app over, then remove the old shape in a later deploy — because during a rollout old and new code run against the same schema and both must work. Zero-downtime sequence per change type:

- Add column: add nullable, backfill in batches, then add `NOT NULL`/default.
- Remove column: stop reading and writing it, deploy, then drop.
- Rename column: add new, dual-write, backfill, switch reads, drop old.
- Add index: `CREATE INDEX CONCURRENTLY` (outside a transaction).
- Change type: add new column, migrate, swap.

For a database already in production, do not ship a breaking change in one step; test migrations against a copy of production data; keep a rollback path; back up before destructive steps (and ask before running them, per `universal-rules`). Commit migration files with the code that needs them (`prisma migrate dev`, `drizzle-kit generate`, `php artisan make:migration`), and never edit a migration that has already run in production — write a new one. Before the first deploy, collapsing or rewriting migrations is fine.

## 7. `/proplan` data model

`database-architect` writes `04-data-model.md` of a `/proplan` with this skill, after the architecture checkpoint (template in `KIT/skills/proplan/templates/`). Include:

- An entity list with what each owns, and an ER diagram (Mermaid `erDiagram` is fine).
- For each table: columns with types, keys, constraints, indexes and the query each index serves.
- Money, stock and audit rules (where totals are stored, how balances are derived, what is append-only).
- Personal data inventory: which columns hold personal or sensitive data, who can read them, retention (Data Privacy Act of 2012 for Philippine clients).
- Migration and seed plan, including any import from spreadsheets or a legacy system.
- The `R-`/`NFR-` IDs each part serves, so the plan traces end to end.

## 8. Script (advisory)

`schema_validator.py <project-or-file>` reads Prisma (single or multi-file), Drizzle, Laravel migrations and raw SQL. Errors: a Prisma model with no identifier, a SQL `CREATE TABLE` with no primary key. Warnings: Laravel `foreignId()` without `constrained()`, a Drizzle table with no primary key. Info: foreign-key columns without an index, models without `createdAt`, non-PascalCase model names. Flags: `--json`, `--verbose`, `--fail-on error|warning|never` (default `error`). Treat its output as review notes; `npx prisma validate`, `drizzle-kit check` or `php artisan migrate --pretend` do the real validation.

```powershell
python "KIT/skills/database-design/scripts/schema_validator.py" .
```

Related: `api-patterns` for pagination contracts, `vulnerability-scanner` for injection and secrets checks, `architecture` for the decisions a schema depends on.
