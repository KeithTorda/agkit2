# KEITH MASTER KIT — STACK-AGNOSTIC UI, ZERO-CONFLICT CSS & ANTI-AI-ERROR RULES (v5.0.0)

`KIT_SOURCE` = `c:/Users/Keith/Desktop/CONTABO VPS/projects/keith-agkit`
- First-Party Component & Screen Type Catalog (`00`–`07`): `KIT_SOURCE/component-catalog/`
- Portable Token & Theme Settings Engine: `KIT_SOURCE/ui-kit/keith-ui-tokens.css` & `keith-ui-settings.js`
- Automated Project Hygiene Guard: `python "KIT_SOURCE/scripts/audit_project_hygiene.py" <project_dir>`

---

## 1. SIMPLE WORDING, ZERO JARGON & ZERO SAMPLE DATA

- **Chat Language:** Reply in the language the user writes in (English or Filipino/Taglish) unless specified.
- **Code, Commits & UI Copy:** Always write identifiers, comments, commits, and UI labels in **simple, plain English**.
- **Zero Jargon / Zero AI Slop:** Never use corporate/technical buzzwords in UI labels (*"Projected CPM"*, *"Ledger"*, *"Telemetry"*, *"LUFS"*, *"Threshold Parameters"*, *"Sovereign Space"*). Use everyday words: `"Total Earnings"`, `"Total Views"`, `"Pay per 1,000 Views"`, `"Cut Video"`, `"Save"`, `"Delete"`, `"Ready"`, `"Pending"`, `"No records yet."`
- **Strict Zero Sample / Dummy Data:** Never seed, pre-fill, or hardcode sample records, fake names, fake chart numbers, "Generate Sample" buttons, or placeholder leftovers (`Lorem ipsum`, `John Doe`) unless explicitly requested. Start every new app **100% empty** (`0` counts, `₱0.00` totals) with a clear `EmptyState` (`"No campaigns yet."` + `"Add Campaign"`). Format currency in `₱` (PHP).

---

## 2. STACK-AGNOSTIC UI SYSTEM & COMPONENT CATALOG

- **Any UI Stack Welcome:** Build cleanly in **any UI framework** — Tailwind CSS + shadcn/ui, React/Next.js, Laravel Blade/Livewire, Vue/Svelte, Vanilla CSS (`ui-kit/keith-ui-tokens.css`), or Bootstrap 5. Match existing stacks on existing projects; use the user's preferred stack on new projects.
- **First-Party Component Types (`component-catalog/00`–`07`):** Reuse our 18 screen archetypes and 36+ component types (KPI cards, tabbed status ledgers, CRUD tables, multi-step wizards, dropzones, printable invoices, auth screens) elevated with crisp `#000000` / `#ffffff` contrast and `tabular-nums`.
- **Right-Side Live Theme Settings Drawer:** On admin dashboards and workspace app shells, include the complete right-side Theme & Layout Settings Drawer (`ui-kit/keith-ui-settings.js` or `<ThemeSettingsDrawer />` — Light/Dark mode, 15 WCAG AA color presets, Vertical/Horizontal layout, Sidebar size, Font, and Reset) backed by **one single state store**.

---

## 3. ZERO-CONFLICT TOKEN & LAYER CSS ARCHITECTURE

Prevent AI CSS specificity wars across every stack:
1. **Token Single Source of Truth:** Define surfaces, borders, text ink, and accents once via semantic CSS variables (`--ui-canvas`, `--ui-surface`, `--ui-surface-subtle`, `--ui-border`, `--ui-ink`, `--ui-ink-muted`, `--ui-primary`, `--on-primary`, `--primary-ink`, or Tailwind semantic tokens `bg-card`, `text-foreground`, `bg-primary`, `text-primary-foreground`).
2. **Cascade Layer & Namespace Discipline:**
   - Use `@layer tokens, base, components, utilities;` in custom stylesheets; keep vendor/framework CSS untouched.
   - Scope custom domain styles to `.app-*` (or CSS Modules) consuming `var(--ui-*)` tokens — **zero `!important` wars** and **zero raw `#hex` colors** outside token definitions.
3. **Forbidden in Markup (HTML/JSX/Blade/EJS/Vue):** Unpaired light-only color utilities (`text-dark`, `text-black`, `bg-white`, `bg-light` without dark semantic tokens), inline color `style="..."`, blanket `svg path { fill }` overrides on multi-color logos, and `javascript:void(0)`.

---

## 4. CLEAN CODEBASE ORGANIZATION (SIGNAL OVER BLOAT)

1. **Purpose-Only File Header (2–3 lines):** State file responsibility at the top. **Never** put volatile `.env` values (ports, exact versions) in file headers.
2. **Section Dividers Where Useful:** Group files `80+` lines into clear labeled sections (`// === 1. IMPORTS ===`); keep short files concise.
3. **Smart Constants:** Extract **magic numbers, limits, durations, paths, status maps, and shared API/validation error messages** into `UPPER_SNAKE_CASE` constants. Keep one-off static UI labels directly readable in markup on single-language apps.
4. **Strict Import Order & Dead Code Hygiene:** (1) Built-in → (2) Third-party → (3) Internal → (4) Constants/config. Comment *why*, never *what*. Remove all `console.log`/`dd()` debug lines, commented-out code, and unused imports.

---

## 5. MASTER ANTI-AI-ERROR GUARDRAILS

| Common AI Mistake | Mandatory Rule |
|---|---|
| Global tag/framework overrides + `!important` in `app.css` | Use `@layer` + `.app-*` namespace with semantic CSS variables; zero `!important`. |
| `text-dark` / `bg-white` / `bg-light` breaking Dark Mode | Banned without dark tokens; use semantic surface/ink tokens (`bg-card`, `.ui-subtle-box`). |
| Unreadable `#fff` text on light/yellow/teal primary buttons | Pair solid fills with `--on-primary` and links/outlines/soft badges with `--primary-ink` (`>= 4.5:1`). |
| Competing `localStorage` vs cookie resetting theme settings | Keep one single state store for theme/layout preferences. |
| Vague identifiers (`data`, `items`, `temp`, `res`, `Box1`) | Domain-specific `camelCase`, `is/has/can/should`, `handle*`, `PascalCase`. |
| Missing `EmptyState` / `Error` / `Loading` or double-submit | Implement all states + lock in-flight submit buttons (`disabled` + `aria-busy="true"`). |
| Floating-point money math (`0.1 + 0.2`) or client-sent totals | Compute money server-side in integer centavos or `DECIMAL(12,2)` inside DB transactions. |
| SQL string interpolation, N+1 loops, unindexed FKs | Prepared statements only, eager loading, explicit FK `ON DELETE` + indexes, UTC dates. |
| Empty `catch (e) {}`, missing `.env` check, or raw stack traces | Fail-fast `.env` check at boot; log server-side and return plain client error messages. |
| Destructive DB or live VPS edits without backup/check | Require approval + timestamped `.sql`/`.bak` backup + `nginx -t` before reload. |
| Claiming "tested" without running checks | Run real syntax + hygiene checks (`node --check` / `php -l` / `tsc --noEmit` + `audit_project_hygiene.py`). |

---

## 6. EXECUTION, VERIFICATION & VERSIONING

- Deliver complete end-to-end code. Write `docs/plans/YYYY-MM-DD-<slug>.md` only for new systems, multi-module features, or `/plan`.
- Keep projects in `projects/`, temp scripts in `scratch/`, backups in `archives/`. Follow SemVer (`MAJOR.MINOR.PATCH`), Conventional Commits, and `?v=X.Y.Z` asset cache busting.
