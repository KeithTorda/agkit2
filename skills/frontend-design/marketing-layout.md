# Marketing layout (frontend-design §1.B, §4.1-§4.3, §4.5-§4.6, marketing §4.7-§4.8)

Read when: building a landing page, marketing site, portfolio, or any page-level marketing UI. SKILL.md core comes first (§0 design read, §1 dials, §4.0 judgment gate everything here). `DESIGN.md` tokens win over every value below.

## 1.B Dial presets
| Use case | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Landing, SaaS mainstream | 7 | 6 | 4 |
| Landing, agency / creative | 9 | 8 | 3 |
| Landing, premium consumer | 7 | 6 | 3 |
| Portfolio, designer / studio | 8 | 7 | 3 |
| Portfolio, developer | 6 | 5 | 4 |
| Editorial / blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |

App page (dashboard-like) is a row of the inference table (SKILL.md §1.A).

## 4.1 Typography
- Display `text-4xl md:text-6xl tracking-tighter leading-none`; body `text-base leading-relaxed max-w-[65ch]`.
- Sans per `DESIGN.md`. Without one, prefer a face with character (Geist, Satoshi, Cabinet Grotesk, Outfit). Inter is an anti-default: fine when the brief asks for a neutral / Linear-style / public-sector feel.
- Serif only when the brand names one or the aesthetic is genuinely editorial / luxury / publication / heritage, and you can say why this serif fits; "creative brief = serif" is the most-tested AI tell (Fraunces / Instrument Serif are anti-defaults for it). A deliberate serif-display + sans-body pairing is fine in those cases; document it in `DESIGN.md`.
- Emphasis inside a headline: italic or bold of the same family, not a serif word dropped into a sans headline.
- Italic display words with `y g j p q` need `leading-[1.1]` minimum plus `pb-1`, or the descender clips.
- Data numbers: `tabular-nums` or mono. `text-wrap: balance` on headlines, `text-wrap: pretty` on body.

## 4.2 Color
- One accent, saturation under 80% by default, on a neutral base (zinc / slate / stone), the same accent across the whole page (no blue CTA in section 7 of a rose-accented site). Do not mix warm and cool grays in one project.
- Purple / violet primaries are an anti-default (SKILL.md §0.E). When the brand or `DESIGN.md` asks for purple, embrace it with a consistent palette and restrained gradients.
- **Premium-consumer trap:** cookware, wellness, artisan, luxury, and DTC home-goods briefs pull the same "warm cream + brass/clay/oxblood + espresso" palette every time. Use it only when the brand names those colors or is vintage-craft; else pick another family on purpose (silver/chrome, forest + bone + amber, off-black + tan, cobalt + cream, terracotta + slate, monochrome + one saturated pop).
- Shadows tinted to the background hue; no pure-black drop shadows on light backgrounds. No pure `#000000` or `#ffffff` surfaces; off-black and off-white keep depth.

## 4.3 Layout, cards, shape
- Centered hero is avoided at `DESIGN_VARIANCE > 4`: 50/50 split, left content / right asset, or asymmetric whitespace. Centered is right for editorial / manifesto / launch briefs where the message is the design.
- Cards only where elevation communicates hierarchy; otherwise group with `border-t`, `divide-y`, or space. At `VISUAL_DENSITY > 7` no generic card containers.
- Three equal feature cards are an anti-default: prefer a 2-col split, asymmetric grid, bento, or horizontal scroll; three cards are fine when the content is genuinely three parallel items.
- **Radius**: one scale from `DESIGN.md` `rounded` (all-sharp, all-soft 12-16px, or all-pill for interactive); mixed radii only under a documented rule ("buttons pill, cards 16px, inputs 8px") applied everywhere.
- Z-index only for systemic layers (sticky nav, modal, overlay, grain), documented in one constants file; no arbitrary `z-50`.

