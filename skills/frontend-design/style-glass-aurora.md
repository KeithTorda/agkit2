# Style: Glass, aurora and glow

Variant of [SKILL.md](./SKILL.md). Use when the brief or `DESIGN.md` asks for glassmorphism, frosted panels, aurora or mesh gradients, glow, "futuristic", "premium", visionOS-like, or when it is the chosen direction for a consumer product, launch, event, music or AI product. Done well, it looks expensive; done by reflex, it looks generated. The difference is contrast, restraint in count, and a real layer behind the glass.

## Dials
`DESIGN_VARIANCE 7`, `MOTION_INTENSITY 6`, `VISUAL_DENSITY 3` unless the design read says otherwise.

## Rules of the style
- **Something worth seeing behind the glass.** A photo, video, gradient field or content scrolling underneath. Glass over a flat colour is just a grey box.
- **Few layers.** One to three glass surfaces per view (nav, a hero card, a modal). Content-heavy areas (tables, long forms, articles) sit on solid surfaces.
- **One gradient field per view.** The aurora or mesh lives in the background layer and is built from 2-4 brand hues; foreground elements stay solid or glass.
- **Glow means emphasis.** One glowing element per view (the primary CTA, the live item, the selected card).

## Recipes
Hex and rgba values are labelled examples; map them to `DESIGN.md` tokens.

```css
/* Glass panel */
.glass-panel {
  background: rgb(255 255 255 / 0.08);                 /* example tint; darker tint on light backgrounds */
  border: 1px solid rgb(255 255 255 / 0.18);
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.25), 0 8px 32px rgb(0 0 0 / 0.25);
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
}
/* Fallbacks: no blur support, or the user asked for less transparency */
@supports not (backdrop-filter: blur(1px)) { .glass-panel { background: var(--color-surface); } }
@media (prefers-reduced-transparency: reduce) { .glass-panel { background: var(--color-surface); backdrop-filter: none; } }

/* Aurora background: fixed layer, not on scrolling content */
.aurora {
  position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background:
    radial-gradient(60% 50% at 20% 20%, var(--color-aurora-1) 0%, transparent 60%),  /* example #7C3AED at 45% */
    radial-gradient(50% 40% at 80% 30%, var(--color-aurora-2) 0%, transparent 60%),  /* example #06B6D4 at 35% */
    radial-gradient(60% 50% at 50% 90%, var(--color-aurora-3) 0%, transparent 60%),  /* example #F472B6 at 30% */
    var(--color-base);                                                                 /* example #0A0A12 */
  filter: blur(40px);
}
@media (prefers-reduced-motion: no-preference) {
  .aurora { animation: aurora-drift 30s ease-in-out infinite alternate; }
}
@keyframes aurora-drift { to { transform: translate3d(0, -4%, 0) scale(1.08); } }

/* Glow on the one element that earns it */
.cta-glow { box-shadow: 0 0 0 1px var(--color-accent), 0 0 32px -4px var(--color-accent); }
```

- Gradient text: fine on one display headline with a solid-colour fallback (`color` set before `background-clip: text`) and at display sizes only; body and UI text stay solid.
- Gradient borders: `border-image` or a masked pseudo-element; one highlighted card, not every card.

## Accessibility and performance (firm)
- Text on glass must meet 4.5:1 against the **worst** part of what is behind it. Raise the panel tint, add a scrim under text, or darken the background layer until it does. Check with the rendered page (`/see`, computed styles plus a screenshot), since the declared colours cannot tell you.
- Honour `prefers-reduced-motion` (aurora and glow stay still) and `prefers-reduced-transparency` (solid surfaces).
- `backdrop-filter` is expensive on low-end Android: keep it to a few fixed-size elements, never on long scrolling lists, and test the scroll on a throttled profile when the audience is mobile-first.
- Focus rings stay solid and visible; a glow is not a focus indicator.
