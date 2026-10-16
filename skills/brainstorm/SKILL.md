---
name: brainstorm
description: "Explore credible approaches and recommend one from the user's constraints. Use /brainstorm for options and tradeoffs before committing to implementation."
version: 2.8.2
---

# /brainstorm

Use the topic after the command. Read `KIT/skills/brainstorming/SKILL.md`; add `architecture` only for system-boundary decisions.

Frame the outcome, existing constraints and evidence. Compare as many genuinely different approaches as the decision needs, including keeping the current approach when credible. For each, explain how it works, its main benefit, cost and limitation. Recommend a choice tied to the constraints and state what evidence would change it.

If the request is exploration-only, finish with the recommendation and any unresolved decision; do not edit code. If the user also authorized implementation, continue after the relevant decision is settled. For a new visual design, the style/reference conversation in design-rules still applies; do not turn brainstorming into a compulsory questionnaire.

Present options in a compact table or short prose. Separate facts from estimates and assumptions. Do not save decisions to memory unless requested or an authorized project workflow calls for it.
