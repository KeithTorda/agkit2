# 07 — Auth, Printable Invoices, POS, Inbox & System Pages (14 Screen Types)

---

## 1. Authentication & Session Screens (5 Types)

All auth screens use a clean centered `AuthCard` (`max-w-[420px]`, `--ui-surface`, `--ui-border`, brand mark at top, plain labels, zero marketing fluff):
1. **`SignInScreen`:** Email/username + `PasswordFieldWithToggle` + `Remember me` + `Forgot password?` link + locked `Sign In` submit button + generic safe auth error (`"Invalid email or password."`).
2. **`RegisterScreen`:** Full name, email, password + strength/match hint, terms checkbox, `Create Account` button.
3. **`ForgotAndResetPasswordScreen`:** Email input returning neutral confirmation (`"If an account exists, a reset link was sent."`) + token-verified new password screen.
4. **`SessionLockScreen`:** Current user avatar/name + password unlock input + `"Sign in with a different account"` link.
5. **`OtpVerificationScreen`:** 6-digit `inputmode="numeric"` `tabular-nums` code input with paste support and resend cooldown timer.

---

## 2. Printable Invoices, POS & E-Commerce Screens (5 Types)

6. **`PrintableInvoiceAndStatement` (`@media print` Ready):**
   - Top bar (`no-print`): `Back` button + `Print Statement` (`window.print()`) button.
   - Sheet body: Organization/Brand header + Official Seal/Logo slot, Statement/Invoice `#` & UTC/Local Date (`tabular-nums`), `From` & `To` blocks, itemized table (`Description`, `Platform/Ref`, `Views/Qty`, `Rate`, `Amount`), right-aligned `Subtotal`, `VAT/Deductions` (if applicable), bold `Total Amount (₱)`, `StatusBadge` (`Paid` / `Pending` / `Voided`), and signature/verification footer.
   - `@media print`: Hides sidebar, header, settings drawer, and `.no-print` buttons; forces pure `#ffffff` paper background and `#000000` ink with zero box shadows.
7. **`ProductCatalogGrid`:** Responsive `1 → 2 → 3 → 4` column card grid with locked image `aspect-ratio`, title, stock `StatusBadge`, bold `₱` price (`tabular-nums`), and `Add` CTA.
8. **`ProductListRowView`:** Horizontal media row variant for dense wholesale/supply inventory browsing.
9. **`ProductDetailView`:** Left image/media preview + Right variant pills, stock count, quantity stepper, and `Add to Cart` / `Edit Stock` actions.
10. **`TwoColumnCheckoutAndPos`:** Left customer/delivery/payment form + Right sticky cart line-items, server-verified promo/tax breakdown, and transactional `Place Order` button.

---

## 3. Profile, Inbox, Calendar & HTTP Error Screens (4 Types)

11. **`UserProfileAndSettings`:** Compact cover/header card (avatar upload with MIME/size check, name, role badge) + tabbed `Account Details`, `Change Password`, and `Activity Log`.
12. **`SplitInboxAndTicketThread`:** Folder/status filter rail + paginated message list + thread reader with safe attachment download & reply form.
13. **`ScheduleCalendarScreen`:** Month/Week/Day grid with category badges and modal event creation/editing.
14. **`HttpErrorAndMaintenanceScreens` (`400`, `403`, `404`, `500`, `503`):** Crisp status code (`tabular-nums`), plain human explanation (`"Page not found."`, `"You do not have access to this page."`, `"Something went wrong on our end."`), and a single `Back to Dashboard` button — never raw stack traces.
