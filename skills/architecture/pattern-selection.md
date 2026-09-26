# Pattern Selection

Decision trees for the common architecture questions. They give the default; the project's real constraints can override them, and the override goes in an ADR.

## Decision tree

```
What is the main concern?

Data access complexity
  LOW (CRUD, one database)        -> use the ORM directly (Eloquent, Prisma, Drizzle, SQLAlchemy)
  HIGH (complex queries, several sources, heavy testing needs)
                                  -> repository or query objects around the hard parts only
     Check: will the data source really change, or do tests need the seam? If not, stay direct.

Business rule complexity
  LOW (validation, simple CRUD)   -> transaction script: one action or service function per use case
  HIGH (rules vary by context, many invariants)
                                  -> rich domain model around the core (pricing, stock, grading, ballots)
     Check: are the rules stable and understood? Partial DDD (entities with behaviour,
     clear module boundaries) is usually enough; full DDD needs domain experts in the loop.

Independent scaling or deployment
  NO                              -> modular monolith (extract later if proven)
  YES                             -> separate services are worth it when most of these hold:
                                     clear domain boundaries, separate teams, different scaling
                                     or release needs, and the ops capacity to run them

Real-time or async needs
  Updates must reach users instantly (dashboards, queues, chat)
                                  -> push: WebSocket / SSE / Laravel Reverb / a provider (Pusher, Ably, Supabase Realtime)
  Work can finish later (e-mail, SMS, reports, imports)
                                  -> background jobs (Laravel queues, BullMQ, Celery/ARQ)
  Several systems react to one event
                                  -> event-driven, only if eventual consistency is acceptable;
                                     otherwise synchronous calls
  Otherwise                       -> synchronous request/response

Unreliable connectivity at the point of use (POS, field data collection)
                                  -> local-first client (IndexedDB / SQLite) with a sync queue and
                                     server-side idempotency keys; decide conflict rules up front
```

## The three questions (before any pattern)

1. **Problem solved:** what specific problem does this pattern solve here?
2. **Simpler alternative:** what is the simplest thing that would work, and why is it not enough?
3. **Deferred complexity:** can this be added later, when the need is proven?

## Over-engineering signs

| Pattern | Sign it is premature | Simpler alternative |
|---|---|---|
| Microservices | One team, one deploy cadence, shared database | Modular monolith |
| Clean / hexagonal layers | Interfaces with one implementation, mapping code everywhere | Concrete code first, extract a seam when a second implementation or a test needs it |
| Event sourcing | Only needed an audit trail | Append-only audit log table |
| CQRS | Reads and writes use the same shape | One model; a read-optimised query or view where needed |
| Repository | Wraps simple ORM calls one-to-one | Use the ORM directly |
| Message broker | Work fits in the request or a DB-backed queue | Laravel database queue, a jobs table, or `after()` |
