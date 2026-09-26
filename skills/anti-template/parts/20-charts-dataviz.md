---
part: 20
title: Charts and Data Visualisation
covers: chart vs table choice, pie and donut abuse, 3-point line charts, gradient area fills, glow lines, dual axes, axes and scales, legends, colors, labels, tooltips, sparklines, KPI trend arrows, fake data, Chart.js Recharts ApexCharts ECharts defaults, responsive charts, chart accessibility, chart motion, maps, election and LGU data
---

# 20 — Charts and Data Visualisation

Read when: adding any chart, graph, sparkline, trend arrow, gauge, map, or report visual to a dashboard, report page, election results page or public data page.

Stat tiles and tables live in part 19. Dashboard layout lives in part 22. General color tokens live in part 12. Chart motion follows part 25.

## 20.1 Chart or table or sentence

Pick the smallest thing that answers the question. A chart earns its place when the shape of the data matters: trend, distribution, comparison across many items.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Chart for 2 or 3 data points | Chart as decoration | A sentence or two numbers: "₱120k in July, ₱148k in August (+23%)" |
| Line chart with 3 points | Implies a trend that is not there | Table, or text. Line charts need about 7+ points |
| Donut for 2 categories | Circle for a ratio | Text: "62% paid, 38% unpaid", or one horizontal bar |
| Every dashboard section gets a chart | Charts grid filler | Chart only where someone decides something from the shape. Everything else is a number or a table |
| Chart where users need exact values (payroll, grades, tax) | Values read off gridlines | Table with exact values; chart optional beside it |
| Chart with no question behind it ("Users overview") | Generic title, generic chart | Title states the question or finding: "Sales by week, last 12 weeks" or "Sales fell after the price change" |
| Full-width empty chart area for a new account | Big blank frame | Right-size the space; show the empty-state text instead of an empty axis. See part 04 |
| Same data shown as a chart and as a tile and as a table on one page | Triple display | One primary form; link to details |

## 20.2 Chart type misuse

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Pie or donut with 6+ slices | Angles cannot be compared | Horizontal bar chart, sorted by value |
| Donut with the total in the middle in 40px bold | Dashboard trope | Total as a plain number above a bar chart |
| Multiple donuts side by side for comparison | Impossible to compare | Grouped or stacked bar chart, or a small table |
| Pie slices that sum to more or less than 100% | Categories overlap or data missing | Pie only for parts of one whole; otherwise bars |
| 3D pie, 3D bars, perspective tilt | Distorts values | Flat 2D |
| Radar/spider chart for skills or product comparison | Looks technical, reads poorly | Bar chart or table |
| Gauge/speedometer for a single percentage | Heavy for one number | The number plus a thin progress bar, with the target stated |
| Area chart for categorical data (departments, products) | Implies continuity | Bar chart |
| Line chart connecting unrelated categories (Region I, NCR, CAR) | Implies order and trend | Bar chart |
| Stacked area with 8 series | Only the bottom series is readable | Small multiples (one small chart per series) or a line chart with 3 to 5 highlighted series |
| Stacked bars where users must compare middle segments | Middle segments have no common baseline | Grouped bars, or separate bar charts |
| Bubble chart for 5 items | Size is hard to judge | Bar chart |
| Funnel graphic for 3 steps | Decoration | Table: step, count, % of previous |
| Treemap for 4 categories | Showcase | Bar chart |
| Heatmap calendar of activity on a profile | GitHub trope | Skip, unless the client asked for it. See part 23 |
| Word cloud | Size of words means little | Bar chart of top terms with counts |
| Sankey for a simple two-step flow | Complex for no reason | Table or two bar charts |

## 20.3 Line and area charts

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Gradient area fill from the line color to transparent under every line | The AI dashboard look | Line only. If an area is needed (single cumulative series), flat fill at low opacity from a token |
| Glow on lines (`shadowBlur`, drop-shadow filter) | Neon trope | Plain 2px line |
| Smoothed curves (`tension: 0.4`, `type="monotone"`) on sparse data | Invents values between points and hides steps | Straight segments (`tension: 0`, `type="linear"`). Use step lines for values that change in steps (prices, stock levels) |
| Point markers with white fill and colored border on every point of a 365-day series | Clutter | No markers for dense series; markers only for fewer than about 15 points or the last point |
| Line chart with a gap filled by drawing through missing days | Lies about missing data | Show gaps (`spanGaps: false`, `connectNulls={false}`) and note missing periods |
| 6+ lines in one chart, all saturated colors | Spaghetti | Highlight 1 to 3 series in color, rest in a muted gray token; or small multiples |
| Line ending in a pulsing dot | Motion trope | Static last-point marker with its value label |
| Y axis starting at a non-zero value on an area chart | Area implies zero baseline | Area and bar charts start at zero. Line charts may start elsewhere if the axis is clearly labelled |

