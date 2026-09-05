# API Security Testing

Test the API the way an attacker would. Map each check to the OWASP API Security Top 10 and fix findings in `@[skills/vulnerability-scanner]` severity order.

## OWASP API Top 10 focus

| Risk | Test |
|------|------|
| API1 Broken object-level authorization (BOLA/IDOR) | Capture a request as user A, replay with user B's session, swap ids |
| API2 Broken authentication | JWT `alg: none` and algorithm confusion, weak secrets, missing `exp`/`aud` checks, predictable sessions, logout not invalidating |
| API3 Broken object property authorization | Mass assignment (`role`, `isAdmin` in body), over-exposed fields in responses |
| API4 Unrestricted resource consumption | No rate limit, unbounded page sizes, huge uploads, expensive queries |
| API5 Broken function-level authorization | Call admin endpoints as a normal user; try other HTTP methods |
| API6 Unrestricted access to sensitive business flows | Automate purchase, signup, or voting flows; check for abuse controls |
| API7 SSRF | URL parameters that fetch server-side (`?url=`, webhooks) reaching internal addresses |
| API8 Security misconfiguration | CORS `*` with credentials, debug endpoints, verbose errors, missing headers |
| API9 Improper inventory management | Old versions (`/v1`) and undocumented routes still live |
| API10 Unsafe consumption of APIs | Trusting upstream responses without validation |

## Method

1. Enumerate: routes from code and OpenAPI, plus guesses (`/admin`, `/v1`, `/debug`).
2. Authentication: bypass attempts, token tampering, credential strength, session lifetime.
3. Authorization: horizontal (peer data), vertical (higher role), and context (outside allowed scope) tests on every id-bearing endpoint.
4. Input: SQL/NoSQL/command/LDAP injection on every parameter, type coercion, boundaries, and what error messages leak.
5. Rate limiting: does it exist, is it per user or per IP, can `X-Forwarded-For`, method changes, or case changes bypass it.
6. GraphQL: introspection in production, batching and nesting depth, field-level authorization.
7. Report each finding with endpoint, reproduction request, impact, and fix.
