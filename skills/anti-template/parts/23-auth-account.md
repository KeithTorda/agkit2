---
part: 23
title: Auth and Account
covers: sign in, register, forgot and reset password, 2FA and OTP, email verification, social login, profile, account settings, account deletion, sessions and devices, onboarding flows, invite flows, billing pages
---

# 23 — Auth and Account

Read when: building sign in, sign up, password reset, OTP/2FA, email verification, profile, account settings, sessions, invites, onboarding or billing screens.

Field-level rules (labels, input types, autocomplete, password fields) are in part 17. Button labels and toast wording are in part 03. Backend auth code is in part 32. This part covers how auth and account screens are laid out and how the flows behave.

## 23.1 Sign-in page layout

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Split-screen: illustration or gradient on one half, form on the other | Default AI auth template | Simple centered form, 360–400px wide, on the page background |
| Gradient or animated background (aurora, mesh, moving blobs, particles) | Visual trope; costs battery on phones | Solid page background token |
| Glass card over a photo | Glassmorphism, poor contrast | Plain form on the page surface; a card with 1px border is optional |
| Form card with 24px radius and 2xl shadow | Toy look | Radius and shadow tokens from DESIGN.md, or no card |
| Giant logo (120px+) above the form | Wasted space, pushes form down on phones | Logo at normal header size (24–40px tall) |
| "Welcome back! We missed you 👋" heading | Chatty. See part 03 | "Sign in" |
| Subtext "Sign in to continue your journey" | Filler | None, or the product name if the logo does not say it |
| Testimonial quote beside the sign-in form | Marketing on a utility page | Remove |
| Feature list or carousel beside the form | Selling to users who already signed up | Remove |
| Terms paragraph in 11px gray text under the Sign in button | Unreadable legal filler | Terms and privacy links in the footer; on sign up, one line with links |
| Header nav with 6 marketing links above the sign-in form | Distraction, extra tab stops | Logo linking home; no nav, or a single "Back to site" link |
| Sign-in form hidden in a modal on the landing page | No URL, password managers struggle | Dedicated `/login` page |
| Dark mode only for auth pages | Inconsistent with the app | Same theme as the app |
| Social proof ("Join 10,000+ users") on the sign-in page | Existing users do not need it | Remove |

## 23.2 Sign-in form behaviour

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Separate "Username" field when the app uses email | Unclear what to type | Label what the app accepts: "Email", "Email or mobile number", "LRN", "Employee ID" |
| Placeholder-only fields ("Enter your email") | No label once typing starts | Visible label above each field. See part 17 |
| Email field `type="text"` with no autocomplete | Password managers fail | `type="email" autocomplete="username"`; password `autocomplete="current-password"` |
| Eye icon toggle with no label | Unclear, hard to hit | "Show password" checkbox, or an icon button with `aria-label="Show password"` and 44x44 target |
| Tiny gray "Forgot password?" link | Hard to find when needed | Normal-size link near the password field |
| "Don't have an account? Sign up" styled as a big secondary button or gradient link | Over-styled | Plain text link under the form |
| "Remember me" checkbox that does nothing | Fake control | Implement it (longer session) or remove it |
| Error "Invalid credentials" in a toast that disappears | User misses it | Inline error above the form, persistent until the next attempt |
| Error says "Email not found" / "Wrong password" separately | Leaks which accounts exist | "Email or password is incorrect." For admin systems keep this rule strictly |
| Password field cleared but email also cleared after a failed attempt | Retyping everything | Keep the email, clear only the password |
| Sign in button disabled until both fields are filled | Users do not know why it is disabled | Always enabled; show errors on submit |
| No loading state on submit; double posts | Duplicate requests | Disable the button while pending, keep the label: "Signing in…" |
| No lockout message after many attempts | Silent failures or unlimited guessing | Rate limit on the server; show "Too many attempts. Try again in 15 minutes." |
| CAPTCHA on a site with 10 users | Friction with no threat | Add CAPTCHA only when there is abuse; prefer server rate limits first |
| Auto-focus on the email field on mobile opening the keyboard over the logo | Jumpy on small screens | Auto-focus on desktop only, or not at all |
| Sign-in redirects to the dashboard home, losing the page the user wanted | Deep links break | Redirect back to the original URL (validated as same-origin) |

