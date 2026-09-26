---
part: 32
title: Backend, API and Database
covers: service and manager layers, repository pattern, controllers, response envelopes, status codes, error responses, catch-all 500s, validation, mass assignment, API naming, pagination, filtering, versioning, auth and sessions, mock auth, rate limiting, CORS, secrets and env handling, logging secrets, SQL string building, N+1, indexes, transactions, constraints, schema boilerplate, soft delete, enums, money and time columns, migrations, webhooks and payments, idempotency, receipt numbering, background jobs, SMS and email sending, Supabase and Firebase rules, framework-specific tells, Data Privacy Act handling
---

# 32 — Backend, API and Database

Read when: designing or reviewing API routes, server handlers, database schemas, migrations, auth, payment callbacks, background jobs, or Supabase/Firebase rules. JS and TS language tells are in part 30. Next.js server actions and route handler placement are in part 31. API docs and log message wording are in part 06.

## 32.1 Layers and abstraction

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `UserService`, `UserManager`, `UserHandler`, `UserController`, `UserRepository`, `UserDAO` for one table with 3 queries | Enterprise layering pasted onto a small app. Each layer only forwards the call. | Route handler calls a small data module (`residents.ts` with `listResidents`, `getResident`, `createResident`). Add a service layer when business rules span several tables or callers. |
| Repository pattern wrapping an ORM that is already a repository | Prisma, Eloquent, Django ORM, Drizzle already abstract the DB | Use the ORM directly in data functions. Wrap only to share complex queries. |
| `BaseRepository<T>` with generic `findAll`, `findById`, `update`, `delete` used by every model | Generic CRUD hides real queries and permissions | Write the queries each feature needs, with its filters and access checks. |
| Controller methods that only call `service.x(req.body)` and return the result | Pass-through layer | Merge the layers. Keep validation and auth in the handler, logic in one function. |
| Interfaces for every service (`IUserService`) with one implementation | Java habit | Concrete modules. Add an interface when a second implementation exists (a real SMS provider and a test fake). |
| DI containers (Inversify, tsyringe) in an Express app with 10 routes | Ceremony | Import modules. Pass clients as function arguments where tests need to replace them. |
| `helpers/`, `utils/`, `lib/`, `common/`, `core/`, `shared/` all present on the server | Template folders | Group by feature: `payments/`, `residents/`, `elections/`. See part 33. |
| Microservices for an LGU portal or school system with one team | Network calls where function calls would do | One deployable app. Split only when a part has different scaling or ownership. |
| Event bus and CQRS for CRUD screens | Pattern cosplay | Direct writes and reads. |
| GraphQL server for one frontend with 12 fixed screens | Schema, resolvers and N+1 problems for no gain | REST or RPC (tRPC, server actions). GraphQL when many clients need flexible queries. |

```ts
// Banned
class ResidentController {
  constructor(private residentService: IResidentService) {}
  async getAll(req, res) { res.json(await this.residentService.getAll()); }
}
class ResidentService implements IResidentService {
  constructor(private repo: IResidentRepository) {}
  getAll() { return this.repo.findAll(); }
}

// Use
app.get("/residents", requireRole("secretary"), async (req, res) => {
  const q = ListResidentsQuery.parse(req.query);
  res.json(await listResidents(db, { barangayId: req.user.barangayId, ...q }));
});
```

