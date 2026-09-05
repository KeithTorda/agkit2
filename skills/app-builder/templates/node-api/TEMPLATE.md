---
name: node-api
description: Standalone Node.js API template. Hono by default (edge-capable), Fastify when Node-heavy, Express only for existing code. TypeScript, Prisma or Drizzle, Zod.
---

# Node API Template (Hono)

> Pin to the current stable line when scaffolding. Use this template only for a standalone API; inside a Next.js app the backend is Route Handlers + Server Actions (`nextjs-fullstack`).

## Tech Stack

| Component | Technology | Notes |
|-----------|------------|-------|
| Runtime | Node.js 24 LTS | Native TypeScript (type stripping); Bun where the project already uses it |
| Framework | Hono (default) | Runs unchanged on Node, Cloudflare Workers, Vercel, Deno, Bun; typed routes and `hono/client` RPC |
| Alternative | Fastify | When the API is Node-heavy: long-lived connections, streams, heavy plugins, maximum throughput on a server |
| Legacy | Express 5 | Existing code only — do not start a new API on Express |
| Language | TypeScript 5.9+ | Strict mode |
| Database | PostgreSQL + Prisma 7 or Drizzle | Both edge-capable; UUIDv7 keys |
| Validation | Zod (default); Valibot or ArkType when bundle size matters | `@hono/zod-validator` / `@hono/valibot-validator` at the route boundary |
| Auth | Better Auth (or JWT with `hono/jwt` for service-to-service) | Sessions in httpOnly cookies for browser clients |
| Lint / tests | ESLint 9 flat config; Vitest or `node:test` | `app.request()` tests the app without a network port |

## Directory Structure

```
project-name/
├── prisma/schema.prisma      # or drizzle/ with drizzle.config.ts
├── src/
│   ├── app.ts                # new Hono() + middleware + routes (no listen)
│   ├── server.ts             # Node entry: serve({ fetch: app.fetch, port })
│   ├── config/env.ts         # Zod-parsed environment
│   ├── routes/               # One file per resource: routes/orders.ts exports a Hono sub-app
│   ├── services/             # Business logic (framework-agnostic)
│   ├── repositories/         # Database access (Prisma/Drizzle)
│   ├── middleware/           # auth, request id, error handler
│   ├── schemas/              # Zod schemas shared by routes and tests
│   └── lib/                  # db client, logger
├── tests/                    # Vitest: app.request('/orders') against src/app.ts
├── eslint.config.js
└── package.json
```

## Middleware order

| Order | Middleware | Hono |
|-------|------------|------|
| 1 | Request id + structured logger | `hono/request-id`, `hono/logger` (or pino) |
| 2 | Security headers, CORS | `hono/secure-headers`, `hono/cors` |
| 3 | Body limit, compression | `hono/body-limit`, `hono/compress` |
| 4 | Auth | `hono/jwt` or a Better Auth session check on protected groups |
| 5 | Routes | `app.route('/orders', orders)` |
| 6 | Error handler | `app.onError()` returns one error shape; `app.notFound()` |

## API response format

| Type | Structure |
|------|-----------|
| Success | `{ success: true, data: {...} }` |
| Error | `{ error: "message", details: [...] }` — never a stack trace |

## Setup Steps

1. `npm init -y`; set `"type": "module"`.
2. `npm install hono @hono/node-server @hono/zod-validator zod @prisma/client`
3. `npm install -D typescript @types/node prisma vitest eslint @eslint/js typescript-eslint`
4. `npx prisma init` (or `npm install drizzle-orm && npm install -D drizzle-kit`)
5. Scripts: `"dev": "node --watch src/server.ts"`, `"test": "vitest run"`, `"lint": "eslint ."`
6. `npx prisma migrate dev`, then `npm run dev`

Fastify instead: `npm install fastify @fastify/cors @fastify/helmet fastify-type-provider-zod`; the same layering applies (routes → services → repositories), plugins are registered in `app.ts`, and `app.inject()` replaces `app.request()` in tests.

## Best Practices

- Split `app.ts` (wiring) from `server.ts` (`serve`) so tests import the app without opening a port; deploy the same `app.fetch` to an edge runtime when needed.
- Layer: routes validate and translate, services hold the logic, repositories talk to the database.
- Validate every input with Zod at the route boundary; infer the TypeScript types from the schemas.
- Centralised error handler with one response shape; log with request ids, never PII or tokens.
- Environment through a Zod-parsed `config/env.ts`; fail fast on a missing variable.
- Rate-limit unauthenticated routes; health endpoint at `/health`; OpenAPI via `@hono/zod-openapi` when the API is public.
