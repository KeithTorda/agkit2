---
part: 04
title: State Microcopy and Formats
covers: empty states, error pages 400 to 503, offline, maintenance, permission, rate limit, session expired, onboarding and first-run copy, tooltips, in-app notifications, badges and labels, Live and real-time labels, ranks and gamification, status words, timestamps, relative time, numbers, currency, dates and times, pluralisation, truncation, units
---

# 04 — State Microcopy and Formats

Read when: writing empty states, error pages, offline or maintenance screens, onboarding, tooltips, notifications, badges, status labels, or formatting numbers, pesos, dates, times, plurals and units.

## 04.1 Empty states: the rule

An empty state says what is missing, then gives the next action if the user can take one. No cheerleading, no illustration required, no emoji.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Illustration plus headline plus paragraph plus button for every empty list | Template block | One line of text plus one action link. Illustration only on the first-run screen of a main module, if DESIGN.md has one. |
| "Nothing here yet!" | Cheerful filler | Name the object: "No orders yet." |
| "Your journey starts soon ✨" | Banned words, emoji | Delete |
| "It's lonely in here… 👻" | Joke | "No messages." |
| Same empty text on first use, no results and filtered-to-zero | Different causes need different fixes | Separate strings per cause (04.2) |
| Empty state that hides the page header and filters | User cannot change the filter | Keep the header, filters and search visible |
| Empty table showing headers plus plugin text "No data available in table" | Plugin default | Headers kept, one row: "No records." plus action link |
| Big "Create your first X" button when the user lacks permission to create | Dead end | Show the fact only, and who can add: "No products. Ask an admin to add products." |
| Empty chart with axes and "No data" in the middle | Wasted space | Replace the chart with one line: "No sales in this period." |

## 04.2 Empty states: every kind

| Context | AI (banned) | Use |
|---|---|---|
| Empty list (first use) | "Nothing here yet! Your journey starts soon ✨" | "No threads yet." plus "Create thread" |
| Empty search | "We couldn't find what you're looking for 🔍" | "No results for 'xyz'." plus "Clear search" |
| Search with suggestion | "Did you mean something else? 🤔" | "No results for 'Juan Dela Cruz'. Try the last name only." |
| Filtered to zero | "No matches! Try adjusting your filters ✨" | "No orders match these filters." plus "Clear filters" |
| Date range with no data | "Looks quiet around here 🌙" | "No sales from 1 to 7 Sep 2026." plus "Change dates" |
| Empty inbox | "Your inbox is empty! Time to start connecting 💬" | "No messages." |
| Inbox zero after reading all | "You're all caught up! 🎉 Go touch grass!" | "No unread messages." |
| Empty notifications | "No notifications yet! We'll let you know 🔔" | "No notifications." |
| Empty dashboard | "Welcome! Let's set up your dashboard 🎉" | "No data yet. Add your first entry." |
| Empty cart | "Your cart is feeling lonely 🛒" | "Cart is empty." plus "Browse products" |
| Empty wishlist | "Start saving your faves! 💖" | "No saved items." |
| Empty orders (customer) | "No orders yet… Time to treat yourself! 🛍️" | "No orders yet." plus "Shop" |
| Empty file list | "Drop some files to get the party started 🎉" | "No files. Upload file" |
| Empty comments | "Be the first to share your thoughts! 💭" | "No comments." plus the comment box |
| Empty team / members | "It's just you for now! Invite your crew 👥" | "No other members. Invite member" |
| Empty class list (school) | "Your class is waiting to be filled! 📚" | "No students in Grade 7 - Sampaguita. Add students or Import from CSV" |
| Empty grade sheet | "Grades coming soon! ✏️" | "No grades entered for Quarter 1." |
| Empty voter list / precinct search (COMELEC) | "Oops! We couldn't find you 😢" | "No record found for this name and birth date. Check the spelling, or visit your local COMELEC office." |
| Empty resident list (barangay) | "Your barangay is empty!" | "No residents recorded for Purok 3." plus "Add resident" |
| No requests (barangay clearance queue) | "All clear! Nothing to process 🎉" | "No pending requests." |
| Empty inventory | "Your shelves are empty! Let's stock up 📦" | "No products. Add product or Import from CSV" |
| Out-of-stock list empty | "Great news! Everything's in stock! 🎉" | "No items below reorder level." |
| No sales today (POS) | "No sales yet today, but the day is young! ☀️" | "No sales today." |
| No transactions in a shift | "Quiet shift so far!" | "No transactions this shift." |
| Empty audit log | "Nothing to see here 👀" | "No activity in this period." |
| Empty trash | "Squeaky clean! ✨" | "Trash is empty." |
| Empty archive | "No archived items yet!" | "No archived items." |
| Empty calendar day | "Enjoy your free day! 🏖️" | "No events." |
| No announcements (school or LGU) | "Stay tuned for exciting news! 📢" | "No announcements." |
| No job openings | "We're not hiring right now, but stay tuned! 🚀" | "No open positions." |
| Error-caused empty | "Nothing here!" (when the load failed) | Do not show an empty state. Show the error: "Could not load orders. Retry" |
| No permission to see items | "Nothing to show" | "You don't have access to Payroll. Ask an admin." |
| Deleted or moved item | "It vanished! 🪄" | "This item was deleted." or "Moved to Archive." |
| Feature not set up | "Unlock this feature! ✨" | "Online payment is not set up. Set up GCash in Settings." |

