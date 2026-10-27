# Bootstrap 5.3 data, form and feedback blocks

Uses `kit.css` and the shell from [bootstrap-app.md](bootstrap-app.md), tokens from [tokens-and-theme.md](tokens-and-theme.md), rows from [demo-data.md](demo-data.md).

## 5. Data table page

```html
<div class="card">
  <div class="card-body d-flex flex-wrap gap-2 align-items-center border-bottom">
    <div class="input-group" style="max-width:18rem"><span class="input-group-text"><i class="bi bi-search" aria-hidden="true"></i></span>
      <input id="q" type="search" class="form-control" placeholder="Search order or customer" aria-label="Search orders"></div>
    <div class="dropdown">
      <button class="btn btn-surface" data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false"><i class="bi bi-funnel me-1"></i>Status <span class="badge-soft badge-soft-primary ms-1" id="fCount" hidden></span></button>
      <div class="dropdown-menu p-3" style="min-width:14rem"><div class="vstack gap-2" id="statusFilters"></div>
        <div class="d-flex justify-content-between mt-3"><button class="btn btn-sm btn-ghost" id="fReset">Reset</button><button class="btn btn-sm btn-primary" id="fApply">Apply</button></div></div>
    </div>
    <div class="input-group w-auto"><span class="input-group-text"><i class="bi bi-calendar3" aria-hidden="true"></i></span>
      <input type="date" class="form-control" value="2026-10-01" aria-label="From date"><input type="date" class="form-control" value="2026-10-27" aria-label="To date"></div>
    <div class="ms-auto d-flex gap-2">
      <div class="dropdown"><button class="btn btn-surface" data-bs-toggle="dropdown" aria-expanded="false"><i class="bi bi-box-arrow-up me-1"></i>Export</button>
        <ul class="dropdown-menu dropdown-menu-end"><li><button class="dropdown-item"><i class="bi bi-filetype-csv me-2"></i>CSV</button></li><li><button class="dropdown-item"><i class="bi bi-file-earmark-excel me-2"></i>Excel</button></li><li><button class="dropdown-item"><i class="bi bi-file-earmark-pdf me-2"></i>PDF</button></li></ul></div>
      <button class="btn btn-primary"><i class="bi bi-plus-lg me-1"></i>Add order</button>
    </div>
  </div>
  <div id="bulkBar" class="px-3 py-2 border-bottom bg-body-tertiary small d-flex align-items-center gap-2" hidden>
    <span id="selCount"></span><button class="btn btn-sm btn-surface">Mark as paid</button><button class="btn btn-sm btn-danger">Cancel</button></div>
  <div class="table-wrap">
    <table class="table table-hover align-middle mb-0">
      <thead><tr>
        <th scope="col" style="width:2.5rem"><input class="form-check-input" type="checkbox" id="selAll" aria-label="Select all rows"></th>
        <th scope="col">Order</th><th scope="col">Customer</th><th scope="col">Branch</th><th scope="col">Date</th>
        <th scope="col" class="text-end">Amount</th><th scope="col">Status</th><th scope="col" class="text-end"><span class="visually-hidden">Actions</span></th></tr></thead>
      <tbody id="rows"></tbody>
    </table>
  </div>
  <div class="card-body d-flex flex-wrap justify-content-between align-items-center gap-2 border-top">
    <small class="text-body-secondary" id="rowCount"></small>
    <nav aria-label="Orders pages"><ul class="pagination pagination-sm mb-0">
      <li class="page-item disabled"><span class="page-link" aria-label="Previous page"><i class="bi bi-chevron-left"></i></span></li>
      <li class="page-item active" aria-current="page"><span class="page-link">1</span></li>
      <li class="page-item"><a class="page-link" href="?page=2">2</a></li><li class="page-item"><a class="page-link" href="?page=3">3</a></li>
      <li class="page-item"><a class="page-link" href="?page=2" aria-label="Next page"><i class="bi bi-chevron-right"></i></a></li></ul></nav>
  </div>
</div>

<script>
const tbody = document.getElementById('rows'), cap = (s) => s[0].toUpperCase() + s.slice(1);
const skeletonRows = (n = 6) => Array.from({ length: n }, () => `<tr aria-hidden="true"><td><span class="skeleton" style="width:1rem;height:1rem"></span></td>
  <td><span class="skeleton" style="width:5rem;height:.8rem"></span></td><td><div class="d-flex gap-2 align-items-center"><span class="skeleton rounded-circle" style="width:2.25rem;height:2.25rem"></span><span class="skeleton" style="width:7rem;height:.8rem"></span></div></td>
  <td><span class="skeleton" style="width:4rem;height:.8rem"></span></td><td><span class="skeleton" style="width:5rem;height:.8rem"></span></td><td><span class="skeleton ms-auto" style="width:4rem;height:.8rem"></span></td><td><span class="skeleton" style="width:4.5rem;height:1.4rem;border-radius:999px"></span></td><td></td></tr>`).join('');
const emptyRow = `<tr><td colspan="8"><div class="text-center py-5"><span class="icon-chip mx-auto mb-3"><i class="bi bi-inbox" aria-hidden="true"></i></span>
  <h3 class="h6">No orders match your filters</h3><p class="text-body-secondary small mb-3">Try a different status or date range.</p>
  <button class="btn btn-surface btn-sm" id="clearFilters">Clear filters</button></div></td></tr>`;
function renderRows(list) {
  tbody.innerHTML = list.length ? list.map((o) => `<tr>
    <td><input class="form-check-input row-check" type="checkbox" aria-label="Select ${o.id}"></td>
    <td><a href="/orders/${o.id}" class="fw-semibold text-decoration-none">${o.id}</a></td>
    <td><div class="d-flex align-items-center gap-2"><span class="avatar">${fmt.initials(o.customer)}</span><div class="lh-sm"><div class="fw-semibold">${o.customer}</div><small class="text-body-secondary">${o.email}</small></div></div></td>
    <td>${o.branch}</td><td class="text-nowrap">${fmt.date(o.date)}</td><td class="text-end fw-semibold">${fmt.peso(o.amount)}</td>
    <td><span class="badge-soft badge-soft-${STATUS_TONE[o.status]}">${cap(o.status)}</span></td>
    <td class="text-end"><div class="dropdown"><button class="btn btn-ghost btn-icon" data-bs-toggle="dropdown" data-bs-popper-config='{"strategy":"fixed"}' aria-expanded="false" aria-label="Actions for ${o.id}"><i class="bi bi-three-dots-vertical"></i></button>
      <ul class="dropdown-menu dropdown-menu-end"><li><a class="dropdown-item" href="/orders/${o.id}"><i class="bi bi-eye me-2"></i>View</a></li><li><button class="dropdown-item"><i class="bi bi-pencil me-2"></i>Edit</button></li>
      <li><button class="dropdown-item"><i class="bi bi-printer me-2"></i>Print receipt</button></li><li><hr class="dropdown-divider"></li><li><button class="dropdown-item text-danger"><i class="bi bi-x-circle me-2"></i>Cancel order</button></li></ul></div></td></tr>`).join('') : emptyRow;
  document.getElementById('rowCount').textContent = `Showing ${list.length ? 1 : 0}–${list.length} of ${DEMO.ordersTotal} orders`;
}
tbody.innerHTML = skeletonRows();                 // loading state
setTimeout(() => renderRows(DEMO.orders), 600);   // replace with: fetch('/api/orders').then(r => r.json()).then(renderRows)
document.getElementById('q').addEventListener('input', (e) => { const q = e.target.value.toLowerCase();
  renderRows(DEMO.orders.filter((o) => (o.id + o.customer).toLowerCase().includes(q))); });
document.getElementById('statusFilters').innerHTML = Object.keys(STATUS_TONE).map((s) => `<div class="form-check"><input class="form-check-input" type="checkbox" id="st-${s}" value="${s}"><label class="form-check-label" for="st-${s}">${cap(s)}</label></div>`).join('');
const applyStatus = (reset) => { const on = [...document.querySelectorAll('#statusFilters input')].filter((i) => (reset ? (i.checked = false) : i.checked)).map((i) => i.value);
  const fc = document.getElementById('fCount'); fc.hidden = !on.length; fc.textContent = on.length;
  renderRows(on.length ? DEMO.orders.filter((o) => on.includes(o.status)) : DEMO.orders); };
document.getElementById('fApply').onclick = () => applyStatus(false);
document.getElementById('fReset').onclick = () => applyStatus(true);
tbody.addEventListener('click', (e) => { if (e.target.id === 'clearFilters') { document.getElementById('q').value = ''; applyStatus(true); } });
const selAll = document.getElementById('selAll');
document.addEventListener('change', (e) => {
  const boxes = [...document.querySelectorAll('.row-check')];
  if (e.target === selAll) boxes.forEach((b) => (b.checked = selAll.checked));
  const n = boxes.filter((b) => b.checked).length;
  selAll.checked = n > 0 && n === boxes.length; selAll.indeterminate = n > 0 && n < boxes.length;
  document.getElementById('bulkBar').hidden = !n; document.getElementById('selCount').textContent = `${n} selected`;
});
</script>
```

