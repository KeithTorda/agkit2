---
part: 31
title: React, Next and Vue
covers: useEffect abuse, useState for derived data, state shape, data fetching in effects, loading and error states, caching, prop drilling, context overuse, premature primitives, component explosion, giant components, keys, memoisation, refs, forms in React, "use client" everywhere, Next.js App Router tells, next/image and metadata, env leaks, shadcn/ui defaults, component library defaults, styling in components, Vue and Nuxt tells, Svelte notes, folder structure
---

# 31 — React, Next and Vue

Read when: writing or reviewing components, hooks, pages or routes in React, Next.js, Vue, Nuxt or Svelte. General JS and TS tells (any, console.log, silent catch, timers) are in part 30. Folder and file naming rules are in part 33. Form UX is in part 17. Loading and error UI copy is in parts 03, 04 and 21.

## 31.1 useEffect abuse

Effects are for syncing with something outside React: network, subscriptions, timers, DOM APIs, third-party widgets. Most generated effects are not that.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Effect that sets state from props or other state: `useEffect(() => setFullName(first + " " + last), [first, last])` | Extra render, stale frame, one more state to keep in sync | Compute during render: `const fullName = first + " " + last`. |
| Effect that filters or sorts a list into state | Same as above for lists | `const visible = items.filter(...)`. Wrap in `useMemo` only if the list is large and the render is measured slow. |
| Effect that reacts to a button click by watching a flag: `setSubmitted(true)` then `useEffect(() => { if (submitted) save() }, [submitted])` | Event logic moved into an effect | Call `save()` in the click handler. |
| Effect to reset state when a prop changes | Flicker and double render | Pass a `key` to the component so React remounts it: `<Editor key={residentId} />`. |
| Effect to notify the parent: `useEffect(() => onChange(value), [value])` | Fires on mount and on every change, loops easily | Call `onChange` in the same handler that sets the value. |
| Chains of effects, each setting state that triggers the next | Cascading renders, hard to trace | One event handler that computes the next state, or a reducer. |
| Effect with an empty dependency array that reads props or state | Stale values, lint rule disabled to hide it | Include dependencies. If it must run once, move the logic out of React or into an event. |
| `// eslint-disable-next-line react-hooks/exhaustive-deps` | Hides a real bug | Fix the dependencies. Move functions inside the effect or stabilise them. |
| Effect for data fetching with no cleanup, no abort, no race handling | Out-of-order responses overwrite newer data | Use a data library (TanStack Query, SWR) or server components. If raw, abort in cleanup. See 31.3. |
| Effect that runs `document.title = ...` in Next.js | Framework has metadata | `export const metadata` or `generateMetadata`. |
| Effect to read `localStorage` then set state, causing a flash | Hydration flicker | Lazy initial state: `useState(() => readSaved())` in client-only components, or `useSyncExternalStore`. |
| Effect that adds a listener without removing it | Duplicate handlers after remount, and twice in Strict Mode | Return a cleanup that removes it. |
| Timers in effects without `clearTimeout`/`clearInterval` | Runs after unmount | Return cleanup. |
| Effects on every render (no dependency array) | Runs constantly | Add the array. Usually the logic belongs in render or an event instead. |
| Turning off Strict Mode because effects run twice in dev | Hides missing cleanup | Keep Strict Mode. Fix the effect. |

```tsx
// Banned
const [total, setTotal] = useState(0);
useEffect(() => {
  setTotal(items.reduce((s, i) => s + i.priceCentavos * i.qty, 0));
}, [items]);

// Use
const totalCentavos = items.reduce((s, i) => s + i.priceCentavos * i.qty, 0);
```

