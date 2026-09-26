---
part: 06
title: Docs and Code Text
covers: README, docs pages, API docs, changelogs, release notes, commit messages, PR descriptions, issue text, code comments, docstrings, log messages, CLI output, error messages in code, TODOs, license and contributing boilerplate
---

# 06 — Docs and Code Text

Read when: writing a README, docs page, API reference, changelog, commit, PR, issue, code comment, docstring, log line, CLI output or thrown error message.

Code structure tells (console.log left in, silent catch, over-abstraction) are in part 30. Backend response shapes are in part 32. File and variable naming is in part 33. This part covers the words inside and around code.

## 06.1 README: top of the file

The first screen of a README answers three things: what it is, who it is for, how to run it.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Title "🚀 ProjectName — The Ultimate Enterprise-Grade Platform" | Emoji, banned adjectives | `# project-name` then one sentence: what it is and who uses it |
| "Enterprise-Grade High-Performance Platform" tagline | Banned adjectives, no data | "Inventory and POS web app for {Client}'s 3 stores. Laravel 11, MySQL." |
| Badge wall (build, coverage, license, stars, downloads, PRs welcome, made-with-love) on a private client repo | Decoration copied from open-source templates | No badges, or only the CI status badge if CI exists |
| Centered logo image and `<p align="center">` block | Template header | Plain markdown heading |
| "Welcome to ProjectName! 👋" | Greeting, emoji | Start with the description sentence |
| Opening paragraph that repeats the title with adjectives | Filler | One sentence, then Install |
| "A powerful, flexible, and intuitive solution for..." | Triad of banned adjectives | Say what it does: "Tracks stock across branches and prints BIR receipts." |
| Table of contents for 3 or 4 sections | Unneeded navigation | TOC only above ~8 sections |
| Screenshot placeholder `![screenshot](screenshot.png)` with no file | Broken template | Real screenshot, or remove the line |
| "Demo: coming soon" | Dead promise | Remove until a demo URL exists |
| Built-with list of 15 logos/badges | Padding | One line: "Next.js 15, Postgres 16, Tailwind 4." |

## 06.2 README: body sections

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Emoji section headers: `## ⚡ Features`, `## 🚀 Getting Started`, `## 🛠️ Tech Stack`, `## 📦 Installation` | Emoji headings, see part 02 | Boring headings: Install, Run, Config, Deploy, Limits |
| Numbered "Key Features" list with adjectives and no data | Marketing copy in a README | Short list of what it does, each item a verb phrase: "Prints receipts to 58mm thermal printers" |
| "✨ Real-time updates", "🔒 Bank-level security" feature bullets | Emoji plus hype | Plain facts: "Polls for new orders every 30s", "Passwords hashed with bcrypt" |
| Install steps that were never run | Steps fail on a clean machine | Run every command on a fresh clone before writing it down |
| `npm install` when the repo uses pnpm (lockfile says so) | Default guess | Match the lockfile: `pnpm install` |
| "Simply run the following command" / "Just clone and go" | Minimising words | "Run:" followed by the command |
| Prerequisites missing | Reader discovers them by failing | List versions: "Node 20+, PHP 8.3, MySQL 8, Composer 2" |
| `.env` setup described as "Configure your environment variables" | Vague | Copy command and table of each variable, required or optional, example value |
| No mention of limitations | Hides the truth | Limits section: "No auth yet. SQLite only. Max 1,000 rows per import. Tested on Chrome only." |
| Contributing guide for a solo or client project | Open-source boilerplate | Remove, or one line: "Private repo. Changes via PR to main." |
| Code of conduct in a personal or client repo | Boilerplate | Remove |
| "Roadmap" with 10 unchecked boxes invented by the agent | Fabricated plan | Only items the owner listed, or no roadmap |
| "Acknowledgements" thanking "the amazing open-source community" | Filler | Remove, or name the real library you forked from |
| "Support: ⭐ Star this repo if you found it helpful!" | Begging line, emoji | Remove |
| "Made with ❤️ by" footer | Template sign-off | Remove, or "Maintained by {Name}, {email}" |
| "Happy coding! 🎉" closer | Chatbot sign-off | Remove |
| Folder tree of every file, including `node_modules` hints | Padding | Tree of top-level folders only, one comment per folder, only if non-obvious |
| API section duplicating the full API docs | Two sources drift | Link to the API docs file |
| "License: MIT" on a client's proprietary code | Wrong license | Ask the owner. Proprietary: "Private. Copyright 2026 {Client}. All rights reserved." |

