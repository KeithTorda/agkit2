---
part: 21
title: Overlays and asynchronous feedback
covers: dialogs, confirmations, drawers, popovers, tooltips, toasts, alerts, loading, optimistic updates
---

# 21 - Overlays and asynchronous feedback

Read when an interface opens a temporary layer or reports asynchronous state. Materials, radius, blur, transitions, and placement follow the chosen direction; interaction needs determine modality and persistence.

## Choose the container

Use inline content when the message belongs to a field or section, a banner for a broader condition, a toast for secondary feedback, and a dialog when a focused decision or task warrants interruption. A drawer or sheet can preserve page context. Do not convert every update into a modal or ban modals because they are familiar.

## Modal behavior

Use a tested dialog primitive or native `<dialog>` with `showModal()` where appropriate. A modal needs an accessible name, sensible initial focus, background interaction containment, keyboard operation, and focus restoration. Native behavior still needs testing in the supported environment.

Escape and a visible close/cancel action should normally dismiss a noncritical modal. Unsaved or irreversible operations may need specific handling that explains the consequence. Do not silently lose entered data. Backdrop dismissal can be useful, but should not be the only close method or accidentally discard a long form.

Choose initial focus from content: a heading may suit an informational dialog, a field may suit a short form, and a safe action may suit a destructive confirmation. Long dialogs need scrolling that keeps controls reachable on small screens and with the keyboard open. Do not trap focus inside nonmodal content.

## Drawers, popovers, and tooltips

A drawer may be modal or nonmodal; implement the chosen behavior consistently. Hidden layers should not remain focusable. Popovers and dropdowns need meaningful trigger state, correct stacking, escape behavior, and keyboard conventions for their actual pattern. A list of navigation links is not automatically an ARIA menu.

Tooltips supplement an understandable label, not replace essential instructions. They should work on focus as well as hover, be dismissible as appropriate, and not disappear while the user moves into relevant hover content. Touch users need an available alternative for important information.

## Toasts, alerts, and announcements

Communicate the operation and outcome without taking focus for routine feedback. Use polite status announcements for ordinary changes and assertive alerts only where immediate interruption matters. Avoid duplicate announcements from overlapping live regions.

Duration and persistence should match importance, reading effort, and actions. Errors requiring recovery and toasts with important actions need enough time and a persistent path; a short success toast may disappear. Pause a timed notification on hover/focus when appropriate and avoid unbounded stacks. No fixed toast-count or timeout rule fits every product.

An undo action needs a real reversal path, correct expiry, and conflict handling. Do not tell the user a change was undone if the server rejected the reversal. Partial failures need a useful explanation and targeted retry.

## Loading and optimistic updates

Use a spinner for unknown progress, a progress bar for measured progress, and skeletons when they meaningfully preserve a known layout. Consider delaying a loading indicator for very short operations to avoid flashing, based on actual latency. Do not invent percentages or fake waits to showcase an animation.

Preserve useful previous content during refetching when it remains accurate enough, and show freshness where relevant. Optimistic changes need rollback and error recovery. High-impact operations such as payments should not appear final before authoritative confirmation.

## Review

Test open, close, Escape, keyboard order, focus return, nested-layer behavior where supported, small-screen scrolling, timeouts, and failure recovery. Check overlays on the actual chosen background, including contrast and reduced-motion behavior.
