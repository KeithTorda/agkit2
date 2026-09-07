# Redesign protocol and audit checklist (frontend-design §8)

Read when: the site or app already exists (preserve or overhaul). SKILL.md core comes first (§0 design read, §1 dials); §8.A-§8.F below is the protocol, the checklist after it is the concrete list of things to look for during the §8.B audit. Findings go into the audit notes and, where they are tokens, into `DESIGN.md`.

## 8. Redesign protocol

### 8.A Detect the mode first
- **Greenfield**: no existing site, or full overhaul approved. Dials from SKILL.md §1.
- **Redesign, preserve**: modernise without breaking the brand. Audit, extract tokens, evolve.
- **Redesign, overhaul**: new visual language over existing content and IA. Greenfield for visuals; content and IA preserved.
If ambiguous, ask once: *"Preserve the existing brand, or start visually from scratch?"*

### 8.B Audit before touching
Scan the codebase (framework, styling method, Tailwind version, component library) and document: brand tokens (colors, type, logo treatment, radii); information architecture (page tree, nav, conversion paths); content blocks (working vs filler); patterns to preserve (signature interactions, copy voice) and to retire (AI tells, broken layouts, dead links, generic stock, perf traps); the existing dial reading (starting point, not baseline); SEO baseline (ranking pages, meta, structured data, OG cards): SEO migration is the #1 redesign risk. Write the tokens into `DESIGN.md` (create it if missing) before the first CSS change. The checklist below is the concrete grep list.

### 8.C Preservation rules
Keep slugs, anchor IDs, and primary nav labels stable. Extract brand colors before applying the color rules (marketing-layout.md §4.2): a brand that is already purple stays purple. Preserve copy voice unless a rewrite was asked for. Do not regress focus states, alt text, keyboard nav, or contrast. Keep button names, form field names and order, and section IDs that analytics depend on. Work with the existing stack: no framework or styling migrations, no new library without checking the dependency file, small reviewable changes, test after each.

### 8.D Fix order (stop when the brief is satisfied)
1. Typography (family, scale, tracking, line length): biggest lift per unit of risk.
2. Color (one accent, unified neutrals, tinted shadows, keep the brand hue).
3. Spacing and layout rhythm (container width, section padding, grid, mobile collapse).
4. States and interaction (hover, active, focus-visible, loading, empty, error, active nav item, no `#` links).
5. Motion layer at the dial level the read allows.
6. Hero and key-section recomposition.
7. Block replacement, only for blocks that are unsalvageable.

### 8.E Targeted evolution vs full redesign
IA, content, and SEO sound → targeted evolution (steps 1-5; ~70% of the value at ~40% of the risk). Structural visual debt (broken IA, no system, broken mobile) → full redesign with strict content preservation. Brand itself changing → greenfield.

### 8.F Never changed silently
URL structure and slugs, primary nav labels, form field names or order, logo or wordmark, legal / consent / cookie copy. Each needs explicit approval.

## Audit checklist (for §8.B)

### Stack facts to record first
- Framework and router; styling method (Tailwind version, CSS modules, styled-components, vanilla); component library and icon set already installed; animation library; font loading method.
- Existing tokens: colors actually used (count hex values), font families, radius values, spacing scale, shadow recipes, z-index values.
- Current color scheme: light, dark, or both, and how it is switched.

### Grep targets (concrete)
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

### Content and copy findings
- Placeholder names, brands, and avatars (same photo reused for different people).
- Lorem ipsum, "Oops!"-style errors, exclamation-mark success messages, passive voice, Title Case On Every Heading.
- Identical blog dates, round fake metrics, invented precision.
- Stock "diverse team" photos and generic hero blobs.
- Copy voice: note what is distinctive and worth preserving before changing anything.

### Structure and layout findings
- Missing container max-width; content stretching edge to edge on wide screens.
- Card groups with buttons at random heights (pin CTAs to the card bottom); pricing or comparison columns whose feature lists start at different Y positions.
- Optical alignment errors: icons next to text, play buttons in circles, text in buttons that need 1-2px nudges.
- Orphaned single words on the last line of headlines (`text-wrap: balance` / `pretty`).
- Only weights 400 and 700 in use; no 500/600 for mid-level hierarchy.
- Proportional figures in data tables (`tabular-nums` missing).
- No active-page indicator in navigation; no "back" path on inner pages.
- Anchor jumps without `scroll-behavior: smooth`.

### Strategic omissions (usually missing)
- Privacy policy and terms links in the footer.
- Custom 404 page.
- Skip-to-content link; visible focus styles; keyboard-operable menus and modals.
- Client-side form validation with inline errors; server-side validation mirrored.
- `<title>`, meta description, `og:image` and social cards per page; favicon and touch icons.
- Cookie consent where the jurisdiction requires it.
- Loading, empty, and error states for every data-bound view.

### Before proposing changes
- List the SEO-bearing surfaces (ranking URLs, meta, structured data) and mark them "do not change silently" (§8.F).
- List analytics-bound identifiers (button names, form field names, section IDs).
- Read the existing site's three dials (SKILL.md §1) and record them as the starting point.
