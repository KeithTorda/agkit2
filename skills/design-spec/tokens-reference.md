# Tokens reference

Read when creating or extending a `DESIGN.md`; [SKILL.md](./SKILL.md) defines intake and scope. Keep existing token consumers compatible and avoid a second source of truth.

## 1. Token schema

```yaml
name: Example project
description: Optional short description
colorScheme: light
colors:
  primary: "#194B3A"
  on-primary: "#FFFFFF"
  surface: "#FBFAF7"
  on-surface: "#1A1C1E"
typography:
  body-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
rounded: { md: 8px }
spacing: { md: 16px }
shadow: { modal: "0 8px 24px rgb(26 28 30 / 0.12)" }
motion:
  duration: { fast: 140ms, base: 180ms }
  easing: { standard: "cubic-bezier(0.2, 0, 0, 1)" }
breakpoints: { md: 768px }
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 12px
```

These are examples of supported roles, not required quantities or values. Use `light`, `dark`, or `both` to describe requested/existing scope; no automatic second theme.

### Value conventions
- Color: quoted sRGB hex, for example `"#194B3A"`. Preserve an existing wider-color/alpha pipeline when needed; external CLI support may be narrower than project CSS.
- Dimension: number with unit such as `16px`, `1rem`, or `0.02em`; numeric zero is useful where supported. Durations use `ms` or `s`.
- Typography: `fontFamily`, `fontSize`, numeric `fontWeight`, and optional `lineHeight`, `letterSpacing`, `fontFeature`, `fontVariation`. Use a unitless line height where appropriate.
- Shadow: a complete CSS box-shadow string or `none`.
- Easing: quote CSS functions, especially inside flow mappings; unquoted commas can change YAML parsing.
- Reference: quote `"{path.to.token}"`. Resolve the full path; reject missing targets and cycles. Composite typography references belong where the consumer expects typography.
- Component properties may include `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, and `width`. Document additional properties in an existing consumer instead of assuming every external exporter supports them.
- States may use related entries such as `button-primary-hover` or the project's existing state schema. Provide actual focus/disabled/error roles when relevant.

### Theme counterparts
For a new spec using this kit's simple convention, changing colors in `both` may use `-dark` counterparts:

```yaml
colorScheme: both
colors:
  primary: "#194B3A"
  primary-dark: "#A8D5BE"
  on-primary: "#FFFFFF"
  on-primary-dark: "#12382B"
  surface: "#FBFAF7"
  surface-dark: "#131816"
  on-surface: "#1A1C1E"
  on-surface-dark: "#F1F5F2"
```

Map each counterpart to the same semantic role when switching themes. Keep unchanged colors shared. If a project already has theme modes, CSS variable overrides, or a different token structure, document that mapping rather than renaming everything to this example. Check both themes in the rendered UI. Light/dark color-blocked sections within one theme may use separate section roles instead.

### Naming
Choose names for meaning and reuse. Possible roles include `primary`, `on-primary`, `surface`, `on-surface`, `muted`, `border`, `focus`, `error`, and `success`. Typography may use `display`, `heading`, `body`, `label`, and `code` at the actual sizes needed. A project does not need 9-15 typography levels, multiple fonts, a shadow scale, or an unused dark palette.

## 2. Document sections

| Section | Contents |
|---|---|
| Overview | Approved direction, purpose, audience, useful references or delegation; optional existing dials |
| Colors | Semantic palette, theme scope, and intentional section contrast |
| Typography | Type roles, font sources, language coverage, hierarchy, reading measure |
| Layout | Containers, spacing relationships, grid, responsive reflow, information density |
| Elevation & Depth | Tonal layers, borders, shadows, transparency, and their roles |
| Shapes | Role-based radius/shape treatment |
| Components | Reusable controls and states beyond primitive tokens |
| Do's and Don'ts | Specific agreed choices to preserve, rather than generic style prohibitions |
| Motion / Imagery / Iconography | Useful additional detail when the design actually uses it |

Keep unique headings. If interoperating with an external DESIGN.md linter, use its supported section order and aliases as needed; do not discard existing useful content just to imitate an example. Minimal projects can use a short subset.

## 3. Consumers

Use the existing project pipeline:

- CSS: semantic custom properties in the project's token entrypoint; local section roles can inherit/override them.
- Tailwind: map colors, fonts, sizes, radius, spacing, shadows, easing, and breakpoints to the installed version's supported theme mechanism. In v4 these may be `@theme` variables such as `--color-*`, `--font-*`, `--text-*`, `--radius-*`, `--shadow-*`, `--ease-*`, and `--breakpoint-*`. Do not assume every composite maps to a single variable.
- Component systems: feed their supported theme/token API without creating a competing CSS reset.
- Native: `mobile-design` may map the same semantic decisions into React Native or Flutter theme objects.

Check actual consumer output. A linter or exporter may support fewer value/property types than project CSS; report the mismatch and preserve the approved implementation instead of claiming an unsupported export succeeded.

## 4. Concise complete example

```markdown
---
name: Clinic Scheduler
colorScheme: light
colors:
  primary: "#194B3A"
  on-primary: "#FFFFFF"
  surface: "#FBFAF7"
  on-surface: "#1A1C1E"
  border: "#D6DBD7"
  focus: "#194B3A"
  error: "#A82727"
typography:
  heading-md: { fontFamily: Public Sans, fontSize: 30px, fontWeight: 600, lineHeight: 1.2 }
  body-md: { fontFamily: Public Sans, fontSize: 16px, fontWeight: 400, lineHeight: 1.5 }
  label-md: { fontFamily: Public Sans, fontSize: 14px, fontWeight: 500, lineHeight: 1.4 }
rounded: { control: 6px, panel: 12px }
spacing: { sm: 8px, md: 16px, lg: 24px, xl: 40px }
motion:
  duration: { fast: 140ms, base: 180ms }
  easing: { standard: "cubic-bezier(0.2, 0, 0, 1)" }
components:
  button-primary: { backgroundColor: "{colors.primary}", textColor: "{colors.on-primary}", rounded: "{rounded.control}", padding: 12px }
  input: { backgroundColor: "{colors.surface}", textColor: "{colors.on-surface}", rounded: "{rounded.control}", height: 44px }
---

# Clinic Scheduler

## Overview
The user chose a calm service interface and asked to keep the clinic's green identity. Reference preference: no external reference; build on the existing product.

## Colors
Light mode only. Primary carries action and focus; error is reserved for actual errors. Verify contrast on rendered controls and feedback.

## Typography
Public Sans from the project's existing font pipeline. Clear title, body, and label roles; allow long patient names and translated labels.

## Layout
Lead with appointment selection. Group related fields, use the existing container, and reflow according to content width. Keep the next action reachable on mobile.

## Shapes
Control radius for inputs/buttons; panel radius for grouped appointment information.

## Components
Persistent labels, associated field errors, pending submission feedback, and preserved input after failed submission.

## Motion
Feedback only, with reduced-motion transitions disabled. No scroll reveals or ambient loops.

## Do's and Don'ts
- Keep the approved clinic identity and working booking flow.
- Use real assets and truthful availability; visibly identify any demo data.
- Verify responsive wrapping, focus, labels, and the affected interaction.
```

The example is a specific direction, not a universal recipe. Change the content and decisions to match the user's actual brief.
