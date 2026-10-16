# Marketing layout

Read for landing pages, marketing sites, and portfolios after the intake in [SKILL.md](./SKILL.md). The agreed brief and `DESIGN.md` control the direction; examples here are options.

## 1.B Composition intent
Decide what the page must communicate, which evidence supports it, and what action follows. Sequence sections around that story. A portfolio may need large work samples; a service page may need scope, process, and proof; a product launch may need a concise statement and an honest demonstration. Do not insert sections just to fill a familiar template.

If dials are used, choose them from the approved direction and audience. Marketing does not automatically mean high variance or high motion. A static launch page can be excellent.

## 4.1 Typography
- Choose type for the actual brand character, reading needs, language coverage, availability, and loading cost. Neutral sans, expressive grotesk, serif, and mixed display treatments are all valid.
- Establish a deliberate display/body/label hierarchy with fluid sizes where helpful. Headline line count depends on wording, measure, viewport, and intended composition. A four-line headline is not automatically an error.
- Check real wrapping at narrow, intermediate, and wide sizes. Adjust width, wording, size, and line height together. Preserve descenders, avoid accidental isolated words, and use `text-wrap: balance` when supported and useful.
- Default to a small purposeful font palette. A third mono face may be justified for code or data; it is not required. Record roles so style recipes do not accidentally add families.
- Ensure source and licensing for chosen fonts. Use the existing font pipeline or self-hosted assets when available; do not assume a named commercial typeface can be served.

## 4.2 Color
Build semantic roles for canvas, text, surfaces, action, and state. Single-accent, multicolor, monochrome, high contrast, gradient, warm, and cool palettes can all be coherent. Pick the relationship deliberately and apply it consistently.

Retain real brand colors unless changing them is requested. Do not reject purple, saturated color, pure black/white, or cream because they are common. The failure is an unexplained choice disconnected from the brief, not the hue itself. Check text, controls, and focus against each actual background, including section inversions.

## 4.3 Layout, cards, and shape
- Choose centered, split, asymmetric, image-led, or typographic compositions based on the content and desired focus. A dial does not prohibit a centered hero.
- Use cards for discrete related items, interaction, or surface grouping. Use lists, open grids, rules, and whitespace when those communicate the structure better. Three equal cards are appropriate for three parallel items.
- Reuse layout families where repetition helps scanning and recognition. Vary rhythm when the story changes. No maximum repetitions, minimum number of families, or zigzag quota.
- Radius, elevation, and border systems can vary by component role. Use a clear rule instead of forcing every shape to share one radius.
- Use the project's layer scale for navigation, overlays, dialogs, and decorative media. Keep reading order and focus order intact when compositions overlap.

## 4.5 Hero and page rhythm
The first view should establish what the product/service is, why the audience should care, and the next useful action. Use enough content to make that decision. Concision helps; hard word, line, text-element, or viewport quotas do not.

Fit headline, media, proof, and navigation together as one composition. An intentional oversized or tall hero is valid if the key message is clear and scrolling remains obvious. A compact conversion page may instead keep its action visible immediately. Do not shrink expressive type solely to satisfy a two-line rule.

Use eyebrows, trust strips, side explanations, quotes, pricing, navigation, and footer links when they help the story. Review repetitive decoration as a pattern, not with a per-section count. Navigation may adapt before a named breakpoint if actual labels need it.

Color-blocked or inverted sections are welcome when they create useful emphasis or pacing. Preserve recognizable type, spacing, and color roles, and check each surface's text/controls. A dark section inside a light page is not the same as adding a full dark theme.

## 4.6 Images and product evidence
Choose assets by authenticity, relevance and the agreed art direction. Useful sources include:

1. User-supplied or project-owned brand assets, real product images, screenshots, and photography.
2. Suitable real editorial, stock, or open-license assets from verified sources when sourcing is allowed. Confirm subject, usable rights, crop, quality, and loading behavior; do not use random-image endpoints as finished assets.
3. Generated photography, illustration, texture, or abstract graphics when they suit the approved direction and available tools. Generation is an option, not the first step for every section.
4. If a needed real asset is unavailable, use a clearly identified prototype placeholder or compose the section without the asset. Tell the user what needs replacement.

There is no image quota. Text-led and minimalist pages may use no images; a catalogue may need many. Every asset should improve understanding or expression.

For product UI, prefer real screenshots or a faithful implementation of actual product behavior. A coded static preview or live mini-demo is useful when accurate; identify illustrative/demo content visibly where users could mistake it for current functionality. Never generate a screenshot and present it as evidence that a real feature exists. Avoid invented controls, fabricated customer data, and fake browser chrome that imply a real integration.

Use logos only for real, authorized relationships; an invented prototype brand may use an original mark. Never invent customers to fill a logo wall. Provide descriptive alternatives for meaningful images, empty alternatives for decoration, reserved dimensions, responsive crops, and appropriate loading priority. Prioritize the actual above-the-fold/LCP media where useful; avoid eager-loading the whole asset collection or preloading an asset that does not help initial rendering.

## 4.7 Copy and proof
Headlines should make a clear, specific claim; body copy provides the detail needed for the task. Prefer readable sections over arbitrary word limits. Longer specifications, comparison tables, and substantive lists are appropriate when the audience needs them; organize them with headings and navigation rather than deleting useful facts.

Testimonials, awards, pricing, availability, numerical claims, and customer names must come from the brief or a verified source. For a prototype, visibly label illustrative content where it could be confused with real evidence. A hidden source comment is not a disclosure. Match the requested language, locale, punctuation, and brand voice.

## 4.8 Critique a draft
Inspect the rendered page and ask:

- Does the first view communicate the actual offering and next action?
- Are visual emphasis and content order intentional, with strong alignment and typography?
- Do assets belong to this brand and subject? Is product evidence honest?
- Do repeated components help scanning, and do section changes help the story?
- Does the selected style survive on mobile without clipping, overflow, or unreadable overlays?
- Are key links and actions usable, with meaningful loading/error states where relevant?

Fix demonstrated weaknesses. Do not mechanically remove gradients, serif words, centered heroes, FAQ accordions, pricing columns, footers, or animation solely because they are familiar patterns.
