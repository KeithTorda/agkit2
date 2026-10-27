# Bootstrap 5.3 app blocks

Dashboard, data table and form screens. Landing and auth: [bootstrap-landing.md](bootstrap-landing.md). Tokens, head script and the Bootstrap bridge: [tokens-and-theme.md](tokens-and-theme.md). Data: [demo-data.md](demo-data.md).

## 0. Page head and kit.css

```html
<head>
  <!-- 1. theme head script from tokens-and-theme.md (ATTR = 'data-bs-theme') -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
  <link href="assets/css/tokens.css" rel="stylesheet"> <!-- tokens + Bootstrap bridge -->
  <link href="assets/css/kit.css" rel="stylesheet">
</head>
<!-- end of body: bootstrap.bundle.min.js, chart.js@4, demo-data.js, page script -->
```

```css
/* kit.css: shared pieces used by every app block (tokens only) */
.card { border-radius: var(--radius); box-shadow: var(--shadow-sm); transition: box-shadow var(--dur) var(--ease), transform var(--dur) var(--ease); }
.card-hover:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.icon-chip { display: grid; place-items: center; width: 2.75rem; height: 2.75rem; border-radius: var(--radius-sm); background: var(--primary-soft); color: var(--primary); font-size: 1.25rem; }
.avatar { display: inline-grid; place-items: center; width: 2.25rem; height: 2.25rem; border-radius: 50%; background: var(--primary-soft); color: var(--primary); font-weight: 600; font-size: .8rem; flex: none; }
.badge-soft { display: inline-flex; align-items: center; gap: .35rem; padding: .3rem .6rem; border-radius: 999px; font-size: .75rem; font-weight: 600; }
.badge-soft::before { content: ""; width: .4rem; height: .4rem; border-radius: 50%; background: currentColor; }
.badge-soft-success { background: var(--success-soft); color: var(--success); }
.badge-soft-warning { background: var(--warning-soft); color: var(--warning); }
.badge-soft-error   { background: var(--error-soft);   color: var(--error); }
.badge-soft-info    { background: var(--info-soft);    color: var(--info); }
.badge-soft-primary { background: var(--primary-soft); color: var(--primary); }
.badge-soft-muted   { background: var(--muted);        color: var(--muted-foreground); }
.btn-surface { --bs-btn-bg: var(--surface); --bs-btn-color: var(--foreground); --bs-btn-border-color: var(--border);
  --bs-btn-hover-bg: var(--surface-muted); --bs-btn-hover-color: var(--foreground); --bs-btn-hover-border-color: var(--input);
  --bs-btn-active-bg: var(--muted); --bs-btn-active-color: var(--foreground); --bs-btn-active-border-color: var(--input);
  --bs-btn-disabled-bg: var(--surface); --bs-btn-disabled-color: var(--muted-foreground); --bs-btn-disabled-border-color: var(--border); }
.btn-ghost { --bs-btn-color: var(--muted-foreground); --bs-btn-hover-bg: var(--surface-muted); --bs-btn-hover-color: var(--foreground);
  --bs-btn-active-bg: var(--muted); --bs-btn-active-color: var(--foreground); --bs-btn-border-color: transparent; --bs-btn-disabled-color: var(--muted-foreground); }
.btn-icon { display: inline-grid; place-items: center; width: 2.25rem; height: 2.25rem; padding: 0; position: relative; }
.btn:active { transform: scale(.97); }
.skeleton { display: block; border-radius: var(--radius-sm); background: linear-gradient(90deg, var(--muted) 25%, var(--surface-muted) 50%, var(--muted) 75%); background-size: 200% 100%; animation: shimmer 1.4s infinite linear; }
@keyframes shimmer { to { background-position: -200% 0; } }

/* app shell */
.app { display: flex; min-height: 100vh; }
.app-sidebar { --w: 16.5rem; background-image: linear-gradient(var(--sidebar-bg), var(--sidebar-bg)); color: var(--sidebar-fg); border-right: 1px solid var(--border); --bs-offcanvas-width: var(--w); }
.app-main { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.sidebar-brand { display: flex; align-items: center; gap: .6rem; height: 4rem; padding: 0 1.25rem; font-weight: 700; color: var(--foreground); text-decoration: none; }
.brand-mark { display: grid; place-items: center; width: 2rem; height: 2rem; border-radius: .6rem; background: var(--gradient-brand); color: var(--primary-foreground); }
.nav-group-label { padding: 1rem 1.25rem .4rem; font-size: .7rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--muted-foreground); }
.nav-app { display: flex; align-items: center; gap: .75rem; margin: 2px .75rem; padding: .55rem .75rem; border-radius: var(--radius-sm); color: var(--sidebar-fg); text-decoration: none; position: relative; transition: background var(--dur-fast) var(--ease), color var(--dur-fast) var(--ease); }
.nav-app i { font-size: 1.1rem; transition: transform var(--dur-fast) var(--ease); }
.nav-app:hover { background: var(--surface-muted); color: var(--foreground); }
.nav-app:hover i { transform: translateX(2px); }
.nav-app:active { background: var(--muted); }
.nav-app.active { background: var(--sidebar-active-bg); color: var(--sidebar-active-fg); font-weight: 600; }
.nav-app.active::before { content: ""; position: absolute; left: -.75rem; top: 20%; bottom: 20%; width: 3px; border-radius: 0 3px 3px 0; background: var(--primary); }
.nav-app[aria-disabled="true"] { opacity: .5; pointer-events: none; }
.nav-app .bi-chevron-down { margin-left: auto; font-size: .8rem; }
.nav-app[aria-expanded="true"] .bi-chevron-down { transform: rotate(180deg); }
.nav-sub .nav-app { padding-left: 2.6rem; font-size: .9rem; }
.app-topbar { position: sticky; top: 0; z-index: 1020; display: flex; align-items: center; gap: .75rem; height: 4rem; padding: 0 1.25rem;
  background: color-mix(in oklab, var(--surface) 86%, transparent); backdrop-filter: blur(10px); border-bottom: 1px solid var(--border); }
.topbar-search { max-width: 22rem; }
.dot { position: absolute; top: .45rem; right: .5rem; width: .5rem; height: .5rem; border-radius: 50%; background: var(--error); box-shadow: 0 0 0 2px var(--surface); }
@media (min-width: 992px) {
  .app-sidebar { position: sticky; top: 0; height: 100vh; width: var(--w); flex: none; overflow-y: auto; transition: width var(--dur-slow) var(--ease); }
  .app.is-collapsed .app-sidebar { --w: 4.75rem; }
  .app.is-collapsed :is(.nav-text, .nav-group-label, .nav-app .badge, .bi-chevron-down, .nav-sub) { display: none; }
  .app.is-collapsed .nav-app { justify-content: center; }
}
.page-body { padding: 1.5rem; }
.form-actions { position: sticky; bottom: 0; z-index: 10; display: flex; justify-content: flex-end; gap: .5rem; padding: .9rem 1.5rem;
  background: color-mix(in oklab, var(--surface) 92%, transparent); backdrop-filter: blur(8px); border-top: 1px solid var(--border); }
.table-wrap { max-height: 34rem; overflow: auto; }
.table-wrap thead th { position: sticky; top: 0; z-index: 1; background: var(--surface-muted); font-size: .75rem; text-transform: uppercase; letter-spacing: .05em; color: var(--muted-foreground); }
```