## 20.4 Bar charts

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Bars with rounded tops at 8 to 12px radius | Template look; top blurs the value | 0 to 2px radius |
| Gradient fills in bars | Decoration | Solid fill from a token |
| Every bar a different color | Rainbow without meaning | One color for all bars; highlight one bar in the accent when it matters |
| Vertical bars with rotated 45-degree category labels | Labels unreadable | Horizontal bars when labels are longer than about 6 characters |
| Bars unsorted (alphabetical or DB order) for ranking data | Hard to rank | Sort by value, descending, unless the categories have a natural order (months, grades) |
| Bar axis not starting at zero | Exaggerates differences | Bars start at zero, always |
| Very thin bars with wide gaps, or fat bars touching | Default spacing | Gap about 20 to 40% of bar width |
| Value labels plus gridlines plus axis ticks plus tooltips all showing the same numbers | Redundant ink | Direct value labels at the bar end and drop gridlines, or keep gridlines and drop labels |
| Hover that grows the bar or adds a shadow | Motion trope | Hover dims other bars slightly or shows a tooltip; nothing grows |

## 20.5 Axes, scales and gridlines

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Dual Y axes (two different units on left and right) | Any two lines can be made to look correlated | Two charts stacked with a shared X axis, or index both series to a base of 100 |
| Truncated Y axis to make a small change look large | Misleading | Zero baseline for bars and areas; state the range clearly for lines |
| Axis labels missing units | "What is 40?" | Units in the axis title or tick format: "₱ thousands", "Students", "%" |
| Tick labels like 0, 2500000, 5000000 | Unformatted | `₱2.5M` in ticks, exact values in tooltips; locale-aware formatting |
| 10+ gridlines at high contrast | Heavy | 3 to 5 horizontal gridlines in a faint border token; no vertical gridlines for time series |
| Log scale with no label | Readers assume linear | Avoid log scale in dashboards for general users; if used, label "Log scale" |
| Time axis with irregular gaps drawn as equal spacing | Categorical axis for dates | Time scale (`type: 'time'`) so gaps are proportional |
| X axis showing every date label on a 90-day chart | Label pile-up | Auto-skip ticks; show weekly or monthly ticks |
| Axis lines, tick marks and chart border all drawn | Box around everything | Drop the chart border and top/right axes; keep a baseline |

## 20.6 Labels, titles and legends

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Chart title "Analytics Overview" or "Performance" | Says nothing | Title names the measure, unit and period: "Paid orders per week, Jan–Jun 2025" |
| Legend placed far from the lines, requiring color matching | Eye travel | Direct labels at the end of each line or next to each series |
| Legend for a single-series chart | Redundant | Remove; the title names the series |
| Legend items with round color dots at 8px | Hard to match | Short line or square swatches at 12px with text labels |
| Clickable legend that hides series, but nothing says so | Hidden feature | Either keep the default without relying on it, or add a visible "Show/hide series" control |
| Source and "as of" date missing | Cannot trust or reuse | Caption under the chart: "Source: POS sales. Updated 23 Sep 2025, 8:00 AM" |
| Annotations missing for obvious events (price change, holiday, system outage) | Spike unexplained | Short annotation on the chart at that point |
| Percent labels on pie slices overlapping | Default labelling | Fewer slices, or a bar chart with labels |
| Chart subtitle with hype ("See how your business is growing") | Marketing tone | Delete, or state the finding in plain words |

