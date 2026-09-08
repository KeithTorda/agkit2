# AG Kit v2 — Changelog

## v2.2.2 (2026-09-08) — Document Generation Gate, CSS Invariant Audit & Verification Harness

### 1. Document Generation Gate & Verification (`/see-doc`, `document-generation`)
- **Document Generation Skill (`skills/document-generation`)**:
  - Comprehensive standards for downloadable artifacts: spreadsheet exports (CSV, XLSX), print & official PDFs (receipts, certificates, invoices, official forms), and editable Office documents (DOCX).
  - Enforces official form bounds, margin compliance, embedded vector typography, and currency/precision formatting.
- **Visual Document Inspection (`/see-doc`, `skills/see-doc`)**:
  - Automated PDF rendering and verification harness (`scripts/doc_verify.py`).
  - Verifies page size, font embedding, glyph survival, edge clearance, and visual diffing against blank government templates.
- **Core Protocol & Code Rules Update**:
  - `code-rules.md` & `core-protocol.md`: Added Step 8.3 document generation verification gate. Downloaded documents must be inspected before calling work done.

### 2. Strict CSS Quality Invariant Audit (`scripts/css_audit.py`)
- **Automated CSS Invariant Audit**:
  - Integrated into `checklist.py` P1 Code Quality required checks.
  - Strictly detects and fails on `!important` declarations, inline hardcoded colors, undefined `var()` tokens, duplicate token collisions outside theme selectors, and conflicting cross-file property overrides.

### 3. UI Verification Engine (`scripts/ui_verify.py`)
- **Automated Verification Contract Checker**:
  - Audits `.agents/verify/<task-slug>/` disk artifacts for `verdict.json`, `after.png`, `mobile-after.png`, and `before.png`.
  - Enforces mandatory breakpoint coverage (`[390, 768, 1440]`), 0 console errors, and pass/skipped status before tasks are signed off.

### 4. Test Suite & Catalog Expansion
- **Test Toolkit (`scripts/tests/test_toolkit.py`)**:
  - Expanded test suite to 22 automated tests covering legacy directory checks, secret scanning bounds, and token ratchets.
- **Catalogs & References (`quick-reference.md`, `AG_KIT_SLASH_COMMANDS.md`)**:
  - Re-indexed 15 primary workflow commands, 34 domain skills, and 27 verification scripts.

---

## v2.2.1 (2026-09-07) — Evidence-on-Disk Verification, Audience Design System & Token Ratchets

### 1. Evidence-on-Disk Verification Gate Contract
- **Durable Disk Artifacts (`browser-verification`, `/see`, `/fix-ui`)**:
  - Verification reports in responses are treated as claims; proof must now be persisted to disk under `<project>/.agents/verify/<task-slug>/`:
    - `verdict.json`: Machine-readable audit artifact recording route, tested breakpoints (`[390, 768, 1440]`), console error count, failed network request count, interaction test status, token violations, overall status (`pass`, `fail`, or `skipped` with reason), and unverified items.
    - `after.png` (1440px desktop) and `mobile-after.png` (390px mobile).
    - `before.png` (mandatory on repairs as irrefutable evidence of the defect before remediation).
- **Specialist Agent Done Criteria**:
  - `agents/frontend-specialist.md`: Updated Done gate 2 to mandate that `.agents/verify/<task-slug>/verdict.json` exists with status `pass` (or `skipped` stating the blocked precondition).
  - `agents/mobile-developer.md`: Updated Done gate 3 to mandate simulator/device screenshots and `verdict.json` in `.agents/verify/<task-slug>/`.

### 2. Audience- & Domain-Driven Design Reference System
- **`skills/design-spec/collection.md`**:
  - Complete restructuring into 12 domain- and audience-specific sections: Public Service/Civic, Money/Fintech/Billing, Retail/Storefront/POS, Marketplace/Classifieds, Health/Clinic, Education/Learning, Logistics/Delivery, Booking/Hospitality, Work Tools/Productivity, Media/Editorial, Consumer Apps, and Developer Products (placed last).
  - Prevents LLM design bias of defaulting to dark-mode developer tools when building portals, healthcare, public services, or e-commerce.
- **`skills/design-spec/fetchable.md`**:
  - Split out published `DESIGN.md` fetch URLs and slug references into a dedicated reference file for when browsing tools are available.
