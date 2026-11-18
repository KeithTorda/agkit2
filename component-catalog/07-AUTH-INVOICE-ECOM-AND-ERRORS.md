# 07 — Authentication, Printable Invoices, E-Commerce/POS & Error Pages

Extracted from `page-login.html`, `page-register.html`, `page-forgot-password.html`, `page-lock-screen.html`, `ecom-invoice.html`, `ecom-product-grid.html`, `ecom-checkout.html`, and `page-error-400..503.html`.

---

## 1. Centered Authentication Card (`page-login.html` / `page-register.html`)

Standalone `vh-100` layout without `#main-wrapper` sidebar:

```html
<body class="vh-100" data-theme-version="light" data-primary="color_1">
  <div class="authincation h-100">
    <div class="container h-100">
      <div class="row justify-content-center h-100 align-items-center">
        <div class="col-md-6 col-lg-5">
          <div class="authincation-content">
            <div class="row no-gutters">
              <div class="col-xl-12">
                <div class="auth-form">
                  <div class="text-center mb-3">
                    <a href="/" class="fw-bold fs-3 text-primary text-decoration-none">SystemName</a>
                  </div>
                  <h4 class="text-center mb-4">Sign in to your account</h4>

                  <form action="/login" method="POST">
                    <div class="mb-3">
                      <label class="form-label mb-1" for="loginEmail"><strong>Email Address</strong></label>
                      <input type="email" id="loginEmail" name="email" class="form-control" placeholder="name@company.com" autocomplete="username" required>
                    </div>
                    <div class="mb-3">
                      <label class="form-label mb-1" for="loginPassword"><strong>Password</strong></label>
                      <input type="password" id="loginPassword" name="password" class="form-control" placeholder="Enter your password" autocomplete="current-password" required>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mt-4 mb-3">
                      <div class="form-check custom-checkbox ms-1">
                        <input type="checkbox" class="form-check-input" id="rememberSession" name="remember">
                        <label class="form-check-label" for="rememberSession">Keep me signed in</label>
                      </div>
                      <a href="/forgot-password" class="text-primary">Forgot Password?</a>
                    </div>
                    <div class="text-center">
                      <button type="submit" class="btn btn-primary btn-block w-100">Sign In</button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
```

---

## 2. Printable Invoice / Official Statement (`ecom-invoice.html`)

Ready for Billing, POS Sales Invoices, Purchase Orders, and Official Slips (pair with `@media print { .nav-header, .header, .dlabnav, .footer, .no-print { display: none !important; } .content-body { margin-left: 0 !important; padding-top: 0 !important; } }`):

```html
<div class="card mt-3">
  <div class="card-header d-flex justify-content-between align-items-center">
    <span class="tabular-nums">Invoice <strong>#SI-2026-00418</strong></span>
    <span><strong>Status:</strong> <span class="badge light badge-success ms-1">Paid</span></span>
  </div>
  <div class="card-body">
    <div class="row mb-4">
      <div class="mt-2 col-xl-4 col-md-6">
        <h6 class="text-muted text-uppercase fs-12">Issued By</h6>
        <div><strong>System Business Name</strong></div>
        <div>Poblacion, Luna, Apayao</div>
        <div>TIN: <span class="tabular-nums">000-123-456-000</span></div>
      </div>
      <div class="mt-2 col-xl-4 col-md-6">
        <h6 class="text-muted text-uppercase fs-12">Billed To</h6>
        <div><strong>Juan Dela Cruz</strong></div>
        <div>San Isidro, Luna, Apayao</div>
        <div>Date Issued: <span class="tabular-nums">2026-11-18</span></div>
      </div>
      <div class="mt-2 col-xl-4 col-md-12 text-xl-end no-print">
        <button type="button" class="btn btn-primary" onclick="window.print()">
          <i class="las la-print me-1" aria-hidden="true"></i> Print Invoice
        </button>
      </div>
    </div>

    <div class="table-responsive">
      <table class="table table-striped align-middle">
        <thead>
          <tr>
            <th class="text-center">#</th>
            <th>Item Description</th>
            <th class="text-end">Unit Cost</th>
            <th class="text-center">Qty</th>
            <th class="text-end">Line Total</th>
          </tr>
        </thead>
        <tbody class="tabular-nums">
          <tr>
            <td class="text-center">1</td>
            <td class="fw-medium">Engine Oil 10W-40 Synthetic (1L)</td>
            <td class="text-end">₱480.00</td>
            <td class="text-center">2</td>
            <td class="text-end fw-semibold">₱960.00</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="row justify-content-end">
      <div class="col-lg-4 col-sm-6">
        <table class="table table-clear mb-0 tabular-nums">
          <tbody>
            <tr>
              <td class="text-start"><strong>VATable Sales</strong></td>
              <td class="text-end">₱857.14</td>
            </tr>
            <tr>
              <td class="text-start"><strong>VAT (12%)</strong></td>
              <td class="text-end">₱102.86</td>
            </tr>
            <tr>
              <td class="text-start"><strong>Total Amount Due</strong></td>
              <td class="text-end"><strong>₱960.00</strong></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
```

---

## 3. Product / Item Card Grid (`ecom-product-grid.html`)

Reusable for Storefronts, POS Product Pickers, Equipment Catalogs, and Course/Module Directories:

```html
<div class="col-xl-3 col-lg-6 col-sm-6">
  <div class="card">
    <div class="card-body">
      <div class="new-arrival-product">
        <div class="new-arrivals-img-contnent rounded overflow-hidden">
          <img class="img-fluid w-100" src="/assets/images/product/1.jpg" alt="Brake Pad Set">
        </div>
        <div class="new-arrival-content text-center mt-3">
          <h4><a href="/products/brake-pad-set" class="text-dark">Ceramic Brake Pad Set</a></h4>
          <span class="badge light badge-success mb-2 tabular-nums">28 in stock</span>
          <span class="price d-block fw-bold text-primary fs-18 tabular-nums">₱1,450.00</span>
          <button type="button" class="btn btn-primary btn-sm mt-2 w-100">
            <i class="las la-shopping-cart me-1" aria-hidden="true"></i> Add to Order
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
```

---

## 4. System Error Pages (`page-error-400..503.html`)

Reusable for `400`, `403`, `404`, `500`, and `503` Maintenance / Suspended Hosting notices:

```html
<body class="vh-100" data-theme-version="light">
  <div class="authincation h-100">
    <div class="container h-100">
      <div class="row justify-content-center h-100 align-items-center">
        <div class="col-md-7">
          <div class="form-input-content text-center error-page">
            <h1 class="error-text fw-bold tabular-nums">404</h1>
            <h4><i class="fa fa-exclamation-triangle text-warning me-2" aria-hidden="true"></i>Page Not Found</h4>
            <p>The requested page was moved, removed, or the address was typed incorrectly.</p>
            <div>
              <a class="btn btn-primary" href="/dashboard">Return to Dashboard</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
```
