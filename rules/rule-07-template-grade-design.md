---
name: rule-07-template-grade-design
version: 3.1.0
priority: P0
trigger: glob
globs: "**/*.html, **/*.css, **/*.scss, **/*.tsx, **/*.jsx, **/*.vue, **/*.svelte, **/*.astro, **/*.blade.php, **/*.dart, **/components/**, **/resources/views/**, **/app/**/page.*, **/pages/**"
description: Rule 07 - every page, dashboard and app screen looks like a complete, premium, ready-made template (ThemeForest / Tailwind UI / CoreUI / Metronic level), not a minimal bare page. Works with Rule 01 tokens.
---

# RULE 07 — TEMPLATE-GRADE DESIGN

## Default look

Every UI you build should look like a **premium ready-made template** someone would buy: complete, polished, rich, and ready to ship. Not minimal, not a wireframe, not a plain white page with text.

- Minimal / editorial style only when the user explicitly asks for minimal.
- An existing project's approved design system wins; match its level of polish and fill gaps at template grade.
- All colors, spacing, radius, shadows and motion come from Rule 01 tokens and work in Light and Dark.

## What "template-grade" means

Every screen has:
- **Complete chrome:** header/navbar with logo, navigation, search or actions, user/profile menu; footer on public pages; sidebar with grouped sections, icons and active state on apps.
- **Visual depth:** layered surfaces, cards with soft shadows or borders, accent colors, gradient or pattern accents used with purpose, consistent icon set (Lucide, Tabler, Bootstrap Icons, Heroicons).
- **Real-looking content:** realistic demo data (Philippine context: ₱ amounts, local names, branches, dates), never "Lorem ipsum" or "Item 1, Item 2". Demo data lives in one clearly named file (`demo-data.*`) so it is easy to replace.
- **Imagery:** hero images, illustrations, avatars, product images or tasteful placeholders (gradient blocks with icons, `picsum`/`ui-avatars`-style placeholders) instead of empty boxes.
- **Interaction polish:** hover, focus, active and pressed states on every control; smooth transitions (150–300 ms); skeleton loaders; toasts; animated counters or charts where fitting; respects `prefers-reduced-motion`.
- **All states designed:** loading skeleton, empty state with illustration/icon and next action, error with recovery, success feedback.

## Page recipes (minimum sections)

**Landing / marketing page:** sticky navbar → hero (headline, subtext, 2 CTAs, visual) → logos/trust strip → features grid with icons → feature detail rows (image + text alternating) → stats/metrics band → testimonials → pricing (3 tiers, highlighted plan) → FAQ accordion → final CTA band → full footer (columns, socials, newsletter, legal).

**Admin dashboard:** collapsible sidebar with grouped nav + badges → top bar (search, notifications, theme toggle, profile) → page header with breadcrumb and primary action → 4 KPI cards (icon, value, trend %, sparkline) → main chart + side chart/list → recent activity / table with avatars, status badges, actions menu, pagination → quick actions or alerts panel.

**Data table page:** toolbar (search, filters, date range, export, add button) → table with sticky header, row selection, status badges, row actions, pagination, row count → empty and loading rows → detail drawer or modal.

**Form page:** sectioned card layout with titles and helper text → two-column grid on desktop → proper inputs (selects styled, date pickers, file upload with preview, toggles) → inline validation → sticky action bar (Cancel / Save).

**Auth pages:** split layout (brand visual or illustration on one side, form card on the other) → social/SSO buttons when relevant → remember me, forgot password, sign-up link.

**Mobile app screens:** app bar with title/actions → cards and lists with icons/avatars → bottom tab bar or FAB → pull-to-refresh, skeletons, empty states with illustration.

## Component library expectations

Build or reuse a consistent set: buttons (primary, secondary, ghost, danger, icon, loading), badges, avatars, cards (stat, profile, product), tabs, dropdown menus, modals, drawers, toasts, tooltips, breadcrumbs, pagination, steppers, progress, charts (Chart.js / Recharts / ApexCharts), skeletons. Every component has hover, focus, disabled and dark-mode styling.

## Instead of shortcuts

- Instead of centered text and one button: build the full recipe for that page type.
- Instead of browser-default controls: style every control (`.form-select`, custom checkbox/switch, styled file input).
- Instead of empty boxes or "TODO": add an icon, illustration or styled placeholder with a caption.
- Instead of one flat color: use surface layers, accent color, borders and shadows from tokens.
- Instead of real company logos or certifications: use neutral demo brands.

Copy-ready blocks for every recipe: `KIT/skills/template-ui-blocks/SKILL.md`.

## Before you answer, check

- The screen could be shown to a client as a finished template without "it's still a draft" excuses.
- Every section in the matching recipe above exists (or the user asked to skip it).
- Light and Dark both look finished (Rule 01).
