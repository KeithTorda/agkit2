---
part: 04
title: States and formats
covers: empty states, errors, offline, onboarding, tooltips, notifications, status, live data, numbers, money, dates
---

# 04 - States and formats

Read when content changes with state or when displaying dates, amounts, status, or measurements. Style can be expressive; the information must remain accurate.

## Empty, loading, and error states

Distinguish an empty account, no filtered results, no permission, loading, partial data, and a failed request. "No receipts yet" must not appear merely because loading has not finished. Offer an appropriate next step: add the first item, clear a filter, request access, or retry. Illustration, humor, and animation are optional if they fit the chosen direction and do not obscure the task.

For errors, explain what the user can do without exposing stack traces or secrets. A 404 should help recover navigation. A permission error should not pretend a record is missing unless deliberately required by the security model. Preserve state after a transient failure. Maintenance notices need an honest time estimate when one exists, and an update channel if available. Rate-limit messages should state when retry is possible from actual server information.

## Onboarding and contextual help

Explain a useful next action, not every visible control. Allow a tour to be skipped and returned to where the workflow supports it. Tooltips should supplement labels; essential instructions belong visibly in the page. Hover content should also work with keyboard focus, and its meaning should remain available on touch devices.

## Notifications, badges, and status

- Use status terms the domain actually distinguishes: "Draft," "Pending approval," "Paid," "Voided."
- Mark new content with real criteria and retire stale badges. Do not invent "popular," "verified," or "official" labels.
- Gamification titles are acceptable when part of the product, understandable to its audience, and backed by real rules.
- A presence dot requires a presence signal. Show stale, disconnected, and unknown states where relevant.
- Describe data freshness honestly. Streaming, polling, periodic imports, and static snapshots can all be useful. "Live" is a product claim about timely updates, not proof that a specific transport such as WebSocket exists. State refresh cadence or "As of..." where delay affects interpretation.

## Dates, time, and numbers

Use explicit locale and time zone where ambiguity affects decisions. Store instants consistently, keep date-only values as dates, and avoid shifting birthdays or deadlines through unintended UTC conversion. Relative labels should update or be paired with a stable absolute timestamp. Use `<time datetime="...">` for machine-readable dates when useful.

Prefer unambiguous dates such as "16 October 2026" when users may disagree about numeric order. Let the chosen locale guide thousands separators and decimal marks. Use pluralization rules rather than building English strings from `count + ' item(s)'`.

Use currency-aware formatting such as `Intl.NumberFormat` with explicit currency. Keep calculation precision separate from display formatting. Receipts and accounting values normally require the domain's fractional precision; a compact KPI can use an abbreviation if the full amount is available. Do not visually truncate a value a user must compare, copy, or verify.

## Truncation and measurements

Use units and precision that match the task. Label percentages and distinguish percentage change from percentage points. If long names or references are truncated in a dense view, provide an accessible way to read and copy the full value. `title` alone is inadequate on touch. Preserve leading zeros in identifiers; they are strings rather than quantities.

## Review

Exercise loading, empty, partial, stale, offline, unauthorized, failed, and successful states that the feature can actually reach. Check long content, zero values, time-zone boundaries, full identifiers, and readable amounts. Do not create an exhaustive state flow for a static page that has none.
