# AG Kit v2 — Health Check & Fix Plan

Checked: VERSION 2026.9.8 (CHANGES.md v2.2.2), 178 source files (17 agents, 49 skills, 27 scripts, 7 rules, docs, installer).
Method: ran `validate_kit.py` and the unittest suite, regenerated `quick-reference.md` and diffed it, cross-referenced every `agents/`, `skills/`, `scripts/` path mentioned in any `.md`, checked agent skeletons and Read-now budgets, then ran the kit's own audit scripts against a real project (the Barangay Allig site) to see what they catch and miss.

---

## 1. Verdict

Structurally the kit is in very good shape. Everything below passed cleanly:

| Check | Result |
|---|---|
| `validate_kit.py` | 0 errors, 0 warnings |
| `scripts/tests/test_toolkit.py` | 22 tests: 19 pass, 2 skipped, 195 subtests pass; the 1 "failure" only fires when `.git/` is absent (my copy), passes on your machine |
| `quick-reference.md` vs `build_quick_reference.py` | in sync (only a trailing newline differs) |
| Broken cross-references (agents ↔ skills ↔ scripts ↔ commands) | none in live files; 3 stale script names in `DECISIONS.md` only (`auto_preview.py`, `convert_rules.py`, `x.py`), all in a "deleted" note, so fine |
| Orphan skills (referenced by nothing) | none |
| Skill frontmatter (name / description / version) | complete on all 49 |
| Agent six-section skeleton (Own / Build / Repair / Decide / Never / Done) | all 17 conform |
| All 15 slash commands in `request-routing` | each has a `skills/<cmd>/SKILL.md` |
| Command wrappers (`brainstorm`→`brainstorming`, `plan`→`plan-writing`, `debug`→`systematic-debugging`, `fix-ui`→`ui-repair`, `review`→`adversarial-review`, `verify`→`verify-changes`, `see`→`browser-verification`) | intentional thin wrappers, not duplicates; keep |

The problems are not structural. They are (a) one P0 rule that contradicts the design skills and has already leaked into real output, (b) portability for the team, and (c) doc drift. Ranked below.

---

## 2. Problems, ranked

### 2.1 `design-rules.md` "Ultra High-Contrast / Anti-Blur Invariant" contradicts the kit's own design skills — and it is winning (HIGH)

`rules/design-rules.md` §"Ultra High-Contrast" is `priority: P0`, always applied on UI files, and says:
- dark theme primary text **must** be pure `#FFFFFF`, light theme **must** be pure `#000000`
- status badges **must** use luminous foregrounds "e.g. Emerald `#34D399`"
- reusable styles **must** live in Tailwind `@layer components`

Meanwhile the skills say the opposite:
- `frontend-design/marketing-layout.md:30` — "No pure `#000000` or `#ffffff` surfaces; off-black and off-white keep depth."
- `frontend-design/SKILL.md` §4.2 — "no pure white"
- `mobile-design/mobile-typography.md:271` — "Don't use pure white (#FFF) on dark."
- `mobile-design/mobile-color-system.md:344` — pure white in dark mode → eye strain
- `design-rules.md` itself, three lines earlier — "one design system per project… when `DESIGN.md` exists, its tokens override any skill guidance."

Per `core-protocol` precedence (global rules → agent → skill), the rule beats the skills. Proof it is doing damage: the Barangay Allig site's `DESIGN.md` says "no pure white or black, no neon or saturated colours", yet its CSS shipped `.barangay-badge-radiant-green { background:#D1FAE5; color:#064E3B; border:#34D399 }` and `#FFFFFF` in six places. That is this rule overriding the project's own design spec.

Root cause: this block was written for one dark-navy dashboard problem (Slate-400 text on navy) and promoted to a global invariant. It also assumes Tailwind, but the kit supports plain CSS (`css-architecture/plain-css.md`).

