---
name: frontend-design
description: Designs and builds web UI that does not look templated - landing pages, marketing and product sites, portfolios, page-level app UI, and audit-first redesigns. Reads the brief, consumes the project's DESIGN.md tokens, picks a real design system when one applies, sets layout/motion/density dials, and runs a short mechanical pre-flight. Use for any web UI design, build, or design-review task. Not for mobile apps (mobile-design) or DESIGN.md authoring (design-spec).
version: 2.0.0
---

# Frontend Design

Web UI for landing pages, marketing and product sites, portfolios, page-level app UI, and redesigns. Not for mobile apps (`mobile-design`), dense data tables, code editors, or realtime-collab surfaces: say so and apply only the parts that fit.

Everything in §1-§8 is a **contextual default**: apply what fits the design read, override it when the brief, brand, or `DESIGN.md` says otherwise, and say so when you do. The pre-flight boxes in §10 are the skill's self-check; the required gate is the global `code-rules` rule.

Sub-files (read only when the brief calls for it):

| File | When |
|---|---|
| [style-minimalist.md](./style-minimalist.md) | Brief chooses clean, warm-monochrome, editorial minimalism |
| [style-brutalist.md](./style-brutalist.md) | Brief chooses raw Swiss-industrial or terminal/telemetry aesthetics |
| [redesign.md](./redesign.md) | Audit checklist for an existing codebase (protocol is §8 here) |
| `./scripts/ux_audit.py`, `./scripts/accessibility_checker.py` | See §9 |

