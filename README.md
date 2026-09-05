# AG Kit v2 (agkit2)

> **The Principal-Engineer Toolkit for Google Antigravity**  
> 17 specialist agents, 40 workflow skills, 11 primary slash commands, 23 automated audit & verification scripts, and always-on engineering excellence.

Maintained by [@KeithTorda](https://github.com/KeithTorda). Based on `vudovn/ag-kit`, rebuilt for a modern, high-performance global Antigravity environment.

---

## ⚡ Key Highlights

* **17 Specialist Agents:** Dedicated personas for Frontend, Mobile, Backend, Database Architecture, Security Auditing, Performance Optimization, Devops, and Orchestration.
* **11 Primary Slash Commands:** `/create`, `/plan`, `/brainstorm`, `/debug`, `/verify`, `/deploy`, `/enhance`, `/orchestrate`, `/test`, `/status`, `/remember`.
* **Always-On Engineering Excellence:** Enforces principal-engineer design standards, failure anticipation, hostile diff reviews, and evidence-based verification on every response.
* **Automated Quality Gates:** Integrated Python verification suite (`scripts/checklist.py`) testing security vulnerabilities, types, linting, and automated tests.
* **Modernized Stack (2026 Baseline):** Next.js 16 / React 19 compiler-first, Tailwind CSS v4 `@theme`, `motion/react`, Node.js 24 LTS, Python 3.14, and OWASP Top 10 security scanning.

---

## 🚀 Quick Installation

To install **AG Kit v2** into your global Antigravity configuration on Windows:

### Option A: Automated PowerShell Setup (Recommended)
Run the included `install.ps1` script:
```powershell
.\install.ps1
```

### Option B: Manual Installation
1. Copy the plugin contents into your Antigravity plugins directory:
   ```powershell
   Copy-Item -Path ".\*" -Destination "$env:USERPROFILE\.gemini\config\plugins\ag-kit-v2" -Recurse -Force -Exclude "rules", ".git", "install.ps1", "README.md"
   ```
2. Copy the rules into your Antigravity rules directory:
   ```powershell
   Copy-Item -Path ".\rules\*" -Destination "$env:USERPROFILE\.gemini\config\rules" -Recurse -Force
   ```
3. Run the self-validation script to verify integrity:
   ```powershell
   python "$env:USERPROFILE\.gemini\config\plugins\ag-kit-v2\scripts\validate_kit.py"
   ```

---

## 📋 Slash Commands Summary

| Command | Purpose |
| :--- | :--- |
| **`/create`** | Scaffolds a complete project from scratch (interview, plan file, `DESIGN.md`, dev server). |
| **`/plan`** | Writes a technical implementation roadmap to `docs/plans/{task-slug}.md` before writing code. |
| **`/brainstorm`** | Compares 2–4 architectural approaches with honest trade-offs and recommendations. |
| **`/debug`** | 4-phase systematic debugging: Reproduce → Isolate → Root Cause → Regression Test & Fix. |
| **`/verify`** | Runs security scans, types, linter, tests, and build check to prove code works with evidence. |
| **`/deploy`** | Runs pre-flight checks, bundles assets, and deploys via SSH/SFTP with health verification. |
| **`/enhance`** | Safely adds or refactors features in an existing codebase without breaking legacy behavior. |
| **`/orchestrate`** | Splits multi-domain full-stack work across parallel specialist subagents. |
| **`/test`** | Generates, executes, and fixes unit, integration, and Playwright E2E test suites. |
| **`/status`** | High-level summary of repo health, git changes, and checklist states without touching code. |
| **`/remember`** | Persists decisions and conventions to `.agents/memory/MEMORY.md` across chat sessions. |

For detailed guidance on specialist domain skills (e.g. `/frontend-design`, `/database-design`, `/vulnerability-scanner`), check out [`AG_KIT_SLASH_COMMANDS.md`](./AG_KIT_SLASH_COMMANDS.md).

---

## 📂 Repository Structure

```
agkit2/
├── agents/                       # 17 specialist agent markdown files
├── skills/                       # 40 modular workflow skills (frontend, backend, security, etc.)
├── scripts/                      # 23 automated Python verification & audit scripts
│   ├── checklist.py              # Required P0–P4 fast verification gate
│   ├── validate_kit.py           # Self-validation script for toolkit integrity
│   └── build_quick_reference.py  # Auto-generates quick-reference rule
├── rules/                        # Global Antigravity rules
│   ├── engineering-excellence.md # Always-on thinking & quality guidelines
│   ├── core-protocol.md          # Task routing, execution phases, and gates
│   ├── request-routing.md        # Natural language classifier to specialist agents
│   ├── code-rules.md             # Required vs advisory verification policy
│   ├── design-rules.md           # DESIGN.md token gate & UI ownership
│   └── universal-rules.md        # Safety, language, and host conventions
├── plugin.json                   # Antigravity plugin manifest
├── CHANGES.md                    # Detailed migration & optimization changelog
├── DECISIONS.md                  # Kit design rationale & policy definitions
├── AG_KIT_SLASH_COMMANDS.md      # Comprehensive cheatsheet for slash commands
├── install.ps1                   # One-click Windows PowerShell installer
└── VERSION                       # Semantic version (2.0.0)
```

---

## 🛠️ Verification & Maintenance

Validate the entire toolkit after modifying agents or skills:
```bash
# 1. Run toolkit self-validation
python scripts/validate_kit.py

# 2. Re-generate quick reference catalog
python scripts/build_quick_reference.py --write

# 3. Run toolkit unit tests
python scripts/tests/test_toolkit.py
```

---

## 📜 License & Credits

* Based on [vudovn/ag-kit](https://github.com/vudovn/ag-kit).
* Maintained, optimized, and modernized by [Keith Torda](https://github.com/KeithTorda).
* MIT License.