## 4.5 Layout rules
Fix these before delivering; each is mechanically checkable.
- **Hero fits the first viewport**: headline ≤ 2 lines, subtext ≤ 20 words and ≤ 4 lines, CTAs visible without scrolling. Plan font scale and asset size together: `text-4xl md:text-5xl lg:text-6xl` for most heroes, `text-7xl` only for 3-5-word headlines; a 4-line headline is a font-size error. Top padding ≤ `pt-24` at desktop.
- **Hero stack ≤ 4 text elements**: eyebrow or brand strip (or neither), headline, subtext, CTAs (1 primary + ≤ 1 secondary). Taglines under CTAs, trust strips, pricing teasers, feature bullets, avatar rows, and the logo wall get their own sections below the hero.
- **Navigation** on one line at `lg`, height ≤ 80px (default 64-72): condense, drop, or hamburger.
- **Eyebrows** (small uppercase tracked labels above headlines): at most 1 per 3 sections, hero counts as one; count > ceil(sections / 3) fails (`grep -c "uppercase tracking"` across section components). Dropping the eyebrow is the default fix; the headline is enough.
- **Split-header** (big headline left, small explainer floating right) is an anti-default; stack headline over body (`max-w-[65ch]`) unless the right column carries a visual or interactive element.
- **Bento grids** have exactly as many cells as content items (3 items → 1+2 or 2+1, never a blank tile) and real variation in at least 2-3 cells (image, brand gradient, pattern, tint).
- **Layout-family repetition**: a family (3-col cards, full-width quote, split text/image) appears at most once per page; an 8-section page uses at least 4 families; image/text zigzag at most 2 sections in a row.
- **Section theme lock**: sections do not invert the page's color scheme mid-scroll (SKILL.md §4.9).

## 4.6 Images and visual assets
Landing pages and portfolios are visual products; text-only pages with fake-screenshot divs are slop.
1. **Image-generation tool first.** If any image tool is available, generate section-specific assets (hero, product shot, texture, mood) at the section's aspect ratio.
2. **Real photography second.** `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}`, brand or stock URLs from the brief, open-license sources when allowed.
3. **Last resort: labeled placeholder slots** (`<!-- TODO: hero product photo, 1600x1200 -->`) plus a closing line listing what the page needs. Never fill the gap with hand-rolled SVG illustrations or div-built "screenshots".

- Even minimalist sites need 2-3 real images (hero, one product or lifestyle shot, one supporting image).
- Logo walls: real SVG marks (`https://cdn.simpleicons.org/{slug}/{hex}`, `simple-icons`, devicon for tech stacks); invented brands get a simple inline SVG monogram. Logos only, no category labels, both color schemes covered.
- Product previews: real screenshot, generated image, or live mini-component; never a dashboard, task list, or terminal made of `<div>`s.
- Every meaningful image has descriptive `alt`, decorative images `alt=""`; hero image `priority` / preloaded; every image has reserved dimensions.

## 4.7 Marketing copy (the marketing half of SKILL.md §4.7)
The app-UI string rules, banned words, dash rule, and copy self-audit in SKILL.md §4.7 apply here too.
- Per section: headline ≤ 8 words, sub-paragraph ≤ 25 words, one visual or one CTA. Cut the rest.
- No data-dump sections on marketing pages (20-row tables, 30-row award lists): top 3-5 + "View all", or another page. Lists over 5 items get a real component (2-col groups, card grid, tabs, scroll-snap pills, one marquee), not a longer `<ul>` with a hairline under every row. Spec sheets: grouped chunks, featured-vs-rest disclosure, or a 2-col spec card grid.
- Quotes ≤ 3 lines, attribution name + role (+ company), typographic quotes or none.
- Numbers are real (brief, brand, public data) or labeled mock (`<!-- mock -->`); no invented precision (`5.8 mm`, `4.1×`) and no round fakes (`99.99%`, `50%`).
- Names, brands, avatars: locale-appropriate, specific, non-repeating; no "John Doe", "Acme", "Nexus", egg avatars, or the same face twice.

## 4.8 Marketing AI tells (the marketing half of SKILL.md §4.8)
Avoid unless the brief asks. App-UI tells and the shadcn/ui rule: SKILL.md §4.8.
- Visual: neon outer glows, gradient text on large headers, oversaturated accents, custom cursors, crosshair or hairline grid lines as decoration, decorative status dots (real state only, one per section), `·` as universal separator (max one per line).
- Labels: version labels (`V0.6`, `BETA`) unless the brief is a launch; section-number eyebrows (`001 · Capabilities`); `01 / 4` tile pagination; scroll cues; hero-bottom strips (`DESIGN · BUILD · SHIP`); floating top-right sub-text in section headers; locale / time / weather strips unless the brand is place-based.
- Copy: "Quietly trusted by", "Field notes"-style poetic labels, "Stage 1 / Stage 2" (use the verb-noun), micro-meta sentences under headings, mock-humble asides, photo-credit captions on stock images, tags overlaid on photos, fake version footers (`v1.4.2`, "last sync 4s ago").
- Layout: `border-t` and `border-b` on every row; filled-track progress bars as comparison visuals; `<br>`-split italic headlines; vertical rotated text; H1s that scream by size alone.
- Components (discouraged defaults, not bans): accordion FAQ, three-tower pricing, dotted testimonial carousel, sun/moon toggle, 4-column footer link farm, filled-plus-ghost button pair. Fine when the content shape fits (ten questions is an accordion); the tell is reaching for them unexamined.
