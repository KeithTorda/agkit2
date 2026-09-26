---
part: 18
title: Buttons and Actions
covers: button hierarchy, primary secondary tertiary, too many primaries, gradient and glow buttons, icon buttons, button sizes, loading buttons, disabled states, destructive buttons, link vs button, FABs, button groups, split buttons, action placement, bulk actions, keyboard shortcuts
---

# 18 — Buttons and Actions

Read when: adding any button, link-styled action, toolbar, action bar, row action, bulk action, FAB, button group or keyboard shortcut.

Button label wording (verbs, CTA text) lives in part 03. Button CSS values in general live in part 11. Hover and press motion lives in part 25. This part owns hierarchy, states, placement and behaviour.

## 18.1 Hierarchy

Three levels are enough: primary (filled with the primary token), secondary (outline or neutral fill), tertiary (text only). Destructive is a variant, not a fourth level.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Three or more primary buttons in one view | Every action shouts, none wins | One primary per view or per dialog. Others secondary or tertiary |
| Primary and secondary look almost the same (two shades of indigo) | No real hierarchy | Primary: filled `var(--color-primary)`. Secondary: `var(--surface)` with 1px `var(--border)`. Tertiary: text in primary color |
| Different CTA styles across pages (pill on home, square in app, gradient on pricing) | Each screen generated alone | One button style set for the whole app, defined in DESIGN.md. Original rule: one CTA style, no mixing |
| Five button variants (primary, secondary, tertiary, ghost, soft, outline, subtle, link) | UI-kit showcase copied in | Three variants plus destructive. Delete unused variants from the component |
| Colored buttons by meaning of the page (green on finance, orange on orders) | Color as decoration | Primary token everywhere. Color changes only for destructive (danger token) |
| Hero with "Get started" primary and "Learn more" secondary side by side | Landing template pair | One action that fits the page. If a second is needed, make it a text link. Labels in part 03 |
| Cancel given the primary style | Wrong emphasis | Cancel is secondary or tertiary |
| Primary action placed as a text link at the bottom while a decorative button sits at the top | Hierarchy inverted | Main task gets the primary style where the eye finishes the task |

## 18.2 Gradient, glow and decorative buttons

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `background: linear-gradient(135deg,#6366f1,#8b5cf6)` | The AI default button | Solid `var(--color-primary)` |
| Glow: `box-shadow: 0 0 20px rgba(99,102,241,0.5)` | Crypto-site look | No shadow, or the small elevation token from DESIGN.md |
| Shimmer sweep animation across the button | Aceternity/MagicUI copy | Static button. See part 10 |
| Animated border beam or rotating conic-gradient border | Showcase trope | 1px solid border for secondary; none for primary |
| Arrow icon that slides right on hover on every button | Template flourish | No icon, or a static trailing arrow only on links that go to another page |
| Tailwind `bg-gradient-to-r from-purple-500 to-pink-500 hover:scale-105 shadow-lg shadow-purple-500/50` | Class-soup signature | `bg-primary text-primary-foreground hover:bg-primary/90` using config tokens, or the project's `.btn-primary` |
| `hover:scale-105` / `transform: scale(1.05)` on hover | Jumpy, shifts layout neighbours | Background or opacity change: `.btn:hover { opacity: 0.9; }` or a darker token |
| `active:scale-95` press shrink on every button | Toy feel | Darker background on `:active`, or none |
| Pill-shaped (9999px) buttons in a data app with 4px inputs | Radius mismatch | Button radius equals input radius from DESIGN.md. Pills only if the whole system is pill |
| Buttons with 2 lines of text (title plus subtitle) | Card-button hybrid | One short label. Put detail next to the button |
| Emoji inside the label ("Launch 🚀") | Chat-tone UI | Plain label. See part 03 |
| Text in all caps with 0.1em tracking | Material v1 default | Sentence case |
| Uneven heights: text button 40px, icon button 36px, select 38px in one toolbar | Assembled from different kits | All controls in one row share one height token |

