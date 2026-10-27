# AGKIT2 3.2

An agent kit for the **Antigravity IDE**: a small set of rules, 14 focused agents, and 58 skills and slash commands that make the AI build like a senior team. Plans, code and UI follow our own standards. The UI the kit builds looks like a premium ready-made template, not a bare minimal page.

- Source folder: `agkit2` (this repo)
- Installed plugin: `~/.gemini/config/plugins/ag-kit-v2`
- Installed rules: `~/.gemini/config/rules`

---

## Rules

Rules are short, each owns one topic, and they never repeat each other.

| Rule | Loads | What it enforces |
|---|---|---|
| `kit-core` | always | Kit path, rule map, agent and command routing, checks only when asked |
| `rule-01-unified-theme-system` | UI files | One semantic-token design system with Light, Dark and System modes (full text) |
| `rule-01b-theme-quick` | UI files | Rule 01 as a 12-item quick card (Gemini follows short rules better) |
| `rule-02-work-style` | always | English, direct, decide and finish the job, fixed report format, no fake "tests passed", actions that need approval |
| `rule-03-code-standards` | code files | Existing stack first, domain naming, no CSS override hacks, every data screen handles all states, no dead code |
| `rule-04-system-integration` | backend, database and plan files | Option B: separate DB per system, one owner per table, outbox + middleman, webhooks + nightly reconciliation, versioned API |
| `rule-05-planning-and-docs` | always | Every plan saved as `docs/plans/<yyyy-mm-dd>-<slug>.md` in one format; README/API docs minimum |
| `rule-06-security-baseline` | code files | Server-side auth and per-resource permissions, input validation, secrets, money records never hard-deleted, audit trail, uploads |
| `rule-07-template-grade-design` | UI files | Every page looks like a complete premium template (full chrome, depth, realistic demo data, imagery, polish, all states); minimal only on request |
| `quick-reference` | on demand | Generated catalog of agents, skills, commands and scripts |

## Agents

| Agent | Use for |
|---|---|
| `lead` | Big or cross-area tasks: split work, assign agents, agree contracts, integrate, final report |
| `architect` | System design, tech choices, ADRs, Rule 04 integration design, plan reviews |
| `product-planner` | Goals, requirements, acceptance criteria, MVP scope, task plans, milestones, risks |
| `ux-designer` | Flows, sitemap, screen inventory with states, DESIGN.md, Rule 01 token set |
| `frontend-engineer` | Web UI in React/Next.js, Blade, Bootstrap 5, Tailwind; theming; SEO |
| `backend-engineer` | APIs, Laravel/Node services, auth, jobs, webhooks, outbox sync, exports and receipts |
| `database-engineer` | Schema, migrations, indexes, queries, seeds, data ownership |
| `mobile-engineer` | Expo/React Native/Flutter apps, offline sync, device features, store builds |
| `qa-engineer` | Tests, test plans, code review (on request) |
| `debugger` | Root-cause bug fixing and measured performance fixes |
| `security-engineer` | Security review, threat model, permission matrix, authorized pentest |
| `devops-engineer` | VPS/Nginx/PM2/Docker, CI/CD, env, backups, deploy and rollback |
| `docs-writer` | README, guides, API docs, user/admin manuals, handover |
| `explorer` | Read-only codebase mapping, legacy code explanation, feasibility |

Every agent file uses the same template: **Mission, Owns / Does not own, Before starting, How to work, Stack notes, Quality bar, Common mistakes to avoid, Handoff format.**

## Slash commands

| Command | What it does |
|---|---|
| `/create` | Build a new app, page or feature |
| `/enhance` | Extend or change the existing project |
| `/plan` | Write a feature plan to `docs/plans/` |
| `/proplan` | Full system plan set (goals, requirements, architecture, data, API, UX, security, quality, ops, roadmap, risks) |
| `/brainstorm` | Compare approaches and recommend one |
| `/orchestrate` | Run a plan or milestone across several agents |
| `/debug` | Reproduce and fix a bug at its root cause |
| `/fix-ui` | Repair a broken layout or component |
| `/see` `/see-doc` | Inspect a rendered page or generated document (on request) |
| `/test` `/verify` `/review` | Run tests, verify a change, review a diff (on request) |
| `/deploy` | Perform an authorized release |
| `/status` `/remember` | Project status; save project notes |
| `/init-project` | Create the project's `AGENTS.md` facts file (stack, commands, data ownership) |
| `/doctor` `/updatekit` | Check or update the kit installation |

