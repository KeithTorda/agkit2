---
name: frontend-design
description: Designing and building web UI with taste and range - landing pages, marketing sites, portfolios, app screens, dashboards, redesigns. Direction comes from the brief, the audience, named references and DESIGN.md; offers 2-3 distinct directions when the brief is open. Use for any web UI design, build or design review; not for mobile (mobile-design) or DESIGN.md authoring (design-spec).
version: 2.5.0
---

# Frontend Design

Good UI here means: it fits the people who use it, it has a point of view, and it is built with craft (type, spacing, states, motion, accessibility). It does not mean one safe look. A barangay portal, a streetwear drop, a POS till and a crypto dashboard should not come out the same.

Where the direction comes from, in order: the user's explicit request → `DESIGN.md` → the brief and its audience → named references → this skill's defaults. Everything below §0 is a default you can override with a reason; say the reason in one line.

Firm, whatever the style: accessibility (`design-rules` 4, `anti-template` part 27) and honest, hype-free system copy (§4.7). Every glossy effect has an accessible way to build it; find that way instead of refusing the effect.

| File | Read when |
|---|---|
| directions.md | New page or app with an open brief: offering 2-3 directions, and the style menu (editorial, civic, corporate, playful, bold, and the rest) |
| style-minimalist.md | The chosen direction is warm minimal / editorial workspace |
| style-brutalist.md | The chosen direction is Swiss-industrial or terminal/telemetry |
| style-dark-dashboard.md | The chosen direction is a high-contrast dark dashboard (bright text, luminous status badges) |
| style-glass-aurora.md | The chosen direction uses glass, aurora or mesh gradients, glow |
| app-ui.md (§4.4, §5.E, §7) | Any app screen: dashboard, settings, form, table, POS, admin |
| marketing-layout.md (§1.B, §4.1-§4.3, §4.5-§4.8) | Landing page, marketing site, portfolio |
| motion.md (§5, §5.A-§5.D) | `MOTION_INTENSITY` 6 or more, or the brief asks for scroll, pinned or animated sections |
| design-systems.md (§2, §3, §4.9) | The brief names a design system, choosing fonts or icons, light/dark setup |
| redesign.md (§8) | The site or app already exists |
| `KIT/skills/design-spec/collection.md` | Picking named references, by audience and domain |
| `KIT/skills/anti-template/SKILL.md` | Checking a draft for template defaults (parts 10-14 for visuals) |

Adapted in part from [taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT).

## 0. Before building

### 0.A DESIGN.md
- A project `DESIGN.md` wins over everything in this skill: colours, type, spacing, radii, colour scheme, style direction, and which effects are in or out. Build to its tokens; if a request conflicts with it, say so in one line and follow the user.
- New app or new page-level UI without one: write a short one with `design-spec` after the direction is chosen. Existing project without one: infer the tokens from the current CSS and match them. Bug fixes and small tweaks never need one.
- Tokens flow one way: `DESIGN.md` → Tailwind v4 `@theme` (`tailwind-patterns` §2) or `:root` custom properties (`css-architecture`). No second token list.

### 0.B Read the signals
1. **Page kind**: landing (SaaS, consumer, agency, event), portfolio, app screen, editorial, redesign (preserve or overhaul).
2. **Vibe words** the user used ("clean", "Linear-style", "premium", "brutalist", "futuristic", "friendly", "official").
3. **References**: URLs, screenshots, named products, competitors. These beat anything you would pick.
4. **Audience**: who uses it, on what device, in what state of mind (a resident on a cheap Android phone, a cashier mid-shift, a procurement panel, a gamer).
5. **Brand assets**: logo, colours, type, photography. Starting material, especially on a redesign.
6. **Quiet constraints**: accessibility-critical, public sector, regulated, low bandwidth, kids. These narrow the range; they do not remove taste.

### 0.C The design read (one line)
Before code, name the page kind, audience, direction, and 1-2 shipped products it should sit next to with the one thing you borrow from each (grid, type treatment, nav, density, colour logic):
*"<page kind>, <audience>. <Direction>. <Product> (<what you borrow>), <Product> (<what you borrow>)."*
- Pick references from `design-spec/collection.md` in the section for this **audience and domain**, not the aesthetic you know best. A civic portal sits next to public-service products; a POS next to retail tools; a developer-product reference belongs on a developer product.
- The user's own references always win. Name a product outside the collection when it fits better.
- Adjectives and dials constrain; a named reference gives you something to aim at. It is the single biggest lever against generic output.

### 0.D Open brief: offer directions. Clear brief: declare and go.
- **Open brief** (new page or app, no `DESIGN.md`, no references, vibe words vague or absent): offer **2-3 distinct directions** in one message before building. Each gets a name, one line of feel, the references, palette logic, type pairing, and the signature move. Make them genuinely different (for example an editorial one, a bold expressive one, a calm civic one), recommend one, and say you will build the recommendation if they do not choose. Format and the style menu: `directions.md`.
- **Clear brief** (direction named, references given, `DESIGN.md` exists, or it is a component inside an existing design): state the design read and build. No questions.
- Design questions share the `core-protocol` budget: one message, at most 3 questions total.

