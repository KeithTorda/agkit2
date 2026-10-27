# Detect the actual deliverable

Read the request's object and inspect the repository before choosing a template. “Inventory” describes a domain; it does not decide whether the deliverable is a web portal, offline mobile client, desktop tool, API or spreadsheet. “Modern” does not select a stack.

## Evidence to gather

- Existing repository: framework and language manifests, lockfiles, entrypoints, routing, schema/migrations, project scripts, tests and deployment configuration.
- Product: primary users and flow, data source, roles, native capabilities, offline writes, expected usage, integrations and the actual hosting environment.
- Delivery: editable source, static files, hosted app, store package, extension, CLI or service. Respect an explicit choice.

Extend an existing foundation when it can support the request. A Laravel project stays Laravel unless a justified migration is within scope; a brochure may need only static HTML, and a dashboard can consume an existing API without a new database.

## Route by constraints

| Deliverable | Candidate reference when appropriate |
|---|---|
| Content-heavy static site | `astro-static` or the existing static pipeline |
| Static React-oriented site | `nextjs-static`; plain HTML can be simpler |
| React full-stack product | `nextjs-fullstack` |
| Subscription product on that foundation | `nextjs-saas` only if billing is actually required |
| Vue application | `nuxt-app` |
| Standalone Node/Python service | `node-api` / `python-fastapi` |
| React Native or Flutter mobile product | `react-native-app` / `flutter-app` |
| Electron desktop product | `electron-desktop` |
| Browser extension / command line tool | `chrome-extension` / `cli-tool` |
| Several independently built packages | `monorepo-turborepo` when its orchestration is useful |

These are examples already available in the kit, not an exhaustive platform list. Native Swift/Kotlin, PHP frameworks, other supported stacks, or no framework may fit better. Use current official setup guidance for the selected foundation.

For a new visual design, decide the direction unless genuinely unclear. Ask about a missing platform or offline model only when it changes a consequential choice; inspect/infer what is already established. Do not require a question count or treat silence as acceptance.
