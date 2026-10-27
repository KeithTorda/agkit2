---
name: plan-writing
description: "Create durable task plans with clear outcomes, dependencies, owners and observable verification. Use for /plan or multi-session coordination; no fixed task or line count applies."
version: 2.8.2
---

# Plan Writing

Planning depth follows uncertainty and coordination needs. A simple change can be completed directly; a short task list can support bounded work. Use `docs/plans/<yyyy-mm-dd>-<slug>.md` for a durable record, continuing the existing plan for the same task. Use proplan for a linked system specification when warranted.

## Make work executable

Describe the goal, scope boundaries and material assumptions. Break work at meaningful ownership and verification boundaries. Each task says what changes, who owns it, important files/contracts, dependencies and how the result will be judged. Avoid arbitrary task counts, mandatory libraries or a ceremony for every edit.

```markdown
# Order history

## Goal
Customers can see their own previous orders and recover from loading failures.

## Assumptions
- Existing authentication and order schema remain in use.

## Scope
- List and detail views; existing pagination contract.

## Tasks
- [ ] Add the authenticated history query (owner: backend-engineer)
  - files: src/orders/service.ts
  - verify: current user sees own orders; another user's ID returns no private data.
- [ ] Build history states (owner: frontend-engineer; after query contract)
  - verify: populated/empty/error states render; opening an order shows its details.

## Done when
- The requested journey works and relevant checks provide evidence.
```

Dependencies are real blockers, not merely a preferred order. Parallel labels require independent files and settled shared decisions. Include migration, docs or operations tasks when the outcome needs them; do not append a generic bundle to every plan.

Use estimates only when useful, with the basis and uncertainty. Mark tasks complete after their verify criterion has evidence and record meaningful limitations. A future plan is not authorization for external actions and is not proof the work is done.
