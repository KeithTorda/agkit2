# JavaScript hot-path decisions

Use these techniques for a measured hot path or substantial data set. A shorter expression or fewer passes does not automatically make the user experience faster. Keep order, mutation, locale and numeric semantics intact.

## Rule 7.1: Avoid layout thrashing

Alternating DOM writes and layout reads can force repeated synchronous layout. Batch compatible reads, then writes, or use CSS/framework layout mechanisms. Preserve dependencies when a measurement intentionally follows a write. Verify the browser trace; not every property read causes layout.

## Rule 7.2: Index repeated lookups when worthwhile

A Map/Set can reduce repeated linear searches, but costs construction/memory and needs correct key identity. A single lookup in a short list rarely needs an index. Rebuild/invalidate the index when source data changes; stale indexes are correctness defects.

```js
const byId = new Map(records.map(record => [record.id, record]))
const selected = requestedIds.map(id => byId.get(id))
```

This assumes duplicate IDs have a deliberate policy and callers handle absent records. Constructing the map does not validate uniqueness.

## Rule 7.3: Bound and invalidate caches

Memoizing repeated expensive pure work may help. Include every semantic input in the key, bound memory and decide expiry/cleanup. Locale, permissions and normalization can change results. Caching storage/cookie reads can make preferences or identity stale. A module-level Map is not a safe default for server user data.

## Rule 7.4: Combine iteration only when clearer or proven

Multiple array passes can be perfectly readable and adequate. A combined loop can reduce allocation on large hot paths, but preserve order, short-circuiting, sparse-array semantics and side effects. Do not rewrite ordinary `map`/`filter` chains across the repository as a performance ritual.

## Rule 7.5: Check cheap conditions when semantics allow

Short-circuit inexpensive guards before expensive pure comparisons if it reduces real work. Reordering may change observable side effects, thrown errors or timing-sensitive behavior. Verify null/empty handling and compare expected distributions rather than choosing from intuition alone.

## Rule 7.6: Reuse regular expressions carefully

Reuse expensive expressions when useful, but global/sticky regular expressions carry mutable `lastIndex`. Hoisting one can create surprising repeated-test behavior. Bound input and assess pathological patterns when untrusted text can cause excessive backtracking.

## Rule 7.7: Choose the required algorithm

A single min/max needs a linear scan rather than sorting the whole collection. Define behavior for empty input, NaN and mixed numeric types. Spread into `Math.max` can fail for very large argument lists; a loop may be appropriate. Use a representative benchmark when this is a claimed bottleneck.

## Rule 7.8: Preserve collection ownership

Do not mutate props/state/shared arrays accidentally with `sort`. Use a supported nonmutating method or copy first when ownership requires it. Runtime support for newer methods must match the deployed environment; do not introduce a polyfill or upgrade without need. Define locale/numeric comparator semantics explicitly when relevant.

Verify observable results and comparable timing/memory. Avoid fragile microbenchmarks that exclude warmup, input distribution or real allocation costs.
