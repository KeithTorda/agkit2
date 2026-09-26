---
part: 08
title: Email, Social and Meta Text
covers: transactional emails, welcome, verify, password reset, receipts, invoices, newsletters, SMS, push notifications, Facebook posts for LGU and school pages, app store listings, SEO titles, meta descriptions, Open Graph tags, page titles, alt text, image captions, announcement banners, cookie banners, public notices
---

# 08 — Email, Social and Meta Text

Read when: writing any email template, SMS or push text, social media post, app store listing, `<title>`, meta description, OG tag, alt text, caption, site-wide banner, or public notice for a barangay, LGU, school or COMELEC-style page.

In-app notification and toast wording is in part 03 and 04. Filipino language tells are in part 09. Image choice is in part 26. SEO technical setup (robots, sitemap, duplicate titles at scale) is in part 34.

## 08.1 Rules for every message sent outside the app

- The subject line, SMS or push title says what happened or what to do. No greeting in it.
- Sender name is the product or office name, not "Team {Product}" or "The {Product} Family".
- The first line of the body repeats the key fact, because previews show only 40 to 90 characters.
- One action per message. The button or link names that action.
- Include what the reader needs to act without opening the app: amount, date, reference number, deadline.
- No emoji in subject lines, SMS, push titles or official notices.

## 08.2 Email subject lines and preheaders

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Welcome to {Product}! 🎉" | Greeting, emoji, no information | "Your {Product} account is ready" |
| "You're in! Let's get started 🚀" | Hype, "Let's" | "Account created: sign in at {domain}" |
| "Action Required: Please Verify Your Email Address" | Title Case, alarm prefix | "Confirm your email for {Product}" |
| "🔐 Reset your password" | Emoji | "Reset your {Product} password" |
| "Thank you for your purchase!" | No order data | "Receipt for order #1042: ₱1,250.00" |
| "Your invoice is here!" | Exclamation, no amount or date | "Invoice INV-2026-0312: ₱4,990.00, due 15 March 2026" |
| "Important Update Regarding Your Account" | Vague, phishing-like | Name the change: "Your plan changes to Basic on 1 April" |
| "Don't miss out! ⏰" | Pressure, emoji | The fact and date: "Enrollment closes 15 June" |
| "We miss you! Come back 💔" | Guilt, emoji | Send nothing, or "Your saved cart expires on 20 March" if true |
| "Quick question..." / "Following up" | Sales-sequence tells | Direct subject naming the matter |
| "RE:" or "FWD:" on a first message | Deceptive | Never |
| ALL CAPS words in subject | Spam signal | Sentence case |
| Preheader left as "View this email in your browser" | Template default | Preheader = the next key fact: "Paid via GCash on 3 March, 2:14pm" |
| Preheader repeating the subject | Wasted space | Add information: amount, deadline, or who sent it |

## 08.3 Welcome and account emails

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Welcome aboard! We're thrilled to have you!" | Feeling-first, exclamation | "Your account is ready. Sign in at {url} with {email}." |
| "Your journey starts now ✨" | Banned noun, emoji | Omit |
| Three-paragraph company story in the welcome email | Nobody asked | Sign-in link, what to do first (one step), support contact |
| "Here are 5 tips to get the most out of {Product}" | Onboarding padding | One next step, linked. Tips only if a real user needed them |
| "If you have any questions, don't hesitate to reach out! We're always here to help 😊" | Filler, emoji, false availability | "Questions: {email}, Mon–Fri 9am–5pm." |
| Sign-off "Cheers, The {Product} Team 💙" | Faceless team, emoji | Office or person name: "{Name}, {Company} support" |
| Social icon row under every transactional email | Distraction, links to dead pages | Omit from transactional mail |
| Invite email: "{Name} invited you to join their amazing workspace!" | Hype | "{Name} added you to {Workspace} on {Product}. Accept by 10 March: {link}" |
| Account deleted email: "We're sad to see you go 😢" | Guilt, emoji | "Your account and data were deleted on 3 March 2026. This cannot be undone." |
| Role changed email missing who changed it | Security gap | "{Admin name} changed your role to Cashier on 3 March, 4:10pm." |

