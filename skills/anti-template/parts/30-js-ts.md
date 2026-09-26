---
part: 30
title: JavaScript and TypeScript
covers: comments, docstrings in code, over-abstraction, single-use helpers, classes and factories, any, interface bloat, type assertions, enums, error handling, silent catch, try/catch everywhere, defensive null checks, console.log, async misuse, timers and polling cleanup, event listeners, magic strings and numbers, utils dumping ground, reinventing platform and library features, fake implementations, mock data, TODO placeholders, emoji in code, generic names, legacy syntax, money and dates in PH projects
---

# 30 — JavaScript and TypeScript

Read when: writing or reviewing any JS or TS that is not React-specific, including Node scripts, vanilla front-end code, service workers, Express handlers' helper code, and shared TS types. React, Next and Vue patterns are in part 31. API and database design is in part 32. File and folder naming is in part 33.

## 30.1 Comments

Comments explain why. Code explains what. Docstring and doc-page style rules are in part 06.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `// Increment counter` above `count++` | Restates the line. Every generated file has these. | Delete. Keep comments that explain a reason, a constraint or a workaround. |
| `// Import dependencies`, `// Define constants`, `// Export the function` | Narrates file structure | Delete. |
| Section banners: `// ========== HELPERS ==========` in a 60-line file | Template scaffolding | Delete. If the file needs banners, split the file. |
| `// Function to handle click` above `function handleClick()` | Repeats the name | Delete. |
| JSDoc on every function with `@param {string} name - The name` | Types already say it. Adds 5 lines per function. | JSDoc only for public library APIs or when the param has a constraint: `@param amountCentavos Integer centavos, never pesos`. |
| `// Updated to fix the bug`, `// Changed per request`, `// New implementation` | Chat history leaking into code. Git holds history. | Delete. Put the reason in the commit message. See part 06. |
| `// This is a robust and efficient solution for...` | Marketing voice in code | Delete, or state the fact: `// O(n). Runs on every keystroke, keep it cheap.` |
| `// Note: ...`, `// Important: ...`, `// IMPORTANT!!!` | Shouting without a reason | State the constraint plainly: `// BIR requires the OR number to stay sequential. Do not reuse on void.` |
| Commented-out code blocks left "for reference" | Dead code that misleads search | Delete. Git has it. |
| `// eslint-disable-next-line` with no reason | Hides a real warning | Fix the warning, or add the reason after `--`: `// eslint-disable-next-line no-await-in-loop -- rate limit requires sequential calls`. |
| `// @ts-ignore` above a type error | Silences the compiler forever | Fix the type. If needed, use `// @ts-expect-error <reason>` so it fails when the error goes away. |
| Comment that contradicts the code after a later edit | Comments not updated with changes | When changing code, update or delete the comment in the same edit. |
| Emoji in comments: `// 🚀 Start server`, `// ✅ Validated` | Chat-reply habit | Plain text. See 30.14. |
| Explaining language basics: `// Use map to transform the array` | Written for a tutorial reader | Delete. |

```js
// Banned
// Function to calculate the total
// This function takes items and returns the total price
function calculateTotal(items) {
  // Initialize total to 0
  let total = 0;
  // Loop through items
  for (const item of items) {
    total += item.price; // Add price to total
  }
  return total; // Return the total
}

// Use
// Prices are integer centavos to avoid float drift on ₱ totals.
function totalCentavos(items) {
  return items.reduce((sum, item) => sum + item.priceCentavos * item.qty, 0);
}
```

