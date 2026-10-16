# Coordinate only useful specialist work

Use the available delegation mechanism when independent work would improve quality or reduce time. A single agent can complete a small feature. Do not assume a particular subagent tool exists, force a fixed specialist pipeline, or create user-visible chats as an implementation detail.

Before delegation, establish the request, accepted direction, ownership and shared contracts. For new visual work one coordinator asks the short style/reference question and waits; specialists reuse that answer. Pass context rather than asking the user the same question again.

Useful boundaries include data/schema, backend contract, UI built against that contract, focused tests, or independent review. Parallelize only when dependencies are resolved. Two agents editing the same shared shell or token source need explicit coordination; more agents are not automatically faster.

Each assignment should include:

- Requested outcome and acceptance conditions.
- Relevant current files, constraints and accepted design decisions.
- Files or module boundary owned by that worker, with shared interfaces.
- What may be mocked and how it must be labeled.
- Relevant validation and the expected evidence/limitations in the return.

Integrate returned work: inspect edits, resolve interface mismatch, run affected checks and exercise the combined flow. A worker's “done” is not proof that all components run together. Add a security, performance or accessibility specialist when the change has a material concern or that review is requested; do not turn every small feature into a universal audit.

The coordinating agent remains responsible for a coherent result and honest completion report. Follow the environment's authorization rules for external communication, publishing, deployment or production data changes.
