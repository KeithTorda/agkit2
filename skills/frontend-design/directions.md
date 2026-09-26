# Directions and the style menu (frontend-design §0.D)

Read when: starting a new page or app and the brief leaves the look open. Core SKILL.md first (§0.B signals, §0.C design read). `DESIGN.md` or a named direction from the user skips this file: build what was asked.

## Offering 2-3 directions

One message, before any code. Each direction must be something you would be glad to build, and the set must be genuinely different: change at least two of palette logic, type, layout structure and effects between them. Three shades of the same clean SaaS page is one direction.

```markdown
Design read: <page kind>, <audience>, <device>.

**A. <Name>** (recommended) - <one line of feel>.
References: <Product> (<what you borrow>), <Product> (<what you borrow>).
Palette: <logic, not hex: "deep green ink on warm paper, one saffron accent">. Type: <display + body>.
Signature move: <the one thing people will remember>. Dials: V<n> M<n> D<n>.

**B. <Name>** - ...
**C. <Name>** - ...

I will build A unless you pick another. <At most 2 other blocking questions, each with a default.>
```

- Recommend the one that best fits the audience, not the one that is safest.
- A civic or trust-first brief still gets range: for example civic-official, warm community, and bold public-information poster.
- A playful or premium brief should include at least one direction that uses effects (gradient, glass, glow, motion) well.
- After the choice, write it into `DESIGN.md` (`design-spec`), including the effects that are in and out.
- If the user says "just build it", pick the recommendation and state the design read in one line.

## The style menu

Starting points, not templates. Each can be quiet or loud; the dials and references decide. Hex values anywhere in the style files are labelled examples; `DESIGN.md` tokens replace them.

| Direction | Feels like | Fits | Signature moves | Watch |
|---|---|---|---|---|
| Minimal / warm editorial (`style-minimalist.md`) | Notion, Linear docs, a good book | Tools, studios, writing, SaaS for calm users | Serif display + sans body, hairline dividers, generous space | Can go empty; needs real imagery and one strong accent |
| Editorial / magazine | Guardian, NYT, a print annual | News, publications, portfolios, cultural orgs, long reads | Strong type scale, columns, big pull quotes, image-led spreads | Measure (60-75 ch), heading hierarchy, image rights |
| Brutalist / Swiss (`style-brutalist.md`) | Machinery manuals, terminals, poster design | Studios, dev tools, telemetry, art projects | Heavy grotesk, visible grid, mono data, zero radius | Contrast of accent colours at small sizes |
| Dark dashboard (`style-dark-dashboard.md`) | Grafana, trading and ops consoles | Monitoring, POS back office, admin used in low light | Bright text on deep surfaces, luminous status badges, dense tables | Colour must carry state; keep the palette small |
| Glass / aurora (`style-glass-aurora.md`) | visionOS, premium consumer apps, music/event sites | Consumer products, launches, events, portfolios, AI products | Layered translucent panels, aurora or mesh gradients, soft glow | Text contrast over moving backgrounds, blur cost on phones |
| Playful / expressive | Duolingo, Headspace, Gumroad | Consumer apps, kids and education, community, food | Chunky shapes, bright palette, illustrated moments, bouncy motion | Keep controls conventional; reduced-motion fallbacks |
| Bold / maximal | Agency sites, fashion drops, Awwwards pages | Brands, launches, creative portfolios | Oversized type, colour blocking, full-bleed media, scroll storytelling | Performance, one focal point per view still applies |
| Government / civic | GOV.UK, USWDS, Singpass, Service NSW | LGU, barangay, school, COMELEC, public services | Plain language, one task per page, large targets, official identity (seal, colours) | Low bandwidth, old phones, print; decoration must not slow the task |
| Corporate / professional | Stripe marketing, Deloitte, bank sites | B2B services, firms, cooperatives, enterprise | Measured grid, confident photography, restrained accent, clear proof | Stock-photo blandness; give it one distinctive element |
| Retail / marketplace | Shopee, Lazada, Shopify Dawn | Stores, catalogues, promos in PH/SEA | Dense product cards, price and badge hierarchy, promotional rails | Density is expected here; keep it scannable |

Short recipes for the directions without their own file:

- **Editorial**: display serif or high-contrast grotesk at 3-4 sizes, body at 18-20 px, 12-column grid with deliberate asymmetry, images at real aspect ratios with captions, section rules instead of cards. Motion minimal.
- **Playful**: rounded radius scale (12-24 px), 2-3 saturated brand colours on a light or tinted base, a custom illustration or icon style, springy motion on feedback (press, success), friendly but still specific copy. Contrast checks on every coloured surface.
- **Bold / maximal**: one oversized type moment per section, colour blocks or full-bleed media, scroll-driven reveals (motion.md), a strict underlying grid so the loudness reads as intent.
- **Government / civic**: official colours and seal from the agency's identity, public-service type (for example Public Sans, Source Sans, Noto Sans), announcement lists with dates, a prominent lookup or search, bilingual labels where the audience needs them (`anti-template` part 09). Modern and well-crafted is allowed; noise is not.
- **Corporate**: 12-column grid, one accent, photography of real people and places, proof near claims (client logos, numbers with sources), calm motion. One distinctive element (a type choice, a colour, an illustration style) keeps it from reading as stock.
- **Retail**: product image first, price second, badges third; filters as a first-class surface; sticky cart; promotional banners allowed but capped per view.
