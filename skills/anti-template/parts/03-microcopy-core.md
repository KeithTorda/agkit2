---
part: 03
title: Core Microcopy
covers: button labels, CTA labels, verb consistency, link text, form labels, placeholders, helper text, validation errors, success toasts, error toasts, info and warning messages, confirm dialogs, destructive actions, loading text, sign-in and sign-up headings, consent prompts, sentence case, UI punctuation, payment microcopy
---

# 03 — Core Microcopy

Read when: writing any button, link, label, placeholder, helper text, error, toast, dialog or loading string in an app, form, dashboard, POS or portal.

## 03.1 Rules for every UI string

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Exclamation marks in system text: "Saved!" | Model cheerfulness | "Saved." No "!" in any system string. |
| Emoji in toasts, buttons, labels: "🎉 Done" | Chat-output voice | No emoji. Icon from the icon set if the design needs one. |
| Cheerleading: "Awesome!", "Great job!", "You're all set!" | Performed emotion | State what happened: "Order placed." |
| Interjections: "Oops!", "Uh oh!", "Whoops!", "Hmm", "Yay!" | Cute filler | Delete; start with what failed |
| "Please" on every string | Padding that hides the action | Use "please" only when asking the user to wait or do something inconvenient: "Please wait while the file uploads." Max once per screen. |
| "Successfully" in success messages: "Successfully saved" | Redundant | "Saved." |
| "Your" on every noun: "Your profile has been updated successfully" | Padding | "Profile saved." |
| Passive "has been": "The item has been deleted" | Wordy | "Item deleted." |
| Blaming the user: "You entered an invalid email" | Accusing | "Enter an email like name@example.com." |
| Humour in errors | Irritates a user who is already stuck | Plain cause and fix |
| Different words for the same action on different screens | Inconsistent | One verb per action. See 03.4. |
| Title Case On Buttons And Labels | Model default | Sentence case: "Add product". See 03.17. |
| Mixed "my" and "your": "My orders" in nav, "Your orders" on page | Inconsistent voice | Pick one; default to no pronoun: "Orders" |
| Tech words in user copy: "Null", "undefined", "payload", "token expired", "500" | Leaked internals | Plain words. Status codes only in a small "Error code: 500" line for support. |

## 03.2 Button and CTA labels

Every item from the original banned list, plus in-app additions. Marketing hero CTAs are in part 05.

| AI (banned) | Why it reads as generated | Use |
|---|---|---|
| Get Started / Get Started Today | Says nothing about what happens | The first action: "Create account", "Add first product" |
| Start Free / Start Your Free Trial | Sales label | "Create free account", or "Start 14-day trial" if a trial exists |
| Try Demo / Try it Free | Vague | "Open demo", "View sample dashboard" |
| Learn More | Unclear target | What the link opens: "Enrollment requirements", "Pricing" |
| Explore Features | Banned verb | "View features", or link each feature |
| Unlock Now | Banned verb | "Upgrade to Pro", "Pay ₱499" |
| Discover | Banned verb | "View", "Browse {object}" |
| Dive in | Banned phrase | "Open", "Start" |
| See how it works | Vague | "Watch 2-minute video", "Read setup steps" |
| Book a demo | Fine only if a real booking flow exists | "Book a call" with the calendar, or remove |
| Supercharge your ... | Banned verb | The action |
| Join the revolution | Hype | "Create account" |
| Claim your spot / Reserve your seat | Fake scarcity | "Register", "Reserve seat" only if seats are real and counted |
| Take the first step | Journey metaphor | The first step's name |
| See it in action | Vague | "Watch video", "Open demo" |
| Request access | Fine if access is gated | "Request access" only when approval exists; otherwise "Sign up" |
| Start building / Start creating | Vague | "Create project", "New page" |
| See the magic / See the difference | Hype | Delete, or "Compare plans" |
| Let's go! / Let's do this! | Chummy | "Continue", "Start" |
| Click here | Not a label | The action or destination |
| Submit (on everything) | Generic | The outcome: "Send message", "File complaint", "Register voter". "Submit" is fine on long government forms where the whole form is sent. |
| OK (in a confirm dialog) | Ambiguous | The action: "Delete", "Publish" |
| Yes / No (in a dialog) | Forces reading the question twice | Action verbs: "Delete order" / "Cancel" |
| Proceed | Formal, vague | "Continue", "Pay ₱1,250.00" |
| Go | Vague | "Search", "Apply filter" |
| Do it / Make it happen | Chummy | The action |
| Save changes (when nothing changed) | Misleading | Keep enabled; show "No changes to save." on click, or hide until dirty |
| Next → → with arrows in the text | Decorative characters | "Next"; an arrow icon from the set if needed |
| I'm in! / Count me in! | Chummy | "Join", "Register" |
| No thanks, I don't like saving money | Confirmshaming | "No thanks" |
| Maybe later (on a required step) | Misleading | "Skip" only if the step is optional |

