---
part: 17
title: Forms and Inputs
covers: labels, floating labels, placeholders, validation timing, error display, required markers, wizards, disabled submit, selects, checkboxes, radios, toggles, date pickers, file upload, search inputs, password fields, OTP, phone fields, address fields, autocomplete, input types, inputmode, long government forms, multi-column forms, save and cancel placement
---

# 17 — Forms and Inputs

Read when: building any form, input, filter field, sign-up, checkout, registration, survey, settings page or government/school application form.

Wording of labels, helper text and error messages lives in part 03. Auth-specific screens live in part 23. This part owns structure, behaviour and markup of the fields.

## 17.1 Form shape and length

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Wizard (stepper) for 4 fields | Template reaches for a stepper to look "guided" | Single form. Use a wizard only for 10+ fields that split into real groups a user can finish separately |
| Stepper with 5 circles, gradient connecting line and checkmark animation | Decoration copied from UI kits | Plain text "Step 2 of 4: Address" above the form, plus the step list as text links if steps can be revisited |
| Accordion form: each section collapsed behind a chevron | Hides fields, user cannot see what is left | Flat form with `<fieldset>` and `<legend>` or h2 headings per group |
| Form in a modal with 6+ fields | Modal scroll traps, lost data on backdrop click | Dedicated page for more than 3 fields. Modal only for 1 to 3 fields. See part 21 |
| Tabs splitting one form (Personal / Contact / Other) with one Save at the bottom | User saves without seeing errors on hidden tabs | One page with headings. If tabs are required, show an error count on each tab label |
| Every form wrapped in a card with shadow and 32px radius, centered on a gradient | Landing-page styling on a utility screen | Form on the page surface, left-aligned in the content column, max-width 640px for single-column forms |
| Decorative icon or illustration above a short form | Filler | Page heading (h1) naming the task: "Add product", "Register voter", "Request barangay clearance" |
| Intro paragraph that repeats the heading ("Fill out the form below to create your account") | Says nothing | Delete it. Keep an intro only when it states a fact the user needs: fees, documents to prepare, time needed |
| Every optional field the schema has, shown by default | Model dumps the DB columns into the form | Ask for what the task needs now. Move the rest to a later edit screen |
| Same field asked twice (email + confirm email) | Boilerplate from old templates | One email field. Verify by sending a link or code. Keep "confirm" only for a new password when there is no show-password option |
| Success page with a big check icon and confetti after a simple save | Celebration for a routine action | Inline message near the Save button or a toast "Saved." Redirect to the saved record for create forms |

## 17.2 Labels

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Placeholder used as the label | Disappears on typing, fails contrast, not read reliably by screen readers | Visible `<label for>` above the input. Placeholder optional, for format examples only |
| Floating labels (label slides up inside the input on focus) | Material/UI-kit default; small text, animation, cramped | Static label above the field, 4 to 8px gap, same weight on every field |
| Label to the left of the input on mobile | Squeezes inputs to 150px | Label above input on all widths. Left labels only on wide desktop settings pages, right-aligned text, fixed label column |
| Label text in ALL CAPS with 0.1em letter spacing | Styling trend, harder to read | Sentence case. See part 13 for label typography |
| Label wrapped in a `<div>` with no `for`/`id` link | Clicking the label does not focus the input | `<label for="tin">TIN</label><input id="tin">` or wrap the input inside the label |
| `aria-label` on an input that already has a visible label | Duplicated or conflicting names | Visible `<label>` only. Use `aria-label` only for inputs with no visible text, such as a table-row search |
| Icon in place of a label (envelope icon = email) | Guessing game, not announced | Text label. Icon optional and decorative (`aria-hidden="true"`) |
| Labels with a trailing colon on some fields and not others | Inconsistent generation | No colons on stacked labels. Pick one rule for the whole app |
| Label that is a question ("What's your email?") | Chatty tone | Noun: "Email". Questions only for yes/no fields where a noun reads badly |
| Helper text placed under the error, or placeholder used as helper text | Helper disappears, order changes on error | Order: label, helper text, input, error. Link helper and error with `aria-describedby` |

```html
<!-- Banned -->
<div class="relative">
  <input id="email" placeholder=" " class="peer ...">
  <label class="absolute top-2 peer-focus:-top-3 peer-focus:text-xs ...">Email address</label>
</div>

<!-- Use -->
<label for="email">Email</label>
<p id="email-hint" class="field-hint">We send the receipt here.</p>
<input id="email" name="email" type="email" autocomplete="email" aria-describedby="email-hint">
```