### 0.E Defaults to question (not bans)
Each of these shows up when nobody made a choice. Ask the question; if the answer is yes, use it and build it well.

| Default | Ask | Fine when |
|---|---|---|
| Purple/indigo/violet primary | Did anyone choose this colour? | The brand is purple, or the direction calls for it |
| Inter / system sans everywhere | Does the type carry any character for this brand? | Neutral is the point: public sector, dense app UI, Linear-style tools |
| Glass / frosted panels | Is there something behind it worth seeing, and does text stay readable? | Photo- or video-led heroes, media overlays, premium consumer, a glass/aurora direction (`style-glass-aurora.md`) |
| Gradients (backgrounds, text, borders) | Does the gradient belong to the brand or just fill space? | Brand gradient, aurora or mesh direction, a single hero statement, playful/consumer |
| Glow, neon, luminous accents | Does glow mean something (live, selected, status) or is it decoration? | Dark dashboards (`style-dark-dashboard.md`), gaming, music, nightlife, crypto, event sites |
| Pure white / pure black | Is the contrast step deliberate? | High-contrast dark dashboards, brutalist print, accessibility-first; many good systems use them |
| Hero + three equal feature cards + CTA | Is the content really three parallel items? | It is; otherwise split, bento, list or story |
| Centred hero over a dark mesh | Is the message itself the design? | Launch, manifesto, event; otherwise try split or asymmetric |
| Animation on every card | What does each animation tell the user? | Playful or agency directions at high `MOTION_INTENSITY`, done with reduced-motion fallbacks |
| shadcn/ui default look | Did you change radii, colour, type, shadows? | Always fine as a foundation; ship it restyled |
| Dark "developer" aesthetic | Are the users engineers? | Developer tools, technical products, or the client asks for it |

The tell is usually the combination (indigo + glass + gradient text + three cards + hype headline), not any single element. Deeper lists: `anti-template` parts 10-14.

### 0.F Screen read (for page-level or new UI)
Five lines on what the screen must do, before layout:
1. **Job**: what the user accomplishes here, one sentence.
2. **Entry and exit**: where they come from, what they know on arrival, where success takes them.
3. **Primary action**: one; at most one secondary; the rest demoted.
4. **First seen**: the one fact they need to decide, where the eye lands first.
5. **States and their words**: loading, empty, error, long content, no permission; write the real sentence for each (§4.7).
Inputs: the PRD or `/proplan` screens (`ux-architect`), or stated assumptions.

## 1. The three dials
Set after the design read; they tune layout, motion and density. `DESIGN_VARIANCE` (1 symmetric, 10 art-directed), `MOTION_INTENSITY` (1 static, 10 cinematic), `VISUAL_DENSITY` (1 gallery, 10 cockpit). Presets: marketing-layout.md §1.B. Write them in `DESIGN.md` `## Overview`.

### 1.A Dial inference
| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| minimalist / calm / editorial / Linear-style | 5-6 | 3-4 | 2-3 |
| premium consumer / luxury / brand | 7-8 | 5-7 | 3-4 |
| playful / agency / Awwwards / experimental | 9-10 | 8-10 | 3-4 |
| glass / aurora / futuristic consumer | 7-8 | 6-8 | 3-4 |
| landing / portfolio / marketing (default) | 7-9 | 6-8 | 3-5 |
| public sector / trust-first / accessibility-critical | 3-4 | 2-3 | 4-5 |
| corporate / B2B services | 4-5 | 3-4 | 4-5 |
| app screen / dashboard / POS | 3-4 | 2-3 | 6-8 |
| redesign, preserve | match existing | +1 | match |
| redesign, overhaul | +2 | +2 | match |

### 1.C What the levels mean
- **VARIANCE** 1-3: symmetric 12-column grid, centred. 4-7: overlaps (`-mt-8`), mixed aspect ratios, left-aligned headers over centred data. 8-10: masonry, fractional grids (`grid-cols-[2fr_1fr_1fr]`), large empty zones. At 4-10 every asymmetric layout collapses to one column below `md`.
- **MOTION** 1-3: hover and active states only. 4-7: `transform`/`opacity` transitions, staggered entry. 8-10: scroll-driven reveals, parallax, pinned sections (`motion/react`, GSAP ScrollTrigger, CSS `animation-timeline`), never a raw `scroll` listener (motion.md §5.D).
- **DENSITY** 1-3: `py-32` to `py-48` section gaps. 4-7: `py-16` to `py-24`. 8-10: tight padding, 1px rules instead of cards, mono `tabular-nums` numbers.

