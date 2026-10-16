# Questions that change a decision

Use this reference when the request leaves a consequential ambiguity. It supplements [SKILL.md](./SKILL.md), not a mandatory interview script.

## Decide whether to ask

First inspect the brief, accepted choices and relevant current files. Then name what would change with each plausible answer. If the answer would not change the deliverable or an important constraint, use a sensible implementation choice and continue.

Ask now for product commitments, missing permission/data boundaries, incompatible constraints or expensive-to-reverse choices. Defer details until the affected work is near. Do not ask the user to select a database, library or storage vendor merely because several exist; explain the consequential requirement instead.

New visual designs have a specific user preference: ask one conversational question about style and references and wait unless that answer or explicit delegation already exists. Example: “Anong style ang gusto mo, at may site o screenshot kang reference? Puwede rin akong pumili kung gusto mo.” Do not repeat this intake for each screen, worker or repair within the approved direction.

## Useful question shape

Give enough context to make the choice understandable: the decision, why it affects the outcome, credible alternatives if helpful and a recommendation. A conversational sentence often does this better than a numbered questionnaire. A proposed default is not accepted through silence; an explicitly delegated choice is sufficient.

| Context | Ask about the consequence | Avoid premature machinery |
|---|---|---|
| Orders/inventory | Must a sale reserve stock immediately, or can staff resolve a shortage later? | “Which database do you want?” |
| Offline tool | Which tasks must continue without a connection, and how should conflicts be resolved? | “Should we add a service worker?” |
| Approval flow | Who may approve, and may they approve their own request? | “RBAC or ABAC?” |
| Content editing | Can editors publish directly, or does someone review changes first? | “Which CMS package?” |
| Payments | What payment outcome must be confirmed before access is granted? | “Which webhook framework?” |

These are examples, not questions to ask every project. Read the request first; it may already settle them.

## Keep work moving

When a required answer is pending, continue independent research, source inspection or preparation that does not choose for the user. Later discoveries can justify a focused follow-up; do not reopen settled choices without new evidence. Record material assumptions in the work artifact, and save them to memory only when that persistence is authorized.