## 32.2 Response shapes

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `{ success: true, message: "Operation successful", data: {...} }` on every response | `success` duplicates the HTTP status. `message` is filler nobody reads. | Return the resource on 2xx. Use the status code for outcome. `201` with the created object, `204` with no body. |
| `{ success: false, message: "Something went wrong" }` with status 200 | Clients, caches and monitoring all see a success | Correct 4xx/5xx status and a structured error body. |
| Every response wrapped in `{ data: { data: {...} } }` | Nested envelopes from two layers wrapping | One level. `data` only when you also return `meta` (pagination). |
| Error body shapes that differ per route (`error`, `err`, `message`, `errors[]`, `msg`) | Each route written in a different session | One error format for the whole API. Problem Details (RFC 9457) or a fixed `{ error: { code, message, fields } }`. |
| Error messages written for humans only, no machine code | Client must match on English text | Stable `code` (`OR_NUMBER_TAKEN`, `VOTER_NOT_FOUND`) plus a plain `message`. |
| Validation errors as one string: `"Invalid input"` | Form cannot highlight fields | Field errors: `{ fields: { mobile: "Use 09XXXXXXXXX or +639XXXXXXXXX." } }`. Copy rules in part 03. |
| Returning the full DB row including `password_hash`, `otp_secret`, internal flags | Data leak | Select or map to an output type. Never return secrets or hashes. |
| Dates as locale strings: `"9/10/2026, 3:00:00 PM"` | Ambiguous MM/DD vs DD/MM, not parseable | ISO 8601 with offset: `2026-10-09T15:00:00+08:00`, or UTC `Z`. Format in the client. |
| Money as a float: `"amount": 1250.5` | Float drift, unclear unit | Integer centavos with the unit in the name: `"amount_centavos": 125050`, plus `"currency": "PHP"`. Or a decimal string `"1250.50"`. Pick one and document it. |
| camelCase in one route, snake_case in another | Mixed conventions | One casing across the API. |
| `null`, `""`, `[]` and missing keys used interchangeably for "none" | Client code full of checks | Defined rules: arrays always present (`[]`), optional scalars `null`, never omit documented keys. |

```json
// Banned (HTTP 200)
{ "success": false, "message": "Operation failed", "data": null }

// Use (HTTP 422)
{
  "type": "https://example.gov.ph/errors/validation",
  "title": "Validation failed",
  "status": 422,
  "code": "VALIDATION_FAILED",
  "fields": { "birthdate": "Enter a date in the past." }
}
```

