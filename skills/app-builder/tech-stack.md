# Tech Stack Selection

Default and alternative technology choices when the project has no preference. The existing stack always wins. Versions follow the September 2026 baseline in `code-rules`; pin the current stable line when scaffolding.

## Default Stack (Web App)

```yaml
Frontend:
  framework: Next.js 16+ (App Router)
  language: TypeScript 5.9+
  styling: Tailwind CSS v4 (CSS-first config)
  ui: React 19.2 — compiler-first when the React Compiler is enabled; the memo rule is in nextjs-react-expert
  data: Server Components for reads; Server Actions + useActionState for mutations; TanStack Query only for client-interactive server state
  motion: motion (motion/react)
  bundler: Turbopack (default)

Backend:
  runtime: Node.js 24 LTS
  inside the Next.js app: Route Handlers + Server Actions
  standalone Node API: Hono (edge-capable) by default, Fastify when Node-heavy; Express only for existing code (template: node-api)
  validation: Zod (default); Valibot or ArkType when bundle size matters
  lint: ESLint 9 flat config (eslint.config.js)
  other stacks: Python 3.13+ (3.14 current) with FastAPI or Django, Ruff; PHP 8.4 / Laravel 12+ with Pest, Blade + Livewire or Inertia (React/Vue)

Database:
  primary: PostgreSQL 17/18
  orm: Prisma 7 (prisma.config.ts, driver adapter) / Drizzle; Eloquent in Laravel
  ids: UUIDv7 for sortable keys
  hosting: Supabase / Neon; MySQL or Postgres on the client's VPS or cPanel when that is where it must live

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

## Mobile

Expo SDK 54+ with Expo Router and the New Architecture (`react-native-app`); Flutter 3.3x with Riverpod 3 when the brief asks for Flutter (`flutter-app`).

## AI Application Pattern

When building an AI or LLM-powered application:
- **Streaming**: Use Vercel AI SDK `streamText` in Route Handlers or Server Actions.
- **UI state**: `useChat` / `useCompletion` from `@ai-sdk/react`, with React 19 optimistic updates.
- **Embeddings & Vector**: Store vectors in PostgreSQL using `pgvector` extension; query via cosine similarity.
- **Safety and rate limits**: Protect AI endpoints with rate limiting (`api-patterns`) and Zod schema parsing.