Fix:
1. Replace the block with the principle, not the values: *"Text must meet WCAG AA (4.5:1 body, 3:1 large). Never dark-on-dark or light-on-light. Colour values come from `DESIGN.md`; if a project has no `DESIGN.md`, follow `frontend-design` / `mobile-design`."*
2. Move the `#FFFFFF` / `#34D399` / `@layer components` recipe into `frontend-design/app-ui.md` as the *dark-dashboard* style option, alongside `style-brutalist.md` and `style-minimalist.md`, so it is picked deliberately.
3. Make `@layer components` conditional: "in Tailwind projects"; plain-CSS projects follow `css-architecture`.
4. Remove the matching prose from `README.md` §"Ultra High-Contrast Typography Standard" and `AG_KIT_SLASH_COMMANDS.md:93`.
5. Add a test in `test_toolkit.py`: no rule file contains a literal hex colour (rules state principles; skills hold values).

### 2.2 Portability: 151 hardcoded `C:/Users/Keith` paths in 68 files (HIGH for the team)

`install.ps1` rewrites them, but:
- A Windows username with a space (`C:/Users/Juan Dela Cruz`) produces unquoted commands like `python C:/Users/Juan Dela Cruz/.gemini/.../checklist.py .` in every rule and agent — they all break.
- The README's "Manual Installation (macOS / Linux)" section never rewrites paths at all, so a Mac user's rules point at `C:/Users/Keith/...`. The manual commands are also PowerShell syntax on a Mac section.
- Two reference styles coexist: absolute paths (agents, rules, 0 uses of `@[...]`) and Antigravity's own `@[skills/x]` mentions (39 uses inside command skills). The `@[...]` form is already proven to work in the kit.

Fix:
1. Switch every path in `agents/` and `rules/` to the `@[skills/<name>/SKILL.md]` / `@[scripts/<name>.py]` form the command skills already use; keep one absolute example in `core-protocol` if Antigravity needs it for `python` invocations, and quote it.
2. In `install.ps1`, quote the path when substituting (`"$UserProfileForward"`) and emit `python "…/checklist.py"` forms.
3. Add `install.sh` for macOS/Linux (same four steps, `$HOME`), or state plainly that the kit is Windows-only.
4. `universal-rules.md` §1 "Nikko often writes Taglish" and §7 "Host: Windows 11, PowerShell 7" are personal in a team-distributed kit. Move them to a `~/.gemini/GEMINI.md` user file (which `plugin.json` already names as the entry file) and keep the rule generic.

### 2.3 `core-protocol` step 1 is missing the REPAIR type (MEDIUM)

`request-routing.md` classifies eight types including **REPAIR** (fix, broken, misaligned → Repair steps / `/fix-ui`), which is the whole point of the v2.2 UI-repair work. `core-protocol.md` step 1 lists only seven: "QUESTION, SURVEY, SIMPLE CODE, COMPLEX CODE, NEW APP, MULTI-DOMAIN, COMMAND". A model following core-protocol literally never emits REPAIR, so the Repair branch in step 7 is reached only by luck.

Fix: add REPAIR to the step-1 list and to the `build_quick_reference.py` output; add a test that the two lists are identical.

### 2.4 Installer never removes stale files, and copies junk (MEDIUM)

`Copy-Item -Recurse -Force` merges into an existing `ag-kit-v2/`. A skill you delete or rename in the repo stays installed forever (e.g. anything removed since `brainstorm`/`brainstorming` were split), and `validate_kit.py` then validates the union, not the repo. It also copies `scripts/__pycache__/`, `scripts/tests/`, `.gitignore`, `CHANGES.md`, `DECISIONS.md` into the plugin.

Fix: `Remove-Item $PluginsDir -Recurse` before copying (after a `-WhatIf`-style confirmation or a backup rename), and add `__pycache__`, `tests`, `.gitignore`, `CHANGES.md`, `DECISIONS.md` to the exclude list. Print the installed file count so a partial copy is visible.

### 2.5 Two scripts disagree about `!important`, and the rule over-claims (LOW)

