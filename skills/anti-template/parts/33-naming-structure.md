---
part: 33
title: Naming and Project Structure
covers: file names, folder names, variable names, function names, class and type names, component names, asset names, project and package names, env var names, barrel files, config sprawl, duplicate files, create-* template leftovers, casing conventions, domain terms, Philippine domain naming
---

# 33 — Naming and Project Structure

Read when: creating files or folders, scaffolding a project, naming anything in code, cleaning a repo before handoff, or reviewing a generated codebase.

A generated repo is easy to spot before anyone opens a file. The tree has `utils/`, `helpers/`, `common/` and `lib/` side by side, a `vite.svg` in `public/`, `App.css` with a spinning logo, and `Button.tsx` next to `ButtonNew.tsx`. This part covers names and the shape of the tree. Code smells inside functions are in part 30 (JS/TS), part 31 (React/Vue), part 32 (backend layers, API and DB naming) and part 29 (CSS class names and CSS files).

## 33.1 File names

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `utils.ts` / `utils.js` holding 20 unrelated functions | Default dumping ground. Name says nothing about contents | Name the file by what it does: `format-peso.ts`, `parse-date.ts`, `slugify.ts`. Move a function next to its only caller if it has one caller. |
| `helpers.js`, `helper.php`, `functions.php` (non-WordPress) | Same as `utils`, one level vaguer | Split by subject: `precinct-lookup.ts`, `receipt-number.ts`. |
| `common.ts`, `shared.ts`, `misc.ts`, `general.ts`, `stuff.js` | No subject. Grows forever | Name the subject. If there is none, the code belongs to its caller. |
| `constants.ts` with every constant in the app | Unrelated values coupled in one file; edits collide | Keep constants in the module that uses them. A shared file only for values used in 3+ modules, named by subject: `vat-rates.ts`. |
| `types.ts` with every type in the app | 600-line file; circular imports | Types live beside the code that owns them: `order.ts` exports `Order`. A shared `types/` only for API contract types. |
| `index.js` as the only file in 15 folders | Editor tabs all read `index.js`; search results unreadable | Name the file after the thing: `Receipt.tsx`, `receipt.service.ts`. Use `index` only where the framework requires it (Next `page.tsx`, route files). |
| `new-dashboard.tsx`, `NewHeader.jsx` | "New" is only true for a week | Name what it is: `SalesDashboard.tsx`. Delete the old one. |
| `final.css`, `final-final.css`, `main-final-v2.css` | Version history in file names | One file. Git holds history. |
| `Header2.tsx`, `style2.css`, `script2.js`, `page1.html` | Numbered copies; nobody knows which is live | Rename to purpose (`CheckoutHeader.tsx`) or delete the unused copy. |
| `ButtonV2.tsx`, `TableNew.tsx`, `FormOld.tsx`, `Card.backup.tsx` | Two versions shipped side by side | Replace in place. If both are needed short term, name by purpose, not by version. |
| `copy of index.html`, `index (1).html`, `logo copy.png` | OS duplicate names committed | Delete. Add a pre-commit check for ` copy`, ` (1)`. |
| `*.bak`, `*.old`, `*.orig`, `*~`, `*.swp` in the repo | Editor and merge leftovers | Delete. Add to `.gitignore`. |
| `test.js`, `test.php`, `test.html` in project root | Scratch file shipped to production | Delete, or move to `tests/` with a real name: `receipt-total.test.ts`. |
| `temp.ts`, `tmp.js`, `scratch.ts`, `playground.tsx` committed | Experiments left in | Delete before commit. |
| `script.js` + `style.css` + `index.html` in a multi-page site | Tutorial names at scale | Name per page or component: `precinct-finder.js`, `precinct-finder.css`. |
| Mixed casing in one folder: `userProfile.tsx`, `User-Card.tsx`, `user_list.tsx` | No convention; generated in separate sessions | Pick one per file type (33.11) and rename all. |
| `MyComponent.tsx`, `MyButton.tsx`, `CustomInput.tsx` | "My" and "Custom" add nothing | `Button.tsx`, `PesoInput.tsx`, `SearchInput.tsx`. |
| `Enhanced*`, `Smart*`, `Super*`, `Advanced*`, `Ultimate*`, `Pro*` prefixes | Marketing words in code | Name the behavior: `SortableTable`, `DebouncedSearch`. |
| `component.tsx` + `component.styles.ts` + `component.types.ts` + `component.constants.ts` + `component.hooks.ts` for a 40-line component | Enterprise template for tiny code | One file until it passes about 200 lines or a second consumer needs a piece. |
| File named after the tool that made it: `gpt-output.ts`, `generated.tsx`, `ai-component.jsx` | Tells the reader how it was made, not what it is | Name by purpose. Generated code (OpenAPI, Prisma) goes in a `generated/` folder with the generator named in a header comment. |
| Spaces or uppercase in URL-served files: `About Us.html`, `Logo.PNG` | Breaks links on case-sensitive hosts; `%20` in URLs | `about-us.html`, `logo.png`. Lowercase, hyphenated. |

