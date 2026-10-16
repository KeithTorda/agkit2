# Nuxt application

## Fit and inspection

Use when Vue/Nuxt is selected or already present. Inspect release, server runtime, rendering mode, deployment adapter and existing module choices.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Follow installed conventions for pages, layouts, composables and server routes. Keep private runtime configuration out of client-exposed configuration.

- Choose SSR, prerendering or client rendering by content, identity and hosting needs; verify hydration and data-fetch behavior.

- Reuse existing UI/state modules. Nuxt UI, a global store, ORM or animation package are options rather than requirements.

For new visual design, complete the shared short style/reference intake and wait unless already answered or delegated. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Run relevant build/type checks, inspect SSR/hydration and affected routes, exercise mutations and authorization where present, and confirm the chosen hosting output.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
