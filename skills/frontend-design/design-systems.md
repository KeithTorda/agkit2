# Design systems and stack (frontend-design §2-§3, §4.9)

Read when: the brief names a design system, you choose fonts or icons for a new project, or you set up the light/dark color scheme. SKILL.md core comes first (§0.A DESIGN.md gate, §0.E anti-defaults, §1 dials).

## 2. Brief → design system map

### 2.A Real design systems (use the official package)
| Brief reads as | Reach for | Install |
|---|---|---|
| Microsoft / enterprise SaaS / dashboards | Fluent UI React v9 | `@fluentui/react-components` |
| Google-ish, Material-flavored product | MUI or Material Tailwind with Material 3 tokens (`@material/web` is in maintenance mode: only when the project already uses it) | `@mui/material` / `@material-tailwind/react` |
| IBM-style B2B / enterprise analytics | Carbon | `@carbon/react @carbon/styles` |
| Shopify app surfaces | Polaris web components (required for admin UI) | `cdn.shopify.com/shopifycloud/polaris.js` |
| Atlassian / Jira-style product | Atlassian Design System | `@atlaskit/tokens` + components |
| GitHub-style devtool / community page | Primer React (product) / Primer Brand (marketing) | `@primer/react` / `@primer/react-brand` |
| UK public-sector service | GOV.UK Frontend (regulatorily expected) | `govuk-frontend` |
| US public-sector / trust-first | USWDS v3 | `@uswds/uswds` |
| Fast local-business / agency MVP | Bootstrap 5.3 | `bootstrap` |
| Accessible React foundation you own | Radix Themes, or shadcn/ui on Radix (customize; never the default look) | `@radix-ui/themes` / `npx shadcn@latest init` |
| Tailwind-based SaaS / marketing (default for indie and small teams) | Tailwind v4 utilities + `DESIGN.md` tokens | `tailwindcss @tailwindcss/postcss` |

**Honesty rule.** If the brief reads as one of these systems, install and use the official package. Do not recreate its CSS by hand, and do not import its tokens and then override 90% of them. **One system per project**: no Fluent next to Carbon, no shadcn/ui inside a Material app.

### 2.B Aesthetics without an official package
Glassmorphism, bento, brutalism, editorial, dark-tech, aurora/mesh gradients, kinetic type: native CSS + Tailwind, with comments saying what is borrowed inspiration.
- **Glass**: `backdrop-filter: blur(24px) saturate(180%)`, 1px `border-white/20`, inset top highlight (`shadow-[inset_0_1px_0_rgba(255,255,255,0.3)]`), solid-fill fallback under `@media (prefers-reduced-transparency: reduce)` (support is uneven; keep contrast without blur). Right for premium consumer, Apple-adjacent, media overlays; wrong for dashboards, public sector, plain B2B. Apple Liquid Glass is an Apple-platform feature with no official web CSS; this recipe is the web approximation, labeled as one.

## 3. Stack defaults

Unless §2.A picks a system, build on the tech baseline: Next.js 16 App Router, React 19, TypeScript, Tailwind CSS v4, `motion/react`. React Compiler is on by default in the kit's templates; details and the memo rule: nextjs-react-expert.

### 3.A Framework and styling
- Server Components by default. Anything using motion, pointer physics, `IntersectionObserver`, or browser APIs is an isolated leaf with `"use client"` at the top; providers live in a client wrapper.
- Tailwind v4, tokens in `@theme` (mechanics: `tailwind-patterns`). Tailwind v3 only when the existing project demands it (check the version before touching config).
- Animation: `import { motion } from "motion/react"`; `framer-motion` is the legacy alias, not for new code. GSAP + ScrollTrigger only for pin/scrub work (motion.md §5.A-§5.B).
- Fonts: `next/font` or self-hosted `@font-face` with `font-display: swap`; no Google Fonts `<link>` in production; family per `DESIGN.md`.
- Data and forms: Server Actions + `useActionState` for mutations, `react-hook-form` + `zod` for complex forms; data layer in `frontend-architecture`.

### 3.B State
- `useState` / `useReducer` for isolated UI; Zustand or Jotai for shared client state; React Context only for rarely-changing values (theme, session).
- Never track continuous input-driven values (mouse position, scroll progress, magnetic hover) in `useState`: they re-render the tree every frame. Use motion values instead (motion.md §5.C, §5.D).

### 3.C Icons
Allowed: `lucide-react`, `@phosphor-icons/react`, `@radix-ui/react-icons`, `@tabler/icons-react`; `@heroicons/react` is fine for Tailwind-UI-style projects. One family per project, one `strokeWidth` (`1.5` or `2`). Do not hand-draw icon paths; if a glyph is missing, compose from primitives or add one more family deliberately.

### 3.D Emoji
Not in markup, headings, or alt text by default; use icon glyphs. Allowed sparingly when the brief asks for a playful, chat-style, or social-native tone.

### 3.E Responsiveness and layout mechanics
Breakpoints, container queries, grid-over-flex, and `min-h-dvh` heroes are `tailwind-patterns` §4. The design-side rules: page container `max-w-7xl mx-auto` (or `max-w-[1400px]`); full-height hero `min-h-[100dvh]`, never `h-screen` (`grep -rn "h-screen"` before delivering); every multi-column section declares its `< md` collapse in the same component.

### 3.F Dependency check
Before importing any third-party package, check `package.json`; if it is missing, output the install command first. Never assume a library exists.

## 4.9 Color scheme (light / dark)
- Ship the scheme `DESIGN.md` or the brief specifies (light-only, dark-only, both); unspecified means both. One mechanism per project: semantic token values swapped under `.dark` (`@custom-variant dark`, `.dark` on `<html>` from `prefers-color-scheme`; a manual toggle only when one mode would lose brand expression); `dark:` utilities for one-off exceptions only. Setup: `tailwind-patterns` §3.
- **Page theme lock**: one scheme per page, sections never flip light/dark mid-scroll; tints within the family are fine (`bg-zinc-900` inside `bg-zinc-950`), `bg-amber-50` inside a `bg-zinc-950` page is broken. One deliberate color-block switch is allowed when the brief asks. Design-system themes (Radix `<Theme>`, shadcn) are set once at the root.
- Both modes keep WCAG AA contrast, the same hierarchy (a CTA that pops in light pops in dark), and a recognizable brand color. Test both before finishing when both ship.
