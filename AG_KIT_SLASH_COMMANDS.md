# AG Kit v2 — Slash Commands & Skills Master Reference

A comprehensive guide to all slash commands, specialist skills, and IDE automation tools available in **AG Kit v2**.

---

## 1. Primary Workflow Commands (15 Commands)

These are your core commands covering the complete software engineering lifecycle:

| Command | Purpose | When to Use & Example Scenario |
| :--- | :--- | :--- |
| `/create` | End-to-End Project Scaffolding | **Starting a new project from scratch.** Conducts a brief requirements interview, builds a structured plan (`docs/plans/`), sets up `DESIGN.md` tokens, generates code via specialist agents, and boots a running dev server.<br>*Example: `"/create full-stack voter registration portal using Vite + React and Node.js"`* |
| `/plan` | Architecture & Implementation Blueprints | **Before touching code on complex or multi-file features.** Writes a verifiable breakdown to `docs/plans/{task-slug}.md` complete with task checkboxes, file ownership, and risk mitigations.<br>*Example: `"/plan integrate biometric authentication and offline voter caching"`* |
| `/brainstorm` | Trade-Off & Approach Exploration | **When deciding between competing technical paths.** Explores 2–4 concrete architectures, libraries, or data models with honest trade-offs and recommendations before writing code.<br>*Example: `"/brainstorm WebSockets vs Server-Sent Events (SSE) for live election precinct counts"`* |
| `/debug` | Systematic 4-Phase Debugging | **Investigating bugs, crashes, regressions, or failing tests.** Strictly follows the scientific method: Reproduce → Isolate → Root Cause → Regression Test & Fix (eliminates guess-and-check edits).<br>*Example: `"/debug map container crashes on mobile when tapping a barangay pin"`* |
| `/fix-ui` | Container-First UI Layout Repair | **Diagnosing and fixing existing web UI that renders wrong.** Locates parent layout mode and computed box model, names 1 of 8 root causes, fixes container at source without layout overrides (`!important` or hack wrappers).<br>*Example: `"/fix-ui sidebar overlaps main content area on tablet breakpoint"`* |
| `/verify` | Automated Quality & Pre-Commit Gate | **Proving code works with hard evidence.** Executes the automated gate suite: security scans, linter, TypeScript compiler, automated tests, and production build check.<br>*Example: `"/verify ensure all changes compile and pass security gates"`* |
| `/see` | Live Browser UI & Visual Render Verification | **Verifying UI before declaring done.** Opens the live application in a headless browser to inspect rendered DOM, computed CSS tokens against `DESIGN.md`, console errors, and interaction responsive states.<br>*Example: `"/see verify the login card and student roster table in dark mode"`* |
| `/see-doc` | Visual Document & PDF Inspection | **Verifying generated downloadable documents before declaring done.** Renders PDFs, checks embedded fonts, glyph integrity, form bounds, margin clearances, and visual diffs against official templates.<br>*Example: `"/see-doc verify voter certificate PDF and official ballot margin bounds"`* |
| `/review` | Adversarial Diff & Blast Radius Review | **Hostile code review before PR or deployment.** Attacks the current diff hunting for untested edges, unhandled errors, race conditions, security vulnerabilities, and logic flaws.<br>*Example: `"/review check the authentication middleware refactor for security holes"`* |
| `/deploy` | Release & Production Shipping | **Shipping code to staging or production servers.** Runs pre-flight checks, generates optimized bundles, uploads via SFTP/SSH, verifies live HTTP status, and handles rollbacks.<br>*Example: `"/deploy ship the latest build to VPS on port 8095"`* |
| `/enhance` | Safe Brownfield Feature Expansion | **Adding or improving features in an existing codebase.** Analyzes existing architecture, conventions, and dependencies so the update integrates seamlessly without breaking legacy behavior.<br>*Example: `"/enhance add an export-to-PDF button for the precinct list"`* |
| `/orchestrate` | Multi-Agent Subagent Coordination | **Large full-stack tasks spanning multiple domains.** Coordinates specialist subagents in parallel (Frontend, Backend, Database, Security) under single file-ownership isolation.<br>*Example: `"/orchestrate build voter registration with schema, API endpoints, and UI"`* |
| `/test` | Automated Test Engineering | **Generating, running, or fixing test suites.** Generates unit tests (Vitest/Jest/Pest), integration tests, and Playwright end-to-end browser automation suites with coverage reports.<br>*Example: `"/test write regression tests for the mobile dropdown selection"`* |
| `/status` | Repository Health & Diff Assessment | **Checking project progress without altering code.** Summarizes git status, recent file changes, required checklist health, open plan tasks, and active subagents.<br>*Example: `"/status give me a summary of all changes made this session"`* |
| `/remember` | Persistent Project Memory Index | **Saving conventions, preferences, or technical decisions.** Records notes directly into `.agents/memory/MEMORY.md` so the assistant retains context across future chat sessions.<br>*Example: `"/remember always serve COMELEC Flora through Nginx on Port 8095"`* |

---

## 2. Specialist Domain Skills (34 Skills)

Every skill in the kit can be referenced directly during conversation or invoked via prompt context:

### Frontend, UI & Ergonomics
- **`frontend-design`**: Bespoke, non-templated UI. Typographic pairings, curated palettes, visual density dials, and micro-interactions.
- **`ui-repair`**: Root-cause UI layout diagnosis (8 structural causes, container constraints, never overrides).
- **`css-architecture`**: Single token source, cascade layers, co-located component styles, override ban as a method.
- **`browser-verification`**: Headless browser verification engine backing the `/see` command.
- **`design-spec`**: Generates and synchronizes design tokens in `DESIGN.md` (colors, radius, shadows, spacing) mapped directly to Tailwind v4 `@theme`.
- **`mobile-design`**: Audits touch target sizes, bottom sheets, thumb-zone layout, and React Native / Flutter apps.
- **`tailwind-patterns`**: Tailwind CSS v4 mechanics, CSS-first configuration, `@theme` token wiring, container queries, and dark variants.
- **`nextjs-react-expert`**: React 19 & Next.js 16 performance, waterfall fetch elimination, React Compiler integration, and re-rendering optimization.
- **`web-design-guidelines`**: Audits UI code against Vercel Web Interface Guidelines for accessibility, keyboard navigation, and form UX.
- **`frontend-architecture`**: Organizes frontend code by responsibility (UI, logic, data, types, validation) with React 19 / Next.js Server Components.

### Backend, Database & Security
- **`api-patterns`**: REST, tRPC, or GraphQL APIs with proper HTTP status codes, pagination, rate limiting, and idempotency headers.
- **`database-design`**: PostgreSQL / SQLite schema modeling, indexing strategies, UUIDv7 keys, and zero-downtime migrations (Prisma/Drizzle/Eloquent).
- **`document-generation`**: Standards for downloadable files: spreadsheet exports (CSV, XLSX), official PDFs (receipts, certificates, invoices, official forms), and editable Word documents (DOCX).
- **`nodejs-best-practices`**: Node.js 24 LTS layered Hono/Fastify architecture, Zod schema validations, and async error handling.
- **`python-patterns`**: Python 3.14 async endpoints, type annotations, Pydantic v2 schemas, and background worker queues.
- **`vulnerability-scanner`**: Scans for leaked secrets, SQL injection, XSS vulnerabilities, and supply-chain dependency risks against OWASP Top 10:2025.
- **`red-team-tactics`**: Threat modeling, penetration testing tactics, and defense posture assessment on authorized environments.
- **`mcp-builder`**: Model Context Protocol (MCP) servers and clients under the 2026 spec.

### Performance, SEO, Reliability & Infrastructure
- **`clean-code`**: Pragmatic coding standards: functions under 30 lines, nesting depth max 3, no dead code, self-documenting identifiers.
- **`performance-profiling`**: Audits Core Web Vitals (LCP, INP, CLS), bundle size analysis, and runtime memory profiling.
- **`seo-fundamentals`**: JSON-LD structured data, metadata tags, sitemaps, and Generative Engine Optimization (GEO) for AI search engines.
- **`i18n-localization`**: Locale translation files, ICU plurals, and RTL layouts without hardcoded UI strings.
- **`shell-ops`**: Cross-platform PowerShell 7 scripts, Nginx configurations, Systemd services, and SSH administration.
- **`testing-patterns`**: AAA unit tests, mocking conventions, Pest/PHPUnit, and Playwright E2E suites.
- **`systematic-debugging`**: Scientific 4-phase debugging method backing the `/debug` command.
- **`verify-changes`**: Underlying runtime verification logic backing the `/verify` command.
- **`adversarial-review`**: Hostile diff analysis backing the `/review` command.
- **`parallel-agents`**: Subagent coordination mechanics backing the `/orchestrate` command.
- **`architecture`**: Architecture decision records (ADRs) and pattern trade-off matrices.
- **`plan-writing`**: Implementation plan format and verification checklist generation.
- **`memory-system`**: Persistent repository memory structure and recall algorithms.
- **`app-builder`**: Application scaffolding engine backing `/create`.
- **`brainstorming`**: Divergence and convergence methodology backing `/brainstorm`.

---

## 3. Native Platform Automation Commands

Platform-level commands provided by the Antigravity engine:

- **`/goal`**: Autonomous Goal Mode. Instructs the assistant to work continuously without stopping until a complex, long-running goal is 100% verified.
- **`/grill-me`**: Interactive Interview Mode. Thoroughly interrogates you with targeted technical questions to resolve ambiguities before coding begins.
- **`/schedule`**: Timers & Recurring Schedules. Sets up one-time timers or recurring background checks.
- **`/learn`**: Habit & Pattern Retention. Captures a solution or manual workflow correction to permanently persist as an assistant guideline.

---

## 4. The 7 Core Global Rules

The kit ships with 7 invariant rules located in `~/.gemini/config/rules/` that govern every response:

1. **`core-protocol.md`**: The ordered 9-step execution procedure required on every code request.
2. **`code-rules.md`**: The definition of "Done", blocking gates (security high+, lint, types, tests), and the UI-render gate (`/see`).
3. **`design-rules.md`**: The Ultra High-Contrast Typography & Badges standard (Anti-Blur Invariant) and project `DESIGN.md` gate.
4. **`engineering-excellence.md`**: The principal-engineer bar: solve the problem behind the words, anticipate failure, and prove before claiming.
5. **`request-routing.md`**: Classifies prompts into 7 types and routes to the owning specialist agent.
6. **`universal-rules.md`**: Direct, professional communication, memory recall, host environment conventions, and safety boundaries.
7. **`quick-reference.md`**: Auto-generated catalog mapping keywords to agents, skills, and audit scripts.
