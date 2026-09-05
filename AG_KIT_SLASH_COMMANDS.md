# AG Kit v2 — Slash Commands & Skills Master Reference

A comprehensive guide to all slash commands, specialist skills, and IDE automation tools available in **AG Kit v2**.

---

## 🚀 1. The 11 Primary Workflow Commands

These are your day-to-day commands covering the complete software engineering lifecycle:

| Command | Purpose | When to Use & Example Scenario |
| :--- | :--- | :--- |
| **`/create`** | **End-to-End App Scaffolding** | **Starting a new project from scratch.** Conducts a brief requirements interview, builds a structured plan (`docs/plans/`), sets up `DESIGN.md` tokens, generates code via specialist agents, and boots a running dev server.<br>*Example: `"/create full-stack voter registration portal using Vite + React and Node.js"`* |
| **`/plan`** | **Architecture & Implementation Plan** | **Before touching code on complex or multi-file features.** Writes a verifiable breakdown to `docs/plans/{task-slug}.md` complete with task checkboxes, file ownership, and risk mitigations.<br>*Example: `"/plan how to integrate biometric authentication and offline voter caching"`* |
| **`/brainstorm`** | **Trade-Off & Approach Exploration** | **When deciding between competing technical paths.** Explores 2–4 concrete architectures, libraries, or data models with honest trade-offs and recommendations before writing code.<br>*Example: `"/brainstorm WebSockets vs Server-Sent Events (SSE) for live election precinct counts"`* |
| **`/debug`** | **Systematic 4-Phase Debugging** | **Investigating bugs, crashes, regressions, or failing tests.** Strictly follows the scientific method: Reproduce → Isolate → Root Cause → Regression Test & Fix (eliminates guess-and-check edits).<br>*Example: `"/debug map container crashes on mobile when tapping a barangay pin"`* |
| **`/verify`** | **Automated Quality & Pre-Commit Gate** | **Proving code works with hard evidence.** Executes the automated gate suite: security scans, linter, TypeScript compiler, automated tests, and production build check.<br>*Example: `"/verify verify that all changes compile and pass security gates"`* |
| **`/deploy`** | **Release & Production Shipping** | **Shipping code to staging or production servers.** Runs pre-flight checks, generates optimized bundles, uploads via SFTP/SSH, verifies live HTTP status, and handles rollbacks.<br>*Example: `"/deploy ship the latest build to Contabo VPS on port 8095"`* |
| **`/enhance`** | **Safe Feature Expansion** | **Adding or improving features in an existing codebase.** Analyzes existing architecture, conventions, and dependencies so the update integrates seamlessly without breaking legacy behavior.<br>*Example: `"/enhance add an export-to-PDF button for the precinct list"`* |
| **`/orchestrate`** | **Multi-Agent Coordination** | **Massive full-stack tasks spanning multiple domains.** Coordinates specialist subagents in parallel (Frontend, Backend, Database, Security) under single file-ownership isolation.<br>*Example: `"/orchestrate build voter registration with schema, API endpoints, and UI"`* |
| **`/test`** | **Automated Test Engineering** | **Generating, running, or fixing test suites.** Generates unit tests (Vitest/Jest), integration tests, and Playwright end-to-end browser automation suites with coverage reports.<br>*Example: `"/test write regression tests for the mobile dropdown selection"`* |
| **`/status`** | **Repository & Health Overview** | **Checking project progress without altering code.** Summarizes git status, recent file changes, required checklist health, open plan tasks, and active subagents.<br>*Example: `"/status give me a summary of all changes made this session"`* |
| **`/remember`** | **Persistent Project Memory** | **Saving conventions, preferences, or technical decisions.** Records notes directly into `.agents/memory/MEMORY.md` so the assistant retains context across future chat sessions.<br>*Example: `"/remember always serve COMELEC Flora through Nginx on Port 8095"`* |

---

## 🎨 2. Specialist Domain Commands

Every skill in the kit can be invoked directly as a slash command:

### 📱 Frontend, UI & Ergonomics
* **`/frontend-design`** – **Bespoke, Non-Templated UI.** Modern typography pairing, curated color palettes, visual density dials, and micro-interactions.
* **`/design-spec`** – **Design System Tokens.** Generates and synchronizes design tokens in `DESIGN.md` (colors, radius, shadows, spacing) mapped directly to Tailwind v4 `@theme`.
* **`/mobile-design`** – **Mobile-First UX.** Audits touch target sizes, bottom sheets, thumb-zone layout, and React Native / Flutter apps.
* **`/tailwind-patterns`** – **Tailwind CSS v4 Mechanics.** Implements CSS-first configuration, `@theme` token wiring, container queries, and dark variants.
* **`/nextjs-react-expert`** – **React 19 & Next.js Performance.** Eliminates waterfall fetches, configures React Compiler, and resolves re-rendering bottlenecks.
* **`/web-design-guidelines`** – **Vercel Web Interface Guidelines.** Audits UI code against industry best practices for accessibility, keyboard navigation, and form UX.

### 🛡️ Backend, Database & Security
* **`/api-patterns`** – **API Architecture.** Designs clean REST, tRPC, or GraphQL APIs with proper HTTP status codes, pagination, rate limiting, and idempotency headers.
* **`/database-design`** – **Schema Design & Query Optimization.** PostgreSQL / SQLite schema modeling, indexing strategies, UUIDv7 keys, and zero-downtime migrations (Prisma/Drizzle).
* **`/nodejs-best-practices`** – **Node.js 24 LTS.** Clean layered Hono/Fastify architecture, Zod schema validations, and async error-handling patterns.
* **`/python-patterns`** – **FastAPI / Django Backend.** Async endpoints, type annotations, Pydantic v2 schemas, and background worker queues.
* **`/vulnerability-scanner`** – **OWASP Top 10 Security Audit.** Scans for leaked secrets, SQL injection, XSS vulnerabilities, and supply-chain dependency risks.
* **`/red-team-tactics`** – **Authorized Security Simulation.** Threat modeling, penetration testing tactics, and defense posture assessment on your own environments.

### ⚡ Performance, SEO & Quality
* **`/clean-code`** – **Code Simplification & Refactoring.** Keeps functions under 30 lines, eliminates nesting, removes dead code, and reduces cognitive load.
* **`/performance-profiling`** – **Core Web Vitals & Speed.** Audits LCP, INP, and CLS metrics, optimizes bundle size, and profiles runtime memory.
* **`/seo-fundamentals`** – **Search Engine & AI-Answer Visibility.** Configures JSON-LD structured data, metadata tags, sitemaps, and GEO (Generative Engine Optimization).
* **`/i18n-localization`** – **Internationalization.** Manages locale translation files, ICU plurals, and RTL layouts without hardcoded UI strings.
* **`/shell-ops`** – **CLI & Server Operations.** Cross-platform PowerShell 7 scripts, Nginx configurations, Systemd services, and SSH administration.

---

## 🛠️ 3. Built-In IDE Automation Commands

Platform-level commands built into the Antigravity engine:

* **`/goal`** – **Autonomous Goal Mode.** Instructs the assistant to work continuously without stopping until a complex, long-running goal is 100% verified.
* **`/grill-me`** – **Interactive Interview Mode.** Thoroughly interrogates you with targeted technical questions to resolve ambiguities before coding begins.
* **`/schedule`** – **Timers & Recurring Cron Jobs.** Sets up one-time timers or scheduled background checks (e.g., checking deployment health every 30 minutes).
* **`/learn`** – **Habit & Workflow Retention.** Captures a solution or manual workflow correction to permanently persist as an assistant guideline.

---

## 🌟 4. The "Always-On" Rules (No Slash Command Needed)

These rules are permanently active and govern every response and code change:

1. **`engineering-excellence` (Always On):** Principal-engineer standard. Requires thinking before building, anticipating edge cases, hostile diff reviews, and evidence-based verification.
2. **`universal-rules` (Always On):** Respects your language, safety constraints (no hardcoded secrets, no destructive commands without asking), and Windows 11/PowerShell 7 host rules.
3. **`core-protocol` (Always On):** Enforces clean task routing, asking questions only when architectural divergence exists, and systematic execution phases.
