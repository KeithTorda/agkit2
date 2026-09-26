---
part: 35
title: Master Checklist and Grep Patterns
covers: pre-ship checklist for all 35 parts, ripgrep patterns for copy, visual, code, SEO, theming and PH-context tells, 30-second review order
---

# 35 — Master Checklist and Grep Patterns

Read when: before marking any task done, before a PR, before a client demo, or when reviewing a generated project you did not write.

Guidance: DESIGN.md and the brief override this part. Run it when the `code-rules` tier or the user asks for a review; it is a checklist, not a gate.

This part adds no rules. Each item names the part that owns the rule as `(NN)`; open that part for the fix. Run the grep patterns in 35.8 first, then the checklist sections the task touched. The 30-second review in 35.9 is the minimum for any change.

## 35.1 How to run this checklist

- Tick only what you checked in the running app or the diff.
- Check at 390px and 1440px wide at least (15). Check light and dark if both exist (34).
- Small change: run 35.9 and the sections that match the files changed. New page or project: run every section.
- Report failures you did not fix in the task report, with the part number (07).

## 35.2 Copy

### Words and phrases (01, 02)
- [ ] No banned adjectives: seamless, powerful, robust, cutting-edge, next-gen, revolutionary, world-class, intuitive, sleek, stunning, comprehensive, innovative, premium (01).
- [ ] No banned verbs: unlock, unleash, empower, elevate, supercharge, streamline, leverage, harness, revolutionize, embark, dive in (01).
- [ ] No LLM-signature words: delve, tapestry, testament, realm, landscape, pivotal, crucial, foster, navigate (figurative), bustling, meticulous, vibrant (01).
- [ ] No filler adverbs: seamlessly, effortlessly, truly, simply, just, really, actually (01).
- [ ] Adjectives kept only where a number or fact backs them (01).
- [ ] No banned phrases: "your journey", "in just a few clicks", "all in one place", "we've got you covered", "take it to the next level", "at your fingertips", "out of the box" (02).
- [ ] No transitions: Moreover, Furthermore, Additionally, In conclusion, It's worth noting, It is important to note (02).
- [ ] No triad slogans ("Fast. Secure. Simple."), no "not just X, but Y", no "whether you're a... or a...", no "designed to / built to" + abstract benefit (02).
- [ ] No colon reveals ("The result?"), no "And the best part?", no em-dash asides in UI copy (02).
- [ ] No rhetorical question headings: "Why choose us?", "Ready to get started?" (02).
- [ ] No "We believe / We're passionate about / We care deeply" statements (02).
- [ ] No anthropomorphised product ("{App} understands your needs") (02).
- [ ] Bold used at most once per paragraph; no emoji in headings; no ALL CAPS feature names; no mystery ellipsis (02).
- [ ] One idea per sentence. Second clause cut where it adds nothing (02).

### Microcopy (03)
- [ ] Buttons and CTAs name the literal action: Save, Post, Sign in, Export, Delete, Create account (03).
- [ ] No "Get Started", "Learn More", "Try it Free", "Explore Features", "See it in action", "Unlock Now" (03, 05).
- [ ] One CTA style across the app; one verb per action (Delete, not Delete/Remove/Trash) (03).
- [ ] Sentence case on buttons, labels, headings and menu items (03).
- [ ] Link text says where it goes; no "Click here", "Read more" alone (03).
- [ ] Every input has a visible label; placeholders are examples, not labels (03, 17).
- [ ] Error messages name what failed and what to do: "Email is required.", "Could not save. Try again." (03).
- [ ] No "Oops", "Whoops", "Uh-oh", "Hmm", "Awesome", "Yay", "Poof" in system text (03).
- [ ] No exclamation marks in system UI text (03).
- [ ] No emoji in labels, toasts, headings or errors (03).
- [ ] Success toasts short: "Saved.", "Thread created.", "Copied." (03).
- [ ] Confirm dialogs name the object and the consequence: "Delete this thread? This is permanent." (03).
- [ ] Destructive buttons say the action ("Delete thread"), not "Yes" / "OK" (03, 18).
- [ ] Loading text is "Loading..." or nothing; no "Hang tight" (03).

### States and formats (04)
- [ ] Empty states: fact plus next action, no cheerleading: "No threads yet." (04).
- [ ] Empty search names the query: "No results for 'xyz'." (04).
- [ ] 404/403/500/503 pages say what happened and the next step; no "lost in space", no hamsters (04).
- [ ] Maintenance message states when service returns (04).
- [ ] Offline, session expired, rate limit and permission states exist and are plain (04).
- [ ] No welcome banner, no "Welcome to {App}!" (04).
- [ ] Notifications name who did what: "John replied to your thread." (04).
- [ ] "Live" only on real push (WebSocket/SSE); polling shows "Updated 2m ago"; cron shows "Synced hourly" (04).
- [ ] Badges (New, Beta, Pro) only where true; no "New" older than a release cycle (04).
- [ ] Pluralisation correct for 0, 1 and many ("1 item", "2 items") (04).
- [ ] Numbers use thousands separators; units have a space and consistent abbreviation (04).
- [ ] Status words consistent across screens (Pending, Paid, Void) (04).
- [ ] Ranks and roles plain: Admin, Mod, Member, Level 12, Staff; no fantasy titles (04).

### Marketing (05)
- [ ] Hero headline says what the product does and for whom (05).
- [ ] No eyebrow pill with "New" or "Introducing" unless there is real news (05, 10).
- [ ] No invented testimonials, names, logos, ratings or user counts (05).
- [ ] No "10x", "99.9%", "Join 10,000+ teams" without a source the client can show (05).
- [ ] No fake urgency or scarcity ("Only 3 left!") (05).
- [ ] Pricing shows real prices and limits; plan names plain (05).
- [ ] About/Team pages use real people and facts, no mission-statement fluff (05).
- [ ] Trust badges only for certifications the client holds (05).