## 1. App shell (sidebar + topbar)

`offcanvas-lg` = inline sidebar on desktop, slide-in drawer below 992px.

```html
<div class="app" id="app">
  <aside class="app-sidebar offcanvas-lg offcanvas-start" id="sidebar" tabindex="-1" aria-label="Main navigation">
    <div class="offcanvas-header"><span class="fw-bold">Tala Commerce</span>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" data-bs-target="#sidebar" aria-label="Close menu"></button></div>
    <a href="/" class="sidebar-brand d-none d-lg-flex"><span class="brand-mark"><i class="bi bi-stars" aria-hidden="true"></i></span><span class="nav-text">Tala Commerce</span></a>
    <nav class="pb-4">
      <div class="nav-group-label">Overview</div>
      <a class="nav-app active" href="/dashboard" aria-current="page" title="Dashboard"><i class="bi bi-grid-1x2" aria-hidden="true"></i><span class="nav-text">Dashboard</span></a>
      <a class="nav-app" href="/reports" title="Reports"><i class="bi bi-graph-up-arrow" aria-hidden="true"></i><span class="nav-text">Reports</span></a>
      <div class="nav-group-label">Sales</div>
      <a class="nav-app" href="/orders" title="Orders"><i class="bi bi-bag" aria-hidden="true"></i><span class="nav-text">Orders</span><span class="badge rounded-pill text-bg-primary ms-auto">12</span></a>
      <a class="nav-app" href="#inv" data-bs-toggle="collapse" role="button" aria-expanded="false" aria-controls="inv" title="Inventory"><i class="bi bi-box-seam" aria-hidden="true"></i><span class="nav-text">Inventory</span><i class="bi bi-chevron-down" aria-hidden="true"></i></a>
      <div class="collapse nav-sub" id="inv">
        <a class="nav-app" href="/inventory/items">Items</a><a class="nav-app" href="/inventory/transfers">Transfers</a>
      </div>
      <a class="nav-app" href="/customers" title="Customers"><i class="bi bi-people" aria-hidden="true"></i><span class="nav-text">Customers</span></a>
      <div class="nav-group-label">System</div>
      <a class="nav-app" href="/settings" title="Settings"><i class="bi bi-gear" aria-hidden="true"></i><span class="nav-text">Settings</span></a>
      <a class="nav-app" aria-disabled="true" title="Billing (soon)"><i class="bi bi-credit-card" aria-hidden="true"></i><span class="nav-text">Billing</span><span class="badge text-bg-secondary ms-auto">Soon</span></a>
    </nav>
  </aside>

  <div class="app-main">
    <header class="app-topbar">
      <button class="btn btn-ghost btn-icon d-lg-none" data-bs-toggle="offcanvas" data-bs-target="#sidebar" aria-controls="sidebar" aria-label="Open menu"><i class="bi bi-list fs-5"></i></button>
      <button class="btn btn-ghost btn-icon d-none d-lg-inline-grid" id="collapseBtn" aria-label="Collapse sidebar" aria-pressed="false"><i class="bi bi-layout-sidebar"></i></button>
      <form class="topbar-search flex-grow-1 d-none d-md-block" role="search">
        <div class="input-group"><span class="input-group-text"><i class="bi bi-search" aria-hidden="true"></i></span>
          <input class="form-control" type="search" placeholder="Search orders, customers…" aria-label="Search"></div>
      </form>
      <div class="ms-auto d-flex align-items-center gap-1">
        <div class="dropdown">
          <button class="btn btn-ghost btn-icon" data-bs-toggle="dropdown" aria-expanded="false" aria-label="Theme"><i class="bi bi-circle-half"></i></button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><button class="dropdown-item" data-theme-set="light" aria-pressed="false"><i class="bi bi-sun me-2"></i>Light</button></li>
            <li><button class="dropdown-item" data-theme-set="dark" aria-pressed="false"><i class="bi bi-moon-stars me-2"></i>Dark</button></li>
            <li><button class="dropdown-item" data-theme-set="system" aria-pressed="false"><i class="bi bi-display me-2"></i>System</button></li>
          </ul>
        </div>
        <div class="dropdown">
          <button class="btn btn-ghost btn-icon" data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false" aria-label="Notifications, 2 unread"><i class="bi bi-bell"></i><span class="dot"></span></button>
          <div class="dropdown-menu dropdown-menu-end p-0" style="width: 22rem">
            <div class="d-flex justify-content-between align-items-center px-3 py-2 border-bottom"><strong>Notifications</strong><button class="btn btn-link btn-sm p-0">Mark all read</button></div>
            <div id="notifList" class="list-group list-group-flush"></div>
            <a class="dropdown-item text-center py-2 border-top small" href="/notifications">View all</a>
          </div>
        </div>
        <div class="dropdown">
          <button class="btn btn-ghost d-flex align-items-center gap-2 ps-1" data-bs-toggle="dropdown" aria-expanded="false" aria-label="Account menu">
            <span class="avatar">AR</span><span class="d-none d-sm-block text-start lh-sm"><span class="d-block fw-semibold small">Andrea Reyes</span><span class="d-block text-body-secondary" style="font-size:.75rem">Branch Manager</span></span></button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item" href="/profile"><i class="bi bi-person me-2"></i>Profile</a></li>
            <li><a class="dropdown-item" href="/settings"><i class="bi bi-gear me-2"></i>Settings</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><button class="dropdown-item text-danger"><i class="bi bi-box-arrow-right me-2"></i>Sign out</button></li>
          </ul>
        </div>
      </div>
    </header>
    <main class="page-body" id="content"><!-- page header + blocks --></main>
  </div>
</div>

<script>
const app = document.getElementById('app'), cBtn = document.getElementById('collapseBtn');
const setCollapsed = (on) => { app.classList.toggle('is-collapsed', on); cBtn.setAttribute('aria-pressed', on); try { localStorage.setItem('sidebarCollapsed', on ? '1' : ''); } catch (e) {} };
try { setCollapsed(localStorage.getItem('sidebarCollapsed') === '1'); } catch (e) {}
cBtn.addEventListener('click', () => setCollapsed(!app.classList.contains('is-collapsed')));
document.getElementById('notifList').innerHTML = DEMO.notifications.map((n) => `
  <a href="#" class="list-group-item list-group-item-action d-flex gap-3 py-3 ${n.unread ? 'bg-body-tertiary' : ''}">
    <span class="icon-chip badge-soft-${n.tone}" style="width:2.25rem;height:2.25rem;font-size:1rem"><i class="bi bi-${n.icon}" aria-hidden="true"></i></span>
    <span><span class="d-block small fw-semibold">${n.title}</span><span class="d-block text-body-secondary" style="font-size:.75rem">${n.meta}</span></span></a>`).join('');
</script>
```