Use the verb the button performs: Save, Post thread, Sign in, Continue, Run, Export, Create account, Delete, Filter, Download, Send message, Upload file, Add row, Submit, Cancel, Close, Back, Next, Done, Print receipt, Pay, Approve, Reject, Assign, Void sale, Refund.

| Rule | Detail |
|---|---|
| Verb first | "Add student", not "Student add" or "New student entry" |
| Verb plus object when the screen has more than one object | "Delete photo", "Delete album" |
| Max 3 words, 4 with a number | "Pay ₱1,250.00", "Export 42 rows" |
| One CTA style for the whole app | Same casing, same verb for the same action, no mixing "Sign in" and "Log in" |
| The button label matches the page title it opens | "Add product" opens "Add product" |
| The confirm button repeats the verb from the question | "Delete 3 orders?" then "Delete orders" |

## 03.3 Stack-specific label tells

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Default component labels left in: shadcn "Continue", Bootstrap modal "Save changes" / "Close" on every dialog | Template copy never edited | Write the label for this dialog |
| `<button>Submit</button>` from a form generator | Default | The outcome verb |
| React Hook Form / Formik default error "This field is required" on every field | Library default | Name the field: "Enter the student's LRN." |
| HTML5 native bubble messages ("Please fill out this field.") mixed with custom messages | Two voices | Use `novalidate` with custom messages, or native only, not both |
| Laravel default "The email field is required." / "The given data was invalid." | Framework default | Custom messages in the language file with field names users know |
| Django "This field is required." everywhere | Framework default | Override per field |
| Toast library default title "Success" / "Error" plus body | Two lines for one fact | One line: "Saved." |
| SweetAlert "Good job!" / "Are you sure?" / "You won't be able to revert this!" | Copy-pasted from the library demo | See 03.12 |
| DataTables "No data available in table", "Showing 0 to 0 of 0 entries" | Plugin default | "No records." See part 04. |

## 03.4 Verb and term consistency

Pick one term per row and use it everywhere: buttons, toasts, titles, emails, docs.

| Pair | Pick | Rule |
|---|---|---|
| Sign in / Log in / Login | Sign in | "Login" is a noun, not a verb. Pair: Sign in / Sign out. |
| Sign up / Register / Create account | Create account (button), Sign up (link) | For voter or student registration, "Register" is the domain word; keep it. |
| Delete / Remove | Delete = gone from the system. Remove = taken out of a list or group, still exists. | "Remove from class" vs "Delete student" |
| Save / Submit / Update / Apply | Save = store edits. Submit = send for review or processing. Apply = take effect now (filters, settings). | Never "Update" as a button label for saving a form |
| Cancel / Close / Dismiss | Cancel = abandon an action. Close = leave a view with nothing pending. Dismiss = hide a message. | A dialog with no pending action has "Close", not "Cancel" |
| Add / Create / New | Add = put an existing thing into a list. Create = make a new record. "New" as a menu heading only. | "Add to cart", "Create invoice" |
| Edit / Modify / Change / Update | Edit | "Change" for a single value: "Change password" |
| Send / Submit / Post | Send = message or email. Post = public content. Submit = form for processing. | |
| Export / Download | Export = generate a file from data. Download = get an existing file. | "Export CSV", "Download receipt" |
| Archive / Deactivate / Disable | Archive = hide but keep. Deactivate = account cannot sign in. Disable = feature off. | |
| Void / Cancel / Refund (POS) | Void = cancel an unpaid or same-day sale. Refund = return money. | Follow the BIR and client's POS terms; do not mix |
| Approve / Accept / Confirm | Approve = someone with authority says yes. Confirm = user checks their own input. | |
| Upload / Attach / Import | Upload = file to storage. Attach = file to a record. Import = data rows from a file. | |
| Search / Find / Filter | Search = free text. Filter = narrow by fields. | |
| Settings / Preferences / Options / Configuration | Settings | One word in the whole app |
| Account / Profile | Account = sign-in, billing, security. Profile = public info. | |
| Dashboard / Home / Overview | One name for the landing screen | |
| User / Member / Customer / Client | The domain word: student, voter, resident, customer | Never "user" in UI copy when a domain word exists |