### Docs and code text (06)
- [ ] README: one sentence what and who for, working install/run commands, real limits, boring headings (06).
- [ ] No badge walls, emoji headers, adjective feature lists, or contributing guide/code of conduct on a solo or client repo (06).
- [ ] Commit messages say what changed and why, in the imperative; no emoji (06).
- [ ] Changelog entries list user-visible changes, not "various improvements" (06).
- [ ] Code comments explain why, not what (06, 30).
- [ ] Log and CLI messages plain, no emoji, no "Successfully" on every line (06).

### Agent replies (07)
- [ ] Report starts with the result, not "Great question!" or "Certainly!"; no emoji status lists or "✅ Done!" walls (07).
- [ ] Claims of testing match what was run; untested items listed as untested (07).
- [ ] No recap of every file touched unless asked; key paths and open issues only (07).
- [ ] No "Let me know if you need anything else" closer (07).
- [ ] Plan files contain steps and decisions, no fluff intro (07).

### Email, social, meta (08)
- [ ] Transactional emails: subject names the event ("Your receipt for order 1042"), body states facts and one action (08).
- [ ] Page title names the page and site; meta description names what the page shows, no selling (08).
- [ ] OG title, description and image set per page type (08, 34).
- [ ] Alt text describes the image content or is empty for decoration (08, 26).
- [ ] Facebook posts for LGU/school pages: what, when, where, who; no hype, no hashtag walls (08).
- [ ] Public notices follow notice format: title, date, body, signatory (08, 09).

## 35.3 Visual

### Tropes (10)
- [ ] No glassmorphism unless DESIGN.md asks for it; no neon glow, no gradient text (10).
- [ ] No aurora/mesh gradients, blobs, grain overlays, dot or grid backgrounds (10).
- [ ] No spotlight cursor, border beams, shimmer buttons, 3D tilt cards, orbs, sparkles; no bento grid or marquee logo row unless content needs it (10).
- [ ] No fake browser or macOS window chrome, no fake terminal mockups (10).
- [ ] No emoji used as icons (10, 26).
- [ ] Not the hero + 3 features + CTA template; layout follows the content (10).
- [ ] Auth pages centered, no split-screen illustration (10, 23).
- [ ] No alternating full-bleed colour sections (10).
- [ ] No neumorphism, skeuomorphic textures, parallax, or decorative wave/gradient dividers (10).
- [ ] No unmodified shadcn / Aceternity / MagicUI look; no black "Vercel-style" hero by default (10).

### CSS (11)
- [ ] Shadows subtle or none; no `shadow-2xl` on everything (11).
- [ ] Radius from tokens: small for inputs, medium for cards, pill only for chips and avatars (11).
- [ ] No `backdrop-filter` on nav or cards (11).
- [ ] Hover changes background or opacity, not `scale` or `translateY` on lists and cards (11).
- [ ] No `transition: all`; list the properties (11).
- [ ] No `!important` outside utility overrides the framework needs (11).
- [ ] No `z-index: 9999`; z-index from a small token scale (11).
- [ ] No `100vh` for full-height mobile layouts; use `dvh`/`svh` (11, 15).
- [ ] No fixed heights on text containers; no `overflow: hidden` hiding bugs (11).
- [ ] No arbitrary Tailwind values like `text-[13px]`; no class soup over about 15 classes on one element (11).
- [ ] Bootstrap customised via Sass variables, not override hell (11, 29).
- [ ] Focus style: `:focus-visible` outline from tokens (11, 27).

### Colour (12)
- [ ] Colours from DESIGN.md tokens only; no default indigo/violet `#6366f1`/`#8b5cf6`, no purple-pink gradients (12).
- [ ] One accent per viewport (12).
- [ ] No pure black backgrounds or pure white text on black (12, 34).
- [ ] Status colours used only for status (12).
- [ ] No gradient badges (12).
- [ ] Semantic tokens, not an opacity-based colour system (12).
- [ ] Text contrast at least 4.5:1; large text and UI parts at least 3:1 (12, 27).
- [ ] No text on busy images without a solid backing (12).
- [ ] Meaning not conveyed by colour alone (12, 27).
- [ ] Chart palette distinguishable and themed (12, 20).

### Typography (13)
- [ ] Font chosen from DESIGN.md, not Inter/Poppins/Space Grotesk/Plus Jakarta by reflex (13).
- [ ] No `font-extrabold tracking-tight` hero on utility pages; app page titles modest (13).
- [ ] Max 2 families, 2–3 weights (13, 34).
- [ ] Body 16px preferred, 14px minimum; line-height 1.5–1.6 for body (13).
- [ ] Line length 45–75 characters for reading text (13).
- [ ] No letter-spacing on body; uppercase only on short labels (13).
- [ ] `tabular-nums` on tables, prices and totals (13).
- [ ] Heading levels in order, no skipped levels for styling (13, 28).
- [ ] No justified text; `text-wrap: balance` on headings, `pretty` on paragraphs where supported (13).
- [ ] Links underlined in body text (13).

### Layout and spacing (14)
- [ ] Not everything in a card; content sits on the page surface with dividers (14).
- [ ] No equal 3-column card grid for stats; inline stats, `<dl>` or table (14).
- [ ] Not everything centered; left-aligned reading content (14).
- [ ] Max widths set: about 720px for text, wider for dashboards (14).
- [ ] Spacing from one scale; gaps consistent between siblings (14).
- [ ] No `py-24` on every section; section padding sized to content (14).
- [ ] Density fits the app: dense for data tools, looser for marketing (14).
- [ ] Only the header is sticky (14).
- [ ] One scroll context per view (14).
- [ ] Key content visible without scrolling on utility pages (14).