## 31.2 State

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `useState` for everything, including values derived from other state | Many states to keep in sync, bugs when one is missed | Keep the minimum state. Derive the rest during render. |
| Boolean soup: `isLoading`, `isError`, `isSuccess`, `isEmpty`, `isFetching` as separate states | Impossible combinations (loading and error both true) | One status: `type Status = "idle" | "loading" | "error" | "success"`, or use the data library's state. |
| Copying props into state: `const [name, setName] = useState(props.name)` | State stops following the prop | Use the prop. If it is an initial value for an editable field, name it `initialName` and document that updates are ignored, or reset with `key`. |
| Five related `useState` calls updated together | Updates can split | One object state or `useReducer`. |
| `useReducer` with 20 action types for a 3-field form | Redux habit | `useState` or a form library. |
| Redux or Zustand store for state used by one component | Global state for local data | Local state. Lift to the nearest shared parent. Global store only for state used across distant parts (cart, session, POS shift). |
| Server data copied into a global store | Two caches drift | Keep server data in the query cache (TanStack Query, SWR, server components). Store only client state. |
| Filters, tabs, page number and search in `useState` on list pages | Refresh loses them. Links cannot be shared. Back button breaks. | Put them in the URL: `useSearchParams` (Next), `route.query` (Vue Router). |
| `setCount(count + 1)` in async code or repeated calls | Stale closure drops updates | Functional update: `setCount(c => c + 1)`. |
| Mutating state: `items.push(x); setItems(items)` | No re-render or wrong render | New array: `setItems([...items, x])`. |
| Storing JSX or components in state | Hard to serialise, stale props | Store data. Render JSX from data. |
| `useRef` used as state to "avoid re-renders" for values the UI shows | UI does not update | State for anything rendered. Refs for values the render does not read (timer IDs, previous values, DOM nodes). |

## 31.3 Data fetching, loading and error states

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `fetch` in `useEffect` with `useState` for data, loading and error, copied into every component | Duplicated code, no caching, no dedupe, race bugs | TanStack Query or SWR on the client. Server components or loaders (Next, Remix, Nuxt `useFetch`) where the framework supports them. |
| Fetch on every render or every mount of a tab | Same request repeated, slow on PH mobile data | Cache with a stale time (for example 30–60s for lists). Fetch once and reuse. |
| No loading state: blank screen, then content pops in | Looks broken on slow 3G | Show a loading state. Skeleton only if the wait is often over 500ms. See part 21. |
| No error state: data is `undefined`, page renders empty | Failure looks like "no data" | Render an error with a retry action. Use error boundaries (`error.tsx` in Next) for unexpected errors. |
| No empty state distinct from loading | "No results" flashes before data loads | Three branches: loading, error, empty, then data. |
| Loading spinner that replaces the whole page on refetch | Content disappears when filters change | Keep previous data during refetch (`placeholderData: keepPreviousData`). Show a small inline indicator. |
| Waterfalls: parent fetches, then child fetches after mount, then grandchild | Serial round trips | Fetch in parallel at the route level, or with `Promise.all` in a server component. |
| Fetching in a client component in Next.js App Router when the data is not user-interactive | Extra JS, extra round trip, loading spinners | Fetch in a server component. Pass data down. |
| Next.js server component calling its own `/api/...` route with `fetch` | Round trip to itself | Call the data function directly. |
| Mutations with no pending state; double-click submits twice | Duplicate orders, duplicate payments | Disable the button while pending, show "Saving…". Use an idempotency key on the server for payments. See part 18 and part 32. |
| Optimistic updates without rollback | UI shows paid when payment failed | Roll back on error and show the error, or do not use optimistic updates for money. |
| Query keys as ad-hoc strings: `["users"]`, `["user-list"]`, `["Users"]` | Invalidation misses | Query key factory: `residentKeys.list(filters)`, `residentKeys.detail(id)`. |
| `invalidateQueries()` with no key after every mutation | Refetches the whole app | Invalidate the affected keys. |
| Axios instance plus fetch wrapper plus a custom `useApi` hook in one app | Three clients | One client. |

