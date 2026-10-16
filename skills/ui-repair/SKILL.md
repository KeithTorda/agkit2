---
name: ui-repair
description: "Reproduce and repair existing web UI defects using rendered state, computed layout, cascade and behavior evidence. Covers overlap, overflow, stacking, sizing, responsiveness and component state without silently redesigning the approved interface."
version: 2.8.2
---

# Repair the demonstrated UI defect

Preserve the approved design and working flow. A repair is not a new aesthetic intake unless the user actually requests a new direction. Diagnose the component, its ancestors, cascade and state before changing code; the cause can be in any of those layers.

## Reproduce and locate

Confirm the route, width, state, browser and content that trigger the defect. Inspect the actual app with available tools and save a before capture when useful. If only source or a supplied screenshot is available, state that limit and treat the diagnosis as provisional. Do not ask for facts that the project or available render can establish.

Find the rendered element, owning component and relevant ancestors. Read computed display, position, sizing, min/max constraints, overflow, flex/grid behavior, containing blocks, transforms and stacking contexts. Inspect the actual winning CSS rule and relevant JavaScript state rather than assuming class names equal computed behavior.

## Common causes to investigate

| Cause | Evidence and useful remedy |
|---|---|
| Indefinite height or available-space model | Check how percentage height resolves and which container owns scroll. Use a definite track/height or flexible min-size where the actual layout requires it; `min-height` alone does not universally make every descendant percentage resolve. |
| Wrong flow or constraints | Inspect sibling relationships and min/max sizing. Change the existing layout owner to suitable grid/flex/flow rather than compensating with an unexplained offset. |
| Stacking/containing context | Trace ancestors creating contexts. A larger child `z-index` cannot escape its parent's context; adjust the context or use the product's overlay/top-layer mechanism. |
| Overflow and sticky scrollport | Identify which ancestor clips or scrolls. `overflow` can change the scroll container; `overflow: clip` has different behavior. Confirm sticky thresholds and available travel instead of banning overflow ancestors. |
| Fixed/sticky assumptions | Fixed content may need reserved space; sticky needs a suitable scroll container and room. Check keyboard and mobile viewport behavior. |
| Width/box model | Inspect padding, border, intrinsic content, `box-sizing`, percentages and calculations. Use a local correction rather than hiding page overflow globally. |
| Automatic flex/grid minimum | `min-width: auto` or an intrinsic grid track may resist shrink. Consider `min-width: 0`, `minmax(0,1fr)`, wrapping or a deliberate scroll region. |
| Breakpoint or content boundary | Test the failing interval and just across relevant transitions. Fix overlap/gaps or an overly narrow content assumption. |
| Readable but impractical density | Compare actual-size labels, status and secondary actions with the task. Check the width left after navigation before reducing type. Correct the owning composition/type role; fitting without overflow is insufficient evidence of usability. |
| Offscreen essential data | Identify the actual data table/region rather than the first table on the page. Verify where status, totals and actions move, how their availability is communicated, and that scrolling, focus or the chosen detail view reaches them. |
| State, asset or lifecycle | Check stale async data, missing fonts/media, measured dimensions, provider placement, animation cleanup and hydration. A CSS tweak cannot fix the wrong state. |

This is a diagnostic map, not a requirement to assign every defect a category. Form a testable cause, make a small explanatory change, and observe its effect. If automation fails, inspect its initial state and intended target before changing functioning UI to satisfy a wrong test.

## Implement a durable correction

Change the owning constraint, token, component state or library configuration. Remove only rules or wrappers made obsolete after checking their callers. Preserve legitimate variants, themes and local layout adjustments. An override can be appropriate for an uncontrollable vendor boundary; keep it narrow and explain the reason. A universal ban on inline values, positioning, wrappers or `!important` is not a diagnosis.

Use [components.md](components.md) for shells, navigation, dialogs, popovers, tables, forms and notifications. Use `css-architecture` for styling ownership and `systematic-debugging` for broader failure isolation.

## Verify the fix

Recheck the reproduced route/state at the broken size and nearby affected layouts. Exercise relevant focus, scroll, input, dismissal or the component's primary action. When a shared shell changes, inspect representative consumers. Use meaningful regression tests for behavioral defects when the project supports them; a reversible spacing correction does not need a test that repeats CSS values.

Follow `browser-verification` for actual render evidence. Explain the cause, correction, checked conditions and concrete limits. Do not describe source reasoning as a seen result or claim all routes are verified from one screenshot.