## 08.4 Verification, OTP and password emails

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Please click the magical button below to verify your email ✨" | Cute, emoji | "Confirm your email: {button: Confirm email}. Link expires in 24 hours." |
| No expiry time stated | Reader does not know urgency | State expiry in hours or minutes |
| No "didn't request this" line | Security gap | "If you did not create this account, ignore this email." |
| OTP buried in paragraph 3 | Hard to find on a phone | OTP in the subject or first line, large, monospace, with expiry |
| OTP split with spaces for style ("1 2 3 4 5 6") | Copy fails | Plain 6 digits; allow copy |
| Password reset: "Forgot your password? No worries, it happens to the best of us! 😅" | Chummy, emoji | "Reset your password: {button: Reset password}. Expires in 60 minutes. If you did not ask for this, ignore this email; your password stays the same." |
| Password changed notice without time or device | Security gap | "Your password was changed on 3 March 2026, 9:42pm (Asia/Manila) from Chrome on Android. Not you? {link: Secure your account}" |
| Plain password sent in email | Security failure | Never; send a reset link |
| "Your security is our top priority" | Boilerplate | Omit; state the specific protection |
| Link text "Click here" | Unclear, poor for screen readers | Name the action: "Reset password" |

## 08.5 Receipts, invoices and payment emails

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Thanks for your order! 🛍️ We're so excited!" | Emoji, feeling | "Order #1042 received. ₱1,250.00 paid via GCash." |
| Missing line items | Receipt without content | Item, quantity, unit price, line total, subtotal, VAT, discount, total |
| Amounts as "$1250" or "PHP 1250" | Wrong or unformatted | "₱1,250.00" with 2 decimals on receipts |
| No payment method or reference | Customer cannot reconcile | "Paid via GCash, ref 1234 567 890123, 3 March 2026 2:14pm" |
| Calling an email "Official Receipt" when it is not a BIR-registered OR | Legal problem | "Order confirmation" or "Acknowledgement receipt" unless the client issues BIR-registered e-receipts; see part 09 |
| Missing seller details | Incomplete for BIR and customer | Registered name, address, TIN, as the client provides |
| Invoice with no due date or no payment instructions | Cannot act | Due date, accepted methods (GCash number, Maya, bank name and account name), what to put in the reference |
| Payment reminder: "Friendly reminder! Your payment is overdue 😬" | Cute, emoji | "Invoice INV-0312 for ₱4,990.00 was due 15 March. Pay at {link} or reply if already paid." |
| Failed payment: "Uh oh! Your payment didn't go through" | Cute | "Payment of ₱499.00 failed: card declined. Update your card by 20 March to keep your plan." |
| Refund email with no amount or timeline | Vague | "Refund of ₱1,250.00 sent to your GCash on 5 March. It can take up to 3 banking days to appear." |
| Order shipped with no tracking | Missing the point | Courier name, tracking number, link, expected date |
| COD order email missing the amount to prepare | Local need | "Prepare ₱1,250.00 cash on delivery." |

## 08.6 Newsletters and announcement emails

Newsletter signup blocks are in part 05. This covers the email itself.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Hey there, friend! 👋" opener | Emoji, fake intimacy | Start with the first item, or use the subscriber's first name once |
| "Hope this email finds you well!" | Email cliche | Omit |
| "We've been busy bees 🐝 working on exciting updates!" | Cute, emoji, no content | List the updates with dates |
| "In this issue:" table of contents for 3 items | Padding | The 3 items |
| Every item ends with "Read more →" | Repeated vague link | Link text names the article |
| Stock image header on every issue | Template | Omit, or a real photo from the event or product |
| "That's all for now! Stay awesome ✌️" | Cute sign-off | Omit, or the name of the sender |
| Unsubscribe link hidden in grey 10px text | Dark pattern | Clear "Unsubscribe" link, normal size, one click |
| No reason given for receiving the email | Spam-like | "You get this because you signed up at {domain} on {date}." |
| School newsletter full of adjectives ("an amazing week of learning") | Hype | Events, dates, results, reminders: "Quarterly exams 10–12 March. Report cards released 20 March." |