```tsx
// Banned
function Residents() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetch("/api/residents").then(r => r.json()).then(d => { setData(d); setLoading(false); });
  }, []);
  if (loading) return <p>Loading...</p>;
  return data.map((r: any) => <Row r={r} />);
}

// Use
function Residents() {
  const { data, status, refetch } = useQuery({
    queryKey: residentKeys.list(),
    queryFn: fetchResidents,
    staleTime: 60_000,
  });
  if (status === "pending") return <TableSkeleton rows={10} />;
  if (status === "error") return <ErrorState message="Could not load residents." onRetry={refetch} />;
  if (data.length === 0) return <EmptyState text="No residents yet." action={<Link href="/residents/new">Add resident</Link>} />;
  return <ResidentTable rows={data} />;
}
```

## 31.4 Component size and splitting

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Over-componentizing on day 1: `Header`, `HeaderLeft`, `HeaderRight`, `HeaderLogo`, `HeaderLogoImage` for 20 lines of JSX | Folder of 5-line files | Keep it in one component. Extract when a piece repeats 3 times, has its own state, or the file passes about 200–300 lines. |
| One 900-line page component with fetching, forms, tables and modals | Everything in one place, impossible to review | Split by responsibility: data loading, table, filter bar, dialog. Each file under about 300 lines. |
| Premature primitives: `<Box>`, `<Text>`, `<Flex>`, `<Stack>`, `<Heading>` wrappers around `div` and `p` in an app with no design system package | Rebuilt a UI library badly | Use HTML elements with classes. Use a primitive layer only when it comes from the chosen library (Chakra, Mantine) or a real design system. |
| `Button`, `PrimaryButton`, `SecondaryButton`, `DangerButton`, `IconButton`, `SubmitButton` as six components | Variant as a component | One `Button` with a `variant` prop. |
| Props with 15 booleans: `isLarge`, `isSmall`, `isRounded`, `isOutlined`, `isGhost`, `hasIcon` | Conflicting combinations | Enumerated props: `size="sm" | "md"`, `variant="primary" | "secondary" | "ghost"`. |
| Wrapper components that pass through every prop and add nothing | Extra layer in DevTools and imports | Use the underlying component. |
| `{...props}` spread onto DOM elements from untyped objects | Invalid attributes, leaks internal props, React warnings | Destructure known props. Spread only a typed `rest` of native attributes. |
| `renderHeader`, `renderBody`, `renderFooter` functions inside one component | Hidden components with no memo boundary or name | Separate components, or inline JSX if short. |
| Components defined inside other components | Remounts on every render, loses state and focus | Define components at module level. |
| HOCs (`withAuth(withTheme(withData(Page)))`) in new code | Pre-hooks pattern | Hooks and layout components. Auth in middleware or the route layout. |
| Custom hook for one line: `useToggle` that wraps `useState(!x)` used once | Hook for show | Inline. Extract hooks when logic with state or effects repeats. |

## 31.5 Props, context and state sharing

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Prop drilling through 4+ layers where middle layers do not use the prop | Every change touches 5 files | Composition: pass `children` or elements. Or context at the nearest shared parent. |
| Context for everything: `ThemeContext`, `UserContext`, `SidebarContext`, `ModalContext`, `ToastContext`, `FormContext` wrapping the whole app | Provider pyramid, every update re-renders consumers | Context for values read in many places that change rarely (session, theme, locale). Local state or URL for the rest. |
| One giant `AppContext` holding user, cart, filters, modals | Any change re-renders the whole tree | Split contexts by update frequency, or use a store with selectors (Zustand). |
| Context value built inline: `<Ctx.Provider value={{ user, setUser }}>` in a parent that re-renders often | New object each render, all consumers re-render | `useMemo` the value, or split state and setter contexts. |
| Context with no default and no guard hook | Undefined errors outside provider | `useSession()` hook that throws a clear error when the provider is missing. |
| Passing setters down instead of events: `setItems` given to a child | Child knows parent's state shape | Pass intent callbacks: `onAddItem(item)`. |

