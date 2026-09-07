---
name: design-spec
description: Owns the DESIGN.md format - the project-root file that holds machine-readable design tokens (YAML front matter for colors, typography, spacing, rounded, shadow, motion, breakpoints, components, color scheme) plus human-readable rationale. Use when creating or updating a project's DESIGN.md, when a UI task needs a design source of truth before code is written, or when extracting tokens from an existing site. This core holds the structure, the read fields, the token categories, and the authoring procedure; tokens-reference.md holds the full schema and template. Pairs with frontend-design (web) and mobile-design (mobile), which consume the file.
version: 2.1.0
---

# DESIGN.md Specification

`DESIGN.md` at the project root is the single source of truth for a project's visual language: machine-readable **tokens** (YAML front matter, normative) plus human-readable **rationale** (markdown body, context). Prose may use descriptive names ("Midnight Forest Green") that map to token names (`primary`).

This skill owns the format only. Whether and when the file is required is the global `design-rules` rule's call: before a new app or a new page-level UI; inferred and offered for components in an existing project; skipped for bug fixes and trivial tweaks. Format adapted from the [DESIGN.md spec](https://github.com/google-labs-code/design.md) (Google Labs, Apache-2.0).

| File | Read when |
|---|---|
| [tokens-reference.md](./tokens-reference.md) | Writing or extending the token block: full schema, value types, component properties, dark values, section table, consumer mapping, complete template |
| [collection.md](./collection.md) | Picking references: 85+ shipped products in 12 sections **by audience and domain** (civic, money, retail/POS, marketplace, health, education, logistics, booking, work tools, media, consumer, developer last), each with the one thing worth borrowing |
| [fetchable.md](./fetchable.md) | Fetching a published DESIGN.md to study its token structure: the slug list and URL shape. Only when a browsing tool is available |

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

Front matter starts and ends with a line containing exactly `---`. Body sections use `##` headings in the order above; any may be omitted; extra sections (`## Motion`, `## Iconography`, `## Imagery`) are allowed and preserved by consumers. Two sections with the same heading make the file invalid. Aliases and what each section holds: `tokens-reference.md` §2.

## 2. The five read fields

State these before any token; they gate every visual decision downstream.

| Field | Where | Value |
|---|---|---|
| Design read | `## Overview`, first line | one line (`frontend-design` §0 or `mobile-design`) |
| `DESIGN_VARIANCE` | `## Overview`, `Dials:` line | 1-10 (`frontend-design` §1) |
| `MOTION_INTENSITY` | same line | 1-10 |
| `VISUAL_DENSITY` | same line | 1-10 |
| `colorScheme` | front matter | `light` / `dark` / `both` (default `both`); kit extension, ignored by the linter |

## 3. Token categories (one example each)

```yaml
colors:      { primary: "#1A1C1E", on-primary: "#FFFFFF", surface: "#FBFAF7", surface-dark: "#131316" }   # roles; -dark twin when the value changes
typography:  { body-md: { fontFamily: Public Sans, fontSize: 16px, fontWeight: 400, lineHeight: 1.6 } }    # headline / body / label x size
spacing:     { md: 16px }
rounded:     { md: 8px }
shadow:      { modal: "0 8px 24px rgb(26 28 30 / 0.12)" }   # full CSS box-shadow, or none
motion:      { duration: { base: 250ms }, easing: { standard: cubic-bezier(0.2, 0, 0, 1) } }
breakpoints: { md: 768px }
components:  { button-primary: { backgroundColor: "{colors.primary}", textColor: "{colors.on-primary}", rounded: "{rounded.md}", padding: 12px } }
```

Scales are named levels (`xs sm md lg xl full`; any descriptive key is valid). `{path.to.token}` references a primitive token. Exact value types, component properties, dark-value rules, and recommended token names: `tokens-reference.md` §1. Consumers (`frontend-design` → Tailwind `@theme`; `mobile-design` → RN / Flutter theme objects): `tokens-reference.md` §3.

## 4. Authoring procedure

1. Read the brief; write the design read and the three dials (`frontend-design` §0-§1 or `mobile-design`); choose `colorScheme`.
2. Read [collection.md](./collection.md); go to the section for this project's **audience and domain**, not the one whose aesthetic you know best, and pick the 1-2 closest references there. A developer-product reference belongs only on a developer product. If one of them carries a `(slug)` and a browsing tool is available, fetch it via [fetchable.md](./fetchable.md) and study how it structures tokens and rationale. Adapt, never copy.
3. Copy the template from `tokens-reference.md` §4 and delete what the project does not use. Write `DESIGN.md` at the project root: tokens first, then rationale.
4. Lint when the `@google/design.md` CLI is available (npm, via `npx`); otherwise check the file by hand against §1-§3 and the reference:
   ```bash
   npx @google/design.md lint DESIGN.md                                       # structure, references, WCAG contrast of component pairs
   npx @google/design.md export --format css-tailwind DESIGN.md > theme.css   # Tailwind v4 @theme block
   npx @google/design.md export --format dtcg DESIGN.md > tokens.json         # W3C design-tokens JSON
   npx @google/design.md diff DESIGN.md DESIGN-v2.md                          # token-level regression check
   ```
5. Build UI against the tokens only. Descriptive names in prose must map to token names.
6. Update `DESIGN.md` whenever the visual language changes; the file stays the source of truth.

## 5. Done

- [ ] Front matter opens and closes with `---`; every `##` heading is unique and in canonical order.
- [ ] Design read, the three dials, and `colorScheme` are stated; `colors.primary` exists.
- [ ] `colorScheme: both`: every color whose value changes has a `-dark` twin.
- [ ] Every `{...}` reference resolves to an existing token.
- [ ] Lint passes when the CLI is available; the file sits at the project root.
- [ ] Every descriptive name in the prose maps to a token name.