## 08.7 SMS text

SMS is paid per 160-character segment (70 with any non-GSM character, including ₱ and emoji). Plan the text to fit one segment where possible.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Hi! 👋 Great news from {Product}! 🎉 Your order is on its way! 🚚" | Emoji forces UCS-2, 70-char segments, costs 2 to 3x | "{Store}: Order #1042 shipped via J&T, tracking 1234567. ETA 5 Mar." |
| No sender identification | Recipient cannot tell who sent it | Start with the sender name or registered sender ID |
| ₱ symbol in cost-sensitive bulk SMS | Non-GSM char, halves segment size | "PHP 1,250" or "P1,250" in SMS only; ₱ everywhere else. Confirm with the client |
| OTP SMS: "Your one-time password is 123456. Please do not share this with anyone for your security!" | Wordy, exclamation | "123456 is your {App} code. Expires in 5 min. Do not share it." |
| OTP not at the start | Phones auto-fill better with code early | Code first |
| Links shortened with random shorteners | Looks like phishing | Client's own domain, short path |
| "Reply STOP to unsubscribe" missing on promotional SMS | Required courtesy and often required by the SMS provider | Include opt-out instructions per the provider's rules |
| Taglish SMS written in deep formal Tagalog | Nobody texts like this, see part 09 | Match how the office texts residents: short Taglish or English |
| Barangay SMS blast: "URGENT!!! PLEASE READ!!!" | Alarm fatigue | "Brgy. San Isidro: Water interruption 5 Mar, 8am–5pm, Purok 1–4. Store water tonight." |
| COMELEC-style voter SMS with no official sender | Phishing risk | Only from the verified sender ID; never ask for PINs, OTPs or payment |

## 08.8 Push notifications

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "You've been mentioned! 🔔" | Emoji, no actor or object | "John replied to your thread 'Stock count'." |
| "Don't forget to check out what's new! ✨" | Engagement bait | Send nothing unless something happened to the user |
| "We miss you!" re-engagement push | Guilt | Omit |
| Title and body saying the same thing | Wasted space | Title: who or what. Body: the detail |
| Push with no deep link | Tapping opens the home screen | Deep link to the exact item |
| Title over ~40 characters | Truncated on lock screens | Short title, detail in body |
| Batched pushes firing one per event (30 pushes for 30 orders) | Spam | Group: "12 new orders since 9am" |
| Late-night marketing pushes | Disrespectful | Quiet hours 9pm–8am Asia/Manila for non-urgent pushes |
| Push for expected, user-initiated actions ("Your settings were saved") | Noise | Only async or background events |

## 08.9 Social posts for LGU, school and small-business pages

Facebook is the main channel for PH barangays, LGUs, schools and small stores. Posts must be readable in the feed without clicking.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "📢📢📢 ATTENTION ALL RESIDENTS!!! 📢📢📢" | Emoji walls, caps, exclamations | "ANUNSYO" or "Announcement" once, then the facts |
| Hashtag walls: #Barangay #Community #Service #Excellence #Serbisyo #Proud | Hashtag padding | 0 to 2 hashtags, only ones the office actually uses (e.g. the LGU's official tag) |
| "We are thrilled to announce..." | Feeling-first | What, when, where, who, requirements |
| Post with the key date only inside an image | Not searchable, not accessible | Date, time, place in the post text too |
| Poster image with 200 words of text | Unreadable on phones | Short image text (title, date, place); details in the caption |
| "Stay tuned for more updates! 🙌" | Filler | Omit; say when the next update is if known |
| "Kindly be guided accordingly." on every post | Stiff office closer | Omit, or state the action: "Bring a valid ID." |
| Machine-translated Tagalog caption beside the English one | Stiff, see part 09 | Write both by hand in the office's usual voice, or use one language |
| Motivational quote posts ("Monday motivation! 💪") | Filler content | Only posts with information for residents, parents or customers |
| Invented officials' quotes ("Our beloved Mayor said...") | Fabrication | Only statements the office provided |
| "Hon." placeholders or "Kap. Juan Dela Cruz" | Placeholder never replaced, see part 09 | Real names from the client, or no names |
| Store post: "🔥🔥 SALE SALE SALE 🔥🔥 Grab yours now before it's gone!!!" | Emoji and pressure | "20% off all rice brands, 5–7 March. Store hours 7am–7pm." |
| "Comment 'INTERESTED' for details" | Engagement bait | Put the details in the post; give a Messenger link for orders |
| School post: "Congratulations to our amazing, brilliant, outstanding students!!!" | Stacked adjectives | Names (with parent permission), award, event, date |