```md
<!-- Banned -->
# 🚀 StockFlow — Next-Gen Inventory Management
> A powerful, seamless, and intuitive solution to revolutionize your inventory workflow!

## ✨ Key Features
- ⚡ **Lightning-fast** performance
- 🔒 **Enterprise-grade** security
- 📊 **Real-time** analytics

## 🚀 Getting Started
Simply clone the repo and you're good to go!

<!-- Use -->
# stockflow

Inventory and POS web app for {Client}'s 3 hardware stores in Batangas. Laravel 11, MySQL 8.

## Install
    git clone git@github.com:client/stockflow.git
    cd stockflow
    composer install
    cp .env.example .env
    php artisan key:generate
    php artisan migrate --seed

## Run
    php artisan serve    # http://localhost:8000, login admin@example.test / password

## Limits
- One currency (PHP). No multi-currency.
- Receipt printing tested on Xprinter XP-58 only.
- No offline mode.
```

## 06.3 Docs pages and guides

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Intro: "In this guide, we will explore how to..." / "In this section we will delve into..." | Announcement opener | Start with the first instruction or the one-sentence purpose |
| "Before we dive in, let's take a moment to understand..." | Throat-clearing | Put background in a short "How it works" section, or cut it |
| Every page ends with "Conclusion" / "Wrapping up" / "Next steps 🚀" | Essay shape | End after the last step. Link to the next page if one follows |
| "Congratulations! 🎉 You've successfully set up..." | Cheerleading | "The server is running on port 3000." |
| "It's worth noting that..." / "It's important to remember..." | Hedge transitions, see part 02 | State the thing. Use a "Note:" line only for a real trap |
| Callout boxes on every paragraph (💡 Tip, ⚠️ Warning, 📝 Note) | Callout inflation | Max 1 or 2 callouts per page, only for data loss, security, or a common failure |
| "Simply", "just", "easily", "obviously" before steps | Minimising words; makes stuck readers feel slow | Delete the word |
| Steps written as prose paragraphs | Hard to follow | Numbered steps, one action each, command in a code block |
| Code blocks with `...` hiding required lines | Copy-paste fails | Complete runnable snippets, or state the file and exact line to change |
| Code blocks without language tag | No highlighting, unclear shell vs code | Tag every fence: `bash`, `php`, `ts`, `json` |
| Commands with `$ ` prompts inside copyable blocks | Copy breaks | No prompt characters, or show output in a separate block |
| Placeholders like `YOUR_API_KEY_HERE` without saying where to get it | Dead end | "Replace `sk_test_...` with the key from Settings > API." |
| Screenshots of code or terminal output | Cannot copy, cannot search | Text in code blocks |
| Explaining what a framework is ("Laravel is a powerful PHP framework...") | Padding | Link the framework docs once |
| Docs claiming features the code does not have | Written from intent, not from code | Write docs from the code. Grep for the function before documenting it |
| Heading levels skipped or every heading H2 | Structure tell, see part 28 | H1 page title, H2 sections, H3 sub-steps |
| Glossary of obvious terms ("Dashboard: the main page") | Padding | Only terms a new reader will not know: "Z-reading: end-of-day sales total required by BIR" |
| Tagalog user guide machine-translated from English | See part 09 | Write for the actual staff in the language they use at work; keep UI labels exactly as on screen |
| Admin guide for LGU/school staff written for developers | Wrong reader | Steps with the exact button labels, screenshots of the actual screen, what to do when it fails, who to call |

