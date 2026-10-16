---
part: 31
title: Frontend framework behavior
covers: effects, state, data, components, keys, memoization, refs, forms, server boundaries, library customization, Vue, Svelte
---

# 31 - Frontend framework behavior

Read for React, Next.js, Vue, Nuxt, Svelte, or similar component applications. Use the project's actual framework version and conventions. A default component library is not inherently poor design; style and behavior should serve the user-approved direction.

## State and effects

Keep the smallest useful source of truth. Derive values during rendering when feasible rather than synchronizing duplicate state with effects. Local state suits local interaction; context or a store suits shared state when its lifecycle and ownership are clear. Do not add a global store just because a scaffold includes one.

Effects synchronize with systems outside rendering: subscriptions, DOM APIs, timers, widgets, or network work where that architecture is appropriate. Clean up resources, handle cancellation or stale responses, and avoid feedback loops. Do not move user-triggered mutations into effects without a reason. Framework data loaders or server fetching may simplify data access, but client effects are valid where their contract is implemented correctly.

## Data and mutation states

Model loading, empty, error, stale, partial, and success states that can actually occur. Distinguish a failed request from an empty dataset. Preserve useful data during refetching when appropriate. Cache keys should include relevant parameters and identity scope; invalidate or reconcile after mutation.

Prevent duplicate effects from repeated interaction. Optimistic updates need rollback and conflict handling; payment and authorization decisions require authoritative state. Validate on the server even if the form validates locally. A UI hidden behind a client condition does not enforce permission.

## Component boundaries and lists

Split a component when a meaningful responsibility, reusable contract, or complex lifecycle becomes clearer. Do not enforce a universal line count or create a primitive for every wrapper. Composition can avoid unnecessary prop forwarding; context can avoid broad threading when shared meaning warrants it.

List keys need stable identity when items reorder, filter, or accept insertion. Index keys can be fine for truly static lists. Do not generate a new random key each render. Labels and ARIA references in repeated components need unique stable IDs, especially with server rendering.

## Performance and direct DOM work

Measure expensive rendering before broad memoization. Memo helpers need meaningful cost and stable dependencies to help. Avoid stale closures and incomplete dependency contracts. Virtualization can help large lists but needs keyboard, screen reader, and sizing consideration.

Use refs for imperative boundaries rather than bypassing normal state flow everywhere. Untrusted HTML injection requires a deliberate sanitization strategy. A string cast or client-only rendering does not make it safe.

## Framework boundaries and styling

In Next.js or similar hybrid frameworks, keep secrets and privileged access on the server, and place client boundaries where interactivity or browser APIs require them. Do not add `use client` everywhere by reflex, or remove it from a component that genuinely needs it. Verify serialization, hydration, data freshness, route behavior, and the installed routing conventions.

Metadata, images, fonts, forms, server actions, and route handlers should use the actual supported APIs. Do not assume a memory of another framework version is current. In Vue/Nuxt, preserve reactivity when destructuring, use stable keys, clean up watchers, and respect server/client access. In Svelte, follow the installed reactivity model rather than mixing incompatible syntax.

Use library primitives for accessibility and behavior, then customize tokens, layout, typography, effects, and variants to the selected direction. Retain an existing design system where required. Do not add an animation or UI library solely because a reference uses its aesthetic; choose by actual implementation needs and cost.

## Review

Check actual rendered states, hydration warnings, console/runtime errors, navigation, form behavior, and relevant small-screen interactions. A successful build does not prove that the UI matches the reference or that a server mutation is authorized.
