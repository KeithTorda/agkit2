# Tokens and theme (shared by every block)

The only file in this skill with raw color values. Copy it once per project into `assets/css/tokens.css` (or `app/globals.css`). Every block in the stack files uses these names and nothing else.

Theme attribute: Bootstrap uses `data-bs-theme`, Tailwind/plain CSS uses `data-theme`. The selectors below accept both, so one token file works for either stack.

## 1. tokens.css

```css
/* ---------- LIGHT (default) ---------- */
:root, [data-theme="light"], [data-bs-theme="light"] {
  color-scheme: light;
  --background: #f6f7fb;
  --foreground: #0f172a;
  --surface: #ffffff;
  --surface-elevated: #ffffff;
  --surface-muted: #f1f3f9;
  --primary: #5b4fe9;            /* indigo-violet, 5.6:1 with white */
  --primary-foreground: #ffffff;
  --accent: #c026d3;
  --muted: #eceff6;
  --muted-foreground: #5b6478;
  --border: #e3e6ef;
  --input: #d5d9e4;
  --ring: #5b4fe9;
  --success: #15803d;
  --warning: #b45309;
  --error: #dc2626;
  --info: #0369a1;
  --sidebar-bg: #ffffff;
  --sidebar-fg: #3f4659;
  --chart-1: #5b4fe9; --chart-2: #0ea5e9; --chart-3: #10b981; --chart-4: #f59e0b; --chart-5: #ec4899;
  --chart-grid: #e8ebf3;
  --shadow-sm: 0 1px 2px rgb(16 24 40 / .06);
  --shadow-md: 0 4px 12px -2px rgb(16 24 40 / .08), 0 2px 4px -2px rgb(16 24 40 / .05);
  --shadow-lg: 0 18px 40px -12px rgb(16 24 40 / .18);
  --glow: 0 0 0 1px rgb(91 79 233 / .10), 0 8px 30px -8px rgb(91 79 233 / .35);
  --bs-primary-rgb: 91, 79, 233;  /* Bootstrap only: needs an r,g,b triplet */
}

/* ---------- DARK ---------- */
[data-theme="dark"], [data-bs-theme="dark"] {
  color-scheme: dark;
  --background: #0b0d17;
  --foreground: #e6e8f2;
  --surface: #121527;
  --surface-elevated: #1a1e35;
  --surface-muted: #171a2e;
  --primary: #8b7cff;
  --primary-foreground: #0d0a2b;
  --accent: #e879f9;
  --muted: #1d2138;
  --muted-foreground: #9aa1b9;
  --border: #262b45;
  --input: #2f3554;
  --ring: #a59bff;
  --success: #4ade80;
  --warning: #fbbf24;
  --error: #f87171;
  --info: #38bdf8;
  --sidebar-bg: #0f1222;
  --sidebar-fg: #c3c8dc;
  --chart-1: #8b7cff; --chart-2: #38bdf8; --chart-3: #34d399; --chart-4: #fbbf24; --chart-5: #f472b6;
  --chart-grid: #232843;
  --shadow-sm: 0 1px 2px rgb(0 0 0 / .45);
  --shadow-md: 0 6px 16px -4px rgb(0 0 0 / .55);
  --shadow-lg: 0 24px 48px -12px rgb(0 0 0 / .7);
  --glow: 0 0 0 1px rgb(139 124 255 / .18), 0 10px 40px -10px rgb(139 124 255 / .45);
  --bs-primary-rgb: 139, 124, 255;
}

/* ---------- DERIVED + SCALE (same formula in both themes) ---------- */
:root, [data-theme], [data-bs-theme] {
  --primary-hover: color-mix(in oklab, var(--primary) 88%, var(--foreground));
  --primary-active: color-mix(in oklab, var(--primary) 78%, var(--foreground));
  --primary-soft: color-mix(in oklab, var(--primary) 13%, transparent);
  --success-soft: color-mix(in oklab, var(--success) 14%, transparent);
  --warning-soft: color-mix(in oklab, var(--warning) 16%, transparent);
  --error-soft: color-mix(in oklab, var(--error) 14%, transparent);
  --info-soft: color-mix(in oklab, var(--info) 14%, transparent);
  --ring-soft: color-mix(in oklab, var(--ring) 35%, transparent);
  --sidebar-active-bg: var(--primary-soft);
  --sidebar-active-fg: var(--primary);
  --gradient-brand: linear-gradient(135deg, var(--primary), var(--accent));
  --radius-sm: .5rem; --radius: .75rem; --radius-lg: 1.25rem;
  --dur-fast: 150ms; --dur: 220ms; --dur-slow: 300ms;
  --ease: cubic-bezier(.2, .8, .2, 1);
}

body { background: var(--background); color: var(--foreground); }
:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
::selection { background: var(--primary-soft); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important; animation-iteration-count: 1 !important;
    transition-duration: .01ms !important; scroll-behavior: auto !important;
  }
}
```

