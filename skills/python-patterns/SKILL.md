---
name: python-patterns
description: Python 3.13+ backend patterns - FastAPI, Django or Flask, async versus sync, type hints and Pydantic v2, project structure, background tasks, error handling, and pytest with httpx; tooling with uv and Ruff. Use when writing or reviewing Python services, scripts or APIs, or setting up a Python project's tooling.
version: 2.5.0
---

# Python Patterns

Decision guidance for Python 3.13+ services (3.14 is the newest release; 3.13 is the kit baseline). The project's existing framework, layout and tooling win. For new work, pick the framework and concurrency model for the context (ask once if the choice changes the architecture; otherwise state the default) and use the tooling below. API contract (status codes, error envelope): `api-patterns`.

## 0. Tooling baseline

| Concern | Tool |
|---------|------|
| Interpreter | Python 3.13+ (3.14 current; `requires-python = ">=3.13"` in `pyproject.toml`) |
| Environments and packaging | `uv` (`uv init`, `uv add`, `uv run`); `pyproject.toml` is the single config file |
| Lint and format | Ruff (`ruff check --fix .`, `ruff format .`) replaces flake8, isort, black |
| Types | mypy (`[tool.mypy]`, strict for libraries) or pyright/basedpyright; one of them in CI when the project has CI |
| Tests | pytest, `pytest-asyncio`, `httpx` for API tests |
| Security | Bandit optional (`bandit -r src -ll`); `pip-audit` for dependencies |

---

## 1. Framework Selection

### Decision Tree

```
What are you building?
│
├── API-first / Microservices
│   └── FastAPI (async, modern, fast)
│
├── Full-stack web / CMS / Admin
│   └── Django (batteries-included)
│
├── Simple / Script / Learning
│   └── Flask (minimal, flexible)
│
├── AI/ML API serving
│   └── FastAPI (Pydantic, async, uvicorn)
│
└── Background workers
    └── Celery + any framework
```

### Comparison Principles

| Factor | FastAPI | Django | Flask |
|--------|---------|--------|-------|
| **Best for** | APIs, microservices | Full-stack, CMS | Simple, learning |
| **Async** | Native | Django 5.2 LTS / 6.x | Via extensions |
| **Admin** | Manual | Built-in | Via extensions |
| **ORM** | Choose your own | Django ORM | Choose your own |
| **Learning curve** | Low | Medium | Low |

### Selection questions (answer from context first):
1. Is this API-only or full-stack?
2. Need admin interface?
3. Team familiar with async?
4. Existing infrastructure?

---

## 2. Async vs Sync Decision

Async wins for I/O-bound work with concurrency (DB, HTTP, files, many connections, ASGI/WebSockets). Sync is right for CPU-bound work, simple scripts, and any path that must call a blocking library. The rule that actually causes outages: **one blocking call inside `async def` freezes the whole event loop — every concurrent request stalls, not just that one.**

```python
# WRONG - blocking calls on the async path stall the entire worker
@app.get("/report")
async def report():
    data = requests.get("https://api.example.com/data").json()   # blocks the loop
    rows = sync_session.execute(select(Order)).scalars().all()   # blocks the loop
    return summarize(data, rows)

# RIGHT - async clients on the async path...
@app.get("/report")
async def report(session: AsyncSession = Depends(get_session)):
    async with httpx.AsyncClient() as client:
        data = (await client.get("https://api.example.com/data")).json()
    rows = (await session.execute(select(Order))).scalars().all()
    return summarize(data, rows)

# ...or push an unavoidable blocking call off the loop:
result = await asyncio.to_thread(legacy_blocking_call, arg)
```

A sync driver (`psycopg2`, `requests`, a sync SQLAlchemy `Session`) on an async route is the most common FastAPI performance bug. Go async end to end, or make the route `def` and let FastAPI run it in a threadpool — never half and half.

### Async Library Selection

| Need | Async Library |
|------|---------------|
| HTTP client | httpx |
| PostgreSQL | asyncpg |
| Redis | redis-py (`redis.asyncio`); `aioredis` is archived, do not add it |
| File I/O | aiofiles |
| Database ORM | SQLAlchemy 2.0 async, Tortoise |

---

## 3. Type Hints Strategy

### Type at the edges, enforce in CI

Type function signatures, class attributes and public APIs; let inference handle obvious locals. Small scripts can stay lighter. Types earn their keep only when a checker runs them, so wire mypy or pyright into the project's checks. Treat `Any` as a hole — it silently disables checking on everything it touches downstream. Prefer a pinned ignore (`# type: ignore[arg-type]`) over a bare `# type: ignore`, so it re-fails when the underlying error changes.

### Common Type Patterns

```python
# Modern syntax (3.10+): no Optional/Union/List imports
def find_user(id: int) -> User | None: ...
def process(data: str | dict[str, object]) -> None: ...
def get_items() -> list[Item]: ...

from collections.abc import Callable, Sequence
def apply(fn: Callable[[int], str], items: Sequence[int]) -> list[str]: ...

# 3.12+ PEP 695 generics: type parameters declared inline
class Box[T]: ...
type Pair[T] = tuple[T, T]
```

### Pydantic v2 is your runtime type system