### Responsive (15)
- [ ] Checked at 390, 768, 1024 and 1440px (15).
- [ ] No horizontal page scroll at 390px (15).
- [ ] Touch targets at least 44x44px (24x24 minimum per WCAG 2.2 AA) (15, 27).
- [ ] No hover-only interactions; everything reachable by tap (15).
- [ ] Inputs at 16px or larger to avoid iOS zoom (15).
- [ ] Tables have a mobile plan: priority columns, stacked rows, or scroll with visible cue (15, 19).
- [ ] Safe-area insets respected for fixed bars (15).
- [ ] Tested on a low-end Android with throttled network (15, 34).

### Motion (25)
- [ ] No entrance animations or scroll reveals on content (25).
- [ ] No hover lift or scale on cards and rows (25).
- [ ] No counters, typing effects, confetti, infinite pulse, marquee (25).
- [ ] No page transitions; UI transitions 150–200ms max (25).
- [ ] `prefers-reduced-motion` respected (25, 27).

### Icons and images (26)
- [ ] One icon set, one style (outline or filled), one stroke width (26).
- [ ] Icons only where they aid scanning; not on every heading or stat card (26).
- [ ] Icon-only buttons have `aria-label` and a tooltip (26, 27).
- [ ] No stock photos of people shaking hands or laptops; real photos or screenshots (26).
- [ ] No AI-generated images, Undraw or isometric illustrations as filler (26).
- [ ] No pravatar/randomuser/picsum/Unsplash placeholders in shipped code (26).
- [ ] No fake logo walls; no generated logos (26).
- [ ] Images use `aspect-ratio`; no gradient overlays on hero images (26).
- [ ] No background video (26, 34).

## 35.4 Components

### Navigation (16)
- [ ] Visible nav on desktop; hamburger only on mobile (16).
- [ ] No mega menu on a small site; simple link list (16).
- [ ] Solid header, no blur, no transparent header over hero images (16).
- [ ] Breadcrumbs only at 3+ levels (16).
- [ ] Mobile tab bar max 4–5 items (16).
- [ ] Active state persistent and different from hover (16).
- [ ] Nav items have text labels (16).
- [ ] Skip link present (16, 27).
- [ ] Sidebar 220–260px, max 2 levels, badges only for real counts (16).
- [ ] Footer short on small sites: "© 2026 {Name}", active social links only, no "Made with ❤️", no tech stack line (16).

### Forms (17)
- [ ] Static labels above inputs; no floating labels (17).
- [ ] Single form under about 10 fields; wizard only for long forms (17).
- [ ] Validate on submit; inline only for availability checks (17).
- [ ] Submit button always enabled; errors shown on click (17).
- [ ] Required legend present when using asterisks (17).
- [ ] Native selects, checkboxes and date inputs unless there is a need (17).
- [ ] Toggles only for settings that apply immediately (17).
- [ ] Correct `type`, `inputmode` and `autocomplete` on every field (17).
- [ ] Phone input accepts `09XX` and `+63` formats and stores E.164 (17, 09).
- [ ] Address fields ordered for PH: region, province, city/municipality, barangay, street (17, 09).
- [ ] Forms over 3 fields on a page, not in a modal (17).
- [ ] Save and Cancel placement consistent across forms (17).

### Buttons (18)
- [ ] One primary button per view (18).
- [ ] No gradient or glowing buttons (18).
- [ ] Loading state keeps width and blocks double submit (18).
- [ ] Destructive buttons styled as destructive and labelled with the action (18).
- [ ] Links navigate, buttons act (18, 28).
- [ ] Bulk actions appear on selection; no FAB on desktop web apps (18).

### Data display (19)
- [ ] Tables for tabular data; not cards (19).
- [ ] Zebra, hover, border and shadow: pick one or two, not all (19).
- [ ] Table sits on the page surface, not in a shadowed card (19).
- [ ] Numbers right-aligned with `tabular-nums` (19).
- [ ] Default sort shown; sortable headers marked (19).
- [ ] No pagination under 50 rows; no "Showing 1–10 of 10" (19).
- [ ] Row actions in a menu or on selection, not 4 icons per row (19).
- [ ] Status as text (with colour as support), not icon-only (19).
- [ ] Empty table: "No records." plus an action link (19).
- [ ] Truncated text has a full-value tooltip or detail view (19).

### Charts (20)
- [ ] No pie or donut for 2 categories or more than 5 (20).
- [ ] No line chart for 3 points; use text or a table (20).
- [ ] No gradient area fills or glow lines (20).
- [ ] No dual axes (20).
- [ ] Axes labelled with units; peso values formatted (20, 09).
- [ ] No fake or random data in shipped charts (20).
- [ ] Library defaults changed (Chart.js/Recharts colours, legends, animation) (20).

### Overlays and feedback (21)
- [ ] Modals only for confirmations and short focused tasks (21).
- [ ] No modal chains; max 1 modal open (21).
- [ ] Modals close by Cancel, Esc and backdrop (except critical) (21).
- [ ] Focus moves into the modal and returns on close (21, 27).
- [ ] Error toasts persist until dismissed; max 3 toasts; one position (21).
- [ ] Undo toasts stay at least 8 seconds (21).
- [ ] No success toast for expected, visible results (21).
- [ ] Spinners only after about 200ms; skeletons only for loads over 500ms (21, 34).
- [ ] Confirm only destructive actions (21).

## 35.5 Pages

