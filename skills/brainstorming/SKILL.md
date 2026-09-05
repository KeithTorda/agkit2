---
name: brainstorming
description: Clarifies requirements and explores options before building. Covers how to write a question that changes the implementation, and how to diverge to several real approaches then converge on one with stated trade-offs. Use for new apps, multi-file features, vague requests, design discussions, and /brainstorm.
version: 2.0.0
---

# Brainstorming

> Understand before building. Ask little, ask well; widen the option space before you narrow it.

## When to ask

The questions policy lives in the always-on `core-protocol` rule — follow it there, and never impose a question floor.

This skill is the craft on top of that rule: deciding which questions are worth asking, and how to explore once you have the answers.

Before asking anything, spend the cheap information first — project memory (`@[skills/memory-system]`), `docs/plans/*.md`, `DESIGN.md`, and the code. A question those already answer is wasted.

## How to ask

A question earns its place only by eliminating at least one implementation path. "Which database?" is preference-fishing; "Do orders and inventory need to update in one transaction, or is eventual consistency fine?" forces a choice that changes the data model, the ORM, and the hosting. Principles, generation steps, and domain question banks: [dynamic-questioning.md](./dynamic-questioning.md).

Format — one message, ordered by leverage, every question carrying a default so work proceeds on "proceed":

```markdown
**1. <decision point>** — <question>
Why it matters: <what in the build changes with the answer>
Options: A <pro / con> · B <pro / con>
Default if unanswered: <choice + reason>
```

## Exploring options (/brainstorm, design discussions)

Diverge, then converge. Do not anchor on the first idea that works.

1. **Frame.** Restate the real goal, the user, and the hard constraints (budget, deadline, the stack already in place, scale). Name the problem behind the request, not its literal words.
2. **Diverge.** Put 2–4 genuinely different approaches on the table — not one plan and two strawmen. For each: one-line description, main pro, main con, effort (low / medium / high), and when it fits.
3. **Converge.** Recommend one and tie the reason to the constraints from step 1. A recommendation with no constraint behind it is a guess, not advice.
4. **Hand off.** Let the user decide, then offer `/remember <decision>` and `/plan <topic>`.

No code during exploration; diagrams welcome.

One suggestion is not brainstorming — surface the trade-off the user should own:

```text
Weak:   "I'll build notifications with WebSockets."
Strong: "Notifications three ways: polling (trivial, ~30s lag, fine under ~1k users) ·
         SSE (one-way push, cheap, no client library) · WebSockets (bidirectional,
         needs connection management and scaling). You have ~800 users and no live
         chat, so SSE — move to WebSockets only if you add real-time collaboration."
```

## Anti-patterns

| Avoid | Because |
|---|---|
| A question whose answer would not change the build | Cost with no information |
| Asking again after "proceed" | One round, then defaults (see `core-protocol`) |
| One option presented as the only way | Hides the trade-off the user should own |
| Converging on the first approach that works | Skips the alternative that fits better |
| Silently assuming an unstated requirement | Wrong output; state the assumption instead |
