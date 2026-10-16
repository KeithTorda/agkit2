# Style: Dark operations and data UI

Use for an approved dark dashboard, monitoring view, trading/operations console, or low-light interface. This is one direction, not a kit default. [SKILL.md](./SKILL.md) and the user's actual `DESIGN.md` take precedence.

## Surface and text hierarchy
Choose a base, surface, raised layer, border, foreground, and supporting-text roles that remain distinct on actual screens. Example palette: base `#070B14`, surface `#0B132B`, raised `#111C3A`, foreground `#F1F5F9`. The examples are not mandatory; neutral, warm, or brand-tinted dark canvases can work.

Text needs enough luminance for its size, weight, and context without making every cell equally bright. Pure white can emphasize a headline; softer bright text can make dense reading more comfortable. Aim above minimum contrast where useful, but do not force every secondary label to a particular 7:1 or 10:1 target without considering hierarchy.

Measure normal text against each actual surface; check transparency and overlays in the rendered result. Do not assume a named Tailwind shade always passes or fails.

## State and accent
Use status hues consistently and pair them with words, icons, shapes, or positions. Example success foreground `#34D399` may work on a deep green tint; verify the composited background. Primary action and focus colors can use the real brand palette. Decorative color is allowed when the direction includes it; do not make decoration look like an operational alarm.

A subtle glow may emphasize a live or selected element when useful. Glow does not replace focus or text contrast. Static indicators should not pulse merely to make the screen feel active.

## Components
- Tables: consistent columns, aligned comparable numbers, tabular figures, readable density, and touch/keyboard-accessible actions.
- Charts: a distinguishable palette, labels, usable gridlines, and an alternative to color-only series identification. Use the [chart and data-visualization guidance](../anti-template/parts/20-charts-dataviz.md) when the actual chart needs it.
- Panels: group by task and information relationship. Avoid adding an identical stat-card row where a queue, exception list, or chart is more useful.
- Controls: visible focus on each surface, clear selected/disabled/pending states, and comfortable target spacing.

Reuse the project's component classes/tokens rather than scattering palette literals. Do not install a dashboard package solely for this look.

## Theme and motion scope
Dark-only is valid; both themes ship only when requested or already supported. If both ship, design and verify the light counterpart deliberately. Contrasting light sections may be used for emphasis when the page composition supports them.

Quiet operational UI commonly needs feedback-only motion. Do not auto-add reveal effects, looping grids, or animated charts. Richer behavior follows the agreed intent and reduced-motion preference.

## Review
Inspect real narrow and wide layouts, long values, low-emphasis labels, badge contrast, grayscale state comprehension, focus, and important interactions. A screenshot establishes composition; it does not prove live data correctness or keyboard behavior.