## 30.2 Abstraction

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Single-use helper: `formatUserName(user)` returning `user.name` | Indirection with no reuse | Inline it. Extract a function at 3 uses or when the logic has a name worth knowing. |
| Wrapper around a built-in: `const isEmpty = (arr) => arr.length === 0` | Adds a name to learn for no gain | Write `arr.length === 0`. |
| Class with only static methods: `class StringUtils { static capitalize() {} }` | Java habit in JS | Export plain functions from a module. |
| Class with one method and a constructor: `new PriceCalculator(items).calculate()` | Object for a function | A function: `priceTotal(items)`. |
| Factory for one product: `createLoggerFactory().create("app")` | Pattern cosplay | Create the thing directly. |
| Strategy or plugin system for 2 cases | Built for imagined future needs | An `if` or a `switch`. Refactor when case 4 arrives. |
| Config objects with 15 options for a function called in one place | Options nobody passes | Hard-code the one behaviour used. Add parameters when a second caller needs them. |
| Generic `BaseService`, `AbstractHandler`, `BaseModel` with one subclass | Inheritance without variation | Delete the base. See part 32 for the backend version. |
| `EventEmitter` or pub-sub bus inside one module | Hides control flow | Call the function. |
| Dependency injection container in a 10-file app | Framework ceremony | Import modules directly. Pass dependencies as arguments where tests need to swap them. |
| Layers of re-export: `index.ts` re-exporting `lib/index.ts` re-exporting `lib/core/index.ts` | Barrel chains slow builds and create cycles | Import from the file that defines it. See part 33. |
| `constants.ts` with one constant per exported line used in one file | Hoisting everything "for maintainability" | Keep a constant next to its only user. Move to shared when a second file needs it. |
| Pipeline/compose helpers (`pipe`, `compose`) for 2 steps | Functional style for show | Two lines of normal calls. |
| Premature generic types `function get<T, K extends keyof T, R = T[K]>` for one concrete use | Signature harder than the body | Concrete types. Add generics when a second type needs it. |

```ts
// Banned
class ReceiptNumberGeneratorFactory {
  static create(config: ReceiptConfig): ReceiptNumberGenerator {
    return new ReceiptNumberGenerator(config);
  }
}
const generator = ReceiptNumberGeneratorFactory.create({ prefix: "OR" });
const orNo = generator.generate(last);

// Use
function nextOrNumber(last: number): string {
  return `OR-${String(last + 1).padStart(7, "0")}`;
}
```

## 30.3 TypeScript types

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `any` on parameters, returns and API responses | Turns TS off where it matters | Real types. For unknown input, use `unknown` and narrow, or validate with a schema (Zod, Valibot) at the boundary. |
| `catch (error: any)` | Hides the error shape | `catch (error)` then `if (error instanceof Error)` or a type guard. |
| `Record<string, any>` for known objects | `any` in disguise | Write the object type. |
| `as SomeType` to silence errors: `const user = data as User` | Lies to the compiler about unvalidated data | Validate and narrow. `as` only after a check the compiler cannot see, with a comment. |
| `as unknown as T` double cast | Forced type conversion | Fix the source type. |
| Non-null assertion everywhere: `user!.profile!.name!` | Promises values that can be null at runtime | Handle the null case once, early. Or fix the type so it is not nullable. |
| Interface for 2 props used once: `interface ButtonTextProps { text: string; size: string }` | Type ceremony | Inline the type at the parameter, or a local `type`. |
| `IUser`, `IProduct`, `TProps` prefixes | C# convention, not TS convention | `User`, `Product`, `ButtonProps`. |
| Same shape defined 3 times: `User`, `UserData`, `UserResponse`, `UserType` with the same fields | Each session wrote its own | One type. Derive variants: `Pick<User, "id" | "name">`, `Omit<User, "passwordHash">`. |
| Types hand-written for DB rows and API responses | Drift from the real schema | Generate from the source: Prisma, Drizzle, Supabase `generate_typescript_types`, OpenAPI codegen. |
| Every field optional: `name?: string; email?: string; id?: string` | Avoids thinking about required data. Forces null checks everywhere. | Required by default. Optional only when the data can be absent. Separate types for create input and stored record. |
| `enum Status { ACTIVE = "ACTIVE", INACTIVE = "INACTIVE" }` for string sets | Runtime objects and import friction | String literal unions: `type Status = "active" | "inactive"`, or an `as const` object when you need the list at runtime. |
| `types.ts` with 80 unrelated types | Dumping ground | Types live next to the code that owns them. Share only cross-module types. |
| `type Props = {}` or `interface Empty {}` | Placeholder | Delete, or `Record<string, never>` when the empty shape matters. |
| `Function`, `Object`, `object`, `{}` as types | Near-`any` | Exact signatures: `(id: string) => Promise<void>`. |
| Overloads for one implementation that takes a union | Verbose | Single signature with a union parameter. |
| `strict: false` in `tsconfig.json`, or `noImplicitAny: false` | Turned off to get the build green | `strict: true`. Fix errors. |
| `skipLibCheck` removed then errors silenced with `any` | Wrong fix | Keep `skipLibCheck: true`. Fix your own types. |
| Utility types stacked five deep: `Partial<Omit<Pick<Required<User>, ...>>>` | Hard to read | Write the resulting type out if it is used more than once. |
| Branded types or phantom types for a CRUD form | Overkill | Plain types. Brand only where mixing values costs money, e.g. `Centavos` vs `Pesos`. |

