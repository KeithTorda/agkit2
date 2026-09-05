---
name: brainstorm
description: "/brainstorm — Explores 2–4 approaches with trade-offs and recommends one before any code is written. Use when the user wants options, is unsure how to build something, or wants to compare architectures, libraries, or data models."
version: 2.0.0
---

# /brainstorm

**Input:** the text after `/brainstorm` is the topic. If it is empty, ask for the topic in one line.
**Agent:** read `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/project-planner.md`.
**Skills:** `@[skills/brainstorming]` (question format, option format); `@[skills/architecture]` when the topic is system design.

## Steps

1. **Frame.** Restate the problem in one paragraph: goal, user, constraints (stack, scale, deadline, existing code). Apply project memory if it was loaded; do not ask what memory, `docs/plans/`, or `DESIGN.md` already answer. Ask a clarifying question (per `core-protocol`) only when the topic is too vague to generate real options; otherwise start exploring.
2. **Diverge.** Produce 2–4 genuinely different approaches — not variants of one idea. For each: what it is, pros, cons, effort (low / medium / high), and when it fits. Include one option the user probably has not considered.
3. **Converge.** Recommend one option and tie the reasoning to a constraint you named in step 1. Name what would change the choice.
4. Close with the next step: `/plan <topic>` for a multi-file change or new app, `/enhance <topic>` for a small change in an existing app, `/remember <decision>` once the user decides.

## Output

```markdown
## Brainstorm: <topic>

### Context
<problem, user, constraints>

### Option A: <name>
<one paragraph>
Pros: ... · Cons: ... · Effort: Low | Medium | High · Fits when: ...

### Option B: <name>
...

### Recommendation
Option <X> because <reason tied to a constraint above>. Next: /plan <topic>
```

## Rules

- No code and no file changes; Mermaid diagrams are welcome for architecture.
- Every option lists at least one real con; hide no complexity.
- The user decides; do not start planning or building in the same turn.

## Verification

- Zero files written.
- Each option has pros, cons, effort, and a fit condition.
- The recommendation references a constraint from the Context section.
