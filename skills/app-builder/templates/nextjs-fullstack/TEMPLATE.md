# Next.js full-stack product

## Fit and inspection

Use after Next.js is selected for a product with server data or mutations. Inspect the installed router/runtime, deployment limitations, data store and identity model before choosing APIs.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Keep server-only data and credentials behind supported boundaries. Authorize data reads and mutations where they occur; a redirect or middleware check alone is insufficient.

- Choose Route Handlers, server functions/actions or a separate service from actual callers and infrastructure needs. Validate untrusted input and return stable errors.

- Use the existing database/ORM or select one for the domain. Plan constraints, migrations, transactions and private-cache isolation; do not mandate a specific ORM, ID algorithm or store.

For new visual design, complete the shared short style/reference intake and wait unless already answered or delegated. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Verify the complete user flow, denied/invalid requests, affected data persistence and relevant build/type checks; inspect actual UI. Report external credentials or services still required.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
