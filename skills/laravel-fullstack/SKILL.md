---
name: laravel-fullstack
description: Use this skill when building or refactoring Laravel 11/12 applications (Blade, Livewire, Inertia/React, Tailwind, or Vanilla/Bootstrap UI) with Form Requests, Policies, Services, and Eloquent optimization.
---

# Laravel Full-Stack Skill (Stack-Agnostic UI + Clean Backend)

## 1. Layout & Reusable View Components

- Match the project's UI stack (Tailwind CSS, Inertia/React, Livewire, `ui-kit/keith-ui-tokens.css`, or Bootstrap) and map screens from `component-catalog/00-MASTER-SCREEN-AND-COMPONENT-TYPES.md`.
- Organize reusable Blade/React primitives cleanly (`layouts/app`, `layouts/guest`, `components/stat-card`, `status-badge`, `data-table`, `confirm-modal`, `empty-state`) and version static assets (`?v={{ config('app.asset_version', '1.0.0') }}`).
- Centralize navigation items in a single config/composer and highlight active routes accurately via `request()->routeIs(...)`.
- Always include `@csrf` in `<form method="POST">` and `@method('PUT'|'DELETE')` where required.

## 2. Backend Architecture, Money Precision & Performance

- **Thin Controllers:**
  - Validate input via `FormRequest` classes (`app/Http/Requests/`).
  - Authorize resource actions via `Policy` classes (`$this->authorize('update', $invoice)`).
  - Delegate business math, payouts, stock adjustments, and multi-model writes to `Service` or `Action` classes wrapped in `DB::transaction()`.
- **Eloquent & Financial Hygiene:**
  - Store currency in `DECIMAL(12,2)` or integer centavos; never hard-delete financial rows (soft-void with reason & UTC timestamp).
  - Prevent N+1 queries with `with()`, `withCount()`, and `withSum()`, paginate list endpoints (`->paginate(15)->withQueryString()`), and define explicit `$fillable` on models.
