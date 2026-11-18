# 06 — Buttons, Badges, Modals, Alerts, Tabs & Accordions

Extracted from `ui-button.html`, `ui-button-group.html`, `ui-badge.html`, `ui-modal.html`, `ui-alert.html`, `ui-tab.html`, `ui-accordion.html`, `uc-sweetalert.html`, and `uc-toastr.html`.

---

## 1. Button System (`ui-button.html`)

Always use semantic `<button type="button|submit">` for actions and `<a>` for navigation:

```html
<!-- 1. Primary Action -->
<button type="submit" class="btn btn-primary">Save Changes</button>

<!-- 2. Soft Tinted Secondary Action (Signature Template Style) -->
<button type="button" class="btn btn-primary light">Export CSV</button>

<!-- 3. Outline Action -->
<button type="button" class="btn btn-outline-primary">Filter Records</button>

<!-- 4. Destructive Action -->
<button type="button" class="btn btn-danger">Delete Customer</button>
<button type="button" class="btn btn-danger light">Void Receipt</button>

<!-- 5. Button with Leading Icon -->
<button type="button" class="btn btn-primary">
  <span class="btn-icon-start text-primary">
    <i class="fa fa-plus" aria-hidden="true"></i>
  </span>
  Create Invoice
</button>

<!-- 6. Square Icon-Only Row Action Buttons (.sharp) — Always include aria-label -->
<button type="button" class="btn btn-primary shadow btn-xs sharp" aria-label="Edit record">
  <i class="fas fa-pencil-alt" aria-hidden="true"></i>
</button>
<button type="button" class="btn btn-danger shadow btn-xs sharp" aria-label="Delete record">
  <i class="fa fa-trash" aria-hidden="true"></i>
</button>

<!-- 7. In-Flight Loading State (Duplicate Submit Protection) -->
<button type="submit" class="btn btn-primary" disabled aria-busy="true">
  <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
  Saving...
</button>
```

---

## 2. Status Badges (`ui-badge.html`)

Standardize status colors across every table and detail header in the system:

```html
<!-- Soft Tinted Status Pills (Preferred for Tables) -->
<span class="badge light badge-success">Paid / Active</span>
<span class="badge light badge-warning">Pending Verification</span>
<span class="badge light badge-info">Processing</span>
<span class="badge light badge-danger">Voided / Suspended</span>
<span class="badge light badge-secondary">Archived / Draft</span>

<!-- Rounded Pill & Sizing Modifiers -->
<span class="badge badge-rounded badge-primary">Primary Pill</span>
<span class="badge badge-sm light badge-primary">Small</span>
<span class="badge badge-lg light badge-success">Large</span>
```

---

## 3. Centered Action & Confirmation Modals (`ui-modal.html`)

### Form / Detail Modal (`modal-dialog-centered`)
```html
<div class="modal fade" id="recordFormModal" tabindex="-1" aria-labelledby="recordFormModalTitle" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="recordFormModalTitle">Update Inventory Item</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close modal"></button>
      </div>
      <div class="modal-body">
        <!-- Form fields -->
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-danger light" data-bs-dismiss="modal">Cancel</button>
        <button type="submit" class="btn btn-primary">Save Changes</button>
      </div>
    </div>
  </div>
</div>
```

### Destructive Confirmation Modal (Replaces Browser `confirm()`)
```html
<div class="modal fade" id="confirmDeleteModal" tabindex="-1" aria-labelledby="confirmDeleteTitle" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header border-0 pb-0">
        <h5 class="modal-title text-danger" id="confirmDeleteTitle">Void Official Receipt?</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p class="mb-2">Receipt <strong>#OR-2026-0891</strong> will be marked as voided and excluded from daily collections. This action is recorded in the audit log.</p>
        <label class="form-label fw-semibold" for="voidReasonInput">Reason for voiding <span class="text-danger">*</span></label>
        <input type="text" id="voidReasonInput" class="form-control" placeholder="e.g. Incorrect amount entered" required>
      </div>
      <div class="modal-footer border-0 pt-0">
        <button type="button" class="btn btn-light" data-bs-dismiss="modal">Keep Receipt</button>
        <button type="button" class="btn btn-danger">Confirm Void</button>
      </div>
    </div>
  </div>
</div>
```

---

## 4. Inline Alerts (`ui-alert.html`)

```html
<!-- Soft Dismissible Feedback Alert with SVG Icon -->
<div class="alert alert-success alert-dismissible fade show" role="alert">
  <i class="las la-check-circle fs-20 me-2 align-middle" aria-hidden="true"></i>
  <strong>Saved!</strong> Patient record has been updated.
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>

<!-- Left-Border Accent Alert (.alert-alt) for System Notices / Errors -->
<div class="alert alert-danger solid alert-end-icon alert-dismissible fade show" role="alert">
  <span><i class="las la-exclamation-triangle" aria-hidden="true"></i></span>
  <strong>Host Connection Error:</strong> Unable to reach payment gateway. Verify network connection and retry.
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
```

---

## 5. Content Tabs & Accordions (`ui-tab.html` & `ui-accordion.html`)

- **Underline Content Tabs (`.custom-tab-1`):** Best inside profile, settings, and multi-section detail cards (`<div class="custom-tab-1"><ul class="nav nav-tabs">...</ul><div class="tab-content pt-4">...</div></div>`).
- **Bordered / Primary Header Accordion (`accordion accordion-primary`):** Best for FAQ, policy sections, or grouped settings (`ui-accordion.html`).
