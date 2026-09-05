---
name: nextjs-react-expert
description: React 19 and Next.js 16 performance guidance (App Router, React Compiler, Cache Components). Use when building React components or Next.js pages, eliminating data-fetching waterfalls, reducing bundle size, fixing re-render or rendering bottlenecks, or reviewing a React/Next.js codebase for performance.
version: 2.0.0
---

# Next.js & React Performance

Rules distilled from Vercel Engineering, updated for Next.js 16 (App Router, Turbopack) and React 19.2 with the React Compiler enabled. Order of work: eliminate waterfalls, then shrink the bundle, then fix server-side work, then micro-optimize.

## Baseline assumptions

- Compiler-first when the React Compiler is enabled (`reactCompiler: true` in next.config / babel-plugin-react-compiler in Expo — the kit's templates enable it); check the flag before removing manual memo. With the compiler on, do not add `useMemo`, `useCallback`, or `React.memo` by default; add them only when the compiler bails out on a component or profiling shows a hot path. See `./5-rerender-re-render-optimization.md`.
- Server Components for reads; Server Actions + `useActionState` for mutations; TanStack Query only for client-interactive server state (polling, infinite lists, optimistic UI). See `./4-client-client-side-data-fetching.md`.
- `next lint` no longer exists. Run the project's own ESLint script (`npm run lint` if defined, otherwise `npx eslint .`) and `npx tsc --noEmit`.
- Animations: `motion/react` (not `framer-motion`); scroll-driven effects use CSS scroll-driven animations or `useScroll` from `motion/react`, never a scroll listener that sets React state.

## Reading map

Read only the section that matches the task.

| File | Impact | Read when |
|------|--------|-----------|
| `./1-async-eliminating-waterfalls.md` | Critical | Slow page loads, sequential `await`s, data-fetching waterfalls |
| `./2-bundle-bundle-size-optimization.md` | Critical | Large bundles, slow Time to Interactive, barrel imports |
| `./3-server-server-side-performance.md` | High | Slow SSR, Server Action auth, RSC serialization, `after()` |
| `./4-client-client-side-data-fetching.md` | Medium-high | Client data layer, TanStack Query, shared listeners, localStorage |
| `./5-rerender-re-render-optimization.md` | Medium | Excess re-renders, derived state, key resets, context splitting, transitions |
| `./6-rendering-rendering-performance.md` | Medium | `content-visibility`, hydration flicker, `<Activity>`, `useTransition` |
| `./7-js-javascript-performance.md` | Low-medium | Hot-path micro-optimizations, layout thrashing |
| `./8-advanced-advanced-patterns.md` | Variable | Init-once, `useEffectEvent`, handler refs |
| `./9-cache-components.md` | Critical (Next.js 16) | `use cache`, `cacheLife`, `cacheTag`, PPR |

## Symptom to section

| Symptom | Start with |
|---------|-----------|
| Slow first load / long TTI | 1, then 2 |
| Bundle over ~200 KB gzipped for the main chunk | 2 |
| Slow server render or API route | 3, then 9 |
| UI lag, too many renders | 5 (check the compiler is active before adding memo) |
| Scroll jank, layout shift, hydration flash | 6 |
| Redundant client requests | 4 |
| Stale or over-fetched cached data | 9 |

## Review checklist

Critical: no sequential `await` for independent work; no barrel imports of large libraries in app code; heavy components loaded with `next/dynamic` from a Client Component; Suspense boundaries around slow data; Server Actions verify auth and validate input inside the action.

High: Server Components by default, with the `"use client"` boundary pushed to the interactive leaf, not a page or layout (a high directive drags its whole import subtree into the client bundle); no N+1 queries in route handlers; static or cached rendering where content allows; only needed fields cross the RSC boundary.

Medium: long lists virtualized or `content-visibility: auto`; images through `next/image`; no state derived in effects; with the compiler on, no manual `useMemo` / `useCallback` / `React.memo` added by default — and do not strip existing memo without first confirming the compiler flag is actually on (off plus stripped memo is the regression).

## Script

`./scripts/react_performance_checker.py <project_path>` flags consecutive `await`s (critical), barrel imports, large components imported statically, `useEffect` data fetching, and `<img>` without `next/image`. It is regex-based and advisory: a flagged `await` chain is fine when the second call depends on the first, so review before changing code. Only critical findings return exit code 1 (`--fail-on-warnings` makes warnings blocking too). It does not check memoization.

```powershell
python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/nextjs-react-expert/scripts/react_performance_checker.py .
```

## Related skills

`@[skills/frontend-architecture]` for state and data-layer decisions, `@[skills/tailwind-patterns]` for styling, `@[skills/api-patterns]` for API shape, `@[skills/database-design]` for query performance, `@[skills/testing-patterns]` for tests, `@[skills/performance-profiling]` for Lighthouse and bundle analysis.