```html
<!-- Banned -->
<div class="grid grid-cols-2 min-h-screen">
  <div class="bg-gradient-to-br from-indigo-600 to-purple-700 p-12 text-white">
    <h2>Welcome back! 👋</h2><p>"This app changed my life." — Sarah J.</p>
  </div>
  <form class="backdrop-blur-xl bg-white/10 rounded-3xl p-10 shadow-2xl">
    <input placeholder="Enter your email">
    <input type="password" placeholder="••••••••">
    <a class="text-xs text-gray-400">Forgot password?</a>
    <button class="bg-gradient-to-r from-purple-500 to-pink-500">Sign In ✨</button>
  </form>
</div>

<!-- Use -->
<main class="auth">
  <img src="/logo.svg" alt="Santos Hardware" height="32">
  <h1>Sign in</h1>
  <form method="post" action="/login">
    <label for="email">Email</label>
    <input id="email" name="email" type="email" autocomplete="username" required>
    <label for="password">Password</label>
    <input id="password" name="password" type="password" autocomplete="current-password" required>
    <label><input type="checkbox" id="show-pw"> Show password</label>
    <button type="submit">Sign in</button>
    <p><a href="/forgot-password">Forgot password?</a></p>
  </form>
</main>
```

## 23.3 Social and alternative sign-in

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Google, GitHub, Apple, Facebook, X, Microsoft buttons with none implemented | Template filler; buttons lead nowhere | Show only providers that are wired up and tested |
| "Or continue with" divider when there is only one method | Divider with nothing on one side | Skip the divider |
| GitHub sign-in on a barangay, school or store app | Wrong audience | Providers the users have: Google for schools on Google Workspace; Facebook only if the client asks; email/mobile otherwise |
| Social buttons in brand colors all at full weight, above the email form | Pushes the main method down | One consistent outline style with each provider's official logo; order by what users actually use |
| Custom-drawn provider logos | Violates brand guidelines, looks off | Official logo assets at the provider's required sizes |
| Magic link as the only option for users on shared devices or without email | Many PH users rely on mobile numbers | Offer mobile number + OTP, or password, where the audience needs it |
| Passkey button with no explanation and no fallback | Users do not know what it is | "Sign in with a passkey" plus password or OTP fallback |
| Social sign-in creates duplicate accounts for the same email | Data split | Link by verified email; ask to connect when an account already exists |

## 23.4 Registration

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Join our amazing community! 🚀" heading | Hype. See part 03 | "Create account" |
| "Start your journey today" subtext | Filler | None, or one line that states what the account gives: "Required to request barangay certificates online" |
| Register form asking for 12 fields up front (birthday, gender, company size, role, how did you hear) | Survey before value | Only what is needed to create the account; collect the rest when a feature needs it |
| Confirm email field | Users paste the same value | Remove; verify by email or show the email back on the next screen |
| Confirm password field plus eye icon | Redundant | One password field with "Show password" |
| Password rules shown only after an error | Trial and error | State the rule under the field before typing: "At least 8 characters" |
| Password strength meter that blocks submit on "weak" with no rule | Arbitrary gate | State the minimum; check against breached/common passwords on the server; meter optional and never the only guide |
| Composition rules (1 uppercase, 1 symbol, 1 number) | Outdated, leads to weak patterns | Length minimum (8+, or 12+ for admin accounts), no forced mix, allow paste and spaces |
| Terms checkbox that must be ticked | Friction unless legally required | Line "By creating an account you agree to the Terms and Privacy Policy" with links; checkbox only where law or the client requires it |
| Data Privacy consent missing on PH apps collecting personal data | Data Privacy Act of 2012 notice expected | Short privacy notice with purpose, link to full policy, and consent capture where processing needs it |
| Username availability checked only on submit | Late error | Inline check after typing stops (debounced), for usernames only |
| Green checkmarks on every valid field | Visual noise | Validate on submit; inline only for availability checks |
| Registration wizard for 4 fields | Steps for nothing | Single form; wizard only for 10+ fields that group naturally |
| Split-screen with illustration on register | Same trope as sign in | Centered form |
| After register: "Welcome aboard! We're thrilled to have you! 🎉" full page | Celebration page | Sign the user in and land on the first useful screen with a short notice: "Account created." |
| Mobile number field with no country handling | PH numbers typed many ways | Accept 09XX, +639XX, 9XX; normalize to E.164 (+63) on save; show format hint "0917 123 4567" |
| Birthday date picker scrolling from the current year | Slow to reach 1980 | Three fields (day, month, year) or a text input with format "DD/MM/YYYY" stated |

