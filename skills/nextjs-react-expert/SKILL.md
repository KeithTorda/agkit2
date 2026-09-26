---
name: nextjs-react-expert
description: React 19.2 and Next.js 16 guidance (App Router, React Compiler, Cache Components, proxy.ts) with performance rules for waterfalls, bundle size, server work, re-renders and rendering. Use when building React components or Next.js pages, fixing slow loads or excess re-renders, upgrading to Next.js 16, or reviewing a React/Next.js codebase for performance.
version: 2.5.0
---

# Next.js and React

Rules distilled from Vercel Engineering's React best practices, updated for Next.js 16 (App Router, Turbopack) and React 19.2 with the React Compiler. Order of work when something is slow: remove waterfalls, then shrink the bundle, then fix server work, then micro-optimise. Measure before and after; most code never needs sections 7-8.

## Next.js 16 and React 19.2 facts to get right

- **Async request APIs.** `params`, `searchParams`, `cookies()`, `headers()` and `draftMode()` are async; synchronous access was removed in 16. `const { id } = await params`.
- **`proxy.ts` replaces `middleware.ts`.** Same idea (runs before routes), renamed, Node.js runtime by default. `middleware.ts` still works for the edge runtime but is deprecated. Do not put authorisation only here: check it in each Server Action and Route Handler too (section 3.1).
- **Turbopack is the default** for `next dev` and `next build`. A custom webpack config needs `--webpack` or a migration.
- **React Compiler** is stable: `reactCompiler: true` at the top level of `next.config.ts` (with `babel-plugin-react-compiler` installed); Expo uses the Babel plugin.
- **Caching** is opt-in with Cache Components: `cacheComponents: true`, `'use cache'`, `cacheLife`, `cacheTag`, `updateTag`, `revalidateTag(tag, profile)`. See `9-cache-components.md`.
- **`next lint` is gone.** Run the project's ESLint script (`npm run lint`, else `npx eslint .`) with `eslint-config-next` in flat config, and `npx tsc --noEmit`.
- **React 19.2:** `<Activity>` for hidden-but-kept UI, `useEffectEvent` for effect callbacks that read the latest values, `use()` for promises and context, Actions with `useActionState` / `useFormStatus` / `useOptimistic`, `ref` as a plain prop (no `forwardRef` in new code).
- **Animation:** `motion/react` (the package formerly `framer-motion`); scroll-linked effects use CSS scroll-driven animations or `useScroll`, never a scroll listener that sets React state.

Follow the project's version: on Next.js 15 or earlier, use its APIs (sync request APIs, `middleware.ts`, `fetch` cache options) and do not half-migrate.

## The memo rule (single statement for the kit)

When the React Compiler is enabled, do not add `useMemo` / `useCallback` / `React.memo` by default; the compiler memoises components, hooks and JSX. Reach for manual memo only when the compiler bailed out on a component or a profile shows a hot path. Check the flag before removing existing memo: compiler off plus stripped memo is a regression. Bailout detection and the remaining valid uses: `5-rerender-re-render-optimization.md`. Other kit files point here.

## Data layer default

Server Components for reads; Server Actions + `useActionState` for mutations; TanStack Query only for client-interactive server state (polling, infinite lists, optimistic UI). Decision detail: `frontend-architecture`; client rules: `4-client-client-side-data-fetching.md`.

## Reading map

Read only the section that matches the task.

| File | Impact | Read when |
|------|--------|-----------|
| `1-async-eliminating-waterfalls.md` | Critical | Slow page loads, sequential `await`s, data-fetching waterfalls |
| `2-bundle-bundle-size-optimization.md` | Critical | Large bundles, slow Time to Interactive, barrel imports |
| `3-server-server-side-performance.md` | High | Slow SSR, Server Action auth, RSC serialization, `after()` |
| `4-client-client-side-data-fetching.md` | Medium-high | Client data layer, TanStack Query, shared listeners, localStorage |
| `5-rerender-re-render-optimization.md` | Medium | Excess re-renders, derived state, key resets, context splitting, transitions |
| `6-rendering-rendering-performance.md` | Medium | `content-visibility`, hydration flicker, `<Activity>`, `useTransition` |
| `7-js-javascript-performance.md` | Low-medium | Hot-path micro-optimisations, layout thrashing |
| `8-advanced-advanced-patterns.md` | Variable | Init-once, `useEffectEvent` |
| `9-cache-components.md` | Critical (Next.js 16) | `use cache`, `cacheLife`, `cacheTag`, partial prerendering |

## Symptom to section

| Symptom | Start with |
|---------|-----------|
| Slow first load / long TTI | 1, then 2 |
| Main chunk well over ~200 KB gzipped | 2 |
| Slow server render or API route | 3, then 9 |
| UI lag, too many renders | 5 (memo rule above first) |
| Scroll jank, layout shift, hydration flash | 6 |
| Redundant client requests | 4 |
| Stale or over-fetched cached data | 9 |

## Review prompts

Use these when reviewing; weight them by what the page does.

- **Correctness and security (firm):** Server Actions and Route Handlers validate input and check auth and ownership inside the function; no secrets or server-only modules imported into Client Components.
- **High impact:** no sequential `await` for independent work; Suspense around slow data; `"use client"` pushed to the interactive leaf (the directive pulls its whole import subtree into the client bundle); heavy client-only widgets loaded with `next/dynamic`; only needed fields cross the RSC boundary; no N+1 queries in server code.
- **Medium:** long lists virtualised or `content-visibility: auto`; images through `next/image` with sizes; no state derived in effects; memo follows the rule above.

## Script (advisory)

`react_performance_checker.py <project>` is a static check. Errors (App Router mistakes that break build or runtime): a `'use client'` file exporting `metadata`, an async client component, a server page or layout importing client hooks, `error.tsx` without `'use client'`. Warnings: `.map()` list items without a `key`, independent sequential `await`s (request waterfall), whole-library icon imports. Info: `<img>` instead of `next/image`, `/index` barrel imports, `fetch` in `useEffect`, index as key, very large client components. Flags: `--json`, `--verbose`, `--fail-on error|warning|never` (default `error`; `--fail-on-warnings` is an alias for `warning`). It is pattern-based: a flagged `await` chain is fine when the second call depends on the first, so review each finding before changing code. It does not check memoisation.

```powershell
python "KIT/skills/nextjs-react-expert/scripts/react_performance_checker.py" .
```

## Related skills

`frontend-architecture` (state and data-layer decisions), `tailwind-patterns` (styling), `api-patterns` (API shape), `database-design` (query performance), `testing-patterns` (tests), `performance-profiling` (Lighthouse, Web Vitals and bundle analysis).