- `code-rules.md` says `css_audit.py` "fails on `!important`". It actually fails only on `!important` applied to a **colour** property (by design, and correct — the `prefers-reduced-motion` reset legitimately uses it). Tested: the barangay site's four `!important` in a reduced-motion block pass `css_audit` but are flagged as advisory by `naming_check.py`.
- Fix: make `code-rules` say "on a colour property", and either drop the `!important` advisory from `naming_check.py` (it is not a naming concern) or move it into `css_audit` as a warning that skips `@media (prefers-reduced-motion)`.

### 2.6 Doc drift (LOW, but it is what a new team member reads first)

| Where | Says | Actual |
|---|---|---|
| README §Automated Verification Gates | "23 automated Python verification scripts" | 27 (README's own tree says 27) |
| README §Toolkit Maintenance | "unit test suite (15 test cases)" | 22 (badge says 22) |
| README §Prerequisites | Python 3.12+, Node 20+ | `code-rules` baseline: Python 3.13+, Node 24 LTS; README §Technology Baseline: Python 3.14 |
| README §Ultra High-Contrast | whole section | remove per 2.1 |
| README §Slash Commands | "34 domain skills" | 49 skill dirs = 15 commands + 34 domain; say so once |
| CHANGES.md v2.2.2 §3 | `ui_verify.py` audits `after.png`, `mobile-after.png`, `before.png` | script and all skills use `<before\|after>-<width>.png` |
| Versioning | CHANGES.md "v2.2.2", VERSION "2026.9.8", rules 2.0.0 / 2.2.0, `plugin.json` no version | pick one scheme; put it in `plugin.json` and have `validate_kit.py` assert VERSION == plugin.json.version == top CHANGES heading |

### 2.7 Token budget: `quick-reference.md` is always-on (LOW)

Always-on rules total ~31 KB, and `quick-reference.md` is 10 KB of that — a catalog of every agent, skill and script. `request-routing` already picks the agent, and each agent already lists its skills, so the catalog is read on every request but consulted almost never. Set its `trigger` to `model_decision` (or `manual`) with a description like "look up the full catalog of skills and scripts", and the always-on cost drops by a third. The read-when skills are fine (`mobile-design` is 141 KB but nothing loads it whole).

### 2.8 What the advisory scripts did not catch (informational)

Run against the barangay site: `checklist.py` reported 10/10 pass. It did not flag 10.5 px label text, a 3:1 badge contrast (rgba badge over a photo overlay, so the pair is not declared in CSS), 8 MB of unoptimised JPGs, or an 829 KB favicon. `accessibility_checker.py` has no contrast computation at all (0 mentions); contrast lives only in `css_audit.py` and only for declared solid pairs. If you want the P4 advisory tier to earn its place, add: minimum font-size in px/rem (< 12 px → warn), image byte size over a threshold, and favicon type/size. These are three small regexes in `ux_audit.py`.

---

## 3. Fix order

1. **2.1** design-rules rewrite + README/SLASH_COMMANDS prose + hex-in-rules test. (Highest impact: it changes what the kit ships on every UI task.)
2. **2.3** add REPAIR to core-protocol step 1 + list-equality test. (Five minutes.)
3. **2.2** path references → `@[...]` form; quote paths in installer; decide Windows-only or add `install.sh`; move personal lines out of `universal-rules`.
4. **2.4** installer clean-before-copy + exclude list.
5. **2.6** doc drift table, and the version-consistency assertion in `validate_kit.py`.
6. **2.5**, **2.7**, **2.8** as time allows.

After each step: `python scripts/validate_kit.py`, `python -m unittest discover -s scripts/tests`, `python scripts/build_quick_reference.py --write`, then bump VERSION / CHANGES together.

---

## 4. Not verified

- Nothing was run inside Antigravity itself; all checks were static or via the kit's own Python scripts on Linux.
- Test count "22" assumes unittest's count of test methods; pytest reports 20 + 2 skipped, which is the same 22.
- The Barangay Allig site was used as the real-world probe on the assumption it was built with this kit (its CSS carries the kit's `@layer` and radiant-badge fingerprints).