```ts
// Banned
async function getUser(id: any): Promise<any> {
  const res = await fetch(`/api/users/${id}`);
  const data = (await res.json()) as any;
  return data!.user!;
}

// Use
const UserSchema = z.object({ id: z.string(), name: z.string(), barangay: z.string() });
type User = z.infer<typeof UserSchema>;

async function getUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`GET /api/users/${id} failed: ${res.status}`);
  return UserSchema.parse(await res.json());
}
```

## 30.4 Error handling

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Silent catch: `catch (e) {}` | Failure disappears. User sees nothing, logs show nothing. | Handle, log with context, or rethrow. An empty catch needs a comment that says why ignoring is correct. |
| `catch (e) { console.log(e) }` then continue as if it worked | Logged and forgotten | Rethrow, return an error result, or show the user a message. |
| `try/catch` around every function body | Noise. Most catches only log and rethrow. | Catch where you can act: at the UI boundary, the request handler, the job runner. Let errors bubble elsewhere. |
| Catch, log, rethrow at every layer | Same error logged 4 times | Log once at the boundary that handles it. |
| `throw "Something went wrong"` or `throw { message: "error" }` | Strings and objects lose stack traces | `throw new Error("Could not load precinct list: 503")`. Use `cause` for wrapped errors: `new Error("...", { cause: err })`. |
| Error messages like "An error occurred", "Something went wrong", "Oops" | Tells nobody what failed | Name the operation and the value: `Payment ref ${ref} not found in GCash callback`. User-facing copy rules are in part 03. |
| Returning `null` on failure and `null` on "not found" | Caller cannot tell them apart | Throw on failure. Return `null` only for a real absence. Or return a result type `{ ok: false, error }`. |
| `.catch(() => [])` on fetches | Network failure looks like "no data" | Surface the error state. See part 21 for UI. |
| Fallback defaults that hide bugs: `const price = item.price || 0` | ₱0.00 on a receipt when the price failed to load | Fail loudly when required data is missing. Use `??` only for real optional values. |
| `process.on("uncaughtException", () => {})` to keep the server alive | Keeps a broken process running | Log and exit. Let the process manager restart it. |
| `window.onerror = () => true` | Suppresses all errors | Report errors (Sentry or your logger). Do not suppress. |
| Custom error class hierarchy with 12 classes for a small app | Ceremony | One or two custom errors (`NotFoundError`, `ValidationError`) the handler maps to status codes. |
| `if (error) { return; }` after an async call that throws, not returns | Misreads the API | Check the library's contract. Supabase returns `{ data, error }`. `fetch` resolves on 4xx/5xx and needs `res.ok`. Axios throws. |
| `fetch` without checking `res.ok` | 500 page HTML parsed as JSON, then a confusing error | `if (!res.ok) throw new Error(...)` before `res.json()`. |
| Alerts for errors: `alert("Error!")` | Blocking, no context | Inline error or toast with the failed action named. |

```js
// Banned
try {
  await savePayment(data);
} catch (e) {}

// Use
try {
  await savePayment(data);
} catch (err) {
  logger.error("savePayment failed", { orNo: data.orNo, err });
  showError(`Could not save payment ${data.orNo}. Try again.`);
  throw err;
}
```

## 30.5 Defensive checks

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Optional chaining on everything: `user?.profile?.address?.barangay?.name` when types say it exists | Distrust of its own types | Use `?.` only where the type allows null. Fix the type otherwise. |
| `if (arr && arr.length > 0 && Array.isArray(arr))` | Belt, braces and a rope | `if (arr.length > 0)` when `arr` is typed as an array. |
| `typeof x === "string"` checks on a parameter typed `string` | Runtime check duplicating the compiler | Validate once at the boundary (request body, form, localStorage, URL params). Trust types inside. |
| `|| []`, `|| {}`, `|| ""` after every access | Hides undefined bugs and turns `0` and `""` into defaults | Use `??` for nullish defaults. Remove defaults where the value is required. |
| Validation functions for the same input repeated in 4 layers | No boundary defined | Validate at entry (form submit, API handler). Pass typed data inward. |
| `if (!this) return;` or `if (!window) return;` in browser-only code | Guards against impossible states | Delete. For SSR, check `typeof window !== "undefined"` once where it matters. |
| `if (value === undefined || value === null || value === "")` | Long form of a nullish check | `value == null` (the one valid `==`) or `!value` when empty string is also invalid. Say which. |
| Checking `res.data.data.data` with fallbacks | Guessing the response shape | Read the API docs or log one real response. Type it. |