## 33.2 Folder structure

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `utils/`, `helpers/`, `lib/`, `common/`, `shared/`, `core/` all present | Six folders for one idea. Nobody knows where to put a new function | Keep at most one of them (`lib/`). Better: put code in the feature that uses it. |
| Empty folders: `hooks/`, `context/`, `services/`, `types/`, `constants/`, `store/` with `.gitkeep` | Scaffolded "for later". Later never comes | Create a folder when the first file needs it. Delete empty ones. |
| `components/common/shared/ui/base/Button.tsx` | 5 levels of nesting for one button | `components/Button.tsx` or `components/ui/Button.tsx`. Max 3 levels under `src/`. |
| `components/` with 80 flat files for every screen | No grouping; screen parts mixed with primitives | Group by feature: `features/pos/`, `features/inventory/`, `features/reports/`. Keep shared primitives in `components/`. |
| Both `features/` and `modules/` and `pages/` and `views/` and `screens/` | Several structure ideas stacked from different templates | Pick one grouping. Pages folder only if the framework routes from it. |
| Layered folders for a 3-endpoint API: `controllers/`, `services/`, `repositories/`, `models/`, `dtos/`, `interfaces/`, `mappers/`, `validators/` | Enterprise layout copied from a Java tutorial | Route file per resource with its query and validation inline. Add layers when a second consumer needs them. Layer smells: see part 32. |
| `src/app/` + `src/pages/` in Next.js with both in use | Two routers; generated from mixed docs | Use one router. Delete the other folder. |
| `styles/` folder with `variables.css`, `mixins.css`, `base.css`, `reset.css`, `utilities.css`, `animations.css`, each under 20 lines | File-per-idea scaffold | One `tokens.css` and one `base.css`. CSS file layout rules: see part 29. |
| Duplicate top-level trees: `client/` and `frontend/`, `server/` and `backend/` and `api/` | Two generations of scaffold in one repo | One of each. Delete the dead tree after checking imports. |
| `docs/` folder with one empty `README.md` | Placeholder | Delete, or write the doc (see part 06). |
| `__tests__/` folder with one snapshot test from the template | Fake test suite | Delete the template test. Add real tests beside the code: `receipt.test.ts`. |
| `.github/workflows/` copied from another project, never run or always failing | CI theater | Delete, or fix it until it passes on the current branch. |
| Laravel/Django app with stock folders untouched plus a custom `app/Helpers/`, `app/Services/`, `app/Utils/` | Framework conventions ignored in favor of a generic template | Use framework places: Laravel Actions, Form Requests, Policies; Django `forms.py`, `services.py` per app only when needed. |
| Monorepo tooling (Turborepo, Nx, `packages/`) for one app | Setup cost with no second package | Single package. Add a workspace when a second deployable exists. |

## 33.3 Variable names

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `data` | Everything is data | Name the thing: `precincts`, `salesByDay`, `voter`. |
| `data2`, `newData`, `finalData`, `updatedData`, `processedData` | Versions of a vague name | Name each stage by content: `rawRows`, `validRows`, `rowsByBarangay`. |
| `response.data.data` | Axios wrapper plus API envelope, never unwrapped | Destructure once: `const { data: orders } = await api.get(...)`, then use `orders`. |
| `info`, `details`, `stuff`, `thing`, `obj`, `object` | No meaning | `studentProfile`, `receiptHeader`, `paymentMethod`. |
| `item` in a loop over `orders` | Loses the noun | `for (const order of orders)`. |
| `temp`, `tmp`, `t`, `x` outside 3-line math | Unknown purpose | `subtotal`, `retryDelayMs`. Single letters only for indexes and short math (`i`, `x`, `y`). |
| `result`, `res`, `ret`, `output`, `val`, `value` for everything | Placeholder name kept | Name what came back: `insertedId`, `matches`, `taxAmount`. `res` only for the HTTP response object. |
| `arr`, `list`, `array`, `items` | Type as name | Plural noun: `products`, `lineItems`. |
| `str`, `num`, `bool`, `int` | Hungarian by type | Name the meaning: `searchQuery`, `quantity`, `isVoid`. |
| `myVar`, `myData`, `myList` | Tutorial names | Real names. |
| `foo`, `bar`, `baz`, `test123` left in shipped code | Sample code not replaced | Replace with real names or delete. |
| Booleans named `flag`, `status`, `check`, `active`, `open`, `loading2` | Unclear true meaning | `isOpen`, `hasPaid`, `canEdit`, `shouldRetry`, `isSubmitting`. |
| Negative booleans: `isNotValid`, `disableNotAllowed`, `noError` | Double negatives in conditions | Positive form: `isValid`, `isAllowed`, `hasError`. |
| `isTrue`, `isFalse`, `isBoolean` | Name of the type, not the state | Name the state: `isVerified`. |
| Numbers without units: `timeout = 5000`, `size = 2`, `delay`, `amount` | Reader guesses ms or s, MB or KB, pesos or centavos | Put the unit in the name: `timeoutMs`, `maxUploadMb`, `totalCentavos`, `amountPhp`. |
| Money in floats named `price` | Rounding bugs; unit unknown | Store integer centavos: `priceCentavos`. Format at display. Peso display rules: see part 04 and part 09. |
| Abbreviations: `usr`, `btn`, `cnt`, `msg`, `idx`, `qty`, `amt`, `desc` mixed with full words | Inconsistent; `desc` could mean description or descending | Full words in names: `user`, `count`, `message`, `description`. Keep universal ones (`id`, `url`, `db`, `i`). |
| Mixed synonyms for one concept: `user`, `member`, `account`, `profile`, `customer` for the same record | Generated in different sessions | Pick one term per concept. Write the glossary in the plan and use it everywhere. |
| `e`, `ev`, `evt`, `err`, `ex` mixed in one codebase | No convention | One name each: `event` for events, `error` in catch blocks. |
| Global mutable names like `window.appData`, `globalState` | Shared state with no owner | Module-scoped variable or a store with a named slice: `cartStore`. |
| Names copied from the prompt: `userRequestedFeature`, `newFeatureData` | Agent names things after the task, not the domain | Domain name: `discountRule`, `enrollmentWindow`. |
| Names that lie after a refactor: `userList` holding a `Map`, `getActiveUsers` returning all users | Code changed, names did not | Rename in the same commit as the change. |

