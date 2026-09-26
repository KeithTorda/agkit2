---
part: 16
title: Navigation
covers: header, navbar, mega menu, hamburger, mobile menu, sidebar, breadcrumbs, tabs, bottom tab bar, pagination, footer, back buttons, active states, skip links, command palette, search in nav, user menu, notification bell, government and school site navigation
---

# 16 — Navigation

Read when: building a header, navbar, sidebar, menu, tabs, breadcrumbs, pagination, footer, or any control that moves the user between pages or views.

## 16.1 Header

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Sticky header with blur (original 3.2) | Frosted glass nav, the default AI look. Blur costs GPU on low-end phones. | Solid header on a surface token from DESIGN.md with a 1px bottom border. |
| Transparent header over hero image (original 3.2) | Nav text unreadable over light parts of the photo. | Solid header, or a guaranteed dark overlay behind nav text that passes 4.5:1. |
| Header that changes from transparent to solid on scroll | Scroll listener, layout flash, template behaviour. | One solid state. |
| Header that hides on scroll down, shows on scroll up | Jumps under the finger. Users hunt for it. | Static or plain sticky. |
| Header height 80–96px | Wastes the first screen, more on phones. | 56–64px desktop, 48–56px mobile. |
| "Announcement bar" above the header on every page (`New: v2 is here →`) | Launch template. Copy: see part 08. | Only for time-bound real notices (office closure, enrollment deadline). Dismissible. Removed after the date. |
| Glowing "New" pill in the nav | See part 10. | Plain text label if the item is actually new, removed after 30 days. |
| Header with logo, 7 links, search, language switch, theme toggle, bell, avatar, CTA | Everything in one row. Wraps at 1024px. | Logo, 4–6 primary links, one action. Move the rest to menus or the footer. |
| CTA button in header on a logged-in app ("Get Started", "Upgrade") | Marketing pattern inside a tool. | Logged-in header shows app actions only. Upgrade in billing settings. |
| Two CTA buttons in marketing header ("Sign in" filled + "Get started" gradient) | Two competing primaries. See part 18. | "Sign in" as a text link, one primary button. |
| Theme toggle in header of a site nobody asked dark mode for | Template feature. See part 34. | Follow system preference, or no toggle. |
| Logo as only home link (original 3.2) | Some users do not know the logo is a link. | Logo links home, and include an explicit "Home" link where the audience is general (LGU, school, election sites). |
| Logo at 48px height with tagline beside it | Oversized brand block. | Logo 24–40px tall. Tagline off the header. |
| Header contents not aligned with page container | Different container width. See part 14. | Same container as main. |

## 16.2 Desktop navbar links

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hamburger on desktop (original 3.2) | Hides nav when there is room to show it. | Visible nav links at desktop widths. Hamburger on mobile only. |
| Decorative underline animations on every nav link (original 2.2) | Slide-in or grow-from-center underline on each hover. Template signature. | Static hover state (color or underline appears). An animated underline on one or two links at most. |
| Active same as hover (original 3.2) | User cannot tell where they are. | Active state persistent (weight, underline or indicator bar, `aria-current="page"`). Hover transient and weaker. |
| Nav labels as marketing phrases ("Our Solutions", "Why Us", "Discover") | Vague. Copy: see part 01. | Nouns for what the page contains: "Services", "Pricing", "Officials", "Enrollment", "Contact". |
| Nav labels in ALL CAPS with wide tracking | Shouting. See part 13. | Sentence case. |
| 8+ top-level links | Crowded, wraps. | 4–6 top-level items. Group the rest. |
| Dropdown for a menu with one or two items | Extra click. | Direct links. |
| Pill-shaped hover background sliding between links (animated indicator) | Motion trope. See part 25. | Static hover background or none. |
| Icon before every nav label | Icon noise. See part 26. | Text only in top nav. Icons in the app sidebar only if they aid scanning. |
| "Home" link active on every page because of prefix match | `/` matches all paths. | Exact match for home. Prefix match for sections. |
| Links opening in new tabs | Breaks back button. | Same tab for internal links. New tab only for files when stated. |

## 16.3 Hamburger and mobile menu

