# Tailwind KPI, chart, table, form and feedback blocks

Uses `components.css`, `ui.js` and the shell from [tailwind-app.md](tailwind-app.md), tokens from [tokens-and-theme.md](tokens-and-theme.md), data from [demo-data.md](demo-data.md). Call `lucide.createIcons()` after every render.

## 1. KPI cards + chart card

```html
<div id="kpis" class="mb-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4"></div>
<div class="mb-6 grid gap-4 xl:grid-cols-3">
  <section class="card xl:col-span-2"><div class="flex items-center justify-between border-b border-border px-5 py-4"><div><h2 class="font-semibold">Sales by branch</h2><p class="text-xs text-muted-foreground">Last 6 months</p></div>
    <select class="input h-9 w-auto text-sm" aria-label="Period"><option>6 months</option><option>12 months</option></select></div>
    <div class="h-[300px] p-5"><canvas id="salesChart" role="img" aria-label="Line chart of monthly sales for Cauayan, Santiago and Tuguegarao"></canvas></div></section>
  <section class="card"><div class="border-b border-border px-5 py-4"><h2 class="font-semibold">Top branches</h2></div><div id="topBranches" class="space-y-4 p-5"></div></section>
</div>
<script>
const icon = { 'cash-stack': 'wallet', 'bag-check': 'shopping-bag', people: 'users', receipt: 'receipt' };
document.getElementById('kpis').innerHTML = DEMO.kpis.map((k) => `<div class="card card-hover p-5">
  <div class="mb-4 flex items-start justify-between"><span class="icon-chip"><i data-lucide="${icon[k.icon]}" class="size-5"></i></span>
    <span class="badge-soft ${k.trend >= 0 ? 'tone-success' : 'tone-error'}" aria-label="${k.trend >= 0 ? 'Up' : 'Down'} ${Math.abs(k.trend)}% vs last month">${k.trend >= 0 ? '↑' : '↓'} ${Math.abs(k.trend)}%</span></div>
  <p class="text-sm text-muted-foreground">${k.label}</p>
  <div class="flex items-end justify-between gap-2"><p class="text-2xl font-bold tracking-tight">${k.format === 'currency' ? fmt.peso(k.value) : fmt.num(k.value)}</p>${spark(k.spark)}</div></div>`).join('');
const totals = DEMO.salesByMonth.series.map((s) => ({ name: s.name, total: s.data.reduce((a, b) => a + b, 0) })), top = Math.max(...totals.map((t) => t.total));
document.getElementById('topBranches').innerHTML = totals.map((t, i) => `<div><div class="mb-1 flex justify-between text-sm"><span class="font-semibold">${t.name}</span><span>${fmt.peso(t.total)}</span></div>
  <div class="h-2 rounded-full bg-muted" role="progressbar" aria-label="${t.name} share" aria-valuenow="${Math.round(t.total / top * 100)}" aria-valuemin="0" aria-valuemax="100"><div class="h-2 rounded-full" style="width:${t.total / top * 100}%;background:var(--chart-${i + 1})"></div></div></div>`).join('');
lucide.createIcons();
</script>
```

`spark()`, the Chart.js config and `themeChart()` (reads `--chart-*`, `--chart-grid`, `--muted-foreground`, re-themes on `themechange` with `chart.update('none')`, no re-init) are stack-agnostic: copy blocks 3 and 4 scripts from [bootstrap-app.md](bootstrap-app.md) unchanged.

## 2. Data table page

