# Design conversation and reference palette

Before every new visual design or intentional redesign, ask one short question covering style and references, then wait. Adapt naturally to the user's language and project:

> Para sa app na ito, anong style ang gusto mo at may site o screenshot ka bang reference? Puwede mo ring sabihin na ako ang pumili.

Explicit existing answers, “no reference”, and delegation to choose satisfy intake. Silence does not. A small repair or a component matching an approved system does not reopen it. Existing `DESIGN.md` is useful context when asking about an intentional redesign. Inspect code, assets and constraints while waiting, without inventing the new look.

## Help with meaningful options

When the user wants ideas, describe a few distinct directions through purpose, hierarchy, typography, composition, imagery, materials and motion. Give a recommendation tied to their audience/content. Do not force a menu, a numeric dial, a reference count, or a stereotyped industry look. Mixed directions are valid when the relationships remain coherent.

| Possible direction | Qualities to develop | Execution to watch |
|---|---|---|
| Quiet/editorial | Type hierarchy, rhythm, tactile surfaces, purposeful imagery | Empty composition or weak emphasis |
| Expressive magazine | Columns, captions, image-led narrative, contrast in scale | Narrow-screen reading order and long text |
| Swiss/brutalist | Grid, rules, strong type, deliberate asymmetry | Small metadata, clipped display type, excess competing emphasis |
| Dark operations | Surface hierarchy, useful density, semantic status | Muted contrast, color-only meaning, glowing noise |
| Glass/aurora | Translucency, atmospheric depth, color fields | Real-backdrop contrast, blur cost, solid fallback |
| Playful/graphic | Illustration, character, color blocking, tactile feedback | Understandable controls and optional motion |
| Bold/media-led | Full-bleed assets, confident type, memorable transitions | Competing focal points, asset weight, blocked scroll |
| Civic/professional | Trustworthy content, clear tasks, brand continuity | Institutional stereotypes and interchangeable copy |
| Commerce | Product focus, price/availability hierarchy, useful filtering | Promotion obscuring purchase and invented urgency |

## Optional resources

Use the user's actual reference first. The kit's style examples and `design-spec/collection.md` offer starting points when helpful. The [BrewedOps Motion Library](https://brewedops.cloud/motionlibrary/) is now an explicit option for interface/motion inspiration and selected code patterns. It includes self-contained HTML examples and prompts across categories such as heroes, dashboards, login views, mobile layouts and 3D/GSAP treatments. Categories and availability can change; inspect the relevant current example rather than hardcoding a catalog count.

Ask which quality matters only if it is unclear. A pattern can inspire timing or layering without imposing its colors, layout, framework, package or full animation intensity. Follow [motion.md](motion.md) for implementation, reduced motion, performance and pattern-adoption boundaries. Offering this resource does not trigger another style question after intake is answered.
