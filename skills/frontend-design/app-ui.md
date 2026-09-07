# App UI (frontend-design §4.4, §5.E, §7)

Read when: building or fixing an app page: dashboard, settings, form, table, any non-marketing screen. Core SKILL.md first (§0.F screen read, §1.A app-page dials, §4.0 judgment, §4.7 copy, §4.8 app-UI tells all apply here).

## 4.4 States and forms
- Full cycle, designed in the screen read (SKILL.md §0.F): loading = skeletons matching the final layout, not spinners; empty = composed, says how to populate, first run shows the one action that creates the first item; error = inline for forms, toast only for transient, `aria-live`, always a way forward (retry, edit, link out); long content = design for the 200-char title and 500-row list, truncate or paginate deliberately; `:active` = `scale-[0.98]` or `-translate-y-px`.
- `focus-visible` ring on every interactive element, never `outline: none` without a replacement; state never by colour alone (add an icon, label, or weight).
- Buttons: AA text on their own background (4.5:1; 3:1 at 18px+); scrim or stroke under ghost buttons over photos; primary CTA label one line at desktop (1024px+), three words max; one label per intent per page ("Get in touch" and "Let's talk" are one intent: pick one for nav, hero, footer).
- Forms: label above input (never placeholder-as-label), helper text in markup, error text below, `gap-2` blocks; inputs, placeholders, labels, rings, errors pass AA on the section background, in every shipped color scheme; validate against a schema, not `window.alert()`.

## 5.E Feedback on action (interaction, not decoration)
The motion that matters most is the half-second after a click.
- Every mutation shows pending **on the control that triggered it** (disabled + "Saving..."), not a page-wide spinner; success shows inline or by navigating, a toast only when the user has already left the context.
- Errors appear next to their cause and read per SKILL.md §4.7.
- Optimistic UI only for reversible, high-frequency actions (like, toggle, reorder), with a visible revert on failure; never for payments, deletes, or anything with a receipt.
- Hover changes one property (colour or elevation) over `DESIGN.md` `motion.duration.fast`; state transitions use `motion.duration.base`. Under 100 ms feels instant; over 300 ms needs a pending state.

## 7. App-page and component work
Page-level app UI (settings, onboarding, dashboards, forms, tables): app-page dials (SKILL.md §1.A), `DESIGN.md` component tokens, a design system when the brief names one (design-systems.md §2.A). Dense tables: TanStack Table or AG Grid; editors: Monaco / CodeMirror; multi-step forms: form-library patterns. SKILL.md §0.F, §4.0, §4.7 and design-systems.md §4.9 apply everywhere; marketing rules (hero, eyebrows, logo walls: marketing-layout.md) do not.

Hierarchy on an app page (marketing counterpart: marketing-layout.md §4.5):
- **One primary action per view**, in one fixed place (top-right of the page header, or bottom-right of a form); never the same action twice, never two filled buttons in one region.
- **Page header** = title, one line of context, actions. Greetings and stat rows are not headers.
- **Forms** in groups of ≤ 5 fields under a group heading; single column below `lg`; the field the user fills first is first; helper text only where a field is genuinely ambiguous.
- **Tables**: numeric columns right-aligned, text left; the column the user scans first is first; row height from the density dial, not padding guesses; a row's primary action visible without hover on touch.
- **Lead with what the user checks first** (SKILL.md §0.F item 4): a dashboard opens on the one number or list that answers "is anything wrong", not a row of tiles. The grayscale-and-squint test (SKILL.md §4.0) applies here as on a landing page.
