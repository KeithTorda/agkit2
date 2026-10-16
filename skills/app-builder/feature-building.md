# Add a feature within the existing application

Find the closest working feature, route, data flow, permission model and tests. Read repository guidance and preserve uncommitted user work. Identify what the user should be able to do after the change and what visible or stored evidence establishes success.

Trace the complete path: entry action, client state, server validation, authorization, persistence/integration, response and feedback. Implement the feature through those boundaries rather than producing only a new screen with inert controls. Use existing components and contracts before creating competing abstractions.

Record a short plan for a simple change or a durable plan for substantial cross-cutting work. Resolve API/data ownership before parallel implementation. An optional integration or speculative feature should not expand the user's request.

New visual design follows the shared style/reference question and waits for its answer unless already supplied or delegated. A matching component or bug fix preserves the approved system without another intake. Inspect real content and affected empty/loading/error conditions rather than injecting a whole new visual system into a local feature.

Keep schema migrations forward-compatible where the deployment requires it. Consider duplicate requests, concurrency, permission denial and recoverable failures where the feature can encounter them. Do not introduce a database, provider, dependency or global store solely because a template uses one.

Run focused checks and exercise the actual feature, including relevant negative paths. Inspect changed UI in the appropriate renderer. If an external service or device cannot run, verify the reachable boundary and state the unverified part precisely. Report the resulting capability, meaningful decisions, actual validation and setup still needed.