## 17.3 Placeholders

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Placeholder that repeats the label ("Enter your email") | Adds nothing | Empty placeholder, or a format example: `juan@example.com` |
| Placeholder with fake person name "John Doe" in a PH app | Foreign default | Leave empty. If an example is needed: "Dela Cruz" in a surname field, or nothing |
| Placeholder carrying rules ("Must be 8+ characters with a symbol") | Rules vanish when typing starts | Put rules in helper text above the input |
| Placeholder text at light gray `#9ca3af` on white | Fails 4.5:1 | Placeholder color from DESIGN.md token that meets 4.5:1, or no placeholder |
| Placeholder in an input that already has a value-like look, so users think it is filled | Common in AI forms with dark placeholder text | Placeholder visibly lighter than entered text, still at 4.5:1; or remove it |
| `placeholder="Search anything..."` | Vague | Name the thing searched: "Search products", "Search by name or LRN". See part 03 |

## 17.4 Required and optional markers

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Red asterisk with no legend | Users are expected to guess | "* Required" note once at the top of the form, or "(optional)" on optional fields |
| Asterisk on every field when all are required | Noise | If all fields are required, say "All fields are required." once and drop the asterisks |
| Both asterisks on required and "(optional)" on optional | Double marking | Mark the minority. Most fields required: mark "(optional)". Most optional: mark "*" |
| Required status shown only by color (red label) | Fails color-only rule | Asterisk or text, plus `required` attribute on the input |
| `required` attribute missing while UI shows an asterisk | Visual and semantic mismatch | Add `required` (or `aria-required="true"` when using custom validation with `novalidate`) |
| Asterisk inside the placeholder | Vanishes on typing | Asterisk in the label text |

## 17.5 Validation timing

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Green checkmark on every valid field | Visual noise, false confidence | Validate on submit. Show a success mark only for checks that hit the server: username or email availability |
| Error shown on first keystroke ("Invalid email" after typing "j") | Punishes the user mid-typing | Validate a field on blur, then re-validate on input only after it has shown an error |
| Validation only on the client | Bypassed by any request | Same rules on the server. Client checks are a convenience. See part 32 |
| Red border on all empty required fields on page load | Shouts before the user did anything | No error styling until first submit or blur |
| Submit clears the whole form on server error | User retypes everything | Keep every value. Re-render with errors next to fields |
| Password fields cleared on any validation error | Common framework default | Keep other fields. Clearing the password is acceptable only after a failed sign-in |
| Regex that rejects valid input (`+` in email, `ñ` in names, apostrophes in "O'Neil", hyphenated surnames) | Copied pattern | Loose client check; let the server decide. Allow Unicode letters, spaces, `'`, `-`, `.` in names |
| Name fields limited to 20 characters | Arbitrary | 100+ characters for names. Filipino full names with multiple middle names are long |
| Email check that demands a TLD from a fixed list | Blocks `.ph`, `.gov.ph`, `.edu.ph` | `type="email"` plus server-side check. Never hard-code TLDs |

## 17.6 Error display

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Single toast "Please fix the errors" and no inline messages | User hunts for the problem | Inline message under each field, plus an error summary at the top listing each error as a link to its field |
| Focus stays on the Submit button after a failed submit | Keyboard and screen reader users lose context | Move focus to the error summary (`tabindex="-1"`) or to the first invalid field |
| Error shown in a tooltip on hover | Hidden on touch and keyboard | Visible text under the field |
| Error text in red only, no icon, no text change | Color-only | Red token plus an error icon or "Error:" prefix hidden visually; link with `aria-describedby`; set `aria-invalid="true"` |
| Shake animation on the field | Motion that says nothing | Static error text. No shake |
| Errors that clear the moment focus leaves the field, before fixing | Flicker | Clear the error when the value becomes valid |
| Generic "Invalid input" on every field | Model did not map rules | Name the rule: "Enter an 11-digit mobile number starting with 09". Wording rules in part 03 |
| Server error codes shown raw ("ERR_VALIDATION_422") | Leaks internals | Map to field errors. Show a request ID only in a details line for support |
| `alert()` popups for validation | Browser default, blocks the page | Inline errors |