```css
/* Banned */
.btn-primary {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
  border-radius: 9999px;
  transition: all 0.3s;
}
.btn-primary:hover { transform: scale(1.05); }

/* Use */
.btn-primary {
  background: var(--color-primary);
  color: var(--color-on-primary);
  border: 1px solid transparent;
  border-radius: var(--radius-control);
  transition: background-color 120ms ease-out;
}
.btn-primary:hover { background: var(--color-primary-hover); }
.btn-primary:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
```

## 18.3 Sizes and targets

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Giant 56 to 64px buttons in an app UI | Landing-page sizing | 32 to 40px height on desktop app UI; 44px on touch |
| 24px-tall buttons in a mobile POS | Mis-taps with fingers | 44x44px minimum for touch targets, 48px+ for cashier screens used all day |
| Four sizes (xs, sm, md, lg, xl) all used on one page | No system | Two sizes: default and small (tables, toolbars). Large only for a single main action on mobile |
| Full-width buttons on desktop forms | Mobile habit on desktop | Width fits label plus padding; full width only under about 480px or in a narrow sheet |
| Buttons of different widths in one group forced equal with `w-full` grid | Stretched labels | Natural width, same height |
| Horizontal padding 40px on short labels ("OK") | Fat buttons | 12 to 16px horizontal padding, min-width 64 to 80px |
| Adjacent small buttons with 2px gap | Mis-taps | At least 8px between targets; WCAG 2.2 target size 24x24 minimum spacing rule |

## 18.4 Icon buttons

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Icon-only buttons with no accessible name | Silent to screen readers | `aria-label="Edit"` plus a tooltip; or a visible text label (preferred for less common actions) |
| Icon-only button for rare or ambiguous actions (archive vs download vs export icons) | Users guess | Text label, or icon plus text |
| Tooltip only on hover | No keyboard or touch access | Tooltip on focus as well; on touch, use visible labels |
| Mixed icon sets in one toolbar (Lucide + Heroicons + Font Awesome) | Assembled from snippets | One icon set. See part 26 |
| Icon buttons in colored circles (blue edit, red delete, green view) | Rainbow row | Neutral icon color; danger color only on hover/focus for delete, or keep neutral and confirm |
| 16px icon with a 16px hit area | Too small | Icon 16 to 20px inside a 32px (desktop) or 44px (touch) button |
| Custom icons for standard actions | Unfamiliar | Standard metaphors: pencil edit, trash delete, x close, magnifier search |
| `<i class="fa fa-trash" onclick=...>` | Not a button | `<button type="button" aria-label="Delete"><svg aria-hidden="true">...</svg></button>` |
| Toggle icon button (bold, pin, favorite) with no pressed state exposed | State unclear | `aria-pressed="true|false"` and a visible pressed style |

## 18.5 Loading buttons

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| No loading state; users click Pay three times | Duplicate orders | On click: disable, keep the width, show a spinner or "Saving...", re-enable on response |
| Button width jumps when label changes to "Loading..." | Layout shift | Keep min-width; overlay a spinner or swap to a same-length label |
| Spinner replaces the label entirely | Screen reader hears nothing | Keep text visible or use `aria-busy="true"` with visually hidden "Saving" text; announce result in a live region |
| Spinner shows for 50ms fast actions | Flicker | Show the spinner only after about 300ms. See part 25 |
| Loading text "Hang tight..." or "Working some magic..." | Chatty | "Saving...", "Sending...", "Processing payment..." |
| Button stays disabled forever on network error | No recovery | Re-enable on error and show the error message |
| Every button on the page disabled while one saves | Overreach | Disable only the triggering button and conflicting actions |
| Optimistic UI with no rollback | Lies on failure | Revert and show "Could not save" when the request fails |

## 18.6 Disabled states

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Disabled with no explanation | User cannot tell why | Keep enabled and explain on click; or show the reason as text next to the button ("Add an item to check out") |
| Disabled button at 30% opacity, unreadable | Fails comprehension | Disabled token from DESIGN.md; text still legible. Disabled controls are exempt from contrast rules but should stay readable |
| Disabled buttons with `cursor: not-allowed` and no tooltip | Half-done | Visible reason text; tooltip on a wrapper if the button is disabled (disabled elements do not get focus) |
| `disabled` on a link (`<a disabled>`) | Attribute does nothing | Remove the `href` and render text, or use a real button |
| Paid features shown as disabled buttons with a lock icon everywhere | Nag UI | Show the feature once with a plain upgrade link. See part 05 for plan copy |
| `aria-disabled` without blocking the click | Still fires | With `aria-disabled="true"`, guard the handler |

