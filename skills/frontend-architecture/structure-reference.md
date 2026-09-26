# Structure reference

Read when: scaffolding a new app or restructuring folders; core first.

## 1. Layers and where they live

A unit of code does one of these:

| Layer | Holds | Lives in |
|---|---|---|
| UI | Rendering, markup, presentational state | `components/` |
| Logic | State, effects, transforms, reusable UI logic | `hooks/` (React), `composables/` (Vue) |
| Data | Server reads, actions, API calls, cache keys | Server Components, `actions/*.ts`, `lib/*.api.ts` |
| Type | TypeScript types, domain models | `types.ts` / `*.types.ts` |
| Validation | Form and data schemas | `*.schema.ts` (Zod by default; Valibot or ArkType when bundle size matters) |

The folders above are code *kinds*, not one flat bucket each. A grown app groups them by feature:

```
src/
├─ app/                      # routes only; composes features, never imported by them
├─ features/
│  └─ booking/
│     ├─ components/
│     ├─ hooks/
│     ├─ booking.api.ts      # service file (fetch/axios)
│     ├─ booking.actions.ts  # Server Actions ("use server")
│     └─ booking.schema.ts   # zod schema shared by form and action
├─ components/ui/            # shared primitives (second consumer or later)
├─ hooks/                    # shared hooks (second consumer or later)
└─ lib/                      # shared utilities and service files
```

Full Next.js tree, path aliases and core files: `KIT/skills/app-builder/scaffolding.md`. Multi-app repos (`apps/` deployable, `packages/` shared, `@repo/*` via `workspace:*`): `KIT/skills/app-builder/templates/monorepo-turborepo/TEMPLATE.md`.

## 2. File responsibility and size

One responsibility per file. Size is a signal, not a limit: a clear 230-line file beats a 90-line file that fetches, validates, renders, and juggles modals. Comfortable ranges: UI component 80-180 lines, page 100-220, hook/composable 40-150, service 50-200. Split when a file mixes UI + data + business logic + validation; do not split a coherent file to hit a number.

Two call sites that merely look alike are not a pattern. A premature abstraction couples callers to a shape you guessed wrong, and unwinding it later costs more than the duplication would have.

## 3. State tiers

| Need | Use |
|---|---|
| Component-internal | `useState` / `ref` |
| Reusable state or logic in one feature | custom hook / composable |
| Shareable UI state (filters, tab, pagination, sort) | URL `searchParams` via `nuqs` or the router — not `useState`, so it survives reload, deep link, and Back |
| Shared client state in a subtree or across the app | Zustand or Jotai (React); Pinia (Vue) |
| Rarely-changing values (theme, session, locale) | React Context / `provide`-`inject` (Vue) — never for frequently updated state |
| Server state | §4, never a global store |
| Continuous input-driven values (scroll, pointer) | refs or `motion/react` motion values (`nextjs-react-expert` Rule 5.10) |

## 4. Data layer (default order)

1. **Reads: Server Components.** `page.tsx` / `layout.tsx` fetch directly (DB, API, cached `fetch`) and pass plain data down. No client fetching for data known at render time.
2. **Mutations: Server Actions + `useActionState`.** Submits call an action in `*.actions.ts` (`"use server"`) that validates with the shared Zod schema and checks auth inside the action; the component reads `[state, formAction, isPending]` for inline errors and pending UI; `updateTag` / `revalidatePath` after the write (`nextjs-react-expert` section 9). Server Actions are for mutations, not real-time data.
3. **Client-interactive server state: TanStack Query.** For polling, infinite lists, optimistic UI or background refetching. Queries wrap service functions; mutations call Server Actions or the service. Keep server state out of Zustand or Redux; a project already on SWR keeps it.
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

Vue/Nuxt: `useFetch` / `$fetch` for reads, TanStack Query for interactive state, same service-file rule.

## 5. Forms validate against a schema

- React/Next: native `<form action={serverAction}>` + `useActionState` for simple forms; `react-hook-form` + `zod` (via `@hookform/resolvers`) for complex forms (multi-step, dynamic fields, heavy client validation), still submitting to a Server Action.
- Vue: `vee-validate` + zod/yup.
- Schemas live in `*.schema.ts` next to the form, shared with the server action. Errors render inline next to the field (form states: `frontend-design`).
- Laravel: a Form Request holds the rules; Blade shows `@error('field')` next to the input and keeps `old('field')` values.

## 6. Vue: Composition API + composables

Production apps use `<script setup>` SFCs (Options API is fine for small or legacy cases). `components/` → UI, `composables/` → reusable pure logic (`useX`), service files → API calls. A composable when reusing logic; a component when reusing logic and layout.

## 7. Naming and props

| Prefer | Avoid |
|---|---|
| `UserProfileCard.tsx` | `Card.tsx` |
| `useCreateBooking.ts` | `handle.ts` |
| `booking.api.ts`, `booking.actions.ts` | `api.ts`, `actions.ts` (bare) |
| `booking.schema.ts` | `data.ts` |

Type props explicitly; pass the object, not a scatter of primitives: `{ product: Product; onSelect?: (p: Product) => void }` instead of seven loose props.

## 8. Splitting a god component

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

## 9. Minimum tests

Utilities and important hooks/composables → unit tests; main forms → validation tests; critical flows → e2e. Colocate or use `tests/unit` + `tests/e2e`, one convention per project. Details: `testing-patterns`.

## 10. TypeScript

`strict: true`; avoid `any` (use `unknown` and narrow, or a schema); explicit types for props, API responses and domain models; unions over enums (Node's type stripping and `erasableSyntaxOnly` reject enums); schemas for external data, because types do not guard runtime input. TypeScript 5.9+ baseline.

## 11. Laravel Blade (with Livewire or Alpine)

```
app/
├─ Http/Controllers/OrderController.php     # thin: validate (Form Request), authorise (Policy), call an action
├─ Http/Requests/StoreOrderRequest.php
├─ Actions/Orders/CreateOrder.php           # business logic, one use case per class
├─ Livewire/Orders/OrderTable.php           # interactive pieces only (if Livewire is used)
resources/views/
├─ layouts/app.blade.php
├─ components/                              # Blade components: <x-order-status-badge>
└─ orders/index.blade.php, create.blade.php
resources/css/app.css, resources/js/app.js  # Vite entry points
```

Blade components for repeated markup; Livewire or Alpine for the interactive islands; Inertia (Vue or React) when the app is mostly client-side screens. Keep queries out of views: pass prepared data from the controller, and eager-load relations there (`database-design`).

## 12. Plain HTML, CSS and JavaScript sites

```
index.html, about.html, ...
assets/css/tokens.css      # custom properties from DESIGN.md
assets/css/base.css, layout.css, components/*.css
assets/js/main.js          # small ES modules, one per feature: nav.js, precinct-finder.js
assets/img/, assets/data/*.json
```

One ES module per behaviour, loaded with `<script type="module">`; data in JSON files rather than inside scripts; progressive enhancement so content works before JavaScript loads. Reach for a build tool or framework when pages share a lot of repeated markup or the site needs templating.
