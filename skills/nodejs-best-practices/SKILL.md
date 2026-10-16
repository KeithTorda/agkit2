---
name: nodejs-best-practices
description: Implement and review Node.js services, workers and CLIs with sound async behavior, resource lifetimes, validation and failure handling. Use for Node/TypeScript backend work; follow the installed runtime and framework.
version: 2.8.2
---

# Node.js Engineering

Read runtime constraints, package manager, module type, build pipeline, framework and deployment before changing code. Keep a suitable existing framework. Select a new one from integration, workload, support and team needs rather than a mandatory Hono/Express/Fastify default.

## Runtime and modules

Use the runtime selected by the project/deployment and verify supported syntax, Web APIs, test runner and TypeScript execution. Native type stripping, a transpiler and the TypeScript compiler provide different guarantees; executing a file does not typecheck it. Do not change ESM/CommonJS, package exports or file extensions without inspecting consumers and tooling.

Treat environment variables as untrusted strings and validate required configuration at an appropriate startup boundary. Keep credentials out of logs and source. Connection pools and clients should have deliberate process/request lifetimes rather than being recreated for every query.

## Requests and domain operations

Parse external input with the project's validation library or equivalent explicit validation. A type assertion is not validation. A handler owns protocol concerns; extract domain logic when it creates a useful test/ownership boundary. Avoid mandatory controller/service/repository layers for a small endpoint.

Apply authentication and resource/tenant authorization at protected operations. Format expected domain failures consistently, with user-safe messages and correlation IDs; retain underlying causes in redacted diagnostics. Do not turn every exception into a successful response or keep running after unrecoverable state corruption.

## Async work and capacity

- Await dependent work in order. Start independent work concurrently when access, capacity and failure semantics permit; bound fan-out instead of launching unbounded requests.
- `Promise.all` fails early but does not cancel its siblings. `Promise.allSettled` suits independent outcomes. `Promise.race` ending a wait does not stop the losing operation: use supported abort signals and clean up resources.
- Blocking I/O and CPU-heavy work can stall request handling. Use async APIs/streams for I/O and worker/process/job boundaries for demonstrated CPU costs. Async syntax does not make CPU work parallel.
- Set deadlines on external calls, respect upstream limits and retry only eligible failures with bounded backoff. Unknown write outcomes need status reconciliation/idempotency.
- Streams need backpressure, error handling, cancellation and limits. Upload size checks must hold during streaming, not after buffering an unlimited body.

## Background work and lifecycle

In-process post-response work is suitable only when its loss is acceptable and the host supports its lifetime. Durable email delivery, payment processing, imports and scheduled work usually need a persistent queue/outbox or platform equivalent. Consumers handle duplicate delivery, poison messages and partial failure; do not promise exactly-once execution from retries alone.

On shutdown, stop accepting new work, allow/drain bounded in-flight work and release resources within the host's deadline. Inspect process-manager/serverless behavior before assuming hooks always run. Avoid leaking timers or listeners in reload/reconnect paths.

## Verification

Exercise changed business rules plus invalid input, denied access, upstream timeout/rejection and duplicate work when relevant. Use the project's test runner and framework test facilities; add no framework merely for a trivial edit. Profile event-loop delay, CPU, heap or query cost when those are the actual concern. Report measured observations, not assumed speed/security gains.

Use `api-patterns` for client contracts, `database-design` for transaction guarantees, `testing-patterns` for coverage and `performance-profiling` for evidence.