## 23.5 Email verification

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Verification wall before the user can see anything | Blocks value; many users abandon | Let users in; require verification before actions that need it (posting, payment, receiving official documents) |
| "Check your inbox! 📬" page with no email shown and no resend | Dead end if the email is wrong | Show the address, a Resend button with cooldown, and "Wrong email? Change it" |
| Resend button with no cooldown | Spam and rate limits | 60s cooldown with visible countdown |
| Verification link that expires in 10 minutes | Email delivery can be slow | 24h for email links; 5–10 min for OTP codes |
| Clicking an old link shows a generic error | User stuck | "This link has expired. Send a new one." with a button |
| Verification link that signs the user in on any device | Security risk on shared links | Verify the email; sign-in only if the same browser session started it |
| Unverified banner shown on every page in red | Alarm for a routine step | One neutral banner with Resend, dismissible for the session |

## 23.6 Forgot and reset password

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Forgot your password? No worries! 😊" heading | Chatty | "Reset password" |
| Message reveals whether the email exists | Account enumeration | "If an account exists for that email, we sent a reset link." Same message either way |
| Reset link valid forever or reusable | Security gap | Single-use, expires in 30–60 minutes, invalidated when the password changes |
| Reset page asks for the old password | User forgot it | New password and nothing else |
| After reset, user must sign in again with no prefilled email | Extra steps | Sign the user in, or land on sign in with the email prefilled; notify by email that the password changed |
| Reset does not end other sessions | Attacker keeps access | Offer "Sign out of other devices" checked by default |
| Reset by SMS OTP with no rate limit | SMS cost and abuse | Rate limit per number and per IP; cooldown on resend |
| Security questions ("Your first pet?") | Outdated and guessable | Email or SMS reset; admin-assisted reset for staff accounts with an audit record |
| Staff/teacher accounts with self-reset to personal email | Account takeover risk | Admin-initiated reset for org-managed accounts |

## 23.7 OTP and two-factor

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Six separate single-digit boxes that break paste and autofill | Fancy but broken | One input: `inputmode="numeric" autocomplete="one-time-code" pattern="[0-9]*" maxlength="6"`; if boxes are used, paste must fill all |
| OTP auto-submits and shows an error before the user finishes typing | Premature | Auto-submit only when all digits are entered; allow correcting |
| "Enter the code we sent you" with no destination shown | User does not know where to look | "Enter the 6-digit code sent to 0917 *** 4567" |
| No resend timer; resend spammable | Cost, SMS provider blocks | "Resend code in 60s", then Resend; cap attempts per hour |
| OTP expiry not stated | Users type stale codes | "Code expires in 5 minutes." |
| SMS OTP as the only 2FA for admin accounts | SIM swap risk | Authenticator app (TOTP) or passkey for admins; SMS as a fallback |
| 2FA setup with a QR code only | Cannot scan on the same phone | Show the setup key as text with a copy button next to the QR |
| No recovery codes after enabling 2FA | Lockout when the phone is lost | Generate 8–10 recovery codes; require the user to download or copy them before finishing |
| "Trust this device for 30 days" default on for shared computers (school labs, barangay hall) | Others sign in as the user | Default off; label clearly "Only on your own device" |
| SMS text like "Your OTP is 123456 🔐 Don't share it with anyone! 😊" | Emoji and chatty. See part 08 | "123456 is your Santos POS code. Expires in 5 min. Do not share it." |