```html
<!-- Use: error summary after submit -->
<div class="error-summary" role="alert" tabindex="-1" id="error-summary">
  <h2>2 problems with this form</h2>
  <ul>
    <li><a href="#mobile">Mobile number must be 11 digits</a></li>
    <li><a href="#birthdate">Enter your birth date</a></li>
  </ul>
</div>
```

## 17.7 Submit button behaviour

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Submit disabled until the form is valid | User cannot learn what is wrong; disabled buttons often fail contrast | Keep Submit enabled. On click, validate and show errors |
| Submit label "Submit" on every form | Generic | The action: "Create account", "Save product", "Send request", "Register". See part 03 |
| Double submit possible (no guard) | Duplicate records, double charges | Disable only while the request is in flight, show a spinner or "Saving..." in the button, re-enable on response. See part 18 |
| Enter key does nothing because the button is outside the `<form>` or is a `<div>` | Built from divs | Real `<form>` with `<button type="submit">` inside, or `form="id"` attribute |
| Every button inside a form defaults to `type="submit"` (e.g. "Show password", "Add row") | Missing `type="button"` | `type="button"` on every non-submit button inside a form |
| Full-width gradient submit button on a desktop form | Landing-page style | Button sized to its label, left-aligned with the fields. Full width only below 480px |
| Two submit buttons of equal weight ("Save" and "Save & New" both primary) | Hierarchy lost | One primary. Secondary style for the alternate. See part 18 |

## 17.8 Save and cancel placement

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Cancel styled as a red button | Cancel is not destructive | Cancel as secondary or text link |
| Cancel on the right, Save on the left on one screen and swapped on another | Random order | One order app-wide. Common: primary first (left) in left-aligned forms; primary last (right) in dialogs. Write the choice in DESIGN.md |
| Save button only at the top of a long form | User scrolls back up | Save at the bottom. For forms over two screens, add a sticky footer bar with Save and Cancel |
| Sticky save bar on a 3-field form | Chrome for nothing | Plain buttons after the last field |
| Cancel that discards 20 fields of input without asking | Data loss | If the form is dirty, confirm "Discard changes?" before leaving. Also handle `beforeunload` for long forms |
| "Reset" button next to Submit | Accidental wipe, rarely needed | Remove Reset |
| Auto-save plus a Save button with no status | User unsure what is stored | Pick one. For auto-save, show "Saved 10:42" text near the heading and no Save button |

## 17.9 Layout of fields

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Two-column form for unrelated fields | Eye zigzags, tab order confuses | Single column. Pair fields only when they belong together: first/last name, city/ZIP, start/end date |
| Two columns kept on mobile | Inputs 140px wide | One column under 640px |
| All inputs full width, including ZIP code and age | Width tells nothing about expected length | Width matches expected length: ZIP 6ch to 8ch, age 4ch, mobile 14ch, name 20 to 30ch |
| 48px gap between every field | Section-padding habit | 16 to 24px between fields, 32 to 48px between groups |
| Inputs 56px tall with 16px radius | Toy look on data forms | 36 to 44px height, radius from DESIGN.md (commonly 4 to 6px). See part 11 |
| Icon inside every input (user icon in name, envelope in email) | Decoration | No icons in inputs, except search (magnifier) and password visibility |
| Label column right-aligned on some rows, left on others | Inconsistent | One alignment for the whole form |
| Tab order that jumps (DOM order differs from visual order via grid tricks) | CSS `order` or absolute positioning | DOM order equals visual order |

## 17.10 Input types, inputmode and autocomplete

Use the correct `type`, `inputmode` and `autocomplete` on every field. Wrong values break autofill, mobile keyboards and password managers.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `type="text"` for email | Wrong keyboard, no autofill | `type="email" autocomplete="email"` |
| `type="number"` for phone, TIN, LRN, ZIP, OTP, account numbers | Strips leading zero, shows spinners, allows `e` | `type="text" inputmode="numeric"` (or `type="tel"` for phone) with a `pattern` |
| `type="number"` for money with spinner arrows | Scroll wheel changes the amount | `type="text" inputmode="decimal"`, format on blur. See 17.17 |
| Missing `autocomplete` on name, address, phone | Autofill fails | `autocomplete="given-name"`, `family-name`, `tel`, `street-address`, `address-level2`, `postal-code`, `bday` |
| `autocomplete="off"` on every field | Copied "security" habit; browsers ignore it for passwords anyway | Remove. Use `autocomplete="one-time-code"` for OTP, `new-password` on sign-up and reset, `current-password` on sign-in |
| Random `name` attributes (`input1`, `field_3`) | Autofill and server mapping fail | Meaningful names that match the backend: `mobile`, `birth_date`, `barangay` |
| No `maxlength` on fixed-length codes | Users paste extra characters | `maxlength` matching the real rule (OTP 6, mobile 11 for 09XX format) |
| `spellcheck` on for codes and usernames | Red squiggles under TINs | `spellcheck="false" autocapitalize="off"` on usernames, codes, emails |
| Font size under 16px on mobile inputs | iOS zooms the page on focus | 16px minimum input text on mobile. See part 15 |

