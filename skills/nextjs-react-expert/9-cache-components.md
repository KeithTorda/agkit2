# Cache scope, freshness and supported Cache Components

Use when a trace or product requirement justifies caching, or when stale/incorrect data needs diagnosis. Start from the installed Next.js version/router, configuration, deployment adapter and existing cache mechanism. Do not enable Cache Components or upgrade the application merely to match this reference.

## Define the cache contract first

For each candidate, identify:

- **Owner/source:** which authoritative operation changes the data?
- **Scope:** request, browser session, process, deployment or shared external cache?
- **Key:** which inputs, actor/tenant permissions and locale affect the result?
- **Freshness:** what staleness is acceptable, and what must be read immediately after a write?
- **Lifetime/capacity:** eviction, memory/storage bounds and behavior across instances/redeploys?
- **Failure:** stale response, negative/error caching, dependency outage and concurrent misses?
- **Invalidation:** who invalidates/updates it, and can a failed step leave users seeing stale data?

A cache is not a source of truth. Authorization must remain correct on a hit as well as a miss. Never share private/current-user output under a public key.

## Choose a supported mechanism

Request memoization, explicit fetch caching, route/static output, query-library caches, process LRUs and distributed stores have different guarantees. Framework defaults change by release/configuration. Inspect the actual build/runtime behavior and official installed-version docs before changing `fetch`, segment options or persistence.

A serverless process may be reused or disappear; neither persistent sharing nor complete isolation follows from the word "serverless". Multi-instance invalidation needs an actual shared framework/provider contract.

## When Cache Components is actually available

For Next.js projects that support and enable Cache Components, the documented API may include `'use cache'`, `cacheLife`, `cacheTag` and mutation invalidation helpers. Verify exact imports, configuration, directive restrictions and supported runtime for the installed version before writing code.

A cached computation should take explicit appropriate inputs and return supported serializable output. Request-specific APIs such as cookies/headers may be constrained inside a cached scope; resolve access/identity using the documented pattern rather than reading ambient state and assuming it enters the key.

Lifetime profiles govern staleness/revalidation/expiry with specific semantics; read their actual definitions instead of hard-coding remembered durations. Choose a profile from product freshness needs. Tags group invalidation; they do not establish authorization or automatically include every read of the same record.

## Mutations and read-your-write behavior

After a successful authoritative write, invalidate/update the actual read caches. Helpers such as `updateTag`, `revalidateTag`, `revalidatePath` or `refresh` differ by supported context, version and whether they expire cached data or refresh a client view. Do not treat these names as interchangeable or copy a deprecated signature from another release.

If invalidation fails after commit, preserve the fact that the write succeeded and define recovery. Retrying the business mutation is not automatically a safe invalidation fix. Client query caches and server caches may both need updates.

## Streaming and pre-rendering

Supported partial/static rendering can combine cached and dynamic regions, often with Suspense boundaries. Check actual configuration and output; not every uncached expression has the same behavior in every release. Ensure fallback sizing/accessibility and do not make authentication assumptions from a prerendered shell.

## Verification matrix

Exercise hit/miss, changed key dimensions, cross-user/tenant denial, mutation then immediate read, expiry/revalidation, concurrent miss and relevant instance/redeploy behavior. Observe actual headers/logs/requests where useful. A faster second request does not prove safe isolation or correct invalidation. Report measured benefits and remaining limits.