- **`skills/frontend-design/SKILL.md` (§0.C)**:
  - Updated design read guidelines to strictly require selecting references tailored to audience and domain before writing code.
  - Linked `agents/frontend-specialist.md` directly to `design-spec/collection.md` on every design read.

### 3. Context Token Ratchet & Skill Core Slimming
- **`skills/browser-verification/troubleshooting.md`**:
  - Split out browser actuation rules, Chrome preconditions, and the 7 common verification pitfalls from `browser-verification/SKILL.md` to conserve context window tokens.
- **`scripts/tests/test_toolkit.py`**:
  - Added architectural token ratchet `test_read_now_skill_cores_do_not_grow()` enforcing an 8 KB cap on all Read-now (L2) skill cores with tracked historical debt pinned.
  - Added test suite count to 20 automated regression tests.

---

## v2.2.0 (2026-09-07) — Rules Update, Fix-at-Source Invariant, UI Repair & Naming Enforcement

### 1. Global Rules Evolution
- **`core-protocol.md` (v2.2.0)**:
  - Token conservation: Split agent loading into mandatory **Read now** (max 3 files) and conditional **Read when** paths to drastically reduce context window overhead.
  - Added **Build vs Repair** distinction to Step 7: new features run Build steps; fixes run systematic Repair steps (reproduce, locate, identify root cause, fix at source, verify).
  - Added `/fix-ui` command into Step 3 and Step 8 for UI repair tasks.
- **`code-rules.md`**:
  - **Fix at the source (Required)**: Strict ban on layout overrides (`!important`, inline hacks, wrapper elements to win cascade, child margin hacks). Prescribes `ui-repair` (`/fix-ui`) and `css-architecture`.
  - **Unique, searchable names (Required)**: Enforces `<domain>-<role>.<ext>` (`invoice-table.tsx`, `invoice-table.css`), strictly banning bare generic filenames (`utils.ts`, `helpers.ts`, `styles.css`, `types.ts`, duplicate `index.*`). Exported symbols must be domain-prefixed; CSS classes component-prefixed.
- **`request-routing.md`**:
  - Added explicit `REPAIR` routing category mapping bugs/alignment/layout issues to specialist Repair workflows and UI defects to `/fix-ui`.
  - Added `/fix-ui` to COMMAND catalog.
- **`quick-reference.md`**:
  - Catalog rebuilt to index 17 agents, 44 skills, 14 slash commands, and updated scripts.

### 2. Specialist Agents (All 17 Agents -> v2.2.0)
- Upgraded every specialist agent with explicit `Read now` (immediate required skills) and `Read when` (conditional skills) headers.
- Structured agent bodies into dual execution modes: **Build (new work)** and **Repair (existing work that is wrong)** with explicit root-cause taxonomy and verification gates.

### 3. New Skills & Architectural References
- **`fix-ui` (`/fix-ui`)**: Systematic UI repair workflow that captures headless browser renders, locates container layout modes, isolates 1 of 8 root causes, and corrects the parent constraint.
- **`ui-repair`**: Deep dive into layout defect root causes and components constraints (`components.md`).
- **`css-architecture`**: Single token source of truth, CSS cascade layers (`@layer`), co-located component styling, and plain CSS/SCSS mode for Laravel Blade (`plain-css.md`).
- **Modular Skill Extensions**:
  - `design-spec/tokens-reference.md`: Canonical schema and tokens reference.
  - `frontend-architecture/structure-reference.md`: Feature folder and state-tier structural reference.
  - `frontend-design/`: Modularized into `app-ui.md`, `design-systems.md`, `marketing-layout.md`, and `motion.md`.

### 4. Verification Scripts & Gates
- **`scripts/naming_check.py`**: Automated static checker detecting banned generic filenames (`utils.*`, `helpers.*`, `types.*`, `styles.*`) and bare duplicate index files.
- **`scripts/checklist.py`**: Integrated `naming_check.py` into P1 Code Quality checks.
- **`scripts/tests/test_toolkit.py`**: Expanded to 19 automated tests covering scanner regex boundaries, path resolution, and repository test configurations.

---

## v2.1.0 / Initial Install (2026-09-05) — Rebuild from original ag-kit

Based on vudovn/ag-kit. Rebuilt for a global Antigravity install on this machine. Full audit: `ag-kit-audit.md`; policies every file follows: `DECISIONS.md` (both next to this file).

