---
name: python-patterns
description: Implement and review Python services, scripts and APIs with appropriate typing, sync/async boundaries, resource management and packaging. Use for Python work; preserve the interpreter, framework and environment supported by the project.
version: 2.8.2
---

# Python Engineering

Inspect `pyproject.toml`, interpreter constraints, lock/requirements files, environment and deployment. Run commands through the project's interpreter/environment. Do not impose a newer Python release, uv, Ruff, FastAPI or Pydantic when the existing stack serves the task.

## Select structure from the work

A small script can remain one coherent file. A growing service benefits from domain modules and explicit I/O boundaries. FastAPI, Django, Flask and other frameworks have different integration/operating costs; choose based on existing infrastructure, admin/auth needs, execution model and maintainers. Verify installed-version APIs before adding framework-specific code.

Use types to describe important contracts. `TypedDict`, dataclasses, protocols, unions and framework models serve different purposes; annotations alone do not validate external input. Validate requests/configuration at boundaries with the adopted library or explicit parsers. Avoid broad `Any` or casts that conceal uncertain data.

## Execution model and resources

- In synchronous code, use supported sync clients and concurrency appropriate to the workload. Async is useful for compatible concurrent I/O; it is not an automatic performance upgrade.
- Inside async work, use non-blocking clients or deliberately offload unavoidable blocking calls. Offloading to a thread may not cancel the underlying call when its awaiter is cancelled.
- CPU-heavy work may need processes/native implementations or a worker queue; measure before selecting concurrency. Do not assume interpreter/thread behavior without checking its build and deployment.
- Use context managers/`with`/`async with` for files, responses, sessions and locks. Bound connection pools, request deadlines, retries and fan-out.
- Preserve cancellation semantics supported by the framework. A timeout is not proof that a side effect did not occur.

## Domain failures and data

Catch exceptions where a useful recovery/translation is possible; preserve causes with `raise ... from exc` when wrapping. Do not swallow broad exceptions, fabricate fallback data or log credentials. Expected validation/domain errors should be distinguishable from infrastructure faults.

Avoid mutable default arguments, accidental shared state and unbounded caches. Decide transaction boundaries and session lifetime explicitly; an ORM object escaping a closed/lazy session can fail later. Check for N+1 queries and external effects inside retriable transactions.

## Work that outlives a request

An in-process background task can be lost on process shutdown. For work that must survive, use the project's durable job system with idempotent handlers, retry limits and visible failure state. Choose queue/backend support from the actual framework version and hosting; do not assume a task API includes a running durable worker.

Scripts/CLIs should have clear arguments, meaningful exits, controlled stdout/stderr and cleanup after partial failure. Make reruns safe when files or remote records may already exist.

## Testing and tooling

Use the configured pytest/unittest framework and environment. Test observable outputs and important failure paths; use a real compatible database for engine-specific behavior. For ASGI/HTTP clients, follow installed-version transport/lifespan APIs instead of copying deprecated constructor arguments. An in-process test may need explicit startup/shutdown management.

Use configured formatting/lint/types, scoped to the change. Do not perform a repository-wide tooling migration as a side effect. `database-design`, `api-patterns`, `systematic-debugging` and `testing-patterns` supply deeper contract/failure guidance.
