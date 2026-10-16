---
part: 11
title: CSS treatment and reliable rendering
covers: shadows, radius, gradients, filters, motion, layout, stacking, sizing, focus, tokens, framework classes
---

# 11 - CSS treatment and reliable rendering

Read while implementing CSS or utility classes. Translate the chosen direction into stable behavior. CSS properties are tools, not an aesthetic banlist.

## Surfaces and materials

Shadows can convey elevation, tactile detail, or intentional glow. Define reusable values when the treatment repeats; choose their strength from the direction and surface context. Borders, tint, and shadow may work together. Check that they produce the intended hierarchy rather than adding a competing edge around everything.

Use square, rounded, pill, or irregular corners as the design calls for them. For nested rounded boxes, compare inner and outer curvature visually; an inner radius related to padding is a useful starting point, not an inflexible formula. Clipping media should not clip keyboard focus or important content.

Gradients, `background-clip: text`, masks, noise, blend modes, blur, and colored shadows are valid. Test actual contrast, rendering support, and cost. Gradient text needs a readable text-color fallback. Glass needs a tint that remains legible without backdrop blur. Sophisticated effects should degrade to a useful composition when unavailable.

## Interaction and motion

Choose transition properties explicitly where unintended animation could occur. `transition: all` is not a proof of failure, but can animate future layout changes unexpectedly. Match duration and easing to distance, purpose, and the chosen motion language. Hover lift or scale is fine when it fits the interaction, leaves room, and does not imply a nonexistent action. Pair hover with focus and touch behavior.

Animating transform and opacity is often efficient; profiling decides whether a specific filter, shadow, clip, or paint-heavy animation is acceptable. Use reduced-motion alternatives and do not hide essential content indefinitely if an observer or animation library fails.

## Layout and sizing

Use grid, flexbox, intrinsic sizing, or positioned elements according to the problem. Absolute positioning is useful for deliberate overlap and art direction; avoid relying on it for text flows that need to rewrap. Let content determine heights where text may grow.

Use responsive units and `clamp()` when useful, but ensure text still scales with user preferences. `100vh`, `svh`, and `dvh` have different browser behavior; choose and test the one appropriate for a full-height composition. A full-screen hero is legitimate if it serves the brief and its important content remains reachable. Do not conceal accidental page overflow with a global `overflow-x: hidden` before finding its source.

## Stacking, specificity, and state

Use a documented layer system where overlays interact. A large z-index alone is not wrong; diagnose stacking contexts, transforms, isolation, and clipping. Platform top-layer dialogs and popovers can simplify the problem. Check fixed elements against safe areas, keyboards, zoom, and focused content.

Prefer maintainable selectors and scoped variants. Inline styles are appropriate for dynamic values; utility arbitrary values can encode intentional art direction. Promote repeated decisions into tokens, but do not force every one-off value into a global system. `!important` has legitimate uses in third-party overrides and utilities; repeated override fights usually need a clearer cascade.

## Tokens and framework integration

Use names that express actual roles: surface, text, accent, focus, border, elevation, radius, spacing, and any chosen glass or glow treatment. Theme values should derive from the agreed palette. There is no ban on `--gradient-hero` or `--shadow-glow` when those are part of the design.

Tailwind, Bootstrap, CSS Modules, vanilla CSS, and CSS-in-JS can all work. Respect the installed version and project conventions. Avoid duplicate resets, unused demo styles, accidental global overrides, and version-mismatched classes. Keep a visible focus indicator and usable selection; never remove those merely to match a screenshot.

## Review

Inspect wrapping, overflow, clipping, focus, state changes, and rendering fallbacks in the changed components. Review a property because of an observed or credible effect, not because its name matches a forbidden-pattern search.
