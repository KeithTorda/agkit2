---
part: 14
title: Composition, layout, and spacing
covers: containers, grids, cards, alignment, rhythm, density, sticky content, scrolling, app shells, hierarchy
---

# 14 - Composition, layout, and spacing

Read when arranging a page or repairing a composition. Follow the agreed style, content, and product purpose. Layout variety is a tool; repetition is also a tool. Neither requires a quota.

## Start with relationships

Identify the main task or story, supporting information, and next action. Group related content with spacing, alignment, contrast, type, surfaces, and position. Use cards when they clarify an independent item or interaction; use open sections when a continuous reading flow works better. Nested cards can be appropriate when they represent meaningful levels, but compare the visual weight of their edges and padding.

Choose a grid from the content. Equal cards suit comparable offerings; asymmetry can establish importance; a list can improve scanning; a full-bleed composition can emphasize imagery. Repeated layouts can create a calm rhythm. Change the arrangement when relationships or narrative pacing change, not because a rule requires every section to be different.

## Width and spacing

Use containers that relate to the content: prose, data tables, galleries, and art-directed heroes need different measures. Align section edges and internal elements intentionally. A shared container is useful; deliberate breakout elements can create emphasis without becoming alignment errors.

A spacing scale helps maintain relationships, but optical adjustments and one-off values are valid. Small gaps should imply closeness; larger gaps should distinguish groups or narrative beats. Dense and spacious designs can both succeed. Remove excessive empty space when it hides the purpose; preserve generous whitespace when it creates the intended pace.

Section padding should adapt to content and viewport. Do not use a fixed page-wide padding limit, force content above an arbitrary fold, or require every section to fill the screen. A full-screen hero can be correct for an immersive launch; a quick lookup tool should surface the lookup promptly. Let audience and purpose decide.

## Sticky, fixed, and scroll behavior

Sticky navigation, fixed CTAs, persistent totals, side notes, and floating controls can help orientation or conversion. Test that they leave enough working space, do not cover content or focus, and adapt to mobile safe areas and onscreen keyboards. Provide appropriate `scroll-margin` or `scroll-padding` for anchors and focus targets.

Use page scrolling for normal documents. Independent scroll regions can serve app shells, tables, sidebars, and panes; make their purpose and boundary clear and keep them keyboard usable. Avoid scroll traps. Do not hide accidental overflow without identifying its source.

## Responsive composition and app shells

Translate the design to each meaningful layout, rather than merely shrinking desktop columns. Decide what stacks, changes order, becomes scrollable, or moves into navigation. DOM reading and keyboard order must remain sensible when visual order changes. Do not delete essential functionality solely because the viewport is narrow.

An app sidebar can be expanded, collapsed, hidden behind a menu, or absent according to the workflow. Ensure the main content can shrink: grid items and flex children may need `min-width: 0`. Persistent headers and footers should respond to content height rather than assuming one fixed label length.

## Review

Inspect the page at its intended presentation size and at constrained widths. Check focal hierarchy, alignment, image scale, text wrap, section rhythm, density, overlapping layers, safe areas, and focus visibility. Use real or representative long content. Distinguish a deliberate overlap or asymmetric edge from a collision that hides information. Correct the latter while preserving the direction.
