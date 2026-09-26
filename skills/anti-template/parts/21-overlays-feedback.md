---
part: 21
title: Overlays and Feedback
covers: modals, dialogs, drawers, sheets, popovers, tooltips, dropdown menus, toasts, alerts, banners, inline messages, progress, spinners, skeletons, confirmations, undo
---

# 21 — Overlays and Feedback

Read when: building any modal, drawer, popover, tooltip, menu, toast, alert, banner, loading state, confirmation or undo flow.

Wording of toasts, errors, confirm text and loading text is in part 03. Error pages and empty states are in part 04. Animation timing detail is in part 25. This part covers when to use each overlay or feedback element, how it behaves, and how it is built.

## 21.1 Choosing the right container

AI output reaches for a modal first. Pick the lightest container that does the job.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Modal for everything (view, edit, create, filter, help) | Template default; hides the page the user was working on | Inline edit for 1–2 fields, a page for 4+ fields, a modal only for short focused tasks and destructive confirms |
| Modal to view a record's details | Blocks the list, no URL, cannot share or open in a new tab | Detail page with its own URL, or an expandable row / side panel |
| Form with more than 3 fields in a modal | Scrolling inside a small box, lost on accidental backdrop click | Dedicated page (`/students/new`) with Save and Cancel |
| Modal chains (modal opens a modal) | No clear way back, focus management breaks | Flat flow: close the first, then open the next; or make it a page with steps |
| Multiple overlapping modals | Stacked backdrops, two Escape presses, z-index fights | Max 1 modal open at a time |
| Full-screen modal for a 2-field form on desktop | Feels like a page that forgot its URL | Centered modal, 480–560px wide |
| Scrollable modal taller than the viewport | Header and buttons scroll out of view | Make it a page; or keep header and footer fixed and scroll only the body, max-height `calc(100dvh - 64px)` |
| Drawer used for a full create form on desktop | Squeezed 360px column of fields | Page for create; drawer only for quick view or filters |
| Popover holding a whole form | Closes on outside click and loses input | Modal or page |
| Tooltip holding essential instructions | Hidden on touch, missed by most users | Helper text under the field |
| Toast used for validation errors | Error is far from the field and disappears | Inline error under the field, summary at top of form |
| Banner for a one-time success | Pushes layout down for something that needs no action | Toast, or nothing if the change is visible |
| Alert box for static page info ("Welcome to the dashboard") | Noise styled as a warning | Delete it, or plain paragraph text |

Decision order: inline change on the page, then a page, then a drawer or popover, then a modal. Use a modal only when the user must decide before continuing.

