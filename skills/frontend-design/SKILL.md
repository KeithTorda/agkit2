---
name: frontend-design
description: Web UI that does not look templated (landing pages, marketing sites, portfolios, app UI, redesigns). Core - DESIGN.md gate, reads, dials, judgment, copy, app-UI tells, pre-flight. Sub-files - app-ui, marketing-layout, motion, design-systems, redesign, style-*. Use for any web UI design, build, or review. Not for mobile (mobile-design) or DESIGN.md authoring (design-spec).
version: 2.1.0
---

# Frontend Design

Not for mobile apps (`mobile-design`), dense data tables, code editors, realtime-collab surfaces: say so, apply what fits. §1-§8 are contextual defaults: override when brief, brand, or `DESIGN.md` says otherwise, and say so. §10 is the self-check; the required gate is the global `code-rules` rule. Read this file first; section numbers are stable across files.

| File | Read when |
|---|---|
| app-ui.md (§4.4, §5.E, §7) | Building or fixing an app page: dashboard, settings, form, table, any non-marketing screen |
| marketing-layout.md (§1.B, §4.1-§4.3, §4.5-§4.6, marketing §4.7-§4.8) | Landing page, marketing site, portfolio, page-level marketing UI |
| motion.md (§5, §5.A-§5.D) | `MOTION_INTENSITY` ≥ 6, or the brief asks for scroll, pinned, or animated sections |
| design-systems.md (§2, §3, §4.9) | Brief names a design system, fonts/icons for a new project, or light/dark setup |
| redesign.md (§8, audit checklist) | The site or app already exists |
| style-minimalist.md | Clean, warm-monochrome, editorial minimalism |
| style-brutalist.md | Raw Swiss-industrial or terminal/telemetry |
| `../design-spec/collection.md` (70+ shipped products) | Every design read (§0.C): the named reference |

Adapted from [taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT).

## 0. Before anything: DESIGN.md, then the design read

### 0.A The DESIGN.md gate
Follow the global `design-rules` rule (applies / infer / skip), never restate it.
- `DESIGN.md` tokens win over everything here (fonts, colors, radius, spacing, color scheme, components); heuristics fill only its gaps. Code matches its tokens at delivery, or say the gate was skipped (trivial tweak).
- No `DESIGN.md` on a new app or page-level UI: author it with `design-spec` first.
- Tokens flow one way, `DESIGN.md` YAML → Tailwind v4 `@theme` (`tailwind-patterns` §2; `npx @google/design.md export --format css-tailwind` writes it); no second token list in `tailwind.config.js` or components.

### 0.B Read the signals
1. **Page kind**: landing (SaaS / consumer / agency / event), portfolio, app page, editorial, redesign (preserve vs overhaul).
2. **Vibe words** used ("minimalist", "Linear-style", "Awwwards", "brutalist", "premium", "dark tech").
3. **References**: URLs, screenshots, named products, competitors.
4. **Audience** (procurement panel, consumer, recruiter, citizen) picks the aesthetic, not your taste.
5. **Brand assets** (logo, colors, type, photography): starting material on a redesign (§8).
6. **Quiet constraints** (accessibility-first, public sector, regulated, trust-first commerce, kids) override aesthetic preference.

### 0.C State the design read in one line
Before code, name page kind, audience, vibe, **and 1-2 shipped products this should sit next to, with the one thing you borrow from each** (grid, type treatment, nav, density, color logic). From `design-spec/collection.md` or your own knowledge; the user's references win. Example: *"B2B SaaS landing, technical buyers. Linear (type scale), Vercel (section rhythm)."* Adjectives and dials constrain; only a named reference gives you something to aim at. A read without one is not a read, and the largest cause of generic output.

### 0.D One question, or none
Design questions count toward the global `core-protocol` budget: at most one, in the same message as planning questions, never a second round ("Linear-clean or Awwwards-experimental?"). If you can infer the direction, declare the read and proceed.

### 0.E Anti-defaults, not bans
Purple/violet primaries, Inter, shadcn/ui, glassmorphism, three equal cards, a centered hero over a dark mesh, micro-animations on every card: never unexamined. Use them when brief, brand, or `DESIGN.md` asks; note the reason in one line.

