---
name: brainstorm
description: "/brainstorm - Explores 2-4 genuinely different approaches with trade-offs and recommends one before any code is written. Use when the user wants options, is unsure how to build something, or wants to compare architectures, libraries or data models."
version: 2.5.0
---

# /brainstorm

**Input:** the text after `/brainstorm` is the topic. If empty, ask for it in one line.
**Read now:** `KIT/skills/brainstorming/SKILL.md` (framing, option format). System design topics: also `KIT/skills/architecture/SKILL.md`.

## Steps

1. **Frame** the goal, user and constraints (stack, scale, budget, deadline, existing code). Do not ask what memory, `docs/plans/`, `DESIGN.md` or the code already answer.
2. **Diverge** to 2-4 real options with pros, cons, effort and fit, per `brainstorming`. Include one the user probably has not considered.
3. **Converge** on one, tied to a named constraint; say what would change the choice.
4. **Hand off:** `/plan <topic>` or `/proplan <system>` for bigger work, `/enhance` for a small change, `/remember <decision>` once decided.

No code and no file changes. Mermaid diagrams are fine. The user decides; do not start building in the same turn.

## Output

```markdown
## Brainstorm: <topic>
Context: <goal, user, constraints>

### A: <name>
<what it is> · Pros: ... · Cons: ... · Effort: low | medium | high · Fits when: ...
### B: <name>
...

Recommendation: <X>, because <constraint>. Changes if <condition>.
Next: /plan <topic>
```