## 2-3. Systems and stack
design-systems.md: §2.A real design systems (official package, one per project), §2.B aesthetics without a package, §3 stack defaults (the project's stack wins; baseline in `code-rules`).

## 4. Craft

### 4.0 Design judgment (considered vs templated)
The bar for every direction, from minimal to maximal:
- **One focal point per view.** One element wins the eye first (headline, primary action, the number that matters). Squint test: if two tie, demote one. Everything loud means nothing is.
- **A real type scale.** 4-6 sizes off one ratio (about 1.2-1.333), not ad-hoc px; neighbouring levels read as distinct. Weight is cheaper hierarchy than size: one family, 2-3 weights, a second family only with a reason.
- **One spacing rhythm.** Every gap is a step on the spacing scale. Related things closer than unrelated; section gaps larger than in-section gaps. A gap whose step you cannot name is probably wrong.
- **A coherent kit.** One accent logic, one radius scale, one shadow or elevation language, one motion vocabulary. Maximal directions are still systems: the gradient, glow or texture repeats by rule, not per section.
- **Effects serve the focal point.** Gradients, glass, glow and texture are strongest when they frame one thing; spread evenly over every card they flatten the page. Whitespace and contrast still do most of the work.

### 4.4 / 5.E / 7 App UI
app-ui.md: §4.4 states and forms, §5.E feedback on action, §7 app-page hierarchy. Read it for any non-marketing screen.

### 4.7 Content and copy (all visible strings)
Words are part of the design. Honest copy is firm; tone can range from formal to playful per the brand.
- **Errors**: what happened, then what to do ("Card declined. Try another card."). No bare "Something went wrong", no "Oops".
- **Empty states**: name what is missing and the action that creates it.
- **Buttons**: verb + object ("Save changes", "Download receipt"). A destructive confirmation names the object ("Delete *Q3 report*?").
- **Placeholders**: example values ("name@company.com"), never the label; the label stays visible.
- No hype words or fake excitement in system text (`anti-template` parts 01-04). Marketing headlines can be bold; they still say something true and specific.
- One voice per page, sentence-case headings by default, no lorem ipsum in delivered work.
- Dashes: the kit default is no em-dash or en-dash in visible copy (use a period, comma, colon or hyphen). Follow the brand's style guide if it says otherwise.
- Re-read every visible string before delivering; rewrite anything vague, broken or cute-but-wrong.

### 4.8 App-UI tells (question them)
Marketing tells: marketing-layout.md §4.8.
- A 4-up stat-tile row on every dashboard, sidebar + grid of identical cards, "Welcome back, {name}" as the header, a chart in every card regardless of data shape. Lead with what the user checks first.
- shadcn/ui: a fine foundation; ship it restyled to `DESIGN.md`.

### 4.9 Colour scheme (light / dark)
design-systems.md §4.9: ship what `DESIGN.md` or the brief says; one switching mechanism; both modes keep AA contrast.

## 5. Motion
Motion should mean something: hierarchy, story, feedback, state change, or brand personality in an expressive direction. At `MOTION_INTENSITY` above 4 the page actually moves (hero entry, reveals on key sections, hover physics on CTAs); at 3 or below it is a clean static page with good feedback states. Always: `transform`/`opacity`, reduced-motion fallback, cleanup on unmount. Recipes and pitfalls: motion.md.

## 6. Performance guardrails
- LCP under 2.5 s (hero image preloaded or `priority`), INP under 200 ms, CLS under 0.1 (reserved space for images, fonts, embeds).
- Blur, large gradients and video are paid for on low-end phones: limit `backdrop-filter` to a few elements, compress media, lazy-load heavy libraries below the fold, one heavy library per section. PH audiences are often on mid-range Android over mobile data.

## 8. Redesign
Existing site: redesign.md before the first CSS change (mode, audit, preservation, fix order).

## 9. Scripts (advisory)
Report findings; ask before changing design or scope. Run from `KIT/skills/frontend-design/scripts/`:
- `python "KIT/skills/frontend-design/scripts/ux_audit.py" <path> [--json] [--fail-on error|warning|never]`: warnings are real usability problems (low contrast in a rule, removed focus outline, small controls or text, skipped headings, no reduced-motion handling); style guidance is info, never a failure, and is suppressed when `DESIGN.md` asks for that style. No errors, so exit 1 only with `--fail-on warning`.
- `python "KIT/skills/frontend-design/scripts/accessibility_checker.py" <path> [--json] [--fail-on ...]`: source checks with `file:line`; errors (missing `alt`, label, accessible name, `lang`, zoom disabled) exit 1 by default. Not a browser audit: rendered contrast and focus order need `playwright_runner.py --a11y` or Lighthouse.

## 10. Self-check before delivering (advisory)
Verification depth follows the `code-rules` tier; this list is for your own eye.
- [ ] The design read names the direction and 1-2 references (§0.C); an open brief got 2-3 directions (§0.D).
- [ ] The page matches `DESIGN.md` tokens, or the tokens were inferred and stated.
- [ ] One focal point per view (§4.0); the type and spacing steps are nameable.
- [ ] Every flagged default in use has a reason (§0.E).
- [ ] Every state (loading, empty, error, long, no permission) has its sentence (§0.F, §4.7).
- [ ] Contrast, focus, labels, keyboard and reduced motion hold, including over gradients, glass and images.
- [ ] Works at 390 px and 1440 px. When a dev server is running and the layout changed, look at it with `/see`.
