# AGKIT2 Decisions (3.2)

1. **Own rules, one owner per topic.** kit-core + Rules 01–07. A topic lives in exactly one rule; agents and skills point to the rule instead of restating it.
2. **Built for Gemini 3.x in Antigravity.** Short rules, numbered steps, positive wording, a "Before you answer, check" recap at the end of every rule, examples over descriptions. Rule files stay under 24,000 bytes; anything over 12,000 characters gets a quick card (Rule 01 → Rule 01b).
3. **Not strict, but complete.** No approval ceremonies or forced questions. Tests, builds and browser checks run only when the user asks. The work itself must be finished, and any claim that something ran includes pasted output.
4. **Session discipline.** Plan first for multi-file work, build one step at a time, start a new chat after each milestone. Plans are `.md` files in `docs/plans/`.
5. **Template-grade UI by default.** Every screen looks like a complete premium ready-made template (Rule 07, `template-ui-blocks`). Minimal only on request. All styling through Rule 01 tokens with Light/Dark/System.
6. **Option B integration for every new system.** Separate DB, one owner per table, outbox + middleman, signed webhooks + nightly reconciliation, versioned API (Rule 04).
7. **14 agents, one template.** Mission, Owns / Does not own, Before starting, How to work, Stack notes, Quality bar, Common mistakes to avoid, Handoff format.
8. **Stack focus.** React/Next.js, Laravel/Blade, Bootstrap 5.3, Tailwind, Expo, MySQL/Postgres, VPS. Philippine business rules live in `ph-business-compliance`.
9. **Safe installs.** The installer validates, backs up, installs and rolls back on failure. Edit the repo, never the installed plugin.
