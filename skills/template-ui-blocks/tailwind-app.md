# Tailwind app blocks

Dashboard shell, page header, KPI cards and chart card. Table, form and feedback blocks: [tailwind-data.md](tailwind-data.md). Landing and auth: [tailwind-landing.md](tailwind-landing.md). Tokens and head script (set `ATTR = 'data-theme'`): [tokens-and-theme.md](tokens-and-theme.md). Data: [demo-data.md](demo-data.md).

## 0. Setup

Tailwind v4 (`app.css`):

```css
@import "tailwindcss";
@import "./tokens.css";
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));
@theme inline {
  --color-background: var(--background); --color-foreground: var(--foreground);
  --color-surface: var(--surface); --color-surface-elevated: var(--surface-elevated); --color-surface-muted: var(--surface-muted);
  --color-primary: var(--primary); --color-primary-foreground: var(--primary-foreground); --color-primary-soft: var(--primary-soft);
  --color-accent: var(--accent); --color-muted: var(--muted); --color-muted-foreground: var(--muted-foreground);
  --color-border: var(--border); --color-input: var(--input); --color-ring: var(--ring);
  --color-success: var(--success); --color-success-soft: var(--success-soft); --color-warning: var(--warning); --color-warning-soft: var(--warning-soft);
  --color-error: var(--error); --color-error-soft: var(--error-soft); --color-info: var(--info); --color-info-soft: var(--info-soft);
  --color-sidebar: var(--sidebar-bg); --color-sidebar-foreground: var(--sidebar-fg);
}
```

Tailwind v3 (`tailwind.config.js`; `@tailwind base; @tailwind components; @tailwind utilities;` then import `tokens.css`):

```js
const v = (n) => `var(--${n})`;
module.exports = {
  darkMode: ['selector', '[data-theme="dark"]'], // v3.4.1+; older v3: ['class', '[data-theme="dark"]']
  content: ['./**/*.{html,js,ts,jsx,tsx,php,vue}'],
  theme: { extend: { colors: Object.fromEntries(['background', 'foreground', 'surface', 'surface-elevated', 'surface-muted', 'primary',
    'primary-foreground', 'primary-soft', 'accent', 'muted', 'muted-foreground', 'border', 'input', 'ring', 'success', 'success-soft',
    'warning', 'warning-soft', 'error', 'error-soft', 'info', 'info-soft'].map((k) => [k, v(k)]).concat([['sidebar', v('sidebar-bg')], ['sidebar-foreground', v('sidebar-fg')]])) } },
};
```

Notes: semantic classes (`bg-surface`, `text-muted-foreground`) already switch with the theme, so `dark:` is only for rare one-offs. In v3, opacity modifiers like `bg-primary/10` do not work on `var()` colors; use the `-soft` tokens (they work in both versions).

Icons: Lucide UMD (`<script src="https://unpkg.com/lucide@0.460.0/dist/umd/lucide.min.js"></script>`), write `<i data-lucide="bell" class="size-4" aria-hidden="true"></i>` and call `lucide.createIcons()` after each render. Heroicons: paste the 24px outline SVG with `class="size-5" aria-hidden="true"`. React: `lucide-react`.

## 1. components.css (shared, tokens only)