| Field | type | inputmode | autocomplete |
|---|---|---|---|
| Email | email | (default) | email |
| Mobile (PH) | tel | tel | tel-national or tel |
| OTP | text | numeric | one-time-code |
| Amount (₱) | text | decimal | off (transaction-amount only for payment) |
| Quantity | number (no spinner styling needed if steppers wanted) or text | numeric | off |
| TIN / LRN / student ID | text | numeric | off |
| Postal code | text | numeric | postal-code |
| Birth date | date or 3 text fields | numeric (for text) | bday, bday-day, bday-month, bday-year |
| URL | url | url | url |
| Search | search | search | off |
| New password | password | (default) | new-password |
| Current password | password | (default) | current-password |

## 17.11 Select, combobox and multi-select

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Custom div-based dropdown for a 5-option list | Breaks keyboard, mobile pickers, screen readers | Native `<select>`. Style the closed state only |
| Native select replaced to add a chevron icon | Extra JS for a visual | `appearance: none` on the `<select>` plus a background-image chevron |
| Dropdown for 2 or 3 options | Hides choices | Radio buttons |
| Dropdown of 81 provinces or 42,000 barangays with no search | Endless scroll | Searchable combobox (ARIA combobox pattern or a tested library). Cascade: Region, Province, City/Municipality, Barangay |
| Cascading selects that do not reset children when the parent changes | Invalid combos saved (Barangay from another city) | Clear and reload child options when a parent changes. Disable the child until the parent has a value, with text "Choose a city first" |
| First option "Select..." that is selectable and submitted as a value | Empty string saved | `<option value="" disabled selected>Choose a province</option>` plus `required` |
| Multi-select using Ctrl+click native `<select multiple>` | Nobody knows the gesture | Checkbox list for up to about 10 options; tag-style combobox for more |
| Chip-style multi-select where the remove "x" is a 12px target | Too small | Remove button at least 24x24px with `aria-label="Remove Cebu"` |
| Options sorted randomly or by DB id | Unfindable | Alphabetical, or by frequency when data supports it. Keep "Other" last |
| Country dropdown defaulting to United States | Template default | Default to Philippines for PH clients, or detect and let the user change |

## 17.12 Checkboxes, radios and toggles

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Custom checkbox built from a `<div>` with a click handler | No keyboard, no form value | Keep the native `<input type="checkbox">`; style with `appearance: none` and pseudo-elements, or `accent-color: var(--color-primary)` |
| Native input hidden with `display: none` then a fake box drawn | Removes it from keyboard and accessibility tree | Visually hide with a clip pattern, never `display: none`, if a custom box is needed |
| Toggle switch for a single yes/no inside a form that has a Save button | A toggle implies instant effect | Checkbox inside forms. Toggle only in settings where the change applies immediately |
| Toggle with no visible state text | Unclear which side is on | Label the setting; the switch shows on/off by position plus fill; add `role="switch"` and `aria-checked` if custom |
| Toggle that saves instantly but gives no feedback | User unsure it stuck | Brief "Saved" text next to it, or revert with an error message on failure |
| Checkbox label text not clickable | Tiny 16px target | Wrap text in the `<label>`; whole row clickable; 24px minimum target, 44px on touch |
| Radio group without `<fieldset>` and `<legend>` | Question not announced | `<fieldset><legend>Sex</legend>...</fieldset>` |
| Radio group with no default where a sensible default exists | Extra click | Preselect the common option unless choosing is legally or ethically meaningful (sex, civil status, consent) |
| "I agree" checkbox pre-checked | Invalid consent | Unchecked by default for consent. Required only if legally needed. See part 23 |
| Large "card" radios with icons and descriptions for simple choices | UI-kit showcase | Plain radios. Card radios only when each option needs a price or 2-line description (plans, delivery methods) |
| Checkbox list of 30 items in one column | Scroll fatigue | 2 or 3 columns on desktop for short labels, grouped under headings |