## 2. Head script (first thing in `<head>`, before any CSS)

Resolves System mode before first paint, persists the choice, follows the OS while in System mode, and syncs across tabs. Change `ATTR` for Tailwind.

```html
<script>
(function () {
  var ATTR = 'data-bs-theme';          // Tailwind / plain CSS: 'data-theme'
  var KEY = 'themePreference';          // 'light' | 'dark' | 'system'
  var mq = window.matchMedia('(prefers-color-scheme: dark)');
  function getPref() { try { return localStorage.getItem(KEY) || 'system'; } catch (e) { return 'system'; } }
  function resolve(p) { return p === 'system' ? (mq.matches ? 'dark' : 'light') : p; }
  function apply(p) {
    var resolved = resolve(p), root = document.documentElement;
    root.setAttribute(ATTR, resolved);
    root.dataset.themePreference = p;
    document.dispatchEvent(new CustomEvent('themechange', { detail: { preference: p, resolved: resolved } }));
  }
  window.appTheme = {
    get: getPref,
    resolved: function () { return resolve(getPref()); },
    set: function (p) { try { localStorage.setItem(KEY, p); } catch (e) {} apply(p); }
  };
  apply(getPref());
  mq.addEventListener('change', function () { if (getPref() === 'system') apply('system'); });
  window.addEventListener('storage', function (e) { if (e.key === KEY) apply(getPref()); });
})();
</script>
```

## 3. Three-state theme toggle

Segmented control (works in any stack). Use it in the topbar, settings page or footer.

```html
<div class="theme-toggle" role="radiogroup" aria-label="Color theme">
  <button type="button" role="radio" data-theme-set="light" aria-label="Light theme"><i class="bi bi-sun" aria-hidden="true"></i></button>
  <button type="button" role="radio" data-theme-set="dark" aria-label="Dark theme"><i class="bi bi-moon-stars" aria-hidden="true"></i></button>
  <button type="button" role="radio" data-theme-set="system" aria-label="Use system theme"><i class="bi bi-circle-half" aria-hidden="true"></i></button>
</div>

<style>
.theme-toggle { display: inline-flex; gap: 2px; padding: 3px; border: 1px solid var(--border); border-radius: 999px; background: var(--surface-muted); }
.theme-toggle button { display: grid; place-items: center; width: 2rem; height: 2rem; border: 0; border-radius: 999px;
  background: transparent; color: var(--muted-foreground); transition: background var(--dur-fast) var(--ease), color var(--dur-fast) var(--ease), transform var(--dur-fast) var(--ease); }
.theme-toggle button:hover { color: var(--foreground); background: var(--muted); }
.theme-toggle button:active { transform: scale(.94); }
.theme-toggle button:focus-visible { outline: 2px solid var(--ring); outline-offset: 1px; }
.theme-toggle button[aria-checked="true"] { background: var(--surface); color: var(--primary); box-shadow: var(--shadow-sm); }
.theme-toggle button:disabled { opacity: .5; pointer-events: none; }
</style>

<script>
document.addEventListener('click', function (e) {
  var btn = e.target.closest('[data-theme-set]');
  if (btn) window.appTheme.set(btn.dataset.themeSet);
});
function syncThemeControls() {
  var p = window.appTheme.get();
  document.querySelectorAll('[data-theme-set]').forEach(function (b) {
    var on = b.dataset.themeSet === p;
    b.setAttribute(/radio/.test(b.getAttribute('role') || '') ? 'aria-checked' : 'aria-pressed', on); // radio + menuitemradio
    b.classList.toggle('active', on);
  });
}
document.addEventListener('themechange', syncThemeControls);
document.addEventListener('DOMContentLoaded', syncThemeControls);
</script>
```

