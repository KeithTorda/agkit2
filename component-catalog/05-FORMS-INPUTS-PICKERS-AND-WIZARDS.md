# 05 — Forms, Inputs, Pickers, Dropzones & Wizards (18 Component Types)

Every form control MUST pair with a plain-English `<label for="...">` (zero jargon), set the proper HTML `type` / `inputmode`, display specific inline field errors below the invalid control, and lock the submit button (`disabled` + `aria-busy="true"` + spinner label) while in flight.

---

## 1. Core Input Primitives (10 Variants)

1. **`TextInputField`:** `0.5rem` radius, `1px solid var(--ui-border)`, pure `--ui-ink` value text, readable `--ui-placeholder`, and `2px solid var(--primary-ink)` `:focus-visible` ring.
2. **`PasswordFieldWithToggle`:** Password input paired with an accessible sibling `<button type="button" aria-label="Show password">` morphing Eye / Eye-Off SVG icon.
3. **`CurrencyAndUnitInputGroup`:** Input prefixed with `₱` or suffixed with unit (`sec`, `%`, `views`), `inputmode="decimal"`, `tabular-nums`, validated and rounded server-side.
4. **`DebouncedSearchInput`:** Leading search icon + clear (`X`) button when non-empty + `250ms–300ms` debounce.
5. **`AutoGrowTextarea`:** Multi-line input with optional live character/tag counter and quick-insert helper pills (e.g., `"Insert Required Tags"`).
6. **`NativeOrCustomSelect`:** Accessible `<select>` (or keyboard-navigable custom listbox) with explicit placeholder option.
7. **`SearchableCombobox`:** Type-ahead single/multi-select dropdown with empty `"No matching options"` state.
8. **`CustomCheckboxAndGroup`:** High-contrast `18x18` rounded-sm checkbox (`--ui-primary` checked fill + `--on-primary` checkmark stroke) with full-row clickable `<label>`.
9. **`RadioCardGroup`:** Tactile selectable cards (e.g., Layout Mode: `Blurred Background`, `Center Crop`, `Top & Bottom Split`) highlighting selected card with `2px solid var(--ui-primary)` and subtle `--ui-primary-soft` tint.
10. **`ToggleSwitch`:** `role="switch"` boolean control with clear immediate state label (`Auto-Balance Volume`).

---

## 2. Advanced Pickers, Uploaders & Multi-Step Flows (8 Variants)

11. **`RangeSliderWithNumericSync`:** Slider paired with a direct numeric readout/input (`tabular-nums`) for start/end trim seconds or thresholds.
12. **`DateAndDateRangePicker`:** ISO-safe date/range selector with quick presets (`Today`, `Last 7 Days`, `This Month`).
13. **`TimeDurationInput`:** Clean `MM:SS` or seconds start/end pair validating `end > start` both client- and server-side.
14. **`FileUploadDropzone`:** Dashed border drop area displaying allowed formats & max size (`MP4, MOV up to 500 MB`), selected filename/size preview, upload progress bar, and server-side MIME/size verification.
15. **`ImageWatermarkPicker`:** Thumbnail preview box (`aspect-ratio: 1 / 1`) with position selector (`Top Right`, `Top Left`, `Bottom Right`, `Bottom Left`) and remove/replace button.
16. **`SectionedFormCard`:** Long forms divided into logical 2–4 field sections with clean subheadings and `<hr>` dividers (never an undivided 12-field wall).
17. **`MultiStepFormWizard`:** Numbered step header (`1. Details` → `2. Rules` → `3. Review`) validating each step before advancing while preserving entered values on `Back`.
18. **`InlineValidationSummary`:** Per-field `.text-danger` message (`aria-describedby`) plus a polite top alert (`role="alert"`) if a server-side submission fails.
