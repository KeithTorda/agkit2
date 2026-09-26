# Architecture Examples

Reference decisions by project type. Use them as starting points; the project's constraints decide.

## 1. LGU, barangay or school portal

```yaml
Requirements:
  - Public information pages, announcements, downloadable forms, a lookup (for example a precinct finder)
  - A few staff editors, traffic spikes on announcement days
  - Cheap hosting, maintained by one developer
Decisions:
  Structure: static-first site (Astro or plain HTML) or Next.js with static rendering
  Data: content in Markdown/JSON in the repo, or a small SQLite/Postgres table for lookups
  Editing: Git-based edits by the developer, or a headless CMS only if staff must edit
  Hosting: static host or CDN (Vercel, Netlify, Cloudflare Pages)
Trade-offs accepted:
  - No admin panel at first -> edits go through the developer
  - Lookup data refreshed by import, not live
Revisit when: staff need to publish without the developer; the lookup needs live data
```

## 2. POS and inventory for one business or school canteen

```yaml
Requirements:
  - Cashier sales, deliveries, stock levels, daily reports, receipts
  - 2-10 staff with roles; money and stock must never drift
  - Internet can drop during a sale
Decisions:
  Structure: monolith - Laravel 12 (Blade/Livewire or Inertia) or Next.js 16 full-stack
  Database: Postgres 17/18 or MySQL 8.4; money as integer centavos or NUMERIC
  Integrity: sale + stock movement + ledger in one transaction; stock as a movements table
             with a derived balance; atomic decrement guarded by a CHECK or WHERE qty >= n
  Audit: append-only audit log of who changed what
  Offline: if required, local queue of sales with client-generated idempotency keys
  Hosting: one VPS or managed platform + managed database, daily backups
Trade-offs accepted:
  - One app, one database -> simple to run, scales to many terminals for one client
  - No separate reporting store -> reports use indexed queries and views
Revisit when: several branches need independent operation; reporting slows sales
```

## 3. SaaS product (several clients, small team)

```yaml
Requirements:
  - 1K-100K users across tenants; billing, users, core domain
  - 2-10 developers, long-lived
Decisions:
  Structure: modular monolith (modules per domain with explicit public functions)
  Stack: Next.js 16 + Postgres, or Next.js front + Hono API when mobile clients also consume it
  Tenancy: tenant_id on every tenant table + row-level security or scoped queries, decided in an ADR
  Auth: session cookies (Better Auth or Clerk); OAuth/OIDC for social or enterprise login
  Async: background jobs for e-mail, exports, webhooks
Trade-offs accepted:
  - Shared database -> cheaper and simpler; per-tenant isolation relies on disciplined scoping
Revisit when: a tenant needs data residency or isolation; one module needs separate scaling
```

## 4. Larger platform (many teams, 100K+ active users)

```yaml
Decisions:
  Structure: modular monolith first; extract services along proven boundaries
  Communication: synchronous APIs inside a request; events (a managed queue or Kafka) between domains
  Data: database per service only where the boundary is real
  Operations: tracing, central logs, dashboards, automated deploys and rollbacks
Trade-offs accepted:
  - Eventual consistency between domains -> needs idempotent consumers and clear ownership
```