## 06.4 API documentation

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "Our powerful RESTful API allows you to seamlessly integrate..." | Hype opener | "Base URL: `https://api.example.ph/v1`. JSON only. Auth: Bearer token." |
| Endpoint list with descriptions "Gets the users", "Creates a user" | Restates the path | Say what is non-obvious: filters, paging, side effects, who may call it |
| Example responses that do not match the real code | Written from memory | Paste actual responses from a real call, with secrets removed |
| Example values "string", "123", "foo", "test@test.com" | Lazy placeholders | Realistic values: `"name": "Maria Santos"`, `"amount": 1250.00`, `"currency": "PHP"`, `"mobile": "+639171234567"` |
| No error table | Callers guess | Table: status code, error code, when it happens, what to do |
| Every error documented as `500 Internal Server Error` | Catch-all, see part 32 | Real codes: 400, 401, 403, 404, 409, 422, 429 with body shape |
| Response `{ "success": true, "message": "Operation successful" }` in docs | Generic envelope, see part 32 | Document the real resource shape |
| Auth section: "Authentication is handled securely" | Says nothing | Header name, token format, expiry, how to refresh, scopes |
| Rate limits "fair usage applies" | Vague | "60 requests per minute per token. 429 with `Retry-After` header." |
| Date fields undocumented | Timezone bugs | "All timestamps ISO 8601 in UTC. Display in Asia/Manila (UTC+8)." |
| Money fields as floats without note | Rounding bugs | "Amounts in centavos as integers" or "decimal string, 2 places", whichever the code does |
| Pagination "supports pagination" | Missing mechanics | Parameter names, default and max page size, response fields |
| Changelog for the API missing | Breaking changes unannounced | Dated entries per version, breaking changes marked "Breaking" |
| Webhook docs with no signature verification | Security gap | Header name, algorithm, sample verification code |
| OpenAPI spec with `description: "The ID"` on every field | Autogenerated filler | Write only descriptions that add information; leave obvious fields blank |

## 06.5 Changelogs and release notes

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "🎉 Exciting new release packed with amazing features!" | Emoji, hype | `## 2.4.0 — 2026-03-03` then the list |
| Sections with emoji: ✨ Features, 🐛 Bug Fixes, 🚀 Performance, 💄 Style | Emoji headings | Added, Changed, Fixed, Removed, Security (Keep a Changelog headings) |
| "Various bug fixes and improvements" | Hides what changed | One line per fix, user-visible effect: "Fixed: receipt total rounded wrong when discount was 12.5%." |
| "Improved performance" | No number | "Sales report loads in 1.2s instead of 6s for 10,000 rows." |
| "Enhanced user experience" | Meaningless | Name the change: "Search now matches partial SKU." |
| "Refactored codebase for better maintainability" in user-facing notes | Internal detail, no user effect | Leave internal refactors out of release notes; keep them in commits |
| No date, no version | Unusable history | Version and ISO date on every entry |
| Breaking change buried mid-list | Readers miss it | "Breaking" section first, with the migration step |
| Entries in past tense in one release, imperative in the next | Inconsistent | Pick one form (past tense: "Added", "Fixed") and keep it |
| Release notes for LGU/school staff with developer terms ("Migrated to Vite") | Wrong reader | Staff-facing notes: what they will see differently and what to do |
| "Thanks to all our amazing contributors!" on a one-person project | Template closer | Remove |
| Changelog that credits the AI or tool ("Generated with...") | Noise | Remove unless the owner asks |

## 06.6 Commit messages

