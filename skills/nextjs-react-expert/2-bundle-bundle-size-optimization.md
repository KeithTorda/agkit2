# 2. Bundle Size Optimization

> **Impact:** CRITICAL
> **Focus:** Reducing initial bundle size improves Time to Interactive and Largest Contentful Paint.

---

## Overview

Five rules for bundle size. Next.js 16 builds with Turbopack by default; the rules below apply to both bundlers.

---

## Rule 2.1: Avoid Barrel File Imports

**Impact:** CRITICAL  
**Tags:** bundle, imports, tree-shaking, barrel-files, performance  

**Barrel files** are entry points that re-export many modules (an `index.ts` full of `export * from './x'`). Large icon and component libraries can have thousands of re-exports in their entry file; importing one symbol can pull the whole graph into dev compilation and server cold starts.

**Why tree-shaking does not fully help:** when a library is external (not bundled) the bundler cannot prune it, and bundling it to enable tree-shaking makes builds slower because the whole module graph is analyzed.

**What Next.js does for you:** `optimizePackageImports` rewrites barrel imports to direct imports at build time. Popular libraries are on the built-in list (including `lucide-react`, `@mui/material`, `@mui/icons-material`, `@headlessui/react`, `@heroicons/react`, `date-fns`, `lodash-es`, `react-icons`, `@tabler/icons-react`, `rxjs`, `recharts`, `react-use`), so keeping the ergonomic import is correct for them:

```tsx
import { Check, X, Menu } from 'lucide-react' // optimized automatically
```

Add other barrel-heavy packages to the list instead of writing deep import paths:

```ts
// next.config.ts
const nextConfig = {
  experimental: {
    optimizePackageImports: ['@acme/design-system', '@radix-ui/themes'],
  },
}
export default nextConfig
```

Do not hand-write internal paths such as `lucide-react/dist/esm/icons/check`; they break on library releases and gain nothing over the build-time rewrite.

**Your own code:** avoid `index.ts` barrels in app code (`components/index.ts` re-exporting everything). Import from the file that defines the component. Barrels in app code defeat route-level code splitting and slow HMR.

Reference: [How we optimized package imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)

---

## Rule 2.2: Conditional Module Loading

**Impact:** HIGH  
**Tags:** bundle, conditional-loading, lazy-loading  

Load large data or modules only when a feature is activated.

**Example (lazy-load animation frames):**

```tsx
function AnimationPlayer({ enabled, setEnabled }: { enabled: boolean; setEnabled: React.Dispatch<React.SetStateAction<boolean>> }) {
  const [frames, setFrames] = useState<Frame[] | null>(null)

  useEffect(() => {
    if (enabled && !frames && typeof window !== 'undefined') {
      import('./animation-frames.js')
        .then(mod => setFrames(mod.frames))
        .catch(() => setEnabled(false))
    }
  }, [enabled, frames, setEnabled])

  if (!frames) return <Skeleton />
  return <Canvas frames={frames} />
}
```

The `typeof window !== 'undefined'` check prevents bundling this module for SSR, optimizing server bundle size and build speed.

---

## Rule 2.3: Defer Non-Critical Third-Party Libraries

**Impact:** MEDIUM  
**Tags:** bundle, third-party, analytics, defer  

Analytics, logging, and error tracking do not block user interaction, so they should not sit in the critical bundle. Load them after hydration.

`next/dynamic` with `{ ssr: false }` is only allowed inside a **Client Component**. A `RootLayout` is a Server Component; calling `dynamic(..., { ssr: false })` there throws at build time.

**Incorrect (Server Component, throws):**

```tsx
// app/layout.tsx  (Server Component)
import dynamic from 'next/dynamic'
const Analytics = dynamic(() => import('@vercel/analytics/react').then(m => m.Analytics), { ssr: false })
```

**Correct (wrap in a Client Component, render it from the layout):**

```tsx
// app/analytics.tsx
'use client'
import dynamic from 'next/dynamic'

export const Analytics = dynamic(
  () => import('@vercel/analytics/react').then(m => m.Analytics),
  { ssr: false }
)
```

```tsx
// app/layout.tsx  (Server Component)
import { Analytics } from './analytics'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

Libraries that ship a Next.js-aware component (for example `@vercel/analytics/next`) already handle this; prefer that entry point when it exists.

---

## Rule 2.4: Dynamic Imports for Heavy Components

**Impact:** CRITICAL  
**Tags:** bundle, dynamic-import, code-splitting, next-dynamic  

Use `next/dynamic` to lazy-load large components not needed on initial render. With `{ ssr: false }` the call must live in a Client Component (`'use client'`); without that option it works in Server Components too.

**Incorrect (Monaco bundles with main chunk ~300KB):**

```tsx
import { MonacoEditor } from './monaco-editor'

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

**Correct (Monaco loads on demand):**

```tsx
'use client'
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(
  () => import('./monaco-editor').then(m => m.MonacoEditor),
  { ssr: false }
)

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

---

## Rule 2.5: Preload Based on User Intent

**Impact:** MEDIUM  
**Tags:** bundle, preload, user-intent, hover  

Preload heavy bundles before they're needed to reduce perceived latency.

**Example (preload on hover/focus):**

```tsx
function EditorButton({ onClick }: { onClick: () => void }) {
  const preload = () => {
    if (typeof window !== 'undefined') {
      void import('./monaco-editor')
    }
  }

  return (
    <button
      onMouseEnter={preload}
      onFocus={preload}
      onClick={onClick}
    >
      Open Editor
    </button>
  )
}
```

**Example (preload when feature flag is enabled):**

```tsx
function FlagsProvider({ children, flags }: Props) {
  useEffect(() => {
    if (flags.editorEnabled && typeof window !== 'undefined') {
      void import('./monaco-editor').then(mod => mod.init())
    }
  }, [flags.editorEnabled])

  return <FlagsContext.Provider value={flags}>
    {children}
  </FlagsContext.Provider>
}
```

The `typeof window !== 'undefined'` check prevents bundling preloaded modules for SSR, optimizing server bundle size and build speed.