```text
# Banned
📢📢 ATTENTION ALL RESIDENTS!!! 📢📢
We are thrilled to announce our AMAZING Libreng Bakuna Program! 💉✨
Don't miss this incredible opportunity! Stay tuned for more updates! 🙌
#Barangay #Health #Community #Serbisyo #Excellence #Proud

# Use
Libreng bakuna laban sa flu, para sa 60 taong gulang pataas.
Kailan: Sabado, 8 Marso 2026, 8am–12nn
Saan: Barangay Health Center, Purok 3
Dalhin: Senior citizen ID o anumang valid ID
Tanong: Brgy. Health Office, 0917 123 4567
```

## 08.10 App store and marketplace listings

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| App name "{Product}: The Ultimate All-in-One Business Solution" | Keyword stuffing, banned words | "{Product} POS" or "{Product}: Sales and Inventory" |
| Subtitle "Revolutionize the way you work" | Banned verb, vague | What it does in 30 characters: "Sales, stock and receipts" |
| Description opening "Are you tired of...?" | Infomercial question | First line: what it does and for whom |
| Feature bullets with emoji at the start of each line | Emoji list | Plain bullets, each one a capability |
| "Download now and join millions of happy users!" | Invented reach, pressure | Omit |
| "5 stars! Best app ever!" written into the description | Fake review | Omit; reviews come from the store |
| Screenshots with marketing text overlays in 3 fonts and gradients | Template | Real screens with one short caption each, same font |
| "What's New: Bug fixes and performance improvements" every release | Hides changes | Name the user-visible changes: "Receipts now show branch code." |
| Keywords field stuffed with competitor names | Policy risk | Terms real users search: "POS, sari-sari, resibo, inventory" |
| Privacy section contradicting the app | Legal risk | Match data actually collected; link the privacy notice |

## 08.11 Page titles

Format: `{Page name} — {Site name}` or `{Page name} | {Site name}`. One separator style across the site. 50 to 60 characters where possible.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Home — Premium Community Experience" | Hype in the title | "Phorum — Community forum" |
| "Home" as the homepage title | No site identity | "{Site name} — {what it is}": "Barangay San Isidro — Services and announcements" |
| Every page titled "{Site name}" | Identical titles, useless tabs and search results | Unique title per page, page name first |
| "Welcome to {Site}" as the title | Greeting | Site name plus what it offers |
| "Best POS Software Philippines | Top POS System | Cheap POS Manila" | Keyword stuffing | "{Product} — POS for small stores in the Philippines" |
| Title Case With Every Word Capitalised | Template default | Sentence case after the site name, unless the brand guide says otherwise |
| Titles over 70 characters | Truncated in search results | Cut adjectives first |
| Admin pages titled "Dashboard" only | Many tabs look the same | "Sales report — Admin — {Site}" |
| Detail pages with a generic title ("Product details") | Unhelpful | Include the item: "Rice 25kg Dinorado — {Store}" |
| Emoji in the title tag | Spam signal, inconsistent rendering | None |
| LGU page title "Official Website of the Municipality of X - Serving with Excellence" | Hype, see part 09 | "Municipality of X, Province" |

## 08.12 Meta descriptions

