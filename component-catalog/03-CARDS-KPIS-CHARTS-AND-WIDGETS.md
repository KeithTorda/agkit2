# 03 — Cards, KPIs, Charts & Dashboard Widgets (16 Component Types)

All numeric metrics, currency values (`₱`), percentages, and dates MUST apply `font-variant-numeric: tabular-nums` (`.tabular-nums`). Start all metrics at `0` / `₱0.00` when empty — zero fake chart or KPI numbers.

---

## 1. KPI & Metric Card Types (5 Variants)

1. **`SolidAccentStatCard`:** Solid contextual or `--ui-primary` surface, `--on-primary` ink, circular translucent icon badge (`48x48`), bold `tabular-nums` value, short 2–3 word plain label (`"Total Earnings"`, `"Active Campaigns"`).
2. **`SurfaceIconStatCard`:** `--ui-surface` card, soft tinted circular icon container (`--ui-primary-soft` + `--primary-ink`), primary metric, and subtle period comparison badge (`+12% vs last month` only when real comparison data exists).
3. **`ProgressStatCard`:** Metric header + target fraction (`12 / 20 Ready`) + horizontal `ProgressBar`.
4. **`SparklineStatCard`:** Compact metric on left + minimal SVG trend sparkline (`aria-hidden="true"`) on right.
5. **`BalanceHeroCard` (Wallet / Payout Summary):** Prominent available balance (`₱`), secondary pending/paid breakdown strip, and primary payout/statement action button.

---

## 2. Surface & Container Card Types (5 Variants)

6. **`StandardSurfaceCard`:** Clean header (`Title` + optional subtitle + right-aligned header action) + padded body + optional footer. Borderless or `1px solid var(--ui-border)` with subtle layered shadow (never stack heavy outline + shadow + colored border).
7. **`TabbedSurfaceCard`:** Card header integrated with `UnderlineTabs` or `SegmentedPills` switching body views without page reload.
8. **`EmptyStateCard`:** Centered muted `48x48`–`64x64` stroke SVG icon + 1 plain sentence (`"No campaigns yet."`) + 1 primary CTA button (`"Add Campaign"`).
9. **`LoadingSkeletonCard`:** Geometry-matching subtle shimmer blocks preserving exact card height to prevent layout shift (CLS).
10. **`SummaryKeyValueCard`:** Clean 2-column definition grid (`Label` muted left, `Value` crisp right) for record/transaction details and receipts.

---

## 3. Operational & Chart Widget Types (6 Variants)

11. **`ActivityTimelineWidget`:** Vertical rail with colored status dots, plain action summary, and relative/UTC timestamp (`tabular-nums`). Includes clean `"No recent activity."` empty state.
12. **`UserMediaListWidget`:** Avatar (`40x40` with initials fallback) + name + plain subtitle + right-aligned status badge or icon button.
13. **`ChecklistComplianceWidget`:** List of pass/fail verification items with crisp semantic `Pass` / `Check Rules` badges and plain explanation per rule.
14. **`TrendAreaChartCard`:** Responsive line/area chart container with header period filter (`7 Days`, `30 Days`, `This Year`) and zero-data empty state overlay when dataset is empty.
15. **`ComparisonBarChartCard`:** Grouped or stacked bar chart using `--ui-primary` + harmonious neutral/secondary token.
16. **`BreakdownDonutCard`:** Donut/ring chart paired with a tabular legend showing exact counts and percentages.