## 31.6 Lists and keys

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `key={index}` on lists that reorder, filter or accept inserts | Inputs keep wrong values, animations jump | Stable IDs from data: `key={resident.id}`. Index is fine only for static lists that never change order. |
| `key={Math.random()}` or `key={crypto.randomUUID()}` in render | Remounts every item every render | Stable IDs. Generate IDs when data is created, not when rendered. |
| Missing keys, warning ignored | Console noise and reconciliation bugs | Add keys. |
| Keys from content that can repeat: `key={name}` | "Juan Dela Cruz" appears twice in a barangay list | Use the record ID. |
| Rendering 5,000 rows at once | Slow on low-end phones and POS tablets | Paginate on the server, or virtualise (TanStack Virtual) for long scrolling lists. See part 19. |

## 31.7 Memoisation and performance

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `useMemo` around every computed value, including `a + b` | Adds cost and noise with no measured gain | Compute in render. Memo when a profiler shows a slow computation or a memoised child needs a stable reference. |
| `useCallback` on every handler | Same | Only when passing to a memoised child or a dependency array that needs stability. |
| `React.memo` on every component | Comparison cost on components that always get new props | Memo components that are expensive and receive stable props. Measure with React DevTools Profiler. |
| Memo added while props are new objects each render | Memo never hits | Fix the prop identity first, or remove the memo. |
| React Compiler enabled and manual `useMemo`/`useCallback` still everywhere | Double work | With the compiler on, remove manual memo unless profiling shows a need. |
| Heavy libraries imported in client components for one feature (full chart library for one sparkline, moment, lodash) | Bundle size on mobile | Lazy load with `dynamic()` or `React.lazy`, or use a lighter option. See part 34. |
| `import * as Icons from "lucide-react"` | Pulls every icon | Import named icons. |
| Context providers wrapping the whole app that change on every keystroke | Global re-render | Keep fast-changing state local. |

## 31.8 Refs, DOM and HTML injection

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `document.getElementById` or `querySelector` inside components | Bypasses React, breaks with multiple instances | `useRef`. |
| `dangerouslySetInnerHTML` with user or CMS content, unsanitised | XSS | Render as text. If HTML is needed (CMS article), sanitise with DOMPurify on the server or at render. |
| `dangerouslySetInnerHTML` for plain text with `<br>` | Unneeded risk | CSS `white-space: pre-line` or split lines into elements. |
| `useLayoutEffect` used everywhere | Blocks paint, warns on server | `useEffect`, unless measuring layout before paint. |
| `forwardRef` wrappers in React 19 projects | Old API | In React 19, `ref` is a regular prop for function components. |
| Manual focus management missing after dialogs close | Keyboard users lose place | Return focus to the trigger. Native `<dialog>` or Radix handles this. See part 27. |

## 31.9 Forms in React and Vue

UX rules are in part 17. Code tells:

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| One `useState` per field and a hand-written `handleChange` per field | 40 lines of boilerplate for a 6-field form | Form library (React Hook Form with a Zod resolver, TanStack Form, VeeValidate for Vue) or uncontrolled inputs with `FormData`. |
| Validation rules written twice, once on client and once on server, and they differ | Client accepts what server rejects | One schema shared between client and server where the stack allows (Zod in a shared package). |
| `e.preventDefault()` then manual serialise of every field | Rebuilt `FormData` | `new FormData(e.currentTarget)` or a server action with `<form action={...}>` in Next. |
| Controlled inputs with `value` but no `onChange` | Read-only input warning, frozen field | Add `onChange`, or use `defaultValue` for uncontrolled. |
| `value={x || ""}` to silence controlled/uncontrolled warnings | Hides `undefined` bugs | Initialise state with real defaults. |
| Submit handler with no pending guard | Double submit | `useActionState`, `useFormStatus`, or `isSubmitting` from the form library. Disable while pending. |
| Server errors not mapped to fields | "Something went wrong" for a duplicate email | Return field errors from the server and set them on the form. |
| Peso amount inputs as `type="number"` bound to floats | Spinners, scroll changes value, float drift | `type="text" inputMode="decimal"`, parse to centavos on submit. See part 30. |