## 17.13 Date and time inputs

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Calendar picker for birth dates | 30+ clicks back to 1985 | Three text fields (Day, Month, Year) or `type="date"` with typing allowed. Picker optional |
| Ambiguous format `03/04/2025` with no hint | PH users read DD/MM or MM/DD depending on context | Show the format in helper text ("MM/DD/YYYY"), or use a month dropdown with names. Store ISO 8601 |
| Custom JS date picker with no keyboard support | Heavy and inaccessible | Native `type="date"` first. Library only for ranges, with keyboard support checked |
| Date range as two unrelated pickers where end can precede start | No constraint | Set `min` on the end date from the start value; validate on server |
| Time input in 24h in a consumer app for PH users | Mismatch with local habit | 12h with AM/PM for public-facing apps; 24h acceptable in internal ops tools. Pick one per app |
| Timezone never stated in a scheduling form | Wrong times for OFW users | Show "Philippine time (UTC+8)" next to time inputs |
| Future dates allowed in birth date | Missing `max` | `max` set to today; server check |

## 17.14 File upload

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Huge dashed drop zone with cloud icon and "Drag & drop your files here or browse" for a single ID photo | Oversized, drag is rare on mobile | Native `<input type="file">` styled, or a compact button "Choose file". Drop zone only for bulk upload |
| No stated limits | Upload fails at the end | Helper text: "JPG or PNG, up to 5 MB." Set `accept="image/jpeg,image/png"` |
| Upload progress shown as an indeterminate spinner for a 20 MB file | No sense of time | Progress bar with percent for files over about 1 MB |
| File name hidden after selecting | User unsure what is attached | Show file name, size and a Remove button |
| Upload fails silently when over size | No feedback | Check size before upload; show the limit in the error |
| Camera capture not offered on mobile for ID/selfie uploads | Missed use | `capture="environment"` or `capture="user"` where a photo is expected |
| Avatar crop modal with zoom slider for a profile photo | Heavy for little value | Simple file input; crop server-side to a square. See part 23 |
| Preview thumbnails with hover-only delete | Hidden on touch | Visible Remove button on each file |

## 17.15 Search inputs

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Search input with no label | Placeholder carries the meaning | Visible label, or `aria-label` when inside a toolbar; `role="search"` on the containing form |
| Search fires on every keystroke with no debounce | Hammering the API | Debounce 250 to 400ms, or search on Enter for expensive queries |
| Clear "x" button that is a 12px icon | Hard to hit | 24px minimum target, `aria-label="Clear search"` |
| Pill-shaped search with glow on focus | Visual trope | Radius from DESIGN.md; focus ring from `:focus-visible` token |
| Cmd+K hint badge in the input on a site with no command palette | Copied from docs sites | Show a shortcut hint only when the shortcut exists. See part 16 |
| Results replace the page with no count or query echo | User loses context | "12 results for 'bigas'" above results. Keep the query in the input and URL (`?q=`) |

## 17.16 Password fields

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Eye icon with no label | Unclear purpose, not announced | "Show password" checkbox, or an icon button with `aria-label="Show password"` and `aria-pressed` |
| Strength meter that blocks submit with vague levels ("Weak", "Medium") | Gamified and arbitrary | State the minimum in helper text: "At least 8 characters." Block only when the stated rule fails |
| Composition rules (1 uppercase, 1 symbol, 1 number) | Outdated practice | Length minimum (8 to 12+), check against a breached-password list server-side |
| `maxlength="16"` on passwords | Breaks passphrases and managers | Allow at least 64 characters |
| Paste disabled on password or confirm fields | Breaks password managers | Allow paste |
| Confirm password field when show-password exists | Redundant | One field with a show option |
| Caps Lock warning missing on sign-in | Silent failures | Show "Caps Lock is on" text when detected |

