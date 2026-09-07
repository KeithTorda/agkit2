---
name: app-builder
description: Builds a new application from a natural-language request — detects the project type, picks the template and tech stack, plans the structure, and coordinates specialist agents through build and verification. Use for /create and any "new app / from scratch" request; for a change to an existing app read feature-building.md only.
version: 2.0.0
---

# App Builder

> From request to running app: detect, plan, design tokens, build with specialists, verify.

Read only the file the current step needs:

| File | Read when |
|---|---|
| [project-detection.md](./project-detection.md) | Mapping the request to a project type and template |
| [tech-stack.md](./tech-stack.md) | Choosing or confirming technologies |
| [templates/README.md](./templates/README.md) | Scaffolding: pick one template and read only its `TEMPLATE.md` |
| [scaffolding.md](./scaffolding.md) | Next.js directory structure and core files |
| [agent-coordination.md](./agent-coordination.md) | Order of specialist agents and gates for a new app |
| [feature-building.md](./feature-building.md) | Adding a feature to an existing project (`/enhance`) |

## Which template, and what to change first

`templates/README.md` maps project type → template; read it, don't restate it. The judgment calls it does not make for you:

- **API with no web UI** → `node-api` (Hono). A Next.js app that only needs its own routes uses Route Handlers + Server Actions — no separate API.
- **SaaS with billing** → `nextjs-saas` (Stripe wired), not `nextjs-fullstack` plus hand-rolled billing.
- **Mostly static** (marketing, blog, docs) → `nextjs-static` or `astro-static`; reach for `nextjs-fullstack` only when you need a database and mutations.
- **Vue team or codebase** → `nuxt-app`, not Next. **Mobile** → `react-native-app` (Expo, cross-platform + OTA) unless the brief mandates Flutter.

After scaffolding, change the expensive-to-reverse things first, before any UI: (1) data model and ID strategy (UUIDv7), (2) auth choice, (3) the data-fetching boundary (Server Components for reads, Server Actions for writes). Name and copy come last. Pin every dependency to its current stable line.

## Process

1. Questions: follow the global `core-protocol` rule. Question format: `@[skills/brainstorming]`.
2. Detect the project type and template; confirm the stack.
3. Plan: `project-planner` writes `docs/plans/{task-slug}.md` in the `@[skills/plan-writing]` format.
4. UI projects: `frontend-specialist` (web) or `mobile-developer` (mobile-only app) creates `DESIGN.md` at the project root per `@[skills/design-spec]` before any UI code.
5. Build in the order in `agent-coordination.md`. Use the minimum number of agents the task needs. A single specialist is a valid outcome of orchestration.
6. Verify with `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py .`, start the dev server, report the URL.

## Example

```
"Make an Instagram clone with photo sharing and likes"
→ type: social app · template: nextjs-fullstack · stack: Next.js + Prisma + Cloudinary + hosted auth
→ docs/plans/instagram-clone.md: schema (users, posts, likes, follows) → API → pages (feed, profile, upload) → components
→ DESIGN.md (frontend-specialist) → database-architect → backend-specialist → frontend-specialist → checklist.py → npm run dev
```
