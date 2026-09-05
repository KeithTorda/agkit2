# Project Templates

> Thirteen scaffolding templates for `app-builder` and `/create`. This folder is not a skill; read only the one template that matches the detected project type.

| Template | Tech Stack | When to Use |
|---|---|---|
| [nextjs-fullstack](nextjs-fullstack/TEMPLATE.md) | Next.js + Prisma; backend as Route Handlers + Server Actions | Full-stack web app |
| [nextjs-saas](nextjs-saas/TEMPLATE.md) | Next.js + Stripe | SaaS product |
| [nextjs-static](nextjs-static/TEMPLATE.md) | Next.js + motion | Landing page, portfolio |
| [nuxt-app](nuxt-app/TEMPLATE.md) | Nuxt 4 + Nuxt UI v4 | Vue full-stack app (when the project or team is Vue) |
| [node-api](node-api/TEMPLATE.md) | Hono (default) or Fastify + Zod | Standalone Node REST API; Express only for existing code |
| [python-fastapi](python-fastapi/TEMPLATE.md) | FastAPI | Python API |
| [react-native-app](react-native-app/TEMPLATE.md) | Expo + NativeWind | Mobile app (React Native) |
| [flutter-app](flutter-app/TEMPLATE.md) | Flutter + Riverpod + Drift | Mobile app (Flutter) |
| [electron-desktop](electron-desktop/TEMPLATE.md) | Electron + React | Desktop app |
| [chrome-extension](chrome-extension/TEMPLATE.md) | Chrome MV3 | Browser extension |
| [cli-tool](cli-tool/TEMPLATE.md) | Node.js + Commander | CLI app |
| [monorepo-turborepo](monorepo-turborepo/TEMPLATE.md) | Turborepo + pnpm | Monorepo |
| [astro-static](astro-static/TEMPLATE.md) | Astro + MDX | Blog / Docs |

No template for Laravel: work in the existing structure, or start a new app with `laravel new` / `composer create-project laravel/laravel` (detection in [project-detection.md](../project-detection.md)).

## Usage

1. Detect the project type ([project-detection.md](../project-detection.md)).
2. Read only that template's `TEMPLATE.md`.
3. Follow its stack and structure; pin versions to the current stable line when scaffolding.
4. UI templates require `DESIGN.md` before UI code (global `design-rules` gate; format: `@[skills/design-spec]`), created by `frontend-specialist` (web) or `mobile-developer` (mobile-only app).