## 2. Page header

```html
<div class="d-flex flex-wrap align-items-end justify-content-between gap-3 mb-4">
  <div>
    <nav aria-label="breadcrumb"><ol class="breadcrumb small mb-1"><li class="breadcrumb-item"><a href="/">Home</a></li><li class="breadcrumb-item active" aria-current="page">Dashboard</li></ol></nav>
    <h1 class="h3 fw-bold mb-0">Good morning, Andrea</h1>
    <p class="text-body-secondary mb-0">Here is what is happening across your 4 branches today.</p>
  </div>
  <div class="d-flex gap-2">
    <button class="btn btn-surface"><i class="bi bi-download me-1"></i>Export</button>
    <button class="btn btn-primary"><i class="bi bi-plus-lg me-1"></i>New order</button>
  </div>
</div>
```

## 3. KPI card row

```html
<div class="row g-3 mb-4" id="kpis"></div>
<script>
const spark = (pts) => { const max = Math.max(...pts), min = Math.min(...pts), w = 96, h = 32;
  const d = pts.map((p, i) => `${(i / (pts.length - 1)) * w},${h - ((p - min) / (max - min || 1)) * h}`).join(' ');
  return `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" aria-hidden="true"><polyline points="${d}" fill="none" stroke="var(--chart-1)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`; };
document.getElementById('kpis').innerHTML = DEMO.kpis.map((k) => `
  <div class="col-sm-6 col-xl-3"><div class="card card-hover h-100"><div class="card-body">
    <div class="d-flex justify-content-between align-items-start mb-3">
      <span class="icon-chip"><i class="bi bi-${k.icon}" aria-hidden="true"></i></span>
      <span class="badge-soft badge-soft-${k.trend >= 0 ? 'success' : 'error'}" aria-label="${k.trend >= 0 ? 'Up' : 'Down'} ${Math.abs(k.trend)}% vs last month">
        <i class="bi bi-arrow-${k.trend >= 0 ? 'up' : 'down'}-right" aria-hidden="true"></i>${Math.abs(k.trend)}%</span>
    </div>
    <div class="text-body-secondary small">${k.label}</div>
    <div class="d-flex justify-content-between align-items-end gap-2">
      <div class="fs-4 fw-bold">${k.format === 'currency' ? fmt.peso(k.value) : fmt.num(k.value)}</div>${spark(k.spark)}
    </div></div></div></div>`).join('');
</script>
```