## 31.10 Next.js App Router

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `"use client"` at the top of every file, including layouts and pages | Throws away server components and ships more JS | Server components by default. Add `"use client"` only to leaf components that need state, effects, event handlers or browser APIs. |
| `"use client"` on a page to use one `onClick` | Whole page tree becomes client | Extract the interactive part into a small client component. |
| Pages Router APIs in App Router: `getServerSideProps`, `getStaticProps`, `next/router`, `_app.tsx` | Mixed training data | `async` server components, `generateStaticParams`, `next/navigation`, `layout.tsx`. |
| `export const dynamic = "force-dynamic"` on every route | Disables caching everywhere to make a stale bug go away | Set caching per fetch (`revalidate`, `cache: "no-store"` where data is per-user). Use `revalidatePath`/`revalidateTag` after mutations. |
| API route (`route.ts`) created for every mutation used only by the app's own forms | Extra layer | Server actions for form mutations. Route handlers for webhooks (GCash, Maya, PayMongo), third-party clients and public APIs. |
| Server actions with no auth check and no input validation | Server actions are public endpoints | Check the session and validate input with a schema in every action. |
| Secrets in `NEXT_PUBLIC_*` env vars | Shipped to every browser | Only public values get `NEXT_PUBLIC_`. Secret keys stay server-only. Import `server-only` in modules that read secrets. |
| `<img>` tags for local images with no size | Layout shift | `next/image` with `width`/`height` or `fill` plus `sizes`. See part 26. |
| `next/image` with `unoptimized` on everything, or `priority` on every image | Default copied to silence errors | Optimise by default. `priority` only on the LCP image. |
| `<a href>` for internal links | Full page reloads | `next/link`. |
| `document.title` or `<Head>` in App Router | Old API | `metadata` export or `generateMetadata`. Copy rules for titles in part 08. |
| `loading.tsx` with a full-page spinner for every segment | Spinners flash on fast navigation | `loading.tsx` with a skeleton matching the layout, only where data is slow. |
| No `error.tsx` or `not-found.tsx` | Default Next error screens shipped | Add both with plain copy. See part 04. |
| Middleware doing heavy database calls on every request | Slow every page | Middleware checks a session cookie or token only. Data checks happen in the route. |
| `app/page.tsx` still showing the create-next-app template, `public/next.svg`, `public/vercel.svg` | Starter leftovers | Delete. See part 33. |

## 31.11 shadcn/ui and component library defaults

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| shadcn/ui installed with default `slate` or `zinc` theme and default `--radius: 0.5rem`, no token changes | Every shadcn app looks the same | Map DESIGN.md tokens into the CSS variables (`--primary`, `--radius`, `--border`) before building screens. |
| Every shadcn component added "for later" (`npx shadcn add --all`) | Dead components in `components/ui` | Add components when used. Delete unused ones. |
| Default shadcn `Card` wrapping every section | Card-everything look | Use Card for real grouped objects. See part 14. |
| shadcn dashboard example copied as the admin panel, with its demo charts and "Recent Sales" | Recognisable demo | Build from the client's actual screens. See part 22. |
| Editing files in `components/ui` heavily, then running `shadcn add` again and losing edits | Owned code treated as a package | Treat `components/ui` as your code. Record changes in commits. Do not re-add over edited files. |
| MUI default theme (Roboto, default blue `#1976d2`, elevation shadows) untouched | Instant "MUI demo" look | `createTheme` with DESIGN.md palette, typography and `shape.borderRadius`. Reduce default elevation. |
| Ant Design, Chakra, Mantine defaults untouched | Same issue | Set theme tokens first. |
| Two component libraries in one app (shadcn plus MUI plus Headless UI) | Mixed look and double bundle | One library. |
| Aceternity, Magic UI, animated components pasted into an admin app | Visual tropes. See part 10. | Remove. Use static components. |
| `lucide-react` icons next to Heroicons next to react-icons | Mixed sets | One icon set. See part 26. |