## 17.17 Money, quantity and number fields

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Amount input with "$" prefix in a PH app | Template default | "₱" prefix as a visually separate element outside the input text, or in the label "Amount (₱)" |
| Amount formatted with commas while typing, cursor jumps | Fragile formatting | Accept raw digits while typing; format `1,250.00` on blur; strip commas on submit |
| Amount stored as float | Rounding errors | Store centavos as integers or a decimal type. See part 32 |
| Quantity stepper with tiny +/- buttons (20px) | Hard on touch, esp. in POS | 44px buttons on touch, typed entry allowed |
| Negative values accepted in price or qty | Missing `min` | `min="0"` and server check |
| Percentage field without "%" and unclear 0.12 vs 12 | Ambiguous | Suffix "%" and accept 12 meaning 12% |

## 17.18 Philippine phone, ID and address fields

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| US phone mask `(555) 123-4567` | Foreign template | Accept `09XX XXX XXXX` or `+63 9XX XXX XXXX`; normalise to E.164 `+639XXXXXXXXX` on the server |
| Country code dropdown with 240 flags for a PH-only service | Heavy | Fixed "+63" prefix shown outside the input; dropdown only when foreign numbers are expected (OFW contacts) |
| Phone field rejecting spaces or dashes | Users type them | Strip spaces and dashes before validating |
| Landline and mobile forced into one pattern | Landlines have area codes | Separate "Mobile" and "Landline (optional)" fields when both matter |
| US address layout (Address line 1, line 2, State, ZIP) | Wrong model | House/Unit no. and Street, Barangay, City/Municipality, Province, ZIP code. Add Purok/Sitio for rural LGU forms |
| Free-text barangay field in an LGU system | Spelling variants break reports | Select from the PSGC list, cascaded from the city/municipality |
| "State" label | US term | "Province" |
| ZIP required with 5 digits | PH ZIP is 4 digits | `pattern="\d{4}"`, optional unless mail delivery needs it |
| ID fields with no format hint (TIN, PhilSys, SSS, PhilHealth, LRN) | Users guess dashes | Helper text with the format: "TIN: 000-000-000-000". Accept with or without dashes |
| Name split as First / Last only | Misses middle name and suffix, which PH forms require | First name, Middle name (optional), Last name, Suffix (Jr., Sr., III) as a short select or text field |
| Mandatory "Middle name" with no "no middle name" option | Excludes some users | Optional, or a "No middle name" checkbox |
| Gender as a free-text field or 7-option list on a government form that legally needs sex at birth | Mismatch with legal requirement | Use the field and options the form's legal basis requires; label it exactly ("Sex") |

## 17.19 OTP and verification code inputs

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Six separate boxes, one digit each | Breaks paste, autofill and screen readers in many builds | One input, `inputmode="numeric" autocomplete="one-time-code" maxlength="6"`, letter-spacing for looks |
| If six boxes are kept: paste only fills the first box | Common bug | Handle paste across all boxes and Backspace moving back; test on Android SMS autofill |
| Auto-submit on the 6th digit with no way to fix | Surprise submit | Auto-submit is fine if errors return focus to the input with the value selected |
| "Resend code" available instantly, spammable | SMS cost, rate limits | Countdown text "Resend in 30s", then a link. Limit resends server-side |
| No hint where the code went | User checks the wrong channel | "Code sent to 0917 *** 4567." with a "Change number" link |

## 17.20 Long government and school forms

Barangay clearance, voter registration, enrolment, scholarship and permit forms. These are long, legal, and often filled on low-end phones.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Whole paper form dumped into one 80-field page with no groups | Unusable on mobile | Group into fieldsets that mirror the paper sections (Personal info, Address, Household, Declaration). Steps only if sections are long |
| Stepper that loses data on back or refresh | No persistence | Save each step server-side or in `sessionStorage`; allow Back without losing input |
| No "Review your answers" step before a legal submission | Errors go into official records | Summary page with Edit links per section before final submit |
| No reference number after submit | Citizen cannot follow up | Show and email/SMS a reference number, the office, and what to bring. Printable page |
| Required documents listed only after the form | User stops midway | List documents, fees and processing time before the form starts |
| Deep formal Tagalog labels or machine-translated labels | Nobody speaks that register | Plain English or plain Filipino matching the agency's paper form; bilingual labels rules in part 09 |
| Fake "Official Form" seals and signature images | Impersonation risk | Only use seals the client supplied and is authorised to use. See part 09 |
| Session timeout at 15 minutes with no warning on a 40-field form | Lost work | Warn 2 minutes before expiry with "Stay signed in"; keep drafts |
| Declaration checkbox with 400 words of legal text inside the label | Unreadable | Short label ("I certify the information is true") with the full text in a visible block above |
| Signature pad required on a web form | Hard on desktop, legally unclear | Typed name plus date as signature, unless the client's legal basis requires a drawn or wet signature |
| PDF-only download to fill by hand, labelled as "online application" | Misleading | Either build the web form or label it "Download form (PDF)" |

