# Async dependencies and critical-path work

Use when traces show avoidable sequential I/O. List dependencies, authorization and capacity before parallelizing. Sequential awaits are correct when later work depends on an earlier result or ordering is part of the contract.

## Rule 1.1: Await only work the branch needs

Move optional work into the branch that uses it. Do not start a request before knowing it is needed if it is expensive, sensitive or has side effects. If a started promise may be abandoned, handle its rejection/cancellation deliberately.

```ts
async function loadReport(includeHistory: boolean) {
  const summary = await getSummary()
  if (!includeHistory) return { summary }
  const history = await getHistory()
  return { summary, history }
}
```

Here history depends on a branch. If both results are always required and independent, concurrent execution may be better. Confirm actual ownership/access checks in real implementations.

## Rule 1.2: Parallelize a dependency graph

Start independent authorized operations together, then await their real dependents. A promise graph often needs no library.

```ts
const [profile, settings] = await Promise.all([
  loadAuthorizedProfile(actor),
  loadAuthorizedSettings(actor),
])
const recommendations = await loadRecommendations(profile.category)
```

The sample assumes `actor` was already validated and each loader checks required scope. Do not fetch protected user data in parallel with an unresolved authorization decision unless the data boundary itself safely enforces that decision.

## Rule 1.3: Trace the whole route

Inspect page/loader/route and downstream service/query work. A route can appear parallel while an N+1 occurs inside a loader. Route handlers and server actions are still external entry points; their validation/access and transaction boundaries come before optimization.

## Rule 1.4: Bound concurrency and failure

`Promise.all` suits results that must all succeed and are safe to overlap. It rejects early without cancelling siblings. `Promise.allSettled` suits independent partial outcomes. Neither bounds an arbitrary list's fan-out. Use a worker pool/batching supported by the project when many requests compete for a connection/rate budget.

For external calls, combine a deadline with supported abort signaling and cleanup. `Promise.race` alone ends waiting, not work. Never retry a timed-out mutation blindly when its commit status is unknown.

## Rule 1.5: Stream useful regions

Supported Suspense/streaming boundaries can reveal useful content while slow regions load. Choose boundaries from user tasks and failure/recovery behavior, not around every component. Reserve appropriate space to avoid disruptive shifts and ensure fallbacks remain accessible.

Server rendering, framework caching and promise-sharing differ by installed version/router. Verify actual requests and streaming in production-like output rather than assuming composition automatically parallelizes every query.

## Rule 1.6: Post-response work has a lifetime

Framework helpers such as `after()` or request-boundary APIs such as `connection()` are version/configuration-specific. Adopt them only when the installed framework documents the intended behavior. A post-response callback is not a durable queue; do not move business-critical writes there merely to shorten response time.

See [3-server-server-side-performance.md](3-server-server-side-performance.md) for server lifetimes and [9-cache-components.md](9-cache-components.md) for cache contracts. Re-measure the same request and check failure/access behavior after a concurrency change.
