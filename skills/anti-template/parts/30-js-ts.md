---
part: 30
title: JavaScript and TypeScript reliability
covers: abstraction, types, errors, validation, async, cleanup, logging, retries, helpers, mocks, numeric and locale handling
---

# 30 - JavaScript and TypeScript reliability

Read for application logic, scripts, shared helpers, and non-framework-specific code. Evaluate behavior and maintainability rather than whether syntax resembles generated code.

## Keep abstractions useful

Use a function, module, class, or service where it clarifies a real responsibility, state lifecycle, or reusable contract. A small direct implementation may be easier to maintain than several forwarding layers. Conversely, do not ban a class or factory when the framework or domain benefits from it. Follow project conventions unless they cause a concrete problem.

Name data and functions from their domain. A helper should have a clear responsibility and call site; related helpers may live together. A `utils` folder is not intrinsically wrong, but an unrelated dumping ground is hard to discover. Avoid inventing generic frameworks for one short task.

Comments should explain invariants, reasons, compatibility constraints, or non-obvious behavior. Useful docstrings are welcome; avoid repeating every statement. Tone, symbols, or emoji in a comment do not determine correctness, though output must remain readable in its actual environment.

## Types and validation

Use types that express actual contracts. `unknown` plus narrowing is useful for untrusted values; `any` may be necessary at a bounded interoperability point but should not hide uncertainty throughout the code. A cast does not validate runtime input. Validate external data where the trust boundary requires it.

Model states so impossible combinations are difficult to construct. Avoid parallel booleans that can contradict one another when a discriminated union or explicit status is clearer. Do not add defensive checks that silently disguise a programming error as valid data. Distinguish optional values, missing records, invalid input, and failed requests.

## Errors and asynchronous behavior

Catch errors where the code can recover, add useful context, translate a boundary response, or perform cleanup. Do not swallow failures or return fake success. Preserve causes for diagnosis while keeping user output safe. A broad catch that logs and continues may be valid for an optional best-effort task if the failure is deliberate and observable.

Await work that must complete; avoid async array methods whose promises are ignored. Choose sequential or parallel execution from dependencies, rate limits, and side effects. Cancellation and stale-response handling matter for changing queries or unmounted views. Use `finally` or structured cleanup for resources and pending state.

Retries need a bounded policy, delay/backoff, and an idempotency strategy for side effects. Choose attempts and timeouts from the service and risk; do not impose a universal count. A failed request that may already have charged a customer requires reconciliation rather than blind retry.

## Timers, listeners, logging, and security

Clean up intervals, timeouts, observers, event listeners, subscriptions, and animation instances at their lifecycle boundary. Prevent overlapping polling and stale updates. Respect document visibility and connection state where material.

Use the project's logger and levels. Debug output can be useful during development, but do not ship accidental dumps of private data. Never log secrets, passwords, tokens, OTPs, authorization headers, or unnecessary personal records. Do not insert untrusted strings into HTML; template literals do not prevent XSS. Use safe DOM/text APIs, framework escaping, and an appropriate sanitizer where HTML is genuinely required.

## Real implementations and data handling

Mock data and stub services are useful for explicit prototypes and tests. Isolate and label them; do not report a placeholder save, auth, export, or payment as working. Handle configuration absence honestly rather than silently activating a fake production path.

Use integer minor units or a decimal strategy for financial calculation. Keep identifiers and phone numbers as strings. Use explicit locale/time-zone formatting, and distinguish instants from date-only values. Test rounding, invalid input, boundaries, and concurrent updates where the feature depends on them.

## Review

Run the relevant checks for changed behavior. Inspect rejection paths, partial completion, cleanup, race conditions, retries, exact values, and security boundaries. Formatting preferences alone are not functional defects.
