# Style: Minimalist / Editorial (warm monochrome)

Variant of [SKILL.md](./SKILL.md). Applies only when the brief chooses this style ("Notion-like", "document-style", "warm minimalism", "editorial workspace") or `DESIGN.md` names it. Everything in SKILL.md still applies; this file adds the style's specifics and lists the places where it deliberately deviates. If `DESIGN.md` exists, its tokens win over the values below.

## Explicit exceptions to SKILL.md
| Deviation | Reason |
|---|---|
| Serif display for hero headings and pull quotes, sans for everything else (SKILL.md §4.1 serif discipline) | The editorial/document aesthetic is the brief; the pairing is the style's signature. Record the pairing in `DESIGN.md`. |
| Card surfaces may be pure `#FFFFFF` on an off-white canvas (SKILL.md §4.2 "no pure white") | The near-white step between canvas and card is the only elevation device in an ultra-flat system. The canvas itself is never pure white. |
| Pastel accent chips carry several hues (SKILL.md §4.2 "one accent") | They are semantic tags (status, category), not brand accents. The brand accent is still one color, used for the single primary action. |
| Accordion FAQ is the default here (SKILL.md §4.8 discouraged default) | Stripped, divider-only accordions are native to the document aesthetic. |

Everything else (eyebrow cap, hero rules, image strategy, copy rules, em-dash rule, color-scheme rule, pre-flight) is unchanged.

## Dials
`DESIGN_VARIANCE 5`, `MOTION_INTENSITY 3`, `VISUAL_DENSITY 3` unless the design read says otherwise.

## Typography
- Sans (body, UI, buttons): `Geist Sans`, `Switzer`, or `Helvetica Neue`, falling back to `system-ui`. Do not name Apple system fonts (`SF Pro`) in `font-family`; they are not web-hostable.
- Serif (hero headings, quotes only): `Newsreader`, `Lyon Text`, `Source Serif 4`. Tracking `-0.02em` to `-0.04em`, line-height `1.1`. Never for body or UI.
- Mono (code, keystrokes, metadata): `Geist Mono`, `JetBrains Mono`.
- Text colors: body `#111111` or `#2F3437` at `line-height: 1.6`; secondary `#6B6A67` (the lighter `#787774` the style is known for fails AA on this canvas; use it only at 18px+). Never `#000000`.
- Weights: 400 body, 500 UI, 600 headings. Sentence case; wide-tracked uppercase only on the few eyebrows the cap allows.

## Color (warm monochrome + spot pastels)
- Canvas: `#FBFBFA` or `#F7F6F3`. Card surface: `#FFFFFF` or `#F9F9F8`.
- Borders and dividers: `#EAEAEA` or `rgba(0,0,0,0.06)`, always 1px.
- Primary action: solid `#111111` with `#FFFFFF` text (hover `#333333`).
- Semantic pastels (chips, inline code, icon tiles): pale red `#FDEBEC` / `#9F2F2D`, pale blue `#E1F3FE` / `#1F6C9F`, pale green `#EDF3EC` / `#346538`, pale yellow `#FBF3DB` / `#956400`.
- Dark scheme, when `DESIGN.md` asks for both: canvas `#191919`, surface `#202020`, border `rgba(255,255,255,0.08)`, body `#E6E6E4`, secondary `#9B9A97`; pastels drop to 12% tints of the same hues.
- No gradients, no neon, no large colored sections, no glass beyond a subtle nav blur, no Tailwind `shadow-md`/`lg`/`xl`; shadows are `0 2px 8px rgba(0,0,0,0.04)` at most.

## Shape and spacing
- Radius scale: `4-6px` buttons and inputs, `8-12px` cards, `9999px` only for small chips and tags. No pill primary buttons, no pill containers.
- Sections `py-24` to `py-32`; typographic content `max-w-4xl` / `max-w-5xl`; cards padded `24-40px`.
- Bento feature grids: asymmetric CSS Grid, `1px solid #EAEAEA` cell borders, ≤ 12px radius, cell count equal to content count (SKILL.md §4.5).

## Components
- Chips and status tags: `text-xs`, pill, `letter-spacing: 0.05em`, pastel background from the list above.
- Accordion: no container boxes; items separated by `border-bottom: 1px solid #EAEAEA`; `+` / `-` toggle glyphs.
- Keystrokes: `<kbd>` with `1px solid #EAEAEA`, `4px` radius, `#F7F6F3` background, mono font.
- Software previews: a real screenshot or generated image (SKILL.md §4.6). A thin `1px #EAEAEA` frame with `8px` radius may wrap a real image; no fake window chrome, no traffic-light dots, no UI built from divs.

## Icons and imagery
- Phosphor (Bold or Fill) or Radix Icons for the slightly heavier stroke this style wants; one family, one weight.
- Illustrations: monochrome continuous-line ink sketches with a single pastel-filled geometric shape.
- Photography: desaturated, warm-toned, with a `0.04` warm grain overlay; picsum seeds when real assets are missing. Backgrounds get depth from low-opacity imagery, a warm radial light spot at `opacity 0.03`, or a minimal line pattern; never a flat empty section.

## Motion (quiet)
- Scroll entry: `translateY(12px)` + `opacity 0` → resolved over `600ms` with `cubic-bezier(0.16, 1, 0.3, 1)`, via `motion/react` `whileInView` or `IntersectionObserver`.
- Hover: card shadow `0 0 0` → `0 2px 8px rgba(0,0,0,0.04)` over `200ms`; buttons `scale(0.98)` on `:active`.
- Stagger: `animation-delay: calc(var(--index) * 80ms)` on lists and grids.
- Optional ambient: one slow radial blob (`20s+`, `opacity 0.02-0.04`) on a `fixed pointer-events-none` layer behind the hero.
- `transform` / `opacity` only; reduced-motion fallback per SKILL.md §5.

## Build order
1. Macro whitespace and container widths first.
2. Type hierarchy and color variables (from `DESIGN.md`) next.
3. Borders and dividers: every one is `1px #EAEAEA`.
4. Imagery and depth per section.
5. Scroll-entry motion last.