Format: imperative subject line, 50 to 72 characters, no period, optional body explaining why. Follow Conventional Commits only if the repo already uses it.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "✨ feat: Add amazing new feature for seamless user experience" | Emoji, hype | `feat: add barcode search to product list` |
| Gitmoji on every commit in a repo that never used gitmoji | Style imported by the agent | Match `git log` style of the repo |
| "Update files" / "Fix stuff" / "Changes" / "WIP" | Says nothing | Name the change: `fix: VAT computed on discounted price` |
| "Refactor code for better readability and maintainability" | Generic justification | Say what moved: `refactor: move receipt formatting into ReceiptPrinter` |
| Subject line over 72 characters | Truncated in tools | Short subject, details in the body |
| Body that lists every file changed | The diff already shows this | Body explains why and any trade-off |
| Body that is a bullet list of 15 "Updated X", "Added Y" lines | Recap wall | Split into several commits, or summarise the one reason |
| "This commit introduces a comprehensive overhaul of..." | Banned words, essay voice | Imperative, plain |
| Past tense "Added X" when repo uses imperative | Inconsistent | Imperative: "add X" |
| One commit mixing a feature, a formatting pass and a dependency bump | Unreviewable | Separate commits |
| Claims in the message that are not in the diff ("Add tests") | False | Only what the diff contains |
| Co-author or tool attribution not requested by the owner | Noise | Follow the repo or session attribution rule only |

```text
# Banned
✨ feat: Implement robust and seamless authentication flow 🚀

This commit introduces a comprehensive authentication system that
empowers users to securely access their accounts.

# Use
feat: add login with email and password

Sessions last 12 hours. Lock account for 15 minutes after 5 failed
attempts, as requested by the barangay IT officer.
```

## 06.7 Pull request descriptions

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| "## 🚀 Summary" / "## ✨ Changes" / "## 🧪 Testing" emoji headings | Emoji headings | Summary, Changes, How to test, Risks |
| Summary paragraph: "This PR introduces a comprehensive set of enhancements..." | Banned words, vague | One or two sentences: what changes for the user and why |
| Changes section listing every file | Duplicates the diff | Group by behaviour: "Receipts: add TIN and branch code. Reports: add Z-reading export." |
| "✅ All tests pass" when no tests exist or were not run | False claim, see part 07 | "Tests: none for this module. Checked manually: steps below." or paste the real test command output summary |
| "No breaking changes" without checking | Unverified | List any change to routes, DB schema, env vars, public APIs. "None found" only after checking |
| Screenshots section with no screenshots | Template leftover | Add before/after images for UI changes, or remove the heading |
| Checklist of unchecked template boxes left in | Template noise | Fill it or remove it |
| "Let me know if you have any questions!" closer | Chat sign-off | Remove |
| Missing migration or deploy steps | Reviewer finds out in production | "Deploy: run `php artisan migrate`. New env var `SMS_API_KEY`." |
| Missing risk section on data-changing PRs | Hides risk | "Risk: rewrites prices for 1,200 products. Backup taken 2026-03-02." |

## 06.8 Issue and bug report text

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Title "Bug: Something isn't working as expected" | Vague | "POS: total is ₱0.01 off when 3 items have 12.5% discount" |
| "It seems like there might be an issue with..." | Over-hedged | State what happens |
| Missing steps to reproduce | Cannot act | Numbered steps, expected result, actual result, environment (browser, device, account role) |
| "Feature request: enhance the user experience of the dashboard" | Vague | "Show today's sales total on the cashier screen" |
| Labels invented that the repo does not use | Noise | Use existing labels only |
| Issue body with 5 headings for a one-line fix | Template bloat | One or two sentences for small issues |
| Priority "Critical" on cosmetic issues | Inflation | Priority from the team's scale, based on user impact |

## 06.9 Code comments