```css
@layer components {
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); box-shadow: var(--shadow-sm); transition: box-shadow var(--dur) var(--ease), transform var(--dur) var(--ease); }
  .card-hover:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
  .btn { display: inline-flex; align-items: center; justify-content: center; gap: .5rem; height: 2.5rem; padding: 0 1rem; border: 1px solid transparent; border-radius: var(--radius-sm);
    font-size: .875rem; font-weight: 600; white-space: nowrap; transition: background var(--dur-fast) var(--ease), color var(--dur-fast) var(--ease), box-shadow var(--dur-fast) var(--ease), transform var(--dur-fast) var(--ease); }
  .btn:focus-visible { outline: none; box-shadow: 0 0 0 3px var(--ring-soft); border-color: var(--ring); }
  .btn:active { transform: scale(.97); }
  .btn:disabled, .btn[aria-disabled="true"] { opacity: .55; pointer-events: none; }
  .btn-primary { background: var(--primary); color: var(--primary-foreground); }
  .btn-primary:hover { background: var(--primary-hover); } .btn-primary:active { background: var(--primary-active); }
  .btn-surface { background: var(--surface); color: var(--foreground); border-color: var(--border); }
  .btn-surface:hover { background: var(--surface-muted); border-color: var(--input); } .btn-surface:active { background: var(--muted); }
  .btn-ghost { background: transparent; color: var(--muted-foreground); }
  .btn-ghost:hover { background: var(--surface-muted); color: var(--foreground); } .btn-ghost:active { background: var(--muted); }
  .btn-danger { background: var(--error); color: var(--primary-foreground); } .btn-danger:hover { background: color-mix(in oklab, var(--error) 88%, var(--foreground)); }
  .btn-icon { width: 2.5rem; padding: 0; position: relative; }
  .btn-sm { height: 2rem; padding: 0 .75rem; font-size: .8rem; }
  .input { width: 100%; height: 2.5rem; padding: 0 .75rem; border: 1px solid var(--input); border-radius: var(--radius-sm); background: var(--surface); color: var(--foreground); transition: border-color var(--dur-fast), box-shadow var(--dur-fast); }
  textarea.input { height: auto; padding: .6rem .75rem; }
  .input::placeholder { color: var(--muted-foreground); }
  .input:hover { border-color: color-mix(in oklab, var(--input) 60%, var(--foreground)); }
  .input:focus { outline: none; border-color: var(--ring); box-shadow: 0 0 0 3px var(--ring-soft); }
  .input:disabled { background: var(--surface-muted); opacity: .7; cursor: not-allowed; }
  .input[aria-invalid="true"] { border-color: var(--error); } .input[aria-invalid="true"]:focus { box-shadow: 0 0 0 3px var(--error-soft); }
  .label { display: block; margin-bottom: .375rem; font-size: .875rem; font-weight: 500; }
  .check { width: 1rem; height: 1rem; accent-color: var(--primary); }
  .icon-chip { display: grid; place-items: center; width: 2.75rem; height: 2.75rem; border-radius: var(--radius-sm); background: var(--primary-soft); color: var(--primary); }
  .avatar { display: inline-grid; place-items: center; width: 2.25rem; height: 2.25rem; flex: none; border-radius: 9999px; background: var(--primary-soft); color: var(--primary); font-size: .75rem; font-weight: 700; }
  .badge-soft { display: inline-flex; align-items: center; gap: .35rem; padding: .2rem .6rem; border-radius: 9999px; font-size: .75rem; font-weight: 600; }
  .badge-soft::before { content: ""; width: .4rem; height: .4rem; border-radius: 9999px; background: currentColor; }
  .tone-success { background: var(--success-soft); color: var(--success); } .tone-warning { background: var(--warning-soft); color: var(--warning); }
  .tone-error { background: var(--error-soft); color: var(--error); } .tone-info { background: var(--info-soft); color: var(--info); }
  .tone-primary { background: var(--primary-soft); color: var(--primary); } .tone-muted { background: var(--muted); color: var(--muted-foreground); }
  .menu { position: absolute; right: 0; top: calc(100% + .5rem); z-index: 50; min-width: 12rem; padding: .375rem; background: var(--surface-elevated); border: 1px solid var(--border); border-radius: var(--radius); box-shadow: var(--shadow-lg); }
  .menu-item { display: flex; width: 100%; align-items: center; gap: .6rem; padding: .5rem .65rem; border-radius: var(--radius-sm); font-size: .875rem; color: var(--foreground); text-align: left; }
  .menu-item:hover, .menu-item:focus-visible { background: var(--surface-muted); outline: none; } .menu-item[aria-checked="true"] { color: var(--primary); background: var(--primary-soft); }
  .nav-app { position: relative; display: flex; align-items: center; gap: .75rem; padding: .55rem .75rem; border-radius: var(--radius-sm); color: var(--sidebar-fg); font-size: .875rem; transition: background var(--dur-fast), color var(--dur-fast); }
  .nav-app:hover { background: var(--surface-muted); color: var(--foreground); } .nav-app:active { background: var(--muted); }
  .nav-app[aria-current="page"] { background: var(--sidebar-active-bg); color: var(--sidebar-active-fg); font-weight: 600; }
  .nav-app[aria-current="page"]::before { content: ""; position: absolute; left: -.75rem; top: 20%; bottom: 20%; width: 3px; border-radius: 0 3px 3px 0; background: var(--primary); }
  .nav-app[aria-disabled="true"] { opacity: .5; pointer-events: none; }
  .skeleton { border-radius: var(--radius-sm); background: linear-gradient(90deg, var(--muted) 25%, var(--surface-muted) 50%, var(--muted) 75%); background-size: 200% 100%; animation: shimmer 1.4s linear infinite; }
  @keyframes shimmer { to { background-position: -200% 0; } }
  .scrim { background: color-mix(in oklab, var(--foreground) 45%, transparent); }
  .topbar { background: color-mix(in oklab, var(--surface) 86%, transparent); backdrop-filter: blur(10px); }
  summary.nav-app::-webkit-details-marker { display: none; }
  [data-collapsed="true"] .sidebar-text { display: none; } [data-collapsed="true"] .nav-app { justify-content: center; }
}
```

