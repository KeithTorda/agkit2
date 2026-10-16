# Structure a mobile screen around its job

Complete the shared style/reference intake before a new visual design and wait unless already answered or delegated. For an existing-screen repair, keep the approved direction. Read the actual content, platform and user task; do not select tabs, a floating button, global state or a particular list package by habit.

## Screen read

Establish what the person needs on arrival, the main next action, related content groups and what success means. A cashier's repeated task, a long article, a media player and an onboarding flow have different hierarchies. “One primary action” can be useful emphasis, but does not mean hiding valid parallel actions or forcing every page into a wizard.

Consider reach, device size, orientation, keyboard, safe areas, reading order, larger text and interruption. A primary action can move with content or sit in an appropriate persistent area; bottom-right is not ideal for every hand, language or flow. Do not use difficulty of reach as the sole protection for destructive actions; use clear consequences, undo or confirmation as the task warrants.

## Pattern questions

- Do top-level destinations need frequent switching, or is this a hierarchical/linear flow? Choose navigation from that relationship rather than a fixed item-count rule.
- Does the region hold a small fixed set or a growing dataset? Choose a suitable scrolling/list strategy and keep state/key ownership stable.
- Is data authoritative, cached, queued or local? Feedback should distinguish these states honestly.
- Is a sheet useful for the focused task, or will long content/keyboard require another presentation?
- Does a gesture conflict with system navigation or require an alternative for assistive input?
- Does the current component already provide platform semantics and state handling?

Use familiar patterns when they serve the task and customize their visual treatment to the accepted brand. A conventional component is not inherently generic; originality can come from content, typography, materials, imagery and composition rather than inventing a new control grammar.

## Validate the idea

Use realistic names, labels, amounts and long/empty content. Inspect actual native output and exercise the important action, not just a web-shaped mock. Test relevant loading, failure, permission and offline behavior without manufacturing nonexistent states. Refine observed weaknesses and record what remains unverified.
