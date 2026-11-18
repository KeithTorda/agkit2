# 05 — Forms, Validation, Pickers & Step Wizards

Extracted from `form-element.html`, `form-validation.html`, `form-pickers.html`, `form-wizard.html`, `form-ckeditor.html`, `uc-select2.html`, and `email-compose.html`.

---

## 1. Standard 2-Column Data Entry Form Card (`form-element.html` + `form-validation.html`)

Always include explicit `<label for="...">`, proper input `type`, inline `.invalid-feedback`, and submit-lock protection:

```html
<div class="card">
  <div class="card-header">
    <div>
      <h4 class="card-title mb-1">Register New Customer</h4>
      <p class="subtitle mb-0">Fields marked with <span class="text-danger">*</span> are required</p>
    </div>
  </div>
  <div class="card-body">
    <div class="basic-form">
      <form id="customerRegistrationForm" novalidate>
        <div class="row">
          <div class="mb-3 col-md-6">
            <label class="form-label fw-semibold" for="customerFullName">
              Full Name <span class="text-danger">*</span>
            </label>
            <input
              type="text"
              id="customerFullName"
              name="full_name"
              class="form-control input-default"
              placeholder="e.g. Juan Dela Cruz"
              required
            >
            <div class="invalid-feedback">Enter the customer's full name.</div>
          </div>

          <div class="mb-3 col-md-6">
            <label class="form-label fw-semibold" for="customerPhone">
              Mobile Number <span class="text-danger">*</span>
            </label>
            <div class="input-group">
              <span class="input-group-text">+63</span>
              <input
                type="tel"
                id="customerPhone"
                name="mobile_number"
                class="form-control tabular-nums"
                placeholder="917 123 4567"
                required
              >
              <div class="invalid-feedback">Enter a valid 10-digit mobile number.</div>
            </div>
          </div>

          <div class="mb-3 col-md-6">
            <label class="form-label fw-semibold" for="customerCategory">Account Type</label>
            <select id="customerCategory" name="account_type" class="default-select form-control wide">
              <option value="retail">Retail Walk-In</option>
              <option value="wholesale">Wholesale Partner</option>
              <option value="government">Government / LGU</option>
            </select>
          </div>

          <div class="mb-3 col-md-6">
            <label class="form-label fw-semibold" for="creditLimitAmount">Credit Limit (₱)</label>
            <input
              type="number"
              step="0.01"
              min="0"
              id="creditLimitAmount"
              name="credit_limit"
              class="form-control tabular-nums"
              placeholder="0.00"
            >
          </div>

          <div class="mb-3 col-12">
            <label class="form-label fw-semibold" for="billingAddress">Complete Address</label>
            <textarea
              id="billingAddress"
              name="billing_address"
              class="form-control"
              rows="3"
              placeholder="House/Unit No., Street, Barangay, Municipality, Province"
            ></textarea>
          </div>

          <div class="mb-4 col-12">
            <div class="form-check custom-checkbox checkbox-primary">
              <input type="checkbox" class="form-check-input" id="isVatExempt">
              <label class="form-check-label" for="isVatExempt">
                Senior Citizen / PWD VAT-Exempt Account
              </label>
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-end gap-2 border-top pt-3">
          <button type="button" class="btn btn-light">Cancel</button>
          <button type="submit" class="btn btn-primary">
            Save Customer
          </button>
        </div>
      </form>
    </div>
  </div>
</div>
```

---

## 2. Input, Checkbox & Select Variants Catalog

| Element | Template Classes | Reference File |
|---|---|---|
| Standard Rounded-12px Input | `form-control input-default` | `form-element.html` |
| Pill Input | `form-control input-rounded` | `form-element.html` |
| Sizing | `form-control form-control-lg` / `form-control-sm` | `form-element.html` |
| Colored Custom Checkbox | `form-check custom-checkbox checkbox-primary` (`info`, `success`, `warning`, `danger`) | `form-element.html` |
| Switch Toggle | `form-check form-switch` | `form-element.html` |
| Icon-Prefixed Input Group | `input-group` + `<span class="input-group-text"><i class="fa fa-user"></i></span>` | `form-validation.html` |
| File Upload Input | `form-file` / `form-control` (`type="file"`) or Dropzone `.dropzone` | `form-element.html`, `email-compose.html` |
| Searchable Select (Large Lists) | `vendor/select2` (`#single-select`, `.multi-select`) | `uc-select2.html` |
| Date / Range / Time Pickers | Native `<input type="date">` (preferred for zero-JS simplicity) or `bootstrap-daterangepicker` / `pickadate` | `form-pickers.html` |

---

## 3. Multi-Step Form Wizard (`form-wizard.html`)

Use for multi-part registrations (Patient Intake, Student Enrollment, Loan/Permit Application, Checkout):

```html
<div class="card">
  <div class="card-header">
    <h4 class="card-title">Enrollment Stepper</h4>
  </div>
  <div class="card-body">
    <div id="smartwizard" class="form-wizard order-create">
      <ul class="nav nav-wizard">
        <li><a class="nav-link active" href="#stepPersonal"><span>1</span></a></li>
        <li><a class="nav-link" href="#stepAddress"><span>2</span></a></li>
        <li><a class="nav-link" href="#stepDocuments"><span>3</span></a></li>
        <li><a class="nav-link" href="#stepReview"><span>4</span></a></li>
      </ul>
      <div class="tab-content mt-4">
        <div id="stepPersonal" class="tab-pane active" role="tabpanel">
          <!-- Step 1 Fields -->
        </div>
      </div>
    </div>
  </div>
</div>
```
*(In React/Next.js, reuse the exact `.form-wizard.order-create` + `ul.nav.nav-wizard` markup driven by `activeStepIndex` state—no jQuery SmartWizard plugin needed!)*
