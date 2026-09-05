---
name: nodejs-best-practices
description: Node.js 24 LTS backend guidance - Hono by default for a standalone API, Fastify when Node-heavy, Express or NestJS only in existing code, ESM and native TypeScript, layered architecture, error handling, async patterns, validation with Zod, security checklist, and testing with node:test or Vitest. Use when building or reviewing a Node.js server, API, worker, or CLI, or choosing a backend framework for a TypeScript project.
version: 2.0.0
---

# Node.js Best Practices

Decision guidance for Node.js 24 LTS services. Choose the framework for the deployment target (ask once if it changes the architecture; otherwise state the default), keep business logic out of HTTP handlers, and validate at every boundary.

---

## 1. Framework Selection

### Decision Tree

```
What are you building?
│
├── Backend inside a Next.js app
│   └── Route Handlers + Server Actions (tRPC in a TypeScript monorepo)
│
├── Standalone Node API (default)
│   └── Hono — edge-capable, runs unchanged on Node, Workers, Vercel, Bun
│
├── Node-heavy API (long-lived connections, streams, heavy plugins, raw throughput)
│   └── Fastify (~5x req/sec of Express in Fastify's own hello-world benchmark; benchmark your own workload)
│
└── Existing code
    └── Express or NestJS stay where they already are; do not start a new API on them
```

### The trade-off, in one line each

- **Hono by default.** One Web-standard (`Request`/`Response`) codebase runs unchanged on Node, Workers, Deno, Bun, and serverless/edge; smallest cold start; native TS end to end. Reach past it only for a concrete reason below.
- **Fastify when the workload is Node-heavy** and wants its plugin/hooks ecosystem, JSON-Schema-based serialization, or raw throughput on a long-lived Node process. Not portable to edge runtimes.
- **Express or NestJS only to match existing code.** Largest ecosystem, but a dated middleware and async-error model; Express 5 is a migration path for existing apps, not a reason to start a new one. Never open a greenfield API on Express.

If the deployment target is unknown and it flips the choice (edge vs long-lived Node), ask once; otherwise default to Hono and say so.

---

## 2. Runtime Considerations

### Native TypeScript

```
Node.js 24 LTS runs .ts files directly (type stripping, no flag needed)
├── Erasable syntax only: no enums, runtime namespaces, or parameter properties
├── Types are stripped, not checked: run `tsc --noEmit` separately
├── Non-erasable syntax or bundling: use tsx or build with tsc/esbuild
└── Good for: scripts, CLIs, small services; still bundle for production deploys
```

Set `"erasableSyntaxOnly": true` and `"verbatimModuleSyntax": true` in `tsconfig.json` so the compiler rejects syntax the runtime cannot strip.

### Module System Decision

```
ESM (import/export)
├── The standard; `"type": "module"` in package.json for new projects
├── Better tree-shaking, top-level await
└── Node 24 can `require()` ESM modules, so ESM-only dependencies are safe

CommonJS (require)
└── Existing codebases only; do not start new projects on it
```

### Runtime Selection

| Runtime | Best For |
|---------|----------|
| **Node.js** | General purpose, largest ecosystem |
| **Bun** | Performance, built-in bundler |
| **Deno** | Security-first, built-in TypeScript |

---

### Tooling

ESLint 9+ flat config (`eslint.config.js`; `.eslintrc*` is legacy), Prettier or Biome for formatting, `tsc --noEmit` in CI, `npm audit` for dependencies. Details and the kit runners: `@[skills/lint-and-validate]`.

---

## 3. Architecture Principles

### Layered Structure Concept

```
Request Flow:
│
├── Controller/Route Layer
│   ├── Handles HTTP specifics
│   ├── Input validation at boundary
│   └── Calls service layer
│
├── Service Layer
│   ├── Business logic
│   ├── Framework-agnostic
│   └── Calls repository layer
│
└── Repository Layer
    ├── Data access only
    ├── Database queries
    └── ORM interactions
```

The payoff is a service layer you can unit-test without spinning up HTTP and swap the ORM under without touching business rules. Do not build three layers for a small script, a one-off worker, or a single-endpoint service — start in one file and extract a service only when a second caller or a test needs it.

---

## 4. Error Handling Principles

### Throw typed errors; format them once

Data and service layers throw typed domain errors; a single top-level handler maps error class to status and to one consistent envelope. The client gets a stable code and a safe message; the full error goes to logs only — never into the response.

```ts
// WRONG - each handler invents a shape and leaks internals
app.get("/users/:id", async (c) => {
  try {
    const user = await db.user.findUnique({ where: { id: c.req.param("id") } });
    return c.json(user);                        // 200 + `null` when missing
  } catch (e) {
    return c.json({ error: e.message }, 500);   // leaks DB/internal message
  }
});

// RIGHT - service throws; one handler maps class -> status + safe envelope
class NotFoundError extends Error {}

app.get("/users/:id", async (c) =>
  c.json(await getUser(c.req.param("id"))));     // throws NotFoundError if absent

app.onError((err, c) => {
  if (err instanceof NotFoundError)
    return c.json({ error: { code: "not_found", message: "User not found" } }, 404);
  console.error(err);                            // full detail to logs only
  return c.json({ error: { code: "internal", message: "Something went wrong" } }, 500);
});
```

