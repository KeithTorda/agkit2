# Subscription product on Next.js

## Fit and inspection

Use when a subscription product actually needs identity, organization/tenant membership, entitlements and billing on a chosen Next.js foundation. A shop or dashboard does not imply subscriptions or a particular payment provider.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Define membership, roles, tenant scope and entitlement rules independently of UI visibility. Enforce them at the server data boundary.

- Use the selected billing provider current integration docs. Verify webhook authenticity, idempotency, out-of-order events and server-confirmed status; a redirect is not payment evidence.

- Represent trials, cancellation, failed payment and entitlement transitions according to the business decision. Keep test-mode data/keys distinct and label demo states.

New visual design follows `rule-01-unified-theme-system`; ask about style only if genuinely unclear. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Test tenant isolation and relevant entitlement transitions with provider sandbox fixtures where available. Never create real charges or subscriptions as a routine verification step without authorized scope.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
