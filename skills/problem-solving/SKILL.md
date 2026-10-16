---
name: problem-solving
description: Investigate difficult defects or consequential decisions through contracts, competing explanations and discriminating evidence. Use when the cause or tradeoff is uncertain, not as a mandatory ritual for routine edits.
version: 2.8.2
---

# Evidence-led Problem Solving

Use this when a symptom has several plausible causes, an attempted fix keeps failing, or a choice will affect a costly contract. For a routine known repair, complete it directly using the relevant domain skill.

## Establish the contract

State the observable result needed and the conditions under which it must hold. Identify inputs, outputs, state transitions and the boundary that owns them. A visible symptom can originate elsewhere: a clipped table may be a parent constraint; a duplicate receipt may be a retry or transaction boundary; a stale view may be a cache key or read-model issue.

Read a small representative path end to end before changing it. Separate what you observed from what you inferred. Seek the actual failing input, route, environment, timing or state. Use a minimal reproduction or a focused trace rather than instrumenting the entire project by reflex. Protect secrets and private production data during diagnosis.

## Compare explanations

Form the plausible causes consistent with the evidence. Ask which observation would distinguish them most cheaply. A correct-looking change that cannot explain the previous failure is still uncertain.

| Situation | Useful next evidence |
|---|---|
| Only one device/width fails | Actual computed layout, content size and breakpoint behavior at that width |
| Request succeeds but state is wrong | Input validation, transaction result, emitted event and the reader's data source |
| Intermittent duplicate action | Retry identifiers, concurrent requests, uniqueness boundary and commit timing |
| Local works, deployed fails | Effective configuration/version/build and a sanitized failing input |
| New dependency or architecture choice | Required capability, existing alternative, compatibility, operating cost and rollback cost |

These are examples of discriminating evidence, not a mandatory checklist. Use the relevant domain reference to interpret the result.

## Choose a bounded intervention

Change the owning layer and the dependents necessary to keep the contract consistent. A small complete repair is preferable to a broad speculative rewrite. If the contract itself is wrong, explain the proposed correction and its consequence rather than hiding it behind a UI patch.

For a consequential choice, compare viable options against actual constraints and choose a path. Explain the tradeoff in ordinary language. Do not ask the user to choose implementation minutiae they have already delegated; do ask when the answer changes requirements or authorized external effects.

Preserve a way back for consequential operations. A backup, migration rollback, transaction, feature flag or isolated reproduction is useful when it addresses a real failure mode; do not add infrastructure merely because a checklist names it.

## Verify the explanation

Reproduce the original failure after the change and check a relevant neighboring/error case. Choose evidence that would fail if the proposed cause were still present. A unit test, compiler, browser observation and production health check establish different things.

If the intervention fails, record what that ruled out and revise the explanation. Avoid stacking unrelated changes or repeating the same attempt without new evidence. A deeper unknown or unavailable environment should be reported precisely, with whatever useful work can still be completed.

Deliver the result with the important causal finding, actual verification and remaining uncertainty. Preserve a durable lesson only through requested/authorized project memory. A solved example is not a universal rule for every later project.