Responsive behaviour (scroll lock, breakpoints) is in part 15.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hamburger icon with no label on public sites | Older users miss it. | Icon plus the word "Menu" on LGU, school and general-audience sites. |
| Animated hamburger-to-X morph with 3 bars rotating | Motion trope. | Swap icon instantly, or a 150ms fade. |
| Full-screen overlay menu with giant 48px links and staggered entrance | Agency template. | Panel or drawer with 16–18px links, 44px rows, no stagger. |
| Menu slides in over 400–600ms with bounce | Slow. Original 3.2: animated menu transitions. | Instant, or 150ms fade/slide max. Reduced motion respected. See part 25. |
| Menu button is a `<div>` with click handler | Not keyboard accessible. See part 27. | `<button aria-expanded="false" aria-controls="menu-id">`. |
| Focus not moved into the menu on open or back to the button on close | Keyboard and screen reader users get lost. | Move focus to the first link on open. Return focus to the button on close. Esc closes. |
| Nested accordions 3 levels deep in the mobile menu | Hard to navigate on phones. | Max 2 levels. Deeper items on section landing pages. |
| Menu does not show the current page | No orientation. | Active state in the mobile menu too. |
| Mobile menu missing items that desktop nav has (search, language) | Features lost on mobile. | All desktop nav functions reachable in the mobile menu. |
| Menu opens from the right on one page and the left on another | Inconsistent. | One side for the whole site. |

## 16.4 Mega menu and dropdowns

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Mega menu on 5-page site (original 3.2) | Structure far bigger than content. | Simple link list in the header. |
| Mega menu with icons, descriptions, featured card, image, and CTA per column | SaaS template. | Mega menu only for 20+ destinations. Plain grouped links with short headings. No featured cards. |
| Dropdown opens on hover only | Touch and keyboard fail. See part 15. | Opens on click. Hover open optional on desktop, with a delay of 150–300ms to avoid flicker. |
| Dropdown closes when the pointer crosses a gap | Fiddly. | No gap between trigger and menu, or a hover-intent delay. |
| Top-level item is both a link and a dropdown trigger | First tap navigates on touch. | Trigger is a button. The section overview is the first link inside the menu. |
| Dropdown menus using `role="menu"` for site navigation | Wrong pattern; changes keyboard expectations. See part 27. | Disclosure pattern: `<button aria-expanded>` + list of links. `role="menu"` only for app action menus. |
| Chevron that rotates 180 degrees with a spring animation | Motion trope. | Chevron changes direction instantly or with a 150ms transition. |
| Dropdown with shadow-2xl, blur, and 16px radius | Stacked effects. See part 11. | Surface token, 1px border, small shadow, radius token. |

## 16.5 Sidebar

Sidebar geometry (width, scroll) is in part 14. These rows cover content and behaviour. Original 3.7 items are included.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Icon-only collapse mode (original 3.7) | Icons without labels require memorising. Tooltips only on hover. | Keep labels, or hide the sidebar fully behind a toggle. |
| 3+ level accordions (original 3.7) | Deep trees in a sidebar. | Max 2 levels. Third level as tabs or a list on the section page. |
| Avatar + name + role + email block at the top of the sidebar (original 3.7) | Profile card template. Takes 120px. | Small avatar in the header bar with a user menu (16.14). |
| Color-coded dividers or colored section labels (original 3.7) | Rainbow sidebar. | One neutral color for dividers and labels. |
| Wider than 280px (original 3.7) | Steals content width. | 220–260px. |
| Badges everywhere (original 3.7): "New", "Pro", counts on every item | Noise. Counts lose meaning. | Only real unread or pending counts, from data. Hide the badge at 0. |
| Footer with version + "Made with ❤️" (original 3.7) | Template footer in a tool. | Remove. Version in Settings > About if needed. |
| Every item with a different colored icon | Decoration. See part 26. | One icon color from tokens, or no icons. |
| Active item with gradient background and glow | See part 10 and 12. | Active: surface-alt background token plus a 2–3px indicator bar or bold text, and `aria-current="page"`. |
| "Upgrade to Pro" card pinned at the sidebar bottom | SaaS template. | Remove, or one text link in billing. |
| Sidebar section labels in tiny uppercase gray (`text-xs uppercase tracking-wider text-gray-400`) | Template labels, low contrast. | Sentence case, 12–13px, muted token that passes 4.5:1. Or no section labels for short lists. |
| Sidebar lists 20+ items flat | Hard to scan. | Group into 3–6 sections by task. Move rare items (audit log, API keys) under Settings. |
| Nav order copied from a template (Dashboard, Analytics, Projects, Team, Settings) | Items that do not exist in the app. | Items from the app's actual modules, most used first. POS: Sales, Products, Inventory, Reports. Barangay admin: Residents, Certificates, Blotter, Officials, Reports. |
| Collapsed state not remembered | Resets on every page. | Remember in `localStorage` (try/catch) or a cookie. |
| Sidebar collapse button that animates width over 300ms and reflows content | Janky, content jumps. | Instant toggle, or 150ms with content not re-laid mid-animation. |
| Workspace/team switcher at the top when the app has one workspace | Template feature. | Remove until there are multiple workspaces. |

