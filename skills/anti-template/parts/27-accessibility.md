---
part: 27
title: Accessible behavior and content
covers: semantics, keyboard, focus, dialogs, labels, live regions, contrast, targets, motion, zoom, language, tables, media, verification
---

# 27 - Accessible behavior and content

Read while building or reviewing interaction, content, and visual treatments. Accessibility supports the chosen style: glass, rich color, expressive type, and motion can be implemented accessibly. Determine the project's actual target; WCAG 2.2 AA is a useful general web target, not a blanket claim of legal compliance.

## Semantics and keyboard

Use native links for navigation and buttons for actions, with explicit button types in forms. Avoid nested interactive elements. A custom widget needs an appropriate name, role, state, keyboard behavior, and focus handling; prefer a proven primitive when it solves that contract. ARIA does not add missing behavior.

Keep a sensible DOM order and avoid positive tabindex. A hidden or `aria-hidden` region must not contain reachable controls. Use `inert` or appropriate hidden state for inactive layers. Every essential action needs keyboard access; drag, swipe, long press, hover, and pointer-only canvas interaction need usable alternatives. Single-character shortcuts require appropriate disable/remap/modifier handling.

Use landmarks and meaningful headings. One visible main region and a clear page heading aid orientation. Name multiple navigation regions and provide a working skip link where repeated content otherwise burdens navigation. Avoid choosing heading levels solely for font size. Accessible names should include visible label text so voice-control users can target controls.

## Focus and overlays

Keep a visible focus indicator across all supported surfaces. Do not remove an outline without an effective replacement. Box shadows can disappear in forced colors; a real outline or suitable forced-color fallback helps. Check clipping and sticky/fixed elements that may obscure the focused control.

Modal dialogs need a name, appropriate initial focus, focus containment, background interaction control, close behavior, and focus restoration. Native dialog or a tested component can provide much of this, but verify actual behavior. Nonmodal panels should not trap focus. After deleting a focused row or changing a route, move or announce focus sensibly. Routine toasts should not steal it.

## Forms and announcements

Connect persistent labels, hints, and errors. Expose required/invalid states and provide text errors, not only red borders. On submit failure, focus a linked error summary or the first relevant invalid field. Group related choices with a useful legend. Allow paste, password managers, autofill, and accessible authentication. Avoid collecting the same information repeatedly without need.

Use polite status regions for ordinary asynchronous updates and assertive alerts only for genuinely urgent interruptions. Avoid announcing a changing timer, character, or animation frame repeatedly. An existing empty live region often gives more reliable announcements than creating the region and message together. Do not duplicate a label with redundant ARIA.

## Contrast, color, and targets

For an AA target, normal text generally needs 4.5:1 and large text 3:1 contrast. Meaningful UI boundaries and graphics generally need 3:1 against adjacent colors, subject to the actual criterion and exceptions. Test actual colors and states. Overlaid text must pass across its relevant backdrops and crops; maintain a chosen gradient or image with an effective treatment rather than deleting it by reflex.

Do not convey essential information through color alone. Labels, patterns, shapes, underlines, icons, or position can supplement it. Links in text need adequate differentiation. Check forced colors and supported themes.

WCAG 2.2 AA target-size criteria generally use 24 by 24 CSS px or applicable spacing/other exceptions. A larger area around 44 px is often a useful touch goal; it is not a universal AA minimum. Dense inline links have specific exceptions. Test real target spacing and separation, especially near destructive actions.

## Motion, timing, zoom, and language

Respect reduced-motion preferences with usable settled or alternative states. Automatically moving content needs pause/stop/hide controls when the applicable criteria require them. Avoid unsafe flashing; do not assume an effect is safe without considering flash area and thresholds. Time limits need warning, adjustment, or an applicable exception. Toast actions should remain reachable or have a persistent alternative.

Allow zoom. Test text enlargement, spacing changes, and reflow around 320 CSS px or equivalent zoom where the criterion applies. Fixed heights must not clip expanded text. Data tables and maps may need deliberate two-dimensional views, while surrounding content still reflows.

Set correct page language and language changes for substantive blocks. Use language names in a language picker rather than relying on flags.

## Tables, images, and media

Use table headers, scope or associations, an accessible purpose/caption, sort state, and labeled selection controls. A custom grid needs its full keyboard and screen reader contract. Scroll regions should be reachable when users need to interact with them.

Images need meaningful alt text or empty alt for decoration. Meaningful SVGs need a name; decorative duplicates should be hidden. Complex diagrams require equivalent information beyond a short alt. Provide captions and transcripts for relevant media and appropriate description of essential visual information. An image or scanned PDF must not be the sole accessible route to essential instructions.

## Verification

Use proportionate automated checks plus manual keyboard, focus, zoom/reflow, contrast, and assistive-technology checks for relevant changes. Automated tools cannot establish complete accessibility. Inspect supported dialog, form, menu, and dynamic states. Report the checks actually performed and limitations; never claim compliance from a score alone.