## 30.6 Logging and console output

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `console.log` left in shipped code | Debug output in users' consoles and server logs | Remove before commit. Add ESLint `no-console` with `warn` and `error` allowed. |
| `console.log("🚀 Server running on port 3000")` | Emoji logs from tutorials | `Listening on :3000`. |
| `console.log("data:", data)` dumping full objects with personal data | Leaks names, addresses, phone numbers, voter IDs into logs | Log IDs and counts, not records. Never log passwords, tokens, OTPs, full card or ID numbers. See part 32. |
| `console.log("here")`, `console.log("1")`, `console.log("test")` | Debug traces | Delete. Use the debugger or a breakpoint. |
| `console.error` for info messages | Wrong level makes alerts noisy | Use levels: `debug`, `info`, `warn`, `error`. |
| Mixed `console.log` and a logger library | Two systems | One logger in server code (pino, winston, or the platform logger). `console` only in scripts. |
| Log messages with no context: `logger.error("Failed")` | Useless when read at 2am | Include operation and IDs: `logger.error("sms send failed", { to: maskPhone(to), provider, status })`. |
| Success logs on every call: `"Successfully fetched users"` | Noise | Log failures and important state changes. Keep request logs at the middleware level. |
| `console.table`, `console.group`, colour codes in production code | Debug aids left in | Remove. |

## 30.7 Async

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `await` inside a `for` loop for independent calls | Sequential when it could be parallel | `await Promise.all(items.map(fn))`. Use a concurrency limit (p-limit) for large lists or rate-limited APIs. |
| `Promise.all` when one failure should not cancel the rest | One SMS failure drops the whole batch result | `Promise.allSettled` and report failures per item. |
| `async` function with no `await` | Returns a Promise for no reason | Remove `async`. |
| `new Promise((resolve) => { asyncFn().then(resolve) })` | Promise constructor anti-pattern | `return asyncFn()`. |
| Mixing `.then()` chains and `await` in one function | Two styles, harder to follow | Use `await` throughout. |
| Missing `await` on a promise that must finish (`saveLog(entry);`) | Unhandled rejection, lost writes | `await` it, or mark intent: `void saveLog(entry)` with a `.catch` that logs. Enable `@typescript-eslint/no-floating-promises`. |
| `return await` everywhere, or never | Style noise, and inside `try` the missing `await` skips the catch | `return await` inside `try` blocks. Plain `return` elsewhere. |
| `setTimeout(fn, 1000)` to wait for data or DOM to "be ready" | Race hidden by a guess | Await the promise, use the event (`DOMContentLoaded`, `load`), or `MutationObserver` for third-party DOM. |
| `async` callbacks in `forEach` | `forEach` does not wait | `for...of` with `await`, or `Promise.all` with `map`. |
| Fire-and-forget fetch on unload | Request dropped by the browser | `navigator.sendBeacon` or `fetch(..., { keepalive: true })`. |
| No timeout on network calls | A hung GCash or SMS gateway call hangs the request | `AbortSignal.timeout(10000)` on fetch. Set timeouts on HTTP clients. |
| Retry loops without limit or backoff | Hammering a failing API | Max 3 attempts with exponential backoff and jitter. Retry only idempotent calls or calls with an idempotency key. |
| Latest-response races in search boxes | Old results overwrite new ones | Abort the previous request with `AbortController`, or check a request ID before applying. |

