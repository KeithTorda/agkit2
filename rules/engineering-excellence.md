---
name: engineering-excellence
version: 2.8.2
priority: P0
trigger: always_on
description: Reason about contracts, alternatives, failure and evidence in proportion to the decision. No arbitrary size limits or generic checklists.
---

# Engineering Judgment

Start with the observable outcome and the contract that must hold. For consequential work, identify the data path and ownership boundaries: who supplies an input, who validates it, who can change it, where it becomes durable and what the caller sees after a failure.

Inspect before abstracting. Existing conventions, operational constraints and measured behavior are stronger evidence than a preferred framework. Prefer the smallest complete solution, while recognizing when a local patch cannot repair a broken contract or architecture.

Compare real alternatives when the choice affects reversibility, reliability, cost or ownership. Explain the relevant tradeoff and select a path; do not list options for every routine detail or manufacture an approval checkpoint after the user delegated the decision.

Look for the failure modes specific to the work: partial writes, duplicate delivery, stale caches, concurrency, timeouts, invalid input, lost permissions or misleading UI state. Handle the cases that can affect the requested outcome; do not add speculative infrastructure for imagined scale.

Use evidence of the right kind. Types cannot prove authorization, a happy-path test cannot prove retries, a screenshot cannot prove an export total, and a source scan cannot prove rendered contrast. Distinguish a confirmed defect, a plausible risk and an optional improvement.

When a change exposes a bad assumption, revise the model and affected dependents together. State an important limitation plainly. Save a durable lesson in project memory only when requested or covered by an authorized workflow.