```html
<section class="card overflow-hidden">
  <div class="flex flex-wrap items-center gap-2 border-b border-border p-4">
    <div class="relative w-full sm:w-72"><i data-lucide="search" class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" aria-hidden="true"></i>
      <input id="q" type="search" class="input pl-9" placeholder="Search order or customer" aria-label="Search orders"></div>
    <div class="relative"><button class="btn btn-surface" data-menu="statusMenu" aria-expanded="false" aria-haspopup="true"><i data-lucide="filter" class="size-4"></i>Status</button>
      <div id="statusMenu" class="menu left-0 right-auto w-56 p-3" hidden><fieldset><legend class="mb-2 text-xs font-semibold uppercase text-muted-foreground">Status</legend><div id="statusFilters" class="space-y-2"></div></fieldset>
        <div class="mt-3 flex justify-between"><button class="btn btn-ghost btn-sm" id="fReset">Reset</button><button class="btn btn-primary btn-sm" id="fApply">Apply</button></div></div></div>
    <div class="flex items-center gap-1"><input type="date" class="input w-auto" value="2026-10-01" aria-label="From date"><span class="text-muted-foreground" aria-hidden="true">–</span><input type="date" class="input w-auto" value="2026-10-27" aria-label="To date"></div>
    <div class="ml-auto flex gap-2">
      <div class="relative"><button class="btn btn-surface" data-menu="exportMenu" aria-expanded="false" aria-haspopup="true"><i data-lucide="upload" class="size-4"></i>Export</button>
        <div id="exportMenu" class="menu" role="menu" hidden><button class="menu-item" role="menuitem">CSV</button><button class="menu-item" role="menuitem">Excel</button><button class="menu-item" role="menuitem">PDF</button></div></div>
      <button class="btn btn-primary"><i data-lucide="plus" class="size-4"></i>Add order</button>
    </div>
  </div>
  <div id="bulkBar" class="flex items-center gap-2 border-b border-border bg-surface-muted px-4 py-2 text-sm" hidden><span id="selCount"></span><button class="btn btn-surface btn-sm">Mark as paid</button><button class="btn btn-danger btn-sm">Cancel</button></div>
  <div class="max-h-[34rem] overflow-auto">
    <table class="w-full text-sm">
      <thead class="sticky top-0 z-10 bg-surface-muted text-left text-xs uppercase tracking-wider text-muted-foreground"><tr>
        <th scope="col" class="w-10 px-4 py-3"><input type="checkbox" class="check" id="selAll" aria-label="Select all rows"></th>
        <th scope="col" class="px-4 py-3">Order</th><th scope="col" class="px-4 py-3">Customer</th><th scope="col" class="px-4 py-3">Branch</th><th scope="col" class="px-4 py-3">Date</th>
        <th scope="col" class="px-4 py-3 text-right">Amount</th><th scope="col" class="px-4 py-3">Status</th><th scope="col" class="px-4 py-3"><span class="sr-only">Actions</span></th></tr></thead>
      <tbody id="rows" class="divide-y divide-border"></tbody>
    </table>
  </div>
  <div class="flex flex-wrap items-center justify-between gap-2 border-t border-border p-4">
    <p class="text-sm text-muted-foreground" id="rowCount"></p>
    <nav aria-label="Orders pages" class="flex gap-1">
      <button class="btn btn-surface btn-icon btn-sm" disabled aria-label="Previous page"><i data-lucide="chevron-left" class="size-4"></i></button>
      <a href="?page=1" class="btn btn-primary btn-sm" aria-current="page">1</a><a href="?page=2" class="btn btn-ghost btn-sm">2</a><a href="?page=3" class="btn btn-ghost btn-sm">3</a>
      <a href="?page=2" class="btn btn-surface btn-icon btn-sm" aria-label="Next page"><i data-lucide="chevron-right" class="size-4"></i></a></nav>
  </div>
</section>
<script>
const tbody = document.getElementById('rows'), cap = (s) => s[0].toUpperCase() + s.slice(1), sk = (w, h = '.8rem') => `<div class="skeleton" style="width:${w};height:${h}"></div>`;
const skeletonRows = (n = 6) => Array.from({ length: n }, () => `<tr aria-hidden="true"><td class="px-4 py-3">${sk('1rem', '1rem')}</td><td class="px-4 py-3">${sk('5rem')}</td>
  <td class="px-4 py-3"><div class="flex items-center gap-2"><div class="skeleton size-9 rounded-full"></div>${sk('7rem')}</div></td><td class="px-4 py-3">${sk('4rem')}</td><td class="px-4 py-3">${sk('5rem')}</td><td class="px-4 py-3">${sk('4rem')}</td><td class="px-4 py-3">${sk('4.5rem', '1.4rem')}</td><td></td></tr>`).join('');
const emptyRow = `<tr><td colspan="8" class="px-4 py-14 text-center"><span class="icon-chip mx-auto mb-3"><i data-lucide="inbox" class="size-5"></i></span>
  <h3 class="font-semibold">No orders match your filters</h3><p class="mb-4 text-sm text-muted-foreground">Try a different status or date range.</p><button class="btn btn-surface btn-sm" id="clearFilters">Clear filters</button></td></tr>`;
function renderRows(list) {
  tbody.innerHTML = list.length ? list.map((o) => `<tr class="transition-colors hover:bg-surface-muted">
    <td class="px-4 py-3"><input type="checkbox" class="check row-check" aria-label="Select ${o.id}"></td>
    <td class="px-4 py-3"><a href="/orders/${o.id}" class="font-semibold text-primary hover:underline">${o.id}</a></td>
    <td class="px-4 py-3"><div class="flex items-center gap-2"><span class="avatar">${fmt.initials(o.customer)}</span><div class="leading-tight"><p class="font-semibold">${o.customer}</p><p class="text-xs text-muted-foreground">${o.email}</p></div></div></td>
    <td class="px-4 py-3">${o.branch}</td><td class="whitespace-nowrap px-4 py-3">${fmt.date(o.date)}</td><td class="px-4 py-3 text-right font-semibold tabular-nums">${fmt.peso(o.amount)}</td>
    <td class="px-4 py-3"><span class="badge-soft tone-${STATUS_TONE[o.status]}">${cap(o.status)}</span></td>
    <td class="relative px-4 py-3 text-right"><button class="btn btn-ghost btn-icon btn-sm" data-menu="m-${o.id}" aria-expanded="false" aria-haspopup="true" aria-label="Actions for ${o.id}"><i data-lucide="ellipsis-vertical" class="size-4"></i></button>
      <div id="m-${o.id}" class="menu" role="menu" hidden><a class="menu-item" role="menuitem" href="/orders/${o.id}"><i data-lucide="eye" class="size-4"></i>View</a><button class="menu-item" role="menuitem"><i data-lucide="pencil" class="size-4"></i>Edit</button>
        <button class="menu-item" role="menuitem"><i data-lucide="printer" class="size-4"></i>Print receipt</button><hr class="my-1 border-border"><button class="menu-item text-error" role="menuitem"><i data-lucide="circle-x" class="size-4"></i>Cancel order</button></div></td></tr>`).join('') : emptyRow;
  document.getElementById('rowCount').textContent = `Showing ${list.length ? 1 : 0}–${list.length} of ${DEMO.ordersTotal} orders`;
  lucide.createIcons();
}
tbody.innerHTML = skeletonRows();
setTimeout(() => renderRows(DEMO.orders), 600); // real data: fetch('/api/orders').then((r) => r.json()).then(renderRows)
document.getElementById('q').addEventListener('input', (e) => { const q = e.target.value.toLowerCase(); renderRows(DEMO.orders.filter((o) => (o.id + o.customer).toLowerCase().includes(q))); });
document.getElementById('statusFilters').innerHTML = Object.keys(STATUS_TONE).map((s) => `<label class="flex items-center gap-2 text-sm"><input type="checkbox" class="check" value="${s}">${cap(s)}</label>`).join('');
const applyStatus = (reset) => { const on = [...document.querySelectorAll('#statusFilters input')].filter((i) => (reset ? (i.checked = false) : i.checked)).map((i) => i.value);
  renderRows(on.length ? DEMO.orders.filter((o) => on.includes(o.status)) : DEMO.orders); };
document.getElementById('fApply').onclick = () => applyStatus(false);
document.getElementById('fReset').onclick = () => applyStatus(true);
tbody.addEventListener('click', (e) => { if (e.target.id === 'clearFilters') { document.getElementById('q').value = ''; applyStatus(true); } });
const selAll = document.getElementById('selAll');
document.addEventListener('change', (e) => { const boxes = [...document.querySelectorAll('.row-check')];
  if (e.target === selAll) boxes.forEach((b) => (b.checked = selAll.checked));
  const n = boxes.filter((b) => b.checked).length; selAll.checked = n > 0 && n === boxes.length; selAll.indeterminate = n > 0 && n < boxes.length;
  document.getElementById('bulkBar').hidden = !n; document.getElementById('selCount').textContent = `${n} selected`; });
</script>
```