## 16.6 Breadcrumbs

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Breadcrumbs on flat site (original 3.2) | Home > About on a 1-level site. | Only at 3+ levels of depth. |
| Breadcrumb as the only way back | Small target. | Breadcrumb plus page title. Back link where the flow is linear (16.11). |
| Breadcrumb ending in a link to the current page | Self-link. | Last item plain text with `aria-current="page"`. |
| Breadcrumb with icons for each level (home icon, folder icon) | Icon noise. | Text only. Home icon allowed as the first item if labelled. |
| Separators as images or custom SVG chevrons with animation | Decoration. | `/` or `›` in CSS `::before`, `aria-hidden`. |
| Breadcrumb that shows the URL slug ("brgy-clearance-req") | Raw data. | Human page titles ("Barangay clearance requests"). |
| Breadcrumb wrapping to 3 lines on mobile | Too long. | On mobile show only the parent: "‹ Residents". |
| Breadcrumb markup as `<div>` spans | No structure. | `<nav aria-label="Breadcrumb"><ol>…</ol></nav>`. |

## 16.7 Tabs

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Tabs for 2 short sections (see original 4.3) | Hides half the content for no reason. | One page with headings. |
| Tabs used as navigation between pages but coded as ARIA tabs | Wrong semantics, broken back button. | Page navigation: links with `aria-current`. ARIA tabs only for in-page panel switching. |
| Tab state not in the URL | Refresh or share loses the tab. | `?tab=payments` or a route per tab. |
| Sliding pill indicator animation | Motion trope. | Static underline or background on the active tab. |
| Pill/segmented tabs with shadow and gradient active state | Template decoration. | Underline tabs or plain segmented control with token colors. |
| 7+ tabs in a row | Overflow, hidden tabs. | Up to 5–6 visible. Overflow into "More", or a select on mobile. |
| Tabs overflowing on mobile with no cue | Hidden tabs. See part 15. | Horizontal scroll with visible partial tab and edge fade, or a select. |
| Tab labels with icons and counts and badges | Noise. | Text label. Count only if it helps decide (e.g. "Pending (12)"). |
| Nested tabs (tabs inside tab panel) | Two levels of hidden content. | One level. Use headings or a second page. |
| Tab switching animates panel content sliding | Motion trope. | Instant swap. |
| Keyboard: arrows do not move between tabs, or Tab key cycles all tabs | Broken tab pattern. | ARIA tabs: arrow keys move, Tab moves into panel. Or use links. See part 27. |

## 16.8 Bottom tab bar (mobile)

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Tab bar 6+ items on mobile (original 3.2) | Cramped, tiny labels. | Max 4–5 items. Overflow into "More". |
| Icons without labels in the tab bar | Guessing game. | Icon plus a text label, 11–12px min. |
| Center floating "+" button raised above the bar with glow | Social-app template. | A normal tab or a clear "New" button in the page header. |
| Bottom bar and a hamburger menu at the same time with different items | Two navigation systems. | One primary mobile nav pattern. |
| Bottom bar on a public website | App pattern on a content site. | Header menu for websites. Bottom bar for app-like tools (POS, field data collection). |
| Bottom bar ignoring safe area | Overlaps the home indicator. See part 15. | `env(safe-area-inset-bottom)` padding. |
| Active tab shown only by color | Color-only. See part 27. | Filled icon or bold label plus color, `aria-current="page"`. |

## 16.9 Pagination

