# 06 — Buttons, Badges, Modals, Alerts, Tabs & Navs (16 Component Types)

Never use `<a href="javascript:void(0)">` or `<div onclick="...">` for interactive controls — always use `<button type="button">` for actions and `<a href="...">` for real URL navigation.

---

## 1. Button System (6 Variants)

1. **`PrimaryButton`:** Solid `--ui-primary` background + `--on-primary` ink. Restrict to **one primary CTA** per card, modal, or form footer.
2. **`SoftTintedButton`:** `--ui-primary-soft` background + `--primary-ink` text — ideal for secondary header/card actions (`View All`, `Copy Caption`).
3. **`OutlineButton`:** Transparent background + `1px solid var(--primary-ink)` border & text — ideal for `Cancel`, `Export`, or filter triggers.
4. **`GhostButton`:** Borderless subtle hover button for low-emphasis toolbar controls.
5. **`DestructiveButton`:** Crimson danger fill (`#dc3545` + `#ffffff`) or soft danger tint — always paired with a confirmation step before deleting/voiding data.
6. **`IconSquareButton` (`Sharp`):** Compact `32x32` or `36x36` square icon button for table row actions — **requires** `aria-label` (`aria-label="Edit campaign"`).

**Tactile & In-Flight Discipline:**
- `:active:not(:disabled)` applies subtle `transform: scale(0.97)` (`120ms` ease-out).
- Submitting forms lock the button (`disabled`, `aria-busy="true"`, inline spinner + `"Saving..."`).

---

## 2. Status Badges & Indicators (3 Variants)

7. **`SoftStatusBadge` (Default for Tables & Cards):** Tinted pill + high-contrast dark/light ink (`>= 4.5:1`) with short plain words (`Ready`, `Pending`, `Paid`, `Active`, `Paused`, `Voided`, `Check Rules`). Avoid heavy solid badges inside dense tables.
8. **`DotStatusBadge`:** `6px` semantic colored dot + crisp label inside a subtle neutral pill.
9. **`CounterPillBadge`:** Compact `tabular-nums` count badge inside tabs or sidebar items.

---

## 3. Modals, Drawers, Alerts & Navigation Primitives (7 Variants)

10. **`CenteredFormModal`:** Clean header (`Title` + `Close` button with `aria-label="Close"`), `1.5rem` padded single-column body, right-aligned primary submit + left `Cancel` (`gap-2`), focus trap, `Escape` close, and focus restoration to trigger.
11. **`DestructiveConfirmDialog`:** Compact `max-w-md` dialog stating the exact consequence in plain words (`"Delete this campaign? This cannot be undone."` or `"Void this payout record?"` + required reason input).
12. **`MediaPreviewModal`:** Centered modal with locked `aspect-ratio` (`9 / 16` vertical clip or `16 / 9` source video) that pauses and unloads `<video src>` immediately when closed.
13. **`InlineAlertBanner`:** Soft semantic surface + left accent bar + plain actionable message (`role="alert"` for errors, `aria-live="polite"` for status updates).
14. **`ToastNotificationStack`:** Non-blocking corner toast (`"Campaign saved."`, `"Copied."`) with `aria-live="polite"` and pause-on-hover auto-dismiss.
15. **`UnderlineAndSegmentedTabs`:** `role="tablist"` / `role="tab"` keyboard-accessible tabs (`ArrowLeft` / `ArrowRight`) with instant `0ms` panel switching.
16. **`AccordionAndProgressBar`:** Accessible `<details>`/`aria-expanded` collapsible sections and smooth GPU/width `ProgressBar` (`role="progressbar"`, `aria-valuenow`).