### 0.F Screen read (UX, before layout)
For any page-level or net-new UI, five lines before §1 (what it must do, not how it looks):
1. **Job**: what the user accomplishes here, one sentence.
2. **Entry and exit**: where they arrive from, what they know on arrival, the next screen on success.
3. **Primary action**: exactly one; at most one secondary; all else demoted.
4. **First-seen**: the one fact they need to decide, where the eye lands first.
5. **States and their words**: loading, empty, error, long content, permission-denied; write the actual sentence for each (§4.7), not "show an error".
Inputs: the PRD's *Screens and flows* (`product-manager`, `docs/`) or stated assumptions. A screen you cannot describe this way is not ready to lay out.

## 1. The three dials
Set after the design read; they gate layout, motion, density. Baseline `8 / 6 / 4`, the read overrides. Exact names, never aliases: `DESIGN_VARIANCE` (1 symmetry, 10 artsy chaos), `MOTION_INTENSITY` (1 static, 10 cinematic), `VISUAL_DENSITY` (1 art gallery, 10 cockpit). Presets: marketing-layout.md §1.B.

### 1.A Dial inference
| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| minimalist / clean / calm / editorial / Linear-style | 5-6 | 3-4 | 2-3 |
| premium consumer / Apple-y / luxury / brand | 7-8 | 5-7 | 3-4 |
| playful / Dribbble / Awwwards / experimental / agency | 9-10 | 8-10 | 3-4 |
| landing / portfolio / marketing (default) | 7-9 | 6-8 | 3-5 |
| trust-first / public sector / regulated / accessibility-critical | 3-4 | 2-3 | 4-5 |
| app page (dashboard-like) | 3-4 | 2-3 | 6-8 |
| redesign, preserve | match existing | +1 | match |
| redesign, overhaul | +2 | +2 | match |

### 1.C What the levels mean
- **VARIANCE** 1-3: symmetrical 12-col grid, centered. 4-7: `-mt-8` overlaps, mixed aspect ratios, left-aligned headers over centered data. 8-10: masonry, fractional grids (`grid-cols-[2fr_1fr_1fr]`), large empty zones. At 4-10 every asymmetric layout collapses to one column below `md`.
- **MOTION** 1-3: `:hover` / `:active` only. 4-7: `transform` / `opacity` transitions, `animation-delay` cascades. 8-10: scroll-driven reveals, parallax, pinned sections (`motion/react`, GSAP ScrollTrigger, CSS `animation-timeline`); never a `scroll` listener (motion.md §5.D).
- **DENSITY** 1-3: `py-32` to `py-48` gaps. 4-7: `py-16` to `py-24`. 8-10: tight padding, 1px rules instead of cards, mono `tabular-nums` numbers.

## 2-3. Systems and stack
design-systems.md: §2.A real systems (official package, one per project), §2.B aesthetics without a package, §3 stack (Next.js 16 App Router, React 19, TypeScript, Tailwind v4, `motion/react`).

## 4. Design directives

### 4.0 Design judgment (considered vs templated)
The bar for every design; §4.1-§4.9 apply it in code (§4.1-§4.3, §4.5-§4.6: marketing-layout.md).
- **One focal point per view.** One element wins the eye first (hero line, primary CTA, the number that matters); the rest subordinate in size, weight, or color. Grayscale-and-squint test: two tie, demote one. Everything bold means nothing is.
- **A real type scale.** 4-6 sizes off one ratio (~1.2-1.333), never ad-hoc px; neighbors read as distinct levels (2px apart reads as a bug). Weight is cheaper hierarchy than size: one family, 2-3 weights; past ~6 sizes or ~3 weights the scale is drifting.
- **One spacing rhythm.** Every gap is a step on the `DESIGN.md` spacing scale, never a one-off `p-[13px]`. Proximity is grouping: related closer than unrelated, section gaps larger than in-section gaps. A gap whose step you cannot name is wrong.
- **Restraint everywhere.** One accent, one type family (two with a reason), one radius scale, one shadow language, one motion vocabulary. Reuse one small kit, not a new color/weight/radius per section; a new element is an exception you justify.
- **Contrast and whitespace do the work.** Emphasis from size, weight, color, space; not stacked borders, boxes, glows, gradients. Whitespace is the cheapest signal of hierarchy and quality; a cramped "premium" layout is a contradiction. Space before a card or divider; motion communicates or goes (§5).