Pagination vs infinite scroll choice for data lists is in part 19.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Pagination for under 20 items (original 3.4) | Extra clicks. | Show all under 50. |
| "Showing 1–10 of 10" (original 3.4) | Useless when everything fits. | Hide the count and pager when there is one page. |
| Numbered pager with 10 visible page numbers | Crowded, small targets. | First, Previous, current with 1–2 neighbours, Next, Last. On mobile: Previous, "Page 3 of 12", Next. |
| Page numbers 28px wide on mobile | Mis-taps. See part 15. | 44px targets. |
| Pager does not update the URL | Back button and sharing break. | `?page=3` in the URL. |
| Page change scrolls to top of page instead of list top | User loses the list header. | Scroll to the list heading, or keep position. Move focus to the list heading. |
| "Load more" that loses position on back navigation | User returns to page 1. | Keep loaded pages in history state, or use numbered pages. |
| Rounded pill pager with gradient current page | Decoration. | Current page with a border or surface token and `aria-current="page"`. |
| Previous/Next as arrows only | Unclear. | "Previous" and "Next" text, arrows optional. |
| Page size selector with 5, 10, 25, 50, 100, 500 options | Clutter. | 25/50/100 or fixed size. |

## 16.10 Active, hover and focus states in navigation

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| No active state at all | User cannot tell the current page. | Active state on every nav pattern: header, sidebar, tabs, bottom bar, breadcrumbs. |
| Active marked only in CSS with a class, no `aria-current` | Screen readers do not know. | `aria-current="page"` on the active link. Style from `[aria-current="page"]`. |
| Focus outline removed from nav links | Keyboard users lost. See part 27. | `:focus-visible` outline 2px with a token color and 2px offset. |
| Hover effects stronger than the active state | Hovered item looks more selected than the current one. | Active > hover in visual weight. |
| Active parent section not marked when on a child page | Sidebar shows nothing active on deep pages. | Mark the parent section as active (weight or indicator) and the child with `aria-current`. |
| Glow, gradient, or scale on active item | See part 10. | Background token, indicator bar, bold. |

## 16.11 Back buttons

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| In-app back button that calls `history.back()` | Leaves the app when the page was opened from a link, e.g. from Messenger. | Link to the logical parent route ("‹ Residents"). |
| Back arrow icon with no label | Unclear destination. | "‹ Back to residents" or the parent name. |
| Back button on top-level pages | Nowhere to go. | Only on child pages (detail, edit, step pages). |
| Custom back button that loses filters and scroll position of the list | User redoes the search. | Keep list state in the URL. Back link carries it. |
| Back button and breadcrumb both on the same page showing the same parent | Duplicate. | One of them. |
| Browser back breaks inside SPA flows (modals, tabs, wizard steps) | State not in history. | Push history for steps and tabs that feel like pages. Do not push for small UI toggles. |
| Wizard "Back" discards entered data | Data loss. | Keep entered data across steps. See part 17. |

## 16.12 Skip links

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| No skip link on sites with long headers | Keyboard users tab through 20+ links on every page. | "Skip to main content" as the first focusable element, visible on focus, targeting `<main id="main">`. |
| Skip link visible permanently or styled as a banner | Misunderstood pattern. | Hidden until focused, then shown at top-left with a solid background. |
| Skip link target without `tabindex="-1"` in older setups, focus does not move | Link scrolls but focus stays. | Target `<main id="main" tabindex="-1">` if focus does not move in testing. |
| Skip link text in marketing voice ("Jump to the good stuff") | Copy tell. | "Skip to main content". Filipino site: "Lumaktaw sa pangunahing nilalaman" if the site is in Filipino. |
| Skip link hidden with `display: none` | Never focusable. | Visually-hidden pattern that shows on `:focus`. See part 27. |

## 16.13 Search in navigation and command palette

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Search bar in the header on a 5-page site | No content to search. | No search until there is enough content. |
| Search icon that opens a full-screen overlay with animation | Template. | Inline expanding field, or a search page. |
| Placeholder "Search anything…" | Copy tell. See part 03. | "Search residents", "Search products". |
| ⌘K shortcut hint on a site used on Windows and phones | Mac-only hint. Irrelevant on touch. | Show "Ctrl K" on Windows, "⌘K" on Mac, nothing on touch. Only if the palette exists. |
| Command palette in a small CRUD app | Developer-tool trope. | Regular search and nav. Add a palette only for apps with many commands and power users. |
| Command palette as the only way to reach some pages | Hidden navigation. | Every palette command also reachable through visible UI. |
| Search that does not submit on Enter or has no submit button | Broken expectations. | `<form role="search">` with an input and a submit button. Enter submits. |
| Search results in a dropdown only, no results page | Cannot share or go back. | Results page with the query in the URL (`/search?q=`). Dropdown suggestions optional. |
| Search field in nav with `type="text"` | No clear button, no search keyboard. | `type="search"`, `enterkeyhint="search"`. Inputs: see part 17. |

