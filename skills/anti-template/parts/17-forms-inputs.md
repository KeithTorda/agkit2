---
part: 17
title: Forms and input behavior
covers: field selection, labels, validation, submit, autocomplete, choice controls, dates, upload, passwords, money, OTP
---

# 17 - Forms and input behavior

Read while building a form. Visual treatment may be compact, spacious, branded, floating-label, illustrated, or another selected style; information and input behavior must remain usable.

## Ask for needed information

Choose fields from the actual task. Explain why sensitive or unexpected data is needed. Group related questions, provide sensible defaults, and preserve entered values across recoverable failures. A single page or a multi-step flow can both work; use steps when grouping, dependencies, or complexity justify them. Avoid demanding the same information twice when it is already available and reliable.

Use a persistent, programmatically associated label. Floating labels are valid when they remain readable, clearly associated, and stable with autofill, long values, errors, zoom, and placeholder behavior. A placeholder is not a substitute for a label. Explain required/optional state consistently and expose it to assistive technology.

## Validation and submission

Validate the actual rules, with useful examples and text errors. Client validation helps input; server validation enforces the contract. Do not trust client totals, roles, or constraints. Prefer blur or submit feedback over disruptive per-keystroke errors; real-time feedback can be useful for constraints such as password strength when accessible.

On submit failure, retain input, mark invalid fields, link descriptions, and move focus to the first relevant error or a summary. A network failure differs from an invalid field. Offer retry without duplicating a payment, invitation, or record. Pending submission needs clear feedback and duplicate prevention; disabling a control is one option, not a reason to hide all explanation.

## Choose controls by meaning

- Use suitable `type`, `inputmode`, and `autocomplete` values for email, phone, names, addresses, passwords, and one-time codes. Preserve native semantics while giving the visible control a deliberate project-coherent treatment. Follow [component guidance](../../frontend-design/components.md) for the custom treatment of visible and open surfaces, including its intentional platform/system exceptions; do not rebuild browser behavior solely to replace semantic HTML.
- A select suits a bounded choice list; search/combobox helps a large or remote dataset. Implement its keyboard, name, state, and option announcements through a proven primitive or established pattern.
- Radio buttons select one choice; checkboxes select independent choices; switches change an immediate setting. Explain deferred save behavior when toggles are part of a larger form.
- Date-only and time-zone-aware inputs represent different data. Show accepted format and constraints; test ambiguous locales, keyboard entry, invalid dates, and boundary dates.
- Uploads need accepted types and sizes, progress based on real transfer if available, errors, retry, removal, and a file input alternative to dragging. Validate content server-side.

## Passwords, OTP, and accessible authentication

Allow paste, password managers, autofill, and appropriate autocomplete. A show-password control needs an accessible name and state. Explain actual password requirements; do not invent complex composition rules without a security requirement.

OTP input may be one field or a carefully implemented segmented control. Support full-code paste, keyboard movement, screen reader naming, autofill, error recovery, and a real resend flow. Countdown and expiry must reflect server behavior. Do not announce each ticking second unnecessarily.

## Money, quantity, addresses, and long forms

Treat identifiers, phones, postal codes, and account numbers as strings where leading zeros matter. Use locale-aware display, exact financial arithmetic, explicit currency, and server-side constraints for amounts. Quantity controls need min/max and meaningful increments from the domain.

Names and addresses should not assume one global format. For Philippine fields, use actual service coverage and maintained validation; see part 09. For long applications or institutional forms, support useful sections, drafts where needed, visible progress when known, and timeout recovery. Do not require a specific step count or field layout.

## Review

Test successful submission, invalid input, network failure, repeated clicks, long content, autofill, keyboard-only operation, and relevant mobile behavior. Verify that visual customization preserved labels, focus, state, and errors.