## 2. ui.js (menus, drawer, sidebar collapse; no framework)

```js
document.addEventListener('click', (e) => {
  const t = e.target.closest('[data-menu]');
  document.querySelectorAll('[data-menu][aria-expanded="true"]').forEach((b) => { if (b !== t) { b.setAttribute('aria-expanded', 'false'); document.getElementById(b.dataset.menu).hidden = true; } });
  if (t) { const m = document.getElementById(t.dataset.menu), open = m.hidden; m.hidden = !open; t.setAttribute('aria-expanded', open); if (open) m.querySelector('a,button,input')?.focus(); }
});
const drawer = document.getElementById('sidebar'), scrim = document.getElementById('scrim');
const setDrawer = (open) => { drawer?.classList.toggle('-translate-x-full', !open); scrim?.classList.toggle('hidden', !open); document.querySelector('[data-drawer-open]')?.setAttribute('aria-expanded', open); if (open) drawer.querySelector('a')?.focus(); };
document.querySelectorAll('[data-drawer-open]').forEach((b) => b.addEventListener('click', () => setDrawer(true)));
document.querySelectorAll('[data-drawer-close]').forEach((b) => b.addEventListener('click', () => setDrawer(false)));
document.addEventListener('keydown', (e) => { if (e.key !== 'Escape') return; setDrawer(false);
  document.querySelectorAll('[data-menu][aria-expanded="true"]').forEach((b) => { b.click(); b.focus(); }); });
const collapseBtn = document.getElementById('collapseBtn');
const setCollapsed = (on) => { drawer.dataset.collapsed = on; drawer.classList.toggle('lg:w-20', on); drawer.classList.toggle('lg:w-64', !on); collapseBtn.setAttribute('aria-pressed', on); try { localStorage.setItem('sidebarCollapsed', on ? '1' : ''); } catch (_) {} };
try { setCollapsed(localStorage.getItem('sidebarCollapsed') === '1'); } catch (_) {}
collapseBtn?.addEventListener('click', () => setCollapsed(drawer.dataset.collapsed !== 'true'));
```

React / Vue: keep the markup and classes; replace `ui.js` with the project's menu/dialog primitives (Headless UI, Radix, Reka) and state hooks.

## 3. App shell

