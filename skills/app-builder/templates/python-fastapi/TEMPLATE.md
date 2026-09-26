---
name: python-fastapi
description: FastAPI REST API template principles. SQLAlchemy, Pydantic, Alembic.
version: 2.5.0
---

# FastAPI API Template

> Pin to the current stable line when scaffolding.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Language | Python 3.13+ (3.14 current), managed with `uv` |
| Lint / types | Ruff + pyright (or mypy) |
| ORM | SQLAlchemy 2.0 (async) |
| Validation | Pydantic v2 |
| Migrations | Alembic |
| Auth | JWT + argon2 (via `pwdlib`) |
| Tests | pytest + pytest-asyncio, httpx `ASGITransport(app=app)` |

---

## Directory Structure

> Domain/module layout (scales better than file-type for non-trivial apps). Each domain owns its router, schemas, models, service.

```
project-name/
├── alembic/             # Migrations
├── src/
│   ├── auth/
│   │   ├── router.py    # APIRouter
│   │   ├── schemas.py   # Pydantic models
│   │   ├── models.py    # SQLAlchemy models
│   │   ├── service.py   # Business logic
│   │   ├── dependencies.py
│   │   └── exceptions.py
│   ├── posts/           # Same shape per domain
│   ├── config.py        # Global settings (BaseSettings)
│   ├── database.py      # Async engine / session
│   ├── models.py        # Shared base models
│   ├── exceptions.py    # Global exceptions
│   └── main.py          # FastAPI() + include_router
├── tests/
├── pyproject.toml       # dependencies and tool config (uv, ruff, pytest)
├── uv.lock
├── alembic.ini
└── .env
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| Domain modules | Each feature folder owns router + schemas + models + service |
| Async | async/await throughout (AsyncSession, async_sessionmaker) |
| Dependency Injection | FastAPI Depends (validation, auth, DB session) |
| Pydantic v2 | Validation + serialization |
| SQLAlchemy 2.0 | Async sessions |

---

## API Structure

| Layer | Responsibility |
|-------|---------------|
| Routers | HTTP handling |
| Dependencies | Auth, validation |
| Services | Business logic |
| Models | Database entities |
| Schemas | Request/response |

---

## Setup Steps

1. `uv init {{name}}; cd {{name}}`
2. `uv add "fastapi[standard]" "sqlalchemy[asyncio]" asyncpg alembic pydantic-settings "pwdlib[argon2]" pyjwt`
3. `uv add --dev ruff pyright pytest pytest-asyncio httpx`
4. Create `.env` (and `.env.example` without secrets); `uv run alembic init -t async alembic`
5. `uv run alembic upgrade head`
6. `uv run fastapi dev src/main.py`

Without uv: `python -m venv .venv`, `.venv\Scripts\Activate.ps1` (PowerShell), then `pip install` the same packages.

---

## Best Practices

- Use async everywhere (AsyncSession, async dependencies; wrap sync SDKs in `run_in_threadpool`)
- Per-module `BaseSettings` over one global config
- Pydantic v2 for validation
- SQLAlchemy 2.0 async sessions
- Alembic migrations: static, reversible, descriptive slugs
- pytest-asyncio for tests with `httpx.AsyncClient(transport=ASGITransport(app=app))`; use `dependency_overrides` to mock
- `redis.asyncio` for Redis (not aioredis); Ruff for lint and format