Detail view: open a `.offcanvas-end` drawer (`--bs-offcanvas-width: 28rem`) from the View action instead of leaving the page.

## 6. Sectioned form card with sticky action bar

```html
<form class="card needs-validation overflow-hidden" novalidate>
  <div class="card-body p-4">
    <div class="row g-4 pb-4 border-bottom">
      <div class="col-lg-4"><h2 class="h6 mb-1">Customer details</h2><p class="small text-body-secondary mb-0">Used on receipts and BIR-ready invoices.</p></div>
      <div class="col-lg-8"><div class="row g-3">
        <div class="col-md-6"><label class="form-label" for="fn">Full name</label><input class="form-control" id="fn" required placeholder="Maria Santos"><div class="invalid-feedback">Enter the customer's name.</div></div>
        <div class="col-md-6"><label class="form-label" for="em">Email</label><input type="email" class="form-control" id="em" required placeholder="maria@mail.example"><div class="invalid-feedback">Enter a valid email.</div></div>
        <div class="col-md-6"><label class="form-label" for="br">Branch</label><select class="form-select" id="br" required><option value="">Choose…</option><option>Cauayan</option><option>Santiago</option><option>Tuguegarao</option></select><div class="invalid-feedback">Pick a branch.</div></div>
        <div class="col-md-6"><label class="form-label" for="dt">Order date</label><input type="date" class="form-control" id="dt" value="2026-10-27"></div>
      </div></div>
    </div>
    <div class="row g-4 py-4 border-bottom">
      <div class="col-lg-4"><h2 class="h6 mb-1">Payment</h2><p class="small text-body-secondary mb-0">Amounts in Philippine peso, VAT inclusive.</p></div>
      <div class="col-lg-8"><div class="row g-3">
        <div class="col-md-6"><label class="form-label" for="amt">Amount</label><div class="input-group has-validation"><span class="input-group-text">₱</span><input type="number" step="0.01" min="1" class="form-control" id="amt" required placeholder="0.00"><div class="invalid-feedback">Amount must be at least ₱1.00.</div></div></div>
        <div class="col-md-6"><label class="form-label" for="pm">Method</label><select class="form-select" id="pm"><option>Cash</option><option>E-wallet</option><option>Bank transfer</option></select></div>
        <div class="col-12"><div class="form-check form-switch"><input class="form-check-input" type="checkbox" role="switch" id="sms" checked><label class="form-check-label" for="sms">Send SMS receipt</label></div></div>
      </div></div>
    </div>
    <div class="row g-4 pt-4">
      <div class="col-lg-4"><h2 class="h6 mb-1">Attachments</h2><p class="small text-body-secondary mb-0">PNG or JPG, up to 2 MB.</p></div>
      <div class="col-lg-8 d-flex align-items-center gap-3">
        <img id="preview" alt="" class="rounded border object-fit-cover" width="72" height="72" hidden>
        <label class="btn btn-surface mb-0" for="file"><i class="bi bi-upload me-1"></i>Upload file</label><input type="file" id="file" accept="image/*" class="visually-hidden">
        <textarea class="form-control" rows="2" placeholder="Notes for the branch (optional)" aria-label="Notes"></textarea>
      </div>
    </div>
  </div>
  <div class="form-actions"><button type="button" class="btn btn-surface">Cancel</button>
    <button type="submit" class="btn btn-primary"><span class="spinner-border spinner-border-sm me-1" hidden aria-hidden="true"></span>Save order</button></div>
</form>
<script>
document.getElementById('file').addEventListener('change', (e) => { const f = e.target.files[0], img = document.getElementById('preview');
  if (f) { img.src = URL.createObjectURL(f); img.hidden = false; img.alt = f.name; } });
document.querySelectorAll('.needs-validation').forEach((form) => form.addEventListener('submit', (e) => {
  e.preventDefault(); form.classList.add('was-validated'); if (!form.checkValidity()) return form.querySelector(':invalid')?.focus();
  const btn = form.querySelector('[type=submit]'); btn.disabled = true; btn.querySelector('.spinner-border').hidden = false;
  setTimeout(() => { btn.disabled = false; btn.querySelector('.spinner-border').hidden = true; showToast('Order saved', 'success'); }, 800);
}));
</script>
```

