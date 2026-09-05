# Redesign audit checklist

The redesign protocol (mode detection, audit, preservation, fix order) is [SKILL.md §8](./SKILL.md). This file is only the concrete list of things to look for in an existing codebase during the §8.B audit. Findings go into the audit notes and, where they are tokens, into `DESIGN.md`. It adds no rules; the rules stay in SKILL.md.

## Stack facts to record first
- Framework and router; styling method (Tailwind version, CSS modules, styled-components, vanilla); component library and icon set already installed; animation library; font loading method.
- Existing tokens: colors actually used (count hex values), font families, radius values, spacing scale, shadow recipes, z-index values.
- Current color scheme: light, dark, or both, and how it is switched.

## Grep targets (concrete)
- `h-screen` / `100vh` on full-height sections.
- `addEventListener("scroll"`, `window.scrollY` in state, `setInterval` animations.
- `href="#"` dead links; buttons without a destination or handler.
- `outline: none` / `outline-none` without a replacement focus style.
- `alt=""` on meaningful images, `alt="image"`, images without `alt`.
- `placeholder=` used as the only label; inputs without `<label>` / `aria-label`.
- Inline `style=` blocks mixed with the styling system; hardcoded pixel widths on layout containers.
- `z-index: 9999`-style arbitrary values.
- `console.log`, commented-out blocks, TODOs, unused imports.
- Imports not present in `package.json`.
- Duplicate `id` attributes; duplicate section headings.
- Em-dash / en-dash characters in copy.

## Content and copy findings
- Placeholder names, brands, and avatars (same photo reused for different people).
- Lorem ipsum, "Oops!"-style errors, exclamation-mark success messages, passive voice, Title Case On Every Heading.
- Identical blog dates, round fake metrics, invented precision.
- Stock "diverse team" photos and generic hero blobs.
- Copy voice: note what is distinctive and worth preserving before changing anything.

## Structure and layout findings
- Missing container max-width; content stretching edge to edge on wide screens.
- Card groups with buttons at random heights (pin CTAs to the card bottom); pricing or comparison columns whose feature lists start at different Y positions.
- Optical alignment errors: icons next to text, play buttons in circles, text in buttons that need 1-2px nudges.
- Orphaned single words on the last line of headlines (`text-wrap: balance` / `pretty`).
- Only weights 400 and 700 in use; no 500/600 for mid-level hierarchy.
- Proportional figures in data tables (`tabular-nums` missing).
- No active-page indicator in navigation; no "back" path on inner pages.
- Anchor jumps without `scroll-behavior: smooth`.

## Strategic omissions (usually missing)
- Privacy policy and terms links in the footer.
- Custom 404 page.
- Skip-to-content link; visible focus styles; keyboard-operable menus and modals.
- Client-side form validation with inline errors; server-side validation mirrored.
- `<title>`, meta description, `og:image` and social cards per page; favicon and touch icons.
- Cookie consent where the jurisdiction requires it.
- Loading, empty, and error states for every data-bound view.

## Before proposing changes
- List the SEO-bearing surfaces (ranking URLs, meta, structured data) and mark them "do not change silently" (SKILL.md §8.F).
- List analytics-bound identifiers (button names, form field names, section IDs).
- Read the existing site's three dials (SKILL.md §1) and record them as the starting point.