## 17.21 Stack-specific tells

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Tailwind `rounded-2xl shadow-xl p-10 bg-white/80 backdrop-blur` form wrapper | Glass card trope | Form on page surface; `rounded` from config tokens; no backdrop blur |
| Tailwind `focus:ring-4 focus:ring-purple-500/50` | Default purple glow | `focus-visible:outline` using the primary token from config |
| `peer-placeholder-shown` floating label trick | Floating label trope | Static label |
| Bootstrap `.form-floating` everywhere | Same trope | `.form-label` above `.form-control` |
| Bootstrap `.was-validated` applied on page load | Everything red or green at once | Add after first submit |
| shadcn `<Form>` with every field wrapped in `FormItem/FormLabel/FormControl/FormDescription/FormMessage` even when no description | Boilerplate left in | Remove unused `FormDescription`; keep labels and messages |
| React controlled inputs re-rendering the whole form on each keystroke (state lifted to page) | Laggy on low-end Android | Uncontrolled inputs with `FormData`, or a form library that isolates field state. See part 31 |
| `onChange` validation with a zod schema on every keystroke | Error on first character | Validate on blur and submit |
| `<form onSubmit>` without `e.preventDefault()` in SPA, or `<div onClick>` as submit | Page reloads or no Enter support | Real form with submit handler |

## 17.22 Check
- [ ] Every input has a visible `<label>` linked by `for`/`id`; no floating labels.
- [ ] Placeholders are empty or show a format example; none repeats the label.
- [ ] Required marking uses one convention with a legend; `required` attribute matches.
- [ ] No validation errors show before first blur or submit.
- [ ] No green checkmarks except server-checked availability.
- [ ] After failed submit, an error summary lists each error as a link and receives focus.
- [ ] Each invalid field has inline text, `aria-invalid="true"` and `aria-describedby`.
- [ ] Submit is enabled before validation; disabled only while the request is in flight.
- [ ] Every non-submit button inside a form has `type="button"`.
- [ ] Button labels name the action, not "Submit".
- [ ] Save/Cancel order is the same across the app; Cancel is not red.
- [ ] Dirty long forms ask before discarding.
- [ ] Single-column layout; paired fields only when related; one column under 640px.
- [ ] Input widths match expected length.
- [ ] Correct `type`, `inputmode` and `autocomplete` on every field; no `type="number"` for IDs, phones or money.
- [ ] Mobile inputs use 16px text or larger.
- [ ] Native `<select>` for short lists; radios for 2 to 3 options; searchable combobox for long lists.
- [ ] Cascading address selects reset children when the parent changes.
- [ ] Checkboxes and radios are native inputs with clickable labels; radio groups use `<fieldset>`/`<legend>`.
- [ ] Toggles only where the change applies immediately.
- [ ] Consent checkboxes are unchecked by default.
- [ ] Birth date does not require a calendar picker; date format is stated.
- [ ] File inputs state type and size limits and show the chosen file name.
- [ ] Password fields allow paste, 64+ characters, and have a labelled show option.
- [ ] OTP is one input with `autocomplete="one-time-code"` or boxes that handle paste.
- [ ] Phone accepts 09XX and +63 formats and normalises on the server.
- [ ] Address uses Barangay, City/Municipality, Province, 4-digit ZIP.
- [ ] Names allow Unicode letters, `ñ`, apostrophes, hyphens; middle name and suffix supported.
- [ ] Money inputs use ₱, `inputmode="decimal"`, and are stored as integers or decimals.
- [ ] Long government forms have groups, draft saving, a review step and a reference number.
- [ ] Documents, fees and processing time are listed before the form starts.
- [ ] Server validates every rule the client checks.
- [ ] Values survive a failed submit.
- [ ] Wizards appear only for 10+ fields in real groups.
- [ ] Forms with more than 3 fields are not in a modal.
- [ ] No success page with confetti for a routine save.
