---
part: 12
title: Color systems and contrast
covers: palette, accents, neutrals, semantic tokens, status, themes, images, charts, focus
---

# 12 - Color systems and contrast

Read when selecting or reviewing color. Use the palette and references agreed with the user. No hue is inherently generic, inappropriate, or prohibited; purple, neon, pure black, pastels, earth tones, and monochrome can all be intentional.

## Build roles from the direction

Choose colors for background, surfaces, primary and secondary text, links, actions, focus, borders, status, and decorative expression as the product needs. The number of hues is a composition decision. A single accent can create restraint; several accents can organize categories or create a vibrant identity. Do not impose an accent quota.

Separate semantic roles from raw swatches when reuse or themes justify it. For example, `--color-action`, `--color-action-text`, and `--color-focus` can reference different values. A brand swatch may work in a logo but need a different value for small text or a button background. Record that relationship rather than silently changing the brand everywhere.

Neutrals need deliberate undertones and enough distinction for the chosen layout. Pure black and white are valid. A tinted or off-black surface is also valid. Evaluate eye comfort, contrast, image rendering, and the desired mood rather than prescribing one neutral recipe.

## Contrast and interaction

For a WCAG AA-oriented interface, normal text generally needs at least 4.5:1 contrast and large text at least 3:1. Meaningful control boundaries and graphics generally need 3:1 against adjacent colors, with criterion-specific exceptions. Test actual pairs and states; a token name such as `muted` does not establish contrast. Large text thresholds and exemptions should follow the applicable accessibility standard.

Measure overlays against the lightest or darkest relevant area, including responsive crops, changing slides, scrolling content, and gradient stops. A scrim, stable tinted panel, outline, shadow, repositioned image, or layout change may resolve the issue while preserving the chosen style. Do not automatically strip images and gradients.

Links, hover, pressed, selected, disabled, error, and focus states need clear distinctions. Focus must remain visible across the surfaces where it appears. Do not rely on color alone for a task-critical difference: pair it with text, shape, underline, marker, icon, or position as appropriate. Disabled controls have specific exemptions; do not reuse their low-contrast styling for normal text.

## Status and data

Use consistent status meanings within the domain and culture. Red may mean danger or a brand identity; context and labels disambiguate. Decorative color does not have to be reserved entirely for status. Ensure a colorful page still lets users identify errors and primary actions.

For charts, distinguish series with labels, markers, patterns, or position as well as color. Sequential and diverging scales should reflect the data structure. Category colors should be stable where users compare views. Avoid implying an order from a categorical rainbow when the categories have no ranking.

## Themes and local context

A site may be light, dark, mixed by section, or adaptive according to the brief. A dark hero above light editorial content can be coherent; changing sections does not mean switching the global user theme. Build additional user themes only when requested or required by the product. If a system option exists, respect explicit user preference first and keep states coherent in every supported mode.

Government or school brands may use institutional palettes, but do not infer a required patriotic palette from locality. Preserve legitimate marks and assets. Check brand variants on their real backgrounds rather than recoloring a logo without authorization.

## Review

Inspect the composition, then measure important text, control, and focus pairs in supported states and themes. Check images, overlays, charts, forced colors, and color-only meaning. Fix actual readability or semantic problems; a palette resembling another site is not by itself a defect.
