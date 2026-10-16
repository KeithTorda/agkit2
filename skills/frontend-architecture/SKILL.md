---
name: frontend-architecture
description: Organize frontend code, state, data access and server/client boundaries around feature ownership. Use when adding behavior or restructuring frontend code; visual direction belongs to frontend-design and React performance to nextjs-react-expert.
version: 2.8.2
---

# Frontend Architecture

Put behavior where its owner and lifetime are clear. Inspect framework, routes, rendering mode, state/data libraries and conventions before choosing structure. Extend a coherent layout; do not migrate a small task into a preferred stack.

## Ownership before folders

Routes compose screens; features own domain interaction; shared UI contains stable primitives; shared services represent real cross-feature contracts. Small apps can stay flat. Extraction depends on shared meaning/change patterns, not fixed numbers of consumers or lines.

Separate presentation, validation, state transitions, data access and effects when that clarifies a real boundary. A short component may own a simple request; a complex workflow may need a hook/service or framework loader. Avoid both giant mixed-responsibility files and layers that only forward calls.

## Data and state fit the environment

Use existing server loaders/rendering for server-owned data where suitable. Client fetching fits interactive freshness, offline work, browser-only data and SPA architecture. Keep the adopted query library; do not require TanStack Query, Server Actions or a global store for every feature.

Classify state as server data, URL/shareable state, form edits, local UI or shared client workflow. Give it one authority and explicit synchronization. URLs suit deep-linkable filters, not every temporary toggle. Server data can live in an existing Redux/query cache with sound invalidation.

For React server/client composition, keep secrets and server-only modules outside the client graph. Choose understandable interaction boundaries that avoid needless client code; they need not be the smallest possible leaf. Verify serialization and hydration with the installed framework.

## Complete interactions

Handle relevant loading, empty, error and success states. Forms preserve input on expected failure, associate errors with fields and prevent inappropriate duplicate writes. Server validation/authorization protects mutations even when client validation exists.

Account for stale responses, navigation, cancellation and optimistic rollback. Real-time subscriptions need cleanup and a source-of-truth strategy. Include locale, tenant and access identity in cache keys when they affect results.

Read [structure-reference.md](structure-reference.md) for layouts, state/data decisions, framework variants and refactoring seams. Use `testing-patterns` for behavior coverage and `nextjs-react-expert` for measured React/Next.js performance.

## Validate changed boundaries

Inspect affected callers/imports, runtime states and real interactions. Run static checks for changed type/build boundaries and inspect rendered UI when structure affects layout/behavior. A neat folder tree does not demonstrate a working frontend.