A meta description names what the page shows, in 120 to 160 characters. It does not sell.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Explore the latest discussions designed to empower users…" | Banned verbs, vague | "Recent forum threads and replies." |
| "Discover our comprehensive range of innovative solutions tailored to your needs." | Banned words, no content | "Price list and delivery areas for {Store} hardware, Lipa City." |
| Same meta description on every page | Duplicate | Unique per page, generated from page content (title, first paragraph, key facts) |
| Missing meta description on key pages | Search engine picks random text | Write one for home, services, pricing, contact, and templates for detail pages |
| Keyword list as description ("POS, inventory, sales, Philippines, cheap, best") | Stuffing | A sentence |
| Description with exclamation marks and emoji | Hype | Plain sentence |
| "Welcome to our website! We are..." | Greeting | Start with the content |
| Description longer than 160 characters | Truncated | Cut to the facts |
| LGU/school description with slogans | No searchable facts | "Barangay clearance, cedula and business permit requirements, office hours and contact numbers for Barangay San Isidro, Lipa City." |
| Article description repeating the title | No added information | The key fact or answer from the article |

## 08.13 Open Graph and social share tags

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `og:title` "Welcome to {Site}! 🚀" | Emoji, greeting | Same as the page title without the site suffix |
| `og:description` copied marketing hype | Hype in every share | Same rules as the meta description |
| `og:image` missing, so Facebook picks a random logo or icon | Broken share preview | 1200x630 image per key page; for announcements, the poster itself |
| `og:image` a generic stock photo on every page | Template | Page-specific image, or the site's default branded card |
| `og:image` with relative URL | Not fetched by crawlers | Absolute HTTPS URL |
| `og:url` pointing to localhost or staging | Leftover from dev | Canonical production URL |
| `og:locale` missing on Filipino pages | Wrong language hint | `en_PH` or `fil_PH` matching the page |
| Twitter/X card tags on a site with no X presence, filled with placeholders | Boilerplate | Only the tags needed; `twitter:card=summary_large_image` is enough for previews |
| `og:site_name` "My Awesome Site" | Template value | Real site name |
| Share preview never tested | Broken on Facebook, the main PH channel | Check with Facebook Sharing Debugger after deploy |

```html
<!-- Banned -->
<title>Home | Welcome to Our Amazing Website!</title>
<meta name="description" content="Discover innovative solutions designed to empower your community and elevate your experience!">
<meta property="og:image" content="/images/hero-gradient.png">

<!-- Use -->
<title>Barangay San Isidro — Services and announcements</title>
<meta name="description" content="Requirements, fees and office hours for barangay clearance, cedula and business permits. Barangay San Isidro, Lipa City, Batangas.">
<meta property="og:image" content="https://sanisidro-lipa.gov.ph/og/default.jpg">
<meta property="og:locale" content="en_PH">
```

## 08.14 Alt text

Alt text says what the image shows that matters on this page. Decorative images get `alt=""`. Accessibility rules for alt attributes are in part 27; this covers the wording.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `alt="image"`, `alt="photo"`, `alt="picture"`, `alt="img1"` | Placeholder | Describe the content, or `alt=""` if decorative |
| `alt="Image of a beautiful sunset over a vibrant cityscape"` | "Image of" plus adjectives | "Sunset over Manila Bay from Roxas Boulevard" |
| `alt="Happy diverse team collaborating in a modern office"` | Stock-photo description, likely a stock photo, see part 26 | Replace the image with a real one; describe it: "Store staff at the Lipa branch counter" |
| Alt text on decorative blobs, dividers, background shapes | Screen reader noise | `alt=""` or CSS background |
| Alt repeating the adjacent caption or heading | Read twice | `alt=""` when the caption already describes it, or make them differ in purpose |
| Logo alt "logo" | No name | "{Company} logo" in content; in a home link, the alt is "{Company} home" |
| Product image alt "product" | Useless for shoppers | "Dinorado rice, 25kg sack" |
| Chart image alt "chart" | Data lost | Summary of the finding: "Sales rose from ₱120,000 in January to ₱185,000 in March" plus a data table nearby |
| Poster image alt "announcement" | Content lost | Key facts from the poster: event, date, time, place |
| Official portrait alt "Hon. Juan Dela Cruz" placeholder | Fake official | Real name and position: "Punong Barangay Maria Santos" |
| Alt text keyword-stuffed for SEO | Spam | Describe the image |
| Alt over ~150 characters | Too long for most images | Short description; long content in the page text |

