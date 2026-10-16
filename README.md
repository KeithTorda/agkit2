# AGKIT2 2.8.2 — Component Craft

An Antigravity kit for understanding, building, diagnosing and delivering software across web, mobile, backend, data, testing, security, deployment, documentation and planning. The editable folder remains agkit2 and the installed plugin remains ag-kit-v2.

## How it works

Start with the outcome, inspect the actual project and select the relevant expertise. The core rules own shared decisions; domain skills explain practical choices and failure modes without introducing a competing global workflow. A small edit stays small, while consequential changes receive the evidence their contracts require.

The 2.8 full refresh rebuilt all existing skill entrypoints and specialist roles. The 2.8.1 refinement applies observed design and verification lessons without replacing working domains. Useful examples and tested helper implementations can remain after review; fresh instructions are not a reason to throw away working behavior. Historical reviews and old plans live under docs/history and do not define current policy. LICENSE and user media are preserved.

The shared problem-solving skill helps when a cause or tradeoff is uncertain: frame the contract, distinguish observations from assumptions, compare plausible explanations, choose an informative intervention and verify the actual failure path. Routine work does not require a new planning ritual.

## Design is a conversation

Before a new visual design, the agent briefly asks about style and references and waits. Already supplied preferences or an explicit “ikaw na bahala” settle the question; maintenance within an approved system does not ask again. The accepted direction controls composition, typography, imagery, color and motion. There is no aesthetic banlist, fixed image/layout quota or compulsory second theme.

[BrewedOps Motion Library](https://brewedops.cloud/motionlibrary/) is an optional source of motion/UI-pattern ideas, prompts and code examples in the reference options. It is not a package to install or an automatic effect layer. Inspect the selected pattern, adapt it to the actual stack, test interaction/reduced motion/performance, and follow the applicable [library terms](https://brewedops.cloud/motionlibrary/legal/license/) and third-party licenses. This kit links to the resource rather than republishing its collection.

## Custom-styled web components

Web controls default to a coherent, project-specific visual treatment, including relevant open, selected, focus and validation states. Native semantic HTML remains useful underneath. A styled select trigger does not make its OS-rendered options popup custom-designed; include the options surface in the custom treatment by default and exercise the visible control. Extend the existing accessible foundation, preserve purposeful platform interfaces and native-mobile conventions, and avoid forced libraries. Read [component guidance](skills/frontend-design/components.md) for these decisions and checks.

## Learn from rendered output

A paired light-dashboard test found both builds functionally correct while the original had better supporting-text legibility and tablet/table presentation. Passing kit or interaction checks did not predict visual quality. The refinement adds actual-size craft review, available-content-width decisions and discoverable essential data without imposing a font minimum or a fixed sidebar breakpoint.

For a requested before/after experiment, use [comparison-testing.md](skills/browser-verification/comparison-testing.md). Ordinary work keeps proportional checks. The optional ui_verify visual-review record validates recorded observations and width coverage; it cannot perceive screenshots or assign a design score. See [the dated evidence note](docs/reviews/2026-10-16-dashboard-comparison.md) for the observed result and limits.

## Capabilities

| Area | Typical work |
|---|---|
| Product and planning | Scope, requirements, flows, architecture, executable milestones and traceability |
| Web and mobile | Visual systems, native platform behavior, components, forms, responsive interaction and actual render checks |
| Backend and data | API contracts, identity/authorization, jobs, retries, transactions, schema and migrations |
| Quality and recovery | Root-cause diagnosis, behavior tests, measured performance, security review and scoped legacy modernization |
| Delivery | CI/deployment, operational health, documentation, exports, generated documents and motion deliverables |
| Kit health | Structural validation, source/installation comparison, active-rule diagnosis and backed-up installation |

Use the nearest role directly or delegate bounded independent work. Skills load progressively; do not load every reference for a small task. There is no universal requirement to adopt a framework, provider, ORM or component library.

## Install and check

The Windows installer uses PowerShell and Python. Run from the editable repository:

```powershell
.\install.ps1 -Check
python -B scripts/validate_kit.py . --strict
python -B -m unittest discover -s scripts/tests -v
.\install.ps1
python -B scripts/kit_doctor.py --json
```

The installer validates source and staging, backs up existing managed files and the global entrypoint, preserves unrelated rules, activates the plugin and validates it. A failed activation restores prior active files. `-ConfigRoot` and `-BackupRoot` support isolated tests. Source edits must be installed before they affect new sessions.

Restart Antigravity and open a new chat after activation. A file-health check cannot inspect instructions already loaded into a running chat.

`/doctor` is read-only: it reports source validity, installed version/file/rule drift, entrypoint problems and tool availability. It neither repairs configuration nor proves that a generated application works.

## Evidence instead of assurances

Source checks, configured test commands, browser interaction, document renders and production health establish different things. Report PASS, FAIL, INCOMPLETE or SKIPPED with the actual scope. Exit zero alone is not proof of complete evidence. Missing tools, unexecuted scenarios and unavailable integrations stay visible in the report.

The checks catch known problems; they cannot guarantee zero future errors, security or taste. Refine the kit from real outcomes without turning a single failure or example into a universal rule.

See AG_KIT_SLASH_COMMANDS.md for entrypoints, DECISIONS.md for current rationale, and CHANGES.md for release history. The completion report and coverage inventory record what was rebuilt and what was reviewed.
