# Frontend ownership and structure reference

Use the project's conventions and framework capabilities. These layouts illustrate useful seams; create only folders/layers that have a real responsibility.

## A feature-oriented example

```text
src/
  app/                    route composition (when the framework uses this directory)
  features/booking/
    BookingForm.tsx       presentation and interaction
    booking.schema.ts     input contract if the project uses schemas
    booking.data.ts       data boundary when useful
    booking.test.ts       observable feature behavior
  components/ui/          stable shared primitives
  lib/                    deliberately shared infrastructure
```

A small feature can use fewer files. A service file should express a meaningful data contract, not exist only to hide a one-line fetch. Framework route files may contain appropriate loader/action work; prevent circular dependencies and route-specific assumptions leaking into shared modules.

Shared packages in a multi-app repository need an actual ownership/build/version contract. A second app alone does not mandate Turborepo, pnpm or publishing a package. Reuse through a folder/workspace only when its lifecycle fits.

## State ownership decisions

| State | Candidate owner | Important contract |
|---|---|---|
| Temporary interaction | Component/subtree | Reset when identity/lifetime changes |
| Form draft | Form workflow | Preserve input, validate, handle pending/failure |
| Deep-linkable filters | Router URL | Parse/serialize defaults; Back/Forward works |
| Server records | Loader/query cache/store already adopted | Key identity, freshness, invalidation and access |
| Shared client workflow | Context/store/reducer or feature boundary | One authority; explicit transitions and reset |
| External subscription | Supported store/subscription adapter | Consistent snapshot, cleanup and SSR behavior |
| High-frequency visual values | CSS/ref/motion value when suitable | Avoid needless renders; preserve accessibility |

Context, Redux, Zustand, Pinia and other tools are alternatives, not a mandatory state ladder. Update frequency, subtree size and debugging needs determine which fits. A global cache must not leak data across sessions/tenants; clear or scope it on identity changes.

## Server/client data boundaries

In a server-rendered app, server loaders/components can fetch private data and pass allowed serializable values to interactive UI. A client query may be appropriate for polling, infinite lists, offline behavior or existing SPA architecture. Avoid duplicate server/client requests by using the framework/query library's supported hydration path.

Server actions, route handlers and controllers are mutation boundaries when adopted by the project. All require validation and authorization. Revalidate the relevant read owner after a successful write. Client caches need deliberate optimistic rollback, error/pending state and duplicate-submission handling.

Cache keys include input dimensions that change results, such as tenant, user permissions, filters or locale. In-memory process globals must not silently become cross-request user state.

## Forms and errors

Native forms, framework actions, form libraries and local state can all be appropriate. Keep labels, field names, server errors and retained input aligned. Client validation is a usability layer; enforce authoritative rules on the server/database. Map expected errors without exposing internal details. Check keyboard submission, focus after errors and concurrent repeated actions.

A schema can be shared where formats align; do not ship server-only dependencies or secrets just to avoid defining a smaller client schema.

## Refactoring a mixed-responsibility screen

Find real seams: filtering, table rendering, editing, data loading, state transitions. Move one coherent responsibility while preserving props, URL behavior, reset rules and accessibility. Avoid extracting solely to hit line/effect counts. A large clear component can be easier than many files whose behavior must be reconstructed.

React hooks/composables encapsulate reusable state or lifecycle; ordinary pure transformations do not need hook names. Keep list keys tied to identity and server/client imports valid. Props may be narrow primitives or domain objects depending on the actual stable contract; neither is universally superior.

## Other frontend environments

- **Vue/Nuxt:** use existing Options/Composition API and loaders/composables consistently. Define state ownership/reactivity and subscription cleanup; no rewrite solely for `script setup`.
- **Laravel/Blade/Livewire/Inertia:** keep database/access work in the application's established controllers/actions/components. Use prepared view data, validation errors and supported component boundaries. Do not force an SPA or one action class per use case.
- **Plain HTML/CSS/JS:** progressive enhancement and small modules can suffice. Group styles/assets by actual reuse; add a framework/build tool only when it solves shared templating, behavior or delivery needs.

## Verification

Check imports/type contracts and a real render/interaction across affected states. Utilities/business rules warrant focused tests when meaningful; broad component snapshots rarely replace them. Use actual framework builds for module/serialization boundaries and browser checks for layout, focus, navigation and hydration. Keep an existing strictness policy; widening compiler config is a separate change with its own compatibility cost.
