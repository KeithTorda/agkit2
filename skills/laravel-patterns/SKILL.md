---
name: laravel-patterns
description: "Laravel 11/12 conventions for controllers, Form Requests, Policies, Services/Actions, Eloquent, queues, events, API Resources, Blade components and tests. Use for any Laravel or Blade work."
version: 3.2.0
---

# Laravel patterns

How to build Laravel code that matches rule-03 (structure), rule-04 (integration) and rule-06 (security).

## Steps

1. **Read first:** `composer.json` (Laravel + PHP version), `routes/web.php`, `routes/api.php`, `app/Http/Controllers`, `app/Models`, existing Policies, `config/`, `.env.example`.
2. **Route:** group by feature, name every route, API routes under `Route::prefix('v1')`. Apply `auth:sanctum` (API) or `auth` (web) middleware on the group.
3. **Validate:** one Form Request per write action (`php artisan make:request StoreSaleRequest`). Put rules and `authorize()` there; controllers receive `$request->validated()` only.
4. **Authorize:** a Policy per model (`make:policy SalePolicy --model=Sale`). Call `$this->authorize('void', $sale)` or `Gate::authorize()`. Scope by branch/tenant in the policy, not in the view.
5. **Business logic:** an Action or Service class (`app/Actions/Sales/PostSale.php`) with one public `handle()`/`__invoke()`. Controllers stay thin: validate → authorize → call action → return resource.
6. **Write atomically:** wrap multi-table writes in `DB::transaction(fn () => ...)`. Insert the outbox row (rule-04) inside the same transaction.
7. **Models:** `$fillable` (never `$guarded = []`), `$casts` (`'total' => 'decimal:2'`, enums, `'meta' => 'array'`), relationships, local scopes (`scopeForBranch`). Eager load in list queries (`with()`), paginate (`paginate(20)`).
8. **Responses:** API Resources (`SaleResource`) for every JSON response; errors via the exception handler as `{ "error": { "code", "message" } }`.
9. **Jobs:** `ShouldQueue` jobs with `$tries`, `backoff()`, `failed()`; dispatch after commit (`->afterCommit()`). Outbox middleman = scheduled command or long-running worker processing `pending` rows per `aggregate_id`.
10. **Webhooks in:** verify HMAC signature middleware, store event id for idempotency, queue the processing.
11. **Blade:** components in `resources/views/components` with `@props`, layouts with `<x-app-layout>`, `{{ }}` escaping, `@csrf`, `@method`. Assets with Vite. Theme per rule-01 (`data-bs-theme` or `data-theme` on `<html>`).
12. **Migrations:** see database-design; money `decimal(15,2)`, `foreignId()->constrained()`, indexes on filter columns.
13. **Tests (when asked):** Pest/PHPUnit feature tests with `RefreshDatabase`, factories, `actingAs()`, `assertDatabaseHas`.

## File map

| Thing | Location | Artisan |
|---|---|---|
| Form Request | `app/Http/Requests/<Feature>/` | `make:request` |
| Policy | `app/Policies/` | `make:policy --model=` |
| Action | `app/Actions/<Feature>/` | (plain class) |
| Resource | `app/Http/Resources/` | `make:resource` |
| Job | `app/Jobs/` | `make:job` |
| Enum | `app/Enums/` | `make:enum` |

## Before you finish, check

- [ ] Every write route has a Form Request and a Policy check.
- [ ] Multi-step writes use `DB::transaction`; outbox row inside it for add-ons.
- [ ] List endpoints eager-load and paginate.
- [ ] JSON goes through API Resources; routes are named and versioned.
