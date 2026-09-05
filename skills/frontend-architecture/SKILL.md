---
name: frontend-architecture
description: Organizes frontend code by responsibility (UI, logic, data, types, validation) with the React 19 / Next.js 16 data-layer default - Server Components for reads, Server Actions with useActionState for mutations, TanStack Query only for client-interactive server state - plus feature/module layout, state tiers, service files, schema-validated forms, naming, props, and god-component splitting for React/Next and Vue. Use when structuring a frontend codebase, deciding where fetching, state, types, or validation should live, when to introduce an abstraction, or reviewing frontend code organization. Not for visual design (frontend-design), Tailwind mechanics (tailwind-patterns), or React performance (nextjs-react-expert).
version: 2.0.0
---

# Frontend Architecture

Separation of concerns over file-type folders, for React/Next and Vue. Directory layout: `app-builder` ([scaffolding.md](../app-builder/scaffolding.md)). Server/client boundaries and stack defaults: `frontend-design` §3. Tailwind hygiene and component extraction: `tailwind-patterns` §6. Performance: `nextjs-react-expert`. This file covers which layer code belongs to.

## 1. Separation of concerns

A unit of code does one of these:

| Layer | Holds | Lives in |
|---|---|---|
| UI | Rendering, markup, presentational state | `components/` |
| Logic | State, effects, transforms, reusable UI logic | `hooks/` (React), `composables/` (Vue) |
| Data | Server reads, actions, API calls, cache keys | Server Components, `actions/*.ts`, `lib/*.api.ts` |
| Type | TypeScript types, domain models | `types.ts` / `*.types.ts` |
| Validation | Form and data schemas | `*.schema.ts` (Zod by default; Valibot or ArkType when bundle size matters) |

**Colocate by feature; hoist to global on the second consumer.** The folders above are code *kinds*, not one flat bucket each. Past a few features, group by feature — `features/booking/{components,hooks,booking.api.ts,booking.schema.ts}` — and keep only genuinely shared code in top-level `components/ui`, `lib/`, `hooks/`. A file graduates to a shared folder when a second feature imports it, not in anticipation. Dependencies point one way: route files (`app/**`) compose features; features never import from `app/**`.

## 2. File responsibility, size, and when to abstract

One responsibility per file. Size is a signal, not a limit: a clear 230-line file beats a 90-line file that fetches, validates, renders, and juggles modals. Comfortable ranges: UI component 80-180 lines, page 100-220, hook/composable 40-150, service 50-200. Split when a file mixes UI + data + business logic + validation; do not split a coherent file to hit a number.

Abstract on the third use, not the first. Duplicate freely twice; extract a shared component, hook, or util when a third caller appears and the shape has stopped changing. Two call sites that merely look alike are not a pattern — the third confirms what actually varies, and that variance becomes the props. A premature abstraction couples callers to a shape you guessed wrong, and unwinding it later costs more than the duplication would have. Never grow a config-driven mega-component to serve two screens.

## 3. Components render; logic lives elsewhere

```tsx
// Component owns the data layer: avoid
function ProductList() {
  const [products, setProducts] = useState([])
  useEffect(() => { fetch('/api/products').then(r => r.json()).then(setProducts) }, [])
  return <ul>{/* render */}</ul>
}

// Component renders; a hook (or a Server Component, §4) owns the data
function ProductList() {
  const { data, isPending } = useProducts()
  if (isPending) return <ProductListSkeleton />
  return <ul>{/* render */}</ul>
}
```

