---
part: 35
title: Contextual review and evidence
covers: proportionate review, design alignment, copy, visual QA, components, code, accessibility, security, searches, reporting
---

# 35 - Contextual review and evidence

Read for a review or completion check. Use the kit's proportional verification workflow and the scope of the actual change. This reference adds no mandatory approval stage and is not a style gate. The user's current brief and agreed design direction are the basis for aesthetic evaluation.

## Review the right work

Identify the changed behavior, visible areas, relevant existing system, and user choices. Load the topic references needed for those areas. Do not run every category for a typo, or skip browser inspection for a meaningful layout change merely because it touched one CSS value. A shared token can affect many screens.

Classify findings clearly:

- **Defect:** broken behavior, unreadable content, accessibility failure, misleading claim, data-integrity issue, or security boundary failure.
- **Mismatch with the brief:** the output does not implement the chosen reference qualities, style, content, or requested interaction.
- **Optional refinement:** a plausible improvement that is not required for correctness or the agreed result.

A reviewer's aesthetic preference is not an automatic defect. Fix actual issues while preserving what the user selected.

## Copy and content

Check that the offer, labels, consequences, and next action are understandable. Marketing can carry personality and emotion. No word, punctuation, phrase, heading structure, or emoji automatically fails review. Confirm real factual claims, testimonials, logos, pricing, deadlines, credentials, and contact details. Mark prototype data clearly; do not fabricate proof. Read relevant parts 01-09.

Check actual loading, empty, permission, stale, failed, and success states. Dates, time zones, currency, precision, and full identifiers should fit the task and locale. A live/freshness claim should reflect actual update behavior and known delay.

## Visual review

Inspect the rendered output at meaningful sizes and states when tools are available. Compare its typography, palette, image direction, composition, density, materials, and motion with the intake and supplied references. Look for real issues: unintended overflow, awkward wrapping, weak hierarchy, poor crops, inconsistent treatment, clipped content, accidental gaps, collisions, and unreadable overlays.

Glass, gradients, glow, texture, large headlines, dark themes, colored sections, cards, repeated grids, sticky headers, illustration, generated assets, and motion are all valid. Do not count them or remove them by reflex. No image minimum, layout-family quota, font-count ceiling, color limit, universal plain surface, universal light mode, or mandatory theme toggle applies. Review execution and fit, using parts 10-15 and 25-26.

## Components and behavior

Use parts 16-24 for the changed pattern. Test relevant navigation, forms, actions, data, charts, overlays, admin, and account flows. Controls should have real destinations/effects, useful feedback, error recovery, and appropriate duplicate prevention. Popovers and dialogs need correct focus/close behavior; tables and charts need truthful scope and readable values. Test keyboard and small-screen interaction that the change affects.

## Accessibility and implementation

Use parts 27-34 as relevant. Check semantic controls, names, keyboard reachability, focus, labels/errors, contrast, non-color meaning, reduced motion, zoom/reflow, and media alternatives. Automated checks supplement manual inspection; they do not establish complete compliance.

For logic and backend changes, review trust boundaries, authorization, secret handling, validation, state/race conditions, retries, idempotency, exact financial arithmetic, database constraints, and migration safety where relevant. Keep fixtures and mocks distinct from real production behavior. Build and check the changed path using the project's actual tools; report a failed check rather than suppress it.

## Searches are leads, not verdicts

Search only the relevant source paths and exclude dependencies, build output, generated assets, and the kit itself. Give `rg` an explicit path so it does not wait on piped stdin. For example, adjust these to the real project:

```sh
rg -n -e 'TODO|FIXME|debugger|console.log' src -g '!**/node_modules/**' -g '!**/dist/**'
rg -n -e 'Lorem ipsum|picsum.photos|placehold.co|vite.svg' src public -g '!**/node_modules/**'
rg -n -e 'user-scalable=no|maximum-scale=1|outline: *none|aria-hidden' src
rg -n -e 'noindex|Disallow: /|localhost|example.com' src public
```

Inspect every relevant hit in context. A TODO can be legitimate, a console log can be intentional, a placeholder can belong to an explicit prototype, outline removal can have an accessible replacement, and noindex can be correct for a private app. Search absence also does not prove safety or correctness.

Do not use grep patterns for gradients, glow, font names, colors, shadows, emoji, or motion as a failure list. If investigating an actual performance or contrast problem, search its implementation to locate the cause, then test the observed behavior. Do not print candidate secrets into a report; use redacted evidence and the project's appropriate secret-checking process.

## Completion evidence

Summarize the actual change, meaningful checks performed, results, and material remaining limitations. Link real artifacts and cite observed output where useful. A successful unit suite does not establish browser appearance; a screenshot does not establish payment integrity. Do not promise zero errors, complete security, universal accessibility, or guaranteed taste. Finish with the result and the practical state the user can review.
