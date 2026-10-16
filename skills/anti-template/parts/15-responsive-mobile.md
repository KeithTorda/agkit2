---
part: 15
title: Responsive and mobile behavior
covers: breakpoints, viewport testing, touch, menus, overflow, height units, tables, safe areas, input zoom, slow networks
---

# 15 - Responsive and mobile behavior

Read when a design must adapt across viewports or input methods. Preserve the chosen character at each size. A mobile layout can have its own composition; it does not have to become a generic stack of identical cards.

## Breakpoints from content

Use the existing system's breakpoints when suitable, and introduce a breakpoint when content or interaction needs it. Device names alone do not define the behavior. Resize continuously around layout changes to catch in-between failures. Representative small phone, wider phone, tablet, and desktop views are useful, but do not treat a fixed list as proof that every width works.

Test important small-screen constraints, including reflow around 320 CSS px where the applicable accessibility target calls for it. Browser zoom and increased text size can create a constrained viewport even on a desktop. Table and map exceptions do not excuse page-wide horizontal overflow.

## Touch and alternative input

Controls need reachable, adequately spaced hit areas. A roughly 44 CSS px touch target is a useful ergonomic goal; applicable WCAG target-size rules have their own minimums and exceptions. Do not confuse the visible icon size with its clickable area. Give destructive adjacent actions sufficient separation for the actual layout.

Hover may enhance a desktop experience but must not be the only way to discover required content or actions. Menus, cards, tooltips, drag handles, swipe gestures, and long-press actions need keyboard and touch alternatives. Keep active and focus states distinct from hover.

## Overflow, height, and safe areas

Find the cause of horizontal overflow: unbreakable text, wide media, minimum widths, transformed elements, negative margins, or grid children. Use intentional scroll containers for data that benefits from comparison. Do not globally hide overflow merely to conceal a bug.

Choose `vh`, `svh`, or `dvh` according to whether the composition should react to browser chrome. Full-height layouts need testing with the address bar and onscreen keyboard. Use content-driven minimum heights when labels or text can grow. Fixed controls should respect `env(safe-area-inset-*)` where needed and avoid covering focused fields.

## Navigation, overlays, and tables

Mobile navigation should open and close reliably, show its state, and preserve the user's location. A modal menu or drawer needs focus management, Escape behavior, appropriate background interaction, and scroll handling. Avoid leaving offscreen menu links focusable when closed.

For tables, choose horizontal scroll, prioritized columns, detail expansion, or a dedicated mobile view from actual comparison needs. Converting every row to a card may lose useful column relationships. Preserve filters, selection, totals, and row actions when they are required. A scroll hint can help when overflow is intentional.

## Text, inputs, images, and performance

Use readable type and allow zoom. Avoid disabling pinch zoom to suppress iOS focus zoom; inspect input font sizing and layout instead. Preserve autocomplete and appropriate input modes. Test long names and translated text, not only a short English example.

Provide image sizes, responsive sources, and intentional focal crops. Important artwork need not disappear on mobile; recompose it if it carries the direction. Optimize actual transfer and decoding costs, especially for the user's priority networks and devices. Do not remove all visual richness merely because a region may have slow connections.

## Review

Inspect visible output and key interactions in an actual browser when available. Test menu, form, overlays, scrolling, orientation where relevant, keyboard opening, and zoom. Report a missing device check honestly instead of replacing it with "checked mentally."
