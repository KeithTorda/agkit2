# <Project name>

<One sentence: what this system does and for whom.>

## Stack
- Framework: <e.g. Laravel 12 / Next.js 15 App Router>
- UI: <Bootstrap 5.3 / Tailwind 4 / React-Bootstrap>, icons: <set>
- Database: <MySQL 8 / Postgres 16>, ORM: <Eloquent / Prisma>
- Hosting: <VPS Nginx + PM2 / Docker>, PHP/Node version: <...>

## Commands
| Task | Command |
|---|---|
| Install | |
| Dev server | |
| Build | |
| Migrate / seed | |
| Tests | |
| Queue worker | |

## Folders
- <path> - <what lives there>

## Data ownership (rule-04)
| Table | Owner | Notes |
|---|---|---|
| | this system / ERP (copy) | |

## Integrations
- Core ERP base URL: <env var name>; API version: v1
- Outbox worker: <command>; webhook endpoint: <route>
- Other services: <payment, SMS, e-invoicing...>

## Design system
- Tokens file: <path>; theme attribute: <data-bs-theme / data-theme>
- DESIGN.md: <path or none>; template recipe in use: <dashboard / landing / ...>

## Business context
- Branches: <...>; VAT status: <...>; roles: <cashier, manager, admin...>

## Env vars (names only)
- <APP_URL, DB_*, ERP_API_URL, ERP_API_KEY, ...>
