# Focused API security checks

Use authorized accounts, local/test data and the least disruptive evidence needed. Select checks for the API's actual trust boundaries. A source review can establish a code-supported defect without launching an active scanner; external active testing follows the engagement's scope.

## Access matrix

Choose representative actors and resources: unauthenticated, normal user, peer user, tenant peer, privileged user, revoked/expired session. For each sensitive operation, compare expected status, returned fields and side effects.

| Boundary | Concrete case | Contract to verify |
|---|---|---|
| Object ownership | User A requests/updates B's object ID | Server denies unauthorized access without modifying data |
| Tenant isolation | Valid account changes tenant/resource scope | Joins, caches, files and exports remain tenant-scoped |
| Function permission | Ordinary user calls admin operation directly | Backend checks permission, independent of hidden UI |
| Field authorization | Body includes role/owner/internal fields | Only allowed fields can be written/read |
| Session/token | Expired, revoked or wrong-audience credential | Actual verifier rejects according to identity design |
| Cookie write | Cross-site state-changing request | Appropriate CSRF protection and cookie policy |

Use the adopted authentication library's supported validation; do not implement token algorithms from memory. A public endpoint is not defective merely because it lacks authentication. GraphQL introspection alone is not a vulnerability; assess exposed data and access policy.

## Inputs, cost and upstream trust

Validate types, bounds, coercion, unknown fields and nested payload complexity. Injection findings require a path from untrusted input to an unsafe sink; search results are candidates. Test malformed/bounded oversized data in a controlled setting rather than attempting resource exhaustion.

For server-side URL fetches, check allowed schemes/hosts, redirect behavior, address resolution, credentials and response bounds. Denying one private address string is not a complete SSRF defense. Rate limiting depends on trustworthy proxy/identity configuration and shared accounting across relevant instances.

GraphQL needs field/object access and appropriate depth/cost/batch controls. Pagination/upload endpoints need bounded work. Validate upstream data, signature and identity rather than trusting third-party success status alone.

## Retry and failure integrity

Test duplicate and concurrent mutations, idempotency-key reuse with a different body, replayed webhooks and upstream timeouts with unknown outcomes. Verify that denial/validation failure produces no partial business effect. Error bodies/logs must not leak credentials, sensitive records or internal traces.

## Report supported evidence

Include operation/location, actor prerequisites, controlled request sequence, response/side effect and impact. Redact tokens and personal data. Distinguish observed failure, code-supported reasoning and unvalidated hypothesis. Use current official risk taxonomy only if exact identifiers are needed; remediation should remain specific even without a label.