## 03.5 Link text

| Context | AI (banned) | Use |
|---|---|---|
| Inline link | "Click here to read our policy" | "Read the refund policy" with the link on "refund policy" |
| Card link | "Learn more →" | "View requirements", "Read the ordinance" |
| Article list | "Read more…" on every item | Link the article title; drop "Read more" |
| Download link | "Download here" | "Download form (PDF, 240 KB)" |
| External link | "Check it out!" | "COMELEC precinct finder (opens comelec.gov.ph)" |
| Bare URL in body copy | "https://example.gov.ph/services/clearance?id=12" | "Barangay clearance request" as link text |
| "this link" / "here" / "this page" | Screen readers list links out of context | Descriptive text that makes sense alone |
| Arrow characters in link text: "View →", "» Next" | Decorative characters read aloud | Plain text; arrow icon with `aria-hidden="true"` if needed |
| Same text for different targets: five "View details" links | Ambiguous in a link list | Add context: "View details for Order 1042", or visually hidden text |
| Email link | "Shoot us an email!" | "support@{domain}" as the link text |
| Phone link | "Give us a ring!" | "0917 123 4567" as a `tel:+639171234567` link |
| Social link | "Follow us on socials!" | "Facebook page" |
| File link without type or size | "Download" | Always add type and size for files over 1 MB or non-HTML |

## 03.6 Form labels

Form layout and field behaviour are in part 17. This is the wording only.

| Context | AI (banned) | Use |
|---|---|---|
| Email | "Enter your email address", "Your Email", "E-mail Address*" | "Email" |
| Name | "Your Full Name", "What should we call you?" | "Full name", or split "First name", "Last name". Government forms: "Last name", "First name", "Middle name", "Suffix". |
| Phone | "Phone Number (Required)", "Your digits" | "Mobile number" |
| Password | "Create a strong password to secure your journey" | "Password (8+ characters)" |
| Confirm password | "Re-enter password to confirm" | "Confirm password" |
| Birthday | "When were you born? 🎂" | "Date of birth" |
| Address | "Where do you live?" | Separate fields: "House no. and street", "Barangay", "City or municipality", "Province", "ZIP code" |
| Message | "Tell us what's on your mind…" | "Message" |
| Company | "Company / Organization Name" | "Company" |
| Amount | "How much?" | "Amount (₱)" |
| Quantity | "Qty" in a form label | "Quantity"; "Qty" allowed in table headers |
| Question labels | "What's your name?", "How can we reach you?" | Noun labels. Questions only for survey questions. |
| Colon after labels | "Email:" | No colon when the label is above the field |
| Label repeated in placeholder | Label "Email", placeholder "Email" | Placeholder shows format or is empty |
| Optional fields | Every required field has "*" and no legend | Mark the minority. If most are required, mark optional ones "(optional)". If "*" is used, add "* Required" at the top. |
| Checkbox label | "I agree" with no object | "I agree to the Terms and Privacy notice" with links |
| Toggle label | "Enable awesome notifications" | "Email me when an order is placed" |
| Select default option | "Select…", "Choose one", "-- Please select --" | "Select province", or preselect the common value if safe |
| Yes/No radio label | "Do you want to maybe receive…?" | Direct question: "Are you a registered voter in this barangay?" |
| Government IDs | "ID #" | The real name: "PhilSys Card Number (PCN)", "TIN", "LRN", "Voter's ID number" |

## 03.7 Placeholders

| Context | AI (banned) | Use |
|---|---|---|
| Search | "Search anything…", "What are you looking for?" | What is searched: "Search threads", "Search by name or LRN" |
| Email | "john.doe@awesome.com", "you@example.com ✨" | "name@example.com" |
| Mobile | "Enter your phone number", "(555) 123-4567" | "0917 123 4567" (Philippine format) |
| Name | "John Doe", "Jane Smith" | Empty, or a local example: "Juan dela Cruz" only when a format example helps |
| Date | "Pick a date 📅" | The format: "DD/MM/YYYY" or "MM/DD/YYYY", whichever the form uses. See part 04. |
| Amount | "0.00" in grey that looks filled | Empty, with "₱" as a prefix outside the input |
| Message | "Type something amazing…" | Empty |
| Placeholder as the only label | Disappears on typing | Real `<label>`; placeholder optional |
| Placeholder with instructions | "Must be 8 characters with one number" | Move to helper text below the field |
| Placeholder in low-contrast grey that looks disabled | Unreadable | Placeholder colour meets 4.5:1, or remove it |
| Placeholder with ellipsis on every field | Template habit | No ellipsis, except search fields if the design uses it |