Comments explain why, not what. If the code needs a "what" comment, rename or restructure the code instead (see part 30 and 33).

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `// Increment counter by 1` above `count++` | Restates the code | Delete |
| `// Import necessary modules` above imports | Restates the code | Delete |
| `// Define the component` / `// Return the JSX` | Narration | Delete |
| `// Handle click event` above `handleClick` | Restates the name | Delete |
| Section banners `// ========== STATE ==========` in a 40-line file | Decoration | Delete. Use them only in long files where the team already does |
| `<!-- Hero Section -->`, `<!-- Features Section -->` on every block | HTML comment tell, see part 28 | Delete; semantic elements and class names carry the meaning |
| `/* Main container styles */` in CSS | Restates the selector | Delete |
| Comments that explain the language ("// useEffect runs after render") | Tutorial voice in production code | Delete |
| `// This function is responsible for handling the logic of...` | Wordy | Delete, or one line of why |
| `// Note: This is a crucial part of the code` | Banned word, no content | Say what breaks if changed |
| `// 🚀 Magic happens here` / `// ✨ Fancy animation` | Emoji, cute voice | Delete, or state the reason |
| `// Hacky fix` without detail | Unhelpful | `// Safari 17 ignores gap on <fieldset>; use margin until we drop 17.` |
| Commented-out code blocks left "for reference" | Dead code | Delete; git keeps history |
| Comment that no longer matches the code | Drift from edits | Update or delete in the same change |
| Tagalog and English comments mixed in one file for no reason | Inconsistent | One language per repo; follow existing comments |
| Good why-comment examples | These add information | `// BIR requires the OR number to be sequential per branch, never reuse.` `// Retry once: GCash sandbox returns 502 on first call after idle.` `// Keep 2dp rounding here; rounding at line total gives ₱0.01 drift.` |

## 06.10 Docstrings and JSDoc

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Docstring on every function, including 2-line private helpers | Boilerplate volume | Docstrings on public or exported functions, and on any function with a non-obvious contract |
| `@param {string} name - The name` | Restates the type and name | Omit, or state the constraint: `@param name - Full name as on PSA birth certificate, max 120 chars` |
| `@returns {Promise<void>} - Returns a promise` | Restates the type | Omit |
| "This function takes in X and returns Y" | Restates the signature | Describe side effects, errors thrown, units, edge cases |
| JSDoc types duplicated in a TypeScript file | Two sources of truth | Types in TS; JSDoc only for meaning |
| Python docstring with Args/Returns/Raises sections all saying the obvious | Template fill | Keep only sections with information |
| "A robust and efficient utility for..." | Banned words | "Formats a number as pesos: 1250.5 -> ₱1,250.50." |
| Examples in docstrings that do not run | Broken docs | Run them, or use doctest where the language supports it |

## 06.11 TODO, FIXME and placeholders

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `// TODO: implement this` in shipped code paths | Unfinished work passed as done | Implement it, or throw a clear error and list it in the report (see part 07) |
| `// TODO: add error handling` | Known gap left silent | Add the handling now, or record in the handover report |
| `// TODO: optimize later` | Vague | Remove, or state the measured problem and ticket |
| TODO without owner, date or ticket | Never gets done | `// TODO(nikko, #142): remove after BIR accreditation of new OR format` |
| Placeholder functions returning mock data (`return [{id:1,name:"John Doe"}]`) | Fake implementation, see part 30 | Real data source, or a visible "Not implemented" error |
| `Lorem ipsum` in any shipped string | Placeholder left in | Real copy or `[TODO: copy from client]` flagged in the report |
| `example.com`, `test@test.com`, `123-456-7890` in production config | Placeholder data | Real values from env or client, or fail on startup when missing |
| "Coming soon" functions in UI wired to nothing | Fake feature | Hide the button until built |

## 06.12 Log messages

