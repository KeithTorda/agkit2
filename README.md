# Keith Master Kit (`agkit2` / `keith-agkit` v4.0.0)

Unified Antigravity plugin, engineering rule system, and **reusable UI component library** powered by **Bootstrap 5 Dashboard Template Pro** (`https://starcodekh.github.io/Bootstrap-5-Dashboard-Template-Pro/`).

Built to replace `agkit2` by merging:
1. **Keith's Master Coding Rules (`v2.2.0`) & Anti-Jargon Copy Rules** — strict domain-specific naming, direct operational English UI labels, accessible semantic buttons, responsive sidebars, WCAG AA contrast, GPU-composited micro-interactions, database backup safety, and Contabo VPS deployment checks.
2. **Clean Antigravity Plugin Architecture** — self-contained inside one plugin bundle (`rules/`, `skills/`, `agents/`, `plugin.json`) with valid frontmatter, explicit subagent `tools:` grants, and zero scattered orphan rules.
3. **Zero-Guesswork Reusable UI Library** — full downloaded template (67 HTML pages, 45 vendor libraries, 10 icon sets, 15 color presets, Light & Dark modes) plus an 8-part itemized `component-catalog/` so every future app reuses proven screens and components immediately.

---

## Folder Structure

```text
projects/keith-agkit/
├── plugin.json                              # Native Antigravity plugin manifest
├── VERSION                                  # Semantic version (1.0.0)
├── install.ps1                              # Validator + safe timestamped plugin installer
├── scripts/
│   └── validate_keith_kit.py                # Automated validator for rules, frontmatter, tools, and catalog
├── rules/                                   # Clean, conflict-free Antigravity rules (<6 KB each)
│   ├── AGENTS.md                            # Core always-on rule (language, template mandate, verification, SemVer)
│   ├── rule-01-template-design-system.md    # UI glob rule (Bootstrap 5 Pro shell, tokens, responsive sidebar, a11y)
│   ├── rule-02-code-naming-and-states.md    # Code glob rule (strict naming, reusable components, loading/empty/error states)
│   ├── rule-03-security-db-and-vps.md       # Backend/SQL/VPS glob rule (RBAC, server money totals, DB & Nginx safety)
│   └── rule-04-planning-and-integration.md  # Model-decision rule (docs/plans/ + optional cross-system outbox sync)
├── component-catalog/                       # Complete itemized breakdown & copy-ready snippets of all 67 pages
│   ├── 00-INDEX-AND-PAGE-MAP.md             # Domain-to-page mapping + full 67-file inventory
│   ├── 01-THEME-TOKENS-AND-PALETTES.md      # Light/Dark CSS tokens + 15 primary brand presets (color_1..15)
│   ├── 02-APP-SHELL-SIDEBAR-HEADER.md       # Sanitized #main-wrapper, .nav-header, .header, .dlabnav, .content-body
│   ├── 03-CARDS-KPI-AND-WIDGETS.md          # .invoice-card, .widget-stat, .widget-timeline, EmptyState & Skeleton
│   ├── 04-TABLES-DATATABLES-AND-FILTERS.md  # .card-tabs.style-1, CRUD tables, .dataTablesCard, sharp row actions
│   ├── 05-FORMS-PICKERS-AND-WIZARDS.md      # .basic-form, validation, checkboxes, Select2, SmartWizard steps
│   ├── 06-BUTTONS-BADGES-MODALS-ALERTS.md   # Solid/light/sharp buttons, .badge.light pills, centered & confirm modals
│   └── 07-AUTH-INVOICE-ECOM-AND-ERRORS.md   # .authincation Login/Register, Printable Invoice, Product Grid, 400–503 pages
├── skills/
│   ├── bootstrap-pro-ui/SKILL.md            # UI assembly workflow for HTML/Blade/PHP and React/Next.js
│   ├── laravel-fullstack/SKILL.md           # Laravel 11/12 + Bootstrap 5 Pro conventions
│   └── vps-safe-deploy/SKILL.md             # Contabo VPS safe backup, syntax check, and deployment runbook
├── agents/                                  # Subagents with explicit read/write/command tool grants
│   ├── ui-template-builder.md
│   ├── fullstack-engineer.md
│   ├── database-architect.md
│   └── vps-devops.md
└── reference-template/
    └── bootstrap-5-dashboard-pro/           # Complete downloaded StarCodeKH Bootstrap 5 Dashboard Template Pro
```

---

## Validation & Installation

```powershell
cd "c:\Users\Keith\Desktop\CONTABO VPS\projects\keith-agkit"

# 1. Validate structure, frontmatter, subagent tools, and template catalog (read-only)
.\install.ps1 -Check

# 2. Install into ~/.gemini/config/plugins/keith-agkit (with automatic backup)
.\install.ps1
```
