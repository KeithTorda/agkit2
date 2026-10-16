# Pattern trade-offs reference

Patterns describe responsibilities and trade-offs; they do not certify scalability or code quality. Choose relevant rows and test the important failure boundary.

| Pattern | Useful when | Costs and failure questions |
|---|---|---|
| Direct ORM/query builder | Access patterns are clear and framework integration helps | Where do transactions, tenant filters and complex reads live? |
| Query object/repository | A meaningful data contract needs isolation or several implementations | Does the abstraction hide necessary query/isolation behavior? |
| Transaction script/action | A use case has a coherent sequence of operations | Are shared invariants duplicated or effects partially committed? |
| Domain model/state machine | Multiple paths share rules and allowed transitions | Is the model clearer than the underlying use cases? |
| Monolith | A unified deployment and data boundary fit | Can modules retain ownership; which workloads contend? |
| Modular monolith | Domains need clearer contracts within one deployment | Are imports/data writes actually constrained across modules? |
| Independently deployed services | Isolation, release/runtime or workload needs justify network boundaries | Who owns each fact, failure, contract, retry and operation? |
| Events/durable jobs | Work outlives requests or consumers are independent | Are delivery, duplicates, poison work and schema changes handled? |
| CQRS/read model | Read shape/cost materially differs from authoritative writes | What lag is acceptable and how is the view rebuilt? |
| Event sourcing | Event history is authoritative and replay semantics are required | Can schemas evolve and past bugs be corrected safely? |
| Saga/compensating workflow | A business operation spans independent commit boundaries | Is compensation possible, visible and idempotent? |
| Local-first with sync | Useful work must continue without connectivity | What conflicts are allowed and which source wins? |

## Avoid misleading substitutions

An audit log is not necessarily event sourcing. A background callback is not necessarily durable. A shared database transaction is not a distributed transaction. A type shared between services is not a deployed compatibility strategy. A queue does not guarantee exactly-once business effects.

## Evaluate the change cost

Some patterns are inexpensive to introduce later; others require substantial data, API or operating migrations. Estimate from this repository and deployment rather than asserting all complexity is cheap to add. Prefer boundaries that improve the current problem and preserve realistic options.

API style comparisons belong in `api-patterns`; schema/isolation detail belongs in `database-design`.