Logs are for the person debugging at 2am. Each line: what happened, to what, with IDs, in a form grep can find.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `console.log("🚀 Server started!")` | Emoji, exclamation | `server listening port=3000 env=production` |
| `console.log("✅ Data fetched successfully!")` | Noise on every success | Log successes only at debug level, or not at all |
| `console.log("here")`, `console.log("test")`, `console.log(data)` | Debug leftovers, see part 30 | Remove before commit |
| `logger.error("Something went wrong")` | No context | `logger.error("receipt print failed", { orderId, printer: "XP-58", err })` |
| `logger.error("Error: " + err)` | Loses stack | Pass the error object so the stack is kept |
| Logging passwords, tokens, OTPs, full card numbers, full mobile numbers | Security and Data Privacy Act risk, see part 32 | Mask: `mobile=+63917****567`, never log OTP or password |
| Different formats per file ("Error:", "[ERROR]", "error -") | Unsearchable | One logger, one format, structured key=value or JSON |
| Log levels all `info` | Cannot filter | error for failures needing action, warn for recoverable, info for lifecycle, debug for detail |
| "Oops! Failed to connect to database 😅" | Cute voice in logs | `db connect failed host=db.internal attempt=3/5` |
| Log message in full sentences with "successfully" | Wordy | Short event names: `order created id=812` |

## 06.13 CLI output

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Spinner plus emoji on every step (🔍 Scanning..., 📦 Packaging..., ✨ Done!) | Decoration | Plain step lines; progress only for steps over ~2s |
| "✅ Success! Your project has been created! 🎉" | Emoji, exclamation | `Created ./my-app. Next: cd my-app && npm run dev` |
| ASCII-art banner on every run | Noise | Banner only on `--version` or not at all |
| Colours on output when piped to a file | Escape codes in logs | Respect `NO_COLOR` and non-TTY |
| Error: "An unexpected error occurred" | No action | `Error: config file not found at ./app.config.json. Run 'app init' to create it.` |
| Exit code 0 on failure | Scripts cannot detect errors | Non-zero exit on any failure |
| `--help` text with marketing lines | Wrong place | Usage line, commands, flags with defaults, one example |
| Prompts with "Would you like to proceed? 🤔" | Emoji, cute | `Delete 312 records? [y/N]` |

## 06.14 Error messages in code

Thrown and returned error messages are read by developers, logs, and sometimes users. Each one says what failed and the value or rule involved. User-facing error wording is in part 03 and 04.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `throw new Error("Something went wrong")` | No information | `throw new Error("Invoice total mismatch: lines=1250.00 header=1200.00 invoiceId=" + id)` |
| `throw new Error("Invalid input")` | Which input, which rule | `"mobile must match +639XXXXXXXXX, got '0917-123'"` |
| `throw new Error("Oops! An error occurred 😢")` | Emoji, cute | Plain message with context |
| Error messages with trailing "Please try again later." inside library code | User copy in the wrong layer | Library throws the fact; UI layer decides the user message |
| Same message for different failures | Undiagnosable | One message per failure cause |
| Leaking SQL or stack traces to the browser | Security issue, see part 32 | Log the detail server-side; return an error code and safe message |
| Error codes invented per call site (`ERR_1`, `ERR_2`) | Meaningless | Named codes: `OR_NUMBER_DUPLICATE`, `STOCK_NEGATIVE` |
| Validation messages "Field is invalid" | Vague | `"birth_date must be YYYY-MM-DD and not in the future"` |

## 06.15 License, contributing and repo boilerplate

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| MIT LICENSE file added to a client project | Wrong legal default | Ask the owner. Proprietary header or no license file |
| LICENSE with "[year] [fullname]" placeholders | Template never filled | Real year and holder |
| CONTRIBUTING.md with fork/PR/issue workflow on a private repo | Open-source template | Remove, or 5 lines: branch naming, how to run tests, who reviews |
| CODE_OF_CONDUCT.md in a client or solo repo | Boilerplate | Remove |
| SECURITY.md with "email security@yourdomain.com" | Placeholder | Real contact, or remove |
| `.github/ISSUE_TEMPLATE` and `FUNDING.yml` on client work | Template sprawl | Remove |
| CHANGELOG.md created with one "Initial release" entry and never updated | Dead file | Create it when the second release happens |
| `docs/` folder with one empty `index.md` | Placeholder | Remove until there is content |
| Header comment in every file with author, date, description, license | Boilerplate noise | Only if the owner's repo already does it |