## 16.14 User menu

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Avatar dropdown with name, email, role, plan badge, 10 links, theme switch | Overloaded. | Name (and role if useful), Profile, Settings, Sign out. |
| Sign out hidden 3 levels deep | Hard to find. Shared computers in LGU offices and school labs. | "Sign out" as the last item in the user menu, always visible. |
| Sign out with a "Leaving so soon?" confirm | See part 03 and 04. | Sign out immediately. Confirm only if unsaved changes exist. |
| Avatar from pravatar/unsplash placeholder | Placeholder left in. See part 26. | User's uploaded photo or initials on a neutral token background. |
| Avatar with online status dot for a single-user admin | Presence indicator without presence. | Remove the dot. Show presence only when it is real. See part 04. |
| User menu trigger is only an avatar with no accessible name | Screen readers say "button". | `aria-label="Account menu for Maria Santos"` or visible name beside avatar. |
| Menu uses `role="menu"` but items are plain links without arrow key support | Half-implemented pattern. | Either full menu pattern with arrow keys, or a disclosure with a list of links. |

## 16.15 Notification bell

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Bell icon in the header with no notification system behind it | Decoration. | No bell until notifications exist. |
| Red badge with a hardcoded number ("3") | Fake data. | Count from data. Hidden at 0. |
| Badge pulses or bounces | See part 25. | Static badge. |
| Badge shows "99+" on a new account | Mock data left in. | Real count. |
| Notification dropdown with emoji and "You've been mentioned! 🔔" text | Copy tell. See part 04. | "Juan replied to your post." with a timestamp. |
| No "Mark all as read" and no link to a full list | Dropdown only. | "Mark all as read" and "View all" linking to a notifications page. |
| Bell and inbox and activity icons all in the header | Three overlapping systems. | One notifications entry. |
| Bell count not announced to screen readers | Icon only. | `aria-label="Notifications, 4 unread"`. |

## 16.16 Footer

Original 3.8 items are included.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| 4-column mega footer on 5-page site (original 3.8) | Template footer. Columns filled with placeholder links. | 1-line footer: copyright, 2–4 links (Privacy, Terms, Contact). |
| 20+ links (original 3.8) | Link dump. | Max 8–10 links. |
| Social icons for nonexistent accounts (original 3.8) | `href="#"` or template accounts. | Only active accounts with real URLs. None if none exist. |
| Newsletter signup in footer (original 3.8) | Template block. | Skip, unless the client sends a newsletter. |
| "Made with ❤️ by" (original 3.8) | Template sign-off. | "© 2026 {Name}". Use the current year from the server, not hardcoded. |
| Tech stack line: "Built with Next.js, Tailwind and ❤️" (original 3.8) | Developer vanity. | Remove. |
| Back to top button (original 3.8) | Floating button on short pages. | Remove unless the page is 5000px+ tall. |
| Dark footer on light site (original 3.8) | Template contrast block. | Same color scheme as the site. Separate with a 1px border token. |
| Footer repeating the whole header nav | Duplicate. | Secondary links only (legal, contact, sitemap). |
| App store badges for apps that do not exist | Placeholder. | Remove. |
| Footer tagline ("Empowering communities since 2024") | Hype copy. See part 01. | Remove, or one factual line (office address). |
| "All rights reserved." plus 3 legal lines on a small site | Boilerplate. | "© 2026 {Name}". Legal pages linked. |
| Footer language, currency, theme selectors on a single-language PH site | Template controls. | Only controls the site uses. |
| Footer 300px tall with big padding | Oversized. See part 14. | 24–32px padding. |
| Footer in a logged-in app shell | Marketing footer in a tool. | No footer in app shells. |

## 16.17 Government, LGU and school site navigation