Static hints are erased at runtime and do not stop a malformed request. Pydantic v2 is the runtime guarantee: use it for every request/response model, settings (`BaseSettings`), and external data crossing a boundary. Parse into a model at the edge and pass the typed instance inward — do not hand-validate dicts. Use v2 methods (`model_validate`, `model_dump`), not the deprecated v1 `.parse_obj`/`.dict`, and reach for `field_validator`/`model_validator` for cross-field rules.

---

## 4. Project Structure Principles

### Structure Selection

```
Small project / Script:
├── main.py
└── pyproject.toml (uv manages the venv and lockfile)

Medium API:
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── schemas/
├── tests/
└── pyproject.toml

Large application:
├── src/
│   └── myapp/
│       ├── core/
│       ├── api/
│       ├── services/
│       ├── models/
│       └── ...
├── tests/
└── pyproject.toml
```

### FastAPI Structure Principles

```
Organize by feature or layer:

By layer:
├── routes/ (API endpoints)
├── services/ (business logic)
├── models/ (database models)
├── schemas/ (Pydantic models)
└── dependencies/ (shared deps)

By feature:
├── users/
│   ├── routes.py
│   ├── service.py
│   └── schemas.py
└── products/
    └── ...
```

---

## 5. Django Principles

### Django Async (5.2 LTS and 6.x)

```
Django supports async:
├── Async views
├── Async middleware
├── Async ORM (limited)
└── ASGI deployment

When to use async in Django:
├── External API calls
├── WebSocket (Channels)
├── High-concurrency views
└── Background task triggering
```

### Django best practices

Thin views: business logic on the model, a custom manager, or a service module rather than in the view. Class-based views for CRUD, function-based for one-off endpoints, DRF viewsets (or Django Ninja) for APIs. Query discipline: `select_related()` for FKs, `prefetch_related()` for M2M, `.only()`/`.defer()` to trim columns, and watch for the N+1 the ORM makes easy (`database-design`).

---

## 6. FastAPI Principles

### async def vs def in FastAPI

`async def` only when the whole handler is non-blocking (async driver, `httpx`, awaited I/O). If any step blocks — sync driver, CPU-bound work, a library with no async API — declare the handler `def` and FastAPI runs it in a threadpool, keeping the loop free. The one thing never to do is a blocking call inside `async def` (see the exemplar in §2).

### Dependency injection

Inject DB sessions, the current user/auth, and config through `Depends()`; use a `yield` dependency for setup/teardown (open then close a session, release a resource). It is also the test seam: override the dependency instead of patching internals.

### Pydantic v2 Integration

```python
# FastAPI + Pydantic are tightly integrated:

# Request validation
@app.post("/users")
async def create(user: UserCreate) -> UserResponse:
    # user is already validated
    ...

# Response serialization
# Return type becomes response schema
```

---

## 7. Background Tasks

### Selection Guide

| Solution | Best For |
|----------|----------|
| **BackgroundTasks** | Simple, in-process tasks |
| **Celery** | Distributed, complex workflows |
| **ARQ** | Async, Redis-based |
| **RQ** | Simple Redis queue |
| **Dramatiq** | Actor-based, simpler than Celery |
| **Django tasks** (`django.tasks`, Django 6.0+) | Django projects; a standard task API, with a backend package that runs the worker |

### When to Use Each

```
FastAPI BackgroundTasks:
├── Quick operations
├── No persistence needed
├── Fire-and-forget
└── Same process

Celery/ARQ:
├── Long-running tasks
├── Need retry logic
├── Distributed workers
├── Persistent queue
└── Complex workflows
```

---

## 8. Error Handling Principles

### Exception strategy

Raise domain exceptions in services; register `exception_handler`s that map them to one consistent shape — a stable `code`, a human `message`, and field `details` when relevant. Never leak stack traces or internal messages to the client; log the internal detail server-side with a request id. The envelope shape is owned by `api-patterns`.

---

## 9. Testing Principles

### Testing Strategy

| Type | Purpose | Tools |
|------|---------|-------|
| **Unit** | Business logic | pytest |
| **Integration** | API endpoints | pytest + httpx/TestClient |
| **E2E** | Full workflows | pytest + DB |

### Async Testing

```python
# pytest-asyncio; httpx >= 0.28 removed AsyncClient(app=...), use ASGITransport
import pytest
from httpx import ASGITransport, AsyncClient

@pytest.mark.asyncio
async def test_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/users")
        assert response.status_code == 200
```

Set `asyncio_mode = "auto"` under `[tool.pytest.ini_options]` to drop the per-test marker. For sync code paths, FastAPI's `TestClient` (Starlette) still works.

### Fixtures Strategy

```
Common fixtures:
├── db_session → Database connection
├── client → Test client
├── authenticated_user → User with token
└── sample_data → Test data setup
```

---

## 10. Common mistakes

| Mistake | Instead |
|---|---|
| Blocking calls inside `async def` | Async clients end to end, a `def` route, or `asyncio.to_thread` |
| Django for a small JSON API with no admin needs | FastAPI (Django is right when you want its admin, auth and ORM) |
| Business logic in routes or views | A service function or model method |
| Hand-validated dicts | Pydantic models at the boundary |
| `requirements.txt` + `setup.py` in a new project | `pyproject.toml` managed by `uv` |
| N+1 queries | Eager loading (`database-design`) |

Before building a new service, settle in one line each: framework, async or sync, project layout, error handling, and whether background work needs a real queue.
