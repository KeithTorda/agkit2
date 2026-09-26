# Patterns Reference

Side-by-side comparison. API styles (REST, GraphQL, tRPC, gRPC, WebSocket) are compared in `api-patterns`.

## Data access

| Pattern | Use when | Avoid when | Complexity |
|---|---|---|---|
| Active Record (Eloquent, Django ORM) | CRUD-heavy apps, fast delivery | Rules must be tested without a database | Low |
| ORM / query builder direct (Prisma, Drizzle, Kysely) | Most TypeScript apps | Several unrelated data sources | Low |
| Repository | Tests need a seam, or data comes from several sources | Simple CRUD on one database | Medium |
| Unit of Work | Many aggregates change in one business transaction | Single-row operations | High |
| Data Mapper | Domain objects must not know about persistence | Simple CRUD | High |

## Domain logic

| Pattern | Use when | Avoid when | Complexity |
|---|---|---|---|
| Transaction script / action class | Clear use cases, modest rules | Rules interact heavily | Low |
| Table module | Record-based logic, reporting | Rich behaviour per entity | Low |
| Domain model | Rules with invariants (stock never negative, a ballot counted once) | Simple CRUD | Medium |
| Full DDD | Complex domain with experts involved | Small domain, no experts | High |

## System structure

| Pattern | Use when | Avoid when | Complexity |
|---|---|---|---|
| Monolith | Solo or small team, one product | - | Low |
| Modular monolith | Several domains, one deploy | Truly independent scaling needs | Medium |
| Services / microservices | Separate teams, scaling or release needs | Small team, shared database | Very high |
| Event-driven | Loose coupling, several consumers of one event | Strong consistency needed | High |
| CQRS | Read and write models diverge sharply | Same shape for both | High |
| Saga | A transaction spans services | One database (use a DB transaction) | High |
| Local-first + sync | Offline use at the point of work | Always-online admin tools | High |

Start simple and add complexity when it is proven necessary: adding a pattern later is cheap, removing one is expensive.
