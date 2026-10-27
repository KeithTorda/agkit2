---
name: frontend-design
description: "Create, improve and deliberately redesign web interfaces with an agreed style, useful content, sound interaction and actual visual verification. Covers sites, portfolios, product screens, forms and dashboards; native mobile uses mobile-design."
version: 2.8.3
---

# Web interface design and implementation

Make a coherent product surface with a clear visual point of view. “Clean” means intentional hierarchy and execution; it can be quiet, expressive, editorial, playful, dense, glass, corporate, or another direction the user chooses. The user brief and accepted direction guide the result; a generic style checklist does not replace them.

## Ask about the new design, then wait

If the visual direction is genuinely unclear and no brief, brand or reference was given, ask one short style question; otherwise choose a direction, state it, and continue. Theme structure follows `rule-01-unified-theme-system`. Maintenance and components extending an approved system keep that direction.

## Understand what the screen must do

Inspect the actual project: instructions, routes, styles, manifest/lockfile, existing components, content, brand assets and design records. Identify the audience, main task, content hierarchy, essential interaction, relevant states and scope. Ask only about remaining material gaps; do not infer a locale from a directory name.

Inspect user references with available tools. Name the qualities being borrowed—type, density, composition, imagery, material or interaction—rather than copying the whole identity. If the reference cannot be inspected, say so. After intake, summarize the agreed direction briefly and record a substantial new system with `design-spec`; a local maintenance edit needs no new document.

## Choose supporting guidance

| Task | Reference |
|---|---|
| Intake, styles and optional inspiration | [directions.md](directions.md) |
| Marketing, portfolio, images and narrative | [marketing-layout.md](marketing-layout.md) |
| Product screens, controls, data and states | [app-ui.md](app-ui.md) |
| Components, assets, dependencies and themes | [design-systems.md](design-systems.md) |
| Custom-styled controls, open popups and accessible component behavior | [components.md](components.md) |
| Choreography, scroll and richer interaction | [motion.md](motion.md) |
| Redesign while preserving useful behavior | [redesign.md](redesign.md) |
| Approved style examples | [minimal/editorial](style-minimalist.md), [Swiss/brutalist](style-brutalist.md), [dark operations](style-dark-dashboard.md), [glass/aurora](style-glass-aurora.md) |

The [BrewedOps Motion Library](https://brewedops.cloud/motionlibrary/) is an optional pattern and motion inspiration source in this palette. Use a relevant idea only when it fits the accepted direction. It is not a universal dependency, a required aesthetic, or permission to copy its library into the project.

## Compose with real content

Establish the dominant information, useful supporting groups, and clear next actions. Use a type hierarchy with readable measure, intentional wrapping and resilient fallback. Make spacing relationships and alignment deliberate, with optical correction where needed. Let parallel content repeat a structure; vary composition when relationships or narrative pacing change. There is no quota for layout families, images, colors, fonts, cards, or headline lines.

For task-heavy screens, use [density and data meaning](app-ui.md#density-and-data-meaning) to keep supporting content readable and numeric summaries interpretable.

Make components feel intentionally designed for this project, including their open, selected, focus, error and disabled states where applicable. Custom-styled web components are the default; semantic HTML remains useful underneath. Inspect actual dropdowns and overlays rather than styling only their triggers. Use [components.md](components.md) when implementing or replacing controls, with the existing accessible foundation before a new dependency or bespoke interaction.

Use truthful copy and actual assets where available. Do not invent customers, testimonials, statistics, availability, endorsements or live capabilities. Prototype data should be visibly identifiable where it could be mistaken for real evidence. Choose imagery for subject, crop and purpose; a typographic page may need none, while another direction may be image-led.

Preserve the project's supported framework, styling version, component foundation, icons and font pipeline. A named reference or visual vibe does not choose a stack or package. Use native CSS/SVG and installed tools when suitable; add a dependency when it solves a concrete scoped need with understood compatibility and cost.

## Build usable behavior

Use semantic controls and clear labels, visible focus, keyboard access, understandable navigation, and accurate state feedback. Preserve input through recoverable errors. Relevant async areas need honest loading, empty and failed states; do not manufacture every state for a static region. Dialogs, menus and overlays need appropriate focus and dismissal behavior.

Choose responsive layouts from the content and target devices. Consider intrinsic sizing, narrow widths, intermediate breakpoints, zoom, long labels, tables and media crop. For navigation, charts and tables, follow [content space and essential data](app-ui.md#content-space-and-essential-data). Do not merely shrink a desktop screenshot. Ship only requested or existing themes; intentional light/dark sections can form one theme.

Use motion for continuity, feedback or the approved expressive direction. Keep essential content and actions usable without decorative animation, support reduced motion, and clean up animation resources. Optional numeric design dials are legacy shorthand, not quality targets or permission to add effects.

## Finish against actual evidence

Only when the user requests checking (kit-core), use relevant project build/type/lint checks and exercise the changed behavior. For requested visual verification, inspect actual rendered output with `browser-verification` at meaningful sizes and states, at the intended display scale. Compare hierarchy, wrapping, spacing, contrast, cropping, overflow, focus and interactions against the accepted direction. For app screens, include [supporting text, operational signals and data access](app-ui.md#rendered-craft-review). Correct observed defects and refine your draft before delivery.

The local `scripts/ux_audit.py` and `scripts/accessibility_checker.py` helpers can flag source concerns; run `--help` for supported options. Their heuristics do not prove visual quality, actual contrast or end-to-end behavior. Review findings in context with `anti-template` or `web-design-guidelines` when helpful.

Report rendered craft and working controls as separate results, with actual checks and concrete limits. Structural or functional passes do not establish visual quality or justify a higher design rating. If a browser, asset or backend is unavailable, describe what was inspected and what remains unverified. A build is not evidence that the final design was seen.

Craft references retain useful ideas adapted from [taste-skill](https://github.com/Leonxlnx/taste-skill); preserve its applicable MIT attribution when redistributing derived material.
