---
name: nextjs-react-expert
description: Implement and diagnose React/Next.js rendering, data, caching and performance with the project's actual framework capabilities. Use for React components or Next.js behavior/performance; verify version-specific APIs and avoid unsolicited migrations.
version: 2.8.2
---

# React and Next.js Engineering

Inspect manifest/lockfile, router, runtime, build configuration, compiler flags and deployment before applying a pattern. React/Next.js capabilities and defaults vary by version/configuration. Use installed-version official documentation when adopting an API; do not upgrade the app to satisfy a remembered example.

## Correctness and measured work

Preserve component purity, stable identity, state ownership and cleanup. Runtime input, server actions and route handlers still need validation and authorization. Server rendering is not an access-control boundary by itself. Keep secrets/server-only modules outside client dependency graphs.

For performance work, identify a real bottleneck before choosing a rule. A waterfall, bundle, server query, rerender and paint problem need different evidence. Removing every sequential await or adding memoization everywhere can introduce errors and complexity.

The memo rule: preserve meaningful existing memoization; add/remove `memo`, `useMemo` or `useCallback` based on semantics, a measured issue and actual compiler coverage. A compiler flag does not prove every file is optimized. Memoization is not a correctness guarantee or a replacement for sound dependencies.

## Read only the relevant reference

| Reference | Use when |
|---|---|
| [1-async-eliminating-waterfalls.md](1-async-eliminating-waterfalls.md) | Critical-path I/O, dependencies and bounded parallelism |
| [2-bundle-bundle-size-optimization.md](2-bundle-bundle-size-optimization.md) | Production client payload/import/loading decisions |
| [3-server-server-side-performance.md](3-server-server-side-performance.md) | Server authorization, data access, serialization and lifetimes |
| [4-client-client-side-data-fetching.md](4-client-client-side-data-fetching.md) | Client fetching, query ownership, subscriptions and storage |
| [5-rerender-re-render-optimization.md](5-rerender-re-render-optimization.md) | State/effect correctness and measured render work |
| [6-rendering-rendering-performance.md](6-rendering-rendering-performance.md) | Hydration, layout, long lists and motion |
| [7-js-javascript-performance.md](7-js-javascript-performance.md) | Proven hot paths and layout thrashing |
| [8-advanced-advanced-patterns.md](8-advanced-advanced-patterns.md) | Initialization, external callbacks and lifecycle subtleties |
| [9-cache-components.md](9-cache-components.md) | Cache scope, isolation, invalidation and supported Cache Components |

## Validate behavior and delivery

Exercise relevant loading/error/empty states, navigation, duplicate input and stale response cases. Check a production build/real browser where the changed server/client or rendering contract requires it. For an optimization, compare equivalent before/after traces or asset evidence and confirm behavior remains correct.

`python "KIT/skills/nextjs-react-expert/scripts/react_performance_checker.py" .` reports source heuristics. Supports `--json`, `--verbose`, `--fail-on error|warning|never`, plus legacy `--fail-on-warnings`. Treat findings as prompts to inspect, not proof of render cost or mandatory refactoring.

Use `frontend-architecture` for ownership, `performance-profiling` for baseline evidence and `testing-patterns` for meaningful regression coverage. Visual style belongs to the user's brief and `frontend-design`.
