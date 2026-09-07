---
name: nextjs-saas
description: Next.js SaaS template. React 19, Server Actions, Prisma 7, Stripe, Resend.
---

# Next.js SaaS Template

> Pin to the current stable line when scaffolding.

## Tech Stack

| Component | Technology | Version / Notes |
|-----------|------------|-----------------|
| Framework | Next.js | 16+ (App Router, Turbopack default, React Compiler enabled by this template via `reactCompiler: true`) |
| Runtime | Node.js | 24 LTS |
| Auth | Better Auth or Clerk; Auth.js for existing projects | Passkeys + OAuth; Lucia is deprecated |
| Payments | Stripe API | Latest |
| Database | PostgreSQL | Prisma 7 (Rust-free client, edge-capable) |
| Email | Resend | React Email |
| UI | Tailwind CSS | v4 (CSS-first, no config file) |
| Lint | ESLint 9 flat config | `eslint .`; `next lint` no longer exists |

---

## Directory Structure

```
project-name/
├── prisma/
│   └── schema.prisma    # Database Schema
├── src/
│   ├── actions/         # Server Actions (mutations; backend-specialist)
│   │   ├── auth-actions.ts
│   │   ├── billing-actions.ts
│   │   └── user-actions.ts
│   ├── app/
│   │   ├── (auth)/      # Route Group: Login, register
│   │   ├── (dashboard)/ # Route Group: Protected routes (App Layout)
│   │   ├── (marketing)/ # Route Group: Landing, pricing (Marketing Layout)
│   │   └── api/         # Only used for Webhooks or Edge cases (backend-specialist)
│   │       └── webhooks/stripe/
│   ├── components/
│   │   ├── emails/      # React Email templates
│   │   ├── forms/       # Client components using useActionState (React 19)
│   │   └── ui/          # Primitives (shadcn/ui acceptable when DESIGN.md or the brief calls for it)
│   ├── lib/
│   │   ├── auth.ts      # Auth library config
│   │   ├── db.ts        # Prisma Singleton
│   │   ├── data/        # Data Access Layer (server-only reads for Server Components)
│   │   └── stripe.ts    # Stripe Singleton
│   └── app/globals.css  # Tailwind v4 imports (@theme in CSS)
├── DESIGN.md            # Visual source of truth (required before UI)
└── package.json
```

---

## SaaS Features

| Feature | Implementation |
|---------|---------------|
| Auth | Better Auth or Clerk (Auth.js in existing projects) with passkeys + OAuth |
| Reads | Server Components via `lib/data/` |
| Data Mutation | Server Actions + `useActionState` (no API routes) |
| Client server-state | TanStack Query only for polling, infinite lists, optimistic UI |
| Subscriptions | Stripe Checkout & Customer Portal |
| Webhooks | Asynchronous Stripe event handling |
| Email | Transactional via Resend |
| Validation | Zod (Server-side validation) |

---

## Database Schema

| Model | Fields (Key fields) |
|-------|---------------------|
| User | id, email, stripeCustomerId, subscriptionId, plan |
| Account | OAuth provider data (Google, GitHub...) |
| Session | User sessions (Database strategy) |

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| DATABASE_URL | Prisma connection string (Postgres) |
| BETTER_AUTH_SECRET / AUTH_SECRET | Session secret for the chosen auth library |
| STRIPE_SECRET_KEY | Payments (Server-side) |
| STRIPE_WEBHOOK_SECRET | Webhook verification |
| RESEND_API_KEY | Email sending |
| NEXT_PUBLIC_APP_URL | Application Canonical URL |

---

## Setup Steps

1. Initialize project (Node 24):
   ```bash
   npx create-next-app@latest {{name}} --typescript --tailwind --eslint --app --src-dir
   ```

2. Install core libraries (auth package per the chosen library: `better-auth` or `@clerk/nextjs`; `next-auth` only in an existing Auth.js project):
   ```bash
   npm install stripe resend @prisma/client zod
   npm install -D prisma babel-plugin-react-compiler
   ```
   Then set `reactCompiler: true` in `next.config.ts` (compiler-first when the React Compiler is enabled; the memo rule is in `nextjs-react-expert`).

3. Tailwind v4 in `globals.css`, tokens from `DESIGN.md`:
   ```css
   @import "tailwindcss";
   @custom-variant dark (&:where(.dark, .dark *));
   ```

4. Configure environment (.env.local)

5. Migrate the database:
   ```bash
   npx prisma migrate dev
   ```

6. Run local Webhook:
   ```bash
   npm run stripe:listen
   ```

7. Run project:
   ```bash
   npm run dev
   ```
