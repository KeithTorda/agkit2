# AG Kit v2.5

An agent kit for Google Antigravity. 20 specialist agents that also run as native subagents, 51 skills and slash commands, 29 helper scripts, and 6 always-on rules (about 12 KB). Built for web apps, admin systems, POS and inventory, and LGU, school and election portals.

Version 2.5.0 (2026-09-27). Maintained by Keith Torda. Based on `vudovn/ag-kit`.

## What changed in 2.5
- **It thinks instead of running a checklist.** The agent works in a loop: understand, choose a process that fits the task size, build, verify according to risk, report. There is no mandatory plan line and no full gate on every edit.
- **Verification by risk tier.** A copy fix runs nothing. Normal work runs the project's own quick checks. Auth, payments, migrations and public APIs run the full set, tests and `/review`. Releases add `verify_all.py` and ask for approval.
- **Design is guidance, not bans.** `DESIGN.md` and the client's brief win. Gradients, glass, glow, motion and dark themes are built properly when the design calls for them. Only accessibility and hype-free system copy stay firm. The 35-part anti-template reference is now a skill the agent reads only when it needs it.
- **`/proplan`.** Plans a system professionally: goals, development goals, requirements, architecture, data, API, UX, security, quality, operations, roadmap, risks and documentation. Planning subagents do the parts, and a checker traces every ID from goal to test.
- **Native subagents.** Agent files use the Antigravity 2.0 subagent format, so the main agent can hand independent work to them with `invoke_subagent`.

## Install (Windows)
```powershell
git clone https://github.com/KeithTorda/agkit2.git
cd agkit2
.\install.ps1
```
Restart Antigravity. The installer:
- does a clean install of the plugin to `~/.gemini/config/plugins/ag-kit-v2`
- copies the 7 rules to `~/.gemini/config/rules`
- removes the old `copy.md` and `design.md` rules
- updates the `KIT` path for your Windows user
- runs the validator

If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.

First run: type `/status` in a project, make one small edit, then try `/proplan --lite <an idea>`.

## How the agent works
| Task size | What it does |
|---|---|
| Question | Answers. |
| Trivial edit | Makes the change and reports in 1-3 lines. |
| Normal feature or fix | Routes to one agent, writes a short plan in the reply, builds, runs quick checks. |
| Big feature or new system | Uses `/plan` or `/proplan`, then builds milestone by milestone with `/orchestrate`. |

It asks questions only when the answer changes what gets built: at most 3 (5 for `/proplan` intake), each with a recommended default. Every report ends with a `Not verified:` line.

## Commands
| Command | Does |
|---|---|
| `/proplan <system>` | Full professional plan in `docs/proplan/<slug>/`, written with planning subagents. Use `--lite` for small systems and `update <slug>` for change requests |
| `/plan <task>` | Task list with an owner and a verify line per task, in `docs/plans/<slug>.md` |
| `/create <app>` | New app: questions, optional `/proplan --lite`, DESIGN.md, build, dev server |
| `/orchestrate <task>` | Multi-agent build. `/orchestrate docs/proplan/<slug> M1` runs milestone 1 |
| `/enhance` | Adds to an existing app |
| `/brainstorm` | 2-4 approaches with trade-offs, before any code |
| `/debug` | Reproduce, find the root cause, fix, add a regression test |
| `/fix-ui` | Layout and styling bugs fixed at the root cause |
| `/see` | Looks at the running app in the browser at mobile and desktop widths |
| `/see-doc` | Renders and checks a generated PDF, XLSX or DOCX |
| `/test` | Writes or runs tests |
| `/verify` | Runs the full check set now |
| `/review` | Hostile review of the current diff |
| `/deploy` | Pre-flight, deploy, health check, rollback plan |
| `/status` | Stack, git changes, plan and proplan progress |
| `/remember <note>` | Saves a fact or `[failure]` to `.agents/memory/MEMORY.md` |

`@agent-name` in a message forces that agent.

## Agents
| Group | Agents |
|---|---|
| Build | frontend-specialist, mobile-developer, backend-specialist, database-architect |
| Plan | product-manager, solution-architect, ux-architect, project-planner, plan-reviewer |
| Quality | test-engineer, debugger, security-auditor, penetration-tester (authorised only), performance-optimizer, seo-specialist |
| Ship and maintain | devops-engineer, documentation-writer, code-archaeologist, explorer-agent |
| Coordinate | orchestrator |

## /proplan in one picture
```
0 Intake ─► 1 Discovery (parallel) ─► 2 Architecture options ─► [you choose] ─► ADRs
          product-manager, ux-architect,        solution-architect
          security-auditor, explorer-agent
─► 3 Detailed design (parallel): 04 data · 05 API · 06 UX · 07 security · 08 quality · 09 operations
─► 4 Delivery: 10 roadmap (M1.., T-001..) · 11 risks · 12 documentation
─► 5 plan-reviewer red-teams it, proplan_check.py traces G → R → T → TC
─► 6 Handoff: /orchestrate docs/proplan/<slug> M1
```
Example: `skills/proplan/example/pos-lite/` (a small cafe POS).

## Layout
```
rules/     always-on: core-protocol, engineering-excellence, code-rules, universal-rules, request-routing
           on UI files: design-rules · on demand: quick-reference (generated)
agents/    20 agent files (Antigravity native subagent format)
skills/    51 skills; each command is skills/<command>/SKILL.md
           anti-template/parts/  35-part design and copy reference (guidance)
           proplan/templates/    the plan document templates
scripts/   checklist.py (risk tiers), verify_all.py, proplan_check.py, css_audit.py, naming_check.py,
           ui_verify.py, doc_verify.py, validate_kit.py, build_quick_reference.py, tests/
```

## Checks
```powershell
python "$env:USERPROFILE/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py" .          # quick: changed files
python "$env:USERPROFILE/.gemini/config/plugins/ag-kit-v2/scripts/checklist.py" . --full   # everything
python "$env:USERPROFILE/.gemini/config/plugins/ag-kit-v2/scripts/proplan_check.py" docs/proplan/<slug>
```
Only these fail a run: security findings rated high or above, type errors and failing tests. Lint style, naming, the CSS audit and UX/SEO heuristics are advisory; `--strict` makes them fail too.

## Editing the kit
After a change, run:
```powershell
python scripts/validate_kit.py
python scripts/build_quick_reference.py --write
python -m unittest scripts/tests/test_toolkit.py
.\install.ps1
```
Keep the always-on rules under 15 KB. Put detail in skills.

## Limits
- Subagent frontmatter follows the Antigravity 2.0 docs, but its runtime behaviour has not been tested on your machine. For example, subagents are assumed to inherit the parent's tools when `tools` is omitted. If a subagent cannot read files, add a `tools:` list to that agent.
- Custom agents may be limited to the Antigravity 2.0 app and CLI. Where `invoke_subagent` is not available, the main agent plays each role in turn.
- The scripts are written for Windows but were tested on Linux.
