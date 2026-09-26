# AG Kit v2.5 — Rebuild Plan

Date: 2026-09-27. Owner: Nikko (Keith Torda). Target: `Desktop/agkit2`, installs to `~/.gemini/config/plugins/ag-kit-v2` (same path as v2.2).

## Why
Current rating 4/10. The kit works structurally (validate_kit passes) but behaves like a checklist machine:

| Problem | Where | Effect |
|---|---|---|
| ~75 KB of always-on rules, 40 KB of it `copy.md` | `rules/` | Every prompt pays for the whole rulebook; the model follows bans instead of thinking |
| Mandatory plan line, `checklist.py`, `/see`, `ui_verify.py`, `/review` on every code task | `core-protocol`, `code-rules`, agents' Done sections | Slow; a one-line CSS fix runs the full gate |
| Two design rules that contradict each other and the skills (pure `#FFFFFF` + emerald glow vs "no pure white, no glow") | `design-rules.md`, `design.md` | Wrong colours shipped (Barangay Allig), generic look either way |
| Anti-AI list written as hard bans | `copy.md`, `frontend-design §0.E` | Clients who ask for gradients or glass get refused; output drifts to the same "safe" look |
| Naming and CSS audits are required failures | `code-rules`, `checklist.py` | Blocks done on style, not correctness |
| No professional planning flow | — | Big systems start from a 12-line plan |
| Agents are persona files the main agent reads; Antigravity 2.0 native subagents (`invoke_subagent`) are unused; frontmatter `skills: a, b` is not the native schema | `agents/` | No real delegation; possible parse issues now that plugin `agents/` are auto-discovered |
| 151 hardcoded `C:/Users/Keith` paths | everywhere | Breaks for teammates with spaces in username |

## Decisions (from Nikko, 2026-09-27)
1. Rewrite `agkit2` in place (git keeps v2.2).
2. Design: guidance, not bans. `DESIGN.md` and the client's request win. Only copy hype and accessibility stay firm.
3. Gates: proportional to risk. No mandatory plan line.
4. Add `/proplan` with subagents; revise all agents, skills and scripts to the "Opus 5.5 working model".

## The working model (what every file now teaches)
1. **Understand before acting.** Read the files the task touches, `DESIGN.md`, `.agents/memory/MEMORY.md`. Batch independent reads.
2. **Right-size the process.** Trivial → just do it. Multi-file → 3–6 line plan in the reply. New system / big feature → `/plan` or `/proplan`.
3. **Ask only when blocked.** One message, max 3 questions, only when the answer changes what gets built. Otherwise state the assumption and go.
4. **Delegate what is independent.** Native subagents via `invoke_subagent` for parallel research or disjoint builds; full briefs; never delegate understanding.
5. **Verify in proportion to risk.** Risk tiers decide which checks run (table in `code-rules`). Never claim what was not run.
6. **Report like an engineer.** Result first, files changed, assumptions, what was not verified. No ceremony.
7. **Taste over rules.** Design decisions come from the brief, the audience and `DESIGN.md`. Anti-template guidance is a list of defaults to question, not a list of bans.

## Architecture v2.5

### Rules (always-on budget ≤ 15 KB)
| File | Change |
|---|---|
| `core-protocol.md` | Rewrite: the working model loop; defines `KIT` path once; no plan line; subagent basics |
| `engineering-excellence.md` | Rewrite: standard of thinking, proportional depth, honesty |
| `code-rules.md` | Soften: risk-tier verification table; fix-at-source as strong default; naming as convention |
| `design-rules.md` | Merged design rule (glob): DESIGN.md is truth, accessibility firm, anti-template as guidance; no hex values |
| `request-routing.md` | Add `/proplan`, 3 new agents, subagent routing |
| `universal-rules.md` | Update: language, style, memory, safety, host |
| `quick-reference.md` | Stays `model_decision`, regenerated |
| `copy.md`, `design.md` | Removed from install (installer deletes stale copies); content moves to `skills/anti-template` |