## 18.7 Destructive actions

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Delete button as prominent red primary next to Save | Invites mistakes | Delete as secondary or text with danger color, placed apart from Save (other side or bottom of the page) |
| Confirm dialog for every action, even safe ones | Confirmation fatigue | Confirm only destructive or irreversible actions. Reversible ones get an Undo. See part 21 |
| "Are you sure?" with Yes / No buttons | Buttons do not say what happens | Buttons name the action: "Delete product" / "Cancel" |
| Destructive confirm defaults focus to the Delete button | Enter deletes | Focus the Cancel button or the dialog heading |
| Type-the-name confirmation for deleting a draft | Friction theatre | Typed confirmation only for high-impact deletes (whole project, database, all records of a barangay) |
| Red "Danger Zone" box with warning icons | GitHub copy | "Delete account" section at the bottom of settings with one confirmation. See part 23 |
| Delete icon on every row visible at all times, next to Edit | Accidental taps | Put Delete inside a row menu or on the detail page; see 18.10 |
| Void/refund in POS as a one-tap button | Cash control risk | Require a reason and, if the client's policy says so, a supervisor PIN |
| Soft-delete labelled "Delete" when records go to an archive | Mislabelled | "Archive" when reversible; "Delete permanently" when not |

## 18.8 Link vs button

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `<a href="#" onclick="...">` as a button | Wrong element, adds `#` to URL | `<button type="button">` for actions |
| `<button onclick="location.href='/orders'">` | Navigation hidden in JS; no open-in-new-tab | `<a href="/orders">` styled as a button if it needs button weight |
| `<div class="btn" onclick>` | No keyboard, no role | Real `<button>`. See part 27 |
| `<a>` without `href` styled as a button | Not focusable | Add `href` for navigation or change to `<button>` |
| Link styled as a filled button in body text | Visual confusion | Links in prose look like links: underlined, primary text color |
| "Click here" links | Meaningless out of context | Link text names the destination. See part 03 |
| External links that open new tabs silently | Unexpected | Open in the same tab by default; if a new tab is required, add "(opens in new tab)" visually hidden or visible, plus `rel="noopener"` |
| Download action as a `<button>` that triggers JS fetch | Breaks right-click save | `<a href="/files/report.pdf" download>` with file type and size: "Download (PDF, 240 KB)" |

## 18.9 Placement

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Primary action top-right on some pages, bottom-left on others | No rule | Page-level actions in the page header (right of the title). Form submit at the end of the form. Write the rule in DESIGN.md |
| Dialog buttons centered and stacked full width on desktop | Mobile layout on desktop | Right-aligned in dialog footer on desktop; stacked full width under 480px |
| Primary action hidden in a kebab menu | Main task buried | The one main action is a visible button; secondary actions go in the overflow menu |
| "Quick actions" card on the dashboard duplicating the nav | Filler card | Put actions where the object lives (Add product on the products list). See part 22 |
| Floating "Chat with us" bubble covering the Save button on mobile | Overlap | Remove the widget from app screens or offset it; never over primary actions |
| Sticky bottom action bar plus a FAB plus a header button for the same action | Tripled | One placement per action per screen |
| Back button that is a large filled primary | Wrong weight | Back as a text link with a left arrow or a browser-native back; see part 16 |
| Mobile primary action at the top of a long form | Thumb reach | Bottom of the form, or sticky bottom bar on long mobile forms |