## Layout
- Plugin renamed to `ag-kit-v2` (the old `ag-kit` plugin is disabled in `~/.gemini/config/config.json`; delete its folder when convenient).
- Rules live only in `~/.gemini/config/rules/` (6 files, same names as before, rewritten). The duplicate `rules/` inside the plugin is gone (it was injected twice).
- `~/.gemini/GEMINI.md` is a 1 KB entry file. Always-on context is now ~7 KB (was ~9–10 k tokens with pointers).
- `workflows/` removed (deprecated in Antigravity). The 13 workflows became 11 slash-command skills: `/brainstorm /create /plan /debug /test /verify /deploy /orchestrate /enhance /remember /status` (`/preview` dropped with its broken script; `/coordinate` merged into `/orchestrate`).
- Every `.agents/agent|skills|scripts/` path became an absolute `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/...` path (93 broken references before).
- All files LF, UTF-8.

## Policies (one definition each — see DECISIONS.md §3)
- Questions: ask only when the answer changes the build; 1–3 questions for new apps/multi-file work; proceed on simple tasks. No 3-question floor, no re-asking after "proceed".
- One announcement line (`🤖 @agent · skills: …`), informational only.
- One phase model: ANALYZE → PLAN → BUILD → VERIFY (defined in `code-rules`).
- Plan file: `docs/plans/{task-slug}.md`, required only for NEW APP / COMPLEX.
- Verification: `checklist.py` gates on required checks only (security high+, lint, type check, tests); everything else is advisory. Auto-fix required failures; report advisory ones.
- `DESIGN.md` is the single design gate and the token source of truth (`design-spec` owns the format; `frontend-design` consumes it).
- Purple / shadcn / Inter / glass etc. are anti-default heuristics, not bans; `DESIGN.md` overrides; scripts warn, never fail.
- Memory is per project (`<project>/.agents/memory/MEMORY.md`), read only if it exists.

## Agents (20 → 17)
- Deleted: `game-developer`; `product-owner` merged into `product-manager`; `qa-automation-engineer` merged into `test-engineer`.
- `frontend-specialist` 26 KB → 6 KB (design judgment moved to the `frontend-design` skill; contradictions removed). `project-planner` 15 KB → 5 KB. `mobile-developer` 13 KB → 5 KB.
- `orchestrator` holds the canonical file-ownership table for all 17 agents.
- Frontmatter: `name`, `description` (ending with `Triggers on: …`), `skills`, `version` — `tools`/`model` dropped (ignored by Antigravity).

## Skills (47 → 40)
- Deleted: game-development (10), rust-pro, intelligent-routing (→ `request-routing` rule), behavioral-modes (→ `core-protocol`), code-review-checklist, code-review-graph, documentation-templates, context-compression, batch-operations, skillify.
- Merged: simplify-code → clean-code; coordinator-mode → parallel-agents; tdd-workflow + webapp-testing → testing-patterns; geo-fundamentals → seo-fundamentals; bash-linux + powershell-windows + server-management → shell-ops; deployment-procedures → `/deploy`; api-patterns and database-design sub-files inlined.
- `frontend-design/SKILL.md` 89 KB → 35 KB; `redesign.md` folded into it; style files marked as explicit exceptions.
- Tech refresh to September 2026: Next.js 16 / React 19.2 compiler-first, Tailwind v4 (`@custom-variant dark`), `motion/react`, TanStack Query instead of SWR, Better Auth (Lucia deprecated), `redis.asyncio`, httpx `ASGITransport`, Prisma 7, UUIDv7, ESLint 9 flat config, Expo SDK 54+/Reanimated 4/FlashList v2, iOS 26 / Android 16 baselines, current AI-crawler names, IETF RateLimit headers.

## Scripts
- `validate_kit.py` rewritten for this layout (0 errors); manifest/lock/dependency-graph machinery removed; `auto_preview.py` (broken) and `convert_rules.py` (dead) deleted; `build_quick_reference.py` added.
- `validation_runner.py`: only required checks gate success. `lint_runner.py`: runs ruff/mypy only if installed. `test_runner.py`: `sys.executable`. `ux_audit.py`: purple is an advisory warning with a `DESIGN.md` override. `react_performance_checker.py`: memoization check removed. `lighthouse_audit.py`: no `--no-sandbox`.
- `tests/test_toolkit.py`: 12 tests, all passing.

## Maintaining the kit
1. Edit agents/skills.
2. `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/validate_kit.py`
3. `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/build_quick_reference.py --write`
4. `python C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/scripts/tests/test_toolkit.py`
