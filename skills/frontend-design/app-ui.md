# App UI

Read for dashboards, settings, onboarding, forms, tables, and other non-marketing screens. [SKILL.md](./SKILL.md) covers new-design intake; maintenance extends the approved design.

## 4.4 Controls, states, and forms
Use custom-styled controls coherent with the approved product. Read [components.md](components.md) when creating or replacing a control: its dropdown, calendar, dialog or other open surface belongs to the design as much as its trigger, with semantic and keyboard behavior preserved.

Design states that actually apply to the screen:

| State | Useful behavior |
|---|---|
| Loading | Indicate activity near the content or action. Use a skeleton for predictable layouts or a spinner/progress label when that communicates better. Avoid fake progress. |
| Empty | Explain what is missing and the next useful action; distinguish first use from no search results. |
| Pending mutation | Show feedback on the triggering control when practical, prevent accidental duplicate submission, and preserve the user's input. |
| Error | Explain the problem near its cause, associate field errors with controls, and provide a recovery path. Use live regions for important asynchronous messages. |
| Success | Update the visible result, navigate, or confirm inline. A toast may supplement context when appropriate. |
| Long content / many items | Allow meaningful wrapping, truncation with access to the full value, sorting, or pagination as needed. |
| Unavailable / no permission | Explain the boundary and useful next step without exposing restricted data. |

Persistent visible labels, helper/error relationships, correct input types, keyboard behavior, and visible focus are part of the component. State must remain understandable without color alone. Check normal text against the actual background; large text thresholds differ from small text. Do not infer a passing contrast result from a color token's name.

Button names should describe their actions. Keep them readable in the user's language; no arbitrary three-word limit. Touch targets and spacing should be comfortable for the audience. Do not force scale or translation feedback on every control.

## 5.E Feedback and behavior
- Keep the UI responsive during work. Disable only controls whose use would cause conflicting or duplicate actions, not an entire screen without reason.
- Use optimistic updates only when failure can be clearly recovered and the product's semantics support it. Preserve existing confirmed transaction flows.
- Hover, focus, press, selection, and validation transitions may use color, opacity, elevation, or a small transform as appropriate. Keep feedback-only or richer choreography aligned with the agreed intent and motion preferences.
- Do not use a toast or `window.alert()` as a replacement for persistent field error information.
- Prototype controls should demonstrate the promised flow or be visibly identified as unavailable/demo. Do not display success without performing the represented operation.
- For navigation that overlays and blocks the page, verify its modal focus contract: move focus appropriately, keep keyboard users out of covered content, support dismissal and restore focus. An inline, nonmodal disclosure keeps ordinary page navigation; do not trap focus merely because a menu is expanded.

## 7. App-page hierarchy
Lead with the information the user needs to decide or act. A monitoring dashboard may lead with exceptions; a work queue with its actionable list; a financial view with a balance. Make operational signals understandable: show the condition, its significance and a clear next action when one is available. Give that action enough emphasis to be found. There is no mandatory stat-tile row, hero, or welcome message.

Give the primary task clear emphasis while allowing multiple equally valid actions when the task requires them. Position repeated actions consistently; a long form may benefit from both top and bottom save access. Headers, greetings, context, and counts are optional content, not banned patterns.

Group forms by meaning and reading order, not a fixed number of fields. Choose single or multiple columns according to dependencies, input width, and viewport; keep labels and errors connected on mobile and under zoom. Preserve submitted values on validation failure.

For tables, align comparable numbers consistently, use tabular figures where useful, provide clear headers and sort state, and expose essential row actions on touch and keyboard. Reuse existing table/editor components; introduce a specialized library only when the actual interaction requires it.

Read `style-dark-dashboard.md` only for an approved dark operations direction. Marketing layout/imagery rules do not automatically apply to app screens.

### Density and data meaning
Choose density from the work: scanning a queue, comparing values or reading an explanation have different needs. Fit useful information through grouping, layout and concise copy; check whether secondary text became small by accident, especially where unused space remains.

Make metrics and charts semantically checkable. State units, period and population where ambiguity changes interpretation; explain non-obvious measures, included statuses or rate denominators. Use the same definitions in labels, calculations and detail views. When filters change, communicate the result context and which summaries, charts or rows follow those filters. A decorative chart or number must not imply an unsupported measure or live result.

### Content space and essential data
Choose navigation, chart arrangements and table presentation from the content space left after navigation, padding and sibling panels. Check intermediate widths: a rail may remain, narrow, move or collapse; charts may stay adjacent or stack according to readable labels and useful plotting space. Device names and preset breakpoints do not establish that the resulting workspace is usable.

Identify the columns and actions needed for the task before adapting a table. If essential data starts offscreen, make it discoverable and reachable with an appropriate overflow cue, prioritized or pinned context columns, column controls or a row-detail view. Choose only the mechanisms the task needs. Verify the initial narrow view, the farthest essential column and row actions with touch and keyboard; check that users can still identify the row they are acting on.

### Rendered craft review
Read the actual render at its intended display scale: supporting labels, status explanations, chart axes/captions, filter context and action text matter alongside headlines and metric values. Check whether an operational issue and its next action can be found, and whether useful density has become cramped microcopy. Inspect the first viewport and below-fold sequence, then verify essential data access at narrow and intermediate widths.

Record craft findings separately from control behavior. A successful filter, scroll or export check proves that behavior; its visual affordance, readability and prominence still need rendered review. Static captures alone do not prove that controls work.
