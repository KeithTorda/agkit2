# Backend boundaries for mobile clients

Mobile adds variable networks, process interruption, constrained background execution and a long tail of installed client versions. An existing web/API backend may already serve it well. Do not force a separate API, device identifier, JWT architecture, attestation or HMAC scheme without a concrete requirement.

## Contracts and identity

Use stable, version-compatible contracts with deliberate deprecation and rollout behavior. Return needed fields, bounded pagination and clear user-safe errors. Batch related calls or add delta sync when measured network cost justifies it. Cursor and offset pagination suit different access patterns; correct ordering/consistency still need design.

Use the provider's supported mobile authentication. A short-lived access token and securely persisted refresh credential may fit, but cookies/session models can also be valid in appropriate clients. Prevent concurrent refresh races, bound retries and avoid replaying non-idempotent operations blindly. On sign-out/account switch reconcile cached data, pending work and device push registration.

Never trust a client to grant authorization. Sensitive operations need server permissions, validation and appropriate rate/resource limits. Device attestation can be a defense layer where justified, with availability/recovery tradeoffs; it is not universal authentication. A secret shipped in an app can be extracted, so a client HMAC key is not a general proof of trusted device identity.

## Offline mutation lifecycle

Define authoritative data, local persistence, pending state, stable mutation IDs and dependency order. Use idempotency where retries can duplicate consequences. Bound retries with backoff/jitter and account for permanent errors, revoked access, expiry and user cancellation. Queue processing need not always be global FIFO; relationships and domain ordering determine it.

Choose explicit conflict behavior, with versions/revisions or a domain merge when useful. Last-write-wins can lose work; realtime services do not automatically implement conflict resolution. Payments and inventory constraints require a server-supported protocol, not simply optimistic UI. Verify interrupted save, process death, duplicate/reordered delivery and reconnection where relevant.

## Push and background work

Use platform/provider-supported registration and token lifecycle. Link device tokens to the correct account/preferences and remove invalid tokens safely. Push can be delayed, suppressed or absent; it is not guaranteed background execution or an authoritative data source. Fetch authorized current data when opened. Avoid sensitive lock-screen payloads and respect actual user notification settings/consent.

## Data, media and observability

Choose cache freshness, image variants, upload size limits, resumability and media delivery from the task. Do not install a complex chunk protocol for a tiny image. Protect upload/download authorization and avoid unbounded client storage.

Collect only useful diagnostic/device metadata within the product's privacy requirements. Correlation IDs, client version and sanitized status/latency can help; persistent hardware/device fingerprints are not required for every request. Alert thresholds need actual service goals/baselines rather than arbitrary universal percentages.

Test the client and server boundary together when possible, including denied scope and relevant retry/failure behavior. Report mocked/provider/device limitations rather than claiming all mobile states work from an API unit test.
