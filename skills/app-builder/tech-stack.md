# Tech Stack Selection

> Default and alternative technology choices for web applications. Prefer the current stable line; pin versions when scaffolding.

## Default Stack (Web App)

```yaml
Frontend:
  framework: Next.js 16+ (App Router)
  language: TypeScript 5.9+
  styling: Tailwind CSS v4 (CSS-first config)
  ui: React 19.2 — compiler-first when the React Compiler is enabled (reactCompiler: true in next.config; the kit's templates enable it); check the flag before removing manual memo
  data: Server Components for reads; Server Actions + useActionState for mutations; TanStack Query only for client-interactive server state
  motion: motion (motion/react)
  bundler: Turbopack (default)

Backend:
  runtime: Node.js 24 LTS
  inside the Next.js app: Route Handlers + Server Actions
  standalone Node API: Hono (edge-capable) by default, Fastify when Node-heavy; Express only for existing code (template: node-api)
  validation: Zod (default); Valibot or ArkType when bundle size matters
  lint: ESLint 9 flat config (eslint.config.js)
  other stacks: Python 3.13+ (3.14 current) with FastAPI or Django; PHP 8.4 / Laravel 12 for Laravel projects

Database:
  primary: PostgreSQL 17/18
  orm: Prisma 7 / Drizzle
  ids: UUIDv7 for sortable keys
  hosting: Supabase / Neon

Auth:
  provider: Better Auth or Clerk; Auth.js for existing projects (Lucia is deprecated)

Monorepo:
  tool: Turborepo 2.x + pnpm
```

## Alternative Options

| Need | Default | Alternative |
|------|---------|-------------|
| Real-time | Supabase Realtime | Socket.io, Ably |
| File storage | Supabase Storage | Cloudinary, AWS S3 |
| Payment | Stripe | LemonSqueezy, Paddle |
| Email | Resend | SendGrid, Postmark |
| Search | Algolia | Typesense, Orama |
| AI / LLM SDK | Vercel AI SDK (`ai` + `@ai-sdk/*`) | LangChain.js, direct REST API |
| Vector Database | PostgreSQL (pgvector via Supabase / Neon) | Pinecone, Qdrant |
| ORM (SQL-first) | Prisma 7 | Drizzle ORM (`drizzle-orm` + `drizzle-kit`) |
| Client server-state | TanStack Query | SWR is legacy; migrate it to TanStack Query |

---

## AI Application Pattern

When building an AI or LLM-powered application:
- **Streaming**: Use Vercel AI SDK `streamText` in Route Handlers or Server Actions.
- **UI State**: Leverage `useChat` / `useCompletion` with React 19 optimistic updates.
- **Embeddings & Vector**: Store vectors in PostgreSQL using `pgvector` extension; query via cosine similarity.
- **Safety & Rate Limits**: Protect AI endpoints with rate limiting (`@[skills/api-patterns]`) and Zod schema parsing.

