---
name: frontend-architecture
description: Where frontend code lives - feature folders, the UI / logic / data / type / validation split, the Next.js 16 data-layer default, state tiers, the "use client" boundary, when to extract or add a package, and splitting god components; for React/Next, Vue, Laravel Blade and plain HTML. Use when structuring a frontend codebase, deciding where fetching, state, types or validation go, or reviewing code organisation. Not for visual design (frontend-design), Tailwind (tailwind-patterns) or React performance (nextjs-react-expert).
version: 2.5.0
---

# Frontend Architecture

Which layer code belongs to and where it lives. The project's existing structure wins: extend it consistently rather than introducing a second convention. These are defaults for new code and for restructuring when asked.

| File | Read when |
|---|---|
| `structure-reference.md` | Scaffolding or restructuring: layer and state tables, feature tree, data-layer detail, forms, Vue, Laravel Blade, plain HTML, god-component seams, TypeScript, tests |

## Decisions

- **Feature folders once the app grows.** Code is UI, logic, data, type or validation (reference §1). A small app can stay flat; past a few features, group by feature — `features/booking/{components,hooks,booking.api.ts,booking.schema.ts}` — and keep only genuinely shared code in `components/ui`, `lib/`, `hooks/`.
- **Hoist on the second consumer.** A file moves to a shared folder when a second feature imports it. Dependencies point one way: route files (`app/**`) compose features; features do not import from `app/**`.
- **A package on the second app.** Move code to `packages/*` (Turborepo + pnpm; `app-builder` monorepo template) when a second deployable app consumes it. One app keeps a plain feature folder.
- **Abstract on the third use.** Duplicate twice; extract a shared component, hook or util when a third caller appears and the shape has settled. Avoid a config-driven mega-component built to serve two screens.
- **Data layer (Next.js App Router default).** Reads: Server Components. Mutations: Server Actions + `useActionState`. Client-interactive server state (polling, infinite lists, optimistic UI): TanStack Query. Real-time: a subscription. Keep server state out of global client stores. A project already on SWR, Redux Toolkit Query or Inertia keeps its tool. Detail: reference §4.
- **State starts local.** `useState` / `ref` → custom hook / composable → URL `searchParams` for shareable UI state → Zustand or Jotai (Pinia in Vue) for shared client state → Context for rarely-changing values. Tier table: reference §3.
- **`"use client"` at the leaf.** The directive is transitive — everything a client module imports becomes client code — so mark the smallest interactive piece and pass server content through `children` or props. **Firm:** never import server-only code (DB clients, secrets, `server-only` modules) into a client module; use `import 'server-only'` in files that must stay on the server.
- **Components render; logic lives elsewhere** once it grows past a few lines: custom hooks (`use*`), service files (`*.api.ts`) for raw `fetch` / axios, actions for mutations. A one-off component calling an API directly is fine in a small app. Memoisation: the memo rule in `nextjs-react-expert`.
- **Names say what it is.** Prefer `UserProfileCard.tsx`, `useCreateBooking.ts`, `booking.api.ts` over `Card.tsx`, `handle.ts`, `api.ts` in new code (reference §7); follow the project's existing naming. Type props explicitly; pass the domain object rather than a scatter of primitives.

## Procedure

1. List the features the task touches; place each new file by kind inside its feature (or the project's equivalent).
2. Reads in the Server Component; mutations in a `"use server"` action with a `*.schema.ts` next to the form; TanStack Query only for the client-interactive cases. (Laravel, Vue, plain HTML: reference §5-§6, §11-§12.)
3. Mark the smallest interactive leaf `"use client"`; pass server content through `children` / props.
4. Pick the lowest state tier that works; shareable UI state goes to the URL.
5. Split a god component along its page seams (reference §8).
6. Verify per the `code-rules` tier; add the tests reference §9 suggests where logic warrants them.

## Exemplar

```tsx
// Component owns the data layer: harder to test and reuse
function ProductList() {
  const [products, setProducts] = useState([])
  useEffect(() => { fetch('/api/products').then(r => r.json()).then(setProducts) }, [])
  return <ul>{/* render */}</ul>
}

// Component renders; a Server Component (or a hook, for client-interactive data) owns the data
export default async function ProductsPage() {
  const products = await getProducts()        // products.api.ts or a DB query
  return <ProductList products={products} />
}
```

## What good looks like

- Data-bound views handle loading, error and empty states.
- `"use client"` sits on leaves; routes compose features; no server-only code in client bundles.
- Forms validate against a schema shared with the server action or controller, and errors render next to the field.
- TypeScript `strict: true`; `any` only with a reason; schemas for external data (reference §10).
- A new developer can find a feature's code in one folder.