## 33.4 Function and method names

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `processData()`, `handleData()`, `manageData()` | Verb and noun both vague | `computeVatBreakdown()`, `groupVotersByPrecinct()`. |
| `doStuff()`, `doSomething()`, `performAction()`, `executeOperation()`, `runProcess()` | Generic verbs from sample code | Name the effect: `voidReceipt()`, `sendOtp()`. |
| `handleClick`, `handleClick2`, `handleClick3` | Numbered handlers | Name by effect: `handleSaveClick`, `handleVoidClick`, or name the action directly: `saveDraft`. |
| `handleChange` reused as the name for 6 different handlers | Copy-paste from a form tutorial | `handleQuantityChange`, `handleBarangayChange`, or one generic handler keyed by `name`. |
| `onClickHandler`, `clickHandlerFunction`, `handleOnClick` | Redundant words | `handleSaveClick` for the handler, `onSave` for the prop. |
| `handle*` used for non-event functions: `handleUserCreation()` in a service | "handle" means event callback in UI code | Plain verb: `createUser()`. |
| `getData()` that also writes, caches, or navigates | `get` promises no side effects | `loadAndCacheOrders()` or split into `fetchOrders()` and `cacheOrders()`. |
| `get*` for a network call and for a sync field read, both | Reader cannot tell cost | `fetch*`/`load*` for network, `get*` for cheap reads, `compute*`/`build*` for derivations. |
| `isValid()` returning an error message string | Boolean prefix on a non-boolean | `validateOrder()` returning errors; `isValid*` returns `true`/`false` only. |
| `checkUser()` | Check what? Returns what? | `isUserActive()`, `assertCanEditReceipt()`. |
| `init()`, `setup()`, `initialize()`, `bootstrap()` in 5 modules | Generic lifecycle names hide what runs | `registerServiceWorker()`, `loadPrinterSettings()`. |
| `helper()`, `util()`, `format()`, `parse()` with no noun | Collides everywhere | `formatPeso()`, `parsePsgcCode()`. |
| `fetchAndProcessAndSaveData()` | Name admits the function does 3 things | Three functions called in sequence by a named caller. |
| `async` functions named like sync ones: `user()`, `orders()` | Callers forget `await` | Verb for async work: `fetchUser()`, `loadOrders()`. |
| Mixed verb sets: `create`/`add`/`new`/`insert`/`make` for the same operation across modules | No convention | Pick one per operation. Usually `create` for records, `add` for adding to a collection. |
| `deleteItem`, `removeItem`, `destroyItem`, `eraseItem` in one app | Same | One verb. `delete` for records, `remove` for taking from a list without deleting. |
| `useCustomHook`, `useHelper`, `useData`, `useStuff` | Hook named after being a hook | `useCart`, `usePrecinctSearch`, `useDebouncedValue`. |
| Event props named `onButtonClick`, `onClickEvent` on a domain component | Exposes internals | Name the outcome: `onSave`, `onVoid`, `onSelectPrecinct`. |