### Dashboards and admin (22)
- [ ] No greeting ("Good morning, Keith! 👋") (22).
- [ ] 1–2 prominent numbers; the rest compact (22).
- [ ] Stat tiles neutral; colour only for status (22).
- [ ] No "Quick Actions" card; actions in nav or context (22).
- [ ] Recent activity grouped by day, entries specific (22).
- [ ] No auto-refresh under 60s; "Updated X ago" shown (22).
- [ ] No onboarding tour overlay (22).
- [ ] CRUD: list, detail and edit pages follow one pattern (22).
- [ ] Filters bar shows active filters and a clear-all (22).
- [ ] Roles and permissions UI shows what each role can do (22).
- [ ] Audit log records who, what, when (22).
- [ ] Reports export to CSV/XLSX/PDF with real column names (22).
- [ ] POS screen: large touch targets, keyboard/scanner friendly, totals always visible (22).
- [ ] Inventory: stock levels as numbers with units; low-stock threshold stated (22).

### Auth and account (23)
- [ ] Heading "Sign in", not "Welcome back!" (23).
- [ ] Only implemented social logins shown; no "Or continue with" for one method (23).
- [ ] "Show password" labelled (23).
- [ ] Forgot password link visible, normal size (23).
- [ ] No CAPTCHA without a spam problem (23).
- [ ] OTP input accepts paste and autofill (`autocomplete="one-time-code"`) (23, 17).
- [ ] Settings on one page with headings when there are few sections; invite and billing pages state amounts and dates plainly (23).
- [ ] "Delete account" at the bottom with a confirmation, no red "Danger Zone" banner (23).
- [ ] No profile completion bar, cover photo or activity heatmap unless core (23).

### Page types (24)
- [ ] Each page type checked against its row in part 24: landing, pricing, about, contact, blog, article, docs, changelog, careers, portfolio, product, cart/checkout, search, legal, coming soon, link-in-bio, event (24).
- [ ] Government/barangay homepage: services, office hours, contact numbers, announcements first (24).
- [ ] School homepage: enrollment, calendar, contact first (24).
- [ ] Election/precinct finder: one search field, clear result, source and date of data shown (24).
- [ ] Contact page has real address, phone and hours; legal pages name the actual company and the Data Privacy Act where it applies (24).

## 35.6 Code

### Accessibility (27)
- [ ] No `div`/`span` with click handlers; real `<button>` and `<a href>` (27, 28).
- [ ] ARIA only where native HTML cannot express it (27).
- [ ] Every input labelled; errors linked with `aria-describedby` and announced (27).
- [ ] Focus outline never removed without a replacement (27).
- [ ] Focus trap in modals; no traps elsewhere (27).
- [ ] Landmarks present: `header`, `nav`, `main`, `footer` (27).
- [ ] `lang` set correctly (`en`, `fil`, `en-PH`); inline language changes marked (27).
- [ ] No `user-scalable=no` or `maximum-scale=1` (27).
- [ ] Full keyboard pass: Tab through every control, Enter/Space work, Esc closes (27).

### HTML (28)
- [ ] Semantic elements; nesting depth 4 or less for most components (28).
- [ ] No `container > wrapper > inner` triples (28).
- [ ] Tables for data (28).
- [ ] No `<!-- Hero Section -->` comment on every block (28).
- [ ] Head has only needed tags; no boilerplate meta junk (28, 34).
- [ ] No inline styles or large inline scripts (28).

### CSS architecture (29)
- [ ] One naming convention (BEM or prefix); no generic `.container .card .title` collisions (29).
- [ ] Selectors flat; no deep nesting (29).
- [ ] Tokens for repeated values only (29).
- [ ] No global overrides file fighting the framework (29).
- [ ] No dead CSS; no copy-pasted reset on top of the framework's reset (29).
- [ ] No `@apply` rebuilding a component library in CSS (29).

### JS/TS (30)
- [ ] No `console.log`, `debugger` or commented-out code (30).
- [ ] No silent `catch {}`; errors logged or rethrown (30).
- [ ] No `any` without a comment explaining why (30).
- [ ] No single-use helpers or abstractions; extract at 3 uses (30).
- [ ] No mock data or fake implementations left in production paths (30).
- [ ] No placeholder TODOs for required behavior (30).
- [ ] Timers, intervals and listeners cleaned up (30).
- [ ] No emoji in code, logs or identifiers (30).

### React/Vue (31)
- [ ] No `useEffect` for derived state; derive during render (31).
- [ ] No fetch in `useEffect` without cache, cancellation and error state (31).
- [ ] Loading, error and empty states exist for each async view (31).
- [ ] No `key={index}` on reorderable lists (31).
- [ ] No `React.memo`/`useMemo` everywhere without a measured need (31).
- [ ] No `"use client"` on every file (31).
- [ ] shadcn components restyled to DESIGN.md tokens (31).
- [ ] Components under about 200 lines; split by responsibility (31).

### Backend, API, DB (32)
- [ ] No `{ success: true, message: "Operation successful" }` envelope; correct status codes (32).
- [ ] Validation real (schema), not `if (!body) return 400` only (32).
- [ ] No catch-all 500 for user errors (32).
- [ ] Parameterised SQL; no string-built queries (32).
- [ ] No N+1 queries on list endpoints; indexes on filtered columns (32).
- [ ] No secrets in logs or in the repo; env handling documented (32).
- [ ] No mock auth, default passwords, or disabled auth checks left in (32).
- [ ] Rate limiting on login, OTP and public search endpoints (32).
- [ ] REST names plural nouns; consistent casing in JSON (32).

### Naming and structure (33)
- [ ] No `utils`, `helpers`, `common`, `misc`, `new`, `final`, `v2`, `copy` files (33).
- [ ] No `data`, `data2`, `temp`, `item`, `handleClick2` names (33).
- [ ] No `Manager`/`Handler`/`Helper` classes without a specific job (33).
- [ ] One term per domain concept (33).
- [ ] No barrel files re-exporting whole folders (33).
- [ ] One lockfile, one lint config, one formatter config (33).
- [ ] create-* leftovers removed: `vite.svg`, `react.svg`, `App.css` logo spin, `next.svg`, `logo192.png`, template README and title (33).

