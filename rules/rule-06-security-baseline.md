---
name: rule-06-security-baseline
version: 3.0.0
priority: P0
trigger: glob
globs: "**/*.ts, **/*.tsx, **/*.js, **/*.jsx, **/*.mjs, **/*.php, **/*.py, **/*.sql, **/routes/**, **/api/**, **/app/Http/**, **/.env*"
description: Rule 06 - security baseline for all server and client code. Server-side auth and role checks, safe queries, secrets, uploads, audit trail for money and records.
---

# RULE 06 — SECURITY BASELINE

## Identity and permissions

- Authenticate on the server. Never trust a role, user ID, branch ID, price or total sent from the client.
- Check permission for every action on every resource ("can this user void *this* receipt in *this* branch?"), not only "is logged in".
- Hide buttons in the UI for convenience, but enforce the rule on the server.
- Session/JWT: httpOnly + secure cookies for web sessions; short-lived tokens; logout invalidates server-side where the stack supports it.

## Input and queries

- Validate every external input at the boundary (request body, query string, headers, webhook payloads, file contents) with the project's validator (Laravel Form Requests, Zod, Pydantic...).
- Parameterized queries / ORM bindings only. No string-built SQL with user input. No user input in shell commands.
- Escape output by default (React, Blade `{{ }}`). Use raw HTML output only for trusted, sanitized content.
- Protect state-changing web requests against CSRF when cookies are used.

## Secrets

- Secrets live in `.env` / the host's secret store. Never in client bundles, logs, error messages, screenshots or commits.
- Client-exposed env vars (`NEXT_PUBLIC_*`, `VITE_*`) contain nothing secret.
- `.env` is in `.gitignore`; keep a `.env.example` with names and dummy values.

## Money, records and audit

- The server computes prices, discounts, VAT and totals from its own data.
- Receipts, invoices, payroll and stock movements are never hard-deleted; they are voided/reversed with a reason.
- Keep an audit trail for sensitive actions: who, when, what, before/after values, and IP/device where available.
- Use database transactions for multi-step writes that must succeed or fail together.

## Files

- Check uploaded file type (by content, not only extension) and size.
- Store uploads outside the public web root or with generated names; never execute uploaded files.
- Serve private files through an authorized route or signed URL.

## Dependencies and errors

- Do not add packages that are unmaintained or unknown when a well-known option exists.
- Production error responses do not include stack traces, SQL or file paths.
- Rate-limit login, OTP, password reset and public form endpoints.