Tests, builds, browser checks and reviews **never run automatically**. They run when you ask.

## Key skills

| Skill | Use |
|---|---|
| `template-ui-blocks` | Copy-ready Bootstrap 5.3 and Tailwind blocks for every Rule 07 page type |
| `laravel-patterns` | Form Requests, Policies, Actions, Resources, jobs, outbox, Blade |
| `bootstrap-patterns` | Bootstrap 5.3 tokens, `data-bs-theme`, React-Bootstrap, admin layouts |
| `ph-business-compliance` | VAT, sales invoices (EOPT), senior/PWD discounts, POS readings, e-invoicing |
| `proplan` / `plan` | System and feature plans |

## Working with Gemini

Gemini 3.x follows short, direct rules and drifts in long chats. The kit is built for that:
- Every rule ends with a short "Before you answer, check" list.
- Plan first, build one step at a time, start a new chat after each milestone.
- Any claim that a command ran must include its output.
- Run `/init-project` once per project so each chat starts with the project facts.

## What the UI looks like

By default every screen follows a Rule 07 recipe:

- **Landing page:** navbar, hero with two CTAs and a visual, trust strip, features, alternating feature rows, stats band, testimonials, pricing, FAQ, final CTA, full footer.
- **Admin dashboard:** grouped collapsible sidebar, top bar with search/notifications/theme toggle/profile, KPI cards with trends, charts, activity table with badges and actions.
- **Tables, forms, auth and mobile screens:** complete layouts with toolbars, styled controls, validation, skeletons and illustrated empty states.

All of it uses Rule 01 tokens, so Light and Dark both look finished. Demo data is realistic (₱, local names) and kept in one `demo-data` file so it is easy to replace.

## Install

Requirements: Windows, PowerShell, Python 3.10+.

```powershell
cd path\to\agkit2
.\install.ps1 -Check        # validate only, no changes
.\install.ps1               # back up current install, then install
```

The installer validates the source, backs up the active plugin, rules and `GEMINI.md` block to `~/.gemini/config/agkit-backups/<timestamp>`, installs, validates again, and restores the backup automatically if anything fails. Restart Antigravity and open a new chat afterwards.

## Check the kit

```powershell
python -B scripts/validate_kit.py . --strict          # structure, frontmatter, references
python -B -m unittest discover -s scripts/tests       # kit test suite
python -B scripts/kit_doctor.py --json                # installed vs source health (read-only)
python -B scripts/build_quick_reference.py --write    # regenerate rules/quick-reference.md
```

## Folder layout

```
agkit2/
  rules/        kit-core + Rules 01-07 + generated quick-reference
  agents/       14 agent files
  skills/       skills and slash commands (each has SKILL.md)
  scripts/      validator, doctor, installer helpers, checks, tests
  docs/plans/   plans behind each version
  docs/eval/    prompts + checklist to test the kit in Antigravity
  install.ps1   installer with backup and rollback
  VERSION       current version
  CHANGES.md    release history
  DECISIONS.md  current design decisions
```

## Changing the kit

1. Edit files in this repo (not in the installed plugin).
2. Run `validate_kit.py . --strict` and the tests.
3. Run `.\install.ps1`.
4. Commit and push.

Add a new rule as `rules/rule-NN-<topic>.md` with frontmatter (`name`, `version`, `trigger`, `globs` for glob rules, `description`), then add it to `kit-core`, `KIT_RULES` in `scripts/validate_kit.py` and `$ruleNames` in `install.ps1`.

See [CHANGES.md](CHANGES.md) for release history, [DECISIONS.md](DECISIONS.md) for the reasoning, and [docs/eval](docs/eval/README.md) to test the kit.
