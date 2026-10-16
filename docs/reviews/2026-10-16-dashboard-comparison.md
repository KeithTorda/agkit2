# Dashboard comparison evidence — 2026-10-16

This dated note records an observed case; current rules and skills define policy. Both samples used the same approved modern light operations-dashboard brief, 18-order fixture, model configuration, local assets and control contract. The baseline was the original pre-repair kit snapshot; the other used 2.8.0. Both builders could inspect and repair their drafts before a frozen first completed handoff.

One blind model reviewer scored original/2.8 respectively: typography 4/3, composition 4/4, responsive presentation 4/3, task clarity 4/4, all out of 5 with equal weights. Equivalent totals were 8/10 and 7/10. These are subjective judgments for one observed pair. Both passed 25 shared browser/functional checks at 1440, 768 and 390 CSS pixels; all four summary metrics and offline opening/search were also checked.

The original's advantage was supporting-text legibility and tablet/table presentation. The 2.8 draft had coherent panels, status differentiation and a compact mobile header, but small supporting labels, reduced tablet content width and weak discoverability of offscreen table data. Scrolling itself worked. This distinguishes functionality from the affordance and readability of that function.

Two harness assumptions were corrected while preserving original artifacts: reloading retained URL filters between independent cases, and selecting the first table measured a hidden chart-data table instead of the order table. Both samples were rerun with the same corrected checks. No frozen dashboard code was altered. Apparent test failures caused by those assumptions were not product defects.

The 2.8.1 guidance applies narrow, contextual lessons: review actual-size task information, choose layout from available content space, reveal and exercise access to essential data, and validate the test's state/target. It does not mandate the original's palette, composition, exact typography, device breakpoint or scoring target. See [app UI](../../skills/frontend-design/app-ui.md) and [comparison testing](../../skills/browser-verification/comparison-testing.md).

The original experiment is preserved separately as the local agkit2-design-test artifact bundle, including frozen sources, screenshots, raw results and blind review. It used Codex builders applying kit snapshots, not live Antigravity generation. One brief and one generation per condition do not establish broad causal superiority, full accessibility or cross-browser coverage. Any later draft repair must be labeled refinement and does not replace this result.
