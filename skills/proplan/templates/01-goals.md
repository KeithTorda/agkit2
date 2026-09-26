---
doc: 01-goals
project: <slug>
version: 0.1.0
status: draft
owner: product-manager
updated: YYYY-MM-DD
---

<!--
Owner: product-manager (Phase 1).
IDs defined here:
  G-01, G-02 ...   business goals (two digits). Define each as a heading: "### G-01 Faster checkout".
  DG-01 ...        development goals: engineering and quality targets the team commits to.
  KPI-01 ...       success metrics, defined as the first cell of the metrics table.
Rules:
- Every G must be traced by at least one requirement in 02 (the checker fails otherwise). A goal nothing serves is either missing requirements or not a goal.
- Goals are SMART: specific, measurable (a number and a baseline), achievable, relevant to the client, time-bound. "Improve the user experience" is not a goal; "median checkout time 45 s or less by the second week after launch (baseline 90 s)" is.
- 2-5 business goals is normal for a small system. More usually means features written as goals.
- Development goals are the engineering promises: test coverage, performance budgets, accessibility level, uptime, security baseline, maintainability. Each should be picked up by an NFR in 02 (write "Traced by NFR-xx").
-->

# Goals

## Problem

<!-- What hurts today, for whom, and how you know. Use numbers you measured or the client gave (time per order, errors per month, hours spent). State the source. -->

## Business goals

<!-- One heading per goal. Keep the four lines; they make the goal testable after launch. -->

### G-01 <Short goal name>

- Target:
- Baseline:
- Deadline:
- Measured by:

## Development goals

<!--
Pick what matters for this system; skip what does not. Typical set:
- Tested logic: line coverage on the modules money, auth or data integrity depend on (e.g. 80%), and one feature test per Must requirement.
- Performance budget: e.g. LCP 2.5 s or less on a mid-range phone over 4G; API p95 300 ms or less; a key interaction 100 ms or less.
- Accessibility: WCAG 2.2 AA for public and staff screens (AAA only if the client needs it).
- Availability: e.g. 99.5% monthly for a cloud app; "works offline for 8 h" for a counter system; planned maintenance window.
- Security baseline: OWASP ASVS level 1 (level 2 for money or personal data at scale), no High findings open at release.
- Maintainability: one-command setup, CI on every push, README runbook, dependency update routine.
- Operability: backups with a tested restore, RPO/RTO stated, alerts to a named person.
-->

### DG-01 <Short development goal>

<!-- One or two sentences with a number. End with "Traced by NFR-xx." -->

## Success metrics

<!-- How each goal is measured after launch. Source must be something the system or the client already records. -->

| KPI | Metric | Source | Target | Review |
|---|---|---|---|---|
| KPI-01 | | | | |

## Non-goals

<!-- Outcomes the client might expect but this plan does not promise (e.g. "increase sales"; the system can only make checkout faster). Prevents scope creep later. -->