## 21.2 Modal behaviour

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Tiny gray X as the only way out | Hard to hit, missed on mobile | Visible Cancel button plus X (min 24x24, ideally 44x44 hit area) plus Escape |
| Backdrop click does nothing | Fights the user; common library default left on `static` | Backdrop click closes; keep it disabled only when unsaved input would be lost or the action is mid-flight |
| Backdrop click closes a form with typed input and loses it | Data loss | If the form is dirty, ask "Discard changes?" or keep the modal open |
| Scale + fade entrance at 300ms+ with bounce | Showy; slows every open | Instant, or 150ms opacity fade. See part 25 |
| Blurred backdrop (`backdrop-filter: blur(8px)`) | Glassmorphism tell; costly on low-end Android | Solid scrim, `var(--color-overlay)` at about 40–60% opacity |
| Modal centered with an icon in a colored circle on top | SweetAlert / template look | Title first, text, buttons. No hero icon; for destructive, the red button is enough |
| Title "Are you sure?" | Says nothing about what happens | Title names the action and object: "Delete 3 students?" |
| Buttons "Yes" / "No" | User must reread the question | Verb buttons: "Delete students" / "Cancel" |
| Button order changes between modals | Muscle memory breaks | One order app-wide. Common: secondary left, primary right, both right-aligned |
| Primary and destructive buttons both filled and same weight | No hierarchy | One filled primary (or danger) button; Cancel as secondary/ghost |
| Focus not moved into the modal on open | Keyboard and screen reader users stay on the page behind | Focus the first field, or the least destructive button for confirms |
| Focus not returned to the trigger on close | User lands at top of page | Return focus to the element that opened it |
| Page behind still scrolls | Scroll bleed on mobile | Lock body scroll while open; native `<dialog>` with `showModal()` handles inert background |
| No `aria-labelledby` / title element | Announced as "dialog" with no name | `aria-labelledby` pointing to the visible title |
| `role="dialog"` on a div with no focus trap | Tab escapes into the page | Native `<dialog>` + `showModal()`, or a library that traps focus |
| Modal opened on page load (newsletter, promo, "What's new") | Interrupts before the user did anything | No auto-open modals. Put announcements in a dismissible banner or a changelog link |
| Modal opened on exit intent | Dark pattern | Remove |
| Modal width 900px+ for a confirm | Huge box with one sentence | 400–480px for confirms, 560–640px for short forms |
| Rounded 24px corners, 2xl shadow | Toy look | Radius token from DESIGN.md (often 8px), one soft shadow token |
| Close X positioned outside the box, top right of screen | Lightbox habit applied to forms | X inside the header, aligned with the title |
| Modal body with its own card inside | Card inside card | Content directly in the modal body |
| Success modal after save ("Success! Your data has been saved") | Extra click to dismiss good news | Close the modal and show a toast or the updated row |
| Modal that cannot be closed while a request runs, with no progress | Looks frozen | Disable the primary button, show spinner inside it, keep Cancel if the request can be aborted |

## 21.3 Modal code

```html
<!-- Banned: div modal with fake backdrop, no focus handling -->
<div class="modal-overlay" onclick="closeModal()">
  <div class="modal glass rounded-3xl shadow-2xl animate-bounce-in">
    <div class="icon-circle bg-gradient-to-r from-purple-500 to-pink-500">✨</div>
    <h2>Are you sure?</h2>
    <p>This action cannot be undone!</p>
    <button onclick="closeModal()">No</button>
    <button onclick="doIt()">Yes!</button>
  </div>
</div>
```

```html
<!-- Use: native dialog, named title, verb buttons -->
<dialog id="delete-student" aria-labelledby="delete-student-title">
  <form method="dialog">
    <h2 id="delete-student-title">Delete Juan Dela Cruz?</h2>
    <p>His grades and attendance for SY 2025–2026 will also be deleted.</p>
    <div class="dialog-actions">
      <button value="cancel" autofocus>Cancel</button>
      <button value="confirm" class="btn-danger">Delete student</button>
    </div>
  </form>
</dialog>
```

```css
/* Banned */
.modal-overlay { backdrop-filter: blur(12px); background: rgba(15, 23, 42, 0.6); }
.modal { animation: pop 400ms cubic-bezier(.68,-0.55,.27,1.55); z-index: 99999; }

/* Use */
dialog::backdrop { background: var(--color-overlay); }
dialog { border: 1px solid var(--color-border); border-radius: var(--radius-md);
  max-width: min(560px, calc(100vw - 32px)); padding: var(--space-6); }
```

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `z-index: 9999` / `99999` on modal | Arms race with other layers | Z-index scale token: `--z-dropdown`, `--z-sticky`, `--z-modal`, `--z-toast` |
| Modal markup copied into every page | Duplicated IDs, drift | One dialog component, content passed in |
| `display: none` toggled with no focus or ARIA work | Inaccessible | `<dialog>` element or a tested library (Radix, Headless UI, Bootstrap modal with defaults left on) |
| Bootstrap: `data-bs-backdrop="static"` on every modal | Traps users for no reason | Default backdrop; `static` only when unsaved input or running action |
| Bootstrap: `.modal-lg` for a two-line confirm | Oversized | `.modal-sm` or default size |
| Bootstrap: `.fade` left on but `.modal-dialog-centered` plus custom keyframes | Double animation | Keep one: Bootstrap default fade, or none |
| React: modal open state held in a global store for a single page | Over-engineering | Local state in the page that owns the modal |
| React: modal rendered inside a `transform`ed parent without a portal | Clipped, wrong stacking | Render in a portal (`createPortal`) or use `<dialog>` top layer |
| shadcn `Dialog` shipped with default copy "Are you absolutely sure?" | Template text left in | Replace title and description with the real action |
| SweetAlert2 default success icon with animated check for every save | Loud template look | Toast or inline confirmation; keep SweetAlert out of admin CRUD |