### Performance, SEO, theming (34)
- [ ] LCP image optimised, sized, not lazy-loaded (34).
- [ ] Fonts `woff2`; no icon font for a handful of icons (34).
- [ ] No animation library for one effect; no `@latest` CDN URLs (34).
- [ ] No render-blocking scripts; one analytics tool max (34).
- [ ] No layout shift from images, banners or fonts (34).
- [ ] No preloader or splash screen (34).
- [ ] Unique title and description per page; no `keywords` meta (34).
- [ ] `robots.txt` and sitemap correct for production; staging not indexed (34).
- [ ] Theme follows system; System/Light/Dark only; no theme flash; no `filter: invert()` (34).

## 35.7 Philippine context

- [ ] Peso amounts use the one format set in part 09, with the `₱` sign; no `$`, and no mix of `PHP 1250`, `P1250` and `₱1,250.00` on one site (09).
- [ ] Money stored as integer centavos; formatted with `Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' })` (09, 33).
- [ ] Phone numbers shown in one format (`0917 123 4567` or `+63 917 123 4567`), stored as E.164 (09, 17).
- [ ] No `09XX-XXX-XXXX` or `+63 9XX` placeholders left in shipped pages (09).
- [ ] Dates unambiguous: month written as a word ("23 Sep 2026" or "September 23, 2026"), not `09/10/2026` (09, 04).
- [ ] Times in 12-hour format with AM/PM for public pages unless the client uses 24-hour; timezone Asia/Manila (09).
- [ ] Addresses: Purok/Sitio, Barangay, City/Municipality, Province; ZIP where used (09).
- [ ] No forced "Mabuhay!", "Tara na!", "Sulit!", "Kabayan" in UI copy (09).
- [ ] Tagalog/Filipino copy written or checked by a speaker; no machine-translated deep Tagalog (09).
- [ ] One language per UI element; bilingual pages keep register consistent (09).
- [ ] No fake seals, invented officials or "Hon. Juan Dela Cruz" placeholders on LGU/school sites (09).
- [ ] No "Official Website of" hype; name the office plainly (09).
- [ ] Official names spelled exactly (barangay, municipality, school, DepEd school ID) (09).
- [ ] GCash/Maya/bank transfer instructions state account name, number, amount and reference steps (09).
- [ ] BIR receipt wording and fields match the client's registration (OR vs sales invoice, TIN, VAT/non-VAT) (09).
- [ ] Local photos of the real place and people, not foreign stock (09, 26).
- [ ] `lang="fil"` on Filipino pages (09, 27).
- [ ] Data Privacy Act notice on forms that collect personal data (08, 24).

## 35.8 Grep patterns

Run from the project root. `rg` skips files listed in `.gitignore` (`node_modules`, `dist`, `.env`).

- Always pass a path (`.` or `src`). In agent shells stdin is often a pipe, and `rg` without a path reads stdin and waits forever.
- Exclude the rulebook itself, or every banned word will match: add `-g '!<kit folder>/**'` (for example `-g '!.agent/**'`).
- A match is a lead, not a verdict. Check the line against the owning part.
- Patterns use `\x27` for a single quote and `\x60` for a backtick so they fit inside single-quoted shell strings.
- Patterns marked `-P` use lookahead and need ripgrep built with PCRE2 (`rg --pcre2-version` to check).

### Copy: words and phrases (01, 02)

```bash
# Banned adjectives (01)
rg -n -i '\b(seamless(ly)?|robust|cutting-edge|next-gen|state-of-the-art|revolutionary|game-changing|transformative|world-class|best-in-class|blazing|lightning-fast|hassle-free|all-in-one|intuitive|sleek|stunning|gorgeous|unparalleled|unmatched|bespoke|top-notch|enterprise-grade|innovative|effortless(ly)?)\b' .

# LLM-signature words and banned verbs (01)
rg -n -i '\b(delve[sd]?|delving|tapestry|testament|realm|landscape|pivotal|crucial|foster(s|ing)?|underscores?|bustling|meticulous(ly)?|vibrant|unlock|unleash|empower(s|ing)?|elevate|supercharge|streamline|leverage|harness|embark|journey)\b' .

# Transitions and filler openers (02)
rg -n -i '\b(moreover|furthermore|additionally|in conclusion|it.s worth noting|it is important to note|in today.s (fast-paced|digital))\b' .

# "not just X but Y" and "whether you're" (02)
rg -n -i '\bnot just\b[^.\n]{1,60}\bbut\b|\bwhether you(.re| are)\b' .

# Triad slogans: "Fast. Secure. Simple." (02)
rg -n '[A-Z][a-z]+\. [A-Z][a-z]+\. [A-Z][a-z]+\.' .

# Rhetorical question headings (02, 05)
rg -n -i '(why choose us|ready to get started|what makes us different|what sets us apart)\??' .

```

### Copy: microcopy and states (03, 04)

```bash
# Banned CTA labels inside tags or strings (03, 05)
rg -n -i '["\x27\x60>]\s*(get started( today)?|learn more|start (your )?free trial|try (it|demo) free|explore features|unlock now|dive in|see it in action|book a demo|see how it works)\s*[<"\x27\x60]' .

# Cheerleading and apology words (03, 04)
rg -n -i '\b(oops|whoops|uh-oh|yay|woohoo|hooray|awesome|hang tight|you.re all set|poof|welcome (back|aboard|to))\b' src

# Exclamation marks inside UI strings (03)
rg -n '["\x27\x60>][A-Z][^"\x27\x60<>\n]{1,80}![\s"\x27\x60<]' src

# Live / real-time labels: check each is real push (04)
rg -n '\b(Live|LIVE|Real-?[Tt]ime)\b' src

# Dashboard greetings (22)
rg -n -i 'good (morning|afternoon|evening)' src
```