## 23.8 Profile

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Avatar crop modal with zoom slider and rotate | Heavy for a small photo | Simple file input; crop to square on the server; preview after upload |
| Cover photo banner on a work tool profile | Social-network template | Skip unless profiles are public and core to the product |
| Profile completion bar "Your profile is 60% complete!" | Nag with made-up percent | Skip; ask for missing info when a feature needs it |
| Activity heatmap (GitHub style) | Decoration | Skip |
| Bio, website, social links, location on an internal staff profile | Social template fields | Only fields the org uses: name, position, office/department, contact number |
| Profile page with tabs for 2 sections | Tab bloat | One page with headings |
| Name split into First/Middle/Last with no suffix field for PH users | Loses "Jr.", "III" and multiple given names | First name(s), middle name (optional), last name, suffix (optional); allow spaces and "ñ" |
| Changing email saves instantly | Lockout on typos | Send a confirmation to the new address; keep the old email until confirmed; notify the old address |
| "Looking good! Your profile is updated ✨" | Chatty. See part 03 | "Profile saved." |
| Username change allowed with no redirect from the old URL | Broken links | Redirect old profile URLs, or disallow changes |

## 23.9 Account settings

Org-level settings are in part 22. This section is the signed-in user's own settings.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Settings split into 6 tabs (General, Security, Notifications, Appearance, Privacy, Billing) with 2 fields each | Tab bloat | One page with headed sections; separate pages only for Billing and large sections |
| Toggles for every preference | Toggle overuse | Checkboxes saved with a Save button; toggles only where the change applies instantly |
| Notification settings matrix (email/push/SMS x 20 event types) | Unusable | Group events into 3–5 categories; SMS only where the app actually sends SMS |
| 10 themes and accent pickers | Showcase feature | Light, dark, system. See part 34 |
| Language setting missing on bilingual apps | Users stuck in one language | English / Filipino switch if the UI is translated; do not offer untranslated languages |
| Password change form without current password | Hijacked session can lock out the owner | Current password, new password; end other sessions option |
| Red "Danger Zone" box with a thick red border | GitHub copy | "Delete account" at the bottom of the page with a plain heading and clear confirm |
| Timezone setting on a PH-only app | Not needed | Default Asia/Manila; show timezone only if users are elsewhere |

## 23.10 Sessions and devices

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| No list of active sessions | User cannot remove a lost device | "Signed-in devices": device/browser, approximate location, last active, "This device" marker, Sign out per row, "Sign out of all other devices" |
| Session list showing raw user-agent strings | Unreadable | "Chrome on Android · Quezon City · Active 2h ago" |
| Session expiry with no warning, losing form input | Data loss on long government forms | Warn 2 minutes before expiry with "Stay signed in"; save drafts; after expiry, sign in and return to the same page with input kept |
| "Session expired! 😢 Please log in again" | Chatty. See part 04 | "You were signed out after 30 minutes of inactivity. Sign in to continue." |
| Very short sessions on consumer apps; very long ones on admin/POS | Wrong trade-off | Admin: shorter idle timeout (15–30 min) plus re-auth for sensitive actions; consumer: longer with remember-me |
| Shared POS terminal where each cashier stays signed in | Sales attributed to the wrong person | Quick cashier switch with PIN; shift tied to the cashier |
| Logout confirm "Leaving so soon? 😢" | Guilt copy | Sign out directly. Confirm only if unsynced offline data exists |
| Logout that only clears the client token | Server session stays valid | Invalidate on the server |

