# Style: Industrial Brutalist / Tactical Telemetry

Variant of [SKILL.md](./SKILL.md). Use when this direction is chosen: "brutalist", "Swiss industrial", "terminal", "HUD / telemetry", "blueprint", "data-heavy raw", or `DESIGN.md` names it. Everything in SKILL.md still applies. Hex values below are labelled examples of the style; `DESIGN.md` tokens replace them.

## What sets this style apart
| Choice | Why |
|---|---|
| Single colour scheme: Swiss Print is light-only, Telemetry is dark-only | Choosing the style is the specification. Record `colorScheme: light` or `dark` in `DESIGN.md`. |
| Crosshairs at grid intersections and ASCII framing brackets | The visible blueprint grid is the content of this style. Marks sit on real grid intersections and real data points. |
| Uppercase for structural headers and metadata | Casing is the style's structural device. Inline metadata rows are not eyebrows. |
| Serif as a textural disruptor | Deliberate contrast against heavy grotesks, degraded (halftone or dither), never for body. |
| Zero radius, 1-2px solid borders as compartments | Visible compartments replace whitespace grouping. Still one radius scale (0). |

Fake data stays out. Strings like `REV 2.6`, `UNIT / D-01`, random coordinates, or fake counters are invented precision (SKILL.md §4.7). Label only real revisions, units, IDs, and readings, or mark mock data as mock. A version label in the hero reads as a template unless it is a real release.

## Dials
`DESIGN_VARIANCE 8`, `MOTION_INTENSITY 3`, `VISUAL_DENSITY 8` unless the design read says otherwise.

## Pick one archetype per project
- **Swiss Industrial Print (light):** 1960s corporate identity and machinery manuals. Off-white paper substrate, monolithic heavy sans, visible grid lines, oversized viewport-bleeding numerals, red as the only accent.
- **Tactical Telemetry / CRT (dark):** mainframes, aerospace HUDs. Deactivated-CRT dark substrate, dense tabular data, monospace dominance, phosphor glow, scanlines, ASCII framing.
Never mix the two substrates in one interface.

## Typography
- Macro (structural headers): heavy neo-grotesque: `Archivo Black`, `Neue Haas Grotesk` (Black), `Roboto Flex` (heavy axis), `Monument Extended`. Fluid scale `clamp(4rem, 10vw, 15rem)`, tracking `-0.03em` to `-0.06em`, line-height `0.85-0.95`, uppercase.
- Micro (data, metadata, nav): monospace: `JetBrains Mono`, `IBM Plex Mono`, `Space Mono`, `VT323` (CRT only). `10-14px`, tracking `0.05-0.1em`, line-height `1.2-1.4`, uppercase, `tabular-nums`.
- Textural serif (rare): `Playfair Display`, `EB Garamond`; only through halftone or 1-bit dither post-processing.

## Colour (example values)
- **Swiss Print:** background `#F4F4F0` or `#EAE8E3`; ink `#050505` to `#111111`; accent `#E61919` / `#FF2A2A` (hazard red) for strike-throughs, thick rules, and vital highlights. Nothing else.
- **Telemetry:** background `#0A0A0A` or `#121212` (not `#000000`); phosphor `#EAEAEA` text; the same red accent; optional terminal green `#4AF626` for exactly one live readout, never as text color.
- The style's own restraint: no gradients, no soft shadows, no translucency. Colors simulate physical media or emissive displays.

## Layout
- Strict CSS Grid; elements anchor to tracks, nothing floats. `display: grid; gap: 1px` with contrasting parent/child backgrounds produces razor-thin dividers without border declarations.
- Bimodal density: tightly packed mono metadata clusters against vast negative space framing macro type.
- Full-width `<hr>` rules segregate operational units. Corners are 90 degrees everywhere.
- Mobile: the grid collapses to one column with the same 1px compartments; macro type keeps the `clamp()` floor.

## Symbology
- ASCII framing on real data points: `[ DELIVERY SYSTEMS ]`, `< RE-IND >`; directional glyphs `>>>`, `///`.
- `®`, `©`, `™` as geometric elements when the mark is real.
- Barcode-like repeating vertical lines and warning stripes as section separators, used sparingly (one device per section).

## Texture and post-processing
- Halftone / 1-bit dither: `mix-blend-mode: multiply` overlays with an SVG radial-dot pattern, or pre-processed images.
- CRT scanlines (Telemetry only): `repeating-linear-gradient(0deg, transparent 0 2px, rgba(0,0,0,0.1) 2px 4px)` on the background.
- Global grain: one low-opacity SVG noise filter on a `fixed pointer-events-none` layer (motion.md §5.D).

## Engineering
- Semantic tags for telemetry: `<data>`, `<samp>`, `<kbd>`, `<output>`, `<dl>`, `<table>` for real tabular data.
- `clamp()` only for macro typography; mono sizes are fixed.
- Motion stays at dial 3: state changes snap or step (`steps()` easing) rather than ease; no parallax, no scroll hijack. Reduced motion needs no special handling when nothing animates continuously.
- Contrast: hazard red on the paper substrate fails AA for small text; use it for rules, highlights, and display sizes only. Phosphor text and terminal green on `#0A0A0A` pass AA.