## 33.5 Class, type and interface names

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `UserManager`, `DataManager`, `AppManager` | "Manager" means "does stuff with" | Name the job: `SessionStore`, `ReceiptPrinter`. Layer smells: see part 32. |
| `*Handler`, `*Processor`, `*Helper`, `*Util`, `*Wrapper` classes | Generic role suffix | Name the responsibility: `OtpSender`, `CsvExporter`, `VatCalculator`. |
| `*Service` for every class, including pure functions | Service as default suffix | Plain exported functions in a module named by subject. Keep `Service` for things that hold connections or config. |
| `AbstractBase*`, `Base*` with one subclass | Inheritance tree for one case | One concrete class or function. Extract a base at the second real subclass. |
| `*Factory`, `*Builder`, `*Provider`, `*Strategy` for a single implementation | Pattern names without the pattern's need | Direct construction. Name patterns only when there are 2+ variants. |
| `IUser`, `IProps`, `IOrderService` | C#/Java prefix in TypeScript | `User`, `OrderServiceOptions`. |
| `TUser`, `UserType`, `UserInterface`, `UserTypeInterface` | Kind of type repeated in the name | `User`. |
| `UserData`, `UserInfo`, `UserDetails`, `UserModel`, `UserEntity`, `UserDTO`, `UserSchema` all for one shape | Six names for one record | One `User` type. Add a second name only for a different shape, named by the difference: `NewUser` (no id), `PublicUser` (no email). |
| `Props` for every component's props, or `ComponentProps` literally | Unsearchable; collides on import | `ReceiptTableProps` when exported. Inline the type when it is used once. Interface bloat: see part 30. |
| Enum named `Status` with values `STATUS_ACTIVE`, `STATUS_INACTIVE` | Prefix repeats the enum name | `OrderStatus.Active` or a union `'active' \| 'void'`. Enum storage in DB: see part 32. |
| Enum values that are display strings: `Status.PENDING = "Pending Approval ⏳"` | Display text in data; emoji in code | Value is a stable key (`'pending'`). Label comes from a label map in the UI layer. |
| Generic type params named `T1`, `T2`, `TData`, `TResult` in app code | Library style in app code | Real types. Generics only in reusable utilities, with meaningful names (`TRow`). |
| Error classes named `CustomError`, `MyError`, `AppError` for everything | One error type; callers cannot branch | Specific names: `ReceiptAlreadyVoidedError`, `OtpExpiredError`. |

## 33.6 Component and UI element names

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `Wrapper`, `Container`, `Box`, `Layout`, `Section`, `Content`, `Inner` as component names | Layout words, not content words | Name the content: `ReceiptSummary`, `PrecinctResults`. Premature primitives: see part 31. |
| `HeroSection`, `FeaturesSection`, `CTASection`, `TestimonialsSection`, `PricingSection` on every landing page | The template's section list became the component list | Name by what the section says: `EnrollmentDates`, `Requirements`, `FeeTable`. If the section is template filler, delete it (part 05, part 24). |
| `Card1`, `Card2`, `StatCard`, `StatCardNew` | Variants by number or age | Name by content: `DailySalesTile`, `LowStockTile`. |
| `ModalComponent`, `ButtonComponent`, `TableComponent` | "Component" suffix on components | `ConfirmVoidDialog`, `ProductTable`. |
| `CustomButton`, `StyledButton`, `MyButton`, `ButtonWrapper` | Several buttons that should be one | One `Button` with variants. Button rules: see part 18. |
| `DashboardPage`, `DashboardView`, `DashboardScreen`, `DashboardContainer` all exist | Container/presenter pattern copied without need | One `Dashboard` route component. Split only when a piece is reused. |
| Component names in the wrong language register: `KabuuangBentaCard` next to `SalesTable` | Mixed languages in identifiers | Code identifiers in English. Filipino belongs in UI copy, not in names (see 33.11). |
| Icon components renamed per use: `DeleteIcon`, `TrashIcon`, `RemoveIcon`, `BinIcon` | Same glyph, four names | Import the icon by its set name once (`Trash2` from the icon set). Icon rules: see part 26. |

## 33.7 Asset and media file names

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `image1.png`, `image2.png`, `img.jpg`, `pic.png` | Unnamed assets | Describe content: `barangay-hall-front.jpg`, `enrollment-step-2.png`. |
| `IMG_2034.jpg`, `DSC00123.JPG`, `Screenshot 2026-09-12 at 10.14.03.png`, `unnamed.png`, `download.jpeg`, `images.jpeg` | Camera and browser defaults committed | Rename to content, lowercase, hyphens. |
| `ChatGPT Image Sep 12, 2026.png`, `Gemini_Generated_Image_x7k2.png`, `DALL·E 2026-...png`, `midjourney_*.png` | Advertises AI images; the image itself is probably a tell (part 26) | Replace with a real photo or screenshot. If an AI image is approved, still name it by content. |
| `hero-bg.jpg`, `hero-bg-new.jpg`, `hero-bg-final.jpg` all present | Versions in names | Keep one. Delete the others. |
| `logo.png`, `logo2.png`, `logo-new.png`, `logo-white.png`, `logo-white-final.png` | Nobody knows which is current | `logo.svg`, `logo-on-dark.svg`. Two files max per logo mark. |
| Seal or emblem files named `seal.png` with no LGU or office name | Unclear source; easy to swap a fake seal in | `seal-municipality-of-<name>.png`, stored with the source noted in the PR. Seal rules: see part 09. |
| Uppercase extensions and mixed formats: `Photo.JPG`, `photo.jpeg`, `photo.jpg` | Inconsistent; case-sensitive hosts break | Lowercase, one extension per format (`.jpg`). |
| Placeholder assets left: `placeholder.png`, `avatar-placeholder.svg`, `sample.pdf`, `dummy.jpg` | Demo content shipped | Replace with real content or remove the element. |
| Fonts committed as `font1.woff2`, `Inter-VariableFont_slnt,wght.ttf` unused | Downloaded and forgotten | Keep only fonts that are referenced. Name by family and weight: `source-sans-3-400.woff2`. |