## 04.3 Error pages

Title states the problem. Body gives the cause if known and the next action. No jokes, no illustrations of astronauts, robots or broken plugs. Keep the site header and footer on error pages so users can navigate.

| Status | AI (banned) | Use |
|---|---|---|
| 400 Bad Request | "Uh oh! Something's not quite right 🤔" | Title "Request not valid". Body "The link or form data was incomplete. Go back and try again." |
| 401 Unauthorized | "Who goes there? 🛡️" | Title "Sign in required". Body "Sign in to view this page." plus "Sign in" |
| 403 Forbidden | "Access denied! You don't have superpowers for this" | Title "No permission". Body "Your account can't open Payroll. Ask an admin for access." |
| 404 Not Found | "Oops! Looks like you're lost in space 🚀" | Title "Page not found". Body "Check the address, or go to the homepage." plus a search box if the site has search |
| 405 Method Not Allowed | "That's not how this works! 🙅" | Title "Action not allowed". Body "This page can't process that request. Go back and try again." |
| 408 Request Timeout | "Took too long, zzz 😴" | Title "Request timed out". Body "The server did not get the full request in time. Try again." |
| 410 Gone | "It's gone forever! 👋" | Title "Page removed". Body "This page was removed on 12 Aug 2026." plus link to the replacement if one exists |
| 413 Payload Too Large | "Whoa, that's huge! 🐘" | Title "File too large". Body "Maximum upload size is 10 MB." |
| 419 Page Expired (Laravel CSRF) | "Page Expired" (framework default, no help) | Title "Form expired". Body "The page was open too long. Reload and submit again. Your typed answers may need to be re-entered." |
| 422 Unprocessable | "Hmm, something's off with your data" | Show field errors on the form, not an error page |
| 429 Too Many Requests | "Slow down, speedy! 🏎️" | Title "Too many requests". Body "Try again in 60 seconds." |
| 500 Internal Server Error | "Our hamsters are fixing things! 🐹" | Title "Server error". Body "Something failed on our side. Try again in a few minutes. Error ID: 8f3a2c." |
| 502 Bad Gateway | "The internet gremlins struck again! 👾" | Title "Server not responding". Body "Try again in a few minutes." |
| 503 Service Unavailable | "We're taking a quick nap 😴" | Title "Service unavailable". Body "Down for maintenance until 3:00 PM." or "Too much traffic. Try again in a few minutes." |
| 504 Gateway Timeout | "Time's up! ⏰" | Title "Server took too long". Body "Try again. If it keeps happening, contact support@{domain}." |

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Giant "404" digits as the hero | Template | Status in small text; the title is the plain message |
| Error page with no navigation | Dead end | Keep the site header; add "Go to homepage" |
| Framework default error page in production (Laravel, Django, Next.js, Nginx, Apache) | Unfinished | Custom pages for 403, 404, 419, 429, 500, 503 |
| Stack trace or SQL error on a public page | Leak and unfinished | Plain message plus error ID; details in logs only |
| "Go back home, astronaut!" | Joke | "Go to homepage" |
| Auto-redirect to home after 5 seconds | Loses the URL the user needs to report | No auto-redirect |
| Same page for 404 and 500 | Wrong cause | One page per status |

