# Cache Components: `use cache` & `cacheLife`

> Next.js 16 only, with `cacheComponents: true` in `next.config.ts`. On Next.js 15 or earlier, or with the flag off, use the older `fetch` cache options and `export const revalidate`.

## Core idea
Next.js 16 moves from segment-level caching (`export const revalidate = 3600`, route-wide `dynamic` settings) to component- and function-level caching: a `'use cache'` directive plus `cacheLife` profiles and `cacheTag` labels. Everything not cached is dynamic and streams inside a Suspense boundary.

## 1. The `use cache` Directive
The `use cache` directive can be applied to **Server Components** or **Functions**.

### Rule: Granular Application
Wrap only the data-fetching function or the specific component that needs caching. Arguments and closed-over values become part of the cache key, so they must be serializable; request-scoped APIs (`cookies()`, `headers()`) cannot be read inside a cached scope.

```tsx
// Good: Granular function caching
async function getProduct(id: string) {
  'use cache'
  return await db.product.findUnique({ where: { id } })
}

// Good: Component-level caching
export default async function ProductCard({ id }: { id: string }) {
  'use cache'
  const product = await getProduct(id)
  return <div>{product.name}</div>
}
```

## 2. Using `cacheLife`
`cacheLife` defines the "Freshness" and "Staleness" of a cached item using pre-defined or custom profiles.

### Usage Pattern
```tsx
import { cacheLife } from 'next/cache'

async function getStockInfo() {
  'use cache'
  cacheLife('minutes') // Using a pre-defined profile
  return await fetchStocks()
}
```

### Profiles
Each profile sets three durations: `stale` (how long the client may reuse its copy without asking the server), `revalidate` (how often the server refreshes in the background), and `expire` (when the entry is dropped and the next request renders dynamically). Built-in profiles, from most to least fresh: `seconds`, `minutes`, `hours`, `days`, `weeks`, `max`. `default` applies when no profile is given: minutes of client staleness, background revalidation on the order of minutes, and a long expiry. Check the current `cacheLife` reference for the exact numbers before promising them; define custom profiles under `cacheLife` in `next.config.ts` when the built-ins do not fit.

```ts
// next.config.ts
const nextConfig = {
  cacheComponents: true,
  cacheLife: {
    catalog: { stale: 300, revalidate: 900, expire: 86400 },
  },
}
export default nextConfig
```

## 3. On-Demand Invalidation with `cacheTag`
`cacheTag` allows you to label cached data for selective purging.

### Implementation
```tsx
import { cacheTag } from 'next/cache'

async function getProfile(user: string) {
  'use cache'
  cacheTag(`profile-${user}`)
  return await db.user.findUnique(...)
}
```

### Revalidation
In a Server Action:
```tsx
import { revalidateTag, updateTag } from 'next/cache'

export async function updateProfile(user: string, data: any) {
  await db.user.update(...)

  // Choice A: mark stale, serve the old value once more while refreshing (stale-while-revalidate)
  revalidateTag(`profile-${user}`)

  // Choice B: expire now so the caller reads its own write on the next render
  updateTag(`profile-${user}`)
}
```

## 4. Partial Prerendering (PPR)
With `cacheComponents` on, each route is split into a static shell (cached and prerendered) and dynamic holes that stream at request time.

### Pattern: Suspense boundaries
Uncached, request-time work must sit inside `<Suspense>`; the build errors otherwise. The fallback becomes part of the static shell.

```tsx
import { Suspense } from 'react'
import { Skeleton } from '@/components/ui/skeleton'

export default function Page() {
  return (
    <main>
      <h1>Static Header</h1>
      <Suspense fallback={<Skeleton />}>
        <DynamicCacheComponent />
      </Suspense>
    </main>
  )
}
```