Row menus near the bottom of the scroll area: add `top-auto bottom-full` to that `.menu` so it opens upward instead of being clipped.

## 3. Sectioned form card with sticky action bar

```html
<form class="card overflow-hidden" novalidate id="orderForm">
  <div class="divide-y divide-border">
    <div class="grid gap-6 p-6 lg:grid-cols-3">
      <div><h2 class="font-semibold">Customer details</h2><p class="text-sm text-muted-foreground">Used on receipts and BIR-ready invoices.</p></div>
      <div class="grid gap-4 sm:grid-cols-2 lg:col-span-2">
        <div><label class="label" for="fn">Full name</label><input id="fn" class="input" required placeholder="Maria Santos" aria-describedby="fn-err"><p id="fn-err" class="mt-1 hidden text-xs text-error">Enter the customer's name.</p></div>
        <div><label class="label" for="em">Email</label><input id="em" type="email" class="input" required placeholder="maria@mail.example" aria-describedby="em-err"><p id="em-err" class="mt-1 hidden text-xs text-error">Enter a valid email.</p></div>
        <div><label class="label" for="br">Branch</label><select id="br" class="input" required aria-describedby="br-err"><option value="">Choose…</option><option>Cauayan</option><option>Santiago</option><option>Tuguegarao</option></select><p id="br-err" class="mt-1 hidden text-xs text-error">Pick a branch.</p></div>
        <div><label class="label" for="dt">Order date</label><input id="dt" type="date" class="input" value="2026-10-27"></div>
      </div>
    </div>
    <div class="grid gap-6 p-6 lg:grid-cols-3">
      <div><h2 class="font-semibold">Payment</h2><p class="text-sm text-muted-foreground">Philippine peso, VAT inclusive.</p></div>
      <div class="grid gap-4 sm:grid-cols-2 lg:col-span-2">
        <div><label class="label" for="amt">Amount</label><div class="relative"><span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">₱</span>
          <input id="amt" type="number" min="1" step="0.01" class="input pl-7" required placeholder="0.00" aria-describedby="amt-err"></div><p id="amt-err" class="mt-1 hidden text-xs text-error">Amount must be at least ₱1.00.</p></div>
        <div><label class="label" for="pm">Method</label><select id="pm" class="input"><option>Cash</option><option>E-wallet</option><option>Bank transfer</option></select></div>
        <label class="flex items-center gap-3 sm:col-span-2"><input type="checkbox" role="switch" class="peer sr-only" checked>
          <span class="relative h-6 w-11 rounded-full bg-muted transition-colors after:absolute after:left-0.5 after:top-0.5 after:size-5 after:rounded-full after:bg-surface after:transition-transform peer-checked:bg-primary peer-checked:after:translate-x-5 peer-focus-visible:ring-4 peer-focus-visible:ring-primary-soft peer-disabled:opacity-50"></span>
          <span class="text-sm">Send SMS receipt</span></label>
      </div>
    </div>
    <div class="grid gap-6 p-6 lg:grid-cols-3">
      <div><h2 class="font-semibold">Attachments</h2><p class="text-sm text-muted-foreground">PNG or JPG, up to 2 MB.</p></div>
      <div class="flex flex-wrap items-center gap-3 lg:col-span-2">
        <img id="preview" alt="" class="size-16 rounded-lg border border-border object-cover" hidden>
        <label for="file" class="btn btn-surface cursor-pointer"><i data-lucide="upload" class="size-4"></i>Upload file</label><input id="file" type="file" accept="image/*" class="sr-only">
        <textarea class="input min-w-[14rem] flex-1" rows="2" placeholder="Notes for the branch (optional)" aria-label="Notes"></textarea>
      </div>
    </div>
  </div>
  <div class="topbar sticky bottom-0 flex justify-end gap-2 border-t border-border px-6 py-4">
    <button type="button" class="btn btn-surface">Cancel</button>
    <button type="submit" class="btn btn-primary"><i data-lucide="loader-circle" class="hidden size-4 animate-spin" aria-hidden="true"></i>Save order</button></div>
</form>
<script>
document.getElementById('file').addEventListener('change', (e) => { const f = e.target.files[0], img = document.getElementById('preview'); if (f) { img.src = URL.createObjectURL(f); img.alt = f.name; img.hidden = false; } });
document.getElementById('orderForm').addEventListener('submit', (e) => { e.preventDefault(); const form = e.target; let first;
  form.querySelectorAll('[required]').forEach((el) => { const bad = !el.checkValidity(); el.setAttribute('aria-invalid', bad);
    document.getElementById(`${el.id}-err`)?.classList.toggle('hidden', !bad); if (bad && !first) first = el; });
  if (first) return first.focus();
  const btn = form.querySelector('[type=submit]'), spin = btn.querySelector('svg, i'); btn.disabled = true; spin.classList.remove('hidden');
  setTimeout(() => { btn.disabled = false; spin.classList.add('hidden'); showToast('Order saved', 'success'); }, 800); });
</script>
```

