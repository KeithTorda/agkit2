# UI Repair — component reference

Read when the broken (or new) element is one of these. Core SKILL.md first.
Bug numbers are the root causes in `SKILL.md` §3. Classes are Tailwind v4; plain CSS is the same rule.

## App shell (sidebar + header + content)

Structure:
- `<div class="min-h-dvh grid grid-rows-[auto_1fr] md:grid-cols-[16rem_1fr]">` — the shell owns the layout
- `<header class="sticky top-0 z-40 h-16 md:col-span-2">`
- `<aside class="hidden md:block md:sticky md:top-16 md:h-[calc(100dvh-4rem)] overflow-y-auto">`
- `<main class="min-w-0 overflow-x-hidden">` — the document scrolls, `main` does not
- Mobile: the same `<aside>` becomes a drawer `fixed inset-y-0 left-0 z-50 w-72` over a backdrop `fixed inset-0 z-40 bg-black/50`; close on Escape and route change
Bugs:
- Sidebar renders below the header → (2) the shell is block flow; set the grid on the shell, never a negative margin on the aside.
- Sidebar scrolls away with the page → (5)/(4) `sticky` needs `top` and no `overflow` ancestor; remove `overflow-hidden` from the shell.
- A wide table pushes the sidebar off-screen → (7) `min-w-0` on `main`, `overflow-x-auto` on the table wrapper.
Accessibility: `<header>`, `<nav aria-label="Main">`, `<main>` landmarks; a skip link first in tab order; the drawer takes focus on open and returns it on close.

## Header / nav

Structure:
- `<header class="sticky top-0 z-40 h-16 border-b bg-background">` → `<div class="mx-auto flex h-full max-w-7xl items-center gap-6 px-4">`
- Logo link · `<nav aria-label="Main" class="hidden md:flex items-center gap-1">` · actions `ml-auto flex items-center gap-2`
- Menu button `md:hidden` opens the app-shell drawer; one nav, not a mobile copy
- Height is the shell's token (`h-16` = `4rem`); sticky offsets below use `top-16`
Bugs:
- Header hides the first line of content → (5) it is `fixed` with nothing reserving its height; make it `sticky` in flow.
- Its menu opens behind a sticky table header → (3) the header is a stacking context (`sticky`, `backdrop-blur`) with no z-index, so its subtree sits under `main`'s `z-10`; give the header `z-40`.
- Nav wraps to two lines at 768 → (8) the nav shows from `md:` but only fits from `lg:`; move the variant or add a "More" menu.
Accessibility: `aria-current="page"` on the active link; the menu button carries `aria-expanded` and `aria-controls`; 44px targets on touch.

## Sidebar

Structure:
- `<aside class="md:sticky md:top-16 md:h-[calc(100dvh-4rem)] overflow-y-auto border-r">` in the shell's first column
- `<nav aria-label="Sidebar" class="flex h-full flex-col gap-1 p-3">`; a pinned bottom block uses `mt-auto`, not `absolute bottom-0`
- Width is the shell's `grid-template-columns`, never the aside's; collapse by changing the shell column (`md:grid-cols-[4rem_1fr]`)
- Item: `<a class="flex items-center gap-3 px-3 py-2"><Icon class="size-4 shrink-0" /><span class="min-w-0 truncate">`
Bugs:
- Does not stick, scrolls away → (4)/(5) an `overflow-hidden` ancestor, or a shell with no height; remove the overflow, give the shell `min-h-dvh`.
- Shorter than the page, bottom block floats → (1) `h-full` under an `auto` ancestor; `md:h-[calc(100dvh-4rem)]` with sticky, or `grid-rows-[auto_1fr]` + `min-h-dvh` on the shell.
- A long label widens the sidebar or gets cut → (7) `min-w-0 truncate` on the label span, not a wider aside.
Accessibility: `<nav aria-label="Sidebar">`; `aria-current="page"` on the active item; icon-only items keep an `aria-label` and a tooltip; DOM order is tab order.

## Modal / dialog

Structure:
- `<dialog>` via `showModal()` (top layer, no z-index needed) or a portal to `body`; never inside a card or a transformed ancestor
- Backdrop `fixed inset-0 z-50 bg-black/50` · positioner `fixed inset-0 z-50 grid place-items-center p-4`
- Panel `w-full max-w-lg max-h-[calc(100dvh-2rem)] overflow-y-auto rounded-xl bg-background` → header (`<h2 id>`), body, footer `flex justify-end gap-2`
- Lock the page while open: `overflow-hidden` on `<html>`, restored on close; the panel scrolls, not the page
Bugs:
- Opens clipped or behind the header → (3)/(4) rendered inside a `transform` or `overflow-hidden` ancestor; portal it to `body` or use `<dialog>`.
- Tall dialog cut off at the bottom on mobile → (1)/(6) a fixed height or `h-screen` on the panel; use `max-h-[calc(100dvh-2rem)] overflow-y-auto`.
- Actions row overflows at 390 → (7)/(8) buttons in a flex row that cannot shrink; `flex-wrap` or stack them below `sm:`.
Accessibility: `role="dialog" aria-modal="true" aria-labelledby`; focus moves in on open, is trapped, and returns to the trigger on close; Escape closes; `<dialog>` gives most of this free.

