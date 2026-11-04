# Tokens and theme (shared by every block)

The only file in this skill with raw color values. Copy it once per project into `assets/css/tokens.css` (or `app/globals.css`). Every block in the stack files uses these names and nothing else.

Theme attribute: `data-theme` on `<html>`.

## 1. tokens.css

```css
/* ---------- LIGHT (default) ---------- */
:root, [data-theme="light"] {
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
}

/* ---------- DARK ---------- */
[data-theme="dark"] {
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
}

/* ---------- DERIVED + SCALE (same formula in both themes) ---------- */
:root, [data-theme] {
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
  var ATTR = 'data-theme';
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


## 5. React / Next.js

Keep the same `tokens.css`. Use one provider: `next-themes` with `attribute="data-theme"`, `defaultTheme="system"`, `enableSystem`, `storageKey="themePreference"`, and `suppressHydrationWarning` on `<html>`. It injects the equivalent head script; do not add the one above as well. Bind the toggle buttons to `setTheme('light' | 'dark' | 'system')` and read `theme` for the checked state.
