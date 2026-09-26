# Style: High-contrast dark dashboard

Variant of [SKILL.md](./SKILL.md). Use only when this direction is chosen: the brief or `DESIGN.md` asks for a dark dashboard, ops console, monitoring screen, POS back office used in low light, or "high contrast dark". It is one option, not a kit default. If `DESIGN.md` says no pure white, no neon or no saturated colours, `DESIGN.md` wins and this file does not apply.

## The problem it solves
The common generated dark UI puts mid-grey text (slate-400 class of values) on navy cards. It passes AA on paper in some pairs, but reads as washed out on real screens, at small sizes, and under glare. This style pushes text luminance up and gives status colour a luminous foreground so state reads at a glance.

## Dials
`DESIGN_VARIANCE 3`, `MOTION_INTENSITY 2`, `VISUAL_DENSITY 7-8` unless the design read says otherwise.

## Colour recipe
All hex values here are labelled examples; put the real values in `DESIGN.md` as tokens.
- **Surfaces**: a deep, slightly tinted base and 2-3 surface steps above it (example: base `#070B14`, card `#0B132B`, raised `#111C3A`). Elevation comes from the surface step plus a 1px border at 8-12% white, not from shadows.
- **Primary text**: pure white (example `#FFFFFF`). Secondary and table body text: high-luminance neutrals (examples `#F1F5F9`, `#E2E8F0`). Aim for 10:1 or better on the card surface for body text; muted text still 7:1 or better.
- **Status badges**: luminous foreground on a translucent tint of the same hue, with a matching border.
  Example: success text `#34D399` on `rgba(16,185,129,0.15)` with border `rgba(52,211,153,0.4)`; warning `#FBBF24` family; danger `#F87171` family; info `#60A5FA` family. Weight 600-700.
- **Accent**: one brand accent for the primary action and focus ring. Status colours are not brand accents.
- Colour always encodes state (ok, warning, error, info, selected). Never decorate with a status hue. State never by colour alone: pair it with a word or icon.
- Light mode, if the project ships both: primary text near-black to black (example `#020617` or `#000000`), the same badge logic with darker foregrounds on pale tints, checked for AA separately.

## Components
Shared classes live in one place. In Tailwind projects put them in `@layer components` in the CSS entry file (`css-architecture`); in plain CSS or Blade projects, one component partial per block in the components layer (`css-architecture/plain-css.md`).

```css
/* Tailwind v4 project; token names come from DESIGN.md. Hex shown only as example values of those tokens. */
@layer components {
  .ui-card {
    background-color: var(--color-surface);        /* example #0B132B */
    border: 1px solid var(--color-border-subtle);  /* example rgba(255,255,255,0.12) */
    color: var(--color-on-surface);                /* example #FFFFFF */
  }
  .status-badge--success {
    background-color: var(--color-success-tint);   /* example rgba(16,185,129,0.15) */
    border: 1px solid var(--color-success-border); /* example rgba(52,211,153,0.4) */
    color: var(--color-success-fg);                /* example #34D399 */
    font-weight: 700;
  }
}
```

- Tables: numeric columns right-aligned with `tabular-nums`; zebra rows by a 2-4% surface step, not by colour.
- Charts: a small categorical palette tuned for dark backgrounds; gridlines at 6-10% white; see the `dataviz` skill if present.
- Focus ring: 2px in the accent, 2px offset, visible on every surface step.
- A soft glow (`box-shadow` in the status hue at low alpha) is fine on a live or selected item. On every card it stops meaning anything.

## Check before delivering
- Computed contrast for body, muted text and every badge pair on each surface step (`browser-verification` computed styles, or `css_audit.py` for declared pairs).
- Badges over images or translucent layers: check the real rendered pair, not the declared one.
- Read the screen in grayscale: state must still be clear from words and icons.