## 21.4 Confirmations

Confirm only when the action destroys data, costs money, sends something to other people, or cannot be reversed. Wording rules are in part 03.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Confirm dialog for safe or reversible actions (save, archive, mark read) | Friction; trains users to click through | Just do it; offer Undo in a toast |
| No confirm for real destructive actions (delete voter record, void OR, reset grades) | Loses data | Confirm with the object named and the consequence stated |
| "This action cannot be undone" when it can (soft delete, trash) | False alarm | State what really happens: "Moved to Trash. Deleted permanently after 30 days." |
| Type-to-confirm for low-stakes deletes | Heavy ceremony copied from GitHub repo deletion | Type-to-confirm only for bulk or irreversible deletes of important data (whole school year, a barangay's resident list) |
| Type-to-confirm asks for the word "DELETE" | Tests typing, not attention | Ask for the object name: "Type the section name (Grade 7 – Sampaguita) to confirm" |
| Confirm that repeats the button text only ("Delete? [Delete]") | No new information | Add count, names, and side effects: "3 receipts will be voided and removed from today's Z-reading." |
| Destructive button is the default focused / Enter-activated | One keypress destroys data | Autofocus Cancel on destructive dialogs |
| Destructive button colored the same as primary | Danger not signalled | Danger token (`var(--color-danger)`) for the destructive button only |
| Double confirm (dialog, then "Are you really sure?") | Distrust of own UI | One confirm, clearly worded |
| Browser `confirm()` / `alert()` in a production app | Unstyled, cannot name buttons, blocks the thread | Custom dialog with verb buttons |
| Confirm on logout | Nobody loses data by signing out | Sign out directly. Confirm only if there is unsynced offline data (POS) |
| Checkbox "Don't ask me again" on a destructive confirm | Removes the safety for good | Only on non-destructive nags; none on deletes |
| Money actions with no confirm (refund, payout, void) | Real cost | Confirm with amount in ₱ and recipient: "Refund ₱1,250.00 to Maria Santos via GCash?" |
| Sending actions with no preview (SMS blast to 2,000 residents) | Cannot be recalled | Confirm with count and a preview of the message; show estimated SMS credits |

## 21.5 Drawers and sheets

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Drawer slides in from the right for every detail view | Default admin template | Detail page for deep records; drawer for quick peek while keeping the list visible |
| Drawer width 90vw on desktop | A modal pretending to be a drawer | 360–480px for peek, up to 640px for rich detail |
| Drawer with no URL change for a record | Cannot link, refresh loses it | Update the URL (`?student=123`) so refresh and back work |
| Drawer and modal both open | Two overlays | One overlay at a time |
| Bottom sheet on desktop | Mobile pattern on a wide screen | Bottom sheet below 768px; popover or modal above |
| Bottom sheet without a drag handle or close button | Users do not know how to dismiss | Visible close button; drag handle optional |
| Bottom sheet covering 100% height with no top gap | Looks like a new page with no back | Leave a visible gap at top, or make it a page |
| Filter drawer that applies on every change and closes | Jumps and loses place | Apply button and Clear button at the bottom; show result count on the Apply button: "Show 42 results" |
| Mobile nav drawer with blurred backdrop and slide + fade + scale | Stacked effects | Solid scrim, 150–200ms slide. See part 16 for nav content |
| Drawer content not scrollable independently of header | Save button scrolls away | Sticky drawer header and footer, scrolling body |
| Offcanvas (Bootstrap) used as main navigation on desktop | Hides navigation for no reason | Visible sidebar or top nav on desktop, offcanvas under 992px only |

## 21.6 Popovers and dropdown menus

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Dropdown menu for 2 actions | Extra click | Show both actions as buttons |
| Kebab (three dots) menu holding the only primary action | Action hidden | Primary action as a visible button; overflow menu for rare actions |
| Every row with a kebab menu containing View / Edit / Delete | Template CRUD table | Row click opens the record; Edit on the detail page; Delete in the detail page or bulk bar. See part 19 |
| Menu items with an icon on every line | Visual noise | Icons only where they aid scanning; text alone is fine |
| Destructive item mixed mid-list with no separator | Easy misclick | Destructive item last, after a divider, in danger color |
| Menu opens on hover | Closes when the pointer drifts; no touch support | Open on click/tap; keyboard with Enter/Space/ArrowDown |
| Menu without keyboard support (arrow keys, Escape) | Div list with click handlers | `role="menu"` with arrow-key handling via a library, or a plain list of buttons in a popover |
| Popover arrow/caret plus shadow plus border plus blur | Four effects on one small box | Border and one small shadow token; arrow optional |
| Popover that does not flip at the viewport edge | Cut off on small screens | Use a positioning library (Floating UI) or the Popover API with anchor fallback |
| Select-like dropdown built from divs for 5 fixed options | Reinvents `<select>` | Native `<select>`. See part 17 |
| User menu with "My Profile", "My Account", "My Settings" as three items | Duplicate destinations | One "Account" or "Settings" item, plus "Sign out" |
| Mega dropdown with icons, descriptions and a featured card for 6 links | Marketing template in an app | Plain list. See part 16 |
| Dropdown width fixed at 200px truncating Filipino labels | Tagalog strings are longer | `min-width` plus `width: max-content`, wrap long labels |
| Popover content lost on outside click while typing | Data loss | Popovers hold no input beyond a single search box; forms go in modals or pages |

## 21.7 Tooltips

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Tooltips on elements that already have visible labels | Repeats the label ("Save" tooltip on a Save button) | No tooltip |
| Tooltip as the only label for icon-only buttons on touch UIs | Hover does not exist on phones | Visible text label, or `aria-label` plus tooltip on desktop and label on mobile |
| "Pro tip!" / "Did you know?" tooltips | Chatty | State the fact: "Shortcut: Ctrl+S" |
| Tooltip with a paragraph of help text | Too long to read before it closes | Max about 80 characters; longer help goes in helper text or a docs link |
| Tooltip containing links or buttons | Cannot be reached before it closes | Use a popover (click-triggered) for interactive content |
| Info (i) icon next to every field label | Help hidden behind hover everywhere | Helper text under the field for the 1–2 fields that need it |
| Tooltip delay 0ms flashing on every mouse pass | Flicker across toolbars | About 300–500ms show delay, 0ms when moving between adjacent tooltips |
| Tooltip on disabled button explaining nothing | User cannot learn why | Explain why in text near the button: "Add at least 1 item to checkout" |
| Tooltip on a disabled `<button>` that never fires | Disabled elements do not get pointer events | Wrap in a span that receives focus, or use `aria-disabled="true"` instead of `disabled` |
| Dark tooltip with gradient background and glow | Visual trope on a utility element | Solid token background, small radius, no shadow or one small shadow |
| Tooltip not reachable by keyboard | Mouse-only | Show on focus as well as hover; dismiss on Escape |
| Tooltips on truncated table cells with no other way to read the text | Unreadable on touch | Wrap text, or show full value on the detail page |
| `title` attribute used as the tooltip system | Slow, unstyled, inconsistent, not on touch | Proper tooltip component, or visible text |

## 21.8 Toasts

Toast wording is in part 03. This section covers when and how toasts appear.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Success toast after every expected action (save a field, toggle a checkbox) | Noise; the change is already visible | Skip. Toast only for background, async or off-screen results ("Report ready. Download"), or when Undo is offered |
| Auto-dismissing error toasts | User misses what failed | Errors persist until dismissed, or show inline next to the cause |
| Toast stack of 5+ | Wall of notices | Max 3 visible; newer replaces older of the same kind; collapse duplicates ("Saved (3)") |
| Toast position varies by page | No place to look | One position app-wide. Bottom-left or bottom-center on desktop; bottom-center above the tab bar on mobile. Top-right is fine if used everywhere |
| Full-width banner toast | Looks like a system outage | 300–400px wide, max 2 lines |
| Undo toast shown for 3s | Too short to read and act | 8s minimum, longer (10–15s) for bulk actions; pause timer on hover and focus |
| Emoji or icon-in-circle in every toast | Template toasts | Small status icon only for error and warning, or none |
| Green/red full-color toasts (Sonner `richColors`, toastify colored theme) | Loud | Neutral surface with a status icon or left border in the status token |
| Progress bar countdown line on every toast | react-toastify default left on | Hide the progress bar (`hideProgressBar`) |
| Toast that covers the Save button or the mobile tab bar | Blocks the next action | Offset from fixed UI; respect safe-area insets |
| Toast with a Close button and auto-dismiss 2s | Cannot reach the button | Either persistent with Close, or auto-dismiss 5s+ with no action |
| Toast as the only record of an important event (payment received) | Gone once dismissed | Also log it: notification center, activity feed, or the record itself |
| Toast on page load ("Welcome back, Keith") | Greeting as noise | None |
| Toast not announced to screen readers | Silent to assistive tech | Container with `role="status"` (`aria-live="polite"`); errors `role="alert"` |
| Toast library added for one message | Dependency for one line | A small `role="status"` region you write yourself, or the library already in the stack |
| Toasts animating in with slide + bounce + scale | Motion stack | 150–200ms fade or short slide. See part 25 |

```js
// Banned: library defaults left on
toast.success("🎉 Saved successfully!", { position: "top-right", autoClose: 2000,
  theme: "colored", hideProgressBar: false, transition: Bounce });

// Use: one position set once, quiet style, toast only when useful
toast("Report ready.", { action: { label: "Download", onClick: download } });
```

## 21.9 Alerts, banners and inline messages

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Alert boxes stacked at the top of every page ("Tip", "Note", "Info") | Decoration styled as warnings | Only show an alert when there is something the user must know or do now |
| Info alert with icon, title, body and a "Learn more" link for one sentence | Over-built | One line of text with the status icon, or plain text |
| Every alert dismissible, including critical ones | User hides a real problem | Critical alerts (account suspended, unpaid invoice, election day lock) stay until resolved |
| Dismissed banner comes back on every page load | Dismissal not stored | Store dismissal per user (server) or per browser (try/catch localStorage) |
| Site-wide banner with a marquee/scrolling ticker | Old portal / LGU template look; hard to read | Static one-line banner with a link to the full notice |
| Announcement banner in gradient with "NEW" pill and emoji | Launch-page trope | Solid neutral or info token background, plain text, one link |
| Two or three banners stacked (cookie + promo + maintenance) | Top of page is all notices | One banner at a time, by priority: outage, then account issue, then announcement. Cookie notice at bottom |
| Banner pushes content down after load (layout shift) | Page jumps | Reserve space server-side, or render it in the first paint |
| Status shown only by color (green/red box, no text) | Fails color-blind users and WCAG 1.4.1 | Text plus icon plus color: "Error: Payment failed" |
| Alert inside a card inside a modal | Nested containers | Alert directly in the modal body, above the buttons |
| Inline error message far from its field (form top only) | Users hunt for the problem | Error under the field, plus a linked summary at top for long forms. See part 17 |
| Inline success message that pushes the form down on every save | Layout jump | Short "Saved" text next to the Save button, fading after 3–5s, or a toast |
| Warning color used for neutral info | Dilutes warning meaning | Info for info, warning only for risk |
| Alert with `role="alert"` on static text rendered at load | Screen readers interrupt on every page | `role="alert"` only for messages inserted after an action; static notices need no role |
| Bootstrap `.alert-dismissible` with `.fade .show` on everything | Template default | Plain `.alert` without dismiss for persistent notices |
| Offline banner that says "You're offline 📡" and hides the app | Blocks work | "No connection. Changes will sync when you're back online." Keep the app usable where possible (POS, attendance). Wording in part 04 |
| Maintenance banner with no time | Useless | Include the window in local time: "Maintenance Sat 25 Oct, 10:00 PM–12:00 AM (PHT)." |

## 21.10 Loading: spinners, progress bars, skeletons

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Spinner shown for responses under 200ms | Flash of spinner on every click | Delay showing loading UI by about 200ms; if data arrives first, show nothing |
| Skeleton for content that loads in under 500ms | Shimmer flash | Skeleton only when load is usually longer than 500ms |
| Shimmer animation on skeletons | Template look; motion for no reason | Static muted blocks; honor `prefers-reduced-motion` if shimmer is kept |
| Skeleton that does not match the final layout | Layout shift when data lands | Skeleton rows the same height and column count as real rows |
| Skeleton with avatar circles and 3 text bars for a table | Generic card skeleton everywhere | Table skeleton: header row real, 5–10 body rows of muted bars |
| Full-page spinner overlay for a small section update | Blocks the whole app | Load only the region that changes; keep the rest interactive |
| Spinner with "Hang tight! Magic is happening ✨" | Chatty. See part 03 | Spinner alone, or "Loading students…" |
| Custom SVG spinner with gradient stroke and glow | Visual trope | Simple ring or the design system's spinner, `currentColor` |
| Three bouncing dots for every load | Chat-typing indicator reused | Spinner or progress bar; dots only for "someone is typing" |
| Progress bar for a single-step action | Fake progress | Spinner in the button, or nothing |
| Fake progress bar that climbs to 90% and waits | Invented progress | Real percent when known (upload bytes, rows processed); indeterminate bar when not |
| Progress shown as percent only for long jobs | No sense of scale | "Importing 1,240 of 3,500 residents" plus a bar |
| Long job (CSV import, report, SMS blast) blocking the page with a spinner | User cannot leave | Run in background, show a status row or notification when done |
| Button loses its label when loading (spinner replaces text) | Button width jumps, user forgets what they clicked | Keep the label, add a spinner, set `aria-busy="true"`, disable repeat clicks: "Saving…" |
| No loading state at all; double submits | Duplicate records, double charges | Disable submit while pending; make the endpoint idempotent. See part 18 |
| Loading state never times out | Endless spinner on bad network | After about 15s show "Still loading. Check your connection or retry." with Retry |
| Page-level top progress bar (NProgress) plus spinner plus skeleton together | Three indicators for one load | One indicator per load |
| `animate-pulse` on real content, not placeholders | Content looks unloaded | Pulse only on placeholders, if at all |
| Lottie animation as a loader | Heavy JSON + runtime for a spinner | CSS spinner. See part 25 |

```css
/* Banned: shimmer skeleton on everything */
.skeleton { background: linear-gradient(90deg,#eee 25%,#f5f5f5 50%,#eee 75%);
  background-size: 200% 100%; animation: shimmer 1.2s infinite; }

/* Use: static placeholder, same size as the real row */
.skeleton { background: var(--color-surface-muted); border-radius: var(--radius-sm); }
.skeleton-row { height: var(--row-height); }
```

```js
// Use: delay the spinner so fast responses never show it
const timer = setTimeout(() => setShowSpinner(true), 200);
try { await load(); } finally { clearTimeout(timer); setShowSpinner(false); }
```

## 21.11 Undo and optimistic updates

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Confirm dialog where Undo would do | Friction on reversible actions | Do it, show "Archived. Undo" toast for 8s+ |
| Undo toast that does not actually undo (UI only, server already deleted) | Fake safety | Delay the server delete until the toast expires, or soft-delete and restore on Undo |
| Undo offered for actions with side effects already sent (SMS, email, payment) | Cannot be recalled | No Undo; confirm before sending instead |
| Undo lost when the user navigates away | Toast tied to the page | Keep the toast in an app-level region so it survives route changes |
| Optimistic update with no rollback on failure | UI shows saved data that is not saved | Roll back and show an error with Retry next to the item |
| Optimistic update for money or votes | Shows a balance or tally that may be wrong | Wait for server confirmation on payments, stock counts at checkout, election tallies |
| Keyboard shortcut Ctrl+Z not supported where Undo is offered | Partial undo | Support Ctrl+Z / Cmd+Z for the last action when the page has an undo stack |
| "Deleted" with no way back and no trash | Permanent by accident | Trash or archive for user content; permanent delete from there |

## 21.12 Stack-specific tells

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Tailwind: `fixed inset-0 bg-black/50 backdrop-blur-sm` on every overlay | Copied Tailwind UI snippet | `bg-[var(--color-overlay)]` or a theme color; drop the blur |
| Tailwind: `rounded-2xl shadow-2xl p-8` modal panel | Oversized, toy look | Radius and shadow from theme tokens (`rounded-md shadow-md` mapped in config) |
| Tailwind: `animate-spin` on an emoji or icon that is not a spinner | Spinning decoration | Only on the spinner element |
| Tailwind: `animate-pulse` on badges, dots and live indicators | Endless motion | Static dot. See part 25 |
| Headless UI `Transition` with enter `duration-300 ease-out scale-95` on every panel | Template motion | `duration-150` opacity only, or no transition |
| Bootstrap: toasts in `.toast-container` top-right with `.bg-success .text-white` | Colored default | Neutral toast, status token for icon or left border only |
| Bootstrap: `data-bs-toggle="tooltip"` on every icon, not initialized | Tooltips silently missing | Initialize once; or remove the attribute |
| Bootstrap: `.spinner-grow` used as a loader | Pulsing dot looks like a notification | `.spinner-border` or a progress bar |
| React: `isLoading && <Spinner/>` without a delay | Spinner flashes on fast networks | Delay 200ms, or use Suspense with a transition that keeps old content |
| React: toast calls inside `useEffect` that fire twice in StrictMode | Duplicate toasts in dev hiding real bugs | Toast from the event handler that caused the result |
| React: `<Modal isOpen={true}>` rendered in list rows (one per row) | 100 dialogs in the DOM | One modal in the parent, record id in state |
| shadcn `AlertDialog` for non-destructive confirms | Wrong primitive | `Dialog` for tasks, `AlertDialog` only for destructive or blocking decisions |
| shadcn/Sonner default `<Toaster richColors closeButton expand />` | Everything on | `<Toaster />` with one position and quiet style |
| Vue: `v-if` on modal with `<Transition name="bounce">` | Bounce motion | Plain fade or none |

## 21.13 Philippines context

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| GCash/Maya payment shown as "Success!" as soon as the user is redirected back | Redirect does not mean paid | Show "Waiting for payment confirmation" until the webhook confirms; poll or refresh status, then "Paid ₱1,250.00 via GCash. Ref 1234 5678 901" |
| Payment pending with a spinner and no reference number | User cannot follow up | Show the reference number and "Keep this number. Payment can take up to 5 minutes to confirm." |
| OTP sent toast with no resend timer | Users tap Send many times | Inline "Code sent to 0917 *** 4567. Resend in 60s." countdown. See part 23 |
| Loading states tuned for fast fiber only | Many users are on prepaid mobile data | Test on throttled 3G; show skeleton or progress for loads over 500ms; allow Retry |
| Offline POS shows a blocking modal | Store cannot sell during outages | Offline banner, queue sales locally, show "3 sales waiting to sync" |
| BIR receipt printed with no feedback on printer error | Cashier does not know it failed | Inline error in the POS: "Printer not responding. Check paper and cable. [Retry print]" |
| Barangay/LGU advisory shown as a pop-up modal on the homepage | Blocks residents looking for services | Banner or a notices list on the homepage with dated items |
| Typhoon/class suspension notice in a small toast | Critical info disappears | Persistent site banner with date, scope (which levels, which barangays) and source |
| Election/precinct lookups with no loading state during peak traffic | Users re-submit and overload | Disable the button, show "Searching…", cache results, rate limit |
| Mixed Tagalog/English in the same toast set ("Na-save na!" beside "Record deleted") | Inconsistent register. See part 09 | One language per UI, or a language switch that covers all messages |

## 21.14 Check
- [ ] Every modal is justified: short focused task or destructive confirm. Everything else is inline, a page or a drawer.
- [ ] No form with more than 3 fields lives in a modal.
- [ ] No modal opens on page load or on exit intent.
- [ ] Max 1 modal open at a time. No modal chains.
- [ ] Modals use `<dialog>` + `showModal()` or a library that traps and returns focus.
- [ ] Modal title names the action and object. No "Are you sure?" title.
- [ ] Buttons are verbs. No Yes/No. Button order is the same in every dialog.
- [ ] Escape, visible Cancel and backdrop click all close the modal, except while dirty or running.
- [ ] Destructive dialogs autofocus Cancel, use the danger token only on the destructive button.
- [ ] Confirms appear only for destructive, costly, sending or irreversible actions.
- [ ] Reversible actions use Undo (8s+, pauses on hover/focus) instead of confirm.
- [ ] Undo really restores data on the server.
- [ ] No `alert()` / `confirm()` in production code.
- [ ] Scrim is a solid overlay token. No `backdrop-filter` on overlays.
- [ ] Modal and toast motion is 150–200ms opacity or none. No bounce, no scale over 0.95–1.
- [ ] Z-index values come from a scale token, not 9999.
- [ ] Drawers update the URL for record views and keep header/footer sticky.
- [ ] Bottom sheets only below 768px.
- [ ] Menus open on click, support arrow keys and Escape, and put destructive items last after a divider.
- [ ] No kebab menu holding the only primary action.
- [ ] Tooltips are short (about 80 characters), show on focus, and never hold essential text or links.
- [ ] Icon-only buttons have a visible label on touch or an `aria-label` plus tooltip on desktop.
- [ ] Toasts appear only for async, off-screen or undoable results.
- [ ] Error toasts persist. Validation errors are inline, not toasts.
- [ ] Max 3 toasts, one position app-wide, 300–400px wide.
- [ ] Toast region has `role="status"`; errors use `role="alert"`.
- [ ] No emoji or colored full-bleed toasts. Library defaults (progress bar, rich colors, bounce) switched off.
- [ ] Only one banner shows at a time; dismissals are remembered; critical banners cannot be dismissed.
- [ ] Status is never color-only.
- [ ] Spinners delay about 200ms; skeletons only for loads over 500ms.
- [ ] Skeletons match the real layout and do not shimmer, or respect reduced motion.
- [ ] One loading indicator per load.
- [ ] Loading buttons keep their label, show a spinner, and block double submit.
- [ ] Long jobs run in the background with real progress ("1,240 of 3,500").
- [ ] Loading states time out with a Retry after about 15s.
- [ ] Optimistic updates roll back on failure and are not used for payments, stock or tallies.
- [ ] GCash/Maya flows show pending until the webhook confirms, with a reference number.
- [ ] Offline states let POS and attendance keep working and show sync counts.
- [ ] Critical public notices (suspensions, advisories) are persistent banners, not toasts or pop-ups.
