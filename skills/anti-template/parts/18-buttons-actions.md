---
part: 18
title: Actions and controls
covers: hierarchy, styling, targets, icons, loading, disabled states, destructive actions, bulk actions, floating controls, feedback
---

# 18 - Actions and controls

Read when designing buttons, links, action groups, and row controls. The chosen aesthetic can use gradients, glow, shadows, pills, hard edges, animation, or plain controls. Judge whether the action remains recognizable and usable.

## Hierarchy and semantics

Make the main next action evident, with secondary and destructive actions distinguishable. More than one equally important action can exist in a complex workspace; do not enforce a fixed count. Establish priority through placement, label, contrast, grouping, and treatment rather than reflexively coloring every button differently.

Use `<button>` for an action and `<a href>` for navigation. Set button type explicitly in forms. Do not nest interactive elements. A whole-card link with secondary controls needs independent targets and a predictable reading/focus order.

## Labels, icons, and hit areas

Labels should describe the actual result in context. Short text is often useful, but a longer label is better than an ambiguous action. Icons can reinforce recognition or carry the action in a dense tool; icon-only controls require an accessible name, adequate hit area, and understandable discoverability. A tooltip helps sighted keyboard users, but essential instructions should remain available without hovering.

Use consistent icon meaning and scale. Decorative icons within an already labeled control should be hidden from assistive technology. Size the clickable area separately from the visual glyph. Test adequate touch area, spacing, long translations, zoom, and destructive action proximity. See part 27 for target-size criteria.

## State and feedback

- Hover and pressed states should feel related to the chosen treatment. Focus must remain visible independently of hover.
- While submitting, show meaningful progress and prevent accidental duplicate effects. Preserve button dimensions where a spinner or label change would otherwise shift the layout.
- A disabled state should have a clear reason when the reason is not obvious. A nearby explanation, an enabled action that reveals missing requirements, or another pattern can work.
- Report success only when the operation actually completes. An optimistic UI needs rollback or recovery if the server rejects it.
- Failed actions need a readable error and a practical recovery path. Do not leave a button permanently spinning.

## Destructive, bulk, and grouped actions

Match confirmation to impact. Reversible changes may be better served by undo; irreversible deletion, payment, publication, or broad bulk changes may need explicit confirmation. Identify the object and actual affected scope. The control should not imply that archiving permanently deletes data or that deleting a draft removes an issued financial record.

Bulk actions need a clear selection count and scope, including whether selection spans filtered results or only the visible page. Protect against stale selection after filtering. Show partial failures honestly and avoid repeating completed operations on retry.

Segmented controls, split buttons, and button groups should reflect their real selection or action semantics. Keyboard shortcuts can speed repeated work when discoverable and compatible with user settings and assistive technology.

## Placement and floating actions

Use location to match workflow: persistent totals or save actions can help long tasks; floating actions can suit mobile creation. They are not categorically forbidden on desktop or admin pages. Verify that fixed elements do not cover content, focus, safe areas, or the onscreen keyboard, and that the action remains reachable when content grows.

## Review

Exercise each changed action through keyboard and pointer, pending, success, failure, and relevant disabled states. Confirm semantics, accessible names, real result, and visual consistency with the selected direction.
