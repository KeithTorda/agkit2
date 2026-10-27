# AGKIT2 v3.0 — New rules and new agents

Date: 2026-10-27
Owner: Keith (Nikko)
Status: Done (3.0.0 built 2026-10-27; defaults used for the 4 open questions: merges as listed, Rules 02–06 as listed, Rule 04 for every new system, English replies)
Current installed version: 2.9.0 (Rule 01 + kit-core)

---

## 1. Why

The 2.9 cleanup removed the old rules but the 20 agents are still the old v2.8 agents with a few lines patched. They are:

- **Too many and overlapping.** product-manager / project-planner / plan-reviewer / ux-architect all plan; security-auditor / penetration-tester split one job; explorer-agent / code-archaeologist both "read old code"; performance-optimizer overlaps debugger.
- **Generic.** Every agent reads like a policy document ("establish the contract", "distinguish evidence"). None of them knows *your* stacks (React/Next, Laravel, Bootstrap admin UI kit, Expo), *your* systems (MyBizMate ERP add-ons: POS, SFA, HRIS), or *your* rules.
- **Abstract instead of actionable.** Long paragraphs, few concrete steps, no examples of a good result, no fixed handoff format.
- **Still carrying old-rule ideas** (intake ceremony wording, "evidence tiers", "manual-only policy" phrasing everywhere).

Goal: our own rule set and a smaller team of sharp agents that build like a senior team you would hire.

---

## 2. Design principles for v3.0

1. **Rules = what must always be true. Agents = who does the work. Skills = how-to detail.** No policy repeated in three places.
2. **Few rules, each owns one topic.** No two rules talk about the same thing.
3. **Concrete over abstract.** Every agent has steps, a quality bar with checkable items, and a fixed handoff format.
4. **Not strict, not lazy.** No approval ceremonies, no forced questions, no automatic browser/test runs. But the work itself must be complete and professional.
5. **Built for Gemini in Antigravity.** Short sentences, numbered steps, explicit "do / don't", examples. Always-on rules stay small (budget ≤ 15 KB total); topic rules load by file glob or by model decision.
6. **English only, no emoji, direct tone.**

---

## 3. New rule set

| # | File | Loads | Owns | Status |
|---|---|---|---|---|
| 00 | `kit-core.md` | always | Kit path, agent/command routing table, "checks only when asked" | Rewrite (new agent names) |
| 01 | `rule-01-unified-theme-system.md` | UI files | Light/Dark/System token theming | **Keep exactly as you wrote it** |
| 02 | `rule-02-work-style.md` | always | How the AI talks and delivers: English, direct, no emoji, finish the job, no fake claims, plans go to `.md` | New |
| 03 | `rule-03-code-standards.md` | code files | Clean organized code: existing stack first, unique domain names, no CSS override hacks, file structure, error handling, no secrets, input validation | New |
| 04 | `rule-04-system-integration.md` | model decision (backend/system work) | ERP ↔ add-on pattern (Option B) for POS, SFA, HRIS and every new system | New |
| 05 | `rule-05-planning-and-docs.md` | model decision (plan/doc work) | Every plan is a `.md` in `docs/plans/`; plan format; README/handover minimums | New |
| 06 | `rule-06-security-baseline.md` | code files | Auth on server, role checks per resource, parameterized queries, secrets in env, safe file uploads, audit trail for money/records | New |
| — | `quick-reference.md` | model decision | Generated catalog | Regenerate |

### Draft content (short form — full text written in Phase 1)

**Rule 02 — Work Style**
- Reply in English. Direct, short, detailed where it matters. No emoji. No hype words.
- Lead with the result. Then what changed, then anything unfinished.
- Finish what was asked. Do not stop at analysis when implementation was requested.
- Ask only when an answer changes scope, data, money, or permission. Otherwise decide and say what you decided.
- Every plan is written to a `.md` file, not only in chat.
- Never claim something ran, passed, or was checked unless it actually did.

**Rule 03 — Code Standards**
- Use the project's existing stack, folder structure and conventions. Do not replatform.
- Names are domain-specific and unique (`posReceiptTotal`, not `data2`). No generic `utils2.js`.
- CSS: fix the owning rule or token. No `!important` piles, no override-on-override, no inline style patches for layout bugs.
- One component = one job. Shared UI goes into the shared component folder.
- Handle loading, empty, error and success states for every data screen.
- Remove dead code you replaced. No commented-out blocks left behind.
- Comments explain *why*, not *what*.

**Rule 04 — System Integration (Option B)**
- Separate database per system. No shared-table access between systems.
- One owner per table: core ERP owns master data (customers, items, prices, branches, users); the add-on owns its own transactions.
- Add-on → ERP: outbox table + middleman worker for realtime sync, with retries and idempotency keys.
- ERP → add-on: ERP webhooks for master-data changes + nightly reconciliation job.
- Versioned API contract (`/api/v1/...`); breaking change = new version.
- Applies to POS, SFA, HRIS and every new MyBizMate system.

**Rule 05 — Planning and Docs**
- Plans live in `docs/plans/<yyyy-mm-dd>-<slug>.md`.
- A plan has: goal, scope (in/out), decisions, steps with owner agent, risks, how we know it is done.
- Big systems use `/proplan` (numbered doc set). Small features use `/plan` (one file).
- After a feature ships: update README / CHANGELOG if behavior changed.

**Rule 06 — Security Baseline**
- Authenticate on the server; check the user's role for every resource action.
- Parameterized queries only. Validate every external input at the boundary.
- Secrets only in `.env`; never in client code, logs or commits.
- Money, receipts, invoices, payroll: server computes totals; keep an audit trail (who, when, before/after).
- File uploads: check type and size; store outside public root or with safe names.