## 31.12 Styling in components

CSS structure rules are in part 29.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Class strings built with template literals and ternaries: `` className={`btn ${active ? "btn-active" : ""} ${size === "lg" ? "btn-lg" : ""}`} `` | Hard to read, trailing spaces | `clsx` or `cn()` helper. |
| `cn()` wrapping a static string with no conditions | Habit | Plain `className="..."`. |
| `style={{ marginTop: 20, color: "#6366f1" }}` inline objects | Bypasses tokens and breakpoints | Classes. Inline style only for runtime values via custom properties: `style={{ "--progress": `${pct}%` }}`. |
| Tailwind class lists of 30+ utilities repeated in several components | Copy-paste styling | Extract a component that owns the class list. |
| Variant logic duplicated in every component | Drift | `cva` or a small variants map for components with real variants. |
| Global CSS imported in random components in Next | Load order bugs | Global CSS in the root layout only. CSS Modules or Tailwind for components. |

## 31.13 Vue and Nuxt

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Options API and Composition API mixed in one project | Two styles | `<script setup lang="ts">` for new code. |
| `watch` used to derive values | Same as effect abuse | `computed`. |
| `watch` with `deep: true` on large objects | Slow, fires often | Watch the specific property. |
| Mutating props: `props.items.push(x)` | Breaks one-way data flow | Emit an event: `emit("add", x)`. Or `defineModel` for two-way binding. |
| `v-if` and `v-for` on the same element | Precedence confusion | Filter with a `computed`, or wrap in `<template v-for>`. |
| `:key="index"` in `v-for` over changing lists | Same bug as React | Stable IDs. |
| `v-html` with user content | XSS | Text interpolation, or sanitise. |
| Pinia store for every component's state | Global state for local data | Local `ref`/`reactive`. Pinia for shared app state. |
| `ref` wrapping objects then `.value` errors everywhere | Mixed `ref` and `reactive` habits | Pick one pattern per project. `ref` for primitives and replaced objects. |
| Nuxt: `onMounted` + `$fetch` for page data | Loses SSR, double fetch | `useFetch` or `useAsyncData` at the page level. |
| Nuxt: `runtimeConfig.public` holding secrets | Shipped to the client | Secrets in private `runtimeConfig` only. |
| `this.$refs` DOM queries for things a binding can do | Imperative habits | Template bindings. |

## 31.14 Svelte and others

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Svelte 4 syntax (`export let`, `$:`) in a Svelte 5 project | Version mix | Runes: `$props()`, `$state()`, `$derived()`, `$effect()`. Check `package.json`. |
| `$effect` used to derive values | Effect abuse again | `$derived`. |
| SvelteKit `onMount` fetch for page data | Loses SSR | `load` functions in `+page.ts` or `+page.server.ts`. |
| Alpine.js `x-data` objects with 200 lines inline in HTML | Logic hidden in attributes | Move to `Alpine.data("name", () => ({...}))` in a script file. |
| Livewire or HTMX pages with a React island for one dropdown | Two paradigms for one widget | Use the native approach of the stack, or a small web component. |

## 31.15 Folder structure tells

