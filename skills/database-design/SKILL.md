---
name: database-design
description: Database decisions and schema design - choosing Postgres, SQLite, or a serverless option, Prisma versus Drizzle, normalisation, primary keys (UUIDv7), timestamps and relationships, indexing, query optimisation, and zero-downtime migrations. Use when designing or reviewing a schema, choosing a database or ORM, writing migrations, or fixing slow queries and N+1 problems.
version: 2.0.0
---

# Database Design

Choose the database and ORM for the deployment target, then design the schema for the queries the app will actually run. Questions: follow the global `core-protocol` rule. When the database choice is unclear and changes the architecture it is one of those questions; otherwise pick the default below and state it.

## 1. Database selection

| Requirement | Choice |
|-------------|--------|
| Full relational features, self-hosted or managed | PostgreSQL 17/18 (default for new apps with a backend) |
| Serverless Postgres, branching for previews, scale to zero | Neon, Supabase |
| Edge or ultra-low latency reads, SQLite-compatible | Turso |
| Embedded, local, single-writer, simple app | SQLite (also fine for small production apps) |
| Vector search for AI features | Postgres + pgvector |
| Global distribution, MySQL compatibility | PlanetScale, CockroachDB |

Do not default to Postgres for a personal tool that fits in SQLite, and do not pick SQLite for a multi-writer service.

## 2. ORM selection (TypeScript)

| Context | Choice |
|---------|--------|
| Schema-first DX, migrations, Studio | Prisma 7 (Rust-free client, edge-capable; runs on Vercel Edge, Cloudflare Workers, and serverless) |
| SQL-like API, smallest bundle, maximum control | Drizzle |
| Type-safe query builder without an ORM | Kysely |
| Complex reporting queries | Raw SQL with typed results |
| Python | SQLAlchemy 2.0 (async) or Django ORM |

Both Prisma 7 and Drizzle are fine on edge runtimes; choose by team preference and whether you want schema-first (Prisma) or SQL-first (Drizzle).

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

Every table: `created_at`, `updated_at` as `TIMESTAMPTZ` (never `TIMESTAMP`), and `deleted_at` if soft delete is needed. Relationships: one-to-one as a separate table with a unique FK; one-to-many with the FK on the child; many-to-many through a junction table with a composite primary key. Choose `ON DELETE` deliberately: `CASCADE` for owned children, `RESTRICT` to protect referenced rows, `SET NULL` for optional links. Use `JSONB` for genuinely schemaless data only; structured data belongs in columns.

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

- **N+1** — one query for parents plus one per child, the most common ORM performance bug. Eager-load instead: Prisma `include`/`select`, Drizzle `with`, SQLAlchemy `selectinload()` (batched `IN` query) or `joinedload()` (single join), Django `select_related()` (FK, join) / `prefetch_related()` (M2M and reverse, second query). In GraphQL, batch per-field resolvers with DataLoader.

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

Wrap writes that must succeed all-or-nothing in one transaction (create order + decrement stock + write ledger). Keep transactions short and free of I/O: never make an HTTP call or wait on user input inside one — you hold locks for its whole duration. A plain transaction does not stop a read-modify-write race (check-then-update on a balance or inventory); for those use row locks (`SELECT ... FOR UPDATE`), an atomic write (`UPDATE ... SET qty = qty - 1 WHERE qty >= 1`), or `SERIALIZABLE` isolation with retry on serialization failure.

## 6. Migrations

Every schema change ships **expand then contract**: deploy the additive change first, migrate data and switch the app over, then remove the old shape in a later deploy — because during a rollout old and new code run against the same schema and both must work. Zero-downtime sequence per change type:

- Add column: add nullable, backfill in batches, then add `NOT NULL`/default.
- Remove column: stop reading and writing it, deploy, then drop.
- Rename column: add new, dual-write, backfill, switch reads, drop old.
- Add index: `CREATE INDEX CONCURRENTLY` (outside a transaction).
- Change type: add new column, migrate, swap.

Never ship a breaking change in one step; test migrations against a copy of production data; keep a rollback path; run reversible steps in a transaction. Commit migration files with the code that needs them (`prisma migrate dev` / `drizzle-kit generate`), and never edit an applied migration.

## 7. Script (advisory)

`./scripts/schema_validator.py <project>` finds Prisma schemas and reports missing relations, index suggestions, and naming issues. It always exits 0, so it never blocks a task; treat its output as review notes and run `npx prisma validate` (or `drizzle-kit check`) for real validation.

```powershell
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/database-design/scripts/schema_validator.py .
```

Related: `@[skills/api-patterns]` for pagination contracts, `@[skills/vulnerability-scanner]` for injection and secrets checks.