## 33.8 Project, package and repo names

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `"name": "vite-project"`, `"my-app"`, `"my-react-app"`, `"nextjs-app"`, `"frontend"`, `"project"` in `package.json` | Scaffold default never changed | Project slug: `"name": "brgy-sanroque-portal"`. |
| `"version": "0.0.0"` or `"1.0.0"` forever | Never versioned | Bump on release, or leave `0.x` and remove the field from the plan's talk of "v1". |
| `"description": "A modern, scalable web application built with..."` | Hype in metadata | One plain line: `"POS for a 3-branch hardware store."` Or delete. |
| `"author": ""`, `"keywords": []`, `"license": "ISC"` defaults | npm init leftovers | Fill with the real owner and license, or remove the empty fields. |
| Repo names: `project-final`, `website-v2`, `new-site`, `test-app`, `keith-website-2026-final` | Version and state in the name | Client and purpose: `mnhs-enrollment`, `keith-portfolio`. |
| `<title>Vite + React + TS</title>`, `<title>React App</title>`, `<title>Create Next App</title>` | Template title shipped | Real page title. Title wording: see part 08. |
| `manifest.json` with `"short_name": "React App"`, `"name": "Create React App Sample"` | CRA leftovers | Real app name, or delete the manifest if there is no PWA. |
| Database named `test`, `mydb`, `database`, `laravel` | Default DB name in production | Project name: `pos_prod`, `pos_dev`. DB schema naming: see part 32. |

## 33.9 Environment variable names

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `REACT_APP_*` variables in a Vite project | Copied from CRA docs; never loaded | `VITE_*` for client values in Vite; `NEXT_PUBLIC_*` in Next. Check the framework before naming. |
| `API_KEY`, `SECRET`, `TOKEN`, `KEY` with no service name | Collides when a second service arrives | `PAYMONGO_SECRET_KEY`, `SEMAPHORE_API_KEY`, `SUPABASE_SERVICE_ROLE_KEY`. |
| Secrets under a client-exposed prefix: `VITE_DB_PASSWORD`, `NEXT_PUBLIC_SECRET_KEY` | Name shows it ships to the browser | Server-only name with no public prefix. Secret handling: see part 32. |
| `.env.example` listing 25 variables the code never reads | Copied from another project | List only variables the code reads. One comment line per variable saying where to get it. |
| Mixed styles: `apiUrl`, `API_URL`, `Api_Url` | No convention | `SCREAMING_SNAKE_CASE` for all env vars. |
| `.env`, `.env.local`, `.env.development`, `.env.dev`, `.env.production`, `.env.prod` all present | Two naming schemes; unclear which loads | The framework's documented set only. Delete the rest. |

## 33.10 Barrel files and imports

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `index.ts` in every folder with `export * from './x'` | Barrel habit; slows builds, hides dead code, causes circular imports | Import from the file directly: `import { Button } from '@/components/Button'`. A barrel only at a real package boundary. |
| Barrel that re-exports 40 components into one import | Tree-shaking and HMR suffer; one change reloads everything | Direct imports. |
| `export default` and named export of the same thing | Two ways to import one symbol | Named exports only, except where the framework needs default (Next pages, Vue SFCs). |
| `import * as Utils from './utils'` | Namespace import of a dumping ground | Named imports from subject files. |
| `../../../../components/Button` | Deep relative paths | One alias (`@/`) set in `tsconfig`/`vite.config`. Use it everywhere or nowhere. |
| Both `@/`, `~/`, `src/` and relative paths used for the same folder | Four styles for one path | One alias. Fix with a codemod or search and replace. |
| Unused imports in most files | Generated then edited | Run the linter's unused-imports rule and fix before commit. |
| Circular import between `utils` and `constants` | Barrels plus dumping grounds | Break by moving the shared piece to the module that owns it. |

## 33.11 Casing and language conventions

Pick one convention per kind of name, write it in the plan or README, and apply it to every file.

