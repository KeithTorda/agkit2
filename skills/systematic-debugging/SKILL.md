---
name: systematic-debugging
description: Diagnose bugs, crashes and inconsistent behavior through reproduction, competing hypotheses and causal evidence, then verify a bounded repair. Use when a failure's cause is unclear or a proposed fix needs validation.
version: 2.8.2
---

# Systematic Debugging

Reduce uncertainty until a change has a defensible causal link to the failure. A fixed number of phases or repeated speculative edits is less useful than one observation that distinguishes hypotheses.

## Establish the failure

Capture expected versus observed behavior, a concrete input/action, environment/version and relevant error. Use the smallest repeatable case available. Preserve useful logs and the current state before changing dependencies, deleting caches or rewriting code.

If reproduction is unavailable, use production traces, a user-provided artifact, code-path reasoning or a controlled simulation. Label the limitation; lack of reproduction does not justify pretending a diagnosis is confirmed or abandoning all useful investigation.

## Locate the broken boundary

Trace the value/event across input, state, service and output. Ask where it first differs from the contract. Compare a working/failing case, inspect callers/configuration and check recent relevant changes. Binary search or `git bisect` can isolate a regression when the workspace and test support it; protect unrelated work.

List materially different hypotheses with evidence for/against them and a discriminating check. Example: a blank result may be a failed request, wrong filter, unauthorized response or stale UI state. Inspect status/body and state before changing CSS or adding retries.

Use narrow instrumentation with redacted values, correlation IDs and timestamps where they help. Avoid dumping secrets or large datasets. A cache-clear fixing symptoms does not establish the root cause of stale data.

## Repair the cause within scope

State why the observed path fails and which invariant the change restores. Apply the smallest coherent fix, updating relevant consumers/configuration. Expected boundary errors may need handling, but a broad catch returning fake success hides the defect. Retry only when failure semantics make it safe.

For intermittent/concurrent failures, consider stale closures, duplicate work, ordering, clocks, resources and transaction isolation. Test relevant timing explicitly rather than replacing the entire subsystem.

## Verify and stop with evidence

Re-run the original reproduction or its best available substitute. Check a meaningful neighboring success/error path and add regression coverage when it will prevent a real recurrence. Verify shared callers when the contract changed. Do not write a test that only asserts the new implementation shape.

Review the final diff for leftover instrumentation, accidental changes and weakened validation. Report cause, fix, evidence and any unverified condition. Once the relevant checks pass, further repeated testing needs a new concern, failure or change.

Use `testing-patterns` for regression design, `performance-profiling` for measured slowness, and `shell-ops` for safe environment/process diagnosis.
