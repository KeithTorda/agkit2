---
name: design-spec
description: Owns the DESIGN.md format - the project-root file that holds machine-readable design tokens (YAML front matter for colors, typography, spacing, rounded, shadow, motion, breakpoints, components, color scheme) plus human-readable rationale. Use when creating or updating a project's DESIGN.md, when a UI task needs a design source of truth before code is written, or when extracting tokens from an existing site. Pairs with frontend-design (web) and mobile-design (mobile), which consume the file.
version: 2.0.0
---

# DESIGN.md Specification

This skill owns the `DESIGN.md` format. The `design-rules` global rule (when the file is required) and the `frontend-design` / `mobile-design` skills (which consume it) point here; this file is the authoritative schema. When you author or extract a `DESIGN.md`, follow the schema below.

`DESIGN.md` at the project root is the single source of truth for a project's visual language. Two layers: machine-readable **tokens** (YAML front matter, normative) and human-readable **rationale** (markdown body, context). Prose may use descriptive names ("Midnight Forest Green") that map to token names (`primary`).

Format adapted from the [DESIGN.md spec](https://github.com/google-labs-code/design.md) (Google Labs, Apache-2.0). Reference library: [collection.md](./collection.md) lists 70+ published DESIGN.md files (Stripe, Linear, Vercel, Airbnb, Apple, ...) by industry with a one-line vibe summary and a URL each. Read the list to find the 1-2 closest in vibe and industry; if a browsing or fetch tool is available in the session, fetch those files and study how they structure tokens and rationale. Adapt, never copy.

Whether and when a `DESIGN.md` is required is the global `design-rules` rule's call; this skill only defines the format.

---

## 1. File structure

```
---
<YAML token front matter>
---

# Project Name

## Overview
## Colors
## Typography
## Layout
## Elevation & Depth
## Shapes
## Components
## Do's and Don'ts
```

Front matter starts and ends with a line containing exactly `---`. Body sections use `##` headings in the order above; any may be omitted; extra sections (`## Motion`, `## Iconography`, `## Imagery`) are allowed and preserved by consumers. Two sections with the same heading make the file invalid.

## 2. Token schema (front matter)

```yaml
version: alpha              # optional
name: Daylight Prestige
description: ...            # optional
colorScheme: both           # kit extension: light | dark | both (default both); the linter ignores it
colors:
  <token-name>: "#RRGGBB"
typography:
  <token-name>:
    fontFamily: Public Sans
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
rounded:
  <scale>: 8px
spacing:
  <scale>: 16px             # Dimension or unitless number
shadow:
  <scale>: "0 1px 2px rgb(0 0 0 / 0.06)"   # full CSS box-shadow; use none for flat designs
motion:
  duration:
    <scale>: 200ms
  easing:
    <name>: cubic-bezier(0.16, 1, 0.3, 1)
breakpoints:
  <name>: 768px             # sm md lg xl, or any named level
components:
  <component-name>:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: 12px
```

`<scale>` is a named level (`xs sm md lg xl full`; any descriptive key is valid).

**Types.** Color: `#` + hex sRGB (`"#1A1C1E"`). Dimension: number + `px` / `em` / `rem` (or `ms` / `s` for durations). Shadow: a full CSS `box-shadow` string, or `none`. Token reference: `{path.to.token}` pointing at a primitive (`{colors.primary-60}`), or at a composite only inside `components` (`{typography.label-md}`). Typography: object with `fontFamily`, `fontSize`, `fontWeight` (number), `lineHeight` (unitless recommended), `letterSpacing`, optional `fontFeature`, `fontVariation`. Motion: `duration.<scale>` (Dimension) plus `easing.<name>` (a CSS timing function or `cubic-bezier(...)`). Breakpoint: Dimension in `px`.

**Component properties.** `backgroundColor`, `textColor` (Color); `typography` (Typography); `rounded`, `padding`, `size`, `height`, `width` (Dimension). States are separate entries with a related key: `button-primary`, `button-primary-hover`, `button-primary-disabled`.

**Dark values.** When `colorScheme: both`, give every color whose value changes a `-dark` counterpart (`surface` / `surface-dark`, `ink` / `ink-dark`). Colors without a counterpart are the same in both schemes. The linter reports `-dark` tokens as "orphaned" when no component references them; that warning is expected.

## 3. Sections (canonical order)

| # | Section | Aliases | Purpose |
|---|---|---|---|
| 1 | Overview | Brand & Style | Brand personality, audience, tone; the one-line design read and the three dials from `frontend-design` §0-§1. Fallback context when a token is missing. |
| 2 | Colors | | Palette rationale, at least `primary`; which color drives interaction; the color scheme (light / dark / both) in words. |
| 3 | Typography | | 9-15 levels as semantic roles (headline / body / label × size); pairing rationale if a serif is used. |
| 4 | Layout | Layout & Spacing | Grid model, spacing scale, container widths, breakpoints, density. |
| 5 | Elevation & Depth | Elevation | Shadow scale, or for flat designs the alternative (borders, tonal layers). |
| 6 | Shapes | | Radius scale and where each level applies. |
| 7 | Components | | Buttons, inputs, cards, chips, lists: per-atom guidance beyond the tokens. |
| 8 | Do's and Don'ts | | Guardrails during generation (anti-defaults the brand accepts or rejects, motion limits, imagery rules). |

Recommended token names (guidance, not required): colors `primary secondary tertiary neutral surface on-surface on-primary error`; typography `headline-display headline-lg headline-md body-lg body-md body-sm label-lg label-md label-sm`; rounded `none sm md lg xl full`; shadow `none sm md lg`; motion.duration `fast base slow`, motion.easing `standard emphasized`; breakpoints `sm md lg xl`. When motion tokens are defined, give them a `## Motion` section (duration/easing rationale, motion limits) after Components.

## 4. What consumers do with it

- `frontend-design` maps every token group cleanly onto Tailwind v4 `@theme`: `colors.*` → `--color-*`, `typography.*.fontFamily` → `--font-*`, `.fontSize` → `--text-*`, `rounded.*` → `--radius-*`, `spacing.*` → `--spacing-*`, `shadow.*` → `--shadow-*`, `motion.easing.*` → `--ease-*`, `breakpoints.*` → `--breakpoint-*` (durations feed the transition/animation utilities). `-dark` values apply under `.dark`; `colorScheme` decides which schemes ship. The `@theme` mechanics themselves live in `tailwind-patterns` §2.
- `mobile-design` reads the same tokens for React Native / Flutter theme objects.
- Unknown content: unknown section headings, token names, and component properties are accepted (properties with a warning); an invalid value is rejected; a duplicate section heading rejects the file.

## 5. Tooling

The `@google/design.md` CLI exists (npm, run via `npx`). Use it when available; otherwise write the file by hand from the template in §6 and check it against §1-§3.

```bash
npx @google/design.md lint DESIGN.md                                  # structure, references, WCAG contrast of component pairs
npx @google/design.md export --format css-tailwind DESIGN.md > theme.css   # Tailwind v4 @theme block
npx @google/design.md export --format dtcg DESIGN.md > tokens.json     # W3C design-tokens JSON
npx @google/design.md diff DESIGN.md DESIGN-v2.md                      # token-level regression check
```

## 6. Template (complete; copy, then delete what the project does not use)

```markdown
---
name: Calm Scheduler
colorScheme: both
colors:
  primary: "#1A1C1E"
  on-primary: "#FFFFFF"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
  surface: "#FBFAF7"
  surface-dark: "#131316"
  on-surface: "#1A1C1E"
  on-surface-dark: "#F4F3EF"
  error: "#B3261E"
typography:
  headline-lg: { fontFamily: Public Sans, fontSize: 48px, fontWeight: 600, lineHeight: 1.1, letterSpacing: -0.02em }
  headline-md: { fontFamily: Public Sans, fontSize: 32px, fontWeight: 600, lineHeight: 1.2 }
  body-md: { fontFamily: Public Sans, fontSize: 16px, fontWeight: 400, lineHeight: 1.6 }
  label-md: { fontFamily: Public Sans, fontSize: 13px, fontWeight: 500, lineHeight: 1.3, letterSpacing: 0.02em }
rounded: { sm: 4px, md: 8px, lg: 16px, full: 9999px }
spacing: { xs: 4px, sm: 8px, md: 16px, lg: 32px, xl: 64px }
shadow: { none: none, modal: "0 8px 24px rgb(26 28 30 / 0.12)" }
motion:
  duration: { fast: 150ms, base: 250ms }
  easing: { standard: cubic-bezier(0.2, 0, 0, 1) }
breakpoints: { sm: 640px, md: 768px, lg: 1024px }
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.sm}"
    height: 44px
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.lg}"
    padding: 24px
---

# Calm Scheduler

## Overview
Design read: healthcare scheduling for clinic staff; calm, trust-first, accessibility-first.
Dials: DESIGN_VARIANCE 4, MOTION_INTENSITY 3, VISUAL_DENSITY 5.

## Colors
Light and dark both ship. Tertiary (#B8422E) is the only interaction color. Surface and on-surface swap to their -dark values in dark mode.

## Typography
Public Sans throughout; no serif. Headlines 600, body 400, labels 500.

## Layout
12-column grid, 1200px container, spacing scale above; sections py-16.

## Elevation & Depth
Flat: 1px borders on surface, no drop shadows except the modal (0 8px 24px at 12% of primary).

## Shapes
sm for inputs, md for buttons, lg for cards, full only for chips.

## Components
Buttons: one primary per view. Inputs: label above, error text below in error color. Cards: no nested cards.

## Motion
Durations 150-250ms with standard easing; motion carries state and feedback only (dial 3), never decoration.

## Do's and Don'ts
- Do use tertiary only for the single most important action per screen.
- Do keep WCAG AA contrast (4.5:1 normal text) in both schemes.
- Don't mix rounded and sharp corners in one view.
- Don't add motion beyond dial 3.
```

## 7. Workflow

1. Read the brief and produce the design read and dials (`frontend-design` §0-§1 or `mobile-design`).
2. Read [collection.md](./collection.md); pick 1-2 references; fetch and study them if a fetch tool is available.
3. Write `DESIGN.md` at the project root: tokens first, then rationale. Run `lint` if the CLI is available.
4. Build UI against the tokens only. Descriptive names in prose must map to token names.
5. Update `DESIGN.md` whenever the visual language changes; the file stays the source of truth.
