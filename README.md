# Keith Master Kit (`agkit2` / `keith-agkit` v5.0.0)

Stack-agnostic Antigravity plugin, engineering rulebook, **First-Party Component & Screen Type Catalog**, and **Zero-Conflict Token & Theme Settings Engine** — built to work cleanly across **ANY UI stack** (Tailwind CSS + shadcn/ui, React / Next.js, Laravel Blade / Livewire, Vue / Svelte, Vanilla CSS, or Bootstrap 5) with **zero third-party template bloat**.

---

## What's Inside

1. **Stack-Agnostic First-Party Component Type Catalog (`component-catalog/00`–`07`):**
   - **18 Screen Archetypes** (Overview Dashboards, Tabbed Ledgers, CRUD Directories, Studio Workspaces, Multi-Step Wizards, POS/Checkout, Printable Official Invoices, Auth & HTTP Error Screens)
   - **38+ Component Types & Variants** (KPI Stat Cards, Charts, Timelines, Data Tables, Currency/Combobox/Dropzone Inputs, Soft Status Badges, Modals, Drawers, Toasts, Tabs)
2. **Portable First-Party UI Token & Settings Engine (`ui-kit/`):**
   - `keith-ui-tokens.css` — Native `@layer tokens, base, components, utilities;` CSS Custom Properties (`--ui-*`, `--on-*`, `--primary-ink`) verified `>= 4.5:1` WCAG AA across **all 15 color presets** in Light & Dark modes.
   - `keith-ui-settings.js` — Zero-jQuery Vanilla ES6 Right-Side Live Theme & Layout Settings Drawer (`Light/Dark`, `15 Color Presets`, `Vertical/Horizontal`, `Sidebar Mode`, `Font`, `Reset`).
3. **Zero-Conflict Engineering & Anti-AI-Error Rules (`rules/` + `docs/`):**
   - Simple everyday English copy, zero jargon, strict zero sample/dummy data (`0` / `₱0.00` + `EmptyState`).
   - Strict domain-specific naming, clean file headers/sections, smart constants, exact server-side money math (`DECIMAL(12,2)` / centavos), fail-fast `.env` checks, and Contabo VPS backup safety.
4. **Automated Validators (`scripts/`):**
   - `validate_keith_kit.py` — Validates plugin manifest, SemVer sync, rule byte budgets (`< 12 KB`), subagent tool grants, catalog completeness, and zero third-party template leftovers.
   - `audit_project_hygiene.py` — Audits any app project for CSS `!important`/hex/selector conflicts, Dark-Mode-breaking hardcoded color classes, `javascript:void(0)`, and placeholder leftovers.

---

## Folder Structure

```text
keith-agkit/
├── plugin.json                              # Antigravity plugin manifest (v5.0.0)
├── VERSION                                  # Semantic version (5.0.0)
├── CHANGES.md                               # Release history
├── install.ps1                              # Validator + safe backed-up plugin installer
├── ui-kit/                                  # First-party portable token & settings engine
│   ├── keith-ui-tokens.css                  # @layer semantic tokens + 15 WCAG AA presets
│   └── keith-ui-settings.js                 # Vanilla ES6 right-side theme & layout drawer
├── component-catalog/                       # Stack-agnostic component & screen blueprints
│   ├── 00-MASTER-SCREEN-AND-COMPONENT-TYPES.md
│   ├── 01-DESIGN-TOKENS-CONTRAST-AND-THEMES.md
│   ├── 02-APP-SHELLS-SIDEBARS-AND-SETTINGS-PANEL.md
│   ├── 03-CARDS-KPIS-CHARTS-AND-WIDGETS.md
│   ├── 04-DATA-TABLES-LEDGERS-AND-FILTERS.md
│   ├── 05-FORMS-INPUTS-PICKERS-AND-WIZARDS.md
│   ├── 06-BUTTONS-BADGES-MODALS-ALERTS-AND-NAVS.md
│   └── 07-AUTH-INVOICE-POS-INBOX-AND-SYSTEM-PAGES.md
├── rules/                                   # Clean Antigravity rules (<11 KB each, 0 warnings)
│   ├── AGENTS.md
│   ├── rule-01-design-and-css-system.md
│   ├── rule-02-code-naming-and-states.md
│   ├── rule-03-security-db-and-vps.md
│   └── rule-04-planning-and-integration.md
├── skills/
│   ├── ui-system-builder/SKILL.md
│   ├── laravel-fullstack/SKILL.md
│   └── vps-safe-deploy/SKILL.md
├── agents/
│   ├── ui-system-builder.md
│   ├── fullstack-engineer.md
│   ├── database-architect.md
│   └── vps-devops.md
├── scripts/
│   ├── validate_keith_kit.py
│   └── audit_project_hygiene.py
└── docs/
    ├── GEMINI.md                            # Synced global ~/.gemini/GEMINI.md (v3.0.0)
    └── AI-ERROR-REGISTRY.md                 # 24 common AI coding errors & preventive rules
```

---

## Validation & Installation

```powershell
# 1. Validate kit structure, byte budgets, tokens & catalog (read-only)
.\install.ps1 -Check

# 2. Install into ~/.gemini/config/plugins/keith-agkit (with timestamped backup)
.\install.ps1
```
