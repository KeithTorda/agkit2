---
name: ui-repair
description: "Diagnoses and fixes existing web UI that renders wrong — misplaced, overlapping, clipped, collapsed, or unresponsive layout — by locating the parent's layout mode and computed box model, naming one of eight root causes, and fixing the container at the source; never an override. Use when UI that exists is wrong, and for /fix-ui."
version: 1.0.0
---

# UI Repair

> A layout bug is almost always in the parent, not in the element that looks wrong.

The container's layout mode, height chain, and stacking contexts decide where an element lands.
Diagnose upward before editing.

## Protocol

### 1. Reproduce

Open the route in the browser at the width the user reported (`browser-verification` §1–2).
Screenshot it. State the defect in one sentence of observation: "the sidebar renders below the
header instead of beside it". If it does not reproduce there, check the other two widths first.

### 2. Locate

Find the misplaced element **and its parent** in the rendered DOM, not the JSX. Read computed
values, not class names, for the element and every ancestor up to `<main>` (or the root when it
sits outside `main`):

```js
// Computed layout facts: the element and its ancestors up to <main> (or the root)
const props = ['display','position','top','left','width','minWidth','maxWidth','height',
  'minHeight','overflow','zIndex','flexDirection','flexGrow','flexShrink',
  'gridTemplateColumns','gridTemplateRows','boxSizing','transform'];
const out = []; let el = document.querySelector('SELECTOR');
while (el && el.tagName !== 'MAIN') {
  const s = getComputedStyle(el);
  out.push({ el: el.tagName + '.' + String(el.className).split(' ')[0],
    ...Object.fromEntries(props.map(p => [p, s[p]])) });
  el = el.parentElement;
}
console.table(out);
```

### 3. Root cause — name ONE of the eight before touching code

1. **Broken height chain** — a `100%` or `flex-1` child needs every ancestor to have a height.
   Symptom: `h-full` collapses to content height; a sticky sidebar does not fill; the footer floats mid-page.
   Tell: an ancestor reports `height: auto` above the `%` child. Fix: `min-h-dvh` on `html`/`body`/`#root`/the shell, `flex-1 min-h-0` down the chain.
2. **Wrong layout mode for the content** — flow where flex or grid is needed, or nested flex where grid areas were the intent.
   Symptom: siblings stack that were meant to sit side by side; widths fight in nested wrappers.
   Tell: the parent is `display: block`, or three flex wrappers deep with `calc()` widths. Fix: `grid` with areas/columns on the existing parent.
3. **Stacking context** — z-index only competes with siblings in the same context; `transform`, `opacity < 1`, `filter`, `will-change`, and `position` + `z-index` each open a new one.
   Symptom: the dropdown or tooltip renders behind a neighbour however high its z-index goes.
   Tell: an ancestor reports one of those properties. Fix: remove it there, raise the ancestor, or portal the overlay to `body`.
4. **Overflow clipping** — `overflow: hidden|auto|clip|scroll` on an ancestor clips absolutely positioned or wide children and breaks `sticky` inside it.
   Symptom: a popover cut at the card edge; a shadow chopped; sticky does nothing.
   Tell: an ancestor between the element and the viewport is not `overflow: visible`. Fix: move the overflow to the element that actually scrolls; portal the overlay.
5. **Fixed vs sticky misuse** — `fixed` leaves the flow and needs reserved space; `sticky` needs a scrolling ancestor with room and no `overflow` in between.
   Symptom: a fixed header covers the first line of content; a sticky sidebar scrolls away or never sticks.
   Tell: `fixed` with content starting at `top: 0`; `sticky` under an `overflow` ancestor or in a parent no taller than itself. Fix: `sticky` + `top` for in-flow bars; `fixed` only for overlays, the flow padded by their height.
6. **Box-sizing / width math** — `width: 100%` plus padding or border overflows without `border-box`; `calc()` with the wrong unit or sign.
   Symptom: an element a few pixels wider than its parent forces a horizontal scrollbar.
   Tell: `box-sizing: content-box` on a `100%` element with padding. Fix: `border-box` in the base layer (Tailwind preflight does this); fix the calc.
7. **Flex `min-width: auto`** — a flex child refuses to shrink below its content width.
   Symptom: a long string or a wide table pushes the sidebar off-screen or overflows the card.
   Tell: the flex child reports `min-width: auto` and a `width` above its parent's content box. Fix: `min-w-0` on the flex child (`min-h-0` on the column axis), `overflow-x-auto` on the table wrapper.
8. **Breakpoint gap** — the rule exists at one width only.
   Symptom: right at 1440, wrong at 768; or wrong at exactly one pixel value.
   Tell: no rule applies at the failing width — `lg:grid-cols-[16rem_1fr]` with nothing at `md:`; `max-width: 768px` beside `min-width: 768px`. Fix: add the missing variant; mobile-first `min-width` only.

### 4. Fix at the source

- Change the container's constraint or the token that owns the behaviour, in the file that owns it.
- Delete the CSS your fix made dead: the old rule, the old variant, the old wrapper.
- Never: a margin or `absolute` hack on the child, `!important`, an inline style, a wrapper div, a
  more specific selector, a platform or width hack that hides the cause. Each one moves the bug
  (`code-rules` "Fix at the source"; where CSS lives: `css-architecture`).
- When the cause is in a shared shell or layout file, fix it there and say so: every route has it.

### 5. Verify

Re-render at 390 / 768 / 1440 through `/see` (`browser-verification` §7). Keep before and after
screenshots. Click the region's primary action and confirm it still works. Record a durable
cause as `[failure]` (`memory-system`) — say, a library wrapper that opens a stacking context.

## Exemplar: the sidebar pushed below the header

```text
WRONG (the child compensates for its parent)
  .sidebar { margin-top: -64px; position: absolute; left: 0; }
  → hides it at 1440, overlaps at 768, breaks again when the header height changes.

RIGHT (the shell owns the layout)
  Cause 2: the app shell is display:block, so header, sidebar, and main stack in flow.
  .app-shell {
    display: grid;
    grid-template-areas: "header header" "sidebar main";
    grid-template-columns: 16rem 1fr;
    grid-template-rows: auto 1fr;
    min-height: 100dvh;
  }
  Tailwind v4: min-h-dvh grid grid-rows-[auto_1fr] md:grid-cols-[16rem_1fr] on the shell.
  (Or the wrapper under the header was meant to be a flex row and lacks display:flex.)
  Then delete .sidebar's margin-top and position.
```

## Failure modes

- **Fixing the child, not the parent** — a negative margin or `absolute` on the sidebar hides the
  symptom at one width and leaves the shell wrong for everything else in it.
- **Stopping at the first change that "looks fixed" at one width** — the width you edited at is the
  one least likely to be broken; the cause is still there at 768.
- **Leaving the old rule in place** — dead CSS and two sources of truth; the next edit lands on the
  wrong one and the bug returns.
- **Adding a wrapper div to create the layout mode** — set `grid` or `flex` on the existing parent;
  a wrapper adds a node, a stacking candidate, and one more place to look.
- **Treating a stacking-context bug as a z-index number contest** — `z-9999` inside a transformed
  card still sits under the next card; find the ancestor that opened the context.

## Boundaries

Building new UI belongs to `frontend-design`; CSS organisation, layers, and naming to
`css-architecture`; render and inspect mechanics to `browser-verification`; the general bug method
(isolate, regression test) to `systematic-debugging`.

## Sub-files

| File | Read when |
|---|---|
| [components.md](./components.md) | The broken element is an app shell, sidebar, header, modal, dropdown, table, form, or toast |
