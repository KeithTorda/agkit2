---
name: copy
version: 3.0.0
priority: P0
trigger: always
description: Complete anti-AI rulebook. Copy, voice, UI, CSS, layout, components, forms, nav, dashboards, modals, tables, auth, code structure. Zero template UI. Zero hype.
---

# Anti-AI Design & Copy Rulebook

Apply to ALL output: UI, CSS, HTML, templates, microcopy, landing pages, buttons, empty states, errors, docs, README, meta tags, commits, and plan text.

---

# PART 1 — COPY & VOICE

## 1.1 Banned Adjectives
```
seamless, powerful, robust, enterprise-grade, cutting-edge,
next-gen, state-of-the-art, revolutionary, game-changing,
transformative, delightful, world-class, best-in-class,
blazing, lightning-fast, ultra-fast, ultra, vibrant, dynamic,
immersive, premium, exclusive, VIP, pro-level, hassle-free,
all-in-one, intuitive, sleek, stunning, gorgeous, beautiful,
elegant, sophisticated, modern, futuristic, innovative,
comprehensive, extensive, unparalleled, unmatched, curated,
handcrafted, hand-picked, bespoke, tailor-made, top-notch,
first-class, exceptional, remarkable, extraordinary, incredible
```

| AI word | Use instead |
|---|---|
| seamless, hassle-free | works with, compatible |
| powerful, robust | solid, reliable |
| enterprise-grade | for teams of 50+ |
| cutting-edge, next-gen | current, rebuilt, v2 |
| premium, exclusive | paid, members-only |
| blazing, lightning-fast | under 200ms, instant |
| vibrant, dynamic, immersive | active, full-screen |
| revolutionary, game-changing | new, changed, rewritten |
| delightful, gorgeous | simple, clear, *(delete)* |
| world-class, best-in-class | *(delete entirely)* |
| intuitive | *(delete — if it needs the word, it isn't)* |
| comprehensive | covers X, Y, Z *(list what it covers)* |
| curated, handcrafted | picked, chosen, built |
| innovative, futuristic | *(delete or say what's new)* |

## 1.2 Banned Verbs
```
unlock, unleash, empower, elevate, supercharge, streamline,
accelerate, revolutionize, dive in, dive into, embark,
journey, forge, harness, leverage, curate, craft (as UI verb),
reimagine, transform, discover, explore (as CTA), onboard,
spearhead, pioneer, champion, orchestrate, catalyze, amplify,
optimize (unless actual perf work), synergize, disrupt
```
Use the literal action: `Save`, `Post`, `Sign in`, `Filter`, `Export`, `Delete`, `Create`, `Run`, `View`, `Copy`, `Send`, `Download`, `Upload`.

## 1.3 Banned Phrases
```
your journey, in just a few clicks, Welcome to {Product}!,
Be the first to, We're excited to announce, Thrilled to,
Simple. Powerful. Beautiful., The all-in-one platform for X,
Build X the modern way, X reimagined, Ship faster with,
Join 10,000+ teams already, Everything you need nothing you don't,
takes the hassle out of, empowers you to, seamlessly integrates with,
Why choose us?, Not just X but Y, designed to / built to / made to,
whether you're a beginner or expert, all in one place,
The future of X is here, Let's get you started,
We've got you covered, You're in good hands, Say goodbye to,
Say hello to, It's that simple, and much more, and beyond,
What sets us apart, Here's what you'll get, Imagine a world where,
Without breaking a sweat, At your fingertips, Under the hood,
Batteries included, Out of the box, Zero to hero, Level up,
Take it to the next level, Hit the ground running,
From day one, Game changer, No-brainer, A breath of fresh air,
Sits at the intersection of, Purpose-built for, Thoughtfully designed
```

## 1.4 CTA & Button Labels
**Banned:**
```
Get Started, Get Started Today, Start Free, Start Your Free Trial,
Try Demo, Try it Free, Learn More, Explore Features, Unlock Now,
Discover, Dive in, See how it works, Book a demo, Supercharge your…,
Join the revolution, Claim your spot, Reserve your seat,
Take the first step, See it in action, Request access,
Start building, Start creating, See the magic, See the difference
```
**Use:** The verb the button performs: `Save`, `Post thread`, `Sign in`, `Continue`, `Run`, `Export`, `Create account`, `Delete`, `Filter`, `Download`, `Send message`, `Upload file`, `Add row`, `Submit`, `Cancel`, `Close`, `Back`, `Next`, `Done`.

One CTA style for the whole app. No mixing.

## 1.5 UI Microcopy

| Context | AI (banned) | Human (use) |
|---|---|---|
| Empty list | "Nothing here yet! Your journey starts soon ✨" | "No threads yet." |
| Empty search | "We couldn't find what you're looking for 🔍" | "No results for 'xyz'." |
| Empty inbox | "Your inbox is empty! Time to start connecting 💬" | "No messages." |
| Empty dashboard | "Welcome! Let's set up your dashboard 🎉" | "No data yet. Add your first entry." |
| Login heading | "Welcome back, hero!" | "Sign in" |
| Login subtext | "Sign in to continue your journey" | *(none — the form is self-explanatory)* |
| Register heading | "Join our amazing community!" | "Create account" |
| Register subtext | "Start your journey today" | *(none)* |
| Success toast | "Awesome! You're all set! 🎉" | "Saved." |
| Success toast 2 | "🎉 Successfully created!" | "Thread created." |
| Account created | "Welcome aboard! We're thrilled to have you!" | "Account created. You're signed in." |
| Error toast | "Oops! Something went wrong! 😅" | "Could not save. Try again." |
| Server error | "We're experiencing issues, please bear with us" | "Server error. Retry in a moment." |
| Validation error | "Hmm, that doesn't look right" | "Email is required." |
| Network error | "Looks like you're offline! 📡" | "No connection." |
| Search placeholder | "Search anything…" / "What are you looking for?" | "Search threads" / "Search members" |
| Upgrade prompt | "Unlock premium features! ✨" | "Pro — $9/mo" |
| Onboarding | "Let's get you started on your journey… 🚀" | "Create account" |
| Notification | "You've been mentioned! 🔔" | "John replied to your thread." |
| Loading text | "Hang tight! We're preparing something… ✨" | "Loading…" / *(spinner only, no text)* |
| Loading skeleton | "Almost there! Getting things ready…" | *(silent skeleton or spinner)* |
| Confirm delete | "Are you sure? This can't be undone! 😱" | "Delete this thread? This is permanent." |
| Confirm action | "You're about to do something awesome!" | "Confirm: publish this draft?" |
| Password field | "Create a strong password to secure your journey" | "Password (8+ characters)" |
| 404 page | "Oops! Looks like you're lost in space 🚀" | "Page not found." |
| 403 page | "Access denied! You don't have superpowers for this" | "No permission." |
| 500 page | "Our hamsters are fixing things! 🐹" | "Server error." |
| Maintenance | "We're making things even better! Be right back ✨" | "Down for maintenance. Back at 3pm." |
| Feature pitch | "Unlock the power of real-time analytics" | "View weekly active users" |
| Welcome banner | "Welcome to {App}! We're so glad you're here 🎉" | *(don't show a welcome banner)* |
| Cookie banner | "We use cookies to enhance your experience ✨" | "This site uses cookies. [Accept] [Decline]" |
| Newsletter signup | "Stay in the loop! Get exclusive updates 📬" | "Email updates" / *(skip if nobody asked)* |
| Tooltip | "Pro tip! 💡 You can also..." | "Keyboard shortcut: Ctrl+S" |
| Logout confirm | "Leaving so soon? 😢" | "Sign out?" |
| Password changed | "Your password has been updated successfully! 🔒" | "Password changed." |
| Profile saved | "Looking good! Your profile is updated ✨" | "Profile saved." |
| File uploaded | "File uploaded successfully! 🎉" | "File uploaded." |
| Item deleted | "Poof! It's gone! 🗑️" | "Deleted." |
| Copied to clipboard | "Copied! You're all set ✨" | "Copied." |
| Form submitted | "Thanks for reaching out! We'll be in touch 🤝" | "Submitted." |

## 1.6 Banned Sentence Patterns
- **Triad slogans:** `Fast. Secure. Simple.` / `Build. Ship. Scale.` / `Create. Collaborate. Ship.`
- **"designed to / built to / made to"** + abstract benefit
- **"whether you're a… or a…"** constructions
- **Rhetorical question headings:** `Why choose us?` / `Ready to get started?` / `What makes us different?`
- **"not just X, but Y":** `Not just a tool, a partner`
- **Parenthetical hype:** `(and it's blazing fast!)` / `(yes, really!)`
- **Em-dash fluff:** `— and it just works —` / `— from anywhere —`
- **Sentence-initial "And" for drama:** `And the best part?`
- **False scarcity:** `Limited spots!` / `Only 3 left!` (when untrue)
- **"We" statements about feelings:** `We believe in…` / `We're passionate about…` / `We care deeply about…`
- **Vague social proof:** `Loved by thousands` / `Trusted by teams worldwide`
- **Fake specificity:** `Built by developers, for developers` / `Made by creators, for creators`
- **Anthropomorphizing the product:** `{App} understands your needs` / `{App} learns and adapts`

**Rules:**
- One idea per sentence. Cut the second clause.
- Delete adjective if you cannot cite a number.
- Replace banned verbs with the actual action.
- Empty states: fact + next action, zero cheerleading.
- No exclamation marks in system UI text. Reserve for user-generated content.

## 1.7 Ranks & Gamification
**Banned fantasy titles:**
```
System Founder, Celestial Luminary, Holographic Prestige,
Digital Architect, Cyber Guardian, Neon Sage, Elite Vanguard,
Astral Pioneer, Cosmic Sentinel, Shadow Alchemist, Code Wizard,
Tech Ninja, Growth Hacker, Community Champion, Forum Wizard,
Power User, Super Contributor, Legendary Member, Elite Member,
Platinum Member, Diamond Tier, Mythic Rank
```
**Use:** `Admin`, `Mod`, `Member`, `Level 12`, `New member`, `Regular`, `Contributor`, `Staff`.
State the requirement plainly: "50 posts" not "Ascend to new heights."

## 1.8 Live / Real-Time Label Abuse

| Actual tech | Correct label |
|---|---|
| WebSocket / SSE push | Live |
| True presence (who's online) | Online |
| Polling / auto-refresh | Updated 2m ago |
| Static dashboard | Dashboard, Activity |
| Preview panel | Preview |
| Cron/scheduled sync | Synced hourly |

Never tag polling or static dashboards as "Live" or "Real-Time."

## 1.9 SEO & Meta Text
- **Banned:** `"Explore the latest discussions designed to empower users…"`
- **Use:** `"Recent forum threads and replies."`
- **Page titles:** `Phorum — Community Forum` not `Home — Premium Community Experience`
- **Meta descriptions:** Name what the page shows, do not sell.

## 1.10 Docs & README
**Banned:**
- Badge walls (rows of shields.io)
- `Enterprise-Grade High-Performance Platform`
- Numbered "Key Features" with adjectives, no data
- Emoji section headers (`## ⚡ Features` / `## 🚀 Getting Started`)
- Repeated superlatives
- No mention of limitations
- Contributing guide for a solo project
- Code of conduct in a personal repo
- Table of contents for 3 sections

**Use:**
- One sentence: what it is + who for
- Install / run commands that work
- Real limits: `no auth yet`, `SQLite only`, `max 1000 rows`
- Boring headings: Install, Config, Deploy, Limits

## 1.11 Punctuation & Formatting Tells
- Too many **bold** words in a paragraph
- `!!!` or emoji in headings
- Long em-dash asides — like this — everywhere
- Parenthetical hype: `(and it's fast!)`
- Quote-like fluff: `"The future of X"`
- ALL CAPS feature names: `LIGHTNING MODE`, `TURBO SYNC`, `SMART ENGINE`
- Exclamation marks in system messages (reserve for user content)
- Ellipsis for mystery: `And that's just the beginning…`
- Oxford comma debates in tech writing (just be consistent)

---

# PART 2 — VISUAL DESIGN & CSS

## 2.1 Banned Visual Tropes

| AI Trope | Why generic | Use instead |
|---|---|---|
| Glassmorphism everywhere (`backdrop-filter: blur`) | Every AI tool defaults to it | Solid bg with `1px` border or 2-4 shade surface diff |
| Neon glow shadows (`box-shadow: 0 0 20px rgba(99,102,241,0.4)`) | Crypto dashboard aesthetic | `0 1px 3px rgba(0,0,0,0.08)` or no shadow |
| Gradient text (`background-clip: text`) | Kills readability, pure decoration | Solid text color from `DESIGN.md` |
| Decorative gradients on content areas | Forum/dashboard don't need gradient headers | Flat bg. One subtle ambient gradient max |
| Cards inside cards | Nesting destroys hierarchy | Flat list with dividers, or single-level card |
| Identical card grid for everything | Same-size cards for stats, feeds, profiles | Table for data, list for feeds, inline for metadata |
| Hero + 3 features + CTA | Default AI landing page template | Design for actual content and user flow |
| Floating/overlapping decorative shapes | Random blurred circles, mesh gradients | Clean background. Content is the visual |
| Rainbow / multi-color accent abuse | 5+ accent colors = chaos | Max 1 accent per viewport |
| Dark mode + neon by default | AI default look | Project's `DESIGN.md` palette. Light mode is fine |
| Split-screen auth pages | Half illustration, half form | Simple centered form. Skip the illustration |
| Oversized hero sections | 100vh hero on a utility tool | Content visible above fold without scrolling |
| Rounded everything (`border-radius: 24px`) | Bubbly toy look on data-heavy UIs | `4px` inputs, `8px` cards, `9999px` pills only |
| Frosted/blurred header/navbar | `backdrop-filter` on sticky nav | Solid opaque header background |
| Decorative dividers (gradient lines, wave SVGs) | Looks like a template | Simple `1px border` or whitespace |
| Asymmetric blob backgrounds | Random organic shapes behind content | No blobs. Solid or very subtle texture |
| Oversized icons as hero elements | Giant Lucide/Heroicon as the main visual | Screenshot, data preview, or nothing |
| Full-bleed color sections alternating | Marketing page template rhythm | Consistent background with spacing and headings |
| Neumorphism (soft emboss shadows) | Dated 2020 trend, poor accessibility | Flat with borders |
| Skeuomorphism (fake textures) | Leather, paper, wood backgrounds | Flat color |
| Parallax scrolling | Nausea-inducing, perf cost | No parallax |
| Scroll-triggered animations everywhere | Every section fades/slides in | Content renders immediately |

## 2.2 Banned CSS Patterns

```css
/* Neon glow on everything */
box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
box-shadow: inset 0 0 30px rgba(59, 130, 246, 0.2);

/* Gradient text */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;

/* Glassmorphism on content cards */
background: rgba(255, 255, 255, 0.05);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.1);

/* Excessive radius on rectangular content */
border-radius: 24px; /* on a table or thread list */

/* Decorative floating blobs */
.blob { position: absolute; border-radius: 50%; filter: blur(80px); }

/* Rainbow borders */
border-image: linear-gradient(to right, #f00, #0f0, #00f) 1;

/* Hover scale on list items */
.card:hover { transform: scale(1.05); }
.row:hover { transform: translateY(-4px); }

/* Gradient buttons (unless DESIGN.md says so) */
background: linear-gradient(135deg, #6366f1, #8b5cf6);

/* Frosted nav */
nav { backdrop-filter: blur(12px); background: rgba(0,0,0,0.5); }

/* Decorative underline animations */
a::after { content: ''; transform: scaleX(0); transition: transform 0.3s; }
a:hover::after { transform: scaleX(1); }
/* (on every nav link — one or two max is fine) */

/* Text shadow glow */
text-shadow: 0 0 10px rgba(99, 102, 241, 0.5);

/* Animated gradient backgrounds */
background-size: 400% 400%;
animation: gradient-shift 15s ease infinite;
```

## 2.3 What to Use Instead

```css
/* Shadows: subtle, functional */
box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);

/* Borders: visible, thin */
border: 1px solid var(--border-color);

/* Radius: match content type */
border-radius: 4px;     /* inputs, small elements */
border-radius: 8px;     /* cards, modals */
border-radius: 9999px;  /* pills, avatars, chips only */

/* Backgrounds: solid tokens */
background-color: var(--surface);
background-color: var(--surface-alt);

/* Hover: subtle, single property */
.row:hover { background-color: var(--surface-alt); }
.btn:hover { opacity: 0.9; }

/* Focus: visible, accessible */
:focus-visible { outline: 2px solid var(--primary); outline-offset: 2px; }
```

---

# PART 3 — LAYOUT & COMPONENT ANTI-PATTERNS

## 3.1 Layout Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Everything in a card with shadow | Visual noise, no hierarchy | Cards sparingly. Most content on page surface with dividers |
| 3-column equal card grid for stats | Fake symmetry, wastes space | Inline stat row, `<dl>`, or compact table |
| Sidebar + main both scrollable | Broken scroll on mobile | One scroll context. Sidebar collapses on mobile |
| Full-width alternating bg sections | Landing page template | Consistent bg, use spacing/headings for sections |
| Icon + Title + Vague Sentence cards | Every AI landing page | Skip for tools. Show screenshot or real data |
| Modal for everything | Settings, view, edit, confirm all modals | Inline editing, dedicated pages, modals for destructive only |
| Dashboard with 6+ metric cards | Overload, no focus | 1-2 key metrics prominent, rest in table |
| Masonry for non-image content | Confusing for text | Standard list or table |
| Two-column layout forced on mobile | Content squished | Single column on mobile, always |
| Sticky everything (header + sidebar + footer) | Viewport consumed by chrome | Sticky header only. Sidebar and footer scroll naturally |
| Fixed-width centered content < 600px | Wastes desktop space on data-heavy apps | Content-appropriate max-width: `720px` text, `1200px` dashboards |
| Full-height sidebar with scroll | Two scroll contexts | Sidebar scrolls with page or collapses |

## 3.2 Navigation Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Hamburger menu on desktop | Hides primary nav on big screens | Visible horizontal nav on desktop, hamburger on mobile only |
| Mega menu with categories on a 5-page site | Over-engineering | Simple link list |
| Sticky header with blur/glassmorphism | Transparency distracts from content | Solid opaque header |
| Breadcrumbs on a flat site (Home > Page) | Useless on 2-level nav | Only if 3+ levels deep |
| Tab bar with 6+ items on mobile | Overflow, tiny tap targets | Max 4-5 items. Overflow into "More" |
| Logo as only home link (no "Home" text) | Users don't always click the logo | Logo links to home, OR explicit "Home" in nav |
| Active state identical to hover state | Can't tell where you are | Active = persistent visual (underline, bg), hover = transient |
| Icon-only nav without tooltips | Guessing game | Text labels, or icons with visible tooltips |
| Animated menu transitions (slide-in from right, bounce) | Slows navigation | Instant show/hide. 150ms fade max |
| Transparent header over hero image | Text unreadable on some images | Solid header, or guaranteed dark overlay on image |

## 3.3 Form Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Multi-step wizard for 4 fields | Over-engineered, annoying | Single form. Wizards only for genuinely complex flows (10+ fields) |
| Floating labels (label inside input, moves up) | Accessibility issues, placeholder disappears | Static label above input, always visible |
| Inline validation with green checkmarks on every field | Distracting, patronizing | Validate on submit. Inline only for username/email availability |
| Password strength meter blocking submit | Users fight the meter | Minimum requirement stated plainly. Meter optional, never blocking |
| Character counter on non-limited fields | "0/∞" is meaningless | Only show when there's an actual limit |
| Custom styled selects/dropdowns | Broken keyboard nav, accessibility | Native `<select>` for simple lists. Custom only if searchable |
| Custom styled checkboxes/radios | Often break screen readers | Style with `appearance: none` + pseudo-elements, keep native `<input>` |
| Toggle switch for single binary option | Often unclear what on/off means | Checkbox with clear label. Toggle only in settings panels |
| Date picker for typing a known date | Clicking through months is slower than typing | Text input with format hint (`YYYY-MM-DD`), date picker as optional |
| Disabled submit button until valid | User doesn't know what's wrong | Always enabled submit. Show errors on click |
| Placeholder text as label | Disappears on focus, not accessible | Real `<label>` element above input |
| Required field asterisk without legend | What does * mean? | `* Required` legend at top, or just say "All fields required" |
| Accordion forms (sections collapse) | Context lost, scroll jumps | Flat form with sections separated by headings |
| Input with icon inside (search glass, email icon) | Often misaligned, takes space | Icon left of input group, or no icon |
| Form in a modal | Can't bookmark, can't share, scroll issues | Dedicated page for forms with >3 fields |
| Success page after form submit | Unnecessary redirect | Inline success message or toast |

## 3.4 Table & Data Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Zebra striping + hover + shadow + rounded | Visual overload | Pick one: zebra OR hover highlight. Not both |
| Wrapping table in a card with shadow | Shadow on data is noise | Table on page surface, subtle header bg |
| Horizontal scroll table without indicator | User doesn't know to scroll | Fixed first column, or show scroll shadow |
| Pagination for < 20 items | Unnecessary clicks | Show all if under 50 items |
| "Showing 1-10 of 10" on single page | Useless info | Hide pagination when all items fit |
| Action buttons in every row (Edit, Delete, View) | Visual clutter | Actions on hover/right-click, or batch actions |
| Icon columns for status when text works | Colored dots without legend | Text: "Active", "Pending", "Rejected" |
| Sortable columns with no indication of default sort | Confusing initial state | Show default sort arrow |
| Empty table with illustration | Cute robot/astronaut for "no data" | "No records." + action link |
| Charts for 2-3 data points | Pie chart with 2 slices is a waste | Text: "80% active, 20% inactive" |
| Full-width table on desktop | Columns stretched to fill | Max-width table, left-aligned |
| Nested tables | Confusing hierarchy | Expandable rows or detail panel |

## 3.5 Modal & Dialog Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Modal for non-destructive view | Can't bookmark, can't share | Dedicated page or inline expand |
| Modal chains (modal opens modal) | Disorienting, z-index hell | Flat flow: page 1 → page 2 |
| Full-screen modal for simple form | Overkill, no escape context | Centered modal or inline form |
| Modal with scrollable content > viewport | Scroll within scroll | Dedicated page |
| Confirmation modal for safe actions | "Are you sure you want to save?" | Just save. Confirm only for delete/irreversible |
| Close button as tiny X in corner | Hard to tap on mobile | Visible "Cancel" button + click outside to close |
| Modal with backdrop that doesn't close on click | Trapped feeling | Click backdrop = close (except for critical confirms) |
| Animation: scale + fade-in from center | Slow entry, 300ms+ | Instant appear, or 150ms fade only |
| Multiple overlapping modals | z-index chaos | Max 1 modal at a time. Use pages for complex flows |

## 3.6 Toast & Notification Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Auto-dismiss on errors | User can't read the error | Errors persist until dismissed manually |
| Stacking 5+ toasts | Screen clutter | Max 3 visible. New replaces oldest |
| Success toast for expected action | "Saved successfully!" after clicking Save | Skip toast for expected outcomes. Show only for async/background |
| Toast with action button (Undo) that auto-dismisses in 3s | User can't click in time | Undo toast stays 8s minimum, or persists |
| Emoji in toasts | "🎉 Thread created!" | "Thread created." |
| Toast position varies (top, bottom, left, right) | Inconsistent | Pick one position for the whole app. Top-right or bottom-center |
| Full-width banner toast | Takes too much space | Fixed-width toast: 300-400px |

## 3.7 Sidebar Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Collapsible sidebar with icon-only mode | Icons without labels = guessing | Either always show labels, or hide sidebar entirely |
| Nested accordion menus 3+ levels | Lost in tree structure | Max 2 levels. Use pages for deeper nav |
| User avatar + full name + role in sidebar header | Wastes 80px of prime nav space | Small avatar in header bar, or just the name |
| Color-coded section dividers in sidebar | Rainbow sidebar | One subtle divider color |
| Sidebar wider than 280px | Eats content space on laptops | 220-260px max |
| Notification badges on every sidebar item | Everything screams for attention | Badges only on items with actual unread counts |
| Sidebar footer with version number + "Made with ❤️" | Wasted space, AI cliché | Remove, or put version in settings page |

## 3.8 Footer Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| 4-column mega footer on a 5-page site | Over-engineered | 1-line footer: copyright + key links |
| Social media icons for accounts that don't exist | Links to empty profiles | Only show social links if accounts are active |
| Newsletter signup in footer | Nobody signs up from the footer | Skip unless there's real email content |
| "Made with ❤️ by {Name}" | AI cliché | "© 2026 {Name}" or nothing |
| "Built with React, Tailwind, Node.js" tech stack | Users don't care | Remove |
| "Back to top" button | Browser has scroll bar and Home key | Remove unless page is 5000px+ |
| Dark footer on light site (or vice versa) | Visual disconnect | Same color scheme as the rest |
| Footer with 20+ links | Nobody reads these | Max 8-10 essential links |

---

# PART 4 — DASHBOARD & AUTH PATTERNS

## 4.1 Dashboard Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| "Good morning, Keith! 👋" greeting | Patronizing, wastes header space | No greeting. Show the data |
| 4-6 stat cards with colored icons and trend arrows | Information overload, no focus | 1-2 key numbers inline. Rest in a compact table or list |
| Every stat card has a different color | Rainbow dashboard | Neutral cards. Color only for status (red=down, green=up) |
| "Recent Activity" feed with identical entries | No hierarchy, wall of text | Group by day, highlight important events only |
| Donut/pie chart for 2 categories | Useless visualization | Text: "80 active, 20 inactive" |
| Line chart with 3 data points | Not enough data to chart | Table or single number |
| Full-width charts that are mostly empty space | Wasted viewport | Right-size charts to their data |
| "Quick Actions" card with 3 buttons | Those buttons should be in the nav | Put actions where they're contextual |
| Skeleton loading on a dashboard that loads in 200ms | Flicker of skeleton then content | No skeleton for fast loads. Skeleton only if >500ms |
| Auto-refreshing everything every 5s | Server load, battery drain | Refresh on user action, or 60s+ interval with "Updated X ago" |
| Dashboard tour/walkthrough overlay on first visit | Annoying, users click through | Let the UI be self-explanatory. Tooltip on hover for complex features |
| KPI cards that nobody has defined | "Revenue", "Growth", "Engagement" with $0 | Only show metrics that have real data |

## 4.2 Auth Page Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Split-screen: illustration left, form right | Template look | Centered form, simple page |
| Gradient background on auth page | AI aesthetic | Solid background matching the site |
| "Welcome back! We missed you" heading | Cringe | "Sign in" |
| Social login buttons (Google, GitHub) when not implemented | Empty promises | Only show implemented auth methods |
| "Or continue with" divider between social + email login | Over-designed for 1 method | Skip divider if only one auth method |
| Password visibility toggle as eye icon without label | What does the eye do? | "Show password" checkbox, or labeled icon |
| "Forgot password?" styled as tiny gray link | Hard to find when you need it | Visible link, normal size |
| "Don't have an account? Sign up" below login form | Fine, but AI over-styles it with colors | Plain text link, same size as other links |
| CAPTCHA on a forum with 10 users | Friction for no reason | CAPTCHA only when spam is an actual problem |
| Email verification wall before any access | Blocks exploration | Let users browse. Verify when they try to post |
| Terms checkbox that must be checked | Legal theater for a personal project | Link to terms in footer. Checkbox only if legally required |
| Animated background on login page | Particle.js, wave SVGs | Static, clean background |

## 4.3 Profile & Settings Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Avatar upload with crop modal | Over-engineered for a profile photo | Simple file input. Server-side crop to square |
| Tabs for 2 settings sections | Tabs are overhead for 2 panels | One scrollable page with headings |
| Toggle switches for everything | Unclear what on/off means without context | Checkboxes with labels for most. Toggles for live-effect settings |
| "Danger Zone" section styled in red | GitHub influence, dramatic for a small app | "Delete account" at bottom, normal styling, confirmation prompt |
| "Your profile is 60% complete!" progress bar | Nagging, patronizing | Skip. Required fields are enforced at input |
| Cover photo upload | Most users leave it default = wasted space | Skip unless visual profiles are core to the app |
| Theme selector with 10 themes on day one | Premature feature, maintenance burden | Light/dark toggle at most. Ship one good theme |
| Activity heatmap (GitHub-style green squares) | Cool but useless for most apps | Skip unless contribution tracking is the product |

---

# PART 5 — TYPOGRAPHY, COLOR, ANIMATION

## 5.1 Typography Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| 48px+ hero heading on utility page | Not a marketing site | Max 32px for app pages. 48px only for landing hero |
| Gradient/colored headings | Distracting, contrast risk | Solid color, high contrast |
| Multiple weights in one paragraph (300/400/600/700) | Messy | 2 weights max: regular + semibold |
| Letter-spacing on body text | Hurts reading speed | `letter-spacing: 0` for body. `0.02-0.05em` for labels only |
| Uppercase everything | NAV, LABELS, HEADINGS all caps | Uppercase for short labels only (badges, tabs). Sentence case everywhere else |
| Decorative pull-quotes in a dashboard | This isn't a magazine | Delete |
| Fancy display font for body text | Hard to read at 14-16px | System font or readable sans-serif for body |
| 12px body text | Unreadable for many users | 14px minimum, 16px preferred |
| Line-height < 1.4 on body | Cramped, hard to scan | 1.5-1.6 for body text |
| Justified text (`text-align: justify`) | Uneven word spacing | Left-aligned |
| Mixing 3+ font families | Chaotic | 1 font family. 2 max (heading + body) |

## 5.2 Color Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Indigo/purple default (`#6366f1`, `#8b5cf6`) | Most recognizable AI color | Project's brand color from `DESIGN.md` |
| Neon green on dark bg | Hacker look, unreadable on light | Muted, accessible accent |
| Multiple accent colors per page | Rainbow, no hierarchy | 1 accent per viewport |
| Pure black bg (`#000`) | Harsh, contrast fatigue | `#111`, `#1a1a1a`, `#18181b` |
| Pure white text on pure black | Max contrast = eye strain | `#e5e5e5` on `#1a1a1a` |
| Status colors as decoration | Red/green/yellow on everything | Status colors for actual status only |
| Gradient badges | AI loves gradient pills | Solid bg, single color |
| Opacity-based color system | `rgba(white, 0.1)` for everything | Named semantic tokens: `--surface`, `--border` |
| Colored sidebar nav items | Each section a different color | One highlight color for active, neutral for rest |
| Tinted backgrounds (blue-tinted gray, purple-tinted white) | Muddy, inconsistent | Clean grays or DESIGN.md surface colors |

## 5.3 Animation & Motion Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Hover lift on every card (`translateY(-4px)`) | Distracting on 20-item list | Background color change only |
| Scale on hover (`transform: scale(1.05)`) | Layout shift, toyish | `opacity: 0.9` or bg change |
| Entrance animations on every element | Staggered fade-in = slow, annoying | Content loads instantly |
| Infinite pulse/glow on badges | Attention-stealing, ad-like | Static |
| Parallax scrolling | Nausea, perf cost | No parallax |
| Smooth scroll forced | Unexpected motion | `scroll-behavior: auto`. User OS handles smoothness |
| Skeleton shimmer on fast-loading content | 200ms shimmer then content = flicker | Skeleton only if genuinely async >500ms |
| Counter animation (numbers counting up) | Vanity metric delay | Show number immediately |
| Page transition animations | Slide/fade between pages = slow | Instant page render |
| Typing animation on headings | "Watch the text appear letter by letter" | Render text immediately |
| Confetti on success | Patronizing | *(delete)* |
| Bounce on scroll | Elements bounce into view | Render in place |
| Loading spinner for <200ms operations | Unnecessary flash | No spinner. Show result instantly |
| Progress bar for single-step operation | Fake progress | Spinner if needed, or nothing |
| Hover animations on mobile (no hover exists) | Dead CSS, confusing touch feedback | Use `:active` for touch, `:hover` for pointer devices |

---

# PART 6 — ICONS, IMAGES & ASSETS

## 6.1 Icon Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Icon next to every single menu item | Visual noise | Icons for primary nav only. Text labels are fine alone |
| Decorative icons on stat cards | Icon doesn't add info | Skip icon if the label is clear |
| Colored icon matching card/section color | Rainbow icon set | One icon color (neutral/gray), or inherit text color |
| Icon-only buttons without labels or tooltips | Guessing game | Add text label, or aria-label + tooltip |
| Mixing icon sets (Heroicons + FontAwesome + Lucide) | Inconsistent stroke/style | One icon set per project |
| Outline AND filled icons mixed | Inconsistent | Pick one style: outline or filled |
| Custom icon for common actions | "Why is save a flower?" | Use standard metaphors: disk=save, trash=delete, pencil=edit |

## 6.2 Image & Media Anti-Patterns

| AI Pattern | Problem | Fix |
|---|---|---|
| Stock photos (handshake, laptop, team) | Screams template | Real product screenshot, or skip |
| Rounded corners on all images equally | 24px radius on a 40px avatar = circle | Match border-radius to context |
| Gradient overlay on hero images | Template dark overlay | Solid dark bg + text, or clean image |
| Aspect ratio inconsistent in grids | Some tall, some wide | Enforce consistent ratio (`aspect-ratio: 16/9`) |
| AI-generated illustrations (isometric, flat) | Recognizably AI | Real screenshots, simple SVG icons, or nothing |
| Full-width hero image on every page | Wastes viewport, slows load | Hero on landing only. Content pages start with content |
| Background video on landing page | Auto-play, perf, battery, accessibility | Static image. Video only if product is video-related |
| SVG illustrations for every empty state | Over-designed for "no data" | Text: "No results." |

---

# PART 7 — CODE STRUCTURE TELLS

## 7.1 HTML Structure Tells

| AI Pattern | Problem | Fix |
|---|---|---|
| Wrapper div nesting 8+ levels deep | DOM bloat, hard to style | Flatten structure. 3-4 levels max for most components |
| `<div>` for everything | No semantics | `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<button>` |
| `<span>` with click handler instead of `<button>` | Not keyboard accessible | Real `<button>` element |
| `<a>` without `href` styled as button | Not a link, not a button | `<button>` for actions, `<a href>` for navigation |
| `<div class="container"><div class="wrapper"><div class="inner">` | Triple nesting for one container | Single container with padding |
| Every section wrapped in `<div class="card">` | Cards everywhere | Content on page surface, cards for grouped items only |
| `role="button"` on a `<div>` | Just use `<button>` | `<button>` |
| `<img>` without `alt` or with `alt="image"` | Accessibility fail | Descriptive alt, or `alt=""` for decorative |
| `<table>` avoided entirely in favor of flexbox/grid | Tables are correct for tabular data | Use `<table>` for data tables |

## 7.2 CSS Structure Tells

| AI Pattern | Problem | Fix |
|---|---|---|
| Utility classes for everything (no component CSS) | Hard to maintain when not using Tailwind | Component CSS files |
| `!important` to fix cascading issues | Root cause not fixed | Fix specificity at the source |
| Inline styles to override | Same as `!important` | Fix in the stylesheet |
| 500+ line single CSS file | Unmaintainable | One file per component |
| CSS custom properties for every value | `--card-padding-top-left: 16px` | Tokens for repeated values only: colors, spacing scale, radii |
| Generic class names: `.container`, `.wrapper`, `.card`, `.title` | Conflicts, no searchability | `.thread-list__card`, `.user-profile__title` |
| Deeply nested selectors: `.page .section .card .header .title span` | Fragile, high specificity | `.thread-title` flat selector |
| Duplicated values instead of variables | Change in 20 places | Token in `:root`, reference everywhere |

## 7.3 JS/Logic Tells

| AI Pattern | Problem | Fix |
|---|---|---|
| Comments explaining obvious code | `// increment counter` above `counter++` | Comment why, not what |
| TypeScript interface for 2 properties | Overhead for trivial types | Inline type or skip for simple objects |
| Abstracting single-use functions | `formatUserName()` called once | Inline the logic where it's used |
| `console.log` left in production | Debug noise | Remove or use proper logger |
| Try/catch that swallows errors silently | Bugs hidden | Log or rethrow. Never empty catch |
| Fetching data on every render without caching | Wasted requests | Cache/memo, or fetch on mount only |
| useState for everything (when useRef or derived state works) | Unnecessary re-renders | Derive from existing state when possible |
| Over-componentizing (Button, Text, Box primitives on day 1) | Premature abstraction | Extract component when reused 3+ times |
| `setTimeout` / `setInterval` for polling without cleanup | Memory leak | Cleanup in useEffect return, or AbortController |

---

# PART 8 — QUICK CHECKLIST

Before shipping any UI, copy, or code:

**Copy:**
- [ ] No banned adjective or verb in any visible text
- [ ] CTAs use literal action verbs
- [ ] Empty states: fact + action, no cheerleading
- [ ] Error messages name what failed + what to do
- [ ] No exclamation marks in system UI text
- [ ] No emoji in headings, labels, or toasts
- [ ] Ranks use plain names
- [ ] `LIVE` label only on true push/WebSocket
- [ ] Page title and meta: name the page, don't sell
- [ ] No "Welcome to {App}!" anywhere

**Visual:**
- [ ] No glow shadows or gradient text
- [ ] No glassmorphism (unless DESIGN.md explicitly says so)
- [ ] Max 1 accent color per viewport
- [ ] No hover lift/scale on list items
- [ ] Cards used sparingly, not default wrapper
- [ ] No decorative blobs, waves, or floating shapes
- [ ] No entrance animations on content
- [ ] No confetti, no typing animation, no counter animation
- [ ] Auth pages: centered form, no split-screen illustration
- [ ] Dashboard: no greeting, max 2 prominent stats

**Code:**
- [ ] Semantic HTML elements, not div soup
- [ ] No wrapper nesting beyond 4 levels
- [ ] One CSS file per component, no generic names
- [ ] No `!important`, no inline style overrides
- [ ] No silent catch blocks
