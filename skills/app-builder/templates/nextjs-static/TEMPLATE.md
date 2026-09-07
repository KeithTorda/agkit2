---
name: nextjs-static
description: Next.js static-export template for landing pages and portfolios. App Router, React 19, Tailwind v4, motion.
---

# Next.js Static Site Template

> Pin to the current stable line when scaffolding.

## Tech Stack

| Component | Technology | Notes |
|---|---|---|
| Framework | Next.js 16+ | App Router, static export; Turbopack is the default bundler |
| UI | React 19.2 | Server Components; React Compiler enabled by this template (`reactCompiler: true`) |
| Language | TypeScript 5.9+ | Strict mode |
| Styling | Tailwind CSS v4 | CSS-first config, no JS config file |
| Animation | motion (`motion/react`) | Successor of framer-motion; layout animations and gestures |
| Icons | Lucide (or one other family from `frontend-design` §3.C: Phosphor, Radix Icons, Tabler; Heroicons for Tailwind-UI-style projects) | One family per project |
| SEO | Metadata API | Native; `sitemap.ts`, `robots.ts`, `opengraph-image.tsx` |
| Lint | ESLint 9 flat config | `eslint .`; `next lint` no longer exists |

## Directory Structure

```
project-name/
├── src/
│   ├── app/
│   │   ├── layout.tsx            # Root metadata, fonts
│   │   ├── page.tsx              # Landing page
│   │   ├── globals.css           # @import "tailwindcss"; @theme from DESIGN.md
│   │   ├── not-found.tsx
│   │   ├── sitemap.ts
│   │   ├── robots.ts
│   │   ├── opengraph-image.tsx
│   │   └── (routes)/             # about, contact, ...
│   ├── components/layout/        # Header, Footer
│   ├── components/sections/      # Hero, Features, Pricing, FAQ, CTA
│   ├── components/ui/            # Button, Card
│   └── lib/utils.ts              # cn, formatters
├── content/                      # Markdown / MDX
├── public/
├── DESIGN.md                     # Visual source of truth (required before UI)
├── next.config.ts
└── package.json
```

## Static Export Config

```typescript
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",            // static hosting (S3, GitHub Pages, Netlify)
  images: { unoptimized: true }, // no image server in static export; or use an image CDN loader
  trailingSlash: true,          // avoids 404s on some static hosts
};

export default nextConfig;
```

## SEO (Metadata API)

```typescript
// src/app/layout.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: { template: "%s | Product", default: "Product — one-line promise" },
  description: "What the product does, for whom.",
  openGraph: { type: "website", locale: "en_US", url: "https://example.com", siteName: "Product" },
};
```

## Landing Page Sections

| Section | Purpose |
|---|---|
| Hero | H1, one-line promise, primary CTA |
| Features | Benefits, not feature lists; vary the layout (avoid three identical cards by default) |
| Social proof | Logos, numbers, testimonials |
| Pricing | Plans with one recommended option |
| FAQ | Objections answered; good for SEO |
| CTA | Final conversion |

## Animation Patterns (motion)

```tsx
import { motion, useScroll, useTransform } from "motion/react";
```

| Pattern | Implementation |
|---|---|
| Fade up | `initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}` |
| Stagger | Parent variants with `staggerChildren` |
| Parallax | `useScroll` + `useTransform` |
| Micro-interactions | `whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}` |

Respect `prefers-reduced-motion` (`useReducedMotion`).

## Setup Steps

1. `npx create-next-app@latest my-site --typescript --tailwind --eslint --app --src-dir`
2. `npm install motion lucide-react clsx tailwind-merge` and `npm install -D babel-plugin-react-compiler`; set `reactCompiler: true` in `next.config.ts` (compiler-first when the React Compiler is enabled; the memo rule is in `nextjs-react-expert`).
3. `src/app/globals.css` with tokens from `DESIGN.md`:
   ```css
   @import "tailwindcss";
   @custom-variant dark (&:where(.dark, .dark *));

   @theme {
     --color-primary: oklch(0.55 0.18 250); /* from DESIGN.md */
     --font-sans: var(--font-brand), system-ui, sans-serif;
   }
   ```
4. `npm run dev`; `npm run build` writes the static site to `out/`.

## Deployment

| Platform | Method | Notes |
|---|---|---|
| Vercel / Netlify | git push | auto-detected |
| GitHub Pages | Actions workflow | set `basePath` when not on a custom domain |
| S3 / CloudFront | upload `out/` | error document → `404.html` |

## Best Practices

- Server Components by default; `'use client'` only for state, event handlers, and motion components.
- `next/font` for self-hosted fonts and zero layout shift; the family comes from `DESIGN.md`.
- Mobile-first with `sm:` / `md:` / `lg:`; images via `<Image />` with an external loader or `unoptimized`.
- Lighthouse is advisory; run it when a URL is available (`@[skills/performance-profiling]`), plus the SEO check (`@[skills/seo-fundamentals]`).