## Dropdown / popover

Structure:
- Trigger `<button aria-haspopup="menu" aria-expanded aria-controls>` · panel `<div role="menu" id class="z-50 min-w-56 border bg-background p-1">`
- Position with Floating UI / Radix (`flip`, `shift`, `offset`) or CSS anchor positioning — never a hand-placed `absolute top-full left-0`
- Render in a portal unless no ancestor has `overflow` or `transform`
- Long lists: `max-h-80 overflow-y-auto` on the panel, never on an ancestor
Bugs:
- Panel renders behind a neighbour → (3) an ancestor with `transform`/`opacity`/`filter`/`will-change`; z-index cannot win; portal the panel or remove the property.
- Panel cut at the card edge → (4) an `overflow-hidden`/`auto` ancestor clips it; portal it, or move the overflow to the region that scrolls.
- Panel opens off-screen at 390 → (8) a fixed `left-0` placement with no flip or shift; use the positioning middleware.
Accessibility: `aria-expanded` mirrors open state; `aria-controls` links trigger and panel; arrow keys move, Escape closes and returns focus; `role="menu"`/`menuitem` for command menus, `listbox` for selects.

## Data table

Structure:
- `<div class="w-full overflow-x-auto rounded-lg border">` → `<table class="w-full min-w-[40rem] text-sm">` with `<thead>`, `<tbody>`, `<th scope="col">`
- Sticky header inside the wrapper: `<thead class="sticky top-0 z-10 bg-background">`, and the wrapper becomes the scroller
- Numeric cells `text-right tabular-nums`; long text `max-w-xs truncate`; actions column `whitespace-nowrap`
- The wrapper sits in a `min-w-0` parent
Bugs:
- Whole page scrolls sideways → (7) the wrapper is a flex or grid child with `min-width: auto`; `min-w-0` on the parent, `overflow-x-auto` on the wrapper.
- Sticky header never sticks → (4)/(5) the wrapper's `overflow-x-auto` makes it the scroll root, not the page; give the wrapper `max-h-[70dvh] overflow-auto`, or drop sticky.
- Columns squash to nothing at 390 → (6) `w-full` with no minimum; `min-w-[40rem]` on the table and let the wrapper scroll.
Accessibility: `<th scope="col">` / `scope="row"`; `<caption>` or `aria-label` on the table; sort buttons inside `<th>` with `aria-sort`; never a `div` grid dressed as a table.

## Form

Structure:
- `<form class="grid gap-6">` → `<fieldset class="grid gap-4 md:grid-cols-2">` per group with a `<legend>`
- Field: `<div class="grid gap-1.5"><label for={id}>` → `<input id class="w-full min-w-0">` → `<p id={hint}>` / `<p id={error} role="alert">`
- Actions `<div class="flex flex-wrap justify-end gap-2">` at the end, primary last; `sticky bottom-0` only on long forms
- Never a fixed pixel width on a control; the column decides
Bugs:
- Inputs overflow their column → (6)/(7) a `w-full` control with `content-box` (missing reset) or a flex child without `min-w-0`; restore `border-box`, add `min-w-0`.
- Two columns stay one column at 768 → (8) the grid has `lg:grid-cols-2` only; use `md:`.
- Label and input misalign in a row → (2) hand-aligned siblings in a flex row with mixed heights; use the stacked field grid above.
Accessibility: every control has a `<label for>` (or `aria-labelledby`); errors linked with `aria-describedby` and `aria-invalid="true"`; `<fieldset>`/`<legend>` for groups; Enter submits.

## Toast

Structure:
- One region at the app root: `<div class="pointer-events-none fixed inset-x-4 bottom-4 z-50 flex flex-col gap-2 sm:left-auto sm:w-96">`
- Each toast `pointer-events-auto border bg-background p-4 shadow-lg`, rendered by a provider, never by the page that fired it
- Enter with `motion/react`, respecting `prefers-reduced-motion`; auto-dismiss at 5 s or more, paused on hover
Bugs:
- Toast appears behind a modal or the header → (3) the region is mounted inside a transformed or lower-z ancestor; mount it at the root, above every layer.
- Toast cut off on the right at 390 → (6) `w-96` plus `right-4` exceeds the viewport; `inset-x-4` on mobile, `sm:left-auto sm:w-96` above it.
- Toast vanishes when its page unmounts → the provider lives in the page, not the root layout; move it up (a structure bug, not one of the eight).
Accessibility: the region is `role="status" aria-live="polite"`; a toast that reports an error is `role="alert"`; the dismiss button has an accessible name; never steal focus.