Design rules adapted from [taste-skill](https://github.com/Leonxlnx/taste-skill) by Leonxlnx (MIT).

---

## 0. Before anything: DESIGN.md, then the design read

### 0.A The DESIGN.md gate
The gate lives in the global `design-rules` rule (when it applies, when to infer, when to skip). Follow it; do not restate it. What it means for the build here:

- If `DESIGN.md` exists, its tokens win over everything in this skill (fonts, colors, radius, spacing, color scheme, components). The heuristics below only fill the gaps it leaves open.
- If it does not and this is a new app or a page-level UI, author it with `design-spec` first, then come back.
- Tokens flow one way: `DESIGN.md` YAML → Tailwind v4 `@theme` (the token→`@theme` mapping and `@theme` mechanics are `tailwind-patterns` §2; `npx @google/design.md export --format css-tailwind` writes it when the CLI is available). One token source; no second list in `tailwind.config.js` or in components.

### 0.B Read the signals
1. **Page kind**: landing (SaaS / consumer / agency / event), portfolio, app page, editorial, redesign (preserve vs overhaul).
2. **Vibe words** the user used: "minimalist", "Linear-style", "Awwwards", "brutalist", "premium", "playful", "serious B2B", "editorial", "dark tech".
3. **References**: URLs, screenshots, named products or competitors.
4. **Audience**: procurement panel, design-conscious consumer, recruiter, citizen. The audience picks the aesthetic, not your taste.
5. **Existing brand assets**: logo, colors, type, photography; for redesigns they are starting material (§8).
6. **Quiet constraints**: accessibility-first audiences, public sector, regulated industries, trust-first commerce, kids' products. These override aesthetic preference.

### 0.C State the design read in one line
Before code, name page kind, audience, vibe, and the design system or aesthetic family you lean toward. Example: *"Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind utilities + Geist + restrained motion."*

### 0.D One question, or none
Questions follow the global `core-protocol` rule. Design questions count toward that budget: at most one, in the same message as any planning questions, never a second round (example: "Closer to Linear-clean or Awwwards-experimental?"). If you can infer the direction, do not ask: declare the design read and proceed.

### 0.E Anti-defaults, not bans
Purple/violet primaries, Inter, shadcn/ui, glassmorphism, three equal cards, a centered hero over a dark mesh, micro-animations on every card: *anti-default heuristics*, not bans. Don't reach for them unexamined; use them when the brief, brand, or `DESIGN.md` asks, and note the reason in one line when you do.

---

## 1. The three dials

After the design read, set three dials. Layout, motion, and density decisions below are gated by them. Baseline `8 / 6 / 4`; the design read overrides it. Use these exact names, never aliases.

- `DESIGN_VARIANCE` (1 = perfect symmetry, 10 = artsy chaos)
- `MOTION_INTENSITY` (1 = static, 10 = cinematic / physics)
- `VISUAL_DENSITY` (1 = art gallery, 10 = cockpit)

### 1.A Dial inference
| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| minimalist / clean / calm / editorial / Linear-style | 5-6 | 3-4 | 2-3 |
| premium consumer / Apple-y / luxury / brand | 7-8 | 5-7 | 3-4 |
| playful / Dribbble / Awwwards / experimental / agency | 9-10 | 8-10 | 3-4 |
| landing page / portfolio / marketing (default) | 7-9 | 6-8 | 3-5 |
| trust-first / public sector / regulated / accessibility-critical | 3-4 | 2-3 | 4-5 |
| redesign, preserve | match existing | +1 | match |
| redesign, overhaul | +2 | +2 | match |

### 1.B Presets
| Use case | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Landing, SaaS mainstream | 7 | 6 | 4 |
| Landing, agency / creative | 9 | 8 | 3 |
| Landing, premium consumer | 7 | 6 | 3 |
| Portfolio, designer / studio | 8 | 7 | 3 |
| Portfolio, developer | 6 | 5 | 4 |
| Editorial / blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |
| App page (dashboard-like) | 3-4 | 2-3 | 6-8 |

### 1.C What the levels mean
- **VARIANCE** 1-3: symmetrical 12-col grid, centered. 4-7: `-mt-8` overlaps, mixed aspect ratios, left-aligned headers over centered data. 8-10: masonry, fractional grids (`grid-cols-[2fr_1fr_1fr]`), large empty zones. At 4-10 every asymmetric layout collapses to one column below `md`.
- **MOTION** 1-3: `:hover` / `:active` only. 4-7: transitions on `transform` / `opacity`, `animation-delay` cascades. 8-10: scroll-driven reveals, parallax, pinned sections via `motion/react`, GSAP ScrollTrigger, or CSS `animation-timeline`; never a `scroll` listener (§5.D).
- **DENSITY** 1-3: `py-32` to `py-48` gaps. 4-7: `py-16` to `py-24`. 8-10: tight padding, 1px rules instead of cards, mono `tabular-nums` numbers.

---

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

---

## 3. Stack defaults

Unless §2.A picks a system, build on the tech baseline: Next.js 16 App Router, React 19 — compiler-first when the React Compiler is enabled (`reactCompiler: true` in next.config / babel-plugin-react-compiler in Expo — the kit's templates enable it); check the flag before removing manual memo — TypeScript, Tailwind CSS v4, `motion/react`.

### 3.A Framework and styling
- Server Components by default. Anything using motion, pointer physics, `IntersectionObserver`, or browser APIs is an isolated leaf with `"use client"` at the top; providers live in a client wrapper.
- Tailwind v4, tokens in `@theme` (mechanics: `tailwind-patterns`). Tailwind v3 only when the existing project demands it (check the version before touching config).
- Animation: `import { motion } from "motion/react"`; `framer-motion` is the legacy alias, not for new code. GSAP + ScrollTrigger only for pin/scrub work (§5).
- Fonts: `next/font` or self-hosted `@font-face` with `font-display: swap`; no Google Fonts `<link>` in production; family per `DESIGN.md`.
- Data and forms: Server Actions + `useActionState` for mutations, `react-hook-form` + `zod` for complex forms; data layer in `frontend-architecture`.

### 3.B State
- `useState` / `useReducer` for isolated UI; Zustand or Jotai for shared client state; React Context only for rarely-changing values (theme, session).
- Never track continuous input-driven values (mouse position, scroll progress, magnetic hover) in `useState` — they re-render the tree every frame. Use motion values instead (§5.C, §5.D).

### 3.C Icons
Allowed: `lucide-react`, `@phosphor-icons/react`, `@radix-ui/react-icons`, `@tabler/icons-react`; `@heroicons/react` is fine for Tailwind-UI-style projects. One family per project, one `strokeWidth` (`1.5` or `2`). Do not hand-draw icon paths; if a glyph is missing, compose from primitives or add one more family deliberately.

### 3.D Emoji
Not in markup, headings, or alt text by default; use icon glyphs. Allowed sparingly when the brief asks for a playful, chat-style, or social-native tone.

### 3.E Responsiveness and layout mechanics
Breakpoints, container queries, grid-over-flex, and `min-h-dvh` heroes are `tailwind-patterns` §4. The design-side rules: page container `max-w-7xl mx-auto` (or `max-w-[1400px]`); full-height hero `min-h-[100dvh]`, never `h-screen`; every multi-column section declares its `< md` collapse in the same component.

### 3.F Dependency check
Before importing any third-party package, check `package.json`; if it is missing, output the install command first. Never assume a library exists.

---

## 4. Design directives (defaults with override paths)

### 4.0 Design judgment (considered vs templated)
The bar for every design; §4.1-§4.9 are the code-level rules that apply it.
- **One focal point per view.** One element wins the eye first (hero line, primary CTA, the one number that matters); everything else is visibly subordinate in size, weight, or color. Test: grayscale and squint; if two things tie for first read, demote one. Everything bold means nothing is.
- **A real type scale.** 4-6 sizes off one ratio (~1.2-1.333), not ad-hoc px; neighbors differ enough to read as distinct levels (two sizes 2px apart look like a bug). Weight carries hierarchy cheaper than size: one family, 2-3 weights. Past ~6 sizes or ~3 weights, the scale is drifting.
- **One spacing rhythm.** Every gap is a step on one scale (the `DESIGN.md` spacing tokens), never a one-off `p-[13px]`. Proximity is grouping: related things sit closer than unrelated, and section gaps read larger than in-section gaps. A gap whose scale step you can't name is wrong.
- **Restraint, applied everywhere.** One accent, one type family (two with a reason), one radius scale, one shadow language, one motion vocabulary. Templated design reaches for a new color/weight/radius per section; considered design reuses one small kit. A new element is an exception you justify, not a reflex.
- **Contrast and whitespace do the work.** Emphasis comes from size, weight, color, and space, not stacked borders, boxes, glows, and gradients. Whitespace is the cheapest signal of hierarchy and quality; a cramped "premium" layout is a contradiction. Reach for space and contrast before a card or a divider. Motion earns its place the same way (§5): it communicates or it goes.

### 4.1 Typography
- Display `text-4xl md:text-6xl tracking-tighter leading-none`; body `text-base leading-relaxed max-w-[65ch]`.
- Sans per `DESIGN.md`. Without one, prefer a face with character (Geist, Satoshi, Cabinet Grotesk, Outfit). Inter is an anti-default: fine when the brief asks for a neutral / Linear-style / public-sector feel.
- Serif only when the brand names one or the aesthetic is genuinely editorial / luxury / publication / heritage, and you can say why this serif fits; "creative brief = serif" is the most-tested AI tell (Fraunces / Instrument Serif are anti-defaults for it). A deliberate serif-display + sans-body pairing is fine in those cases; document it in `DESIGN.md`.
- Emphasis inside a headline: italic or bold of the same family, not a serif word dropped into a sans headline.
- Italic display words with `y g j p q` need `leading-[1.1]` minimum plus `pb-1`, or the descender clips.
- Data numbers: `tabular-nums` or mono. `text-wrap: balance` on headlines, `text-wrap: pretty` on body.

### 4.2 Color
- One accent, saturation under 80% by default, on a neutral base (zinc / slate / stone), the same accent across the whole page (no blue CTA in section 7 of a rose-accented site). Do not mix warm and cool grays in one project.
- Purple / violet primaries are an anti-default (§0.E). When the brand or `DESIGN.md` asks for purple, embrace it with a consistent palette and restrained gradients.
- **Premium-consumer trap:** cookware, wellness, artisan, luxury, and DTC home-goods briefs pull the same "warm cream + brass/clay/oxblood + espresso" palette every time. Use it only when the brand names those colors or is vintage-craft; else pick another family on purpose (silver/chrome, forest + bone + amber, off-black + tan, cobalt + cream, terracotta + slate, monochrome + one saturated pop).
- Shadows tinted to the background hue; no pure-black drop shadows on light backgrounds. No pure `#000000` or `#ffffff` surfaces; off-black and off-white keep depth.

### 4.3 Layout, cards, shape
- Centered hero is avoided at `DESIGN_VARIANCE > 4`: 50/50 split, left content / right asset, or asymmetric whitespace. Centered is right for editorial / manifesto / launch briefs where the message is the design.
- Cards only where elevation communicates hierarchy; otherwise group with `border-t`, `divide-y`, or space. At `VISUAL_DENSITY > 7` no generic card containers.
- Three equal feature cards are an anti-default: prefer a 2-col split, asymmetric grid, bento, or horizontal scroll; three cards are fine when the content is genuinely three parallel items.
- **Radius**: one scale from `DESIGN.md` `rounded` (all-sharp, all-soft 12-16px, or all-pill for interactive); mixed radii only under a documented rule ("buttons pill, cards 16px, inputs 8px") applied everywhere.
- Z-index only for systemic layers (sticky nav, modal, overlay, grain), documented in one constants file; no arbitrary `z-50`.

### 4.4 States and forms
- Ship the full cycle: loading (skeletons matching the final layout, not spinners), empty (composed, says how to populate), error (inline for forms, toast only for transient), `:active` feedback (`scale-[0.98]` or `-translate-y-px`).
- Visible `focus-visible` ring on every interactive element; never `outline: none` without a replacement.
- Buttons: text readable against its own background at WCAG AA (4.5:1, 3:1 for 18px+); ghost buttons over photos get a scrim or stroke. Primary CTA labels fit one line at desktop (three words max). One label per intent per page ("Get in touch" and "Let's talk" are one intent: pick one for nav, hero, footer).
- Forms: label above input (never placeholder-as-label), helper text in markup, error text below, `gap-2` blocks; inputs, placeholders, labels, focus rings, and error text pass AA against the section background. Validate against a schema, not `window.alert()`.

### 4.5 Layout rules
Fix these before delivering; the mechanically checkable ones recur as pre-flight boxes (§10).
- **Hero fits the first viewport**: headline ≤ 2 lines, subtext ≤ 20 words and ≤ 4 lines, CTAs visible without scrolling. Plan font scale and asset size together: `text-4xl md:text-5xl lg:text-6xl` for most heroes, `text-7xl` only for 3-5-word headlines; a 4-line headline is a font-size error. Top padding ≤ `pt-24` at desktop.
- **Hero stack ≤ 4 text elements**: eyebrow or brand strip (or neither), headline, subtext, CTAs (1 primary + ≤ 1 secondary). Taglines under CTAs, trust strips, pricing teasers, feature bullets, avatar rows, and the logo wall get their own sections below the hero.
- **Navigation** on one line at `lg`, height ≤ 80px (default 64-72): condense, drop, or hamburger.
- **Eyebrows** (small uppercase tracked labels above headlines): at most 1 per 3 sections, hero counts as one; count > ceil(sections / 3) fails. Dropping the eyebrow is the default fix; the headline is enough.
- **Split-header** (big headline left, small explainer floating right) is an anti-default; stack headline over body (`max-w-[65ch]`) unless the right column carries a visual or interactive element.
- **Bento grids** have exactly as many cells as content items (3 items → 1+2 or 2+1, never a blank tile) and real variation in at least 2-3 cells (image, brand gradient, pattern, tint).
- **Layout-family repetition**: a family (3-col cards, full-width quote, split text/image) appears at most once per page; an 8-section page uses at least 4 families; image/text zigzag at most 2 sections in a row.
- **Section theme lock**: sections do not invert the page's color scheme mid-scroll (§4.9).

### 4.6 Images and visual assets
Landing pages and portfolios are visual products; text-only pages with fake-screenshot divs are slop.
1. **Image-generation tool first.** If any image tool is available, generate section-specific assets (hero, product shot, texture, mood) at the section's aspect ratio.
2. **Real photography second.** `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}`, brand or stock URLs from the brief, open-license sources when allowed.
3. **Last resort: labeled placeholder slots** (`<!-- TODO: hero product photo, 1600x1200 -->`) plus a closing line listing what the page needs. Never fill the gap with hand-rolled SVG illustrations or div-built "screenshots".

- Even minimalist sites need 2-3 real images (hero, one product or lifestyle shot, one supporting image).
- Logo walls: real SVG marks (`https://cdn.simpleicons.org/{slug}/{hex}`, `simple-icons`, devicon for tech stacks); invented brands get a simple inline SVG monogram. Logos only, no category labels, both color schemes covered.
- Product previews: real screenshot, generated image, or live mini-component; never a dashboard, task list, or terminal made of `<div>`s.
- Every meaningful image has descriptive `alt`, decorative images `alt=""`; hero image `priority` / preloaded; every image has reserved dimensions.

### 4.7 Content and copy (one rule set for all visible strings)
- Per section: headline ≤ 8 words, sub-paragraph ≤ 25 words, one visual or one CTA. Cut the rest.
- No data-dump sections on marketing pages (20-row tables, 30-row award lists): top 3-5 + "View all", or another page. Lists over 5 items get a real component (2-col groups, card grid, tabs, scroll-snap pills, one marquee), not a longer `<ul>` with a hairline under every row. Spec sheets: grouped chunks, featured-vs-rest disclosure, or a 2-col spec card grid.
- Quotes ≤ 3 lines, attribution name + role (+ company), typographic quotes or none.
- Numbers are real (brief, brand, public data) or labeled mock (`<!-- mock -->`); no invented precision (`5.8 mm`, `4.1×`) and no round fakes (`99.99%`, `50%`).
- Names, brands, avatars: locale-appropriate, specific, non-repeating; no "John Doe", "Acme", "Nexus", egg avatars, or the same face twice.
- One voice per page, concrete verbs, sentence-case headings, active voice, no lorem ipsum; no "Elevate", "Seamless", "Unleash", "Next-Gen", "Delve", "Oops!", or exclamation marks in system messages.
- **Dashes:** no em-dash (`—`) or en-dash (`–`) in visible copy: headlines, eyebrows, labels, body, quotes, attribution, captions, buttons, alt text. Use a period, comma, colon, parentheses, or a hyphen (`2018-2026`). Pre-flight grep.
- **Copy self-audit before shipping:** re-read every visible string; rewrite anything grammatically broken, referent-less, cute-but-wrong, or performatively thoughtful. Plain beats clever.

### 4.8 AI tells (avoid unless the brief asks)
- Visual: neon outer glows, gradient text on large headers, oversaturated accents, custom cursors, crosshair or hairline grid lines as decoration, decorative status dots (real state only, one per section), `·` as universal separator (max one per line).
- Labels: version labels (`V0.6`, `BETA`) unless the brief is a launch; section-number eyebrows (`001 · Capabilities`); `01 / 4` tile pagination; scroll cues; hero-bottom strips (`DESIGN · BUILD · SHIP`); floating top-right sub-text in section headers; locale / time / weather strips unless the brand is place-based.
- Copy: "Quietly trusted by", "Field notes"-style poetic labels, "Stage 1 / Stage 2" (use the verb-noun), micro-meta sentences under headings, mock-humble asides, photo-credit captions on stock images, tags overlaid on photos, fake version footers (`v1.4.2`, "last sync 4s ago").
- Layout: `border-t` and `border-b` on every row; filled-track progress bars as comparison visuals; `<br>`-split italic headlines; vertical rotated text; H1s that scream by size alone.
- Components (discouraged defaults, not bans): accordion FAQ, three-tower pricing, dotted testimonial carousel, sun/moon toggle, 4-column footer link farm, filled-plus-ghost button pair. Fine when the content shape fits (ten questions is an accordion); the tell is reaching for them unexamined.
- shadcn/ui is a fine foundation, never in its default look (radii, colors, shadows, type adjusted to the project).

### 4.9 Color scheme (light / dark)
- Ship the scheme `DESIGN.md` or the brief specifies: light-only, dark-only, or both; if unspecified, ship both. One mechanism per project: swap semantic token values under `.dark` (with `@custom-variant dark`, `.dark` on `<html>` from `prefers-color-scheme`, a manual toggle only when one mode would lose brand expression); `dark:` utilities for one-off exceptions only. Setup code is `tailwind-patterns` §3.
- **Page theme lock:** one scheme per page; sections do not flip between light and dark mid-scroll. Tints within the family are fine (`bg-zinc-950` next to `bg-zinc-900`); `bg-amber-50` inside a `bg-zinc-950` page is broken. A single deliberate color-block switch is allowed once when the brief asks for it. Design-system themes (Radix `<Theme>`, shadcn) are set once at the root.
- Both modes keep WCAG AA contrast, the same hierarchy (a CTA that pops in light pops in dark), and a recognizable brand color. Test both before finishing when both ship.

---

## 5. Motion

Motion is motivated or absent: before adding an animation, name what it communicates (hierarchy, storytelling, feedback, state transition). "It looked cool" means drop it.
- If `MOTION_INTENSITY > 4`, the page actually moves (hero entry, reveals on key sections, hover physics on CTAs). If working motion does not fit the scope, set the dial to 3 and ship a clean static page rather than half-built ScrollTriggers.
- Perpetual loops (pulse, typewriter, shimmer, float) only where "live" means something (status, feeds, AI-feel), never on every card. Spring physics (`type: "spring", stiffness: 100, damping: 20`), not linear easing.
- Magnetic / pointer physics only at `MOTION_INTENSITY > 5` for premium / playful / agency briefs, via motion values (§3.B). One marquee per page at most.
- **One animation library per component.** A component imports `motion/react` or `gsap`, never both; they fight over the same frames. GSAP and Three.js live in dedicated client leaves with cleanup. Reduced motion is handled by the library in use: `useReducedMotion()` for Motion, `gsap.matchMedia()` for GSAP, `@media (prefers-reduced-motion)` for CSS.

### 5.A Sticky stack (GSAP, pin/scrub)
```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const mm = gsap.matchMedia();                       // reduced-motion handled by GSAP itself
    mm.add("(prefers-reduced-motion: no-preference)", () => {
      const els = Array.from(ref.current!.querySelectorAll<HTMLElement>(".stack-card"));
      els.forEach((card, i) => {
        if (i === els.length - 1) return;
        ScrollTrigger.create({ trigger: card, start: "top top", endTrigger: els[els.length - 1],
          end: "top top", pin: true, pinSpacing: false });   // "top top", never "top center"
        gsap.to(card, { scale: 0.92, opacity: 0.55, ease: "none",
          scrollTrigger: { trigger: els[i + 1], start: "top bottom", end: "top top", scrub: true } });
      });
    });
    return () => mm.revert();                           // kills triggers and tweens on unmount
  }, []);
  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div key={i} className="stack-card sticky top-0 flex min-h-[100dvh] items-center justify-center">{card}</div>
      ))}
    </div>
  );
}
```
Every card except the last is pinned; card *i* shrinks on card *i+1*'s trigger.

### 5.B Horizontal pan (GSAP, pin/scrub)
```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLElement>(null);
  const track = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const mm = gsap.matchMedia();
    mm.add("(prefers-reduced-motion: no-preference)", () => {
      const distance = () => track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, { x: () => -distance(), ease: "none",
        scrollTrigger: { trigger: wrap.current, start: "top top",   // pin before the first slide moves
          end: () => `+=${distance()}`,                              // scroll length = horizontal travel
          pin: true, scrub: 1, invalidateOnRefresh: true } });
    });
    return () => mm.revert();
  }, []);
  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">{children}</div>
    </section>
  );
}
```

### 5.C Reveal stagger (Motion, no pinning)
For "items appear as they enter", prefer `motion/react` over GSAP: lighter, no ScrollTrigger.
```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li key={item} initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, delay: i * 0.06, ease: [0.16, 1, 0.3, 1] }}>
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

### 5.D Forbidden patterns
- `window.addEventListener("scroll", ...)` and `window.scrollY` in React state: runs every frame, re-renders the tree. Use `useScroll()` from `motion/react`, GSAP ScrollTrigger, `IntersectionObserver`, or CSS scroll-driven animations (`animation-timeline: view()`).
- `requestAnimationFrame` loops that set React state: use motion values.
- Animating `top / left / width / height`: animate `transform` and `opacity` only; `will-change` only on elements that actually animate.
- `layout` / `layoutId` props on static content "for safety": they cost measurement. `staggerChildren` parents and children in the same client tree.
- Grain and noise filters only on a `fixed inset-0 pointer-events-none` layer, never on scrolling containers.

---

## 6. Performance guardrails
- LCP < 2.5s (hero image `priority` or preloaded), INP < 200ms, CLS < 0.1 (reserved space for images, fonts, embeds). Lighthouse is advisory; run it when a URL is available.
- Motion is not tiny and Three.js is large: lazy-load anything below the fold; one heavy library per page section.

---

## 7. App-page and component work
Page-level app UI (settings, onboarding, non-data dashboards): "App page" dials, `DESIGN.md` component tokens, a §2.A system when the brief names one. Dense tables: TanStack Table or AG Grid; editors: Monaco / CodeMirror; multi-step forms: form-library patterns. §4.4 states and §4.9 color scheme apply everywhere; marketing rules (hero, eyebrows, logo walls) do not.

---

## 8. Redesign protocol

### 8.A Detect the mode first
- **Greenfield**: no existing site, or full overhaul approved. Dials from §1.
- **Redesign, preserve**: modernise without breaking the brand. Audit, extract tokens, evolve.
- **Redesign, overhaul**: new visual language over existing content and IA. Greenfield for visuals; content and IA preserved.
If ambiguous, ask once: *"Preserve the existing brand, or start visually from scratch?"*

### 8.B Audit before touching
Scan the codebase (framework, styling method, Tailwind version, component library) and document: brand tokens (colors, type, logo treatment, radii); information architecture (page tree, nav, conversion paths); content blocks (working vs filler); patterns to preserve (signature interactions, copy voice) and to retire (AI tells, broken layouts, dead links, generic stock, perf traps); the existing dial reading (starting point, not baseline); SEO baseline (ranking pages, meta, structured data, OG cards) - SEO migration is the #1 redesign risk. Write the tokens into `DESIGN.md` (create it if missing) before the first CSS change. [redesign.md](./redesign.md) is the concrete grep list.

### 8.C Preservation rules
Keep slugs, anchor IDs, and primary nav labels stable. Extract brand colors before applying §4.2: a brand that is already purple stays purple. Preserve copy voice unless a rewrite was asked for. Do not regress focus states, alt text, keyboard nav, or contrast. Keep button names, form field names and order, and section IDs that analytics depend on. Work with the existing stack: no framework or styling migrations, no new library without checking the dependency file, small reviewable changes, test after each.

### 8.D Fix order (stop when the brief is satisfied)
1. Typography (family, scale, tracking, line length): biggest lift per unit of risk.
2. Color (one accent, unified neutrals, tinted shadows, keep the brand hue).
3. Spacing and layout rhythm (container width, section padding, grid, mobile collapse).
4. States and interaction (hover, active, focus-visible, loading, empty, error, active nav item, no `#` links).
5. Motion layer at the dial level the read allows.
6. Hero and key-section recomposition.
7. Block replacement, only for blocks that are unsalvageable.

### 8.E Targeted evolution vs full redesign
IA, content, and SEO sound → targeted evolution (steps 1-5; ~70% of the value at ~40% of the risk). Structural visual debt (broken IA, no system, broken mobile) → full redesign with strict content preservation. Brand itself changing → greenfield.

### 8.F Never changed silently
URL structure and slugs, primary nav labels, form field names or order, logo or wordmark, legal / consent / cookie copy. Each needs explicit approval.

---

## 9. Scripts
Both are advisory (auto-fix policy: global `code-rules` rule): report findings, ask before changing design or scope because of them.
- `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/frontend-design/scripts/ux_audit.py <path> [--json]`: regex heuristics for typography, color, layout, effects, motion. Anti-default checks (purple palette, hex sprawl, blue-on-food) are warnings; the purple one stays silent when `DESIGN.md` declares purple/violet.
- `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/frontend-design/scripts/accessibility_checker.py <dir>`: a few real source checks on `.html/.jsx/.tsx` (inputs without `id`/`name`/`aria-label`, buttons without text, missing `lang`, missing skip link, `onClick` on non-interactive elements, positive `tabIndex`, unmuted autoplay, `role="button"` without keyboard handling). Few false positives, low coverage; not a substitute for a browser audit.

---

## 10. Pre-flight self-check (advisory to the global gate)
Run before delivering; each box is mechanically checkable. Fix what fails, then deliver. These boxes are the skill's self-check, never the required gate (`code-rules`, `checklist.py`).

- [ ] `DESIGN.md` consistency: fonts, colors, radius, spacing, and color scheme in code match its tokens (or the gate was skipped for a trivial tweak and you said so).
- [ ] Eyebrow count ≤ ceil(sections / 3) (`grep -c "uppercase tracking"` across section components).
- [ ] Zero `—` / `–` in visible strings (`grep -rn "—\|–" src/`).
- [ ] No primary CTA label wraps at 1024px+; one label per CTA intent on the page.
- [ ] Contrast ≥ 4.5:1 (≥ 3:1 for large text) on every button, input, placeholder, and label, in every shipped color scheme.
- [ ] No `h-screen` on full-height sections (`grep -rn "h-screen"`); `min-h-[100dvh]` instead.
- [ ] No `addEventListener('scroll'` / `window.scrollY` in components (`grep -rn "addEventListener(.scroll"`).
- [ ] Every `<img>` / `<Image>` has `alt` (descriptive, or `""` when decorative) and reserved dimensions.
- [ ] Every input has a visible `<label>` (or `aria-label`), error text below it, no placeholder-as-label.
- [ ] Every interactive element has a `focus-visible` style; no `outline-none` without a replacement.
- [ ] Every animation above `MOTION_INTENSITY 3` degrades under reduced motion (`useReducedMotion`, `gsap.matchMedia`, or `@media (prefers-reduced-motion)`) and cleans up on unmount.
- [ ] No `<div>` fake screenshots, hand-rolled SVG illustrations, or text-only pages (real images or labeled placeholder slots; a simple SVG monogram for an invented brand is fine); no component imports both `motion/react` and `gsap`.
