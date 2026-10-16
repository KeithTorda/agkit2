---
part: 19
title: Data display and browsing
covers: tables, lists, cards, sorting, filtering, pagination, density, KPIs, detail views, badges, avatars, feeds, kanban, calendars
---

# 19 - Data display and browsing

Read when presenting records, metrics, activity, or schedules. Data displays can be expressive or restrained according to the design. Choose containers from comparison, scanning, and interaction needs rather than an anti-card rule.

## Select a useful structure

Tables suit repeated fields and cross-record comparison; lists suit a primary item with supporting details; cards suit independent, visual, or richer items; detail lists suit labeled facts. Grids, timelines, kanban, trees, and calendars each convey different relationships. Do not force one container onto unrelated content, or ban repetition when it helps users learn the system.

## Tables and record lists

Use semantic tables for tabular data with headers, captions or an accessible purpose, and row headers when appropriate. Align numeric data for comparison; use tabular numerals when helpful. Choose columns by the user's task, with full values accessible when truncation is necessary. Amounts, references, and dates used for verification must remain readable and copyable.

Sorting should show its direction and data scope. Put a keyboard-reachable sort button in the header and expose the current sort state. Filters and search need visible applied state, clear reset, no-results, loading, error recovery, and stable URL state where users share or revisit results. Distinguish an empty dataset from an empty filtered result.

Use pagination, load more, infinite browsing, or virtualization according to dataset and workflow. Keep totals honest when unknown or approximate. Preserve focus, selection, and return position when rows change. Virtualization can improve performance but requires attention to screen readers, find-in-page, keyboard navigation, and variable row sizes.

## Density and mobile adaptation

Density should reflect reading distance, input method, complexity, and expected repetition. Compact does not mean tiny targets. Spacious does not mean hiding the useful records below a giant header. On mobile, choose a deliberate scroll region, prioritized columns, expansion, or another representation without losing essential relationships or actions.

## KPIs, statuses, badges, and avatars

A metric needs a label, unit, period, and a comparison basis if a trend is shown. Do not invent numbers, trend arrows, or growth percentages. Compact values can have a readable full-value alternative. Icons and color may support scanning or brand expression; there is no icon or hue quota.

Status should have text or another non-color cue. Badges need real criteria. "Verified," presence dots, and unread counts require corresponding data. User avatars may be photos, illustration, initials, or a chosen fallback; handle missing images without a broken-image icon. Do not present generated identities as real customers or staff.

## Other data patterns

Activity feeds should identify what changed, actor where appropriate, and timestamp. Tree views need hierarchy and keyboard behavior. Kanban needs a non-drag way to move cards and clear permissions. Calendars need locale, time zone, overlap handling, and an accessible alternative where the visual arrangement is insufficient. Do not suggest a date is available merely because sample data has no event there.

Loading and partial-error states should preserve useful existing data when appropriate and communicate freshness. Client-side filtering of one fetched page must not be presented as a search across the whole database.

## Review

Check real or representative records, long values, zero values, multiple currencies if supported, sorting/filter combinations, empty/error states, keyboard actions, selection, and small-screen comparison. Verify that displayed facts match their source and period.
