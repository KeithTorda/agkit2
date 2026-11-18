---
trigger: glob
globs: "**/*.ts, **/*.tsx, **/*.js, **/*.jsx, **/*.mjs, **/*.php, **/*.py, **/*.vue, **/*.svelte, **/*.blade.php, **/*.css, **/*.scss, **/*.ejs"
description: Enforces strict domain-specific naming, balanced constants, clean file structure, single-responsibility functions, and complete UI states.
---

# RULE 02 — STRICT NAMING, CLEAN CODE ARCHITECTURE & COMPLETE STATES

## 1. Strict Domain-Specific Naming

Never use vague placeholder identifiers (`data`, `items`, `list`, `arr`, `obj`, `temp`, `val`, `res`, `info`, `thing`, `handleData`, `processItems`, `Component1`, `Modal1`, `.box1`, `.custom`).

- **Variables & Functions (`camelCase`):** `registeredPatients`, `pendingInvoices`, `selectedBranchId`, `productSearchQuery`, `calculateInvoiceSubtotal()`, `fetchActiveSubscriptions()`.
- **Booleans (`is` / `has` / `can` / `should`):** `isSidebarCollapsed`, `isInvoiceSubmitting`, `hasSufficientStock`, `canApprovePayout`.
- **Event Handlers (`handle*`):** `handleCustomerRegistration`, `handleDeleteCampaignConfirm`, `handleThemeToggle`.
- **Components, Classes & Types (`PascalCase`):** `PatientRegistrationForm`, `InventoryStockTable`, `DeleteInvoiceModal`.
- **Constants (`UPPER_SNAKE_CASE`):** `UPLOAD_MAX_FILE_SIZE_BYTES`, `DEFAULT_PAGE_SIZE`, `PHILIPPINE_VAT_RATE`.
- **App CSS Classes (`.app-*`):** Prefix custom project CSS classes with `.app-` (`app-phone-preview`, `app-rule-notes`) so they never collide with Bootstrap or template classes.
- **Consistent Domain Terms:** Use one term per concept across DB, API, and UI (never mix `patient`, `client`, and `customer` for the same entity). Short loop/callback params (`id`, `index`, `event`, `error`) are fine only in tight, unambiguous local scopes.

## 2. Smart Constants & File Organization (Zero Bloat, Zero Magic Values)

1. **Purpose-Only File Header (2–3 lines):** State the file's responsibility at the top. **Never** hardcode volatile `.env` values (ports, package versions, hostnames) in file header comments.
2. **Section Dividers Where Useful:** Use clear section headers (`// === 1. IMPORTS ===`) in files `80+` lines long; keep small modules naturally concise.
3. **Smart Constants (Avoid Both Magic Numbers and Indirection Bloat):**
   - **DO extract** magic numbers, byte/time limits, rates, storage keys, status maps, and shared validation/API error messages into named `UPPER_SNAKE_CASE` constants or a `constants` module.
   - **DO NOT wrap** every one-off static template label (`Save`, `Cancel`, `Add Campaign`) in JS variables on single-language apps — keep static labels readable inline in markup unless implementing multi-language `i18n`.
4. **Single-Responsibility Functions:** Keep functions focused on one job (`<40` lines when practical). Keep business math (totals, VAT, rule checks, permissions) in services/server modules, never inside view templates.
5. **Import Order:** (1) Built-in modules → (2) Third-party packages → (3) Internal modules → (4) Constants/config.

## 3. Complete Screen States & Zero Sample Data

Every data view and form must start **100% empty of sample/dummy data** (unless test data is explicitly requested) and handle all states with plain English:
1. **Loading:** Geometry-matching `LoadingSkeleton` or button/table spinner (zero layout jump).
2. **Empty (Default Initial State):** Clean `EmptyState` inside `.card-body` (`"No campaigns yet."` + `"Add Campaign"` CTA).
3. **Error:** Plain, actionable message (`"Could not save changes. Try again."`) while logging technical details server-side.
4. **Success:** Clear feedback banner/toast (`"Campaign saved."`).
5. **Forms:** Plain `<label for="...">`, proper input `type`, inline field errors, debounced search inputs (`250ms–300ms`), and locked submit button (`disabled` + `aria-busy="true"`) while submitting.

## 4. Pre-Finish Cleanliness Checklist

- Zero `console.log` / `dd()` / `var_dump` debug lines, commented-out dead code, unused imports, or resolved `TODO`s.
- Zero leftover placeholder text (`Lorem ipsum`, `John Doe`, `Acme Corp`, `example@email.com`).
- Comments explain non-obvious *why* decisions, never restate *what* the code already says.