## 23.11 Account deletion and data export

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| No way to delete the account | Required by app stores and expected under the Data Privacy Act | "Delete account" in settings; for org-managed accounts, "Ask your admin to remove your account" |
| Delete account buried in a support email only | Dark pattern | Self-serve delete with clear confirm |
| Confirm that says only "Are you sure?" | No consequences stated | List what is deleted and what is kept by law: "Your posts and profile will be deleted. Official receipts are kept for 10 years as required by BIR." (Adjust to the client's actual retention rule) |
| Type "DELETE" to confirm | Tests typing | Re-enter password, or type the account email |
| "We're sad to see you go 😢" exit survey required | Guilt and friction | Optional one-question reason; not required |
| Immediate irreversible delete | Accidents happen | Grace period (e.g., 14–30 days) with a cancel link sent by email, then permanent delete |
| No data export before delete | User loses records | "Download my data" producing a ZIP or CSV of their records |

## 23.12 Onboarding flows

First-run empty states and onboarding wording are in part 04.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| 4-step welcome carousel with illustrations after sign up | Delays first use | Land on the first useful screen with a clear primary action |
| Product tour with spotlight overlays on every nav item | Covers the UI; users skip | Clear labels; one short hint where a step is not obvious |
| "Tell us about yourself" survey (role, team size, goals) with no effect on the product | Data collection theater | Ask only questions that change what the user sees next |
| Checklist widget "Get started: 2 of 7 done" with confetti on completion | Gamified template | Skip, or a short setup list for real required setup (business details, OR series, first product), without confetti |
| Setup wizard that cannot be skipped or resumed | Lock-in | Save progress; allow skip where the app still works |
| Sample data loaded silently into a real account | Mixes fake and real records | Offer "Load sample data" explicitly, tagged, with "Remove sample data" |
| Onboarding emails with emoji and "Day 1 of your journey" | See part 08 | Plain transactional emails with one action each |
| Required org setup for PH businesses skipped | App cannot issue receipts later | Collect registered business name, TIN, address and VAT status before the first sale |

## 23.13 Invite flows

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Invite form with 5 empty email rows | Template | One field that accepts multiple emails or mobile numbers separated by commas or new lines; role selector |
| Role defaults to Admin | Unsafe | Default to the least-privileged role |
| Invite link never expires | Stale access | Expire in 7 days; allow resend and revoke from a "Pending invites" list |
| Invitee must create an account with a different email than invited | Mismatch, lost invite | Prefill and lock the invited email, or allow change with admin approval |
| Invite email "You've been invited to join an amazing team! 🎉" | Hype. See part 08 | "Ana Reyes invited you to Santos Hardware POS as Cashier. Accept invite (expires 30 Sep)." |
| No record of who invited whom | Audit gap | Log inviter, invitee, role, time, accept time |
| Bulk staff import by CSV with no preview | Bad data | Upload, preview errors per row, then send invites |

## 23.14 Billing pages

Pricing page copy is in parts 05 and 24. This section is the billing area inside the app.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Billing page with plan comparison cards, glowing "Most popular" badge | Marketing template inside the app | Current plan, price, next billing date, payment method, invoices; "Change plan" link to comparison |
| Prices in USD for PH customers | Wrong currency | ₱ with VAT stated: "₱999.00/month, VAT inclusive" (or exclusive, stated) |
| Only card payment | Many PH customers do not use cards | GCash, Maya, bank transfer, over-the-counter where the payment provider supports them |
| Invoices without BIR-required details for business customers | Cannot be used for expense claims | Official receipt or invoice with registered name, TIN, address, invoice number, VAT breakdown |
| Invoice list with only "Download" icons | Unclear | Table: invoice number, date, amount, status (Paid, Due, Overdue), Download PDF |
| Cancel subscription hidden behind chat or email | Dark pattern | "Cancel plan" in billing, with end date stated: "Your plan stays active until 31 Oct 2026." |
| Downgrade confirm with guilt copy and 3 retention offers | Friction | One confirm with what changes; one optional offer at most |
| Failed payment shown only by email | User unaware in the app | Persistent banner in the app with "Update payment method" until resolved |
| Usage meters for limits the plan does not have | Invented metrics | Show only real limits: "Branches: 2 of 3" |
| Free trial countdown banner on every page in red | Pressure | One neutral line in the header or billing page: "Trial ends 30 Sep" |

## 23.15 Stack-specific tells

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| shadcn "authentication" example (split screen, quote by "Sofia Davis", "Acme Inc") copied | Demo left in | Centered form with the client's name; grep for "Acme Inc", "Sofia Davis" |
| Clerk/Auth0/Firebase UI prebuilt widgets with default theme and all providers enabled | Recognizable default | Theme with DESIGN.md tokens; enable only used providers |
| Tailwind `min-h-screen flex items-center justify-center bg-gradient-to-br` wrapper | Template wrapper | `min-h-dvh` centered layout on the page background token |
| Laravel Breeze/Jetstream default auth views with "Laravel" logo and gray card | Scaffold left unchanged | Replace logo, copy and colors; remove unused views (teams, API tokens) if not used |
| Bootstrap `.form-floating` on every auth field | Floating labels. See part 17 | Static labels above fields |
| NextAuth default sign-in page (`/api/auth/signin`) shipped to users | Unstyled framework page | Custom `/login` page |
| Supabase/Firebase error codes shown raw ("auth/invalid-credential", "AuthApiError: Invalid login credentials") | Developer text in UI | Map codes to plain messages |
| JWT in `localStorage` with no refresh handling | Common generated shortcut | HttpOnly secure cookies for web sessions. See part 32 |

## 23.16 Philippines context

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Email required for every user in a barangay or school parent portal | Many residents and parents use mobile numbers, not email | Mobile number + OTP as a primary option; email optional |
| Phone field that rejects "0917 123 4567" formats | Real input rejected | Accept spaces, dashes, 09 and +63 forms; normalize on save |
| OTP via SMS with no note about delays | SMS can take 1–2 minutes on some networks | "Codes can take up to 2 minutes." plus resend after 60s |
| Student sign-in by email when students have no email | Blocks learners | LRN or school-issued ID plus password; guardian accounts linked |
| Government ID upload on sign up for low-risk services | Over-collection | Ask for IDs only when the service legally needs verification; state why and how long it is kept |
| Privacy notice copied from a US template (CCPA, GDPR only) | Wrong law | Reference the Data Privacy Act of 2012 (RA 10173) and name the Data Protection Officer contact |
| Taglish error messages mixed with English on the same form | Inconsistent. See part 09 | One language per UI, or a full switch |

## 23.17 Check
- [ ] Auth pages are a centered form on a solid background. No split screen, gradient, blur, testimonial or feature list.
- [ ] Headings are "Sign in", "Create account", "Reset password". No welcome copy or journey subtext.
- [ ] Sign in is a page with a URL, not a modal.
- [ ] Every field has a visible label, correct `type` and `autocomplete`.
- [ ] Show password is a labelled checkbox or labelled icon button.
- [ ] "Forgot password?" is a normal-size link near the password field.
- [ ] Sign-up link is plain text, not a big button.
- [ ] Only implemented social providers appear. No "Or continue with" for a single method.
- [ ] Sign-in errors are inline, persistent, and do not reveal whether the account exists.
- [ ] Submit buttons are always enabled, show a pending state, and block double submit.
- [ ] Rate limiting and lockout messages exist; CAPTCHA only when there is abuse.
- [ ] After sign in, users return to the page they asked for.
- [ ] Registration asks only for what the account needs. No confirm email; no confirm password when show-password exists.
- [ ] Password rule is stated up front; length-based; paste allowed; breached passwords checked.
- [ ] Terms checkbox only where required; Data Privacy Act notice where personal data is collected.
- [ ] Email verification does not block the whole app; shows address, resend with cooldown, and change email.
- [ ] Reset links are single-use and expire in 30–60 minutes; reset message is the same whether or not the email exists.
- [ ] Password reset offers to sign out other devices and sends a notification email.
- [ ] OTP uses one numeric input with `autocomplete="one-time-code"`, shows destination and expiry, and has a resend timer.
- [ ] Admin 2FA uses TOTP or passkeys, with recovery codes; SMS is fallback only.
- [ ] "Trust this device" is off by default.
- [ ] Profile has no completion bar, cover photo, heatmap or unused social fields.
- [ ] PH name fields allow suffix, multiple given names and "ñ".
- [ ] Email change requires confirmation from the new address.
- [ ] Settings are one page with headings; toggles only for instant changes; themes limited to light/dark/system.
- [ ] Active sessions list with sign out per device; logout invalidates the server session.
- [ ] Session expiry warns first and keeps form input.
- [ ] Account deletion is self-serve, states what is deleted and kept, has a grace period and a data export.
- [ ] Onboarding lands on a useful screen; no carousel, tour or confetti; sample data only on request.
- [ ] Invites default to the least role, expire, can be revoked, and are logged.
- [ ] Billing shows current plan, ₱ price with VAT basis, next date, invoices with BIR details, and a visible Cancel.
- [ ] Local payment methods (GCash, Maya, bank transfer) offered where the provider supports them.
- [ ] Mobile number + OTP is available where users lack email; phone input accepts 09XX and +63.
- [ ] Framework and demo auth pages (Acme Inc, NextAuth default, Laravel logo) are replaced.
- [ ] Raw auth error codes never reach the UI.
