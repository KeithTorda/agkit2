# 04 — Tables, DataTables, Filter Tabs & Pagination

Extracted from `page-transaction.html`, `page-invoices.html`, `table-datatable-basic.html`, `table-bootstrap-basic.html`, and `ui-pagination.html`.

---

## 1. Filter Pill Tabs + Action Toolbar (`page-transaction.html`)

Place directly above transaction, order, ticket, or queue tables:

```html
<div class="d-flex flex-wrap align-items-center justify-content-between mb-3 gap-2">
  <div class="card-tabs style-1">
    <ul class="nav nav-tabs" role="tablist">
      <li class="nav-item" role="presentation">
        <button type="button" class="nav-link active" data-bs-toggle="tab" data-bs-target="#tabAll" role="tab" aria-selected="true">
          All Records
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button type="button" class="nav-link" data-bs-toggle="tab" data-bs-target="#tabPaid" role="tab" aria-selected="false">
          Completed
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button type="button" class="nav-link" data-bs-toggle="tab" data-bs-target="#tabPending" role="tab" aria-selected="false">
          Pending
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button type="button" class="nav-link" data-bs-toggle="tab" data-bs-target="#tabVoided" role="tab" aria-selected="false">
          Voided
        </button>
      </li>
    </ul>
  </div>

  <div class="d-flex align-items-center gap-2">
    <button type="button" class="btn btn-outline-primary">
      <i class="las la-calendar me-2" aria-hidden="true"></i>Filter Date
    </button>
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createRecordModal">
      <i class="las la-plus me-1" aria-hidden="true"></i>Add Record
    </button>
  </div>
</div>
```

---

## 2. Standard CRUD Table Card (`table-datatable-basic.html` & `table-bootstrap-basic.html`)

Features responsive scroll wrapper, bulk selection checkbox, user avatar cell, `.badge.light` status pills, `tabular-nums` alignment, sharp icon buttons, and unclipped upward-safe row dropdowns:

```html
<div class="card">
  <div class="card-header d-sm-flex d-block align-items-center justify-content-between">
    <div>
      <h4 class="card-title mb-1">Registered Patients</h4>
      <p class="subtitle mb-0">Showing active municipal health records</p>
    </div>
    <div class="input-group search-area mt-sm-0 mt-2" style="max-width: 280px;">
      <input type="search" class="form-control" placeholder="Search name or ID..." aria-label="Search patients">
      <span class="input-group-text"><i class="flaticon-381-search-2" aria-hidden="true"></i></span>
    </div>
  </div>

  <div class="card-body">
    <div class="table-responsive">
      <table class="table table-responsive-md table-hover align-middle mb-0">
        <thead>
          <tr>
            <th style="width: 48px;">
              <div class="form-check custom-checkbox checkbox-primary">
                <input type="checkbox" class="form-check-input" id="selectAllRows" aria-label="Select all rows">
                <label class="form-check-label" for="selectAllRows"></label>
              </div>
            </th>
            <th>Record ID</th>
            <th>Patient Name</th>
            <th>Barangay</th>
            <th>Visit Date</th>
            <th class="text-end">Balance</th>
            <th>Status</th>
            <th class="text-end">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <div class="form-check custom-checkbox checkbox-primary">
                <input type="checkbox" class="form-check-input" id="row_1042" aria-label="Select PT-1042">
                <label class="form-check-label" for="row_1042"></label>
              </div>
            </td>
            <td class="fw-semibold tabular-nums">#PT-1042</td>
            <td>
              <div class="d-flex align-items-center">
                <img src="/assets/images/avatar/1.jpg" class="rounded-lg me-2" width="32" height="32" alt="">
                <span class="w-space-no fw-medium">Maria Clara Santos</span>
              </div>
            </td>
            <td>Poblacion</td>
            <td class="tabular-nums">2026-11-18</td>
            <td class="text-end fw-semibold tabular-nums">₱1,250.00</td>
            <td>
              <span class="badge light badge-success">Active</span>
            </td>
            <td class="text-end">
              <div class="d-inline-flex align-items-center">
                <button type="button" class="btn btn-primary shadow btn-xs sharp me-1" aria-label="Edit Maria Clara Santos">
                  <i class="fas fa-pencil-alt" aria-hidden="true"></i>
                </button>
                <button type="button" class="btn btn-danger shadow btn-xs sharp me-1" aria-label="Delete Maria Clara Santos">
                  <i class="fa fa-trash" aria-hidden="true"></i>
                </button>
                <!-- Use class="dropup" on the last 2 rows of short tables to prevent container clipping -->
                <div class="dropdown">
                  <button type="button" class="btn btn-light btn-xs sharp" data-bs-toggle="dropdown" data-bs-boundary="viewport" aria-expanded="false" aria-label="More actions">
                    <i class="fas fa-ellipsis-v" aria-hidden="true"></i>
                  </button>
                  <div class="dropdown-menu dropdown-menu-end">
                    <a class="dropdown-item" href="/patients/1042">View Details</a>
                    <a class="dropdown-item" href="/patients/1042/print">Print Record</a>
                  </div>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination Footer (ui-pagination.html) -->
    <div class="d-sm-flex align-items-center justify-content-between mt-4 pt-2 border-top">
      <small class="text-muted tabular-nums mb-2 mb-sm-0">Showing 1 to 10 of 128 records</small>
      <nav aria-label="Table pagination">
        <ul class="pagination pagination-gutter pagination-primary no-bg mb-0">
          <li class="page-item page-indicator">
            <button type="button" class="page-link" aria-label="Previous page">
              <i class="la la-angle-left" aria-hidden="true"></i>
            </button>
          </li>
          <li class="page-item active"><button type="button" class="page-link tabular-nums">1</button></li>
          <li class="page-item"><button type="button" class="page-link tabular-nums">2</button></li>
          <li class="page-item"><button type="button" class="page-link tabular-nums">3</button></li>
          <li class="page-item page-indicator">
            <button type="button" class="page-link" aria-label="Next page">
              <i class="la la-angle-right" aria-hidden="true"></i>
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</div>
```

---

## 3. Floating Card-Row Ledger Table (`.dataTablesCard` from `page-transaction.html`)

For high-visibility financial/payment ledgers where each `<tr>` renders as a separated card row:
- Table class: `class="table card-table display mb-4 dataTablesCard"`
- Vendor dependency (only if client-side DataTables JS is used): `vendor/datatables/css/jquery.dataTables.min.css` + `vendor/datatables/js/jquery.dataTables.min.js`.
- In React/Next.js or Laravel Livewire/Inertia, keep the exact `.table.card-table.dataTablesCard` classes and drive sorting/pagination via state or server query parameters instead of jQuery DataTables.
