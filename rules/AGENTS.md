# KEITH MASTER KIT — CORE ENGINEERING, ZERO-CONFLICT CSS & ANTI-AI-ERROR RULES (v2.0.0)

`KIT_SOURCE` = `c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit`
- Reference Template (67 HTML pages, CSS, JS, 45 vendors): `KIT_SOURCE/reference-template/bootstrap-5-dashboard-pro/`
- Component Catalog & Locked Theme Bridge: `KIT_SOURCE/component-catalog/`
- Automated Project Hygiene Guard: `python "KIT_SOURCE/scripts/audit_project_hygiene.py" <project_dir>`

---

## 1. SIMPLE WORDING, ZERO JARGON & ZERO SAMPLE DATA

- **Chat Language:** Reply in the language the user writes in (English or Filipino/Taglish) unless specified.
- **Code, Commits & UI Copy:** Always write identifiers, comments, commits, and UI labels in **simple, plain English**.
- **Zero Jargon / Zero AI Slop:** Never use corporate/technical buzzwords in UI labels (*"Projected CPM"*, *"Ledger"*, *"Telemetry"*, *"LUFS"*, *"Threshold Parameters"*, *"Sovereign Space"*). Use everyday words: `"Total Earnings"`, `"Total Views"`, `"Pay per 1,000 Views"`, `"Cut Video"`, `"Save"`, `"Delete"`, `"Ready"`, `"Pending"`, `"No records yet."`
- **Strict Zero Sample / Dummy Data:** Never seed, pre-fill, or hardcode sample records, fake names, fake chart data, "Generate Sample" buttons, or template leftovers (`Lorem ipsum`, `Dompet`, `DexignLab`, `John Doe`) unless explicitly requested. Start every new app **100% empty** (`0` counts, `₱0.00` totals) with a clear `EmptyState` (`"No campaigns yet."` + `"Add Campaign"`). Format currency in `₱` (PHP).

---

## 2. SINGLE REUSABLE DESIGN SOURCE & MANDATORY UI KIT PANEL

- **New Web Apps:** Always reuse **Bootstrap 5 Dashboard Pro** (`#main-wrapper`, `.nav-header`, `.header`, `.dlabnav`, `.content-body`, `.footer`), load `08-COMPACT-PURE-CONTRAST-OVERRIDE.css` (`html { font-size: 13px }` + token-driven `#000000`/`#ffffff` contrast), and **ALWAYS include the complete Right-Side UI Kit Settings Panel (`js/demo.js` + `js/styleSwitcher.js` — `.sidebar-right` & `.dlab-demo-panel`)** on every shell page.
- **Existing Non-Bootstrap Projects:** Match the established UI stack (e.g., Tailwind/shadcn) unless asked to migrate.

---

## 3. ZERO-CONFLICT 3-LAYER CSS RULE (PREVENTS AI CSS WARS)

Never let AI-written styles fight the 30,939-line template stylesheet:
1. **Layer 1 — `style.css` (READ-ONLY Vendor Base):** Never edit.
2. **Layer 2 — `08-COMPACT-PURE-CONTRAST-OVERRIDE.css` (LOCKED Kit Theme Bridge):** Copied untouched from `KIT_SOURCE/component-catalog/`. It is the **ONLY** stylesheet allowed to target Bootstrap/Dompet classes and `[data-*]` theme attributes via `--kit-*` and `--on-*` tokens.
3. **Layer 3 — Project `app.css` (`.app-*` Namespace ONLY):**
   - **FORBIDDEN in `app.css`:** Bare HTML tags (`body`, `h1..h6`, `a`, `label`, `table`), Bootstrap/template classes (`.card`, `.btn*`, `.badge*`, `.form-*`, `.dlabnav`, `.header`, `[data-*]`), raw `#hex` colors, and `!important`.
   - **ALLOWED in `app.css`:** Custom `.app-*` domain classes using `var(--kit-surface)`, `var(--kit-surface-subtle)`, `var(--kit-border)`, `var(--kit-ink)`, `var(--kit-ink-muted)`, `var(--primary)`, `var(--on-primary)`, `var(--primary-ink)`.
4. **FORBIDDEN in HTML/EJS/Blade/JSX:** `text-dark`, `text-black`, `bg-white`, `bg-light`, inline `style="color:...; background:..."`, and `javascript:void(0)`. Use `.kit-subtle-box`, `.kit-muted`, and `<button type="button">`.