## 32.3 Status codes

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `200` for everything, including errors | Status ignored | Use the codes below. |
| Catch-all `500` for validation, auth and not-found errors | Every error becomes a server error, alerts fire for user typos | Map known errors: validation `400` or `422`, auth `401`, permission `403`, missing `404`, conflict `409`, rate limit `429`. `500` only for unexpected failures. |
| `404` for "not allowed to see" and `403` for "not found" swapped at random | Inconsistent security posture | Decide per resource. Return `404` when revealing existence leaks data (another barangay's resident record). Document it. |
| `401` when the user is signed in but lacks permission | Client re-prompts login forever | `403`. |
| `400` for a duplicate email | Client cannot tell a typo from a conflict | `409` with code `EMAIL_TAKEN`. |
| `201` on updates, `200` on creates | Copied handlers | `201` + `Location` header on create. `200` or `204` on update. |
| `500` with the stack trace and SQL in the body | Leaks internals | Generic message to the client with a request ID. Full error in server logs. |
| `503` never used during maintenance | Clients retry blindly | `503` with `Retry-After` during planned downtime. Page copy in part 04. |
| `429` without `Retry-After` | Clients hammer | Include `Retry-After` seconds. |

| Situation | Status |
|---|---|
| Created | 201 |
| Updated, returns body | 200 |
| Deleted or updated, no body | 204 |
| Malformed JSON or bad query param | 400 |
| Body fails validation | 422 (or 400, one choice for the API) |
| Not signed in or token expired | 401 |
| Signed in, not allowed | 403 |
| Resource missing | 404 |
| Duplicate or state conflict (already paid, OR number taken) | 409 |
| Too many requests | 429 |
| Unexpected server failure | 500 |
| Upstream gateway failed (GCash, SMS provider) | 502 |
| Maintenance or overload | 503 |

## 32.4 Validation

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Fake validation: `if (!req.body.email) return error` and nothing else | Checks presence, not type, length or format | Schema validation at the boundary (Zod, Valibot, Joi, Pydantic, Laravel Form Requests, Django forms/serializers). Validate type, length, format and ranges. |
| Validation only in the frontend | Anyone can call the API | Validate on the server always. Client validation is for UX. |
| Trusting client-sent totals, prices, discounts, roles or user IDs | Customer sets their own price, user sets `role: "admin"` | Recompute totals server-side from DB prices. Take user ID and role from the session, never from the body. |
| Mass assignment: `User.create(req.body)`, Laravel `$guarded = []`, Django `fields = "__all__"` | Client can set any column | Allow-list fields: `pick(body, ["name", "mobile", "purok"])`, `$fillable`, explicit serializer fields. |
| No max length on strings | Megabyte names, DB errors | `max` on every string. Match the column size. |
| No limit on request body size or upload size | Memory exhaustion | Body limit (for example `express.json({ limit: "100kb" })`). Upload limit per field. Check MIME type and extension server-side. |
| Regex validation copied without anchors: `/\d{11}/` | Matches substrings | Anchored patterns: `/^09\d{9}$/` or a library. PH phone rules in part 30. |
| Validating then using the raw body instead of the parsed result | Unvalidated extra fields pass through | Use the parsed object returned by the schema. |
| Validation errors thrown as 500 | See 32.3 | Map schema errors to 422 with field messages. |
| File uploads trusted by extension | Renamed executables, SVG with scripts | Check magic bytes, re-encode images, serve uploads from a separate domain or with `Content-Disposition: attachment`. |

## 32.5 API naming and shape

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Verbs in paths: `/getUsers`, `/createResident`, `/deletePayment/5` | RPC names on REST routes | Nouns and methods: `GET /residents`, `POST /residents`, `DELETE /payments/5`. Action endpoints only for real actions: `POST /receipts/42/void`. |
| Mixed plural and singular: `/user/5`, `/residents`, `/payment` | Inconsistent | Plural collections: `/users/5`. |
| Mixed casing in paths: `/barangayOfficials`, `/barangay_officials`, `/Barangay-Officials` | Different sessions | Kebab-case paths: `/barangay-officials`. |
| Deep nesting: `/provinces/1/municipalities/2/barangays/3/puroks/4/residents/5` | Long URLs, hard to authorise | Nest one level at most: `/barangays/3/residents`. Access single records at `/residents/5`. |
| `/api/v1/` added with no plan for v2 | Ritual versioning | Version when a breaking change ships to clients you do not control. Internal APIs used only by your app can skip it. |
| Pagination missing on list endpoints | Returns 50,000 residents | Default limit (for example 50), max limit (200). Cursor pagination for large or live tables, offset for small admin lists. Return `next_cursor` or `total` as needed. |
| Filters in POST bodies for simple reads: `POST /residents/search` | Not cacheable, not linkable | Query params: `GET /residents?purok=3&status=active&q=dela+cruz`. |
| Sort param free-form passed to SQL: `ORDER BY ${req.query.sort}` | SQL injection | Allow-list sortable columns. |
| Boolean query params as `"true"`/`"1"`/`"yes"` parsed differently per route | Inconsistent parsing | One parser. Document accepted values. |
| No idempotency on `POST` for payments and orders | Retries create duplicates | Accept an `Idempotency-Key` header. Store and replay the first response. |
| Endpoints that return different shapes based on a `type` param | Hard to type and document | Separate endpoints. |
| No OpenAPI or route list for a public API (LGU open data, school integration) | Integrators guess | Generate an OpenAPI spec from the schemas. Docs rules in part 06. |

## 32.6 Server error handling

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `try/catch` in every route that returns `res.status(500).json({ message: "Internal server error" })` | Copied blocks, every error becomes 500 | One error middleware or framework handler that maps known error classes to status codes and logs unknown ones. |
| `catch (e) { res.json({ error: e.message }) }` | Leaks DB and library messages to users | Known errors: safe message. Unknown: generic message plus request ID. |
| Missing `await` inside `try` in Express 4 handlers | Rejections escape, request hangs | Express 5, or an async wrapper, or `express-async-errors`. |
| `process.exit()` in request handlers | Kills the server for one bad request | Throw. Let the handler respond. |
| No request ID | Cannot connect a user report to logs | Generate or accept `X-Request-Id`, include in logs and error responses. |
| Health check that returns `200 OK` without checking the DB | Load balancer keeps a broken instance | `/healthz` for liveness, `/readyz` that checks DB connectivity. |

## 32.7 Auth, sessions and access control

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Mock auth left in: `const user = { id: 1, role: "admin" }`, `if (password === "admin123")`, `// TODO: add real auth` | Anyone is admin | Real auth before any deploy. Use the framework's auth (Laravel Breeze/Fortify, Django auth, Auth.js, Lucia-style sessions, Supabase Auth, Clerk). |
| Dev bypass flags: `if (process.env.SKIP_AUTH)` | One env mistake opens the app | No bypass in code. Seed dev accounts in a dev database. |
| Hard-coded JWT secret: `jwt.sign(payload, "secret")`, `"your-secret-key"`, `"changeme"` | Tokens forgeable by anyone who reads tutorials | Long random secret from env, validated at boot. Rotate on leak. |
| JWT with no expiry, or 30-day access tokens | Stolen token works forever | Short access tokens (15–60 min) with refresh, or server sessions with idle and absolute timeouts. |
| Tokens in `localStorage` | Readable by any XSS | `HttpOnly`, `Secure`, `SameSite=Lax` cookies. CSRF protection for cookie auth. |
| Passwords hashed with MD5, SHA-1, SHA-256, or stored plain | Crackable | Argon2id or bcrypt (cost 10–12). Use the framework default hasher. |
| Role checks only in the frontend (hidden buttons) | API still allows it | Check permissions in every server handler. |
| `if (user.role === "admin")` scattered across 40 handlers | Rules drift | One permission function: `can(user, "receipts.void")`. Roles map to permissions. UI in part 22. |
| IDOR: `GET /residents/:id` returns any record if signed in | Staff of one barangay read another barangay's residents | Scope every query by tenant or owner: `WHERE id = $1 AND barangay_id = $2`. |
| Login error "Email not found" vs "Wrong password" | User enumeration | "Email or password is incorrect." Same response time for both paths. |
| No rate limit on login, OTP, password reset, SMS send | Brute force and SMS cost abuse | Rate limit per IP and per account: for example 5 login attempts per 15 min, 3 OTP sends per 10 min per number. Return 429. |
| OTP of 4 digits with no expiry and no attempt limit | Guessable | 6 digits, 5–10 minute expiry, max 5 attempts, single use, hashed at rest. |
| Password reset tokens stored plain and never expiring | Account takeover | Random token, store a hash, expire in 30–60 minutes, single use, invalidate sessions after reset. |
| CORS `origin: "*"` with credentials, or `app.use(cors())` default | Any site can call the API with user cookies | Allow-list origins. No wildcard with credentials. |
| Admin panel on the public internet at `/admin` with default credentials | Target for bots | Strong auth, 2FA for admin roles, IP allow-list for LGU back offices where possible. |
| Security headers absent | Clickjacking, MIME sniffing | `helmet` or framework equivalents: CSP, `X-Content-Type-Options`, `Referrer-Policy`, `frame-ancestors`. |

## 32.8 Secrets, env and config

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `.env` committed to git | Secrets public | `.env` in `.gitignore`. Commit `.env.example` with names and no values. Rotate anything that leaked. |
| Secrets with defaults: `process.env.JWT_SECRET || "dev-secret"` | Production runs with the default when the var is missing | No default for secrets. Fail at boot if missing. |
| `process.env.X` read in 30 files | Typos go unnoticed until runtime | One config module that validates env with a schema at boot and exports typed values. |
| API keys in frontend code: PayMongo secret, SMS gateway key, Supabase service role key | Shipped to every visitor | Server-only. Frontend gets publishable keys only. |
| Secrets in logs, error messages or `console.log(process.env)` | Leaks to log providers | Never log env. Redact known keys in the logger. |
| One `.env` for dev, staging and production | Test payments hit live accounts | Separate env per environment. Live payment keys only in production. |
| Config values in DB and env and code for the same setting | Unclear source of truth | One place per setting. Env for secrets and deploy settings. DB for values admins change (fees, office hours). |

## 32.9 Logging

Log message wording is in part 06.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Logging secrets: passwords, tokens, OTPs, API keys, full `Authorization` headers | Anyone with log access can act as users | Redact in the logger config (`pino` `redact` paths). Never log request bodies of auth routes. |
| Logging personal data: full names with addresses, birthdates, voter IDs, PhilSys numbers, medical info | Data Privacy Act (RA 10173) exposure | Log record IDs. Mask values: `0917***4567`. |
| `console.log(req.body)` in every handler | Floods logs with PII | Structured logs with selected fields. |
| No log levels, everything `info` | Noise | `error` for failures needing action, `warn` for handled problems, `info` for state changes, `debug` off in production. |
| Logs as free text | Cannot filter | JSON logs with `request_id`, `user_id`, `route`, `status`, `duration_ms`. |
| Audit events mixed into app logs | Cannot prove who voided a receipt | Separate `audit_log` table: actor, action, target, before/after, timestamp, IP. UI in part 22. |

## 32.10 SQL and queries

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| SQL built with string concatenation or template literals: `` `SELECT * FROM users WHERE email = '${email}'` `` | SQL injection | Parameterised queries: `db.query("SELECT ... WHERE email = $1", [email])`, ORM query builders, PDO prepared statements. |
| `SELECT *` everywhere | Pulls large columns and secrets, breaks on schema change | Select the columns needed. |
| N+1: loop over residents, query household for each | 1 query becomes 501 | Join, `IN (...)` batch, ORM eager loading (`include`, `with()`, `select_related`, `prefetch_related`). |
| Loading all rows then filtering in JS | Transfers the table | Filter, sort and paginate in SQL. |
| Counting with `SELECT *` then `.length` | Loads every row | `SELECT count(*)`. For big tables, avoid counts on every page load. |
| No indexes except primary keys | Full table scans on search, login, foreign keys | Index foreign keys, columns in `WHERE`, `ORDER BY` and joins. Unique index on login email and on OR numbers per series. Check with `EXPLAIN`. |
| Indexes on every column | Slower writes, wasted space | Index for actual queries. Remove unused indexes. |
| `LIKE '%term%'` search on large tables | Cannot use a B-tree index | Full-text search (Postgres `tsvector`, MySQL FULLTEXT), trigram index (`pg_trgm`), or a search service. |
| Multi-step writes without a transaction (create order, decrement stock, write payment) | Partial writes on failure | Wrap in a transaction. Lock rows that must not race (`SELECT ... FOR UPDATE` on stock). |
| Read-modify-write for counters: read stock, subtract in JS, write back | Lost updates under concurrency | Atomic update: `UPDATE items SET stock = stock - $1 WHERE id = $2 AND stock >= $1`. |
| Raw SQL and ORM mixed randomly in one feature | Two styles | ORM by default. Raw SQL for reports and complex queries, kept in named functions. |
| Queries inside templates or views | Hidden database calls | Load data in the handler or loader. |
| Reports computed on each dashboard load over millions of rows | Slow pages | Summary tables or materialised views refreshed on a schedule. Show "Updated X ago". See part 22. |

```ts
// Banned
const rows = await db.query(`SELECT * FROM residents WHERE name LIKE '%${q}%'`);
for (const r of rows) r.household = await db.query(`SELECT * FROM households WHERE id = ${r.household_id}`);

// Use
const rows = await db.query(
  `SELECT r.id, r.last_name, r.first_name, r.purok, h.household_no
     FROM residents r
     JOIN households h ON h.id = r.household_id
    WHERE r.barangay_id = $1 AND r.search_name % $2
    ORDER BY r.last_name, r.first_name
    LIMIT 50`,
  [barangayId, q],
);
```

## 32.11 Schema design

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `id`, `uuid`, `created_at`, `updated_at`, `deleted_at`, `created_by`, `updated_by`, `version`, `metadata` on every table, most unused | Boilerplate columns copied into every migration | Add columns you use. `id` plus `created_at` is a fine default. Pick one primary key strategy (bigint identity or UUID v7), not both. |
| Both `id SERIAL` and `uuid` with the UUID used nowhere | Two keys, one ignored | One key. Use UUIDs if IDs are exposed in URLs and must not be guessable. |
| Soft delete (`deleted_at`) on every table | Every query needs `WHERE deleted_at IS NULL`, unique constraints break, deleted personal data stays forever | Hard delete by default. Soft delete only where records must be restorable or kept (receipts are voided, not deleted). Use partial unique indexes where soft delete exists. |
| Deleting receipts or financial records at all | Breaks BIR audit trail | Receipts are never deleted. Void with reason, actor and timestamp. The OR number stays used. |
| Status as free text: `status VARCHAR(255)` with `"Pending"`, `"pending"`, `"PENDING "` in data | Inconsistent values | Check constraint or enum type, or a lookup table. Lowercase snake_case values. |
| Enum strings duplicated in DB, API and UI with different spellings | Mapping bugs | One source of values. Generate types from the DB or the schema. |
| Postgres `ENUM` for values that change often (fee types, document types) | Altering enums needs migrations | Lookup table for admin-managed values. Enum or check constraint for fixed states. |
| Money as `FLOAT` or `DOUBLE` | Rounding errors | `BIGINT` centavos or `NUMERIC(12,2)`. Never float. |
| `TIMESTAMP` without time zone | Ambiguous times, reports shift by 8 hours | `TIMESTAMPTZ` in Postgres. Store UTC, convert to `Asia/Manila` for display and daily grouping. |
| Birthdates stored as `TIMESTAMP` | Time zone shifts the date | `DATE`. |
| Every column nullable | No integrity, null checks everywhere | `NOT NULL` by default. Nullable only for data that can be missing. |
| No foreign keys "for flexibility" | Orphan rows | Foreign keys with `ON DELETE` rules chosen on purpose. |
| No unique constraints; uniqueness checked only in code | Race creates duplicates | Unique constraints: email, OR number per series, voter precinct assignment per election. |
| JSON columns for data you query and filter | Hard to index and validate | Real columns for queried fields. JSON for opaque payloads (raw webhook body). |
| `name` single column for Filipino residents | Cannot sort by surname or print forms | `first_name`, `middle_name`, `last_name`, `suffix`. |
| Address as one text field in an LGU system | Cannot filter by purok or barangay | Structured: `house_no`, `street`, `purok`, `barangay_id`, `city_municipality`, `province`, `zip`. Use PSGC codes for barangay, municipality and province. |
| Phone stored in several formats | Duplicate detection fails | E.164 `+639XXXXXXXXX`, normalised on write. |
| Table and column naming mixed: `tblUsers`, `user_accounts`, `UserProfile`, `usr_nm` | Different sessions | snake_case plural tables, snake_case columns, no prefixes or abbreviations. |
| Migrations edited after being applied, or schema changed in the DB console | Environments drift | New migration for each change. Never edit applied migrations. |
| No seed or a seed that inserts fake production-looking data | Fake records leak into prod | Seeds for dev and tests only, clearly fake, never run in production. |

## 32.12 Payments, webhooks and receipts

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Payment marked paid when the user returns to the success URL | Anyone can open the success URL | Mark paid only from a verified webhook (PayMongo, Maya, Xendit, GCash via provider) or a server-side status check. |
| Webhook handler with no signature verification | Forged "paid" events | Verify the provider signature with the raw body before parsing. Reject on mismatch. |
| Webhook handler not idempotent | Provider retries double-credit | Store event IDs. Ignore duplicates. Use a unique constraint on the provider event ID. |
| Webhook handler doing slow work before responding | Provider times out and retries | Verify, store, respond `200` within a few seconds, process in a job. |
| Amount taken from the webhook without checking the order total | Partial payments marked complete | Compare amount and currency with the stored order. |
| OR/invoice numbers from `MAX(or_no) + 1` | Race creates duplicates, gaps on failed transactions | A sequence per series inside the same transaction as the sale, with a unique constraint. Void keeps the number. Follow the BIR-registered series and format. |
| "Official Receipt" wording and BIR fields on a system that is not BIR-accredited | Legal issue | Use "Acknowledgement receipt" or the wording the client's accountant approves. Copy rules in part 09. |
| Refunds by editing the original payment row | No audit trail | Separate refund records linked to the payment. |
| Test and live payment keys mixed | Real charges in testing | Env per environment. Check key prefixes (`sk_test_`/`sk_live_`) at boot. |

## 32.13 Background jobs, SMS and email

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Sending SMS or email inside the request, user waits 5 seconds | Slow requests, failures break the main action | Queue the send (BullMQ, Laravel queues, Celery, Supabase queues, a jobs table). Respond immediately. |
| No retry on SMS or email failures | Messages lost silently | Retry with backoff, max attempts, dead-letter record, admin view of failed sends. |
| Bulk SMS blast in a loop with no throttle | Provider rate limits, huge cost, carrier blocking | Throttle to the provider's limit. Batch. Record per-recipient status. |
| Cron jobs with `setInterval` inside the web server | Runs once per instance, stops on restart | Platform cron (Vercel Cron, Supabase pg_cron, system cron, Laravel scheduler) calling a protected endpoint or job. |
| Cron endpoints with no auth | Anyone can trigger | Secret header check or platform-signed requests. |
| Jobs that are not idempotent | Retries double-send | Idempotency by job key. Record completion. |
| No timezone on schedules | "8am reminder" runs at 4pm Manila | Schedule in UTC and convert, or set `Asia/Manila` explicitly. |

## 32.14 Supabase, Firebase and BaaS

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Row Level Security disabled "for now" | Anon key can read and write every row | Enable RLS on every table in exposed schemas. Write policies per role. Test with the anon key. |
| RLS policy `USING (true)` | RLS on, but open | Policies that check `auth.uid()` and tenant columns. |
| Service role key in the frontend or in `NEXT_PUBLIC_*` | Full bypass of RLS for anyone | Service role key server-only. |
| Policies that call slow functions per row | Slow queries | Wrap `auth.uid()` in `(select auth.uid())`. Index policy columns. Check the Supabase advisors. |
| Firestore rules `allow read, write: if true;` or the test-mode expiry | Open database | Rules that check `request.auth` and document ownership. |
| Storage buckets public for IDs, clearances, medical files | Anyone with the URL downloads | Private buckets and signed URLs with short expiry. |
| Edge functions with no auth check | Public endpoints | Verify the JWT or a secret in each function. |

## 32.15 Framework-specific tells

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Laravel: `$guarded = []` on models | Mass assignment | `$fillable` with listed fields. |
| Laravel: logic in routes files, `DB::select` with interpolated strings | Tutorial shortcuts | Controllers or actions, Eloquent or bindings. |
| Laravel: `APP_DEBUG=true` in production | Stack traces and env shown to users | `APP_DEBUG=false`. |
| Django: `DEBUG = True`, `ALLOWED_HOSTS = ["*"]` in production settings | Info leak | Env-driven settings, explicit hosts. |
| Django REST: `fields = "__all__"` | Exposes every column | Explicit fields. |
| Express: no `helmet`, `app.use(cors())`, `express.json()` without limit, `x-powered-by` on | Defaults from tutorials | Configure each. `app.disable("x-powered-by")`. |
| Express: error handler missing | HTML stack traces | Final error middleware returning JSON. |
| PHP: `mysqli_query` with `$_POST` values | SQL injection | PDO prepared statements. |
| PHP: `md5($password)` | Weak hashing | `password_hash` and `password_verify`. |
| Node: `bodyParser` package in a new Express 4.16+ app | Outdated | `express.json()`. |
| FastAPI: `response_model` missing, returning ORM objects | Leaks fields | Pydantic response models. |

## 32.16 Personal data and PH government systems

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Collecting every field "in case" (religion, income, blood type) on a barangay clearance request | Data Privacy Act requires proportional collection | Collect only what the service needs. Mark optional fields. Privacy notice on the form. |
| No retention rule | Records kept forever | Retention per record type, agreed with the client. Scheduled deletion or archiving. |
| Voter, resident or student exports as open CSV links | Mass data leak | Exports require a role, are logged in the audit log, expire, and mask sensitive columns by default. |
| Precinct finder that returns full voter records | Exposes addresses and birthdates | Return only precinct, clustered precinct number and polling place. Require name plus birthdate match. Rate limit. |
| Public API for school grades with student ID as the only key | Guessable IDs | Auth per student or parent, or a random access code. |
| Production data copied to dev laptops for testing | Uncontrolled copies | Anonymised or synthetic data in dev. |

## 32.17 Check

- [ ] No Service/Manager/Repository layers that only forward calls.
- [ ] No base CRUD classes or interfaces with a single implementation.
- [ ] No `{ success: true, message: "Operation successful" }` envelopes.
- [ ] Status codes match the outcome. No errors with 200. No catch-all 500 for known errors.
- [ ] One error format across the API, with stable `code` values and field errors.
- [ ] No stack traces, SQL or library messages in client responses. Request ID returned.
- [ ] Every input validated server-side with a schema. Parsed output used, not the raw body.
- [ ] Totals, prices, roles and user IDs computed or read server-side, never trusted from the client.
- [ ] Mass assignment blocked with allow-lists.
- [ ] Body size and upload limits set. Uploads checked by content.
- [ ] Paths use plural nouns, kebab-case, at most one nesting level.
- [ ] List endpoints paginated with default and max limits.
- [ ] Sort and filter params allow-listed.
- [ ] Dates ISO 8601 with offset. Money in integer centavos or decimal strings with currency.
- [ ] No mock auth, dev bypass flags or hard-coded credentials.
- [ ] Secrets from env, validated at boot, no defaults. `.env` not committed.
- [ ] Passwords hashed with Argon2id or bcrypt.
- [ ] Tokens in HttpOnly cookies or short-lived with refresh.
- [ ] Permission checks in every handler through one `can()` function.
- [ ] Every query scoped by tenant or owner. No IDOR.
- [ ] Rate limits on login, OTP, reset and SMS endpoints, with 429 and `Retry-After`.
- [ ] CORS allow-list. Security headers set.
- [ ] Logs structured, levelled, with request IDs. No secrets or full personal data in logs.
- [ ] Audit log table for sensitive actions.
- [ ] No SQL string building. Parameterised queries only.
- [ ] No N+1 queries. No `SELECT *` in app code.
- [ ] Indexes on foreign keys and filtered columns. Unique constraints for business keys.
- [ ] Multi-step writes in transactions. Stock and counters updated atomically.
- [ ] Only needed boilerplate columns. One primary key strategy.
- [ ] Soft delete only where required. Receipts voided, never deleted.
- [ ] Status columns constrained. Money not float. `TIMESTAMPTZ` for times, `DATE` for birthdates.
- [ ] Names and addresses structured for PH records, PSGC codes for places.
- [ ] Migrations append-only. Seeds never run in production.
- [ ] Payments confirmed only by verified, idempotent webhooks. Amounts checked.
- [ ] OR numbers from a sequence with a unique constraint. Receipt wording matches BIR status.
- [ ] SMS and email sent from a queue with retries and throttling.
- [ ] Cron runs outside the web process, authenticated, in the right time zone.
- [ ] Supabase RLS on every exposed table with real policies. Service role key server-only.
- [ ] Framework debug modes off in production.
- [ ] Personal data collected only when needed, exports controlled and logged.