## 30.8 Timers, polling and listeners

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `setInterval` without `clearInterval` | Leaks, duplicates on navigation, drains battery | Store the ID. Clear it on teardown. |
| `setTimeout` without cleanup in components or SPA routes | Callback runs after the view is gone | Clear on teardown. React specifics in part 31. |
| Polling every 1–5 seconds for data that changes hourly | Cost on mobile data, server load | Poll at 60s or more, show "Updated X ago" (see part 04 and part 22), or use push (SSE, WebSocket) if the data is live. |
| Polling while the tab is hidden | Wasted requests | Pause on `document.visibilityState === "hidden"`. Resume on `visibilitychange`. |
| Polling with `setInterval` and async work | Overlapping requests when one is slow | Recursive `setTimeout` scheduled after the previous request finishes. |
| `addEventListener` with no `removeEventListener` in code that mounts and unmounts | Handlers stack up. Clicks fire twice. | Use `{ signal }` from an `AbortController` and abort on teardown. |
| Scroll and resize handlers doing layout work on every event | Jank on low-end Android | `IntersectionObserver`, `ResizeObserver`, or throttle with `requestAnimationFrame`. Add `{ passive: true }` to scroll and touch listeners. |
| Global `keydown` listener for one input | Captures keys everywhere, including in other inputs | Attach to the element, or check `event.target` and ignore inputs and textareas. |
| Debounce hand-written with a bug (no clear, wrong `this`) in each file | Copy-pasted helper | One tested debounce (or from a library already in the project). 250–300ms for search input. |

```js
// Banned
setInterval(async () => {
  const res = await fetch("/api/queue");
  render(await res.json());
}, 2000);

// Use
const controller = new AbortController();
async function poll() {
  if (document.visibilityState === "visible") {
    const res = await fetch("/api/queue", { signal: controller.signal });
    if (res.ok) render(await res.json());
  }
  timer = setTimeout(poll, 60_000);
}
let timer = setTimeout(poll, 0);
function stopPolling() { clearTimeout(timer); controller.abort(); }
```

## 30.9 Magic strings and numbers

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Status strings typed inline in 10 files: `if (order.status === "pending")` | One typo breaks a branch silently | One union type or `as const` object: `ORDER_STATUS.pending`. |
| Role checks by string: `if (user.role === "admin" || user.role === "Admin")` | Case bugs, scattered rules | One role type. Permission helper: `can(user, "void_receipt")`. |
| Numbers with no name: `if (age < 18)`, `amount * 0.12`, `setTimeout(fn, 86400000)` | Reader must guess | Named constant: `VAT_RATE = 0.12`, `MIN_VOTER_AGE = 18`, `ONE_DAY_MS = 24 * 60 * 60 * 1000`. Use numeric separators: `86_400_000`. |
| Named constants for obvious values: `const ZERO = 0`, `const EMPTY_STRING = ""` | Constant for its own sake | Use the literal. |
| localStorage keys as literals in several files | Keys drift, data lost | One key map: `STORAGE_KEYS.cart`. Prefix by app: `bm:cart`. |
| Event names, route paths, query keys as literals everywhere | Rename misses one place | Central route helpers and query key factories. |
| Error codes invented per call site | No mapping possible | One list of error codes shared with the API. See part 32. |
| CSS class names built in JS by string concat | Breaks on rename | Toggle attributes or use a class map. See part 29. |

## 30.10 The utils dumping ground

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `utils.ts` or `helpers.js` with 40 unrelated functions | Every session drops helpers there | Split by domain: `money.ts`, `phone.ts`, `dates.ts`, `receipt-number.ts`. File naming rules in part 33. |
| `utils/index.ts` exporting everything | Imports pull the whole file, cycles appear | Import from the specific file. |
| Helpers that are thin aliases of libraries: `formatDate = (d) => dayjs(d).format(...)` used once | Extra hop | Call the library where needed, or one helper used everywhere with a fixed format. |
| Two helpers doing the same thing: `formatCurrency`, `formatMoney`, `toPeso`, `currencyFormat` | Four sessions, four names | Keep one. Replace calls. Delete the rest. |
| Unused helpers exported "for later" | Dead code | Delete. Tools: `knip`, `ts-prune`. |
| Helpers with vague names: `processData`, `handleData`, `transform`, `doStuff` | Name says nothing | Name the result: `groupPaymentsByDay`, `normalizePhone`. See part 33. |

