# Style: Swiss, brutalist, or telemetry

Use for an approved bold grid, Swiss-industrial, raw typography, terminal, or telemetry direction. These are related references, not one mandatory aesthetic. [SKILL.md](./SKILL.md) governs intake, truthful data, accessibility, and implementation.

## Choose the qualities that fit
Swiss print may contribute heavy type, strong rules, a visible grid, generous negative space, and sharp corners. Telemetry may contribute compact monospaced data, framed readouts, dark surfaces, and clear status. Neither forces a light-only/dark-only theme, hazard red, fake coordinates, CRT scanlines, or tiny text.

If combining qualities, define a coherent role system in `DESIGN.md`. Contrasting sections are allowed. A mobile or data-heavy interface needs readable controls even if a reference uses poster-scale type.

## Typography and layout
Use a display face with suitable weight and a readable body/data face. Mono is useful for real readouts; an extra serif is optional only when it has an explicit role, not a required third family. Check licensing and language support.

Oversized type can create impact, but preserve glyphs and meaning across breakpoints. Choose line height from the actual font rather than forcing 0.85 everywhere. Small metadata still needs readable size, contrast, and spacing.

A strong CSS grid, aligned rules, or compartmentalized rows can establish structure. Repeated layouts support scanning. Adapt dense regions and large type to narrow widths instead of forcing all content into absolute panels.

## Color and texture
Example print roles: warm paper `#F4F4F0`, ink `#111111`, signal red `#C52222`. Example telemetry roles: base `#0A0A0A`, foreground `#EAEAEA`, a chosen brand accent. Verify actual pairs; a bright accent is not automatically safe for small text.

Texture, halftone, scanlines, glow, and grain are optional expressive treatments. Keep them behind content, out of hit testing, and cheap to render. Do not apply CRT decoration to every technical product. Shadows, gradients, or translucency are available if the agreed direction uses them coherently.

## Data and motion
Show genuine IDs, revisions, readings, and state. Demo telemetry must be visibly identified when it could look live. Do not fabricate precision to fill the visual system.

Use feedback-only or richer movement according to the agreed intent, with a purpose and reduced-motion behavior. Use semantic tables, lists, `data`, `output`, or `samp` when they match the information.

## Review
Check keyboard access, focus, small text, long values, responsive reading order, accent contrast, and clipping. A bold composition succeeds through deliberate hierarchy, not by making every label uppercase or every boundary visible.