---

## 4. CLEAN CODEBASE ORGANIZATION (SIGNAL OVER BLOAT)

1. **Purpose-Only File Header (2–3 lines):** State file responsibility at the top of each source file. **Never** put volatile `.env` values (port numbers, exact package versions) in file headers where they go stale.
2. **Section Dividers When Needed:** Group files `80+` lines into clear labeled sections (`// === 1. IMPORTS ===`); keep short files naturally concise without banner padding.
3. **Smart Constants (No Indirection Bloat):**
   - Extract **magic numbers, limits, durations, paths, shared status maps, and API/validation error messages** into `UPPER_SNAKE_CASE` constants.
   - Keep **one-off static UI labels** (`<button type="submit">Save Campaign</button>`) directly readable in templates unless building a multi-language (`i18n`) app.
4. **Strict Import Order:** (1) Built-in modules → (2) Third-party packages → (3) Internal modules → (4) Constants/config.
5. **Comments & Dead Code:** Comment *why*, never *what*. Delete all `console.log`/`dd()` debug lines, commented-out code, unused imports, and resolved `TODO`s before finishing.

---

## 5. MASTER ANTI-AI-ERROR GUARDRAILS (20 COMMON AI MISTAKES BLOCKED)

| Common AI Mistake | Mandatory Rule |
|---|---|
| Global tag/Bootstrap overrides + `!important` in `app.css` | Strictly scope `app.css` to `.app-*` using `--kit-*` tokens; zero `!important`. |
| `text-dark` / `bg-white` / `bg-light` breaking Dark Mode | Banned in markup; use `.kit-subtle-box`, `.kit-muted`, or `.badge.light`. |
| Dark Mode + `color_1` turning sidebar/header text black-on-dark | Handled by `--on-sidebar` / `--on-header` / `--on-nav-header` tokens in locked bridge. |
| `#fff` text on light/yellow/white `data-primary` buttons | Bind solid primary fills to `var(--on-primary)` and links/outlines to `var(--primary-ink)`. |
| Blanket `svg path { fill }` wiping out multi-color brand logos | Style only `.svg-title-path` or `currentColor` icons; keep brand marks intact. |
| Dual `localStorage` vs `demo.js` cookie resetting theme | Use `demo.js` cookies (`getCookie('version')` / `setCookie`) as single source of truth. |
| Vague identifiers (`data`, `items`, `temp`, `res`, `Box1`) | Domain-specific `camelCase`, `is/has/can/should`, `handle*`, `PascalCase`. |
| Unlocked submit buttons allowing duplicate POSTs | Lock in-flight buttons (`disabled` + `aria-busy="true"` + spinner text). |
| Missing `EmptyState` / `Error` / `Loading` UI states | Implement all states on every data view and form. |
| Floating-point money math (`0.1 + 0.2`) or client-sent totals | Compute money server-side in integer centavos or `DECIMAL(12,2)` inside DB transactions. |
| SQL string interpolation, N+1 loops, unindexed FKs | Prepared statements only, eager loading, explicit FK `ON DELETE` + indexes, UTC dates. |
| Empty `catch (e) {}` or missing `.env` validation | Validate required `.env` at startup; log errors server-side and return clean user messages. |
| Unvalidated uploads or hard-deleted financial rows | Validate MIME + max bytes + safe generated name; soft-void financial records with reason. |
| Destructive DB or live VPS edits without backup/check | Require approval + timestamped `.sql`/`.bak` backup + `nginx -t` before reload. |
| Claiming "tested" without running checks | Run real syntax + hygiene checks (`node --check` / `php -l` + `audit_project_hygiene.py`). |

---

## 6. EXECUTION, VERIFICATION & VERSIONING

- Deliver complete end-to-end code (routes, validation, DB, UI states). Write `docs/plans/YYYY-MM-DD-<slug>.md` only for new systems, multi-module features, or `/plan`.
- Run fast syntax checks + `audit_project_hygiene.py` before finishing; never claim unexecuted tests passed.
- Keep projects in `projects/`, temp scripts in `scratch/`, backups in `archives/`. Follow SemVer (`MAJOR.MINOR.PATCH`), Conventional Commits, and `?v=X.Y.Z` static asset cache busting.