## 03.8 Helper text

| Context | AI (banned) | Use |
|---|---|---|
| Password rules | "Make it strong and unique! 💪" | "8+ characters. Use a mix of letters and numbers." |
| Email usage | "Don't worry, we'll never spam you!" | "We send receipts to this address." |
| Phone usage | "We promise not to call at 3am 😄" | "For the OTP and pickup updates." |
| File upload | "Drag and drop your amazing files here" | "PDF or JPG, up to 5 MB." |
| Username | "Pick something cool!" | "3 to 20 letters, numbers or underscores. Shown on your posts." |
| Tax field | "Enter your TIN if you have one" | "12 digits, from your BIR Form 1902 or 1904. Needed for official receipts." |
| LRN | "Your student ID" | "12-digit Learner Reference Number from DepEd." |
| Reference number | "Enter the ref no." | "13-digit reference number from your GCash or Maya receipt." |
| Helper text that repeats the label | Label "Email", helper "Your email address" | Delete the helper |
| Helper text on every field | Clutter | Only where format, limit or use is not obvious |
| Helper text that changes into the error | Loses the instruction | Keep helper, show error above or below it |
| Character counter on unlimited fields | Noise | Only where a real limit exists: "42/160" |

## 03.9 Validation errors

Format: what is wrong + how to fix it. Name the field. No blame, no "invalid" alone.

| Context | AI (banned) | Use |
|---|---|---|
| Required field | "Hmm, that doesn't look right", "This field is required" | "Enter your email.", "Email is required." |
| Required select | "Please make a selection" | "Select a province." |
| Required checkbox | "You must agree!" | "Accept the terms to continue." |
| Email format | "Invalid email!", "Oops, that's not an email 🤔" | "Enter an email like name@example.com." |
| Mobile format | "Invalid phone number" | "Enter an 11-digit mobile number starting with 09, or +63 then 10 digits." |
| Password too short | "Password too weak! 😬" | "Password must be at least 8 characters." |
| Passwords do not match | "Oops, passwords don't match!" | "Passwords do not match." |
| Wrong password on sign-in | "Invalid credentials" | "Email or password is incorrect." |
| Email taken | "This email is already taken 😕" | "An account with this email exists. Sign in or reset your password." (links) |
| Username taken | "Already taken, try again!" | "That username is taken." |
| Number range | "Invalid value" | "Enter a number from 1 to 100." |
| Amount over balance | "Insufficient funds!" | "Amount is more than the balance of ₱3,420.00." |
| Date in the past | "Invalid date" | "Choose a date from today onward." |
| Date format | "Wrong format" | "Enter the date as DD/MM/YYYY." |
| Age limit | "You're too young!" | "You must be 18 or older on election day to register." |
| File too large | "File too big! 😱" | "File is 8.2 MB. Maximum is 5 MB." |
| File type | "Unsupported file" | "Upload a PDF, JPG or PNG." |
| Too many files | "Limit reached!" | "Upload up to 3 files." |
| Text too long | "Too long!" | "Keep this under 160 characters. You have 184." |
| Duplicate record | "Duplicate entry" | "A student with LRN 123456789012 already exists." (link to record) |
| Stock too low (POS) | "Error: stock" | "Only 4 in stock." |
| Discount code | "Invalid code 😢" | "Code not found or expired." |
| OTP wrong | "Wrong code, try again!" | "Code is incorrect. 2 tries left." |
| OTP expired | "Your code has expired 😢" | "Code expired. Send a new code." (button) |
| Reference number format | "Invalid reference" | "Reference number is 13 digits. Check your GCash receipt." |
| TIN format | "Invalid TIN" | "TIN is 9 or 12 digits, e.g. 123-456-789-000." |
| Server-side error on field | "The given data was invalid." | The specific field message from the server |
| Error summary at top | "There were some problems with your submission" | "Fix 2 fields: Email, Mobile number." with links to each field |
| Validation on every keystroke | Red text while typing | Validate on blur or submit. Timing is in part 17. |
| Error text in red only | Colour-only meaning | Error icon plus text; link `aria-describedby`. See part 27. |

## 03.10 Success messages and toasts

Only show a success toast when the result is not visible on screen, or when the action ran in the background. Toast behaviour is in part 21.

