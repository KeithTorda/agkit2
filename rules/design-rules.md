---
name: design-rules
version: 2.8.2
priority: P0
trigger: glob
globs: "**/*.html, **/*.css, **/*.scss, **/*.tsx, **/*.jsx, **/*.vue, **/*.svelte, **/*.astro, **/*.blade.php, **/*.dart, **/components/**, **/resources/views/**"
description: New visual designs start with a short style/reference conversation. Approved direction, meaningful craft and actual rendering guide the result.
---

# Visual Direction and Craft

## Start the design conversation

Before a new site, standalone page/app design or intentional redesign, ask one short conversational question about style and references in the user's language, then wait before choosing or implementing the visual direction.

For example: “Anong style ang gusto mo, at may website o screenshot ka bang reference? Puwede rin akong magrekomenda o pumili kung gusto mo.”

A description, dislike, sample image, URL, “no reference” or “ikaw na bahala” can settle the question. Do not demand design terminology, a fixed form, exact colors or a mandatory reference count. Reuse preferences already explicitly supplied for this design and explicit delegation; do not ask again merely because another specialist takes over. Silence is not approval.

An existing `DESIGN.md` is context and a useful suggested starting point for a new design. Fixes, content changes and small components matching an approved system continue that system without a new intake. Ask again only for a materially new direction or genuinely unresolved requirement.

## Implement the accepted direction

Turn the answer into a coherent visual system: information hierarchy, type roles, spacing/alignment, asset treatment, color roles, responsive behavior and interaction states. Record useful decisions in `DESIGN.md` after intake, proportionally to a new system or substantial redesign. A spec should describe the real implementation rather than become a second project to maintain.

References identify qualities to borrow, not a mandate to clone branding or install the reference's framework. The optional reference list in `KIT/skills/frontend-design/directions.md` includes BrewedOps Motion Library for motion and UI-pattern ideas. Choose resources that fit this task; no library, effect or extra theme is compulsory.

Minimalism, glass, gradients, glow, large or serif type, multiple accents, repeated composition, bold motion and contrasting sections can all work. Evaluate execution and fit with the user's choice. Do not use aesthetic bans, image/layout quotas or numeric dials as automatic quality gates.

For web UI, make custom-styled, project-coherent components the default. Buttons, fields, selects, tabs, tables, dialogs and feedback should share the accepted type, spacing, color and interaction language rather than expose an unfinished browser-default surface. Review both the closed control and its open content: a styled select trigger alone does not make an OS-rendered options popup custom-designed. Follow `KIT/skills/frontend-design/components.md` for implementation choices and state/behavior checks.

Custom appearance does not require abandoning semantic HTML or rebuilding accessible behavior. Extend the existing component foundation; native elements such as button, input and dialog can support the designed surface. Apply the custom-styling default to choice popups too, using a suitable accessible component and verifying its interaction without asking the user to repeat this preference. Preserve intentional platform interfaces, required systems and user-requested native controls; state an actual native rendering limitation instead of claiming full custom styling. This web preference does not override native-mobile conventions.

Use supplied/genuine brand and product assets when appropriate. Illustrative or generated material can support the direction but must not impersonate real product functionality, customers or proof. Placeholder/demo content should be recognizable where it could mislead.

Preserve readable contrast, semantics, controls, focus, keyboard/touch usability and reduced-motion alternatives in the contexts actually shipped. Inspect relevant render sizes/states, critique your own draft against the agreed direction, correct defects and recheck affected views. Report tooling limits rather than substituting a mental render for evidence.

Review the actual-size supporting text, status information, chart labels and next actions as carefully as the headline. A layout that fits or has no page overflow can still be hard to read or use. At intermediate widths, judge the working space left after navigation and panels; make offscreen essential data discoverable and reachable. Use the product-specific guidance in `KIT/skills/frontend-design/app-ui.md` rather than shrinking every element or applying one breakpoint to every product.

Web: `frontend-specialist` / `frontend-design`; native mobile: `mobile-developer` / `mobile-design`; flows: `ux-architect`. `anti-template` supports contextual craft review, not taste enforcement.