### Copy: marketing and fake content (05, 26, 30)

```bash
# Unsourced stats: "10x faster", "10,000+ teams", "99.9%" (05)
rg -n -i '\b\d+(\.\d+)?x\s+(faster|more|better|cheaper)\b|\b\d{1,3}(,\d{3})*\+\s+(users|teams|customers|companies|businesses|clients)\b|\b99\.9+%' .

# Lorem ipsum and placeholder people/emails (05, 30)
rg -n -i '\blorem\b|\bipsum\b|dolor sit amet|\b(john|jane) (doe|smith)\b|\bfoo@|test@test|@example\.com\b' src

# Stock AI testimonial names (05)
rg -n '\b(Sarah (Johnson|Chen|Mitchell)|Michael (Chen|Brown|Rodriguez)|Emily (Davis|Rodriguez|Chen)|Alex (Rivera|Morgan|Chen)|David (Kim|Park)|Jessica (Lee|Wong))\b' .

# Placeholder image services (26)
rg -n 'i\.pravatar\.cc|randomuser\.me|picsum\.photos|placehold\.co|via\.placeholder\.com|placekitten|source\.unsplash\.com|images\.unsplash\.com' .

# "Made with love" footers (16)
rg -n -i 'made with (❤|♥|love)' .
```

### Emoji (02, 03, 06, 30)

```bash
# Emoji anywhere in source (UI strings, logs, comments)
rg -n '[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}\x{2B50}\x{2B55}]' src

# Emoji in Markdown headings (06)
rg -n '^#{1,6}\s*[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]' -g '*.md' .

# Vague or emoji commit subjects (06)
git log --format=%s -n 200 | rg -i '^(update|updates|fix|fixes|changes|wip|misc|stuff|final|test)\.?$|[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]'
```

The emoji range also matches glyphs like `✓` and `✕`. Replace those with icons from the project's set (26).

### Visual CSS (10, 11, 12)

```bash
# Glow shadows, CSS (10, 11)
rg -n -i '(box|text)-shadow:\s*(inset\s+)?0(px)?\s+0(px)?\s+\d+px' .

# Glow shadows and coloured shadows, Tailwind (10, 11)
rg -n '\b(shadow|drop-shadow)-\[0_0_|\bshadow-(indigo|violet|purple|fuchsia|pink|cyan|blue|emerald)-\d{3}' .

# Gradient text (10)
rg -n 'background-clip:\s*text|text-fill-color:\s*transparent|\bbg-clip-text\b' .

# Tailwind gradients and purple-pink stops (10, 12)
rg -n '\bbg-(gradient|linear)-to-(r|l|t|b|tr|tl|br|bl)\b|\b(from|via|to)-(purple|violet|indigo|fuchsia|pink)-\d{3}\b' .

# CSS gradients and animated gradient backgrounds (10, 11)
rg -n 'linear-gradient\(|radial-gradient\(|conic-gradient\(|background-size:\s*[2-9]00%' .

# Glassmorphism (10, 11)
rg -n 'backdrop-filter:\s*blur|\bbackdrop-blur(-[a-z0-9]+)?\b' .

# !important (11)
rg -n '!important' -g '!*.min.css' .

# transition: all (11)
rg -n 'transition:\s*all\b|\btransition-all\b' .

# Hover lift and scale (11, 25)
rg -n 'transform:\s*(scale\(1\.\d+|translateY\(-\d)|\bhover:(scale-\d+|-translate-y-\d+)\b' .

# Huge z-index (11)
rg -n 'z-index:\s*\d{4,}|\bz-\[\d{4,}\]' .

# Large radii and heavy shadows (11)
rg -n '\brounded-(2xl|3xl)\b|border-radius:\s*(1[6-9]|[2-9]\d)px|\bshadow-(xl|2xl)\b' .

# Infinite and attention animations (11, 25)
rg -n '\banimate-(pulse|bounce|ping)\b|animation:[^;]*\binfinite\b' .

# Slow transitions over 500ms (25)
rg -n '(transition|animation)(-duration)?:[^;]*\b([5-9]\d\d|\d{4,})ms\b|\bduration-(500|700|1000)\b' .

# Default AI colours: indigo, violet, purple, fuchsia (12)
rg -n -i '#(6366f1|8b5cf6|a855f7|7c3aed|4f46e5|667eea|764ba2|ec4899|d946ef)\b|\b(bg|text|border|ring|from|via|to)-(indigo|violet|purple|fuchsia)-\d{2,3}\b' .

# Pure black backgrounds (12, 34)
rg -n -i 'background(-color)?:\s*(#000(000)?\b|black\b|rgb\(0,\s*0,\s*0\))|\bbg-black\b' .

# Hard-coded hex colours outside tokens.css (12, 29)
rg -n -i '#[0-9a-f]{3,8}\b' -g '*.css' -g '*.scss' -g '*.tsx' -g '*.vue' -g '!tokens.css' src

# Arbitrary Tailwind pixel values (11)
rg -n '\b[a-z]+(-[a-z]+)*-\[\d+(\.\d+)?(px|rem)\]' .

# Section padding bloat: count per file (14)
rg -c '\bpy-(20|24|28|32|40)\b' src

# 100vh and h-screen (11, 15)
rg -n '\b100vh\b|\bh-screen\b' .

# Vendor-prefix junk (11); -e is needed because the pattern starts with a hyphen
rg -n -e '-(moz|ms|o)-(border-radius|box-shadow|transition|transform|user-select)|-webkit-(border-radius|box-shadow)\b' .
```