| Context | AI (banned) | Use |
|---|---|---|
| Generic success | "Awesome! You're all set! 🎉" | "Saved." |
| Record created | "🎉 Successfully created!" | "Thread created." |
| Account created | "Welcome aboard! We're thrilled to have you!" | "Account created. You're signed in." |
| Password changed | "Your password has been updated successfully! 🔒" | "Password changed." |
| Profile saved | "Looking good! Your profile is updated ✨" | "Profile saved." |
| File uploaded | "File uploaded successfully! 🎉" | "File uploaded." |
| Item deleted | "Poof! It's gone! 🗑️" | "Deleted." or "Order 1042 deleted. Undo" |
| Copied | "Copied! You're all set ✨" | "Copied." |
| Form submitted | "Thanks for reaching out! We'll be in touch 🤝" | "Submitted." or "Message sent. We reply within 1 working day." |
| Email sent | "Woohoo! Email is on its way! 📧" | "Email sent to ana@example.com." |
| Invite sent | "Your invite is flying! ✈️" | "Invite sent to 3 people." |
| Settings applied | "Your changes are live! 🚀" | "Settings saved." |
| Payment received | "Cha-ching! 💰 Payment successful!" | "Payment received. ₱1,250.00 via GCash, ref 1234567890123." |
| Order placed | "Woohoo! Your order is confirmed! 🛍️" | "Order 1042 placed." |
| Export ready | "Your export is ready to rock! 📊" | "Export ready. Download CSV (42 rows)." |
| Bulk action | "All done! ✅" | "12 students moved to Grade 8 - Rizal." |
| Import finished | "Import complete! 🎉" | "Imported 480 rows. 3 skipped. View skipped rows." |
| Published | "Your post is live! 🎉" | "Published." |
| Sale completed (POS) | "Sale successful! 🎉" | "Sale 000231 complete. Change: ₱50.00" |
| Two-line toast with title "Success!" plus body | Double message | One line |

## 03.11 Error messages and error toasts

Format: what failed + why if known + what to do. Error toasts stay until dismissed. Full error pages are in part 04.

| Context | AI (banned) | Use |
|---|---|---|
| Generic save failure | "Oops! Something went wrong! 😅" | "Could not save. Try again." |
| Server error in a toast | "We're experiencing issues, please bear with us" | "Server error. Retry in a moment." |
| Network error in a toast | "Looks like you're offline! 📡" | "No connection. Changes will save when you're back online." (only if that is true) or "No connection. Could not save." |
| Timeout | "This is taking longer than expected… 🐢" | "Request timed out. Try again." |
| Permission on an action | "Access denied! You don't have superpowers for this" | "You don't have permission to delete orders. Ask an admin." |
| Upload failed | "Upload failed 😢" | "Could not upload receipt.jpg. Check your connection and try again." |
| Payment failed | "Payment failed! Please try again 😬" | "Payment not completed. GCash returned: insufficient balance. No amount was charged." |
| Payment pending | "Hang on, processing your payment ✨" | "Payment pending. We'll update this page when GCash confirms." |
| Duplicate submit | "Whoa, slow down there!" | "Already submitted. Reference: 2026-000481." |
| Conflict / stale data | "Something changed!" | "This record was edited by Maria at 2:14 PM. Reload to see changes." |
| Not found on action | "Couldn't find it 🔍" | "Order 1042 no longer exists. It may have been deleted." |
| Rate limit on action | "Slow down, speedy! 🏎️" | "Too many attempts. Try again in 5 minutes." |
| Printer (POS) | "Printer's being shy 🖨️" | "Printer not responding. Check the cable and paper, then retry." |
| Scanner (POS) | "Scan fail!" | "Barcode not found. Enter the SKU." |
| Unknown error with raw message | "Error: TypeError: Cannot read properties of undefined" | "Could not load orders. Try again." plus "Error ID: 8f3a2c" for support |
| Error with only a code | "Error 422" | Plain message; code on a second, smaller line |
| Error with no next step | "Something went wrong." | Add the action: Retry button, Contact link, or the fix |
| Apologies on every error | "We're so sorry for the inconvenience!" | No apology for user errors. One short "Sorry" only for our fault when it cost the user something. |
| "Please contact the administrator" | No contact given | Name the contact: "Contact the registrar at registrar@{domain}." |

## 03.12 Confirm dialogs

Confirm only destructive, costly or irreversible actions. Dialog behaviour is in part 21.