## 7. Empty state (standalone card)

```html
<div class="card"><div class="card-body text-center py-5 px-4">
  <div class="mx-auto mb-3 d-grid rounded-circle" style="width:4.5rem;height:4.5rem;place-items:center;background:var(--primary-soft);color:var(--primary)"><i class="bi bi-box-seam fs-2" aria-hidden="true"></i></div>
  <h2 class="h5">No products yet</h2>
  <p class="text-body-secondary mx-auto" style="max-width:26rem">Add your first product or import a CSV from your old system. Stock levels sync to every branch.</p>
  <div class="d-flex justify-content-center gap-2"><button class="btn btn-primary"><i class="bi bi-plus-lg me-1"></i>Add product</button><button class="btn btn-surface"><i class="bi bi-filetype-csv me-1"></i>Import CSV</button></div>
</div></div>
```

Error variant: same layout, `badge-soft-error` colors, icon `bi-wifi-off`, text "We couldn't load orders", button "Retry".

## 8. Toast

```html
<div class="toast-container position-fixed bottom-0 end-0 p-3" id="toasts" aria-live="polite" aria-atomic="true"></div>
<script>
function showToast(msg, tone = 'success') {
  const icon = { success: 'check-circle-fill', error: 'x-circle-fill', warning: 'exclamation-triangle-fill', info: 'info-circle-fill' }[tone];
  const el = document.createElement('div'); el.className = 'toast align-items-center'; el.setAttribute('role', tone === 'error' ? 'alert' : 'status');
  el.innerHTML = `<div class="d-flex align-items-center gap-2 p-3"><i class="bi bi-${icon}" style="color:var(--${tone})" aria-hidden="true"></i><span class="me-auto">${msg}</span>
    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button></div>`;
  document.getElementById('toasts').append(el); const t = new bootstrap.Toast(el, { delay: 4000 }); t.show();
  el.addEventListener('hidden.bs.toast', () => el.remove());
}
</script>
```

## 9. Skeleton loader (cards)

```html
<div class="row g-3" aria-busy="true" aria-label="Loading">
  <div class="col-sm-6 col-xl-3"><div class="card"><div class="card-body">
    <span class="skeleton mb-3" style="width:2.75rem;height:2.75rem"></span>
    <span class="skeleton mb-2" style="width:60%;height:.8rem"></span><span class="skeleton" style="width:80%;height:1.5rem"></span>
  </div></div></div>
  <!-- repeat x4; table rows use skeletonRows() from block 5 -->
</div>
```