| Kind | Common convention | Tell when mixed |
|---|---|---|
| React/Vue component files | `PascalCase.tsx` / `PascalCase.vue` | `userCard.tsx` next to `UserList.tsx` |
| Other TS/JS files | `kebab-case.ts` (or `camelCase.ts`, pick one) | `format_peso.ts` next to `parseDate.ts` |
| CSS files | `kebab-case.css` or matching the component | `Header.css`, `footer_styles.css`, `navBar.css` |
| Variables, functions | `camelCase` | `user_name` in JS |
| Constants | `SCREAMING_SNAKE_CASE` for true constants only | `const API_RESPONSE = await ...` |
| Types, classes, components | `PascalCase` | `type orderItem` |
| DB tables and columns | `snake_case` | `createdAt` in SQL, `created_at` in API, `CreatedAt` in UI. Mapping rules: see part 32. |
| URLs and routes | `kebab-case`, lowercase | `/Enrollment/NewStudent`, `/enrollment_form` |
| Env vars | `SCREAMING_SNAKE_CASE` | `viteApiUrl` |
| CSS classes | project convention (BEM or prefix) | see part 29 |

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Filipino or Taglish identifiers mixed with English: `getBarangayNgUser()`, `kabuuan`, `listahanNgBotante` | Mixed register in code; unreadable to other devs | English identifiers. Keep official Philippine terms that have no English equal as-is (33.12). |
| Transliterated or translated official terms: `villageCaptain` for barangay captain, `ballotPlace` for precinct | Agent translated a proper term | Use the official term: `barangay`, `punongBarangay`, `precinct`, `clusteredPrecinct`, `sangguniang`. |
| Emoji or non-ASCII in identifiers, file names or branch names | Breaks tools and search | ASCII names. Emoji in code: see part 30. |

## 33.12 Domain terms (generic nouns vs real nouns)

Generated code names things by software role (`entity`, `record`, `item`, `resource`). Real code uses the client's nouns. Use the terms the client, the forms and the law use.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `entity`, `record`, `resource`, `object`, `element` as the main noun | Framework words replace domain words | `voter`, `precinct`, `receipt`, `enrollee`, `resident`, `permit`. |
| `Item` table in a POS | Unclear if product, line item or stock unit | `product`, `saleLine`, `stockMovement`. |
| `Transaction` for sale, refund, void and stock-in alike | One vague noun for several things | `sale`, `refund`, `void`, `stockIn`, each named. |
| `location`, `area`, `region` for Philippine addresses | Loses the real levels | `region`, `province`, `cityMunicipality`, `barangay`, `purokSitio`, `street`. Store PSGC codes with names: `barangayPsgc`. Address display: see part 09. |
| `brgy`, `bgy`, `barangay`, `village` mixed across files | Four spellings of one concept | `barangay` in code. `Brgy.` only as a display abbreviation. |
| `city` for a municipality | Wrong level; municipalities are not cities | `cityMunicipality` or separate `lguType: 'city' \| 'municipality'`. |
| `receiptNo`, `invoiceNumber`, `orNumber`, `siNo` mixed for BIR documents | Different BIR documents conflated | Separate fields named for the document the client issues: `officialReceiptNumber`, `salesInvoiceNumber`. Receipt wording: see part 09. |
| `taxId`, `tin_no`, `TIN`, `taxNumber` | Several names for the TIN | `tin` in code, "TIN" in UI. |
| `phone`, `mobile`, `contact`, `cellphone`, `phoneNumber` mixed | Same field, five names | `mobileNumber`, stored in E.164 (`+639...`). Phone input rules: see part 17. |
| `studentId`, `lrn`, `learnerRef` mixed for the LRN | Official identifier renamed | `lrn` for the DepEd Learner Reference Number, `studentId` only for a school's own number. |
| `voterId`, `vin`, `voterNumber` mixed | Same | Match the COMELEC field the data comes from and keep that name everywhere. |
| `user` for citizens, residents, applicants, staff and admins alike | Roles collapsed | `resident`, `applicant`, `staff`, with `user` only for the login account. |

