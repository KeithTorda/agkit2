---
name: ph-business-compliance
description: "Philippine business rules for POS, invoicing, payroll and records: VAT 12% / VAT-exempt / zero-rated, sales invoice requirements after the EOPT Act, senior citizen and PWD discounts, BIR CAS/POS accreditation needs, e-invoicing (EIS), Z/X readings, peso formatting. Use when building sales, receipts, invoices, reports or payroll for PH businesses."
version: 3.2.0
---

# Philippine business compliance

Requirements to build into PH business systems. Tax rules change: treat this as a checklist, confirm current BIR issuances (Revenue Regulations, RMCs) with the client's accountant, and keep rates and thresholds in config, never hard-coded.

## Steps

1. **Ask the business setup** (or read it from config): VAT-registered or non-VAT, TIN + branch code, registered name/address, whether it uses BIR-accredited POS/CAS, and whether it is covered by e-invoicing (EIS).
2. **Store tax config** in a settings table: VAT rate (currently 12%), VAT status, discount rates, invoice series prefixes, branch codes.
3. **Compute on the server** (rule-06): per line keep `gross`, `discount`, `vatable_sales`, `vat_exempt_sales`, `zero_rated_sales`, `vat_amount`, `net`. Round to 2 decimals at the line, then sum.
4. **VAT math:** VAT-inclusive price → `vatable = price / 1.12`, `vat = price - vatable`. Show VATable Sales, VAT-Exempt Sales, Zero-Rated Sales and VAT Amount on the invoice.
5. **Senior citizen / PWD:** 20% discount on qualified goods/services and exemption from VAT for qualified sales. Typical order: remove VAT (price / 1.12), then apply 20% to the VAT-exclusive amount. Record ID number, name and signature/acknowledgement per transaction. Confirm item eligibility rules with the client.
6. **Invoices:** under the Ease of Paying Taxes (EOPT) Act the Sales Invoice is the primary document for sales of goods and services; Official Receipts are supplementary. Each invoice has a unique sequential serial number per series/branch, date, seller registered name, TIN with branch code, address, VAT status text, buyer details where required, itemized lines, tax breakdown, and the accreditation/PTU details the BIR requires for system-generated invoices.
7. **Numbering:** gapless, sequential, never reused. Void instead of delete; a void keeps the number with status and reason (audit trail).
8. **POS readings:** X-reading (shift/cashier, no reset) and Z-reading (end of day, resets daily totals) with an accumulated grand total that never resets. Keep e-journal/audit logs.
9. **E-invoicing (EIS):** if covered, design an outbound queue (same pattern as rule-04 outbox) to transmit invoices with retries and an acknowledgement status per invoice.
10. **Reports:** daily sales summary, VAT summary, senior/PWD discount report, void report, and per-branch totals; exportable to Excel/PDF.
11. **Formatting:** `₱1,234.56` (`Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' })`), dates `MMM D, YYYY`, Asia/Manila timezone stored as UTC.
12. **Payroll basics (HRIS):** SSS, PhilHealth, Pag-IBIG contribution tables and withholding tax tables change yearly; store them as dated tables, never constants.

## Before you finish, check

- [ ] All rates/tables come from config with an effective date.
- [ ] Totals and VAT breakdown are computed server-side and shown on the invoice.
- [ ] Senior/PWD flow records ID and applies VAT exemption + 20% correctly.
- [ ] Invoice numbers are gapless; voids keep numbers with reason.
- [ ] I flagged anything that needs the client's accountant to confirm.