### Typography and fonts (13, 34)

```bash
# Reflex font choices (13)
rg -n 'font-family:[^;]*\b(Inter|Poppins|Space Grotesk|Plus Jakarta Sans|Outfit|Manrope|DM Sans|Sora|Montserrat)\b|family=(Inter|Poppins|Space\+Grotesk|Plus\+Jakarta\+Sans|Outfit|Manrope|DM\+Sans|Sora|Montserrat)' .

# Four or more font weights in one Google Fonts URL (34)
rg -n 'wght@(\d{3};){3,}\d{3}' .

# Google Fonts @import inside CSS, render-blocking (34)
rg -n '@import\s+url\(["\x27]?https://fonts\.googleapis' .

# Extrabold tight hero and oversized text (13)
rg -n '\bfont-(extrabold|black)\b[^"\x27\x60]*\btracking-tight(er)?\b|\btracking-tight(er)?\b[^"\x27\x60]*\bfont-(extrabold|black)\b|\btext-[6-9]xl\b' .
```

### Accessibility and HTML (27, 28)

```bash
# Click handlers or role="button" on non-interactive elements (27, 28)
rg -n '<(div|span|li|td)\b[^>]*\b((onClick|@click|v-on:click|onclick)=|role=["\x27]button)' .

# Focus outline removed (27)
rg -n 'outline:\s*(none|0)\b|\b(focus:)?outline-none\b' .

# Zoom disabled (27)
rg -n 'user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0)?\b' .

# <img> without alt (27), needs PCRE2
rg -n -P '<img\b(?![^>]*\balt=)[^>]*>' .

# Useless alt text (26, 27)
rg -n -i 'alt=["\x27](image|img|photo|picture|logo|icon|banner|untitled|placeholder)["\x27]|alt=["\x27][^"\x27]*\.(png|jpe?g|webp|svg)["\x27]' .

# Section-label comments on every block (28)
rg -n -i '<!--\s*(hero|features?|footer|header|navbar|cta|testimonials?|pricing|about|contact)(\s+section)?\s*-->|\{/\*\s*(hero|features?|footer|header|navbar|cta|testimonials?|pricing)(\s+section)?\s*\*/\}' .
```

### JS, TS and React (30, 31)

```bash
# console.log and debugger (30)
rg -n '\bconsole\.(log|debug|info|table)\(|^\s*debugger\b' src

# Silent catch blocks, multiline (30)
rg -n -U 'catch\s*(\(\s*\w*\s*\))?\s*\{\s*(//[^\n]*\s*)?\}' src

# any (30)
rg -n ':\s*any\b|\bas any\b|<any>' src

# TODO and placeholder implementations (30)
rg -n '\b(TODO|FIXME|HACK)\b|implement (this|me|later)|not implemented' src

# Index keys (31)
rg -n 'key=\{(i|idx|index)\}' src

# Files marked "use client": compare the count with what needs interactivity (31)
rg -l '^["\x27]use client["\x27]' src

# Fetch inside useEffect, multiline (31)
rg -n -U 'useEffect\(\s*(async\s*)?\(\)\s*=>\s*\{[^}]*\bfetch\(' src
```

### Naming and structure (33)

```bash
# Vague variable names (33)
rg -n '\b(const|let|var)\s+(data\d*|newData|finalData|info|item|temp|tmp|obj|arr|stuff|thing|foo|bar|result\d+)\s*[:=]' src

# Numbered and generic handler/function names (33)
rg -n '\b(handle\w*\d|doStuff|processData|handleData|performAction|executeOperation)\b' src

# Manager/Handler/Helper classes and I-prefixed interfaces (33)
rg -n '\b(class|interface)\s+(\w+(Manager|Handler|Helper|Util|Processor|Wrapper)|I[A-Z]\w+)\b' src

# Generic, versioned and duplicate file names (33)
rg --files . | rg -i '(^|/)(utils?|helpers?|common|misc|shared|stuff|temp|tmp|scratch)\.[a-z]+$|[-_. ](new|old|final|copy|backup|bak|v\d+)\.[a-z]+$|[a-z](\d|New|Old|Final|Copy|V\d+)\.(tsx?|jsx?|vue|css|html|php)$| copy\.| \(\d\)\.|\.(bak|orig|old|swp)$'

# create-* template leftover files (33)
rg --files . | rg -i '(^|/)(vite|react|vue|svelte|next|vercel|globe|window|file|astro)\.svg$|logo(192|512)\.png$|reportWebVitals|setupTests|App\.test\.|HelloWorld\.vue|TheWelcome\.vue|WelcomeItem\.vue|(^|/)App\.css$'

# create-* template leftover text (33)
rg -n -i 'count is \{?count|edit <code>src/|get started by editing|click on the vite and|learn react|welcome to laravel|hello, world!|the install worked successfully' .

# Camera, screenshot and AI-generator asset names (26, 33)
rg --files . | rg -i '(^|/)(IMG_\d+|DSC_?\d+|Screenshot[ _-]|unnamed|download|images?\d*|image\d+|pic\d*)\.[a-z]+$|ChatGPT Image|Gemini_Generated_Image|DALL.E|midjourney'

# Several lockfiles (33)
rg --files . | rg '(^|/)(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|bun\.lockb?)$'
```

### Backend and security (32)

```bash
# Hard-coded secrets and default passwords (32)
rg -n -i '(password|passwd|secret|api_?key|token)\s*[:=]\s*["\x27][^"\x27]{4,}["\x27]|\b(admin123|password123|changeme|secret123|qwerty)\b' .

# Boilerplate success envelopes (32)
rg -n -i 'success:\s*true|operation successful|data fetched successfully' src

# String-built SQL (32)
rg -n -i '["\x27\x60]\s*(select|insert|update|delete)\b[^"\x27\x60]*["\x27\x60]?\s*\+\s*\w|\b(select|insert|update|delete)\b[^\x60\n]*\$\{' src

# Secrets under client-exposed env prefixes (32, 33)
rg -n '\b(VITE|NEXT_PUBLIC|REACT_APP)_\w*(SECRET|PASSWORD|PRIVATE|SERVICE_ROLE)\w*' .
```