The Bootstrap topbar dropdown variant (same `data-theme-set` buttons inside `.dropdown-menu`) is in [bootstrap-app.md](bootstrap-app.md).

## 4. Bootstrap 5.3 bridge (load after `bootstrap.min.css`)

Maps Bootstrap's own variables to the tokens so stock components follow the theme.

```css
:root, [data-bs-theme] {
  --bs-body-bg: var(--background); --bs-body-color: var(--foreground);
  --bs-emphasis-color: var(--foreground); --bs-heading-color: var(--foreground);
  --bs-secondary-color: var(--muted-foreground); --bs-tertiary-color: var(--muted-foreground);
  --bs-secondary-bg: var(--surface-muted); --bs-tertiary-bg: var(--surface-muted);
  --bs-border-color: var(--border); --bs-border-color-translucent: var(--border);
  --bs-border-radius: var(--radius-sm); --bs-border-radius-lg: var(--radius); --bs-border-radius-xl: var(--radius-lg);
  --bs-primary: var(--primary); --bs-success: var(--success); --bs-warning: var(--warning);
  --bs-danger: var(--error); --bs-info: var(--info);
  --bs-link-color: var(--primary); --bs-link-hover-color: var(--primary-hover);
  --bs-link-color-rgb: var(--bs-primary-rgb); --bs-link-hover-color-rgb: var(--bs-primary-rgb);
  --bs-focus-ring-color: var(--ring-soft);
  --bs-form-valid-color: var(--success); --bs-form-valid-border-color: var(--success);
  --bs-form-invalid-color: var(--error); --bs-form-invalid-border-color: var(--error);
  --bs-box-shadow-sm: var(--shadow-sm); --bs-box-shadow: var(--shadow-md); --bs-box-shadow-lg: var(--shadow-lg);
}
.btn { --bs-btn-focus-box-shadow: 0 0 0 .2rem var(--ring-soft); }
.btn-primary {
  --bs-btn-bg: var(--primary); --bs-btn-border-color: var(--primary); --bs-btn-color: var(--primary-foreground);
  --bs-btn-hover-bg: var(--primary-hover); --bs-btn-hover-border-color: var(--primary-hover); --bs-btn-hover-color: var(--primary-foreground);
  --bs-btn-active-bg: var(--primary-active); --bs-btn-active-border-color: var(--primary-active); --bs-btn-active-color: var(--primary-foreground);
  --bs-btn-disabled-bg: var(--primary); --bs-btn-disabled-border-color: var(--primary); --bs-btn-disabled-color: var(--primary-foreground);
}
.btn-danger {
  --bs-btn-bg: var(--error); --bs-btn-border-color: var(--error); --bs-btn-color: var(--primary-foreground);
  --bs-btn-hover-bg: color-mix(in oklab, var(--error) 88%, var(--foreground)); --bs-btn-hover-border-color: var(--error);
  --bs-btn-active-bg: color-mix(in oklab, var(--error) 78%, var(--foreground)); --bs-btn-disabled-bg: var(--error);
}
.card { --bs-card-bg: var(--surface); --bs-card-color: var(--foreground); --bs-card-border-color: var(--border); --bs-card-cap-bg: transparent; }
.dropdown-menu {
  --bs-dropdown-bg: var(--surface-elevated); --bs-dropdown-border-color: var(--border); --bs-dropdown-color: var(--foreground);
  --bs-dropdown-link-color: var(--foreground); --bs-dropdown-link-hover-bg: var(--surface-muted); --bs-dropdown-link-hover-color: var(--foreground);
  --bs-dropdown-link-active-bg: var(--primary-soft); --bs-dropdown-link-active-color: var(--primary);
  --bs-dropdown-link-disabled-color: var(--muted-foreground); --bs-dropdown-header-color: var(--muted-foreground);
  --bs-dropdown-divider-bg: var(--border); box-shadow: var(--shadow-lg);
}
.modal { --bs-modal-bg: var(--surface-elevated); --bs-modal-border-color: var(--border); --bs-modal-color: var(--foreground); }
.offcanvas { --bs-offcanvas-bg: var(--surface); --bs-offcanvas-color: var(--foreground); }
.toast { --bs-toast-bg: var(--surface-elevated); --bs-toast-color: var(--foreground); --bs-toast-border-color: var(--border);
  --bs-toast-header-bg: var(--surface-elevated); --bs-toast-header-color: var(--foreground); --bs-toast-box-shadow: var(--shadow-lg); }
.table { --bs-table-bg: transparent; --bs-table-color: var(--foreground); --bs-table-border-color: var(--border);
  --bs-table-hover-bg: var(--surface-muted); --bs-table-hover-color: var(--foreground); --bs-table-striped-bg: var(--surface-muted); }
.pagination {
  --bs-pagination-bg: var(--surface); --bs-pagination-color: var(--foreground); --bs-pagination-border-color: var(--border);
  --bs-pagination-hover-bg: var(--surface-muted); --bs-pagination-hover-color: var(--foreground); --bs-pagination-hover-border-color: var(--border);
  --bs-pagination-focus-bg: var(--surface-muted); --bs-pagination-focus-color: var(--foreground); --bs-pagination-focus-box-shadow: 0 0 0 .2rem var(--ring-soft);
  --bs-pagination-active-bg: var(--primary); --bs-pagination-active-border-color: var(--primary); --bs-pagination-active-color: var(--primary-foreground);
  --bs-pagination-disabled-bg: var(--surface-muted); --bs-pagination-disabled-color: var(--muted-foreground); --bs-pagination-disabled-border-color: var(--border);
}
.accordion { --bs-accordion-bg: var(--surface); --bs-accordion-color: var(--foreground); --bs-accordion-border-color: var(--border);
  --bs-accordion-btn-color: var(--foreground); --bs-accordion-active-bg: var(--primary-soft); --bs-accordion-active-color: var(--foreground);
  --bs-accordion-btn-focus-box-shadow: 0 0 0 .2rem var(--ring-soft); }
.progress { --bs-progress-bg: var(--muted); --bs-progress-bar-bg: var(--primary); }
.form-control, .form-select { background-color: var(--surface); border-color: var(--input); color: var(--foreground); }
.form-control::placeholder { color: var(--muted-foreground); }
.form-control:focus, .form-select:focus, .form-check-input:focus { border-color: var(--ring); box-shadow: 0 0 0 .2rem var(--ring-soft); }
.form-control:disabled, .form-select:disabled { background-color: var(--surface-muted); opacity: .7; }
.form-check-input { background-color: var(--surface); border-color: var(--input); }
.form-check-input:checked, .form-check-input:indeterminate { background-color: var(--primary); border-color: var(--primary); }
.input-group-text { background: var(--surface-muted); border-color: var(--input); color: var(--muted-foreground); }
```

## 5. React / Next.js

Keep the same `tokens.css`. Use one provider: `next-themes` with `attribute="data-theme"` (or `"data-bs-theme"`), `defaultTheme="system"`, `enableSystem`, `storageKey="themePreference"`, and `suppressHydrationWarning` on `<html>`. It injects the equivalent head script; do not add the one above as well. Bind the toggle buttons to `setTheme('light' | 'dark' | 'system')` and read `theme` for the checked state.
