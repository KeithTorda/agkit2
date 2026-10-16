# Component-specific repair clues

Use with the reproduced defect and computed-layout method in `SKILL.md`. These are diagnostic options, not fixed markup recipes or a required Tailwind version.

## App shell and sidebar

The shell owns the relationship between header, navigation and content. Inspect grid/flex tracks, intrinsic minimums, scroll ownership, sticky offsets and actual header height. A wide table may need `min-width: 0` on a flexible content region plus deliberate table overflow; hiding the whole page's overflow conceals the cause.

A sidebar's width can belong to its grid track, flex basis or supported component variant. Use the existing model rather than declaring one universally correct. For a narrow layout, preserve access to navigation through the approved drawer/disclosure pattern. Check focus, close behavior, route changes and scroll position; do not duplicate incompatible navigation state across two independent copies.

## Header and navigation

Inspect whether the header is fixed, sticky or in ordinary flow and whether content reserves the needed space. Test long labels, zoom and the width at which navigation actually stops fitting. A breakpoint may move or a real overflow-menu pattern may be needed; every nav need not collapse at `md`.

Use meaningful landmarks, current-page state, accessible names and a correctly linked disclosure button. Ordinary website navigation is usually links with a disclosure, not an ARIA application menu.

If the narrow navigation overlays and blocks content, reproduce keyboard use while it is open. Toggling `aria-expanded` and showing a backdrop do not prevent Tab from reaching covered controls. Match the intended modal behavior with appropriate initial focus, background inertness, contained focus, dismissal and focus return. A nonmodal inline disclosure should retain normal page focus order rather than inherit a modal trap.

## Dialog and sheet

Prefer an existing accessible primitive or native dialog/top-layer behavior when appropriate. A portal can escape an unwanted clipping/context boundary, but still needs focus management and correct semantics. A native `dialog` in the top layer may work even when its DOM parent is transformed; do not diagnose from ancestry alone.

Inspect max available height, inner scrolling, keyboard overlap, long content and action wrapping. Verify initial focus, contained keyboard navigation where modal, Escape/cancel behavior, background inertness and focus return. Avoid simultaneously applying two scroll locks or leaving one active after unmount. A higher z-index does not place normal content above the browser top layer.

## Popover, command menu and select

When repairing unfinished browser-default appearance, follow [custom-styled components](../frontend-design/components.md). Inspect the open surface as well as the trigger; changing a select's border or arrow does not change an OS-rendered options popup. Retain semantic controls and the approved component foundation while correcting the visual gap.

Decide which interaction is actually intended. A disclosure, listbox and command menu have different keyboard/ARIA contracts; do not add `role="menu"` to a generic panel. A simple anchored panel can use ordinary positioning when sufficient; complex collision/resize behavior may justify the existing positioning primitive or supported CSS anchor positioning.

Check clipping, containing blocks, flipping/shift near edges, zoom, touch and focus return. Portals solve some ancestry problems and introduce ownership/focus considerations; they are not mandatory for every dropdown.

## Data table

Use native table semantics for relational tabular data. A deliberate interactive grid may use its corresponding complete interaction pattern. Preserve headings, row/column relationships and full critical values. Truncation requires a way to inspect the actual value when it matters.

Trace horizontal overflow through flexible ancestors and intrinsic tracks. Let a designated wrapper scroll when the table truly needs two dimensions, while surrounding content reflows. Sticky headings must be tested in the actual scroll container. `aria-sort` describes the sorted column header, with a properly named sort button inside it when appropriate.

## Forms

Keep labels, help and errors connected to controls. Inspect intrinsic sizing, min-width, box sizing, field grouping, multiline labels and action wrapping. The layout can be stacked or aligned depending on content; replacing every row with a fixed recipe is not a repair.

Verify valid/invalid submission, pending and recoverable failure when affected. Preserve user input and focus the relevant error/summary appropriately. Do not fix layout by dropping necessary labels, zoom support or error text.

## Notifications

Choose placement and lifecycle from the product's actual use. A persistent app-level provider can survive route changes; a local notice can appropriately belong to one page. Important errors should remain discoverable near the task rather than exist only in a vanishing toast.

Check overlay/top-layer interaction, narrow width, keyboard access and safe offsets. Use polite status announcements for ordinary feedback and urgent alerts only for actual urgency. Avoid announcing the same message twice or stealing focus. Timeout, pause and dismissal depend on reading/interaction requirements; there is no universal five-second rule or required motion library.

After any component fix, reproduce the failing condition, inspect adjacent affected sizes/states and exercise the relevant interaction. Explain source cause and observed result rather than merely listing changed classes.