## 18.10 Row actions and bulk actions

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| View, Edit, Delete icon buttons on every table row | Visual noise; action column wider than data | Row click opens the record (make the name a link); secondary actions in one overflow menu per row |
| Action buttons shown only on row hover | Invisible on touch and to keyboard users | Overflow button always visible (can be muted), or actions revealed on focus-within too |
| Row checkbox selection with no bulk action bar | Selection does nothing | Bulk bar appears on first selection: "3 selected" plus actions plus "Clear" |
| Bulk bar that covers the table header or pagination | Overlap | Replace the table toolbar in place, or a sticky bar at the bottom that reserves space |
| "Select all" selects only the visible page with no notice | Surprise scope | "25 on this page selected. Select all 1,240 orders" link |
| Bulk delete with no count in the confirmation | Unknown scope | "Delete 12 products? This cannot be undone." |
| Bulk actions offered that fail on some rows silently | Partial success hidden | Report "10 archived. 2 could not be archived: already paid." with a link to those rows |
| Checkbox column on tables that have no bulk action | Leftover template | Remove the checkbox column |

## 18.11 Button groups, segmented controls and split buttons

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Segmented control used for navigation between pages | Looks like a filter | Tabs or links for navigation; segmented control for switching views of the same data (List / Grid, Day / Week) |
| Segmented control with 6+ segments | Crowded, labels truncate | Select or tabs |
| Selected segment shown only by a slightly different gray | State unclear | Clear selected fill token plus `aria-pressed` or `aria-selected` |
| Split button (main action plus chevron) for 2 options | Complexity for little gain | Two buttons, or one button plus a text link |
| Split button where the chevron and main area are one hit target | Wrong action fires | Separate targets with a divider; chevron has `aria-label="More save options"` |
| Button group with mixed variants (primary, outline, ghost side by side) | Messy | Same variant within a group |
| Toolbar of 12 icon buttons in a row | Everything visible, nothing findable | 3 to 5 common actions visible, rest in "More" |

## 18.12 FABs and floating actions

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Floating action button on desktop web | Android pattern on the web | Primary button in the page header |
| FAB with a speed-dial of 5 actions | Hidden actions | Separate visible buttons or a menu |
| FAB with gradient and glow, pulsing | Trope stack | If a FAB fits (mobile list screens), solid primary token, 56px, `aria-label`, no pulse |
| FAB covering the last list item and pagination | No bottom padding | Add bottom padding equal to FAB size plus 16px |
| Back-to-top floating button on a 2-screen page | Filler | Remove unless page is over about 5000px. See part 16 |

## 18.13 Feedback after actions

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Success toast for every click, including expected navigation | Noise | Toast only for async or background results; visible state change is enough otherwise. See part 21 |
| Confetti after creating a record | Celebration trope | Show the created record |
| Button label changes to "Done ✓" and stays | Stale state | Revert after about 2s or navigate |
| "Copied!" tooltip that never disappears | Stuck state | Swap label to "Copied" for about 2s, announce via `aria-live="polite"` |
| Destructive action with no undo and no confirm | Data loss | Undo toast for reversible deletes (8s minimum), confirm for irreversible |
| Undo toast that lasts 3 seconds | Too short | 8 seconds minimum; pause on hover and focus |

## 18.14 Keyboard shortcuts

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Shortcut hints (`⌘K`, `⌘S`) shown for shortcuts that are not implemented | Copied from demos | Show a hint only after wiring the shortcut |
| Mac-only symbols shown to Windows users (most PH office and school PCs) | Wrong platform | Detect platform: "Ctrl+S" on Windows/Linux, "⌘S" on macOS |
| Single-letter shortcuts that fire while typing in inputs | Typing "d" deletes a row | Ignore shortcuts when focus is in an input, textarea or contenteditable; or use modifier keys. WCAG 2.1.4 |
| Overriding browser shortcuts (Ctrl+F, Ctrl+P, Ctrl+W) | Breaks expectations | Leave browser shortcuts alone unless the app replaces the function fully (e.g. print a receipt) |
| No list of shortcuts | Undiscoverable | "?" opens a shortcut list, or a Keyboard shortcuts page in help |
| POS with mouse-only checkout | Slow for cashiers | Keyboard flow: barcode input focused by default, F-keys or Enter for pay, Esc to cancel. Document the keys on screen |
| Shortcut labels as fancy `<kbd>` pills with gradients and shadows | Decoration | Plain `<kbd>` with a 1px border token |