## 08.15 Image captions

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "A stunning view of our state-of-the-art facility" | Banned adjectives | "Main building, completed 2019. 24 classrooms, 2 labs." |
| Captions on every image, including decorative ones | Noise | Captions only where they add names, dates, places or credit |
| Caption that describes the image without adding facts | Duplicates what is visible | Who, where, when, credit |
| Missing photo credit on photos from others | Rights issue | "Photo: {Name} / {Source}" |
| Event photos captioned "Fun times! 😄" | Cute, emoji | "Grade 6 recognition day, 28 March 2026, covered court" |
| People captioned without names on a school or LGU site | Missing facts | Names and positions with consent, left to right |

## 08.16 Announcement banners and site-wide bars

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Welcome to {App}! We're so glad you're here 🎉" | Welcome banner | Do not show a welcome banner |
| "🎉 Big news! Check out our amazing new features →" | Emoji, hype, vague link | "Offline mode is available. How it works" (only for a real change, remove after 2 weeks) |
| Banner that never goes away | Stale content | Dismissible, with an end date set in code or CMS |
| Several stacked banners (promo + cookie + update + beta) | Clutter | One banner at a time; priority: legal, outage, then everything else |
| Rotating/marquee banner text | Hard to read, see part 25 | Static text |
| Outage banner: "We're experiencing some hiccups! 😅" | Cute | "Online payments are down since 2:10pm. Pay at the cashier. Updates here." |
| Holiday banner: "Happy Holidays from all of us! 🎄✨" | Filler | Only if it carries hours: "Office closed 24–26 Dec. Online requests resume 27 Dec." |
| LGU banner in a blinking red ticker | Alarm fatigue, motion | Static alert with severity in words: "Typhoon signal no. 2. Classes suspended 5 March, all levels." |
| Banner with no source for emergency info | Trust issue | Cite the source: "Per PAGASA 5am bulletin" and link |

## 08.17 Cookie and consent banners

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "We use cookies to enhance your experience ✨" | Emoji, vague purpose | "This site uses cookies. [Accept] [Decline]" plus a link to the privacy notice |
| Cookie banner on a site that sets no non-essential cookies | Boilerplate | No banner. Only session cookies need no consent prompt; confirm with the client |
| "Accept" large and coloured, "Decline" hidden in grey text | Dark pattern | Both buttons the same size and style |
| "By using this site you agree to everything" | Invalid consent | Real choice with Accept and Decline |
| Consent text citing GDPR on a PH-only site | Wrong law | Data Privacy Act of 2012 (RA 10173) where the client confirms it applies |
| Banner covering half the phone screen | Blocks content | Bottom bar, max ~25% of viewport height on 390px width |
| "We value your privacy" as the heading | Boilerplate | No heading; the sentence and buttons are enough |

## 08.18 Public notices and official announcements