```html
<body class="bg-background text-foreground antialiased">
<div id="scrim" class="scrim fixed inset-0 z-40 hidden lg:hidden" data-drawer-close></div>
<div class="flex min-h-screen">
  <aside id="sidebar" class="fixed inset-y-0 left-0 z-50 flex w-64 -translate-x-full flex-col border-r border-border bg-sidebar text-sidebar-foreground transition-[width,transform] duration-300 lg:sticky lg:top-0 lg:h-screen lg:translate-x-0" aria-label="Main navigation">
    <div class="flex h-16 items-center gap-2.5 px-5 font-bold text-foreground">
      <span class="grid size-8 place-items-center rounded-lg text-primary-foreground" style="background:var(--gradient-brand)"><i data-lucide="sparkles" class="size-4" aria-hidden="true"></i></span>
      <span class="sidebar-text">Tala Commerce</span>
      <button class="btn btn-ghost btn-icon ml-auto lg:hidden" data-drawer-close aria-label="Close menu"><i data-lucide="x" class="size-5"></i></button>
    </div>
    <nav class="flex-1 space-y-0.5 overflow-y-auto px-3 pb-6">
      <p class="sidebar-text px-3 pb-1.5 pt-4 text-[.7rem] font-bold uppercase tracking-wider text-muted-foreground">Overview</p>
      <a href="/dashboard" class="nav-app" aria-current="page" title="Dashboard"><i data-lucide="layout-dashboard" class="size-[18px]" aria-hidden="true"></i><span class="sidebar-text">Dashboard</span></a>
      <a href="/reports" class="nav-app" title="Reports"><i data-lucide="chart-line" class="size-[18px]" aria-hidden="true"></i><span class="sidebar-text">Reports</span></a>
      <p class="sidebar-text px-3 pb-1.5 pt-4 text-[.7rem] font-bold uppercase tracking-wider text-muted-foreground">Sales</p>
      <a href="/orders" class="nav-app" title="Orders"><i data-lucide="shopping-bag" class="size-[18px]" aria-hidden="true"></i><span class="sidebar-text">Orders</span><span class="sidebar-text badge-soft tone-primary ml-auto">12</span></a>
      <details class="group">
        <summary class="nav-app cursor-pointer list-none" title="Inventory"><i data-lucide="package" class="size-[18px]" aria-hidden="true"></i><span class="sidebar-text">Inventory</span><i data-lucide="chevron-down" class="sidebar-text ml-auto size-4 transition-transform group-open:rotate-180" aria-hidden="true"></i></summary>
        <div class="sidebar-text ml-9 mt-0.5 space-y-0.5"><a href="/inventory/items" class="nav-app">Items</a><a href="/inventory/transfers" class="nav-app">Transfers</a></div>
      </details>
      <a href="/customers" class="nav-app" title="Customers"><i data-lucide="users" class="size-[18px]" aria-hidden="true"></i><span class="sidebar-text">Customers</span></a>
      <p class="sidebar-text px-3 pb-1.5 pt-4 text-[.7rem] font-bold uppercase tracking-wider text-muted-foreground">System</p>
      <a href="/settings" class="nav-app" title="Settings"><i data-lucide="settings" class="size-[18px]" aria-hidden="true"></i><span class="sidebar-text">Settings</span></a>
      <a class="nav-app" aria-disabled="true" title="Billing (soon)"><i data-lucide="credit-card" class="size-[18px]" aria-hidden="true"></i><span class="sidebar-text">Billing</span><span class="sidebar-text badge-soft tone-muted ml-auto">Soon</span></a>
    </nav>
  </aside>

  <div class="flex min-w-0 flex-1 flex-col">
    <header class="sticky top-0 z-30 flex h-16 items-center gap-3 topbar border-b border-border px-4 lg:px-6">
      <button class="btn btn-ghost btn-icon lg:hidden" data-drawer-open aria-controls="sidebar" aria-expanded="false" aria-label="Open menu"><i data-lucide="menu" class="size-5"></i></button>
      <button id="collapseBtn" class="btn btn-ghost btn-icon hidden lg:inline-flex" aria-label="Collapse sidebar" aria-pressed="false"><i data-lucide="panel-left" class="size-5"></i></button>
      <form role="search" class="relative hidden max-w-sm flex-1 md:block"><i data-lucide="search" class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" aria-hidden="true"></i>
        <input type="search" class="input pl-9" placeholder="Search orders, customers…" aria-label="Search"><kbd class="absolute right-2.5 top-1/2 -translate-y-1/2 rounded border border-border px-1.5 text-xs text-muted-foreground">/</kbd></form>
      <div class="ml-auto flex items-center gap-1">
        <div class="relative"><button class="btn btn-ghost btn-icon" data-menu="themeMenu" aria-expanded="false" aria-haspopup="true" aria-label="Theme"><i data-lucide="sun-moon" class="size-5"></i></button>
          <div id="themeMenu" class="menu" role="menu" hidden>
            <button class="menu-item" role="menuitemradio" data-theme-set="light"><i data-lucide="sun" class="size-4"></i>Light</button>
            <button class="menu-item" role="menuitemradio" data-theme-set="dark"><i data-lucide="moon" class="size-4"></i>Dark</button>
            <button class="menu-item" role="menuitemradio" data-theme-set="system"><i data-lucide="monitor" class="size-4"></i>System</button></div></div>
        <div class="relative"><button class="btn btn-ghost btn-icon" data-menu="notifMenu" aria-expanded="false" aria-haspopup="true" aria-label="Notifications, 2 unread"><i data-lucide="bell" class="size-5"></i><span class="absolute right-2 top-2 size-2 rounded-full bg-error ring-2 ring-surface"></span></button>
          <div id="notifMenu" class="menu w-80 p-0" hidden>
            <div class="flex items-center justify-between border-b border-border px-4 py-3"><strong class="text-sm">Notifications</strong><button class="text-xs font-semibold text-primary hover:underline">Mark all read</button></div>
            <div id="notifList" class="divide-y divide-border"></div>
            <a href="/notifications" class="block border-t border-border py-2.5 text-center text-sm text-primary hover:bg-surface-muted">View all</a></div></div>
        <div class="relative"><button class="btn btn-ghost h-auto gap-2 py-1 pl-1" data-menu="userMenu" aria-expanded="false" aria-haspopup="true" aria-label="Account menu"><span class="avatar">AR</span>
          <span class="hidden text-left leading-tight sm:block"><span class="block text-sm font-semibold text-foreground">Andrea Reyes</span><span class="block text-xs text-muted-foreground">Branch Manager</span></span></button>
          <div id="userMenu" class="menu" role="menu" hidden><a href="/profile" class="menu-item" role="menuitem"><i data-lucide="user" class="size-4"></i>Profile</a><a href="/settings" class="menu-item" role="menuitem"><i data-lucide="settings" class="size-4"></i>Settings</a>
            <hr class="my-1 border-border"><button class="menu-item text-error" role="menuitem"><i data-lucide="log-out" class="size-4"></i>Sign out</button></div></div>
      </div>
    </header>
    <main id="content" class="flex-1 p-4 lg:p-6"><!-- page header + blocks --></main>
  </div>
</div>
<script>
document.getElementById('notifList').innerHTML = DEMO.notifications.map((n) => `<a href="#" class="flex gap-3 px-4 py-3 hover:bg-surface-muted focus-visible:bg-surface-muted ${n.unread ? 'bg-primary-soft' : ''}">
  <span class="icon-chip size-9 tone-${n.tone}"><i data-lucide="${{ 'exclamation-triangle': 'triangle-alert', bank: 'landmark', 'person-plus': 'user-plus' }[n.icon] || n.icon}" class="size-4"></i></span>
  <span><span class="block text-sm font-semibold">${n.title}</span><span class="block text-xs text-muted-foreground">${n.meta}</span></span></a>`).join('');
lucide.createIcons();
</script>
```

## 4. Page header

```html
<div class="mb-6 flex flex-wrap items-end justify-between gap-4">
  <div>
    <nav aria-label="Breadcrumb"><ol class="mb-1 flex items-center gap-1.5 text-sm text-muted-foreground"><li><a href="/" class="hover:text-foreground">Home</a></li><li aria-hidden="true">/</li><li aria-current="page" class="text-foreground">Dashboard</li></ol></nav>
    <h1 class="text-2xl font-bold tracking-tight">Good morning, Andrea</h1>
    <p class="text-muted-foreground">Here is what is happening across your 4 branches today.</p>
  </div>
  <div class="flex gap-2"><button class="btn btn-surface"><i data-lucide="download" class="size-4"></i>Export</button><button class="btn btn-primary"><i data-lucide="plus" class="size-4"></i>New order</button></div>
</div>
```

KPI cards, chart card, data table, form, empty state, toast and skeleton: [tailwind-data.md](tailwind-data.md).