## 18.15 Philippine context

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Pay with GCash" button using a made-up GCash-like blue gradient and logo | Brand impersonation | Use the provider's official button assets per their brand guide, or a neutral button "Pay with GCash" plus the official logo file supplied by the provider |
| Payment buttons with no amount | User unsure what they pay | "Pay ₱1,250.00" on the final pay button |
| "Buy Now" and "Add to Cart" both primary on a product page | Two primaries | One primary ("Add to cart" for shops, "Buy now" for single-item sales), the other secondary |
| "Submit" on a barangay request with no indication of what happens next | Anxiety | Label the action ("Send request"), then show the reference number and pickup details |
| Print button missing on receipts, clearances, certificates | Users screenshot | "Print" button that opens a print stylesheet; also "Download PDF" when an official copy is needed |
| Taglish button labels mixed randomly ("I-save", "Delete", "Ipasa") | Mixed register | One language per UI, or consistent bilingual rule. See part 09 |

## 18.16 Stack-specific tells

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| shadcn `<Button>` with `variant="default"` untouched: black button on white in every project | Library default look | Map `default` variant to the project's primary token in the theme |
| Every shadcn variant used on one page (default, secondary, outline, ghost, link, destructive) | Showcase | Use 3 plus destructive |
| Bootstrap `btn btn-primary btn-lg rounded-pill shadow` stacked classes | Override soup | Customise `$btn-*` Sass variables; use `btn btn-primary` |
| Bootstrap `.btn-success` for Save, `.btn-info` for View, `.btn-warning` for Edit | Rainbow by action | `.btn-primary` for the main action, `.btn-outline-secondary` for the rest, `.btn-outline-danger` for delete |
| Tailwind buttons with 15+ utility classes repeated on every button | Class soup | One Button component or one `.btn` class with `@apply`-free component CSS. See part 29 |
| React `onClick` on `<div>` with `role="button" tabIndex={0}` and keydown handlers | Rebuilt button | `<button>` |
| `<Button asChild><a>` misused so links lose `href` | Broken navigation | Keep `href` on the anchor |
| Framer Motion `whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}` on all buttons | Motion trope | Remove. CSS color transition only |

## 18.17 Check
- [ ] One primary button per view or dialog.
- [ ] Three variants plus destructive; unused variants removed.
- [ ] One button style set app-wide, defined in DESIGN.md.
- [ ] No gradient, glow, shimmer, beam border or scale-on-hover buttons.
- [ ] Button radius and height match inputs in the same row.
- [ ] Buttons are 32 to 40px on desktop, 44px+ on touch, 8px+ apart.
- [ ] Every icon-only button has an accessible name and a tooltip on hover and focus.
- [ ] Toggle buttons expose `aria-pressed`.
- [ ] Buttons show a loading state after about 300ms and block double submit.
- [ ] Loading buttons keep their width and re-enable on error.
- [ ] Disabled buttons have a visible reason, or stay enabled and explain on click.
- [ ] Destructive buttons are separated from Save and named for the action.
- [ ] Confirm dialogs only for irreversible actions; focus starts on Cancel.
- [ ] Reversible deletes offer Undo for 8s or longer.
- [ ] Actions use `<button>`; navigation uses `<a href>`; no `<div>` or `href="#"` buttons.
- [ ] Downloads are links with file type and size.
- [ ] Page actions sit in the page header; form actions at the end of the form, same rule everywhere.
- [ ] Main action is visible, not inside a kebab menu.
- [ ] Rows use a link on the name plus one overflow menu, not three icon buttons.
- [ ] Row actions are reachable without hover.
- [ ] Bulk bar appears on selection with a count and Clear; "select all" states its scope.
- [ ] Bulk results report partial failures.
- [ ] No checkbox column without bulk actions.
- [ ] Segmented controls switch views, not pages; max about 5 segments.
- [ ] No FAB on desktop; mobile FABs do not cover content.
- [ ] No confetti or celebration after actions.
- [ ] Shortcut hints only for implemented shortcuts, platform-correct (Ctrl vs ⌘).
- [ ] Single-key shortcuts do not fire inside inputs.
- [ ] POS screens support keyboard and barcode flow.
- [ ] Pay buttons show the ₱ amount; payment brand assets are official files.
- [ ] Printable documents have a Print button.
- [ ] Library default button variants are mapped to project tokens.
