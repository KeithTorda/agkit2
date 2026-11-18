---
trigger: glob
globs: "**/*.php, **/*.ts, **/*.js, **/*.py, **/*.sql, **/*.prisma, **/*.sh, **/*.ps1, **/*.conf, **/Dockerfile*, **/docker-compose*.yml, **/routes/**, **/api/**, **/database/**, **/.env*"
description: Enforces server-side RBAC, integer/decimal money precision, indexed SQL integrity, fail-fast config validation, structured error handling, and Contabo VPS safety.
---

# RULE 03 — SECURITY, MONEY PRECISION, DATABASE & LIVE VPS SAFETY

## 1. Authentication, Authorization & Boundary Validation

- **Server-Side Enforcement:** Authenticate and authorize every action on the server (`Policies`, `Gates`, middleware). Never trust client-sent `role`, `user_id`, `branch_id`, `price`, or `total`.
- **Boundary Validation:** Validate all request bodies, query params, headers, webhooks, and file uploads on the server (Laravel `FormRequest`, `Zod`, `Pydantic`, or explicit schema validators).
- **Parameterized Queries & N+1 Prevention:** Use prepared statements / ORM bindings exclusively — zero string interpolation in SQL or shell commands (`execFile` / argument arrays over raw shell strings). Eager-load relations (`with()`) and paginate list endpoints.
- **CSRF, Cookies & Rate Limiting:** Enforce CSRF protection on cookie-authenticated mutations, `httpOnly` + `Secure` + `SameSite=Lax` cookies, and rate limits on auth and public submission routes.

## 2. Money Precision, Database Integrity & Error Handling

- **Exact Money Math (Zero Float Drift):** Store money as integer minor units (centavos) or `DECIMAL(12,2)` — **never** compute payouts, VAT, discounts, or invoices with unrounded IEEE-754 floats (`0.1 + 0.2`). Compute all totals server-side inside a DB transaction (`DB::transaction` / `BEGIN IMMEDIATE`).
- **Audit-Safe Financial Records:** Never hard-delete paid receipts, invoices, or ledger rows — mark `voided` with `status_reason` and UTC timestamp.
- **Schema & Index Hygiene:** Define explicit `ON DELETE RESTRICT` / `CASCADE` on every foreign key, add indexes on all foreign keys and frequently filtered/sorted columns, use forward-only migrations, and store timestamps in UTC ISO-8601.
- **Fail-Fast Config & Structured Errors:**
  - Validate required `.env` variables at startup so missing secrets/paths fail immediately on boot.
  - Never write silent empty `catch (error) {}` blocks on server/DB/IO operations (allowed only for optional browser storage fallbacks in locked UI widgets). Log full error context server-side and return plain, safe error messages (`{ error: { code, message } }`) without stack traces.
- **Secrets & File Uploads:** Keep secrets strictly in gitignored `.env` (never in `NEXT_PUBLIC_*` / `VITE_*` or logs). Validate uploaded file MIME type + max byte size, generate safe random/UUID filenames, and disable script execution in upload directories.

## 3. Live Contabo VPS & Database Safety (`147.93.158.118`)

- **Zero Unbacked Destructive DB Commands:** Require explicit user approval AND a verified timestamped `.sql` / `.sqlite` backup before `migrate:fresh`, `db:wipe`, `DROP TABLE`, `TRUNCATE`, or destructive schema changes.
- **Timestamped Config Backups:** Before editing live Nginx, PHP-FPM, PM2, systemd, or `.env` files, create an instant rollback backup (`cp file.conf file.conf.bak.$(date +%Y%m%d-%H%M)`).
- **Syntax Check Before Reload:** Always run `nginx -t`, `php-fpm8.3 -t`, or `sshd -t` before reloading services, and never lock out active SSH/web ports (`22`, `80`, `443`).
