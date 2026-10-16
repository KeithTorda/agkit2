# Discover architecture context

Use this reference when a structural choice depends on constraints that are not yet established. Start from repository/configuration evidence, requirements and existing operations. Avoid inferring the product, country, scale or maintainer's preferences from examples in this kit.

## Evidence to gather selectively

| Area | What changes the decision | Useful evidence |
|---|---|---|
| User outcome | Critical workflows, deadlines, availability expectations | Brief, support cases, acceptance criteria |
| Domain | Facts that must remain consistent, ownership, retention | Rules, schemas, production incidents |
| Load | Peak concurrency, read/write mix, payloads, growth | Logs, traces, representative data, explicit forecasts |
| Operations | Deploy cadence, observability, recovery, staffing | CI/deploy config, runbooks, ownership |
| Environment | Hosting limits, runtime, connectivity, devices | Manifests, infrastructure, actual device/network use |
| Integrations | Protocols, latency, reliability, external ownership | Client code, contracts, failure reports |
| Security/data | Tenant boundaries, sensitive assets, access/retention needs | Identity model, data flows, actual requirements |
| Change cost | Compatibility windows, migration risk, budget | Existing consumers, release constraints, team evidence |

Do not needlessly investigate every row. A local module split may require only imports and callers; a tenancy migration needs data ownership and rollout evidence.

## Separate fact from assumption

Record material items as confirmed, inferred or unknown. Attach evidence where useful. User counts without workload context are weak predictors: 100 active staff doing complex writes can differ from many anonymous cached readers.

Define measurable quality requirements when possible: acceptable response behavior under a named load, recovery point/time targets, data durability, supported offline duration. Do not manufacture numbers to make a plan look precise.

## Resolve a consequential unknown

Ask when competing reasonable answers would materially change the decision and evidence cannot settle it. Keep the question tied to the outcome, with viable options/trade-offs. For an inexpensive reversible choice, state a grounded assumption and proceed within scope.

An offline requirement needs a real definition: read cached content, create drafts, complete payments, or reconcile independent stock? These imply different storage and conflict contracts.

## Useful output

A concise context summary should identify the current system, intended outcome, decisive constraints, important invariants and unresolved assumptions. No project-size classification or fixed stack follows automatically. Carry this evidence into [pattern-selection.md](pattern-selection.md) and an ADR only when the decision merits one.