### Performance, SEO, theming (34)

```bash
# Animation and decoration libraries (25, 34)
rg -n 'from ["\x27](framer-motion|motion/react|gsap|aos|animejs|animate\.css|lottie-react|react-type-animation|typewriter-effect|canvas-confetti|react-confetti|tsparticles)["\x27]|/(aos|animate\.css|gsap)[@/]' .

# Heavy utility libraries (34)
rg -n 'from ["\x27](moment|lodash|jquery)["\x27]|require\(["\x27](moment|lodash|jquery)["\x27]\)' .

# Icon fonts (34)
rg -n -i 'font-?awesome|material-icons|Material\+(Icons|Symbols)|bootstrap-icons(\.min)?\.css' .

# @latest CDN, Tailwind Play CDN, polyfill.io (34)
rg -n '@latest\b|cdn\.tailwindcss\.com|polyfill\.io' .

# Render-blocking external scripts, needs PCRE2 (34)
rg -n -P '<script\b(?![^>]*\b(defer|async|type=["\x27]module["\x27])\b)[^>]*\bsrc=' -g '*.html' -g '*.php' -g '*.astro' .

# Lazy-loaded hero or logo (34)
rg -n -i 'loading=["\x27]lazy["\x27][^>]*(hero|logo)|(hero|logo)[^>]*loading=["\x27]lazy' .

# Boilerplate meta tags (34)
rg -n -i '<meta\s+name=["\x27](keywords|revisit-after|rating|distribution|generator)["\x27]' .

# Template page titles (33, 34)
rg -n '<title>\s*(React App|Vite \+ \w+( \+ TS)?|Create Next App|Home|Document|Untitled)\s*</title>|title:\s*["\x27]Create Next App' .

# noindex and Disallow: / left in (34)
rg -n -i 'noindex|^Disallow:\s*/\s*$' .

# Dev or preview hosts in sitemap and robots (34)
rg -n 'localhost|127\.0\.0\.1|\.vercel\.app|\.netlify\.app' -g '*.xml' -g 'robots.txt' .

# Invert-filter dark mode (34)
rg -n 'filter:\s*invert\(' .

# System theme support present? No output means it is missing (34)
rg -l 'prefers-color-scheme|color-scheme' .
```

### Philippine context (09)

```bash
# Placeholder mobile numbers (09)
rg -n '\b09[Xx]{2}\b|\+63\s?9[Xx]{2}|\b09(12345678|171234567|991234567|123456789)\d?\b' .

# Mixed peso formats and dollar signs; also matches $1 in regex replacements, check each (09)
rg -n '\bPHP\s?\d|\bP\s?\d{1,3}(,\d{3})+\b|\$\s?\d' src

# Locale-less date and number formatting, and float money (04, 09)
rg -n 'toLocale(Date|Time)?String\(\s*\)|Intl\.(NumberFormat|DateTimeFormat)\(\s*\)|toFixed\(2\)' src

# Ambiguous numeric dates in UI text (04, 09)
rg -n '>[^<]*\b\d{1,2}/\d{1,2}/\d{2,4}\b[^<]*<' src

# Forced Filipino slogans (09)
rg -n -i '\b(mabuhay|tara na|sulit|kabayan|lodi|petmalu)\b' src

# Placeholder officials (09)
rg -n -i 'Hon\.\s+(Juan|John|Name|First|\[|\{)|\bJuan (dela|de la) Cruz\b' .
```

## 35.9 30-second review

Run in this order. Stop and fix at the first failure, then continue.

1. Grep: banned adjectives, LLM words, emoji, `console.log`, `Lorem`, `09XX` (35.8). Zero hits in UI strings.
2. Open the page at 390px. No horizontal scroll. Nothing overlaps. Tap targets fit a thumb (15).
3. Read the H1, the primary button and one empty or error state aloud. Each says a literal fact or action (03, 04).
4. Scan for the look: glow, gradient text, glass, blobs, purple-pink, `shadow-2xl`, `rounded-3xl` (10, 11, 12).
5. Count primary buttons and accent colours in the viewport. One of each (12, 18).
6. Hover a card and a row. Background change only, no lift or scale (11, 25).
7. Tab through the page. Focus is visible on every control; Esc closes overlays (27).
8. Reload with Slow 4G throttling. Content shows without a preloader; no layout jump (34).
9. Toggle the OS to dark (if dark mode exists). Every surface follows; no flash (34).
10. Check PH details on the page: peso format, phone format, date format, place names (09).
11. Check the tab title and the diff for leftovers: template title, `vite.svg`, mock data, TODO (33, 34).
12. Write the report: what changed, what was checked, what was not (07).

## 35.10 Check

- [ ] 35.8 grep patterns run, kit folder excluded.
- [ ] Every hit in UI strings fixed or justified in the report.
- [ ] Copy (35.2) passed for every screen touched; Visual (35.3) at 390px and 1440px.
- [ ] Components (35.4) and Pages (35.5) passed for every type touched.
- [ ] Code section (35.6) passed for every file type in the diff.
- [ ] PH context (35.7) passed where the project serves PH users.
- [ ] Unfixed items reported with their part number.
- [ ] 30-second review (35.9) done on the final build, not only in dev.
- [ ] Keyboard, slow-network, and light/dark passes done.
- [ ] No template leftovers, mock data, placeholder names or phones, or Lorem text.
