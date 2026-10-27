---
name: browser-verification
description: "Inspect rendered web output only when browser/visual verification is explicitly requested; do not activate automatically after coding. Check meaningful widths, content states, accessibility, console and network behavior; evidence helpers validate records rather than replace browser inspection."
version: 2.8.3
---

# Rendered web verification

Activation: manual-only under `kit-core` - run only when the user asks (/see, /verify, an explicit request). The procedures below apply to requested browser verification, not ordinary delivery of UI code.

Verify what a person sees and can do. Source review, a running server, a successful build, a screenshot, and a working transaction are different kinds of evidence. Choose checks from the consequence of the change, including a small CSS edit with a wide effect.

## Establish the environment

Confirm the project, dev command, port, changed route, and required state. Reuse a suitable running server or start the project's normal preview without terminating unrelated processes. Check the ready output, then open the actual route with available browser tools. Do not assume that a tab, occupied port, cached response, or server log belongs to the current code.

When setup fails, use [troubleshooting.md](troubleshooting.md). Continue useful static checks and report what could not render. Tool availability never authorizes inventing screenshots, console counts, or successful interactions.

## Inspect output and behavior

1. Reproduce the requested surface with representative content. For repairs, include the reported width and state; preserve a before capture when available.
2. Compare the render to the brief, accepted style, actual references, and surrounding product. Check hierarchy, type wrapping, spacing, alignment, crop, contrast, clipping, and scroll behavior. Inspect at actual display size: a page can fit without overflow while supporting labels, chart metadata, status explanations, or secondary actions remain hard to read or use. Preserve intended visual expression while fixing execution.
3. Exercise affected controls and observe outcomes. Follow a local action through state changes or persistence when that is the intended behavior. Check invalid input, loading, failure, empty or long content where those cases bear on this change.
4. Inspect keyboard reachability, focus visibility/order, labels, and relevant dialog/form behavior. With an overlay navigation or modal open, exercise Tab/Shift+Tab, dismissal and focus return; confirm focus does not enter blocked content. An ordinary nonmodal disclosure has a different contract. Automated accessibility checks are useful but do not establish complete access.
5. Review relevant console errors, failed data requests, broken media, and hydration problems. Distinguish regressions from expected validation, blocked traffic, pre-existing warnings, and confirmed local-server/favicon noise. Confirm the origin before dismissing a diagnostic, and preserve useful failure evidence.
6. Correct observed defects, then recheck the changed region and any affected shared surface.

For a new full page, choose narrow and wide layouts representative of its users, plus a meaningful intermediate layout. Inspect how navigation affects available content width, the visible table columns, and the next action at that size. A repair may need only the failing width and its neighboring layout. Dimensions such as 390 and 1440 CSS px are examples, not the definition of coverage. Choose type and layout from the content and task; no universal font size, content width, or aesthetic score establishes usability.

For a horizontally scrolling table, use the actual scroll region to reach important and final columns. Verify keyboard users can reach the off-screen content as well as pointer/touch users, using the app's supported interaction. Check that users can discover the additional content from the initial view and retain enough row/header context to understand it. Contained overflow or a larger `scrollWidth` alone does not establish reachability or discoverability. Test text enlargement, fallback fonts, or unusually long content when those are plausible failure modes.

For custom-styled controls, inspect their open content in the real page, including viewport-edge positioning and overflow/modal ancestors. Exercise the visible trigger and options with pointer and keyboard, then observe the resulting value or action. A programmatic update to a hidden select can verify data logic while bypassing a broken custom UI. Review selected, active, focus and relevant error/disabled states; follow [component contracts](../frontend-design/components.md) for the affected pattern and state any browser/assistive-technology gaps.

Use computed layout and cascade facts when appearance does not match source: [computed-styles.md](computed-styles.md). Do not force every optical correction or responsive value onto a fixed token scale.

## Keep useful evidence

For substantial work or a handoff, evidence may be saved under `.agents/verify/<task-slug>/`. Record the route, actual viewport widths, meaningful states, interaction observed, console/network findings, defects fixed, and remaining limits. Counts are observed values; absent inspection means unknown, not zero.

The compatible helper accepts an evidence directory:

```powershell
python "KIT/scripts/ui_verify.py" .agents/verify/<task-slug> --widths 390,1440
```

If using its schema, create actual `after-<width>.png` captures and a truthful `verdict.json` containing `route`, `widths`, `consoleErrors`, `failedRequests`, `interaction`, `status`, and `notVerified` as required by the helper. Inspect the helper's supported schema instead of inventing new fields. Use `skipped` with its required reason when browser work could not run. Read the verdict: exit zero may mean an honestly recorded skip.

When claiming a substantive visual review, optionally add `visualReview` with an overall `status` and `views` containing each inspected CSS-pixel `width`, `status`, and nonempty `observation`. Status values are `pass`, `fail`, or `not-verified`. Record actual observations about legibility and task use; do not infer them from a screenshot's existence. To require recorded pass coverage for the widths in scope:

```powershell
python "KIT/scripts/ui_verify.py" .agents/verify/<task-slug> --widths 390,768,1440 --require-visual-review
```

This optional flag checks the review record and width coverage; it cannot perceive screenshots or establish that the observations are truthful. Ordinary small edits do not require this extra record.

The helper checks artifact consistency. It does not operate the browser, judge design, or prove that the asserted interaction happened. Report fit/overflow, legibility/task usability, and control behavior as separate observations; a functional pass is not an aesthetic score. State the actual observed result and exact unverified checks; no ceremonial screenshot set is required for an unrelated nonvisual change.

For a requested paired comparison of generated outputs or instruction changes, use [comparison-testing.md](comparison-testing.md). Ordinary implementation work does not require an A/B experiment.