| Context | AI (banned) | Use |
|---|---|---|
| Delete title | "Are you sure? This can't be undone! 😱" | "Delete this thread? This is permanent." |
| Generic confirm | "You're about to do something awesome!" | "Confirm: publish this draft?" |
| SweetAlert default | "Are you sure?" / "You won't be able to revert this!" / "Yes, delete it!" | "Delete 3 products?" / "This removes them from all branches." / "Delete products" |
| Title as "Confirm" or "Warning" | Says nothing | The question with the object: "Void sale 000231?" |
| Body repeats the title | Padding | Body states the consequence: "Stock is returned and the sale is marked void in the Z-reading." |
| Consequence missing | User cannot judge | Say what is lost, who is affected, whether it can be undone |
| Buttons "Yes" / "No" or "OK" / "Cancel" | Ambiguous | "{Verb} {object}" / "Cancel" |
| Two cancel-like buttons: "Cancel" / "Cancel order" | Confusing | "Keep order" / "Cancel order" |
| Logout confirm | "Leaving so soon? 😢" | "Sign out?" (or no confirm at all) |
| Unsaved changes | "Wait! You have unsaved changes! 😰" | "Discard unsaved changes?" / "Discard" / "Keep editing" |
| Leaving a long form | "Are you sure you want to leave?" | "Leave this page? Your answers are saved as a draft." (only if true) |
| Send to many | "Ready to blast this out? 🚀" | "Send to 1,240 residents?" / "Send SMS" |
| Charge money | "Let's make it rain!" | "Pay ₱1,250.00 with GCash?" / "Pay ₱1,250.00" |
| Confirm on safe actions (mark as read, filter) | Friction | Do it without a dialog |

## 03.13 Destructive actions

| Context | AI (banned) | Use |
|---|---|---|
| Delete account button | "Nuke my account 💣" | "Delete account" |
| Section heading | "⚠️ DANGER ZONE ⚠️" | "Delete account" heading, placed last on the page |
| Type-to-confirm prompt | "Type DELETE to prove you mean it" | "Type the school name to confirm: San Jose National High School" |
| Consequence text | "This will delete everything forever and ever!" | "Deletes 3 years of grades for 412 students. Download a backup first." |
| Soft delete | "Moved to the void" | "Moved to Trash. Items in Trash are deleted after 30 days." |
| Undo after delete | "Oops, undo?" | "Order 1042 deleted. Undo" (8 seconds minimum) |
| Revoke access | "Kick them out!" | "Remove Maria from this branch? She can no longer sign in to it." |
| Void or refund (POS) | "Undo sale" | "Void sale", "Refund ₱350.00". Manager approval text: "Manager PIN required." |
| Cancel a government application | "Cancel request?" | "Withdraw application BC-2026-0481? You will need to apply again and pay the fee again." |
| Button colour and label mismatch | Red "Continue" | Red only on the destructive verb itself: "Delete" |

## 03.14 Loading and progress text

Loading visuals are in part 21. This is the text.

| Context | AI (banned) | Use |
|---|---|---|
| Page loading | "Hang tight! We're preparing something… ✨" | "Loading…" or spinner only |
| Skeleton | "Almost there! Getting things ready…" | Silent skeleton or spinner |
| Rotating fun messages: "Reticulating splines…", "Brewing coffee…" | Joke copy | One plain line, or none |
| Button while saving | "Saving your masterpiece…" | "Saving…" (same button, disabled) |
| Button while paying | "Processing your awesome payment…" | "Processing payment…" plus "Do not close this page." |
| Long job | "Working our magic 🪄" | "Exporting 12,400 rows. About 30 seconds." |
| Upload progress | "Uploading your goodies…" | "Uploading receipt.jpg, 62%" |
| Import progress | "Crunching the numbers…" | "Importing row 1,200 of 4,800" |
| AI or search wait | "Thinking really hard 🤔" | "Searching…" |
| Sending | "Launching your message into space 🚀" | "Sending…" |
| Retry countdown | "Trying again soon!" | "Retrying in 10s. Retry now" |
| Loading text with no ellipsis consistency | "Loading", "Loading...", "Loading…" | One form: "Loading…" |

## 03.15 Sign-in, sign-up and flow headings

Auth page layout is in part 23. This is the heading and short-text wording.