## 04.4 Offline, maintenance, permission, rate limit, session expired

| Context | AI (banned) | Use |
|---|---|---|
| Offline banner | "Looks like you're offline! 📡" | "No connection." |
| Offline with queued changes | "Don't worry, we've got your back! 💪" | "Offline. 3 sales saved on this device. They will upload when the connection returns." (only if true) |
| Back online | "Yay, you're back! 🎉" | "Back online. 3 sales uploaded." |
| Offline and action blocked | "Can't do that right now 😢" | "Payment needs a connection. Try again when online." |
| Slow connection | "Your internet is being slow 🐌" | "Connection is slow. Images are hidden to save data." (only if the app does that) |
| Maintenance page | "We're making things even better! Be right back ✨" | "Down for maintenance. Back at 3pm." Include the date and timezone for long windows: "Back 24 Sep 2026, 6:00 AM (PHT)." |
| Scheduled maintenance banner | "Heads up! Exciting upgrades coming 🚀" | "Maintenance on 28 Sep, 10:00 PM to 12:00 AM. The site will be unavailable." |
| Read-only mode | "Chill mode activated 😎" | "Read-only until 6:00 AM. You can view records but not edit." |
| Permission on a page | "Oops! This area is off-limits 🚫" | "You don't have access to this page. Ask {role or name} for access." |
| Permission on a button | Button hidden with no explanation where users expect it | Disabled button with tooltip "Only managers can void sales." or hide consistently |
| Feature on a higher plan | "Unlock this premium feature! ✨" | "Export is on the Pro plan. View plans" |
| Rate limit on sign-in | "Too many attempts, slow down! 🛑" | "Too many sign-in attempts. Try again in 15 minutes, or reset your password." |
| Rate limit on OTP | "Chill! Wait a bit before trying again" | "Wait 60 seconds before requesting a new code." |
| API quota | "You've hit the limit! 🚧" | "Monthly limit of 1,000 SMS reached. Resets 1 Oct." |
| Session expired | "Your session took a nap 😴" | "Session expired. Sign in again." |
| Session expiring warning | "Still there? 👀" | "You'll be signed out in 2 minutes. Stay signed in" |
| Signed in elsewhere | "Someone else is here! 👻" | "Signed out because this account signed in on another device." |
| Account locked | "Your account is locked 🔒" | "Account locked after 5 failed attempts. Reset your password or contact the admin." |
| Account pending approval | "Hang tight! We're reviewing you ✨" | "Account pending approval by the school registrar. You'll get an email when approved." |
| Browser not supported | "Your browser is so last year! 🦕" | "This site needs Chrome, Edge, Firefox or Safari from 2022 or later." |
| JavaScript disabled | Blank page | `<noscript>`: "This page needs JavaScript. Turn it on in your browser settings." |

## 04.5 Onboarding and first-run copy