## 4. Empty state, toast, skeleton

```html
<!-- Empty state (error variant: tone-error chip, icon wifi-off, "We couldn't load orders", button "Retry") -->
<section class="card px-6 py-14 text-center">
  <span class="mx-auto mb-4 grid size-16 place-items-center rounded-full bg-primary-soft text-primary"><i data-lucide="package-open" class="size-7" aria-hidden="true"></i></span>
  <h2 class="text-lg font-semibold">No products yet</h2>
  <p class="mx-auto mb-5 max-w-md text-sm text-muted-foreground">Add your first product or import a CSV from your old system. Stock levels sync to every branch.</p>
  <div class="flex justify-center gap-2"><button class="btn btn-primary"><i data-lucide="plus" class="size-4"></i>Add product</button><button class="btn btn-surface"><i data-lucide="file-up" class="size-4"></i>Import CSV</button></div>
</section>

<!-- Toast region -->
<div id="toasts" class="fixed bottom-4 right-4 z-[60] flex w-80 flex-col gap-2" aria-live="polite"></div>
<script>
function showToast(msg, tone = 'success') {
  const ic = { success: 'circle-check', error: 'circle-x', warning: 'triangle-alert', info: 'info' }[tone], el = document.createElement('div');
  el.setAttribute('role', tone === 'error' ? 'alert' : 'status');
  el.style.boxShadow = 'var(--shadow-lg)';
  el.className = 'card flex items-center gap-3 p-4 transition duration-200 translate-y-2 opacity-0 motion-reduce:transition-none';
  el.innerHTML = `<i data-lucide="${ic}" class="size-5" style="color:var(--${tone})" aria-hidden="true"></i><p class="flex-1 text-sm">${msg}</p><button class="btn btn-ghost btn-icon btn-sm" aria-label="Dismiss"><i data-lucide="x" class="size-4"></i></button>`;
  document.getElementById('toasts').append(el); lucide.createIcons();
  requestAnimationFrame(() => el.classList.remove('translate-y-2', 'opacity-0'));
  const close = () => { el.classList.add('opacity-0'); setTimeout(() => el.remove(), 200); };
  el.querySelector('button').onclick = close; setTimeout(close, 4000);
}
</script>

<!-- Skeleton cards (table rows: skeletonRows() above) -->
<div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4" aria-busy="true" aria-label="Loading">
  <div class="card p-5"><div class="skeleton mb-4 size-11"></div><div class="skeleton mb-2 h-3 w-3/5"></div><div class="skeleton h-6 w-4/5"></div></div>
  <!-- repeat x4 -->
</div>
```