| Context | AI (banned) | Use |
|---|---|---|
| Login heading | "Welcome back, hero!" | "Sign in" |
| Login subtext | "Sign in to continue your journey" | (none) |
| Register heading | "Join our amazing community!" | "Create account" |
| Register subtext | "Start your journey today" | (none) |
| Onboarding button | "Let's get you started on your journey… 🚀" | "Create account" |
| Forgot password heading | "Forgot your password? No worries! 😊" | "Reset password" |
| Forgot password body | "It happens to the best of us!" | "Enter your email. We'll send a reset link." |
| Reset link sent | "Check your inbox! 📬" | "If an account exists for ana@example.com, a reset link was sent. It expires in 30 minutes." |
| Sign-up switch link | "Don't have an account? Join the fun!" | "No account? Create one" |
| Sign-in switch link | "Already one of us? Welcome back!" | "Have an account? Sign in" |
| OTP heading | "Verify it's really you 🔐" | "Enter the 6-digit code" |
| OTP body | "We sent a magic code to your phone!" | "Sent to 0917 *** 4567. Expires in 5 minutes." |
| Resend code | "Didn't get it? Let's try again!" | "Resend code (available in 45s)" |
| Sign out | "Log me out!" | "Sign out" |
| Checkout step heading | "Almost there! 🛒" | "Payment" |
| Wizard step heading | "Step 2: Tell us about yourself! 😊" | "Step 2 of 4: Personal details" |

## 03.16 Consent, cookie and small signup prompts

| Context | AI (banned) | Use |
|---|---|---|
| Cookie banner | "We use cookies to enhance your experience ✨" | "This site uses cookies. [Accept] [Decline]" |
| Cookie banner with only functional cookies | Any banner at all | No banner if no tracking cookies are set |
| Cookie buttons | "Accept all 🍪" / tiny "Manage preferences" | "Accept" / "Decline" at equal size and weight |
| Privacy consent (PH Data Privacy Act) | "We value your privacy! 💖" | "We collect your name and mobile number to process this request. See the Privacy notice." with a checkbox |
| Newsletter signup | "Stay in the loop! Get exclusive updates 📬" | "Email updates" (or skip if nobody asked) |
| Newsletter button | "Sign me up!" | "Subscribe" |
| Newsletter success | "You're in! 🎉 Welcome to the family!" | "Subscribed. Check your email to confirm." |
| Upgrade prompt | "Unlock premium features! ✨" | "Pro — ₱499/mo" or "Export is on the Pro plan. View plans" |
| Notification permission ask | "Never miss a beat! 🔔 Enable notifications?" | "Get a notification when your order is ready?" / "Allow" / "Not now" |
| Location permission ask | "Let us find you! 📍" | "Use your location to find the nearest precinct?" / "Use location" / "Type address" |
| Feedback prompt | "How are we doing? We'd love to hear from you! 💬" | "Rate this form: 1 to 5" or skip |

## 03.17 Capitalisation

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Title Case Buttons: "Create New Account" | Model default | Sentence case: "Create account" |
| Title Case Labels and Menu Items | Same | "Date of birth", "Order history" |
| Title Case Toasts: "Changes Saved Successfully" | Same | "Changes saved." |
| ALL CAPS buttons via text, not CSS: "SUBMIT" | Hard-coded shouting; screen readers may spell it | Sentence-case source text; `text-transform: uppercase` only if the design system uses it for a specific component |
| Capitalised common nouns: "Please enter your Email Address and Password" | Random emphasis | "Enter your email and password." |
| Capitalised feature names that are not brands: "Use the Smart Filter" | Fake brand | "Use the filter" |
| Inconsistent product name: "Phorum", "PHorum", "phorum" | Sloppy | One spelling from the brand guide |
| Proper nouns lowercased: "gcash", "maya", "comelec", "deped" | Wrong | "GCash", "Maya", "COMELEC", "DepEd", "BIR", "PhilHealth", "Pag-IBIG", "SSS" |
| "barangay" capitalised mid-sentence as a common noun | Inconsistent | "the barangay"; "Barangay San Roque" as a name |
| Title Case headings in the app | Inconsistent with sentence-case buttons | Sentence case for all UI headings |

## 03.18 Punctuation in UI

