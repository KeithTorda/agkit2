---
part: 20
title: Charts and visual evidence
covers: chart selection, axes, labels, color, interaction, trends, sample data, maps, accessibility
---

# 20 - Charts and visual evidence

Read when presenting quantitative or geographic information. Match the visual language to the selected design while preserving truthful interpretation. Gradient fills, glow, animation, rich color, and decorative framing are valid when they do not mislead or hide the data.

## Choose the representation

Start with the question: comparison, trend, distribution, relationship, composition, location, or a single value. A sentence or table may answer more clearly than a chart; a chart may reveal a pattern that a table hides. Do not add visualizations solely to fill a dashboard, or remove them solely because a library demo uses the same shape.

Use line charts for meaningful ordered sequences; bars for comparable categories; scatterplots for relationships; distribution plots for spread; and part-to-whole displays only where the denominator is meaningful. Pie or donut charts can work for a small, legible composition, but many similar slices are difficult to compare. A different chart type is a decision based on the data, not a style prohibition.

## Scales and labels

State the measure, units, period, source, and important filters. Bars generally need a zero baseline because length encodes magnitude; if a specialized view breaks that expectation, make the choice explicit and assess whether another encoding would be more honest. Line charts may use nonzero ranges when clearly labeled. Log scales, dual axes, aggregation, missing values, and cumulative totals require careful explanation.

Avoid connecting across missing observations as though measured values existed. Distinguish zero from missing. Keep date intervals and sampling honest. Tooltips should not be the sole way to learn a critical value or definition. Abbreviate with a full-value alternative and appropriate locale formatting.

## Color and visual treatment

Use the chosen palette with stable series meaning and sufficient distinction. Sequential or diverging scales should reflect the data. Direct labels, patterns, line styles, markers, and position can supplement color. Decorative glow or gradients should not obscure line boundaries, labels, comparative area, or low-contrast series.

Grid lines, typography, margins, and legends should help reading. Remove clutter when it competes, but do not strip explanatory information to create a minimalist screenshot. Adapt axes and labels intentionally at narrow widths; maintain a way to inspect detail.

## Interaction and motion

Provide keyboard and touch access to relevant interaction. Hover effects may enhance exploration; include equivalent focused or selected states and a textual/table view for essential information. Filters and date ranges should update the actual data and explain loading, error, and freshness.

Animated transitions can preserve continuity or explain a change. Use the agreed motion language and reduced-motion alternative. The final data should remain available when animation fails, is disabled, or is skipped. A dashboard value must not wait for a long count-up before becoming readable.

## Real and sample data

Use real data when claiming a real result. Fictional samples are useful in a prototype or demo if clearly labeled and isolated from production records. Do not invent growth rates, election totals, customer counts, or confidence intervals. A trend arrow needs a defined comparison period and formula. A percentage change from zero needs special handling rather than an infinite or misleading value.

## Maps and public information

Maps should use actual locations, correct boundaries for the purpose, source attribution, and a readable legend. Location privacy matters; avoid exposing exact personal addresses in a public demo. Provide a list or textual alternative for offices, services, or polling places that people must find. Verify current official sources for election and public-safety information.

## Review

Check calculations against source data, axes, units, date boundaries, zero/missing values, filter combinations, responsiveness, and accessible alternatives. An attractive chart is not evidence that the data is correct.
