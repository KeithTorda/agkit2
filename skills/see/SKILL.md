---
name: see
description: "Inspect a real web render and relevant interactions against the intended behavior and accepted direction. Use /see for visual verification or a requested UI review."
version: 2.8.2
---

# /see

Use `KIT/skills/browser-verification/SKILL.md`. The target is the supplied route/URL or the current task's affected screen. Reuse an appropriate running server or start the documented one when practical; confirm it serves the intended build before inspection.

Render the affected states and choose viewports from actual device/breakpoint needs. A new responsive screen usually needs representative mobile and desktop views; a localized bug also needs its reported width. Inspect hierarchy, readability, spacing, content fit, focus and relevant DOM/computed styles. Check console/network failures that affect the flow and exercise the changed primary interaction and meaningful invalid/recovery behavior.

Critique against the accepted brief and references, not a generic aesthetic checklist. For your implementation task, refine observed defects and render again. For review-only work, report findings before making changes outside the existing authorization. Maintenance verification does not require new design intake.

Screenshots and ui_verify can record useful evidence when the task warrants them; image existence alone does not prove inspection. Never report unseen widths, clicks or console results. If the runtime/browser cannot be used, diagnose the missing precondition, continue applicable checks and state the visual limit.

Report target/state/widths actually inspected, observed behavior, required fixes or useful polish and any unverified areas. Keep evidence proportional to the claim.
