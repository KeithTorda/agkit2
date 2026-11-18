# 03 — KPI Stat Cards, Standard Cards & Activity Widgets

Extracted from `index.html`, `widget-basic.html`, `cards-center.html`, and `ui-card.html`.

---

## 1. Colored Hero KPI Row (`.invoice-card` from `index.html`)

Used at the very top of dashboards for 4 primary metrics (`col-xl-3 col-xxl-3 col-sm-6`):

```html
<div class="row invoice-card-row">
  <div class="col-xl-3 col-xxl-3 col-sm-6">
    <div class="card bg-primary invoice-card">
      <div class="card-body d-flex align-items-center">
        <div class="icon me-3">
          <i class="las la-file-invoice-dollar text-white fs-36" aria-hidden="true"></i>
        </div>
        <div>
          <h2 class="text-white invoice-num tabular-nums mb-1">₱148,500</h2>
          <span class="text-white fs-18">Total Collections</span>
        </div>
      </div>
    </div>
  </div>

  <div class="col-xl-3 col-xxl-3 col-sm-6">
    <div class="card bg-success invoice-card">
      <div class="card-body d-flex align-items-center">
        <div class="icon me-3">
          <i class="las la-check-circle text-white fs-36" aria-hidden="true"></i>
        </div>
        <div>
          <h2 class="text-white invoice-num tabular-nums mb-1">312</h2>
          <span class="text-white fs-18">Paid Invoices</span>
        </div>
      </div>
    </div>
  </div>

  <div class="col-xl-3 col-xxl-3 col-sm-6">
    <div class="card bg-info invoice-card">
      <div class="card-body d-flex align-items-center">
        <div class="icon me-3">
          <i class="las la-clock text-white fs-36" aria-hidden="true"></i>
        </div>
        <div>
          <h2 class="text-white invoice-num tabular-nums mb-1">24</h2>
          <span class="text-white fs-18">Pending Verification</span>
        </div>
      </div>
    </div>
  </div>

  <div class="col-xl-3 col-xxl-3 col-sm-6">
    <div class="card bg-secondary invoice-card">
      <div class="card-body d-flex align-items-center">
        <div class="icon me-3">
          <i class="las la-users text-white fs-36" aria-hidden="true"></i>
        </div>
        <div>
          <h2 class="text-white invoice-num tabular-nums mb-1">1,284</h2>
          <span class="text-white fs-18">Registered Customers</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

---

## 2. Clean White/Dark Surface KPI Cards (`.widget-stat` from `widget-basic.html`)

Preferred for dense operational dashboards (Clinic patients, School inventory, HRIS attendance) where soft tinted icon circles keep the UI calm and high-contrast in both Light and Dark mode:

### Variant A: Tinted Icon Circle + Metric + Trend Badge
```html
<div class="col-xl-3 col-xxl-6 col-lg-6 col-sm-6">
  <div class="widget-stat card">
    <div class="card-body p-4">
      <div class="media ai-icon">
        <span class="me-3 bgl-primary text-primary">
          <i class="ti-user" aria-hidden="true"></i>
        </span>
        <div class="media-body">
          <p class="mb-1">Registered Patients</p>
          <h4 class="mb-0 tabular-nums">3,280</h4>
          <span class="badge badge-primary tabular-nums">+3.5%</span>
        </div>
      </div>
    </div>
  </div>
</div>
```
*(Available icon background helpers: `bgl-primary text-primary`, `bgl-success text-success`, `bgl-warning text-warning`, `bgl-danger text-danger`, `bgl-info text-info`)*

### Variant B: Metric + Progress Bar Card
```html
<div class="col-xl-3 col-xxl-6 col-lg-6 col-sm-6">
  <div class="widget-stat card">
    <div class="card-body p-4">
      <h4 class="card-title">Monthly Budget Used</h4>
      <h3 class="tabular-nums">₱85,400</h3>
      <div class="progress mb-2">
        <div class="progress-bar progress-animated bg-primary" style="width: 68%" role="progressbar" aria-valuenow="68" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
      <small>68% of ₱125,000 allocation</small>
    </div>
  </div>
</div>
```

---

## 3. Standard Content Card Shell (`ui-card.html`)

Use this exact card header + toolbar pattern for charts, sections, and detail panels:

```html
<div class="card">
  <div class="card-header border-0 pb-0 d-sm-flex d-block align-items-center justify-content-between">
    <div>
      <h4 class="card-title mb-1">Monthly Collections</h4>
      <p class="subtitle mb-0">Verified payments recorded across all branches</p>
    </div>
    <div class="mt-sm-0 mt-2">
      <button type="button" class="btn btn-primary btn-sm">
        <i class="las la-download me-1" aria-hidden="true"></i> Export CSV
      </button>
    </div>
  </div>
  <div class="card-body">
    <!-- Chart, Table, Form, or EmptyState -->
  </div>
</div>
```

---

## 4. Activity Timeline & Recent Logs Widget (`widget-basic.html`)

Ideal for Audit Trails, Patient Visit History, Order Tracking, and System Logs:

```html
<div class="card">
  <div class="card-header border-0 pb-0">
    <h4 class="card-title">Recent Audit Logs</h4>
  </div>
  <div class="card-body">
    <div class="widget-timeline dlab-scroll" style="max-height: 370px;">
      <ul class="timeline">
        <li>
          <div class="timeline-badge success"></div>
          <div class="timeline-panel text-muted">
            <span class="tabular-nums">Today, 10:15 AM</span>
            <h6 class="mb-0">Invoice <strong class="text-primary">#INV-1042</strong> marked Paid by Maria Santos.</h6>
          </div>
        </li>
        <li>
          <div class="timeline-badge warning"></div>
          <div class="timeline-panel text-muted">
            <span class="tabular-nums">Today, 09:42 AM</span>
            <h6 class="mb-0">Stock level low for <strong>Paracetamol 500mg</strong> (12 boxes left).</h6>
          </div>
        </li>
        <li>
          <div class="timeline-badge danger"></div>
          <div class="timeline-panel text-muted">
            <span class="tabular-nums">Yesterday, 04:50 PM</span>
            <h6 class="mb-0">Receipt <strong class="text-danger">#OR-8891</strong> voided (Reason: Duplicate entry).</h6>
          </div>
        </li>
      </ul>
    </div>
  </div>
</div>
```

---

## 5. Designed Empty State & Loading Skeleton (Required on All Data Views)

### Empty State Inside `.card-body`
```html
<div class="card">
  <div class="card-body text-center py-5">
    <div class="d-inline-flex align-items-center justify-content-center rounded-circle bgl-primary text-primary mb-3" style="width: 64px; height: 64px;">
      <i class="las la-folder-open fs-30" aria-hidden="true"></i>
    </div>
    <h5 class="mb-1">No customer records found</h5>
    <p class="text-muted mb-3">Add your first customer record or clear the active search filter.</p>
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createCustomerModal">
      <i class="las la-plus me-1" aria-hidden="true"></i> Add Customer
    </button>
  </div>
</div>
```

### Bootstrap 5 Placeholder Skeleton Inside `.card-body`
```html
<div class="card" aria-busy="true" aria-live="polite">
  <div class="card-body">
    <div class="placeholder-glow mb-3">
      <span class="placeholder col-4 rounded py-2"></span>
    </div>
    <div class="placeholder-glow">
      <span class="placeholder col-12 rounded py-3 mb-2"></span>
      <span class="placeholder col-12 rounded py-3 mb-2"></span>
      <span class="placeholder col-8 rounded py-3"></span>
    </div>
  </div>
</div>
```
