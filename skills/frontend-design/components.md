# Custom-styled web components

Read when building or refining controls, component families or their open states. Extend the approved direction and installed foundation; a component matching that system does not need another style-intake question.

## Design the whole component

Custom-styled, project-coherent components are the default for web UI. Give the visible surface a deliberate relationship to the surrounding product: type roles, label alignment, control height/padding, border/material, icon weight, color roles and feedback. Quiet or familiar components can still look intentional; decoration and animation are not requirements.

Inspect the states the component actually supports. A button may need hover, press, focus, disabled and pending treatment; a field may need filled, invalid and help text; a choice control needs selected and open content. Do not implement irrelevant states merely to fill a checklist. Keep state understandable beyond color, make focus visible and avoid clipped values or jumping layouts.

The open surface is part of the design. A styled `<select>` box can still launch an OS/browser-rendered options popup; a CSS arrow or `appearance: none` on the trigger does not establish a custom options panel. Include the options surface in the custom treatment by default, unless an intentional platform interface, required system or user-requested native control applies. Do not require the user to repeat the preference for each dropdown. Apply the same reasoning to calendars, menus, tooltips and dialogs.

## Choose the behavior foundation

- Extend the existing accessible components and tokens first. A headless primitive may supply behavior while the project supplies its visual design; a full UI system may already cover both. Check the actual installed implementation before importing or replacing it.
- Keep semantic elements where they suit the task. A styled `<button>`, `<input>`, `<progress>`, `<table>` or `<dialog>` can be a custom-designed component. Replacing these with generic containers does not improve the design.
- Browser-owned interfaces such as a file chooser, autofill suggestions or a platform picker may intentionally retain platform behavior. Preserve them when required or useful for the task, and describe relevant styling limits honestly. An explicitly requested native/platform system takes precedence; this web guidance does not redesign native mobile conventions.
- For a custom choice popup, use the existing accessible primitive when available. Without one, select a platform-supported implementation or a scoped complete interaction pattern appropriate to the project. Check target-browser support before relying on newer APIs; do not copy an illustrative accessibility example and assume production support.
- Add a focused dependency only when the required interaction and support burden justify it. The custom-appearance default is not a mandate for one library, a second design system, a framework migration or hand-building every widget.

## Preserve the interaction contract

Choose semantics from the action. Selecting one value, opening navigation and running commands have different contracts; do not label every popup an ARIA menu. Prefer established patterns over invented keyboard shortcuts.

For a select-only combobox/listbox, connect its label, expanded state, popup and options. Make committed selection distinguishable from keyboard exploration when the pattern supports it. Verify arrow navigation, Home/End where relevant, type-ahead, selection, cancellation, Tab/Shift+Tab and ordinary outside dismissal. If focus stays on the trigger using `aria-activedescendant`, keep the referenced active option present and visibly scrolled into view. Escape should follow the pattern's cancellation and focus behavior rather than accidentally resetting the entire form.

Use the [W3C select-only combobox example](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/examples/combobox-select-only/) and [listbox pattern](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/) as interaction references when applicable, not a drop-in production library. Verify the chosen component with its intended browser and assistive-technology support; source markup alone cannot establish that support.

Keep actual application state in sync: selected value, filtered results, URL state when implemented, validation, reset, submitted form data and disabled/pending behavior. Avoid two independently focusable controls representing the same field. A native fallback or hidden form value must not create duplicate labels, tab stops, announcements or stale submissions. Preserve a useful fallback when progressive enhancement is part of the product.

## Verify the open surface

Open each affected control in the real page. Check readable option labels, active/selected differentiation, clear focus, anchor alignment, available height, collision near viewport edges, scrolling, zoom, long content and touch-sized targets. Test within the actual overflow, sticky, modal or transformed ancestors; a popup that works in an isolated component preview may clip in a table panel. A portal/top layer can solve a boundary problem but must preserve the focus and modal contract.

Subtle open/close or selection feedback can improve clarity. Match the approved motion direction, respect reduced-motion preferences and avoid delaying selection or dismissal. Do not add animation merely to make a component qualify as custom-designed.

Exercise visible controls, not only a hidden select or state API. A programmatic filter test can prove data logic while missing a broken trigger, inaccessible option or clipped popup. Keep render observations, interaction results and remaining support limits distinct in the handoff.
