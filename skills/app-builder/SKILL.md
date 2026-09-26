---
name: app-builder
description: Builds a new application from a request - detects the project type, picks the template and stack, sets the structure, and coordinates specialists through build and verification. Use for /create and any "new app / from scratch" request; for a change to an existing app read feature-building.md only.
version: 2.5.0
---

# App Builder

From request to running app: detect, size, design tokens, build, verify by tier, run.

Read only the file the current step needs:

| File | Read when |
|---|---|
| [project-detection.md](./project-detection.md) | Mapping the request (or an existing folder) to a project type and template |
| [tech-stack.md](./tech-stack.md) | Choosing or confirming technologies |
| [templates/README.md](./templates/README.md) | Scaffolding: pick one template and read only its `TEMPLATE.md` |
| [scaffolding.md](./scaffolding.md) | Next.js directory structure and core files |
| [agent-coordination.md](./agent-coordination.md) | Which specialists, in what order, for a new app |
| [feature-building.md](./feature-building.md) | Adding a feature to an existing project (`/enhance`) |

## Which template, and what to change first

`templates/README.md` maps project type → template. The judgment calls it does not make for you:

- **Nikko's common builds.** LGU, barangay, school or COMELEC portal with admin: Laravel if the client hosts on shared PHP hosting or the team knows it, otherwise `nextjs-fullstack`. Plain brochure or landing site: `nextjs-static`, `astro-static`, or plain HTML/CSS/JS when the client wants files they can upload anywhere. POS or inventory: `nextjs-fullstack` or Laravel with Postgres/MySQL, and offline needs settled in the questions.
- **API with no web UI** → `node-api` (Hono) or `python-fastapi`. A Next.js app that only needs its own routes uses Route Handlers + Server Actions, not a separate API.
- **SaaS with billing** → `nextjs-saas` (Stripe wired), not `nextjs-fullstack` plus hand-rolled billing.
- **Mostly static** (marketing, blog, docs) → `nextjs-static` or `astro-static`; `nextjs-fullstack` only when you need a database and mutations.
- **Vue team or codebase** → `nuxt-app`. **Mobile** → `react-native-app` (Expo) unless the brief asks for Flutter.

After scaffolding, change the expensive-to-reverse things first, before any UI: (1) data model and ID strategy (UUIDv7 or the framework default), (2) auth, (3) the data-fetching boundary (Server Components for reads, Server Actions for writes in Next.js). Names and copy come last. Pin every dependency to its current stable line; the stack baseline is in `code-rules`.

## Process

1. Questions only if blocked: at most 3, each with a default (`brainstorming` for format).
2. Detect the type and template; confirm the stack.
3. Size it (`/create` step 2): small site → short plan in the reply; bigger → offer `/proplan --lite`, else a `docs/plans/<slug>.md` (`plan-writing`).
4. UI projects: `DESIGN.md` at the project root before UI code (`design-spec`), from the brief and the client's taste.
5. Build in the order in `agent-coordination.md`, delegating independent parts with `invoke_subagent`.
6. Verify by `code-rules` tier, start the dev server, report the URL.

## Example

```
"Barangay clearance request portal with an admin page"
→ type: admin portal · template: nextjs-fullstack (or Laravel if hosted on cPanel)
→ offer /proplan --lite: residents, requests, statuses, roles, printable clearance
→ DESIGN.md → database-architect (residents, requests, officials) → backend-specialist (actions, auth, PDF)
  → frontend-specialist (request form, admin table) → test-engineer (status transitions, permissions)
→ tier 2 (roles and personal data): checklist.py --full, tests, /review → npm run dev
```
