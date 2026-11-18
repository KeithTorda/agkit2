# 04 — Data Tables, Ledgers, Filters & Pagination (12 Component Types)

Every data table MUST wrap inside a horizontal scroll container (`overflow-x-auto` / `.table-responsive`), declare `<th scope="col">`, right-align currency/numeric columns with `.tabular-nums`, and render a clean full-width `<td colspan="...">` `EmptyState` when empty.

---

## 1. Data Table Archetypes (8 Variants)

1. **`StandardCrudTable`:** Uppercase small-caps column headers (`0.75rem`, `letter-spacing: 0.04em`), comfortable row padding (`0.9rem 1.15rem`), primary-tinted hover state, semantic `StatusBadge`, and right-aligned `IconSquare` action buttons (`Edit`, `View`, `Delete` with `aria-label`).
2. **`TabbedStatusLedger`:** Integrated top `SegmentedStatusTabs` (`All (0)`, `Ready (0)`, `Pending (0)`, `Paid (0)`) filtering rows by status with live `tabular-nums` counters.
3. **`FloatingRowTable`:** Subtle vertical gap (`6px–8px`) between rounded surface rows on `--ui-canvas` for high-scanability transaction queues.
4. **`BulkSelectableTable`:** Header master checkbox (`Select all rows`) + per-row checkboxes + floating contextual bulk-action bar (`Selected: 3` • `Export` • `Mark Paid`) when `>= 1` row is checked.
5. **`ExpandableDetailTable`:** Main summary row with chevron toggle expanding a secondary sub-row (`.ui-subtle-box`) for notes, instructions, or line items.
6. **`ProfileDirectoryTable`:** Avatar/initials circle + primary name & secondary contact info stacked cleanly in column 1, paired with role, date joined, status badge, and row actions.
7. **`FinancialLedgerTable`:** Strict accounting layout: Reference ID, UTC/Local Date, Campaign/Party, Views/Qty, Rate, right-aligned `₱` Subtotal/Total (`DECIMAL(12,2)` server-computed), Payout Status (`Pending`, `Approved`, `Paid`, `Voided`), and `Print Receipt` button (never hard-delete financial rows — soft-void with reason).
8. **`CompactQueueTable`:** Dense `0.65rem 0.9rem` cell padding with inline progress bar or rule badge for high-density monitoring panels.

---

## 2. Table Toolbars, Row Menus & Pagination (4 Variants)

9. **`TableFilterToolbar`:** Left debounced `SearchInput` (`250ms–300ms`) + middle status/category select + right `DateRangeFilter` & primary `Add` button (`flex-wrap`, `gap-2` on mobile).
10. **`UpwardSafeRowActionMenu`:** Row action dropdown (`...`) configured with Popper flip / `dropup` on bottom rows so menus are **never** clipped by `overflow-x-auto` containers.
11. **`GutterPaginationBar`:** Left summary (`Showing 1–15 of 42`) + right page buttons (`Prev`, `1`, `2`, `3`, `Next`) with `--ui-primary` active pill (`--on-primary` ink) and preserved query-string filters.
12. **`PageSizeSelector`:** Clean compact select (`15 / 30 / 50 per page`) synced with URL query params.