Page content for these sites is in part 24. PH wording rules are in part 09.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Nav with marketing labels on an LGU site ("Explore", "Our Story", "Get Involved") | SaaS template applied to government. | Labels that match what residents look for: "Services", "Announcements", "Officials", "Transparency", "Contact". |
| Services hidden under a "Resources" dropdown | Main task buried. | "Services" as a top-level link. Top services (barangay clearance, certificate of residency, business permit, cedula) linked from the homepage. |
| Mega menu with every ordinance and office on a barangay site | Too much structure. | Simple nav. Ordinances on one searchable list page. |
| Invented "GOVPH"-style top bar or seal on a site that is not an official government site | Imitates government branding. | Only official client sites use government marks, with assets supplied by the client. |
| Official client site that restyles or drops the standard government header/footer the agency uses | Breaks the client's required template. | If the client follows the Government Web Template or the national gov.ph standard, keep its top bar and footer as issued. Do not redesign them. |
| Language switch hidden in the footer | Users who need Filipino cannot find it. | Language switch (English / Filipino) in the header, labelled with the language name in that language. |
| School site nav with 10 items including "Vision/Mission", "Hymn", "History", "Org chart" at top level | Every page promoted. | Top level: Admissions, Academics, Announcements, About, Contact. Hymn, history and org chart under About. |
| Election/precinct finder link buried in a dropdown during election season | Main task hidden. | Direct top-level link or homepage search field during the period. |
| Footer without the office address, hotline and office hours | Missing the most-used info. | Footer: office address, phone (+63 format, see part 09), email, office hours. |
| Social icons linking to the mayor's personal page instead of the office page | Wrong account. | Link only to the official office page the client provides. |

## 16.18 Tailwind and Bootstrap specifics

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `fixed top-0 w-full z-50 bg-white/70 backdrop-blur-md border-b border-white/20` | Frosted nav string. | `sticky top-0 z-[var(--z-sticky)] bg-[var(--color-surface)] border-b border-[var(--color-border)]`, or theme colors mapped to tokens. |
| `after:w-0 hover:after:w-full after:transition-all` underline on every nav link | Animated underline trope. | `hover:underline` or color change. |
| `lg:hidden` hamburger missing, so hamburger shows at all widths | Hamburger on desktop. | Hamburger `lg:hidden`, links `hidden lg:flex`. |
| shadcn `NavigationMenu` with viewport animation for 4 links | Heavy component for a link list. | Plain `<nav><ul>` with links. |
| Sidebar from a shadcn block kept with demo items (Playground, Models, Documentation, Acme Inc) | Template leftovers. | Replace with the app's modules. Remove demo team switcher and sample projects. |
| Bootstrap `navbar-dark bg-dark` on a light site | Dark bar by default. | Navbar colors from Sass tokens matching the site. |
| Bootstrap `fixed-top` with `body { padding-top: 70px }` magic number | Height mismatch at other widths. | `sticky-top`, no padding hack. |
| Bootstrap `navbar-expand` (always expanded) | Overflows on phones. See part 15. | `navbar-expand-lg`. |
| Bootstrap `dropdown` with `data-bs-toggle="dropdown"` on a nav link that also navigates | Link unreachable on touch. | Separate button trigger. |
| AdminLTE/CoreUI sidebar kept with demo sections (Widgets, UI Elements, Charts, Examples) | Admin template unchanged. | Remove all demo sections. |

## 16.19 Code: banned vs use

```html
<!-- Banned: frosted fixed header, div menu button, no aria-current, hover-only dropdown -->
<nav class="fixed top-0 w-full z-[9999] bg-white/70 backdrop-blur-xl">
  <div class="logo">Brand</div>
  <div class="links">
    <a href="#" class="active">Home</a>
    <div class="dropdown" onmouseenter="open()">Solutions ▾</div>
  </div>
  <div class="hamburger" onclick="toggle()">☰</div>
</nav>
```

```html
<!-- Use: skip link, solid sticky header, button trigger, aria-current -->
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="container header-row">
    <a class="logo" href="/"><img src="/logo.svg" alt="Barangay San Isidro" width="120" height="32"></a>
    <nav aria-label="Main">
      <ul class="nav-links">
        <li><a href="/" aria-current="page">Home</a></li>
        <li><a href="/services">Services</a></li>
        <li><a href="/announcements">Announcements</a></li>
        <li><a href="/officials">Officials</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
    <button class="menu-btn" aria-expanded="false" aria-controls="mobile-menu">Menu</button>
  </div>
</header>
<main id="main" tabindex="-1">…</main>
```