---

## 4. New agent team (20 → 14)

| New agent | Replaces | Owns |
|---|---|---|
| `lead` | orchestrator | Reads the request, picks agents, splits work, integrates, final report. Default entry for big tasks. |
| `architect` | solution-architect, plan-reviewer | System design, tech choices, ADRs, Rule 04 integration design, reviews plans for gaps. |
| `product-planner` | product-manager, project-planner | Goals, requirements, user stories, acceptance criteria, task breakdown, `/plan` and `/proplan` docs. |
| `ux-designer` | ux-architect (+ design side of frontend) | Flows, sitemap, screen list with states, DESIGN.md, Rule 01 token set, component inventory. |
| `frontend-engineer` | frontend-specialist, seo-specialist | Web UI in React/Next, Blade, Bootstrap 5, Tailwind; Rule 01 theming; SEO/meta. |
| `backend-engineer` | backend-specialist | APIs, Laravel/Node services, auth, jobs, webhooks, exports (PDF/Excel/receipts), outbox/middleman (Rule 04). |
| `database-engineer` | database-architect | Schema, migrations, indexes, queries, seeds, data ownership per Rule 04. |
| `mobile-engineer` | mobile-developer | Expo/React Native/Flutter screens, offline, device features, store builds. |
| `qa-engineer` | test-engineer | Tests and test plans, code review on request, regression protection. |
| `debugger` | debugger, performance-optimizer | Root-cause bug fixing and measured performance fixes. |
| `security-engineer` | security-auditor, penetration-tester | Rule 06 reviews, threat model, authorized pentest. |
| `devops-engineer` | devops-engineer | VPS/Nginx/PM2/Docker, CI/CD, env, backups, rollback, deploy. |
| `docs-writer` | documentation-writer | README, setup/deploy guides, API docs, user/admin manuals, handover. |
| `explorer` | explorer-agent, code-archaeologist | Read-only codebase mapping, legacy code explanation, feasibility answers. |

### New agent file template (every agent uses this)

```markdown
---
name: <agent>
description: "<one sentence: what it owns>. Triggers on: <keywords>."
model: inherit
subagent: true
mainAgent: true
kit-skills: [<max 6 skills>]
version: 3.0.0
---

# <Agent name>

## Mission
One paragraph: what this agent is for and what "great" looks like.

## Owns / Does not own
- Owns: ...
- Hands off to: <agent> for ...

## Before starting (read)
Numbered list of exactly what to read in the project first.

## How to work
Numbered steps for the normal job. Concrete, stack-aware.

## Stack notes
Short per-stack tips (React/Next, Laravel, Bootstrap, Expo...) only where relevant.

## Quality bar
Checklist of concrete, checkable items for a finished job.

## Common mistakes to avoid
5–8 specific bullets (things Gemini actually gets wrong).

## Handoff format
Fixed report shape: Result / Files changed / Decisions / Not done / Next.
```

The validator's required agent sections change to: `Mission, Owns / Does not own, Before starting, How to work, Quality bar, Common mistakes to avoid, Handoff format` (Stack notes optional).

---

## 5. What else must change with the agents

- `kit-core.md` routing table → new 14 names.
- Slash commands: keep the same command names (`/create`, `/plan`, `/proplan`, `/debug`, `/fix-ui`, `/see`, `/test`, `/verify`, `/review`, `/deploy`, `/orchestrate`, `/enhance`, `/brainstorm`, `/status`, `/remember`, `/doctor`, `/updatekit`, `/see-doc`). Update any that name old agents.
- Skills that name old agents: orchestrate, parallel-agents, proplan (doc owners per file), app-builder agent-coordination, plan-writing. Update names only; skill content refresh is a later phase.
- `validate_kit.py`: new agent section list, new rule list (`KIT_RULES`), test fixtures.
- `install.ps1`: new rule file names; remove old agent files from the installed plugin (installer already replaces the whole plugin folder).
- `build_quick_reference.py`: regenerate.
- README, CHANGES, DECISIONS.

---

## 6. Phases

| Phase | Work | Output |
|---|---|---|
| 1 | Write Rules 02–06 in full; rewrite kit-core | 6 rule files |
| 2 | Write the 14 agents from the template (research current best practice per domain; stack-aware for your stacks) | 14 agent files, 20 old ones deleted |
| 3 | Update routing, skills that name agents, validator, tests, installer, quick-reference | Kit validates 0 errors, tests pass |
| 4 | Independent review pass: a separate reviewer reads all rules + agents for conflicts, duplicates, vague lines | Review notes + fixes |
| 5 | Back up and install (same safe script as 2.9) | AGKIT2 3.0.0 active in Antigravity |
| 6 | You test in Antigravity: one UI task, one Laravel API task, one POS-add-on planning task | Your feedback → 3.0.1 |

Rollback at any point: `Desktop\agkit2-backup-v2.8.3`, a new `agkit2-backup-v2.9.0`, and the installer's own backup in `.gemini\config\agkit-backups`.

---

## 7. Decisions needed from you

1. **Agent merge list (section 4)** — OK to go from 20 to 14 with these merges? Anything to keep separate (e.g. SEO, pentest, performance)?
2. **Rules 02–06** — OK with these five topics? Anything to add (e.g. a Laravel-specific rule, a BIR/receipt compliance rule, a Filipino/Taglish UI copy rule)?
3. **Rule 04 scope** — always apply Option B to *every* new system, or only MyBizMate ERP add-ons?
4. **Language of agent replies** — English always (current), or match the language you type in?