## 33.13 Config sprawl

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `.eslintrc.json` and `eslint.config.js` both present | Old and new config formats; one is ignored | The format the installed ESLint version reads. Delete the other. |
| `.prettierrc`, `.prettierrc.json`, `prettier.config.js` together | Same | One file. |
| `jsconfig.json` and `tsconfig.json` in one app | JS and TS configs fighting | `tsconfig.json` only if the project is TS. |
| `tsconfig.json` + `tsconfig.app.json` + `tsconfig.node.json` + `tsconfig.base.json` + `tsconfig.build.json` for a small app | Template split kept and extended | Keep the scaffold's split if the tool needs it; do not add more. |
| `babel.config.js` in a Vite or Next (SWC) project | Babel config nothing reads, or one that disables the fast compiler | Delete unless a plugin needs Babel. |
| `postcss.config.js` with plugins for a project without PostCSS use | Scaffold default | Delete if no plugin runs. |
| `tailwind.config.js` `content` paths pointing to folders that do not exist, or a Tailwind v3 config in a v4 project | Copied config | Match the installed version. Paths that exist. Tailwind config abuse: see part 29. |
| `vercel.json`, `netlify.toml`, `render.yaml`, `Procfile`, `Dockerfile`, `docker-compose.yml` all present for one host | Deploy configs for hosts never used | Keep the config for the actual host. Delete the rest. |
| Dockerfile and compose for a static site | Container for HTML files | Static host. Add Docker when a server process exists. |
| `Makefile`, `justfile`, npm scripts and shell scripts duplicating the same commands | Four ways to run one task | npm scripts (or the stack's standard runner). One place. |
| `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb` in one repo | Different installs by different sessions | One package manager. Delete other lockfiles. Add `"packageManager"` to `package.json`. |
| `.editorconfig`, `.nvmrc`, `.node-version`, `.tool-versions` all set to different Node versions | Conflicting sources of truth | One version file. Match `engines` in `package.json`. |
| `.env` committed | Secrets in git | `.gitignore` it. Commit `.env.example`. Rotate anything exposed. |
| `.gitignore` from a different stack (Python ignore file in a Node repo, or 400 lines covering every OS and IDE) | Copied wholesale | Stack template from the tool's own `init`, plus project-specific lines. |
| `components.json` (shadcn) with no shadcn components used | Setup run, then abandoned | Delete, or use the components. shadcn default look: see part 31. |

## 33.14 Duplicate and dead files

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `Button.jsx` and `Button.tsx` side by side | Migration half done | Finish the migration. Delete the old file. |
| `api.js` and `api.ts`, `utils.js` and `utils.ts` | Same | Same. |
| `styles.css` and `style.css` both imported | Two global files, conflicting rules | One. Merge and delete. |
| `index.html` and `index2.html`, `home.html` and `index.html` with the same content | Draft copies deployed and reachable | Delete the copies. Redirect old URLs if they were public. |
| `old/`, `backup/`, `archive/`, `deprecated/`, `unused/` folders | Git already keeps history | Delete. Retrieve from git if needed. |
| Commented-out whole files or 200-line commented blocks | Dead code kept "just in case" | Delete. Commit message notes what was removed. |
| Two components that render the same thing with small prop differences (`UserCard`, `MemberCard`, `ProfileCard`) | Each session made its own | One component with the needed props. |
| Routes defined but never linked (`/test`, `/demo`, `/playground`, `/components`) | Dev pages shipped | Delete, or guard them behind a dev-only flag. |
| Mock data files (`mockData.ts`, `dummy.json`, `seed-fake.json`) imported by production screens | Demo data in production | Real API calls. Mock data only in tests and stories. Fake implementations: see part 30. |
| Unused dependencies in `package.json` (installed "in case") | Bloated install; security noise | Run `npx depcheck` or `npx knip`. Remove unused packages. |
| Unused exports across the codebase | Dead API surface | Run `npx knip` or `ts-prune`. Delete or unexport. |

## 33.15 create-* template leftovers

Scaffolds ship demo files. Leaving them in shows the project was never cleaned. Check every item for the stack you used.

| Stack | Leftover | Action |
|---|---|---|
| Vite (React/Vue/Svelte) | `public/vite.svg`, `src/assets/react.svg`, `src/assets/vue.svg`, `src/assets/svelte.svg` | Delete. Replace favicon with the project's. |
| Vite React | `App.css` with `.logo`, `.logo.react`, `@keyframes logo-spin`, `.read-the-docs`, `.card { padding: 2em }` | Delete the file or clear it. Remove its import. |
| Vite React | `index.css` defaults: `:root { color-scheme: light dark; color: rgba(255,255,255,0.87); background-color: #242424; font-family: Inter, system-ui... }`, `a { color: #646cff }`, `button { border-radius: 8px; background-color: #1a1a1a }` | Replace with project tokens. These defaults are why many Vite apps ship a dark gray background and indigo links. |
| Vite React | `count is {count}` button, "Edit `src/App.tsx` and save to test HMR", "Click on the Vite and React logos to learn more" | Delete. |
| Vite | `<title>Vite + React + TS</title>`, `<link rel="icon" href="/vite.svg">` | Real title and icon. |
| Vite Vue | `HelloWorld.vue`, `TheWelcome.vue`, `WelcomeItem.vue`, `components/icons/IconCommunity.vue`, `IconDocumentation.vue`, `IconEcosystem.vue`, `IconSupport.vue`, `IconTooling.vue`, `base.css` with `--vt-c-*` vars, `main.css` | Delete. Remove references. |
| Create React App | `logo.svg`, `logo192.png`, `logo512.png`, `reportWebVitals.js`, `setupTests.js`, `App.test.js` ("renders learn react link"), `manifest.json` ("React App"), `robots.txt` with the robotstxt.org comment | Delete or replace. Consider moving off CRA; it is deprecated. |
| Next.js | `public/next.svg`, `vercel.svg`, `file.svg`, `globe.svg`, `window.svg` | Delete. |
| Next.js | `page.tsx` template: "Get started by editing `app/page.tsx`", "Save and see your changes instantly", Deploy now / Read our docs buttons, footer links Learn / Examples / Go to nextjs.org | Replace with real content. |
| Next.js | `Geist` and `Geist_Mono` loaded in `layout.tsx` but not the chosen fonts; `metadata = { title: "Create Next App", description: "Generated by create next app" }` | Real fonts (see part 13) and real metadata (see part 08). |
| Next.js | `globals.css` with the template's `--background`/`--foreground` and `prefers-color-scheme: dark` block unchanged | Replace with project tokens. Theming rules: see part 34. |
| Next.js / CRA | Default `favicon.ico` | Project favicon. |
| Laravel | `welcome.blade.php` still at `/`, stock `README.md` about Laravel, `resources/js/bootstrap.js` with commented Echo/Pusher config, `ExampleTest.php` | Replace the route. Rewrite the README (part 06). Delete example tests and unused scaffolding. |
| Laravel Breeze/Jetstream | Default "Dashboard — You're logged in!" page, Laravel logo component `ApplicationLogo` | Replace text and logo. |
| Django | "The install worked successfully! Congratulations!" page still reachable, empty `tests.py` in every app | Add real URL routes. Delete empty test files or write tests. |
| Angular | `app.component.html` placeholder (Angular logo, "Hello, {title}", resource links), `app.component.spec.ts` checking the title | Replace. Update or delete the spec. |
| Astro / SvelteKit | `Welcome.astro`, `astro.svg`, `background.svg`; "Welcome to SvelteKit" page | Delete or replace. |
| Expo / React Native | `app/(tabs)/explore.tsx`, `HelloWave`, `ParallaxScrollView`, `ThemedText`, `ThemedView`, `Collapsible`, `partial-react-logo.png` | Delete the demo tabs and components. |
| Bootstrap starter template | "Hello, world!" `<h1>`, jumbotron copy, `album`/`carousel` example markup copied from getbootstrap.com examples | Replace. Visual template tells: see part 10. |
| Any | `README.md` still the scaffold's ("This template provides a minimal setup...", "Expanding the ESLint configuration") | Rewrite (part 06). |
| Any | `LICENSE` with the wrong name, wrong year, or MIT on a client project the client owns | Correct owner and year, or remove for private client work. |
| Any | Empty `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` on a solo or client repo | Delete. Docs boilerplate: see part 06. |

## 33.16 Check

- [ ] No file named `utils`, `helpers`, `common`, `misc`, `shared`, `stuff`, `temp`, `tmp`, `test` (outside tests), or `scratch`.
- [ ] No `new`, `old`, `final`, `copy`, `backup`, `v2` or trailing numbers in names; no `*.bak`, `*.orig`, `*.swp`, ` (1)` files.
- [ ] No empty folders or `.gitkeep` placeholders for unused folders.
- [ ] Folder depth under `src/` is 3 or less; only one of `utils/`, `helpers/`, `lib/`, `common/`, `shared/`, `core/` exists.
- [ ] One grouping scheme (features or pages), not several.
- [ ] Layered backend folders only where more than one consumer uses a layer.
- [ ] No variable named `data`, `data2`, `newData`, `info`, `item` (for a known noun), `temp`, `obj`, `arr`, `stuff`, `foo`.
- [ ] `response.data.data` unwrapped once and renamed.
- [ ] Booleans start with `is`, `has`, `can`, `should`, and are positive.
- [ ] Numeric names carry units (`Ms`, `Mb`, `Centavos`, `Px`).
- [ ] Money stored as integer centavos with the unit in the name.
- [ ] One term per domain concept, listed in the plan's glossary.
- [ ] No `handleClick2`, `doStuff`, `processData`, `performAction`, `handleData`.
- [ ] `get` functions have no side effects; network functions use `fetch`/`load`.
- [ ] `is*` functions return booleans.
- [ ] Hooks named by what they provide, not `useData`.
- [ ] No `Manager`, `Handler`, `Helper`, `Util`, `Processor` classes without a specific job in the name.
- [ ] No `I` prefix on interfaces, no `Type`/`Interface` suffix.
- [ ] One type per record shape; variants named by their difference.
- [ ] Enum values are stable keys, not display strings.
- [ ] No `Wrapper`, `Container`, `Section`, `ModalComponent`, `CustomButton`, `Enhanced*`, `Smart*` component names.
- [ ] Section components named by content, not by template slot.
- [ ] Assets named by content in lowercase kebab-case; no `IMG_`, `Screenshot`, `unnamed`, `ChatGPT Image`, `Gemini_Generated_Image`.
- [ ] One current logo file per variant.
- [ ] `package.json` `name`, `description`, `author` are real; no `vite-project` or `my-app`.
- [ ] Env vars use the framework's prefix; secrets have no public prefix; each var names its service.
- [ ] `.env.example` lists only variables the code reads.
- [ ] No barrel `index.ts` re-exporting whole folders.
- [ ] One import alias style; no `../../../../`.
- [ ] No unused imports, dependencies or exports (`knip` or `depcheck` clean).
- [ ] Casing convention written down and followed for files, code, DB, routes, env vars.
- [ ] Code identifiers in English; official Philippine terms kept as-is (`barangay`, `lrn`, `tin`, `precinct`).
- [ ] Address fields follow region, province, city/municipality, barangay, purok/sitio, with PSGC codes.
- [ ] One ESLint config, one Prettier config, one lockfile, one Node version file.
- [ ] Deploy configs only for the actual host.
- [ ] No duplicate `.js`/`.ts` pairs, no `index2.html`, no `old/` folders.
- [ ] No dev-only routes (`/test`, `/demo`, `/playground`) reachable in production.
- [ ] No mock data imported by production code.
- [ ] Every create-* leftover in 33.15 for the chosen stack removed or replaced.
- [ ] README, LICENSE and title are the project's, not the scaffold's.
