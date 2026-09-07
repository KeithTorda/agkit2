---
name: nextjs-fullstack
description: Next.js full-stack template. App Router, Server Components, Server Actions, Prisma, Tailwind v4.
---

# Next.js Full-Stack Template

> Pin to the current stable line when scaffolding.

## Tech Stack

| Component | Technology | Notes |
|---|---|---|
| Framework | Next.js 16+ | App Router; Turbopack is the default bundler |
| Runtime | Node.js 24 LTS | |
| Language | TypeScript 5.9+ | Strict mode |
| UI | React 19.2 | React Compiler enabled by this template (`reactCompiler: true`); Server Actions, `useActionState` |
| Database | PostgreSQL + Prisma 7 | Rust-free client, edge-capable; Drizzle is an accepted alternative |
| Styling | Tailwind CSS v4 | CSS-first config in `globals.css` |
| Auth | Better Auth or Clerk; Auth.js for existing projects | Protected routes via `proxy.ts` |
| Validation | Zod | Shared between actions and forms |
| Lint | ESLint 9 flat config | `eslint .` script; `next lint` no longer exists |

## Directory Structure

```
project-name/
├── prisma/schema.prisma
├── src/
│   ├── app/
│   │   ├── (auth)/            # Login, register
│   │   ├── (dashboard)/       # Protected routes
│   │   ├── api/               # Route Handlers only for webhooks and external clients (backend-specialist)
│   │   ├── layout.tsx         # Root layout, metadata, providers
│   │   ├── page.tsx
│   │   └── globals.css        # @import "tailwindcss"; @theme from DESIGN.md
│   ├── components/ui/         # Primitives (Button, Input)
│   ├── components/forms/      # Client forms using useActionState
│   ├── lib/db.ts              # Prisma singleton
│   ├── lib/dal.ts             # Data Access Layer (server-only, returns DTOs)
│   ├── lib/utils.ts
│   ├── actions/               # Server Actions (mutations; backend-specialist)
│   └── types/
├── public/
├── proxy.ts                   # Network boundary: auth checks, redirects
├── DESIGN.md                  # Visual source of truth (required before UI)
├── next.config.ts
├── eslint.config.js
└── package.json
```

## Data Layer

| Need | Use |
|---|---|
| Reads | Server Components calling `lib/dal.ts` directly; no `useEffect` fetching |
| Mutations | Server Actions in `actions/` + `useActionState` in client forms |
| Client-interactive server state (polling, infinite lists, optimistic UI) | TanStack Query |
| Webhooks, external API consumers | Route Handlers in `app/api/` |

## Environment Variables

| Variable | Purpose |
|---|---|
| DATABASE_URL | PostgreSQL connection string |
| NEXT_PUBLIC_APP_URL | Public application URL |
| BETTER_AUTH_SECRET / AUTH_SECRET | Session secret for the chosen auth library |
| NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY, CLERK_SECRET_KEY | Only when using Clerk |

## Setup Steps

1. Create the project (App Router, `src/`, Tailwind, ESLint):
   ```bash
   npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir
   ```
2. Database and validation:
   ```bash
   npm install @prisma/client zod
   npm install -D prisma tsx   # tsx runs prisma/seed.ts
   npx prisma init
   ```
3. Tailwind v4 theme in `src/app/globals.css` (values from `DESIGN.md`, never invented):
   ```css
   @import "tailwindcss";
   @custom-variant dark (&:where(.dark, .dark *));

   @theme {
     --color-primary: oklch(0.55 0.18 250); /* from DESIGN.md */
     --font-sans: var(--font-brand), system-ui, sans-serif;
   }
   ```
4. Enable the React Compiler in `next.config.ts` (`reactCompiler: true`) and install it: `npm install -D babel-plugin-react-compiler`.
5. Schema and database: edit `prisma/schema.prisma`, then `npx prisma migrate dev`.
6. Run: `npm run dev` (Turbopack by default).

## Best Practices

- Server Components by default; add `'use client'` only for state, effects, or event handlers.
- Compiler-first when the React Compiler is enabled (this template turns it on); the memo rule is in `nextjs-react-expert`.
- Validate every action input with Zod before it reaches Prisma; return typed errors to `useActionState`.
- Keep `lib/dal.ts` server-only (`import 'server-only'`) so database code never reaches the client bundle.
- IDs: UUIDv7 for sortable primary keys.