| Element | Rule |
|---|---|
| Buttons | No end punctuation. No "!" ever. |
| Labels | No colon when above the field. No end punctuation. |
| Headings and titles | No end punctuation. Question mark only on confirm dialog titles. |
| Toasts and inline messages | Full sentence: end with a period. Fragment of 1 to 2 words: period is still fine ("Saved."). Be consistent across the app. |
| Helper text | Period if it is a sentence. |
| Tooltips | No period for fragments, period for sentences. |
| Menu items | No end punctuation. Ellipsis only if the item opens a dialog that asks for more input: "Rename…" |
| Error messages | Period at the end. No "!" |
| Lists in UI | No end punctuation on fragments |
| Quotes around user input | Use quotes around search terms and names: No results for "xyz". |
| Numbers in text | Numerals, not words: "3 files", not "three files" |
| Ampersand | Only where space is tight: tab labels, table headers |
| Exclamation marks | None in system text. Allowed only in user-generated content. |

## 03.19 Payment and money microcopy

Currency formatting rules are in part 04. Filipino-language payment copy is in part 09.

| Context | AI (banned) | Use |
|---|---|---|
| Pay button | "Pay Now! 💳", "Complete Purchase" | "Pay ₱1,250.00" |
| E-wallet choice | "Choose your fave e-wallet!" | "Pay with GCash", "Pay with Maya" |
| Bank transfer instructions | "Just send it to our bank 😊" | "Transfer ₱1,250.00 to BPI 1234-5678-90, account name {Business name}. Upload the receipt below." |
| Proof of payment upload | "Show us the money! 📸" | "Upload proof of payment (screenshot or photo, up to 5 MB)" |
| Reference number field | "Ref #" | "Reference number" |
| Cash on delivery | "Pay when it arrives, easy peasy!" | "Cash on delivery. Prepare exact amount: ₱1,250.00." |
| Change due (POS) | "Your change is ready!" | "Change: ₱50.00" |
| Receipt button (POS) | "Print that receipt!" | "Print receipt", "Reprint", "Email receipt" |
| Official receipt wording | "Invoice" and "Receipt" used interchangeably | Use the document type the client's BIR registration specifies ("Sales invoice", "Official receipt"). Do not invent BIR wording. See part 09. |
| Fees shown late | Fee appears only on the last step | Show "Processing fee: ₱15.00" before the Pay button |
| Refund message | "Your money is on its way back! 💸" | "Refund of ₱350.00 sent to GCash 0917 *** 4567. It can take up to 3 banking days." |

## 03.20 Check

- [ ] No "!" in any system string.
- [ ] No emoji in buttons, labels, toasts, dialogs, errors or loading text.
- [ ] No "Oops", "Whoops", "Uh oh", "Hmm", "Awesome", "Yay", "Woohoo".
- [ ] No "successfully" in success messages.
- [ ] Buttons start with a verb and name the object where needed; max 3 words, 4 with a number.
- [ ] None of the banned CTAs in 03.2: Get Started, Learn More, Explore, Discover, Unlock, Dive in, Try it Free.
- [ ] Confirm buttons repeat the verb from the dialog title; no Yes/No or OK/Cancel pairs.
- [ ] One term per action across the app (03.4): Sign in, Delete vs Remove, Save vs Submit, Cancel vs Close.
- [ ] "User" replaced by the domain word (student, voter, resident, customer).
- [ ] No "Click here", "Read more", "Learn more", bare URLs, or repeated identical link text.
- [ ] File links state type and size.
- [ ] Labels are nouns, no colon, no question form, not repeated in placeholders.
- [ ] Placeholders show format only; never the only label.
- [ ] Philippine formats in examples: 0917 123 4567, ₱, local names only where they help.
- [ ] Every validation message names the field and the fix.
- [ ] Framework default messages (Laravel, Django, HTML5, DataTables, SweetAlert) replaced.
- [ ] Success toasts only where the result is not visible; one line, no title.
- [ ] Error messages state what failed and the next step; no raw stack traces or codes alone.
- [ ] Error toasts persist until dismissed.
- [ ] Confirm dialogs only for destructive, costly or irreversible actions; body states the consequence.
- [ ] No "Danger Zone" heading; delete account is last, plain label.
- [ ] Undo available at least 8 seconds after soft delete.
- [ ] Loading text is "Loading…" or specific progress; no joke messages.
- [ ] Sign-in and sign-up headings are "Sign in" and "Create account" with no subtext.
- [ ] Cookie banner only when tracking cookies exist; Accept and Decline equal weight.
- [ ] Sentence case on buttons, labels, headings, toasts, menus.
- [ ] Brand and agency names spelled correctly: GCash, Maya, COMELEC, DepEd, BIR, PhilHealth.
- [ ] Ellipsis only on loading text and commands that open further input.
- [ ] Pay buttons show the exact amount; fees shown before payment.
- [ ] Receipt wording matches the client's BIR registration; nothing invented.