Naming and general structure are in part 33. Frontend-specific tells:

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `components/`, `hooks/`, `utils/`, `services/`, `types/`, `constants/`, `contexts/`, `helpers/`, `lib/` all created on day 1 with one file each | Template folders, not project needs | Start flat. Group by feature when a feature has 3+ files: `features/payments/`. |
| `components/common/`, `components/shared/`, `components/ui/`, `components/base/` all present | Four names for shared components | One: `components/ui` for primitives, feature folders for the rest. |
| Every component in its own folder with `index.ts`, `Component.tsx`, `Component.types.ts`, `Component.styles.ts`, `Component.test.tsx`, `Component.stories.tsx` for a 20-line component | Ceremony | Single file until it needs more. Add test and story files when they exist. |
| `pages/` and `app/` both present in Next with overlapping routes | Half-migrated router | One router. |
| `hooks/useFetch.ts`, `hooks/useApi.ts`, `hooks/useRequest.ts` doing the same | Repeated sessions | One data layer. |
| `services/api.ts` exporting one function per endpoint with identical bodies | Boilerplate | A typed client (generated from OpenAPI, tRPC, or one generic request function with typed wrappers only where they add value). |
| Leftover `App.css`, `logo.svg`, `reportWebVitals.js`, `setupTests.js`, `vite.svg` | create-* template leftovers | Delete. See part 33. |

## 31.16 Check

- [ ] No effect that sets state derived from props or state. Derived values computed in render.
- [ ] No effect that responds to events. Event logic lives in handlers.
- [ ] Every effect with a subscription, listener or timer returns cleanup.
- [ ] No disabled `exhaustive-deps` lint rule.
- [ ] Strict Mode on.
- [ ] Minimal state. No props copied into state. No boolean soup for request status.
- [ ] Filters, search, tab and page number live in the URL on list pages.
- [ ] Functional state updates where the next value depends on the previous.
- [ ] No global store for local or server data.
- [ ] Data fetched through a query library, server components or framework loaders, not ad-hoc effects.
- [ ] Every data view has loading, error, empty and data branches.
- [ ] Previous data kept during refetch. No full-page spinner on filter changes.
- [ ] No fetch waterfalls. Parallel fetches at the route level.
- [ ] Mutations guard against double submit. Money flows are not optimistic.
- [ ] Query keys from a factory. Invalidation targeted.
- [ ] Components split by responsibility, extracted at 3 uses. No 900-line pages, no 5-line file forests.
- [ ] No premature `Box`/`Text`/`Flex` primitives without a design system.
- [ ] One `Button` with variants, not six button components.
- [ ] No components defined inside components.
- [ ] No prop drilling past 3 layers. No provider pyramid for rarely shared state.
- [ ] Context values memoised or split.
- [ ] List keys are stable record IDs. No index keys on dynamic lists. No random keys.
- [ ] Long lists paginated or virtualised.
- [ ] `useMemo`, `useCallback`, `memo` only where profiling shows a need.
- [ ] No `document.querySelector` in components. No unsanitised `dangerouslySetInnerHTML` or `v-html`.
- [ ] Forms use a form library or `FormData`, one shared schema, pending guard, server errors mapped to fields.
- [ ] `"use client"` only on interactive leaf components.
- [ ] No Pages Router APIs in App Router.
- [ ] No blanket `force-dynamic`.
- [ ] Server actions check auth and validate input.
- [ ] No secrets in `NEXT_PUBLIC_*` or Nuxt public runtime config.
- [ ] `next/image` with sizes, `priority` only on the LCP image. `next/link` for internal links.
- [ ] `metadata` export for titles. `error.tsx` and `not-found.tsx` present.
- [ ] shadcn, MUI or other library themed with DESIGN.md tokens before use.
- [ ] Only components that are used live in `components/ui`.
- [ ] One component library, one icon set.
- [ ] Class names composed with `clsx`/`cn`, no inline style objects for static styles.
- [ ] Vue: `computed` over `watch`, no prop mutation, no `v-if` with `v-for`, `useFetch` for page data.
- [ ] Svelte 5 runes in Svelte 5 projects.
- [ ] Folder structure grows from features, not from a template. Starter files deleted.