## 20.7 Color in charts

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Indigo/violet/pink series palette (#6366f1, #8b5cf6, #ec4899) | AI default | Chart palette tokens from DESIGN.md (`--chart-1` ... `--chart-5`), tested for contrast and color blindness |
| Library default rainbow (Chart.js random colors, ECharts default palette) | Unchanged defaults | Set the palette once in a shared chart theme |
| Red and green as the only difference between series | Fails for red-green color blindness | Different lightness plus labels; add patterns or direct labels |
| Status colors used as series colors (green = product A) | Implies good/bad | Neutral categorical tokens for series; status colors only for status |
| Up = green, down = red regardless of meaning | Rising expenses shown as good | Color by meaning: an increase in overdue accounts is bad. Or keep deltas neutral and state direction in text |
| Sequential data (low to high) with a categorical rainbow | Order lost | Single-hue sequential ramp from light to dark using tokens |
| Diverging data (above/below target) with a sequential ramp | Midpoint lost | Diverging palette with a neutral middle at the target |
| More than 6 to 8 categorical colors | Unreadable | Top 5 plus "Other" in gray |
| Series colors change between charts for the same category | Relearn per chart | Fixed mapping: the same category always uses the same token |
| Dark-mode chart that keeps light-mode colors and gridlines | Poor contrast | Dark-mode chart tokens: lighter series, dimmer gridlines. See part 34 |
| Series lines below 3:1 contrast against the background | Invisible lines | Graphical objects need 3:1 against adjacent colors (WCAG 1.4.11) |

## 20.8 Tooltips and interaction

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Tooltip as the only way to read values | Hover-only; nothing on touch or keyboard | Direct labels for key values, plus a data table view |
| Tooltip with glass blur, gradient border and shadow | Visual trope | Solid surface token, 1px border, readable 13 to 14px text |
| Tooltip showing raw values (`1249.5`, `2025-03-04T00:00:00Z`) | Unformatted | Same formatting as the rest of the UI: `₱1,249.50`, `Mar 4, 2025` |
| Tooltip listing all 8 series in random order | Hard to find | Sort by value, or show only the hovered series |
| Crosshair, zoom, pan, brush and export toolbar enabled by default | Library features left on | Turn off unless users need them. Keep Download CSV if reports are exported |
| Zoom on scroll wheel that hijacks page scroll | Trap | Disable wheel zoom; use buttons or a range selector |
| Click on a chart segment does nothing though the cursor is a pointer | False affordance | Pointer only on elements that link to filtered detail |

## 20.9 Sparklines and KPI trend arrows

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Sparkline in every stat tile | Decoration | Sparkline only where the recent trend changes a decision, with 7+ points |
| Sparkline with no scale, period or current value | Shape without meaning | Current value beside it and period in the label: "Last 30 days" |
| Sparkline with gradient fill and glow | Trope stack | 1.5px line in a neutral or primary token, optional last-point dot |
| Different Y scales on sparklines placed side by side for comparison | Misleading comparison | Shared scale, or note that scales differ |
| Trend arrow "↑ 12.5%" with no comparison base | Unclear | "+12% vs last month" as text |
| Trend arrow green for every increase | Meaning ignored | Color by good/bad for that metric, or neutral color and let the words carry the meaning |
| Percent change on tiny bases ("+300%" from 1 to 4) | Misleading | Show absolute change when the base is small: "+3 (from 1)" |
| Arrow icons as the only indicator | Color and icon only | Text sign and word: "Up 12%", with `aria-label` if an icon is used |
| Invented change figures shown on first load | Fake data | Hide the delta until two real periods exist |

## 20.10 Fake and placeholder data

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hard-coded arrays `[65, 59, 80, 81, 56, 55, 40]` left in production | Chart.js docs sample | Real query results. If data is not wired yet, show "No data yet" text, not a fake chart |
| Labels "January" to "July" in a chart that should show real months | Sample data | Labels from the data |
| `Math.random()` data for demos | Random shape, reloads differently | Fixed seed fixtures in tests only; never in shipped UI |
| Smooth rising curve in the marketing screenshot | Invented success | Real anonymised data, or a labelled illustration ("Sample data") |
| Fake "live" chart ticking with random values | False real-time claim | Live only with push data; otherwise "Updated X ago" |
| Demo data mixed with real data after go-live | Seed data left in | Remove seeders from production; add a check in the deploy script |
| Placeholder chart component for a report nobody asked for | Scope creep | Remove it |

## 20.11 Library defaults

Library defaults are the fastest way to spot a generated dashboard. Set a shared theme once and import it everywhere.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Chart.js default: legend on top, 12px Helvetica, random palette, animated grow-in, tension on lines | Unchanged defaults | Global `Chart.defaults`: font from DESIGN.md, palette tokens, `animation: false` or under 300ms, `tension: 0`, legend off or bottom |
| Recharts `<CartesianGrid strokeDasharray="3 3" />` plus `<Tooltip />` plus `<Legend />` on every chart | Docs example copied | Horizontal solid faint gridlines only, formatted tooltip, legend only for 2+ series |
| Recharts `<defs><linearGradient>` area fills | Docs example | Remove gradient; plain line |
| ApexCharts toolbar (zoom, pan, download icons) visible on every chart | Default on | `toolbar: { show: false }` unless export is needed |
| ECharts default theme with rich-text labels and shadow | Default | Custom theme registered once |
| Highcharts credit link "Highcharts.com" left visible | Default | Remove per license terms, or leave as licensed; check the client's license |
| shadcn chart blocks copied with `chart-1` to `chart-5` default hues | Library default look | Map `--chart-*` variables to DESIGN.md tokens |
| Tremor or similar kit cards with area chart plus delta badge on every tile | Kit look | Use primitives, not the kit's full dashboard pattern |
| Several chart libraries in one app | Bundle size, inconsistent look | One library for the project |
| A full chart library loaded for one sparkline | Heavy | Inline SVG `<polyline>` for sparklines. See part 34 |

```js
// Banned: docs sample left in
new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [{
      label: 'My First Dataset',
      data: [65, 59, 80, 81, 56, 55, 40],
      fill: true,
      backgroundColor: gradient,           // purple to transparent
      borderColor: 'rgb(139, 92, 246)',
      tension: 0.4
    }]
  }
});

// Use: real data, shared theme, no fill, no smoothing
new Chart(ctx, {
  type: 'line',
  data: {
    labels: weeks,                          // from the API
    datasets: [{ label: 'Paid orders', data: paidOrders, borderColor: css('--chart-1'), tension: 0 }]
  },
  options: {
    animation: false,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true, title: { display: true, text: 'Orders' } } }
  }
});
```

## 20.12 Size, layout and responsiveness

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Charts grid: 2x2 equal cards each with a chart | Template dashboard | One main chart at full content width; secondary charts smaller or in a report page. See part 22 |
| Chart height fixed at 400px on a 390px phone | Tall, squashed | Aspect ratio per breakpoint; 200 to 260px tall on mobile |
| Canvas that does not resize when the sidebar collapses | Blurry or overflowing | `responsive: true`, `maintainAspectRatio` set, container with explicit height; ResizeObserver if needed |
| Tiny 10px labels on mobile | Unreadable | 12px minimum; fewer ticks |
| Horizontal bar chart with 40 categories crammed in | Unreadable | Top 10 plus "Show all" table |
| Chart inside a card inside a card with padding on each | Nested frames | Chart on the page surface with a heading |
| Chart printed with dark background and colored lines | Wastes ink, poor print | Print stylesheet: white background, dark lines, legend visible |

## 20.13 Accessibility of charts

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `<canvas>` with no text alternative | Invisible to screen readers | `role="img"` with an `aria-label` stating the finding, plus a visible or toggleable data table |
| SVG chart with every path announced | Noise | `aria-hidden="true"` on decorative parts; summary in a `<figcaption>` |
| Chart wrapped in `<div>` with no caption | No context | `<figure>` with `<figcaption>` giving title, source and date |
| Meaning carried only by color | Fails 1.4.1 | Direct labels, patterns, or shape markers |
| Interactive chart that cannot be reached by keyboard | Mouse-only | Keyboard focus on data points, or a table with the same data |
| Motion that loops (animated flows, pulsing dots) | Distracting, fails 2.2.2 if over 5s | Static chart; respect `prefers-reduced-motion` |

```html
<!-- Use -->
<figure>
  <figcaption>
    <h3>Paid orders per week, Jan–Jun 2025</h3>
    <p>Orders rose from 210 to 340. Source: POS. Updated 23 Sep 2025.</p>
  </figcaption>
  <canvas role="img" aria-label="Line chart. Paid orders per week rose from 210 in January to 340 in June."></canvas>
  <details>
    <summary>Show data table</summary>
    <table>...</table>
  </details>
</figure>
```

## 20.14 Motion in charts

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Bars grow from zero and lines draw in on every page load | Library default animation | `animation: false`, or a single fade under 300ms. See part 25 |
| Re-animation on every data refresh or tab switch | Distracting | Update values in place with no animation |
| Numbers counting up inside donuts | Counter trope | Render the final number |
| Animated gradient or shimmer inside the chart area while loading | Shimmer trope | Plain skeleton box or "Loading..." text if load exceeds about 500ms |

## 20.15 Maps

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Map for data that has one or two locations | Map as decoration | Address text and a link to open in Google Maps or OpenStreetMap |
| Choropleth with raw counts (bigger provinces look darker) | Measures population, not the rate | Normalise: per 1,000 residents, % of voters, per household |
| Rainbow color ramp on a choropleth | Order lost | Single-hue sequential ramp from tokens, 5 to 7 classes, with a legend showing ranges |
| Dark "cyber" map style with neon markers | Trope | Light, low-contrast basemap so data stands out |
| Hundreds of overlapping markers | Unreadable | Clustering, or a choropleth by barangay or municipality |
| Map with no list alternative | Keyboard and screen reader users stuck | A sortable table of the same regions next to or below the map |
| Map that captures scroll and traps the page on mobile | Scroll trap | Require two-finger drag on mobile (`gestureHandling: 'cooperative'` or Leaflet `scrollWheelZoom: false`, `dragging` only after tap) |
| Philippine map missing island groups or with wrong boundaries from a random GeoJSON | Bad source data | Use boundaries from an official or documented source (PSA/PSGC-based sets, NAMRIA, HDX) and cite it |
| Map legend without the unit or data date | Unclear | "Voter turnout, %, as of 13 May 2025" |
| Map tiles from a provider without attribution | License breach | Keep the required attribution (e.g. OpenStreetMap contributors) |

## 20.16 Election, LGU and public data

Public data pages for COMELEC-style results, barangay statistics, school enrolment and LGU budgets carry legal and trust weight.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Results shown as a donut per position | Hard to compare candidates | Horizontal bars sorted by votes, with exact vote counts and % labels |
| Percentages without the vote count and precincts reporting | Cannot verify | "Votes: 12,431 (48.2%). 212 of 240 precincts reporting. As of 9:40 PM, 13 May 2025" |
| Candidate bars colored by party with made-up party colors | Invented | Neutral bars, or colors defined by the client for the report |
| "Live results" badge on a page updated from uploads every hour | False claim | "Updated 9:40 PM" and the update schedule |
| Budget chart in "₱" with no year or source ordinance | Unverifiable | "Annual budget 2025, per Appropriation Ordinance No. XX. Source: Municipal Budget Office" as supplied by the client |
| Population pyramid or charts built from invented numbers for a demo LGU site | Fake public data | Use data the client supplies, with the source line. Otherwise leave the section out |
| Precinct finder results as a map only | Map-only | Precinct number, school name, address and room as text first; map link second |
| Enrolment chart by grade using a pie | Wrong type | Bar chart by grade level, ordered by grade |

## 20.17 Philippine number formats in charts

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "$" in tick labels or tooltips | Template default | `₱` via `Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' })` |
| "1.2B" style abbreviations mixed with "1.2 billion" in one page | Inconsistent | One abbreviation rule: `₱1.2M`, `₱3.4B` in ticks; full values in tables |
| Month labels in a locale the device happens to use | Inconsistent output | Pass the app locale explicitly to date formatters |
| Fiscal and school years shown as calendar years | Mismatch | "SY 2025–2026", "FY 2025" as the client uses |

## 20.18 Check
- [ ] Every chart answers a stated question; the title names measure, unit and period.
- [ ] No charts for 2 to 3 data points; a sentence or table is used instead.
- [ ] Line charts have about 7+ points; no donut for 2 categories.
- [ ] No pie or donut with more than 5 slices; no 3D, radar or gauge for simple values.
- [ ] Bars sorted by value unless categories have a natural order; horizontal bars for long labels.
- [ ] Bars and areas start at zero.
- [ ] No dual Y axes.
- [ ] No gradient area fills, glow lines, rounded bar tops or gradient bars.
- [ ] Lines use straight segments; gaps in data are shown, not bridged.
- [ ] Axes carry units; ticks and tooltips are formatted (₱, commas, dates).
- [ ] 3 to 5 faint horizontal gridlines at most.
- [ ] Direct labels preferred; no legend for single-series charts.
- [ ] Source and "as of" date appear under data charts.
- [ ] Palette comes from DESIGN.md chart tokens; max 5 to 8 categorical colors.
- [ ] Same category uses the same color on every chart.
- [ ] Color is never the only way to tell series apart; series meet 3:1 contrast.
- [ ] Up/down colors follow the metric's meaning.
- [ ] Trend deltas state the comparison base in words; small bases show absolute change.
- [ ] Sparklines only with 7+ points and a stated period.
- [ ] No sample data, `Math.random()` or docs arrays in shipped charts.
- [ ] "Live" appears only for push data.
- [ ] One chart library, one shared theme; library toolbars and credits handled.
- [ ] Sparklines use inline SVG, not a full library.
- [ ] Charts resize with their container; mobile height 200 to 260px; labels 12px+.
- [ ] Each chart is a `<figure>` with a caption, text alternative and a data table option.
- [ ] Chart animation off or under 300ms; no re-animation on refresh; reduced motion respected.
- [ ] Maps only when location matters; choropleths use rates, a sequential ramp and a legend with units.
- [ ] Maps have a table alternative, attribution, and do not trap scroll.
- [ ] PH boundary data comes from a cited source.
- [ ] Election results show vote counts, %, precincts reporting and update time.
- [ ] Public data charts use only client-supplied data with a source line.
- [ ] Currency uses `₱` with `en-PH` formatting; school and fiscal years are labelled as such.
