# 4. Client-Side Data Fetching

> **Impact:** MEDIUM-HIGH
> **Focus:** Fetch server data in the right layer, deduplicate what must run on the client, and keep browser storage small and versioned.

---

## Overview

Four rules. The data-layer default for this kit: Server Components for reads, Server Actions + `useActionState` for mutations, and TanStack Query only for client-interactive server state such as polling, infinite lists, and optimistic UI (decision tree in `@[skills/frontend-architecture]`). Do not introduce SWR; replace it with TanStack Query when you meet it.

---

## Rule 4.1: Share Global Event Listeners with `useSyncExternalStore`

**Impact:** LOW  
**Tags:** client, event-listeners, subscription, useSyncExternalStore  

When many component instances need the same `window` or `document` event, register one listener at module level and let components subscribe through `useSyncExternalStore`. N hook instances then cost one native listener.

**Incorrect (N instances = N listeners):**

```tsx
function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && e.key === key) callback()
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [key, callback])
}
```

**Correct (N instances = 1 listener):**

```tsx
import { useEffect, useSyncExternalStore } from 'react'

// Module-level store: one listener, many subscribers
const callbacks = new Map<string, Set<() => void>>()
let listening = false
let lastKey = ''
const listeners = new Set<() => void>()

function ensureListener() {
  if (listening) return
  listening = true
  window.addEventListener('keydown', (e) => {
    if (!e.metaKey) return
    lastKey = e.key
    callbacks.get(e.key)?.forEach((cb) => cb())
    listeners.forEach((notify) => notify())
  })
}

function subscribe(notify: () => void) {
  ensureListener()
  listeners.add(notify)
  return () => listeners.delete(notify)
}

export function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    if (!callbacks.has(key)) callbacks.set(key, new Set())
    callbacks.get(key)!.add(callback)
    return () => {
      callbacks.get(key)?.delete(callback)
      if (callbacks.get(key)?.size === 0) callbacks.delete(key)
    }
  }, [key, callback])

  // Subscribing keeps the single listener alive; the snapshot is only needed if you render it.
  useSyncExternalStore(subscribe, () => lastKey, () => '')
}
```

The same pattern works for `matchMedia`, `resize`, `online`/`offline`, and `visibilitychange`. `useSyncExternalStore` also gives a server snapshot, so components hydrate without mismatches.

---

## Rule 4.2: Use Passive Event Listeners for Scrolling Performance

**Impact:** MEDIUM  
**Tags:** client, event-listeners, scrolling, performance, touch, wheel  

Add `{ passive: true }` to `touchstart`, `touchmove`, and `wheel` listeners that never call `preventDefault()`. Without it the browser must wait for the handler before scrolling.

```typescript
useEffect(() => {
  const handleWheel = (e: WheelEvent) => track(e.deltaY)
  document.addEventListener('wheel', handleWheel, { passive: true })
  return () => document.removeEventListener('wheel', handleWheel)
}, [])
```

**Use passive when:** tracking, analytics, logging, any listener that does not call `preventDefault()`.

**Do not use passive when:** implementing custom swipe gestures, custom zoom, or anything that must cancel the default scroll.

For scroll-linked visuals (progress bars, parallax, reveal-on-scroll) do not use a scroll listener at all: use CSS scroll-driven animations (`animation-timeline: scroll()` / `view()`) or `useScroll` + `useTransform` from `motion/react`, which run off the React render path.

---

## Rule 4.3: Use TanStack Query for Client-Interactive Server State

**Impact:** MEDIUM-HIGH  
**Tags:** client, tanstack-query, deduplication, data-fetching  

First ask whether the data belongs on the client at all. If a Server Component can read it, do that (no client cache, no loading state). Reach for TanStack Query when the client must own the request lifecycle: polling, infinite scroll, optimistic updates, or data that changes while the user interacts.

**Incorrect (no deduplication, each instance fetches, no cache):**

```tsx
function UserList() {
  const [users, setUsers] = useState<User[]>([])
  useEffect(() => {
    fetch('/api/users').then((r) => r.json()).then(setUsers)
  }, [])
}
```

**Correct (instances share one request and one cache entry):**

```tsx
'use client'
import { useQuery } from '@tanstack/react-query'

function UserList() {
  const { data: users, isPending } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then((r) => r.json() as Promise<User[]>),
    staleTime: 60_000, // do not refetch on every mount for a minute
  })
}
```

**Immutable data:** set `staleTime: Infinity` (and optionally `gcTime: Infinity`) instead of a special hook.

**Polling and infinite lists:** `refetchInterval` for polling; `useInfiniteQuery` with `getNextPageParam` for cursor pagination.

**Mutations:** prefer a Server Action with `useActionState` for form-style writes. Use `useMutation` when the write must update client cache optimistically or the UI is not a form:

```tsx
const queryClient = useQueryClient()
const update = useMutation({
  mutationFn: updateUser,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
})
```

**Setup:** one `QueryClient` per app, created in a Client Component provider mounted from the root layout. With Server Components, prefetch on the server with `queryClient.prefetchQuery` and pass the dehydrated state through `HydrationBoundary` so the first client render has data.

Reference: [https://tanstack.com/query/latest](https://tanstack.com/query/latest)

---

## Rule 4.4: Version and Minimize localStorage Data

**Impact:** MEDIUM  
**Tags:** client, localStorage, storage, versioning, data-minimization  

Prefix keys with a schema version and store only the fields the UI needs. This prevents schema conflicts after deploys and keeps tokens, PII, and internal flags out of storage.

**Incorrect:**

```typescript
localStorage.setItem('userConfig', JSON.stringify(fullUserObject))
const data = localStorage.getItem('userConfig')
```

**Correct:**

```typescript
const VERSION = 'v2'

function saveConfig(config: { theme: string; language: string }) {
  try {
    localStorage.setItem(`userConfig:${VERSION}`, JSON.stringify(config))
  } catch {
    // private mode, quota exceeded, or storage disabled
  }
}

function loadConfig() {
  try {
    const data = localStorage.getItem(`userConfig:${VERSION}`)
    return data ? JSON.parse(data) : null
  } catch {
    return null
  }
}

function migrateV1() {
  try {
    const v1 = localStorage.getItem('userConfig:v1')
    if (!v1) return
    const old = JSON.parse(v1)
    saveConfig({ theme: old.darkMode ? 'dark' : 'light', language: old.lang })
    localStorage.removeItem('userConfig:v1')
  } catch {}
}
```

**Always wrap in try/catch:** `getItem()` and `setItem()` throw in private browsing (Safari, Firefox), when the quota is exceeded, or when storage is disabled.

**Store minimal fields:** a user object with 20 fields becomes `{ theme, notifications }` in storage. Never persist access tokens in localStorage; use httpOnly cookies.