## 4. Chart card (Chart.js, theme-aware, no re-init on theme change)

```html
<div class="row g-3 mb-4">
  <div class="col-xl-8"><div class="card h-100">
    <div class="card-header d-flex justify-content-between align-items-center py-3"><div><h2 class="h6 mb-0">Sales by branch</h2><small class="text-body-secondary">Last 6 months</small></div>
      <select class="form-select form-select-sm w-auto" aria-label="Period"><option>6 months</option><option>12 months</option></select></div>
    <div class="card-body"><div style="height:300px"><canvas id="salesChart" role="img" aria-label="Line chart of monthly sales for Cauayan, Santiago and Tuguegarao"></canvas></div></div>
  </div></div>
  <div class="col-xl-4"><div class="card h-100"><div class="card-header py-3"><h2 class="h6 mb-0">Top branches</h2></div>
    <div class="card-body vstack gap-3" id="topBranches"></div></div></div>
</div>
<script>
const tok = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const S = DEMO.salesByMonth;
const salesChart = new Chart(document.getElementById('salesChart'), {
  type: 'line',
  data: { labels: S.labels, datasets: S.series.map((s, i) => ({ label: s.name, data: s.data, tension: .35, borderWidth: 2,
    pointRadius: 0, pointHoverRadius: 5, fill: i === 0, borderDash: i === 2 ? [6, 4] : [] })) }, // dash = not color-only
  options: { responsive: true, maintainAspectRatio: false, animation: reduceMotion ? false : { duration: 600 },
    interaction: { mode: 'index', intersect: false },
    plugins: { legend: { position: 'bottom', labels: { usePointStyle: true, boxWidth: 8 } },
      tooltip: { borderWidth: 1, padding: 10, callbacks: { label: (c) => ` ${c.dataset.label}: ${fmt.peso(c.parsed.y)}` } } },
    scales: { x: { grid: { display: false }, ticks: {} }, y: { border: { display: false }, grid: {}, ticks: { callback: (v) => '₱' + v / 1000 + 'k' } } } },
});
function themeChart(ch) {
  const c = [1, 2, 3, 4, 5].map((n) => tok(`--chart-${n}`)), muted = tok('--muted-foreground'), grid = tok('--chart-grid');
  ch.data.datasets.forEach((d, i) => { d.borderColor = d.pointBackgroundColor = c[i];
    d.backgroundColor = (ctx) => { const a = ctx.chart.chartArea; if (!a) return 'transparent';
      const g = ctx.chart.ctx.createLinearGradient(0, a.top, 0, a.bottom); g.addColorStop(0, c[i] + '40'); g.addColorStop(1, c[i] + '00'); return g; }; }); // tokens are 6-digit hex
  const o = ch.options; o.scales.x.ticks.color = o.scales.y.ticks.color = o.plugins.legend.labels.color = muted;
  o.scales.y.grid.color = grid;
  Object.assign(o.plugins.tooltip, { backgroundColor: tok('--surface-elevated'), titleColor: tok('--foreground'), bodyColor: tok('--foreground'), borderColor: tok('--border') });
  ch.update('none');
}
themeChart(salesChart);
document.addEventListener('themechange', () => themeChart(salesChart));
const totals = S.series.map((s) => ({ name: s.name, total: s.data.reduce((a, b) => a + b, 0) })), top = Math.max(...totals.map((t) => t.total));
document.getElementById('topBranches').innerHTML = totals.map((t, i) => `<div><div class="d-flex justify-content-between small mb-1"><span class="fw-semibold">${t.name}</span><span>${fmt.peso(t.total)}</span></div>
  <div class="progress" style="height:.5rem" role="progressbar" aria-label="${t.name} share" aria-valuenow="${Math.round(t.total / top * 100)}" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar" style="width:${t.total / top * 100}%;background:var(--chart-${i + 1})"></div></div></div>`).join('');
</script>
```

Data table, form, empty state, toast and skeleton blocks: [bootstrap-data.md](bootstrap-data.md).