```css
/* Use: tokens only */
.site-header { position: sticky; top: 0; z-index: var(--z-sticky); background: var(--color-surface); border-bottom: 1px solid var(--color-border); }
.header-row { display: flex; align-items: center; justify-content: space-between; min-height: 3.5rem; gap: var(--space-4); }
.nav-links { display: none; gap: var(--space-6); list-style: none; margin: 0; padding: 0; }
.nav-links a { color: var(--color-text); text-decoration: none; padding-block: var(--space-2); }
.nav-links a:hover { text-decoration: underline; }
.nav-links a[aria-current="page"] { font-weight: 600; box-shadow: inset 0 -2px 0 var(--color-primary); }
.menu-btn { min-height: 44px; }
@media (min-width: 64rem) { .nav-links { display: flex; } .menu-btn { display: none; } }

.skip-link { position: absolute; left: var(--space-2); top: -100px; background: var(--color-surface); padding: var(--space-2) var(--space-3); z-index: var(--z-toast); }
.skip-link:focus { top: var(--space-2); }

.site-footer { border-top: 1px solid var(--color-border); padding-block: var(--space-6); font-size: var(--text-sm); }
```

```html
<!-- Banned footer -->
<footer class="bg-gray-900 text-white py-24">
  <!-- 4 columns, 24 links, newsletter, 6 social icons with href="#" -->
  <p>Made with ❤️ using Next.js and Tailwind</p>
  <button class="back-to-top">↑</button>
</footer>

<!-- Use -->
<footer class="site-footer">
  <div class="container">
    <p>© 2026 Barangay San Isidro · Purok 3, San Isidro, Tarlac City · (045) 123 4567 · Mon–Fri 8:00–17:00</p>
    <ul class="footer-links"><li><a href="/privacy">Privacy</a></li><li><a href="/contact">Contact</a></li></ul>
  </div>
</footer>
```

## 16.20 Check

- [ ] Header is solid, not blurred or transparent over images.
- [ ] Header 56–64px desktop, 48–56px mobile.
- [ ] Header does not hide or change style on scroll.
- [ ] Logo links home. General-audience sites also have a "Home" link.
- [ ] 4–6 top-level nav items. Labels are nouns for page contents, sentence case.
- [ ] No hamburger at desktop widths.
- [ ] No animated underline on every nav link.
- [ ] Active state differs from hover and is persistent.
- [ ] `aria-current="page"` on the active link in every nav pattern.
- [ ] Focus outlines visible on all nav controls.
- [ ] Menu buttons are `<button>` with `aria-expanded` and `aria-controls`.
- [ ] Menus open on click, not hover only. Esc closes and focus returns.
- [ ] Menu transitions instant or 150ms max.
- [ ] No mega menu under 20 destinations.
- [ ] No `role="menu"` for site navigation links.
- [ ] Sidebar keeps labels. No icon-only collapse mode.
- [ ] Sidebar max 2 levels. 220–260px wide.
- [ ] No avatar/name/role block at the sidebar top.
- [ ] No colored dividers or rainbow icons in the sidebar.
- [ ] Badges show only real counts and hide at 0.
- [ ] No version or "Made with ❤️" in the sidebar.
- [ ] Sidebar items match the app's real modules. No template demo items.
- [ ] Breadcrumbs only at 3+ levels. Last item is not a link.
- [ ] Tabs only for in-page panels. Tab state in the URL.
- [ ] No sliding pill tab indicators.
- [ ] Mobile tab bar 4–5 items with text labels.
- [ ] Pagination hidden when there is one page. Page number in the URL.
- [ ] No pagination for under 20 items.
- [ ] Back links go to the parent route, not `history.back()`.
- [ ] Skip link present, visible on focus, targets `<main>`.
- [ ] Search only when there is content to search. `role="search"` form with submit.
- [ ] No command palette unless the app has many commands. Nothing reachable only through it.
- [ ] User menu: Profile, Settings, Sign out. Sign out without a confirm.
- [ ] No bell without a working notification system. Counts from data.
- [ ] Footer: one line on small sites, max 8–10 links.
- [ ] No social icons for accounts that do not exist.
- [ ] No "Made with ❤️", no tech stack line, no newsletter unless real.
- [ ] Back-to-top only on pages 5000px+.
- [ ] Footer uses the site's color scheme.
- [ ] Copyright year from the server.
- [ ] LGU/school nav uses resident-facing labels. Services top level.
- [ ] Official government templates kept as issued. No invented government marks.
- [ ] Language switch in the header on bilingual sites.
