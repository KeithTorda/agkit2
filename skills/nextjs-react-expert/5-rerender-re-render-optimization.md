# State correctness and render work

React rendering is not itself a defect. Use the profiler/trace to locate expensive work and distinguish render, commit, layout and effects. Respect the installed compiler and existing memo contracts without assuming all files are compiled.

## Rule 5.1: Derive what is already determined

A value computed from current props/state usually need not be mirrored through an effect into new state. Compute it during render if pure and reasonably cheap. Memoize only when its cost/reference contract warrants it. Store a separate value when it represents independent user intent or history, not merely a duplicate.

```tsx
const visibleItems = items.filter(item => matches(item, query))
```

This must be pure; do not mutate `items` or issue effects during rendering.

## Rule 5.2: Reset from identity deliberately

A `key` can remount a subtree when it represents a different entity. It also discards local state, focus and pending work; use it only when that is intended. An effect/state transition can be valid for partial synchronization. Do not force remounts to hide stale-state bugs.

## Rule 5.3: Subscriptions follow update needs

Split context/store selectors when broad updates cause meaningful wasted work or obscure ownership. Context is not prohibited for frequently updated values. Compare provider scope, subscription behavior and complexity before replacing a working design.

## Rule 5.4: Read state where it is needed

Narrow subscriptions can reduce work, but reading only inside an event handler changes reactivity. Use that approach only when the UI does not need updates. Do not remove a router/permission subscription solely to lower a render count.

## Rule 5.5: Observe a semantic signal

A media-query boolean or derived store selector may serve a threshold-based UI better than tracking every pixel. High-frequency values may still be needed for direct visual motion. Keep the authoritative value and accessibility behavior coherent.

## Rule 5.6: Events and effects have different jobs

User actions belong naturally in event handlers. Effects synchronize an external system with rendered state and need cleanup/dependencies. Do not trigger a purchase, notification or analytics event from a render-driven effect unless its duplicate/lifecycle semantics are intentional.

## Rule 5.7: Update from previous state safely

Use a functional setter when the next state depends on prior state, especially with queued/async updates:

```tsx
setCount(previous => previous + 1)
```

The updater stays pure. A functional setter does not fix unrelated stale captured props or server races.

## Rule 5.8: Initialize without repeated expensive work

A lazy initializer can avoid repeated computation during renders. It must remain pure and server/client consistent; development lifecycles may invoke it more than once. Browser-only reads need an explicit SSR/hydration strategy.

## Rule 5.9: Prioritize work according to semantics

Transitions/deferred values can keep urgent input responsive when supported. They do not make expensive synchronous calculation disappear or automatically cancel a network mutation. Keep controlled input state urgent; verify the installed React version's async transition behavior and expected pending/error state.

## Rule 5.10: Transient visual values need not be state

Refs, CSS and adopted motion values can avoid rendering for every pointer/scroll event. Use state for values that must update rendered content. Direct DOM mutation must have clear ownership and cleanup; do not desynchronize React-owned DOM.

## Rule 5.11: Memoization is conditional

Keep/add/remove manual memoization based on measured cost, stable-reference contracts and actual compiler coverage. Do not delete all memo calls merely because a compiler flag is enabled. Never depend on a memo cache to preserve business state or guarantee an effect runs once.

Verify behavior and compare the same interaction profile after changes, including navigation, identity changes and development lifecycle cleanup.