## 30.11 Reinventing platform and library features

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Hand-written currency formatting: `"₱" + amount.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")` | Regex copied from a forum | `new Intl.NumberFormat("en-PH", { style: "currency", currency: "PHP" }).format(pesos)`. Create the formatter once and reuse it. |
| `toLocaleDateString()` with no locale or time zone | Server in UTC prints the wrong day for Manila after 4pm | `new Intl.DateTimeFormat("en-PH", { dateStyle: "medium", timeZone: "Asia/Manila" })`. |
| Manual relative time strings | Bugs at boundaries | `Intl.RelativeTimeFormat("en", { numeric: "auto" })`. Copy rules in part 04. |
| Moment.js added to a new project | Deprecated, large | `Intl`, `date-fns`, `dayjs`, or `Temporal` where supported. |
| `JSON.parse(JSON.stringify(obj))` to clone | Drops dates, Maps, undefined | `structuredClone(obj)`. |
| `Math.random().toString(36)` for IDs, tokens, reference numbers | Not unique, not secure | `crypto.randomUUID()` for IDs. `crypto.getRandomValues` for tokens. Sequential numbers from the DB for OR/receipt numbers. |
| Custom email regex 300 characters long | Rejects valid addresses | `<input type="email">` in the browser, simple `/.+@.+\..+/` check or a schema library on the server. Confirm by sending mail. |
| Hand-written query string parsing | Encoding bugs | `URLSearchParams` and `URL`. |
| Custom deep equal, deep merge, debounce, throttle in each project | Bug-prone copies | Use the platform, or one small library already in the project. |
| jQuery added for `$(".x").hide()` and `$.ajax` | 30 KB for built-ins | `document.querySelector`, `element.hidden = true`, `fetch`. |
| Lodash imported whole for `_.map`, `_.filter`, `_.isEmpty` | Built-ins exist | Array methods. Import single lodash functions only where built-ins lack them (`groupBy` before `Object.groupBy` is available in your targets). |
| Custom modal, dropdown, tooltip positioning code | Accessibility and edge cases missed | `<dialog>`, `popover` attribute, Floating UI. See part 21. |
| Custom form validation messages engine | Duplicates constraint validation | Native constraint validation plus a schema library on submit. See part 17. |
| Custom router in a vanilla app with 3 pages | Rebuilt the browser | Separate HTML pages or links. |
| Base64 "encryption" of data in localStorage | Not encryption | Do not store secrets client-side. If data must be protected, keep it on the server. |
| Custom CSV export with string joins | Breaks on commas, quotes, Filipino names with ñ | Quote every field, escape quotes by doubling, prefix a UTF-8 BOM (`﻿`) so Excel shows ñ and ₱ correctly. Or use a CSV library. |

## 30.12 Fake implementations and leftover mock data

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Functions that pretend: `async function sendOtp() { return true; }` | Looks done, does nothing | Implement it, or throw `new Error("sendOtp not implemented")` and list it in the report. See part 07 for reporting. |
| `await new Promise(r => setTimeout(r, 1500))` to "simulate loading" | Fake delay shipped to users | Delete. Real requests have real latency. |
| Hard-coded arrays of users, products, transactions in the component file | Mock data ships to production | Fetch from the API or a real seed. Keep fixtures in `test/fixtures` or a dev-only seed script. |
| Mock data with invented Filipino names and fake numbers `09123456789`, `Juan Dela Cruz` in production UI | Looks real, is not | Empty state until real data exists. Fixtures only in tests and demos flagged as demo. |
| `if (process.env.NODE_ENV === "development") return mockUser;` in auth | Dev bypass that one config slip exposes | Separate dev seed accounts on a dev database. No auth bypass in code paths. See part 32. |
| `// TODO: implement`, `// TODO: add error handling`, `// TODO: add validation` scattered | Placeholders instead of work | Do it now, or open an issue and reference it: `// TODO(#42): paginate after 500 rows`. No bare TODOs in shipped code. |
| `throw new Error("Not implemented")` in a path the UI calls | Button that crashes | Hide the entry point until implemented. |
| Placeholder text in code: `"Lorem ipsum"`, `"Your text here"`, `"John Doe"`, `"example@example.com"`, `"123 Main St"` | Template leftovers | Real content or an empty state. Grep list in part 35. |
| `return { success: true }` stub for a payment or SMS gateway | Silent fake success on money flows | Real integration against the sandbox (GCash, Maya, PayMongo test keys) or a hard failure. |
| Chart or stat numbers computed from `Math.random()` | Fake dashboard | Real queries. Empty states when there is no data. See part 20 and part 22. |
| Feature flags that are `true` constants | Dead branch | Remove the flag and the dead branch. |
| Test files that assert `expect(true).toBe(true)` | Fake coverage | Real assertions on behaviour, or no test file. |

## 30.13 Generic names in code

