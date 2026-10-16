# Node API service

## Fit and inspection

Use when a standalone Node service is needed. Existing Express, Fastify, Hono or another maintained foundation can remain; a template should not force replacement.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Define a stable contract: input, validation, auth, status/error shape, pagination and idempotency where needed.

- Bound request bodies, timeouts and concurrency as appropriate. Separate configuration from secrets, redact logs, and cleanly release resources.

- Use data constraints/transactions for business invariants and authorize access at the real boundary. Do not treat CORS as authentication.

For new visual design, complete the shared short style/reference intake and wait unless already answered or delegated. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Exercise representative valid, invalid and unauthorized requests, relevant storage/integration behavior, and startup/health behavior using the actual project tools.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