Custom hooks start with `use`. A component calling an API directly is acceptable only for the smallest one-off cases. With the React Compiler on (the kit's templates enable it), write plain functions and skip manual `useMemo` / `useCallback` / `React.memo` by default; the flag check and memoization judgment live in `nextjs-react-expert`.

**Keep the `"use client"` boundary at the leaf.** The directive is transitive — every module imported below a client component becomes client code — so it is a structural seam, not a per-file flag. Mark the smallest interactive piece, and keep server content out of that subtree by passing it in through `children` or props rather than importing it. Getting this wrong ships server-only code to the browser; the bundle and rendering cost is `nextjs-react-expert`.

## 4. Data layer (default order)

1. **Reads: Server Components.** `page.tsx` / `layout.tsx` fetch directly (DB, API, cached `fetch`) and pass plain data down. No client fetching for data known at render time.
2. **Mutations: Server Actions + `useActionState`.** Submits call an action in `actions/*.ts` (`"use server"`) validated with the shared zod schema; the component reads `[state, formAction, isPending]` for inline errors and pending UI; `revalidatePath` / `revalidateTag` after the write. Server Actions are for mutations, not real-time data.
3. **Client-interactive server state: TanStack Query.** Only for polling, infinite lists, optimistic UI, or background refetching. Queries wrap service functions; mutations call Server Actions or the service. No SWR; no server state in Zustand or Redux.
4. **Real-time:** a subscription (WebSocket / SSE / provider SDK) feeding a query cache or local store, never polling through Server Actions.

```ts
// user.api.ts (service: the only place raw fetch/axios lives)
export async function getUsers(): Promise<User[]> {
  const res = await http.get('/users')
  return userSchema.array().parse(res.data)
}

// useUsers.ts (client-interactive only)
export function useUsers() {
  return useQuery({ queryKey: ['users'], queryFn: getUsers })
}
```

Every data-bound view handles loading, error, and empty explicitly. Vue/Nuxt: `useFetch` / `$fetch` for reads, TanStack Query for interactive state, same service-file rule.

## 5. State tiers (start local, escalate only when needed)

| Need | Use |
|---|---|
| Component-internal | `useState` / `ref` |
| Reusable state or logic in one feature | custom hook / composable |
| Shareable UI state (filters, tab, pagination, sort) | URL `searchParams` via `nuqs` or the router — not `useState`, so it survives reload, deep link, and Back |
| Shared client state in a subtree or across the app | Zustand or Jotai (React); Pinia (Vue) |
| Rarely-changing values (theme, session, locale) | React Context / `provide`-`inject` (Vue) — never for frequently updated state |
| Server state | §4, never a global store |
| Continuous input-driven values (scroll, pointer) | motion values (`frontend-design` §3.B) |

No global store on day one.

## 6. Forms validate against a schema

- React/Next: native `<form action={serverAction}>` + `useActionState` for simple forms; `react-hook-form` + `zod` (via `@hookform/resolvers`) for complex forms (multi-step, dynamic fields, heavy client validation), still submitting to a Server Action.
- Vue: `vee-validate` + zod/yup.
- Schemas live in `*.schema.ts` next to the form, shared with the server action. Errors render inline below the field (`frontend-design` §4.4).

## 7. Vue: Composition API + composables

Production apps use `<script setup>` SFCs (Options API is fine for small or legacy cases). `components/` → UI, `composables/` → reusable pure logic (`useX`), service files → API calls. A composable when reusing logic; a component when reusing logic and layout.

## 8. Naming and props

| Prefer | Avoid |
|---|---|
| `UserProfileCard.tsx` | `Card.tsx` |
| `useCreateBooking.ts` | `handle.ts` |
| `booking.api.ts`, `booking.actions.ts` | `api.ts`, `actions.ts` (bare) |
| `booking.schema.ts` | `data.ts` |

Type props explicitly; pass the object, not a scatter of primitives: `{ product: Product; onSelect?: (p: Product) => void }` instead of seven loose props.

## 9. Splitting a god component

Tells: over ~200 lines, more than ~3 `useEffect` / `watch`, many `useState` / `ref`, renders and fetches, many business branches, several modals/tables/forms in one file. Decompose along the page seams:

```
Page (Server Component)
 ├─ Header
 ├─ Filter            (client)
 ├─ Table / List
 ├─ Pagination
 └─ Modal / Form      (client, Server Action)
```

Keep client islands small: one interactive button does not make the whole page `"use client"`.

## 10. TypeScript

`strict: true`; no `any`; explicit types for props, API responses, and domain models; unions over enums when a union suffices; schemas for external data (types do not guard runtime input).

## 11. Minimum tests

Utilities and important hooks/composables → unit tests; main forms → validation tests; critical flows → e2e. Colocate or use `tests/unit` + `tests/e2e`, one convention per project. Details: `testing-patterns`.