Full naming rules are in part 33. Code-level tells:

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `data`, `result`, `res`, `response`, `item`, `obj`, `value`, `temp`, `info` for everything | Name carries no meaning | Name the thing: `payments`, `precinct`, `orNumber`, `voterMatches`. |
| `handleClick`, `handleClick2`, `handleSubmitNew` | Numbered handlers | `handleVoidReceipt`, `handleSearchSubmit`. |
| `isValid`, `flag`, `check`, `status` booleans | Which condition | `hasPaid`, `isRegisteredVoter`, `canVoid`. |
| `getData()`, `fetchData()`, `loadData()` | What data | `fetchBarangayOfficials()`. |
| `newArray`, `filteredArray`, `finalResult`, `updatedData` | Step names, not content | `unpaidBills`, `activeResidents`. |
| Single letters outside tiny lambdas: `const u = await getU(i)` | Minified-looking source | Full words. `i` and `x` only in short loops and callbacks. |
| Hungarian-style suffixes: `userObj`, `nameStr`, `listArr` | Type in the name | `user`, `name`, `residents`. |

## 30.14 Emoji and decoration in code

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Emoji in log messages: `"✅ Connected to DB"`, `"❌ Error:"` | Chat habit | `db connected`, `error:`. |
| Emoji in comments, commit-style headers, section markers | Same | Plain text. |
| Emoji in thrown error messages | Breaks log search and some terminals | Plain text. |
| Emoji in UI strings hard-coded in JS: `toast("Saved! 🎉")` | Banned in system UI | `toast("Saved.")`. Copy rules in part 03. |
| ASCII-art banners printed on server start | Tutorial decoration | One line: `Listening on :3000 (env: production)`. |
| Coloured CLI output with chalk in a library | Imposes on consumers | Colour only in CLIs, and respect `NO_COLOR`. See part 06. |

## 30.15 Legacy and style drift

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `var` in new code | Old tutorials | `const` by default, `let` when reassigned. |
| `==` and `!=` | Coercion bugs | `===` and `!==`. The only accepted `==` is `x == null`. |
| String concatenation for long strings and HTML | Hard to read, XSS risk for HTML | Template literals for strings. For HTML, set `textContent` or use a template element. Never `innerHTML` with user data. |
| `innerHTML = userInput` | XSS | `textContent`, or sanitise with DOMPurify when HTML is required. |
| `eval`, `new Function(string)` | Security hole | Remove. |
| IIFE module pattern in an ES module project | Outdated | ES modules. |
| CommonJS `require` mixed with `import` in one package | Build confusion | Match the package `type`. One module system. |
| Semicolons, quotes and indentation vary by file | Different sessions | Prettier with a committed config. Run on save and in CI. |
| No ESLint, or ESLint with every rule off | Drift unchecked | ESLint with `recommended` plus `typescript-eslint` recommended. Turn on `no-floating-promises`, `no-explicit-any`, `no-console` (warn). |
| `document.write` | Blocks parsing | DOM APIs. |
| `arguments` object | Legacy | Rest parameters `...args`. |
| `.bind(this)` in every constructor | Class boilerplate | Arrow functions or plain functions without `this`. |

## 30.16 Money, phones, dates and IDs in PH projects

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Money as floats: `0.1 + 0.2` on a POS total | ₱ totals off by a centavo, BIR reports do not balance | Store and compute in integer centavos. Format only for display. Round with a stated rule at tax lines. |
| VAT computed per line and summed, then again on total, results differ | No single rounding rule | Pick one rule (per line or per invoice), match what the BIR-registered system or the accountant uses, document it next to `VAT_RATE`. |
| `parseFloat("1,250.00")` returns 1 | Comma in peso input | Strip commas before parsing, or parse with a dedicated money parser. Reject ambiguous input. |
| Phone numbers stored as typed: `0917 123 4567`, `+63 917-123-4567`, `9171234567` | Duplicates and failed SMS | Normalise to E.164 on save: `+639171234567`. Display as `0917 123 4567`. Use `libphonenumber-js` with region `PH`. |
| Phone validation regex `/^09\d{9}$/` only | Rejects `+63` and landlines | Accept `09XXXXXXXXX`, `+639XXXXXXXXX`, `639XXXXXXXXX` for mobile. Landlines need area codes. Validate with libphonenumber. |
| `new Date("09/10/2026")` | Parsed as MM/DD in JS. A Filipino user typing 9 October means 9 October. | Use `<input type="date">` (ISO value) or parse with an explicit format string. Show the expected format next to the field. See part 04 and part 17. |
| `new Date().toISOString().slice(0, 10)` as "today" | UTC date. Wrong for Manila from 00:00 to 08:00. | Compute today in `Asia/Manila`: `new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Manila" }).format(new Date())`. |
| Server and DB in UTC, reports grouped by UTC day | Daily sales for a Manila store split across two days | Group by `AT TIME ZONE 'Asia/Manila'` or convert before grouping. See part 32. |
| Age computed as `year - birthYear` | Off by one for most of the year. Wrong for voter and senior citizen checks. | Compare full dates. Test the day before and on the birthday. |
| ID numbers (PhilSys, TIN, SSS, voter ID) stored as numbers | Leading zeros lost, overflow past 2^53 | Store as strings. Validate the known format. Mask on display. |
| Names forced to ASCII or split into first/last only | Breaks `Ñ`, `ñ`, compound surnames like "Dela Cruz", middle names required on PH forms | Unicode strings. Fields for first, middle, last, suffix (Jr., Sr., III). Do not auto-capitalise after "Dela", "De los", "Mc". |
| String sort for names: `a.localeCompare(b)` without locale | `Ñ` sorts oddly | `new Intl.Collator("es-PH")` or `"fil"`, test with Ñ names. Keep one collator instance. |

