# AG Kit eval set

Run each prompt in a **new Antigravity chat** inside a scratch project after installing the kit. Tick the checklist from what the agent actually produced. Record results in `results-<date>.md`; anything that fails twice becomes a kit fix.

| # | Prompt | Tests |
|---|---|---|
| E1 | "Build an admin dashboard for a 3-branch POS in React + Bootstrap 5.3." | Rule 07 recipe, Rule 01 tokens/theme, demo data |
| E2 | "Create a landing page for a laundry shop in Next.js + Tailwind." | Rule 07 landing recipe, imagery, both themes |
| E3 | "Add a Laravel API endpoint to void a receipt." | Rule 06 permissions, rule-03, laravel-patterns, report format |
| E4 | "Plan a new SFA add-on that syncs orders to our ERP." | Rule 05 plan file, Rule 04 Option B, owners per step |
| E5 | "The sidebar overlaps the content on tablet. Fix it." | fix-ui flow, no automatic browser run, cause stated |
| E6 | "Add a senior citizen discount to the POS checkout." | ph-business-compliance, server-side math, config not constants |

## Pass checklist (every prompt)

- [ ] Reply in English, direct, no emoji; report has Result / Changed / Decisions / Not done / Next and `Rules applied`.
- [ ] No test/build/browser run unless asked; any "ran" claim has pasted output.
- [ ] Multi-file work started with a plan saved in `docs/plans/`.

## Extra checks

- **E1/E2:** full chrome, every recipe section, icons, imagery/placeholders, realistic ₱ demo data in one `demo-data` file, hover/focus states, Light/Dark/System toggle with no flash, no hard-coded colors in components.
- **E3:** Form Request + Policy, branch-scoped permission, void keeps the record with reason + audit trail, API Resource response, versioned route.
- **E4:** table ownership table, outbox + idempotency key, signed webhooks + nightly reconciliation, `/api/v1`, risks, "Done when" per step.
- **E5:** traces parent layout constraint, fixes the owning rule/token, no `!important` pile, states it was not browser-checked.
- **E6:** removes VAT then applies 20%, records ID number, rates in config with effective date, totals on server, report flags items for accountant confirmation.
