# Mobile architecture decisions

Start with the repository and requirements. These comparisons identify meaningful tradeoffs; they do not rank frameworks universally or assign a stack from an app category.

## Platform foundation

Keep an existing supported React Native, Flutter, Swift/UIKit/SwiftUI, Kotlin/Compose or other foundation when it can meet the request. For a new project compare team experience, native APIs, rendering needs, accessibility, performance evidence, release/distribution, maintenance and supported devices. Cross-platform may reduce duplicate work; native may simplify a platform-specific capability. Neither is automatically wrong for an MVP.

Expo is a valid React Native path when compatible with required native modules and build/distribution needs. Flutter can support strongly branded UI, and native controls can also be customized; “pixel perfect” is not a sufficient framework decision. Over-the-air update capabilities have engine, runtime and store-policy constraints; they are not permission to replace native binary changes without release. Verify current official requirements for the selected approach.

## State ownership

| Kind of state | Useful starting question |
|---|---|
| Temporary control state | Can it remain in the component/screen? |
| Shared client workflow | Which consumers need it and what lifecycle owns it? |
| Server data/cache | Who is authoritative, how stale may it be, and how is it invalidated? |
| Durable offline data | What survives process death and how will it sync or conflict? |
| Navigation state | Can the supported router own it instead of duplicating it elsewhere? |

Use existing mechanisms first. Local state, context/inherited values, a query cache, Redux, Zustand, Riverpod, Bloc or another tool can serve different roles. Do not prohibit a healthy store or install both a query cache and a global store for a tiny screen. Define ownership rather than requiring one package for all state.

## Storage and authentication

Preferences and replaceable cache differ from credentials, structured offline data and media. Choose platform-supported secure credential storage for sensitive persisted secrets, a suitable database for relational offline data, and appropriate file/cache directories for media. Review backup, encryption, sign-out cleanup and multi-account isolation. Secure storage is not an unlimited database and does not protect a compromised client from every threat.

Use the identity provider's supported mobile flow. OAuth/OIDC commonly uses an external user agent with PKCE for public clients, appropriate callback validation and secure token handling; exact behavior follows current provider/platform guidance. Biometrics can unlock a local credential but do not replace server authorization. Apple Pay is payment, not user login. Verify actual store rules when third-party sign-in makes them relevant; do not invent an unconditional sign-in requirement.

## Offline and sync

Choose explicitly between online-required behavior, cached reads, durable drafts, queued mutations and full offline editing. Explain unsent/stale state. Define stable mutation IDs, ordering/dependencies, idempotency, retry/backoff, expiry, conflict rules and account boundaries where queued work exists. A WebSocket, realtime service or SDK does not automatically resolve business conflicts or make payments/inventory safe offline.

Keep critical server invariants authoritative. Last-write-wins can lose edits and depends on ordering/timestamp semantics; CRDT/OT or domain merges require deliberate design, not a default label. Test process death, reconnection, duplicate/reordered delivery and revoked access in proportion to the feature.

## Record and verify

Document consequential choices and rejected alternatives briefly when useful. Validate them through a representative complete flow, appropriate device build, realistic data and affected failure cases. Do not label a choice best, fastest or secure without evidence relevant to this product.
