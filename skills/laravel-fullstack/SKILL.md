---
name: laravel-fullstack
description: Use this skill when building or refactoring Laravel 11/12 applications (Blade, Livewire, Inertia, or REST APIs) paired with the Bootstrap 5 Dashboard Pro template, Form Requests, Policies, Services, and Eloquent optimization.
---

# Laravel Full-Stack + Bootstrap 5 Pro Skill

## 1. Layout & Blade Component Structure

- Place copied template assets in `public/assets/` and version stylesheets/scripts with `?v={{ config('app.asset_version', '1.0.0') }}`.
- Extract the master shell from `component-catalog/02-APP-SHELL-SIDEBAR-HEADER.md` into:
  - `resources/views/layouts/app.blade.php` (`#main-wrapper`, `.nav-header`, `.header`, `.dlabnav`, `.content-body`, `.footer`)
  - `resources/views/layouts/guest.blade.php` (`.authincation` centered layout for Login/Register/Forgot Password)
  - `resources/views/components/` (`stat-card`, `status-badge`, `data-table-card`, `confirm-modal`, `empty-state`)
- Centralize sidebar items in a config or view composer and apply `mm-active` via `request()->routeIs(...)`.
- Always include `@csrf` in `<form method="POST">` and `@method('PUT'|'DELETE')` where required.

## 2. Backend Architecture & Performance

- **Thin Controllers:** Keep controllers focused on HTTP orchestration:
  - Validate input via `FormRequest` classes (`app/Http/Requests/`).
  - Authorize resource actions via `Policy` classes (`$this->authorize('update', $invoice)`).
  - Delegate business calculations, stock adjustments, and multi-model writes to `Service` or `Action` classes wrapped in `DB::transaction()`.
- **Eloquent Hygiene:**
  - Prevent N+1 queries with `with()` eager loading and `withCount()` / `withSum()` aggregates.
  - Paginate all list tables (`->paginate(15)->withQueryString()`) and render the `.pagination.pagination-gutter.pagination-primary` footer.
  - Explicitly define `$fillable` on models; never pass `$request->all()` into `create()` or `update()`.