### 4.7 Content and copy (all visible strings)
Words are part of the design, owned by whoever builds the screen; marketing copy: marketing-layout.md §4.7.
- **Errors**: what happened, then what to do ("Card declined. Try another card."); no error codes, no "Oops", no "Something went wrong" without a next step.
- **Empty states**: name the missing thing and the action that creates it, never "No data" or "Nothing here".
- **Buttons**: verb + object ("Save changes"), never "Submit", "OK", "Yes"; a destructive confirmation repeats the object's name and its button is the verb ("Delete *Q3 report*?").
- **Placeholders**: example values ("name@company.com"), never the label or an instruction; the label stays visible above.
- One voice per page, concrete verbs, sentence-case headings, active voice, no lorem ipsum; no "Elevate", "Seamless", "Unleash", "Next-Gen", "Delve", "Oops!", no exclamation marks in system messages.
- **Dashes**: no em-dash (`—`) or en-dash (`–`) in any visible copy, alt text included; use period, comma, colon, parentheses, or hyphen (`2018-2026`).
- **Copy self-audit** before shipping: re-read every visible string; rewrite anything grammatically broken, referent-less, cute-but-wrong, or performatively thoughtful. Plain beats clever.

### 4.8 AI tells (avoid unless the brief asks)
Marketing tells (visual, labels, copy, layout, components): marketing-layout.md §4.8.
- App UI: a 4-up stat-tile row on every dashboard, sidebar + grid of identical cards, "Welcome back, {name}" headers, gradient-circle avatars, a chart in every card regardless of data shape, an avatar column for no reason. Lead with what the user checks first.
- shadcn/ui: a fine foundation, never in its default look (adjust radii, colors, shadows, type).

### 4.9 Color scheme (light / dark)
design-systems.md §4.9: schemes shipped, one mechanism, page theme lock, both modes AA.

## 5. Motion
Motivated or absent: name what each animation communicates (hierarchy, storytelling, feedback, state change) or drop it. At `MOTION_INTENSITY > 4` the page actually moves (hero entry, reveals on key sections, hover physics on CTAs); no scope for working motion means dial 3 and a clean static page. Loops, springs, pointer physics, one library per component, reduced motion, recipes, forbidden patterns: motion.md §5.

## 6. Performance guardrails
- LCP < 2.5s (hero image `priority` or preloaded), INP < 200ms, CLS < 0.1 (reserved space for images, fonts, embeds). Lighthouse is advisory; run it when a URL exists.
- Motion is not tiny, Three.js is large: lazy-load below the fold; one heavy library per section.

## 4.4 / 5.E / 7 - App UI
app-ui.md: §4.4 states and forms, §5.E feedback on action, §7 app-page work and hierarchy.
Read it for any non-marketing screen; §0.F, §4.0, §4.7, §4.8 apply too.

## 8. Redesign
Existing site: redesign.md §8 before the first CSS change (mode, audit, preservation, fix order).

## 9. Scripts
Advisory (global `code-rules` auto-fix policy): report, ask before changing design or scope. In `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/skills/frontend-design/scripts/`, run with `python`.
- `ux_audit.py <path> [--json]`: regex heuristics for typography, color, layout, effects, motion; anti-default hits are warnings, purple silent when `DESIGN.md` declares it.
- `accessibility_checker.py <dir>`: a few source checks on `.html/.jsx/.tsx` (labels, button text, `lang`, skip link, keyboard, autoplay); low coverage, not a browser audit.

## 10. Pre-flight self-check (advisory)
The six boxes most likely to fail; fix, then deliver. Not the required gate (`code-rules`, `checklist.py`).
- [ ] Design read names 1-2 shipped references and what each lends (§0.C).
- [ ] Screen read exists for every page-level or net-new UI (§0.F).
- [ ] One focal point per view; grayscale and squint, nothing ties (§4.0).
- [ ] No anti-default unexamined; each in use has its reason (§0.E).
- [ ] Every state (loading, empty, error, long, denied) has its sentence in the code (§0.F.5, §4.7).
- [ ] Zero `—` / `–` in visible strings (`grep -rn "—\|–" src/`) (§4.7).