```js
// Banned
const total = items.reduce((s, i) => s + i.price * i.qty, 0);
label.textContent = "₱" + total.toFixed(2);

// Use
const peso = new Intl.NumberFormat("en-PH", { style: "currency", currency: "PHP" });
const totalCentavos = items.reduce((s, i) => s + i.priceCentavos * i.qty, 0);
label.textContent = peso.format(totalCentavos / 100);
```

## 30.17 Check

- [ ] No comments that restate the code. Remaining comments explain why.
- [ ] No chat-history comments ("updated", "fixed per request", "new version").
- [ ] No commented-out code.
- [ ] Every `eslint-disable` and `@ts-expect-error` has a reason. No `@ts-ignore`.
- [ ] No single-use helpers or wrappers around built-ins.
- [ ] No classes with only static methods. No factories or strategies for 1–2 cases.
- [ ] No base classes with one subclass.
- [ ] No `any`, `as any`, `Record<string, any>`, `Function` or `{}` types.
- [ ] No `as` casts on unvalidated data. External input validated with a schema at the boundary.
- [ ] Non-null assertions (`!`) rare and justified.
- [ ] No `I`-prefixed interfaces. No interface for 2 props used once.
- [ ] One type per shape. Variants derived with `Pick`/`Omit`.
- [ ] DB and API types generated where a generator exists.
- [ ] `strict: true` in `tsconfig.json`.
- [ ] String unions or `as const` instead of string enums.
- [ ] No empty catch blocks. No catch that only logs and continues.
- [ ] Errors caught only where the code can act.
- [ ] Thrown values are `Error` objects with messages that name the operation and ID.
- [ ] `fetch` calls check `res.ok`.
- [ ] No `|| 0` or `|| []` defaults hiding missing required data.
- [ ] Optional chaining only where types allow null.
- [ ] No `console.log` in shipped code. One logger on the server.
- [ ] Logs carry context and never contain passwords, tokens, OTPs or full ID numbers.
- [ ] No `await` in loops for independent work. `allSettled` where partial failure is acceptable.
- [ ] No floating promises. Lint rule on.
- [ ] No `setTimeout` used to wait for readiness.
- [ ] Network calls have timeouts. Retries are limited with backoff.
- [ ] Every interval, timeout and listener has cleanup.
- [ ] Polling at 60s or slower, paused when the tab is hidden, or replaced by push.
- [ ] Status, role and storage keys come from one definition, not repeated literals.
- [ ] No `utils.ts` dumping ground. Helpers grouped by domain file.
- [ ] Only one helper per job (one money formatter, one date formatter).
- [ ] `Intl.NumberFormat("en-PH", { currency: "PHP" })` for ₱. `Asia/Manila` for dates.
- [ ] `structuredClone`, `crypto.randomUUID`, `URLSearchParams` instead of hand-rolled versions.
- [ ] No fake implementations, fake delays or `return true` stubs.
- [ ] No mock arrays, Lorem ipsum, "John Doe" or `Math.random()` numbers in production code.
- [ ] No bare TODOs. Each TODO references an issue.
- [ ] No emoji in logs, comments, errors or UI strings.
- [ ] No `var`, `==` (except `== null`), `eval` or `innerHTML` with user data.
- [ ] Money in integer centavos. Phones normalised to `+63` E.164. IDs stored as strings.