## 06.16 Words to drop from technical writing

Word lists are owned by part 01. These are the ones that show up most in docs and code text.

```
simply, just, easily, obviously, clearly, of course, straightforward, seamlessly, robust, powerful, comprehensive, leverage, utilize, delve, crucial, essential, streamline, empower, cutting-edge, blazing-fast, magic, awesome, amazing, successfully, basically, actually, in order to, please note, it's worth noting, it is important to note
```

| AI word | Use instead |
|---|---|
| utilize, leverage | use |
| in order to | to |
| successfully created | created |
| please note that | (delete; state the fact) |
| simply run | run |
| a robust solution for handling X | handles X |
| comprehensive documentation | (delete; link the docs) |
| seamlessly integrates with Y | works with Y (name the version) |
| blazing-fast | the measured number, or delete |
| out of the box | by default |
| under the hood | internally, or (delete) |
| batteries included | lists what is included |

## 06.17 Check

- [ ] README first line after the title says what it is and who uses it
- [ ] No emoji in any heading, commit, changelog, log line or CLI output
- [ ] No badge wall; at most the CI badge on a private repo
- [ ] Install and run commands were executed on a clean clone and match the lockfile
- [ ] Prerequisites list exact versions
- [ ] Every env var is listed with required/optional and an example value
- [ ] README has a Limits section with real limits
- [ ] No contributing guide, code of conduct, FUNDING or issue templates on solo or client repos unless asked
- [ ] License matches what the owner chose; no MIT default on client code
- [ ] Docs pages start with the first instruction, not "In this guide we will"
- [ ] No "simply", "just", "easily", "obviously" before a step
- [ ] Code blocks are complete, runnable and tagged with a language
- [ ] Callouts limited to 1 or 2 per page, for real traps only
- [ ] Docs describe only features that exist in the code
- [ ] API docs show real request and response bodies with realistic PH values
- [ ] API docs have an error table, auth details, rate limits, timezone and money format
- [ ] Changelog entries have version, ISO date, and Added/Changed/Fixed/Removed/Security headings
- [ ] No "various bug fixes and improvements"; each fix states the user-visible effect
- [ ] Breaking changes listed first with the migration step
- [ ] Commit subjects are imperative, under 72 characters, match the repo's existing style
- [ ] Commit messages claim only what the diff contains
- [ ] PR description has Summary, Changes, How to test, Risks; no unchecked template boxes
- [ ] PR does not claim tests pass unless the tests were run in this session
- [ ] Deploy steps (migrations, new env vars) are written in the PR
- [ ] Bug reports have steps, expected, actual, environment
- [ ] Comments explain why; no comment restates the next line
- [ ] No `<!-- Hero Section -->` style comments; no section banners in short files
- [ ] No commented-out code blocks
- [ ] Docstrings only on exported or non-obvious functions, and they add information beyond the signature
- [ ] No TODO without owner or ticket in shipped paths; every remaining TODO is in the handover report
- [ ] No `Lorem ipsum`, `test@test.com`, `example.com` or mock data in shipped code
- [ ] Log lines carry event name and IDs; no "Something went wrong", no emoji
- [ ] Logs never contain passwords, OTPs, tokens or full mobile/card numbers
- [ ] Log levels used correctly (error, warn, info, debug)
- [ ] CLI errors say what failed and the next command to run; non-zero exit on failure
- [ ] CLI respects `NO_COLOR` and non-TTY output
- [ ] Thrown errors name the failing value and rule; no "Invalid input"
- [ ] User-facing messages are set in the UI layer, not hardcoded deep in library code