### Agents (20, native subagent frontmatter)
Frontmatter: `name`, `description`, `model: inherit`, `subagent: true`, `mainAgent: true`, `kit-skills: [..]`, `version: 2.5.0`. `tools` omitted so agents inherit the parent's tools (a wrong tool name can hang a subagent).
Body sections: Role · How you work · Build · Repair · Decide · Never · When invoked as a subagent · Done (proportional).
New: `solution-architect`, `ux-architect`, `plan-reviewer`.

### `/proplan` (new)
Professional system planning with development goals, full documentation set, and subagents.
Phases: 0 Intake → 1 Discovery (parallel) → 2 Architecture decision (checkpoint with Nikko) → 3 Detailed design (parallel) → 4 Delivery plan → 5 Plan review (adversarial) → 6 Handoff to `/orchestrate`.
Output: `docs/proplan/<slug>/` — 00-overview … 13-glossary, `adr/`, `TRACEABILITY.md`; checked by `scripts/proplan_check.py` (IDs G-, R-, NFR-, ADR-, T-, TC- link end to end).
Scales: `--lite` (5 docs) for small systems, full set for client systems.

### Skills
- New: `proplan` (+ templates), `anti-template` (35-part reference ported from agkit3, reframed as guidance).
- Revise all 49: remove mandatory gates, use `KIT/…` paths, native subagents in `parallel-agents` / `orchestrate`, softer design skills.

### Scripts
- `checklist.py`: risk-aware (`--quick` default = lint/types/tests on changed files; `--full`), required = security high+, types, tests; naming/CSS advisory.
- `css_audit.py`, `naming_check.py`: advisory by default, `--strict` to fail.
- `validate_kit.py`, `tests/test_toolkit.py`: new schema, new agents/skills, always-on budget check.
- New `proplan_check.py`.
- All skill scripts: bug fixes, Python 3.13, argparse, `--json`, Windows-safe paths, consistent exit codes (0 ok, 1 required failure, 2 usage).

### Install / docs
`install.ps1`: clean plugin install, explicit rule list, deletes stale kit rules (`copy.md`, `design.md`), patches only the `KIT` line, quoted paths. README, AG_KIT_SLASH_COMMANDS, CHANGES (v2.5.0), DECISIONS, VERSION `2026.9.27`, plugin.json.

## Tasks
- [ ] 1. Rules rewrite (owner: main) — verify: always-on rules ≤ 15 KB; no hex in rules
- [ ] 2. `/proplan` skill, templates, `proplan_check.py`, 3 new agents (owner: subagent A) — verify: `proplan_check.py` passes on the bundled example
- [ ] 3. Agents batch 1 + 2 rewrite (owner: subagents B, C) — verify: validate_kit agent checks pass
- [ ] 4. Skills revision in 3 batches (owner: subagents D, E, F) — verify: no required-gate wording left (`grep`), paths use `KIT/`
- [ ] 5. Design skills + anti-template port (owner: subagent G) — verify: no hex values in rules; guidance wording
- [ ] 6. Kit scripts + tests (owner: subagent H) — verify: `python -m unittest` green
- [ ] 7. Skill scripts (owner: subagent I) — verify: each script `--help` exits 0; runs on a sample project
- [ ] 8. Docs, installer, version (owner: main) — verify: validate_kit PASS, tests green
- [ ] 9. Commit files to `Desktop/agkit2`; list obsolete repo files for Nikko to `git rm`

## Done when
- [ ] `python scripts/validate_kit.py` → PASS; `python -m unittest scripts/tests/test_toolkit.py` → green
- [ ] Always-on rules ≤ 15 KB
- [ ] `/proplan` produces a complete doc set that `proplan_check.py` accepts
- [ ] Nikko runs `.\install.ps1`, restarts Antigravity, tries `/status`, one small edit, and `/proplan --lite <idea>`

## Not verifiable from here
Antigravity runtime behaviour (subagent tool inheritance when `tools` is omitted, `invoke_subagent` availability in the IDE vs Antigravity 2.0 app). Test step above covers it.