| Context | AI (banned) | Use |
|---|---|---|
| Welcome banner | "Welcome to {App}! We're so glad you're here 🎉" | (don't show a welcome banner) |
| First screen heading | "Let's get you started on your journey… 🚀" | The first task as a heading: "Add your products" |
| Dashboard greeting | "Good morning, Keith! 👋" | No greeting. Dashboard layout is in part 22. |
| Setup checklist | "Complete these 5 fun steps to unlock the full experience! ✨" | "Setup: 2 of 4 done" with plain task names: "Add a branch", "Add products", "Connect printer", "Invite staff" |
| Progress bar for profile | "Your profile is 60% awesome!" | Skip the percentage bar. List missing required fields only. |
| Product tour overlay | "Let us show you around! 🗺️" | No tour. Put labels and short help next to the controls. If required, one dismissable line: "New: bulk import. See how" |
| Tour step copy | "This is where the magic happens ✨" | Never needed |
| Feature pitch | "Unlock the power of real-time analytics" | "View weekly active users" |
| Feature announcement in app | "🎉 Big news! We just launched something amazing!" | "New: Export to Excel. In Reports, choose Export." with a dismiss button |
| First-run empty module | "Your adventure begins here!" | "No products. Add product or Import from CSV" |
| Sample data notice | "We've added some fun demo data for you to play with! 🎮" | "Sample data shown. Delete sample data" |
| Invite prompt | "Teamwork makes the dream work! 🤝" | "Invite staff so they can record sales." |
| Setup done | "You're all set! Time to crush it! 💪" | Remove the checklist. No message needed. |
| Role picker | "Tell us about yourself! Who are you? 🦸" | "Your role" with options: Owner, Cashier, Manager |
| Skip link | "I'll explore on my own 😎" | "Skip" |

## 04.6 Tooltips

A tooltip adds one missing fact. It never repeats the label, and it never holds content the user needs to finish a task.

| Context | AI (banned) | Use |
|---|---|---|
| Shortcut hint | "Pro tip! 💡 You can also..." | "Keyboard shortcut: Ctrl+S" |
| Icon button | "Click me to do the thing!" | The action name: "Print receipt" |
| Info icon on a field | "This is the amount field" | The missing fact: "Includes 12% VAT." |
| Info icon on a metric | "Your awesome stats!" | The definition: "Paid orders minus refunds, 1 to 30 Sep." |
| Disabled button | No tooltip | Why it is disabled: "Add at least one item." |
| Truncated text | No tooltip | Full text in `title` or a tooltip |
| Tooltip repeating the label | Button "Delete", tooltip "Delete" | No tooltip |
| Tooltip with a paragraph | Hidden essay | Max 1 sentence; move longer help to the page |
| Tooltip with links or buttons inside | Unreachable on touch and keyboard | Use a popover or inline help. See part 21. |
| Tooltip as the only place for required info | Hidden on mobile | Put required info in helper text |
| "Did you know? 🤓" rotating tips | Filler | Delete |

## 04.7 In-app notifications

Email, SMS and push wording is in part 08. This is the notification list and bell panel.

| Context | AI (banned) | Use |
|---|---|---|
| Mention | "You've been mentioned! 🔔" | "John replied to your thread." |
| Reply | "Someone has something to say! 💬" | "Ana replied: 'Pwede po ba bukas?'" (first 60 characters) |
| Assignment | "A new task has landed on your desk! 📋" | "Maria assigned you Order 1042." |
| Approval needed | "Action required! ⚠️⚠️" | "Leave request from Ben needs your approval." |
| Approved | "Great news! 🎉 Your request was approved!" | "Barangay clearance BC-2026-0481 approved. Ready for pickup." |
| Rejected | "Unfortunately, bad news 😔" | "Request BC-2026-0482 returned: missing valid ID. Upload ID" |
| Low stock | "Uh oh, running low! 📉" | "Rice 25kg: 3 left. Reorder level is 10." |
| Payment received | "Ka-ching! 💰" | "₱1,250.00 received from Juan dela Cruz via GCash." |
| System | "Important update from the team! 📣" | "Maintenance on 28 Sep, 10:00 PM to 12:00 AM." |
| Grouped | 12 separate "New order" rows | "12 new orders since 9:00 AM" |
| Notification with no link | Dead end | Every item links to the record |
| Notification titles in Title Case with body repeating title | Double message | One line, sentence case |
| Unread count "99+" when the real count is 3 | Fake urgency | The real count; "99+" only above 99 |
| Bell badge on first sign-in with welcome notifications | Fake activity | Start at 0 |

## 04.8 Badges and labels

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "New" badge that never expires | Stale | Show "New" for a fixed period (e.g. 14 days) set in config, then remove |
| "New" on every menu item | No signal | Max 1 "New" per screen |
| "Beta" on a finished feature | Hedge | Remove, or state what is limited: "Beta: exports max 1,000 rows" |
| "Pro" badge on free features | Misleading | Only on features that need a paid plan |
| "Hot 🔥", "Trending 📈", "Popular ⭐" with no data | Fake social proof | Only when computed: "Most ordered this week" with the rule documented |
| "Best seller" on every product | No signal | Top N by units sold in a stated period |
| "Recommended" with no reason | Unexplained | "Recommended for schools under 500 students" |
| "Limited" / "Exclusive" | Fake scarcity | Delete, or the real limit: "30 seats left" from the database |
| "Verified ✓" without verification | False claim | Only when a verification process exists; state it in the tooltip |
| "Official" on unofficial pages | Misleading, risky for LGU and COMELEC look-alikes | Only on sites run by the agency. See part 09. |
| Gradient or glowing badges | Visual tell | Plain badges. Styling is in part 10 and part 12. |
| Badges with emoji | Chat-output | Text only |
| ALL CAPS badge text in source: "NEW" | Hard-coded shouting | "New" in source; uppercase via CSS only if the design system says so |
| Badge text longer than 2 words | Not a badge | Use a status line instead |

## 04.9 Live and real-time labels

Never tag polling or static dashboards as "Live" or "Real-Time."

| Actual tech | Correct label |
|---|---|
| WebSocket / SSE push | Live |
| True presence (who's online) | Online |
| Polling / auto-refresh | Updated 2m ago |
| Static dashboard | Dashboard, Activity |
| Preview panel | Preview |
| Cron/scheduled sync | Synced hourly |
| Manual refresh only | "As of 2:14 PM" plus "Refresh" |
| Election results feed from a periodic upload | "As of 8:30 PM, 72% of precincts reporting" with the source named. Never "Live results" unless the feed is push. |
| Video stream | Live (only while streaming) |
| Pulsing red dot on a non-live element | Remove the dot |

## 04.10 Ranks and gamification labels

Banned fantasy titles: System Founder, Celestial Luminary, Holographic Prestige, Digital Architect, Cyber Guardian, Neon Sage, Elite Vanguard, Astral Pioneer, Cosmic Sentinel, Shadow Alchemist, Code Wizard, Tech Ninja, Growth Hacker, Community Champion, Forum Wizard, Power User, Super Contributor, Legendary Member, Elite Member, Platinum Member, Diamond Tier, Mythic Rank.

Use: Admin, Mod, Member, Level 12, New member, Regular, Contributor, Staff. State the requirement plainly: "50 posts" not "Ascend to new heights."

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Ascend to new heights", "Unlock your next rank" | Game-quest copy | "Level 3 at 50 posts" |
| XP bars and streak flames on a utility app | Gamification nobody asked for | Remove unless the brief requires it |
| "🔥 7-day streak!" | Emoji plus pressure | "Posted 7 days in a row" if streaks are in scope |
| Achievement toasts: "Achievement unlocked: First Post! 🏆" | Game UI | None |
| Leaderboard of customers or residents | Privacy risk and noise | Remove, unless the brief requires it and users opted in |
| Loyalty tiers named Gold, Platinum, Diamond with no benefit list | Empty status | Tier name plus the benefit: "Tier 2: 5% off" |
| Staff roles invented: "Sales Hero", "Inventory Wizard" | Fantasy titles | Real roles: Cashier, Manager, Inventory clerk |

## 04.11 Status words

Pick one fixed set per record type. Store an enum in code, map it to one label, and use that label everywhere: table, detail page, filter, email, export.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Synonyms for one state across screens: "Pending", "Awaiting", "In review", "Processing" | Inconsistent | One word per state |
| Cute status names: "On its way! 🚚", "Cooking 🍳", "Done & dusted ✅" | Chat voice | Plain words: Shipped, Preparing, Completed |
| Status with emoji only: 🟢 🟡 🔴 | Colour-only meaning | Text label; colour as a secondary cue. See part 27. |
| "Active" / "Inactive" for everything | Vague | The real state: Enrolled, Dropped, Graduated, Transferred |
| "Success" / "Failed" as status on business records | Log language | Paid, Unpaid, Refunded, Voided |
| Status in ALL CAPS in source | Shouting | Sentence case |
| Raw enum shown: "PENDING_APPROVAL", "status_2" | Leaked internals | Mapped label: "Pending approval" |
| Colour that contradicts the word: green "Pending" | Mixed signal | Colour follows meaning from DESIGN.md status tokens |

| Record | Suggested status set |
|---|---|
| Order (online) | Pending payment, Paid, Preparing, Ready for pickup, Shipped, Delivered, Cancelled, Refunded |
| Sale (POS) | Completed, Voided, Refunded, Partially refunded |
| Payment | Unpaid, Pending, Paid, Failed, Refunded |
| Invoice | Draft, Sent, Paid, Overdue, Void |
| Barangay document request | Submitted, In review, Returned, Approved, Ready for pickup, Released |
| Enrollment | Submitted, For verification, Enrolled, Waitlisted, Not enrolled |
| Student record | Enrolled, Transferred out, Dropped, Graduated |
| Voter registration | Pending, Approved, Disapproved, Deactivated (use COMELEC's own terms where the client provides them) |
| Leave request | Pending, Approved, Rejected, Cancelled |
| Ticket / complaint | Open, In progress, Waiting for reply, Resolved, Closed |
| Product stock | In stock, Low stock, Out of stock, Discontinued |
| Account | Active, Pending approval, Locked, Deactivated |
| Job / sync | Queued, Running, Done, Failed |

## 04.12 Timestamps and relative time

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Just now" for anything under 1 hour | Loose | "Just now" under 1 minute, then "5 min ago", "2 hr ago" |
| "a few seconds ago", "about 1 hour ago", "over 2 years ago" (library default wording) | Default moment/date-fns copy | Short fixed forms: "1 min ago", "2 hr ago", "Yesterday", then the date |
| Relative time for dates older than 7 days: "143 days ago" | Hard to place | Absolute date after 7 days: "12 Apr 2026" |
| Relative time only, no absolute anywhere | Cannot verify | Absolute date and time in `title` or a `<time datetime="...">` element |
| Relative time that never updates | Stale | Update every 60 s, or show the absolute time |
| Relative time in exports, receipts, audit logs, legal records | Meaningless later | Absolute date and time with timezone |
| Future relative: "in 3 days" for deadlines without the date | Ambiguous | "Due 26 Sep (in 3 days)" |
| "Yesterday at 11:59 PM" computed in UTC | Wrong day for Philippine users | Compute in Asia/Manila (UTC+8) or the user's timezone |
| Mixed "min", "mins", "minutes", "m" | Inconsistent | One style: "min" and "hr" in lists; full words in sentences |
| "Last updated: {timestamp in ISO}" | Raw format | "Updated 2:14 PM" or "Updated 12 Sep 2026, 2:14 PM" |

## 04.13 Numbers

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| No thousands separator: "12400" | Hard to read | "12,400" (comma separator, period decimal: Philippine and US convention) |
| Mixed separators: "12.400,50" | European format by locale default | Force `en-PH` locale in `Intl.NumberFormat` |
| Rounded vanity numbers: "10K+ users", "99.9% uptime" with no source | Fake stat | The real number from data, or nothing. Marketing stats are in part 05. |
| Abbreviations in tables: "1.2K" | Loses precision where users compare | Full numbers in tables; "1.2K" only in tight chart axes and badges |
| Decimals inconsistent in a column: "12", "12.5", "12.50" | Unaligned | Fixed decimals per column; right-align; `font-variant-numeric: tabular-nums`. Table layout is in part 19. |
| Percent with false precision: "33.3333%" | Unformatted | 0 or 1 decimal: "33.3%" |
| Percent without base: "Up 200%" | Misleading | "Up from 4 to 12 (200%)" |
| Numbers written as words in UI: "three items" | Slower to scan | Numerals: "3 items" |
| Negative numbers with hyphen: "-500" | Minus looks like a dash | True minus "−500", or parentheses in accounting views: "(₱500.00)" |
| Counters animated from 0 | Delay before the real number | Show the number. Motion is in part 25. |
| Ordinals wrong: "1th", "2th", "Grade 1st" | Bug | "1st, 2nd, 3rd, 4th"; "Grade 1" |
| Phone numbers split wrong: "09171234567" | Hard to read | Display "0917 123 4567" or "+63 917 123 4567"; store E.164 "+639171234567" |
| ID numbers without format: "123456789000" (TIN) | Hard to check | Display "123-456-789-000"; LRN as 12 digits without spaces unless the client's format says otherwise |

## 04.14 Currency: peso

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Dollar sign on a Philippine site: "$9/mo" | Template copy | "₱499/mo" |
| "PHP 1250", "P1250", "Php 1,250" mixed | Inconsistent | "₱1,250.00" in UI. "PHP 1,250.00" only where the peso sign cannot render (SMS, some printers, CSV). |
| "1,250 ₱" or "₱ 1,250" | Wrong placement or spacing | Sign before the number, no space: "₱1,250.00" |
| No centavos on prices in a POS or invoice | Inconsistent with receipts | Always 2 decimals in POS, invoices, receipts, statements |
| Centavos on marketing price cards when the price is whole | Clutter | "₱499" is fine on pricing pages; be consistent within the page |
| Float arithmetic: "₱1,249.9999" | Bug | Store centavos as integers; format at display |
| Total without VAT note on a receipt or invoice | Incomplete | Show VATable sales, VAT (12%), VAT-exempt, zero-rated lines as the client's BIR setup requires. Do not invent lines. See part 09. |
| Discount shown as "-₱50" | Hyphen as minus | "Discount: −₱50.00" or "Less: ₱50.00" |
| "Free!" for a ₱0 fee | Hype | "No fee" or "₱0.00" |
| Senior citizen or PWD discount unlabeled | Missing legal context | "Senior citizen discount (20%)", "PWD discount (20%)" with the ID number field if the client requires it |
| `toLocaleString()` with no locale | Output depends on the device | `new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' })` |
| Other currencies shown without code | Ambiguous | "US$10.00", "₱560.00" when both appear |

## 04.15 Dates and times

Philippine forms often use MM/DD/YYYY (government forms follow US order), while many users write DD/MM. Any numeric date with a day from 1 to 12 is ambiguous. Use a month name in display.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "09/10/2026" in display | Ambiguous: 9 Oct or 10 Sep | "10 Sep 2026" or "Sep 10, 2026". Pick one style per project. |
| ISO in UI: "2026-09-10T14:00:00Z" | Raw data | "10 Sep 2026, 10:00 PM" (converted to PHT) |
| Numeric date input with no format hint | Users guess the order | Label or helper "MM/DD/YYYY" matching the parser, or three fields: Month (select), Day, Year |
| Month select with numbers only | Error-prone | Month names: "January" to "December" |
| 24-hour time for general users | Uncommon in PH daily use | "2:30 PM"; 24-hour only in logs and technical screens |
| "2:30pm", "2:30 P.M.", "14:30hrs" mixed | Inconsistent | "2:30 PM" everywhere |
| Timezone missing on deadlines, elections, maintenance | Ambiguous for OFWs and servers in UTC | Add "PHT" or "(Philippine time)" where users may be abroad |
| Server-side dates in UTC shown as local | Off by 8 hours | Store UTC, display in Asia/Manila unless the user sets another |
| Date ranges: "09/01/2026 - 09/07/2026" | Hard to read | "1 to 7 Sep 2026", "28 Sep to 3 Oct 2026" |
| Day names missing on schedules | Users check a calendar | "Mon, 28 Sep" for schedules and appointments |
| School year written "2026-2027" vs "SY 2026–2027" mixed | Inconsistent | One form: "SY 2026–2027" |
| Quarter or semester written differently across pages | Inconsistent | "Q1", "1st Quarter", "1st Semester": pick per client and keep it |
| Birthdates shown with relative time: "38 years ago" | Wrong format | Date, or age if needed: "Age 38" |
| Holidays assumed from US calendar | Wrong | Use the Philippine holiday list for the year; do not hard-code |

## 04.16 Pluralisation

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "1 items", "1 results found" | No plural logic | `Intl.PluralRules` or the framework's plural helper: "1 item", "2 items" |
| "item(s)", "file(s)", "student(s)" | Lazy fallback | Real plural logic |
| "0 items" with a plural sentence around it | Awkward | Empty state instead: "No items." |
| Plural built by adding "s": "1 categorys", "2 boxs", "2 persons" | Wrong English | Full singular and plural strings per key |
| Plural rules copied from English into Filipino strings | Filipino marks plural with "mga", not suffixes | Separate strings per language. See part 09. |
| Count and noun in separate elements that break on wrap | "3" on one line, "items" on the next | Keep count and noun in one string with a non-breaking space if needed |
| "You have 1 new messages!" | No plural logic, plus "!" | "1 new message" |

## 04.17 Truncation

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| CSS `text-overflow: ellipsis` on names, amounts, IDs | Hides the part users need | Never truncate amounts, IDs, reference numbers or dates. Wrap them. |
| Truncated text with no way to read the full value | Data loss | Full value in a tooltip, `title`, or on the detail page |
| Truncation at a fixed character count mid-word: "Barangay San Ro…" | Hard to read | Truncate at word boundaries, or use `line-clamp` with 2 lines for titles |
| Truncating the end of file names | Extension lost | Truncate the middle: "Enrollment-for…Q1.pdf" |
| "Read more" on 2 lines of hidden text | Extra click for little | Show the full text if under about 300 characters |
| Truncated emails | Unverifiable | Wrap at "@" with `overflow-wrap: anywhere` |
| Masked data shown as truncation: "0917…" | Unclear | Mask explicitly: "0917 *** 4567" |
| Notification previews cut in the middle of a name | Awkward | Cut at 60 characters on a word boundary |

## 04.18 Units and measurements

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Imperial units on a Philippine site: "5 lbs", "72°F", "2 miles" | US template copy | Metric: "2.3 kg", "32°C", "3 km". Keep "sq m" or "sqm" for land area, as used locally. |
| No space between number and unit: "5MB", "10km" | Inconsistent | "5 MB", "10 km"; "%" and "°C" attach: "12%", "32°C" |
| Mixed "MB" and "Mb" | Different units | "MB" for file sizes |
| File sizes in bytes: "5242880 bytes" | Raw | "5 MB" |
| Durations in seconds: "3600 seconds" | Raw | "1 hr" |
| "24/7 support" when support is office hours | False | "Mon to Fri, 8 AM to 5 PM" |
| Product units unclear: "Rice ₱1,450" | Missing unit | "Rice, 25 kg sack: ₱1,450.00"; "per kilo", "per piece", "per pack" |
| Quantity units abbreviated inconsistently: "pc", "pcs", "piece(s)" | Inconsistent | "pc" singular and "pcs" plural in tables, or "piece/pieces" in sentences |
| Distance for a precinct or branch without unit or basis | Unclear | "1.2 km away (straight line)" |

## 04.19 Check

- [ ] Every empty state names the object and, where allowed, gives one action.
- [ ] First-use, no results, filtered-to-zero and no-permission states have separate strings.
- [ ] Filters, search and page header stay visible in empty states.
- [ ] Failed loads show an error, not an empty state.
- [ ] No emoji, jokes, "Oops" or illustrations of astronauts or robots on any state screen.
- [ ] Custom pages exist for 401, 403, 404, 419 (Laravel), 429, 500 and 503; no framework defaults in production.
- [ ] Error pages keep site navigation; no auto-redirect.
- [ ] 500 pages show an error ID, never a stack trace.
- [ ] Maintenance copy gives the end time with date and PHT.
- [ ] Offline copy claims queued saving only if the app does it.
- [ ] Session expired, account locked and rate-limit messages say what to do and when.
- [ ] No welcome banner, no greeting, no product tour overlay.
- [ ] Setup checklist uses plain task names and disappears when done.
- [ ] Tooltips add one missing fact; none repeat the label; none hold required info.
- [ ] Every in-app notification names who, what, and links to the record.
- [ ] Unread counts are real.
- [ ] "New" badges expire; max 1 per screen.
- [ ] "Hot", "Trending", "Best seller", "Verified", "Official" appear only when backed by data or process.
- [ ] "Live" only on push; polled data says "Updated Xm ago"; election results say "As of" with source.
- [ ] No fantasy rank titles; ranks state the requirement.
- [ ] One status set per record type, mapped from an enum; no raw enum values shown.
- [ ] Relative time only under 7 days; absolute time available on hover or in `<time>`.
- [ ] Times computed in Asia/Manila unless the user chose another zone.
- [ ] Numbers use comma thousands separators; `en-PH` locale forced.
- [ ] Money shows "₱1,250.00"; no "$", no "P1250", no float artefacts.
- [ ] Receipt and invoice lines follow the client's BIR setup; nothing invented.
- [ ] Display dates use a month name; numeric inputs state the format.
- [ ] Times shown as "2:30 PM".
- [ ] Phone numbers display as "0917 123 4567" or "+63 917 123 4567", stored as E.164.
- [ ] No "item(s)"; plural logic through `Intl.PluralRules` or the framework helper.
- [ ] Amounts, IDs, dates and reference numbers never truncated.
- [ ] Metric units with a space: "5 MB", "3 km"; product prices state the unit.