### Status Code Selection

| Situation | Status | When |
|-----------|--------|------|
| Bad input | 400 | Client sent invalid data |
| No auth | 401 | Missing or invalid credentials |
| No permission | 403 | Valid auth, but not allowed |
| Not found | 404 | Resource doesn't exist |
| Conflict | 409 | Duplicate or state conflict |
| Validation | 422 | Schema valid but business rules fail |
| Server error | 500 | Our fault, log everything |

---

## 5. Async Patterns Principles

### When to Use Each

| Pattern | Use When |
|---------|----------|
| `async/await` | Sequential async operations |
| `Promise.all` | Parallel independent operations |
| `Promise.allSettled` | Parallel where some can fail |
| `Promise.race` | Timeout or first response wins |

`Promise.all` rejects on the first failure and abandons the rest — use `allSettled` when partial success is acceptable. Never `await` in a loop for independent work; collect the promises and `Promise.all` them.

### Keep the event loop free

async only helps I/O-bound work (DB, HTTP, files, network). It does nothing for CPU-bound work (crypto, image/video, large JSON, heavy computation) — that blocks every in-flight request on the process. Never call sync I/O (`fs.readFileSync`, `execSync`) in a request path; stream large payloads instead of buffering; move CPU-heavy work off the loop (worker thread, child process, or a queue).

### When to reach for a queue

In-process fire-and-forget (`queueMicrotask`, an un-awaited async call) is acceptable only for best-effort work that may vanish on restart. Move work to a durable queue — BullMQ on Redis, or a managed queue (SQS, Cloud Tasks) — when any of these holds: it must survive a crash or deploy, needs retries with backoff, must run outside the request's latency budget (outbound email, thumbnails, webhook fan-out), needs rate or concurrency control, or is CPU-heavy. A queue is not a default: it adds a broker to run, monitor, and dead-letter. Work that fits inside the request stays in the request.

---

## 6. Validation Principles

### Validate at Boundaries

```
Where to validate:
├── API entry point (request body/params)
├── Before database operations
├── External data (API responses, file uploads)
└── Environment variables (startup)
```

### Validation Library Selection

| Library | Best For |
|---------|----------|
| **Zod** | TypeScript first, inference |
| **Valibot** | Smaller bundle (tree-shakeable) |
| **ArkType** | Performance critical |
| **Yup** | Existing React Form usage |

### Parse, don't cast

Validate untrusted input with a schema at the boundary and pass the **typed result inward** — `const data = CreateUser.parse(req.body)`, never `req.body as CreateUser`. A cast is a lie to the type system; a parse is a runtime guarantee. Validate environment variables once at startup and fail fast if any are missing.

---

## 7. Security Principles

### Security

Beyond *parse, don't cast* above, the Node-specific, non-obvious items: hash passwords with argon2 or bcrypt (never a fast/general-purpose hash); verify a JWT's signature **and** expiry on every request, not just decode it; set security headers (Helmet or equivalent); parameterised queries only, never string-built SQL; rate-limit unauthenticated routes; secrets from the environment, never in code or the repo.

Every input crosses a trust boundary — query params, body, headers, cookies, uploads, and external API responses. Depth on threats, injection, and scanning: `@[skills/vulnerability-scanner]` and `@[skills/red-team-tactics]`.

---

## 8. Testing Principles

### Test Strategy Selection

| Type | Purpose | Tools |
|------|---------|-------|
| **Unit** | Business logic | `node:test` (built in) or Vitest |
| **Integration** | API endpoints | `app.inject()` (Fastify), `app.request()` (Hono), or Supertest |
| **E2E** | Full flows | Playwright (`@[skills/testing-patterns]`) |

### What to Test (Priorities)

1. **Critical paths**: Auth, payments, core business
2. **Edge cases**: Empty inputs, boundaries
3. **Error handling**: What happens when things fail?
4. **Not worth testing**: Framework code, trivial getters

### Built-in test runner

```
node --test "src/**/*.test.ts"    # explicit glob is the durable form
node --test --watch "src/**/*.test.ts"
node --test --experimental-test-coverage "src/**/*.test.ts"
```

`node:test` needs no dependency and runs `.ts` tests directly on Node 24 (erasable syntax only). Choose Vitest when the project already uses Vite, needs browser-mode or component tests, or wants the richer mocking API. Wire either into `"test"` in `package.json` so `npm test` and the kit's test runner find it.

---

## 9. Anti-Patterns to Avoid

Avoid: Express for a new API (Hono by default, Fastify when Node-heavy), sync `fs` calls in request paths, business logic in controllers, unvalidated input, hard-coded secrets, trusting external data, CPU-heavy work on the event loop.

Do: choose the framework for the deployment target, use layered architecture once the project grows, validate every input with Zod (or Valibot/ArkType), read secrets from the environment, profile before optimizing.

---

## 10. Decision Checklist

Before implementing:

- [ ] **Framework chosen for this context** (asked once if it changes the architecture)
- [ ] **Considered deployment target?**
- [ ] **Planned error handling strategy?**
- [ ] **Identified validation points?**
- [ ] **Considered security requirements?**


