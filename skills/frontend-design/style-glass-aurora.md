# Style: Glass, aurora, and glow

Use for approved translucent layers, aurora/mesh fields, atmospheric gradients, or glow. A request for "premium" or "futuristic" alone is not an automatic glass recipe: settle the user's actual direction through [SKILL.md](./SKILL.md).

## Visual intent
Glass reveals an underlying layer; the backdrop and panel tint must work together. A color field, image, video, or scrolling content can create that depth. Content-heavy surfaces may need stronger tint or solid fill for comfortable reading.

Plan a coherent relationship between atmospheric background, foreground surfaces, and focal emphasis. There is no fixed number of panels, glows, hues, or gradients; count and intensity follow hierarchy, clarity, and performance. Do not put the same glowing treatment on every item by reflex.

Motion is independent of this material style. A static glass design is valid. Follow the agreed motion intent; a static aurora is valid and richer movement needs a purpose and reduced-motion alternative.

## Example material recipe
Map every role to the actual `DESIGN.md`. Start from an opaque readable panel, then opt into translucency only where supported and visually verified:

```css
.glass-panel {
  color: var(--color-on-surface);
  background: var(--color-surface);
  border: 1px solid var(--color-glass-border);
  box-shadow: var(--shadow-glass);
}
@supports (backdrop-filter: blur(1px)) {
  .glass-panel {
    background: var(--color-glass-tint);
    backdrop-filter: blur(18px) saturate(140%);
    -webkit-backdrop-filter: blur(18px) saturate(140%);
  }
}
@media (prefers-reduced-transparency: reduce) {
  .glass-panel {
    background: var(--color-surface);
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
}
```

Support for the reduced-transparency query varies, so readable contrast cannot depend on that query alone. Use sufficient tint/scrim in the ordinary translucent state.

## Gradients and emphasis
Build aurora/mesh fields from the agreed palette, using a static CSS background where enough. If an animated field is approved, isolate it in a bounded decorative layer, avoid input interception, honor reduced motion, and measure its cost. Do not apply a fixed viewport blur to every section by default.

Gradient text needs a readable solid fallback and adequate contrast across the glyphs, not only the headline's average background. Keep body/control text legible. Gradient borders and glow may emphasize selected or featured content; they do not replace a visible keyboard focus ring.

Light and dark material treatments have different tint needs. A contrasting section can change the panel recipe; use local semantic tokens rather than assuming one transparency value works everywhere.

## Accessibility and performance
Inspect text against the worst actual backdrop area, including responsive crops and moving content. Normal text generally needs 4.5:1 contrast; qualifying large text 3:1. Raise tint, simplify the backdrop, or add a scrim to preserve the approved style.

Use real browser inspection for focus, text, scroll, reduced motion, and unsupported blur behavior. Limit large blurred areas and stacked backdrop effects according to observed device cost; a static illustration or gradient can achieve atmosphere more cheaply. Reserve media dimensions and provide controls for meaningful video/audio behavior.

## Review
The composition should still read clearly with blur absent and motion disabled. Check initial load, mobile crops, low-emphasis text, overlays, focus, and scroll performance. Correct the weak local layer instead of stripping the entire glass direction during a generic review.
