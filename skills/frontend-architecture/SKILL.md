---
name: frontend-architecture
description: Organizes frontend code by responsibility (UI, logic, data, types, validation) for React/Next and Vue - feature folders, the React 19 / Next.js 16 data-layer default (Server Components for reads, Server Actions for mutations, TanStack Query only for client-interactive state), state tiers, the "use client" boundary, when to add a package, naming, and god-component splitting. Use when structuring a frontend codebase, deciding where fetching, state, types, or validation live, or reviewing code organization. Not for visual design (frontend-design), Tailwind mechanics (tailwind-patterns), or React performance (nextjs-react-expert).
version: 2.1.0
---

# Frontend Architecture

Separation of concerns over file-type folders, for React/Next and Vue: which layer code belongs to and where it lives. Server/client boundaries and stack defaults: `frontend-design` §3. Tailwind hygiene and component extraction: `tailwind-patterns` §6. Performance: `nextjs-react-expert`.

| File | Read when |
|---|---|
| [structure-reference.md](./structure-reference.md) | Scaffolding a new app or restructuring folders: layer / state / naming tables, feature tree, size ranges, data-layer detail, forms, Vue, god-component tells, TypeScript, tests |

## 1. Decisions

- **Feature folders, not one bucket per file type.** Code is UI, logic, data, type, or validation (reference §1). Past a few features, group by feature — `features/booking/{components,hooks,booking.api.ts,booking.schema.ts}` — and keep only genuinely shared code in top-level `components/ui`, `lib/`, `hooks/`.
- **Hoist on the second consumer.** A file graduates to a shared folder when a second feature imports it, not in anticipation. Dependencies point one way: route files (`app/**`) compose features; features never import from `app/**`.
- **A package on the second app.** Move code to `packages/*` (Turborepo + pnpm; `app-builder` `monorepo-turborepo` template) when a second deployable app consumes it. One app keeps a plain feature folder; no monorepo on day one.
- **Abstract on the third use.** Duplicate freely twice; extract a shared component, hook, or util when a third caller appears and the shape has stopped changing — the third confirms what actually varies, and that variance becomes the props. Never grow a config-driven mega-component to serve two screens.
- **Data layer, in this order.** Reads: Server Components. Mutations: Server Actions + `useActionState`. Client-interactive server state only: TanStack Query. Real-time: a subscription. No SWR; no server state in a global store. Detail: reference §4.
- **State starts local and escalates only when needed.** `useState` / `ref` → custom hook / composable → URL `searchParams` for shareable UI state → Zustand or Jotai (Pinia in Vue) for shared client state → Context only for rarely-changing values. No global store on day one. Tier table: reference §3.
- **`"use client"` stays at the leaf.** The directive is transitive — every module imported below a client component becomes client code — so it is a structural seam, not a per-file flag. Mark the smallest interactive piece; pass server content in through `children` or props rather than importing it. Getting this wrong ships server-only code to the browser (cost: `nextjs-react-expert`).
- **Components render; logic lives elsewhere.** Custom hooks start with `use`; service files (`*.api.ts`) are the only place raw `fetch` / axios lives; a component calling an API directly is acceptable only for the smallest one-off cases. Compiler-first when the React Compiler is enabled; the memo rule is in `nextjs-react-expert`.
- **Names say what, not which kind.** `UserProfileCard.tsx`, `useCreateBooking.ts`, `booking.api.ts`; never bare `Card.tsx`, `handle.ts`, `api.ts` (reference §7). Type props explicitly; pass the object, not a scatter of primitives.

## 2. Procedure

1. List the features the task touches; place each new file by kind inside its feature folder (reference §1-§2).
2. Reads in the Server Component; mutations in a `"use server"` action with a `*.schema.ts` next to the form; TanStack Query only for the client-interactive cases.
3. Mark the smallest interactive leaf `"use client"`; pass server content through `children` / props.
4. Pick the lowest state tier that works; shareable UI state goes to the URL.
5. Split any god component along the page seams (tells and seam tree: reference §8); keep client islands small.
6. Add the minimum tests (reference §9); run the gates.

## 3. Exemplar

```tsx
// Component owns the data layer: avoid
function ProductList() {
  const [products, setProducts] = useState([])
  useEffect(() => { fetch('/api/products').then(r => r.json()).then(setProducts) }, [])
  return <ul>{/* render */}</ul>
}

// Component renders; a hook (or a Server Component, reference §4) owns the data
function ProductList() {
  const { data, isPending } = useProducts()
  if (isPending) return <ProductListSkeleton />
  return <ul>{/* render */}</ul>
}
```

## 4. Done

- [ ] Every data-bound view handles loading, error, and empty explicitly.
- [ ] `"use client"` sits on leaves; `app/**` composes features; no feature imports from `app/**`.
- [ ] Forms validate against a `*.schema.ts` shared with the server action; errors render inline.
- [ ] `strict: true`; no `any`; explicit types (reference §10); schemas for external data.
- [ ] One responsibility per file (reference §2).