Barangay, LGU, school and COMELEC-style notices are read for facts: what, who, when, where, what to bring, whom to ask. Language rules for Tagalog notices are in part 09.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "The Barangay Council is pleased to inform the public..." | Stiff throat-clearing | Start with the notice: "Water interruption: 5 March, 8am–5pm." |
| "Kindly be informed that..." / "Please be advised that..." | Office filler | State the fact |
| No date of issue on the notice | Readers cannot tell if it is current | "Posted 3 March 2026" and notice number if the office uses one |
| Missing who is affected | Everyone reads it, few need it | "Affected: Purok 1 to 4" or "Grade 7 to 10 students" |
| Requirements written as a paragraph | Hard to scan | Numbered list of documents, with copies needed and where to get each |
| Fees missing or "minimal fee" | Readers need to prepare cash | "₱50, pay at the barangay treasurer, Room 2" |
| Deadline without time or timezone | Ambiguous | "Until 5pm, 15 March 2026" |
| No contact | Dead end | Office, phone (09XX or landline with area code), Facebook page, hours |
| Class suspension notice without level or source | Confusion | "No classes, all levels, public and private, 5 March. Per Memo No. 12, s. 2026, Office of the Mayor." |
| Voter or precinct notice with no official source | Misinformation risk | Cite the issuing office; link to the official source; never invent precinct numbers or schedules |
| Election-period notice with partisan wording or candidate photos on an LGU site | Legal problem during campaign periods | Neutral wording, no candidate names or images; confirm rules with the client |
| "Mabuhay!" / "Maraming salamat po!" closer on every notice | Forced ritual phrasing, see part 09 | End with the contact line |
| Notice only as an image (scanned memo) | Not searchable or accessible | Text version on the page, with the scanned memo linked as PDF |
| English and Tagalog versions with different dates or fees | Translation drift | Write facts once in a shared data block; generate both versions from it, or check every number in both |

```text
# Banned
The Barangay Council of San Isidro is pleased to inform everyone that
there will be an exciting Clean-Up Drive! Kindly be guided accordingly.
Your participation is highly appreciated! Mabuhay! 🌿✨

# Use
Clean-up drive, Purok 1 to 3
Date: Saturday, 8 March 2026, 6am–9am
Meeting point: Purok 2 chapel
Bring: gloves, sako, walis tingting
Contact: Kagawad Maria Santos, 0917 123 4567
Posted 3 March 2026
```

## 08.19 Check

- [ ] Subject lines, SMS and push titles state what happened or what to do; no greeting, no emoji
- [ ] Sender name is the product or office, not "The {Product} Family"
- [ ] Preheaders add a new fact; no "View this email in your browser" default
- [ ] Welcome emails: sign-in link, one next step, support contact; no company story
- [ ] Verification and reset emails state expiry and include a "did not request" line
- [ ] OTP appears first, as plain digits, with expiry and "do not share"
- [ ] Security emails state time (Asia/Manila), device and a link to secure the account
- [ ] Receipts list items, VAT, total in ₱ with 2 decimals, method and reference
- [ ] Nothing is called "Official Receipt" unless it is a BIR-registered OR
- [ ] Invoices show due date and exact payment instructions (GCash, Maya, bank)
- [ ] Newsletters say why the reader gets them and have a visible one-click unsubscribe
- [ ] SMS fits one segment where possible; no emoji; sender identified; opt-out on promotional SMS
- [ ] Push notifications name the actor and object, deep link to the item, respect quiet hours
- [ ] Social posts carry date, time, place and contact in the text, not only in the image
- [ ] Social posts use 0 to 2 real hashtags; no emoji walls, no caps shouting
- [ ] No invented officials, quotes, "Hon." or "Juan Dela Cruz" placeholders
- [ ] App store text states what the app does in the first line; "What's New" names real changes
- [ ] Every page has a unique title, page name first, 50 to 60 characters, no emoji
- [ ] Every key page has a unique meta description of 120 to 160 characters that names the content
- [ ] OG image is 1200x630, absolute HTTPS URL, page-specific where it matters
- [ ] `og:url` is the production URL; `og:locale` matches the page language
- [ ] Share preview checked in Facebook Sharing Debugger
- [ ] Alt text describes content; decorative images use `alt=""`; no "image of"
- [ ] Chart and poster images have alt text carrying the key data or facts
- [ ] Captions add names, dates, places or credit; none on decorative images
- [ ] No welcome banner; one site-wide banner at a time, dismissible, with an end date
- [ ] Outage and emergency banners state the fact, the workaround and the source
- [ ] Cookie banner exists only when non-essential cookies are set; Accept and Decline look equal
- [ ] Public notices have date posted, who is affected, requirements as a list, fees in ₱, deadline with time, contact
- [ ] Election and voter notices cite the issuing office and contain no partisan content
- [ ] Notices exist as text, not only as scanned images
- [ ] English and Tagalog versions carry identical dates, fees and numbers
