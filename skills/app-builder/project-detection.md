# Project Type Detection

> Analyze user requests to determine project type and template.

## Keyword Matrix

| Keywords | Project Type | Template |
|----------|--------------|----------|
| blog, post, article | Blog | astro-static |
| e-commerce, product, cart, payment | E-commerce | nextjs-saas |
| dashboard, panel, management | Admin Dashboard | nextjs-fullstack |
| ai, chat, bot, llm, rag, agent app | AI / Chatbot App | nextjs-fullstack (AI SDK / Streaming) |
| api, backend, service, rest | API Service (standalone Node) | node-api |
| php, laravel, artisan, livewire | Laravel App | none — see Existing projects below |
| python, fastapi, django | Python API | python-fastapi |
| mobile, android, ios, react native | Mobile App (RN) | react-native-app |
| flutter, dart | Mobile App (Flutter) | flutter-app |
| portfolio, personal, cv | Portfolio | nextjs-static |
| crm, customer, sales | CRM | nextjs-fullstack |
| saas, subscription, stripe | SaaS | nextjs-saas |
| landing, promotional, marketing | Landing Page | nextjs-static |
| docs, documentation | Documentation | astro-static |
| extension, plugin, chrome | Browser Extension | chrome-extension |
| desktop, electron | Desktop App | electron-desktop |
| cli, command line, terminal | CLI Tool | cli-tool |
| monorepo, workspace | Monorepo | monorepo-turborepo |


## Detection Process

```
1. Tokenize user request
2. Extract keywords
3. Determine project type
4. Detect missing information → one round of questions (Questions: follow the global `core-protocol` rule (ask only when the answer changes the build; 1–3 questions in one message for new apps / multi-file work; proceed on simple tasks). Format: `@[skills/brainstorming]`), then `project-planner`
5. Suggest tech stack
```

## Conflict Resolution

When a request matches multiple keywords (e.g. "a CLI to manage my e-commerce products" matches both `cli` and `e-commerce`), resolve in this order:

| Priority | Rule | Example |
|---|---|---|
| 1 | **Platform wins over domain.** A concrete platform (mobile / desktop / cli / extension) outranks a web/business domain (e-commerce, crm, blog). | "CLI to manage e-commerce" → **cli-tool** (e-commerce is the data domain, not the deliverable) |
| 2 | **Head noun wins.** The keyword describing what is being built (grammatical subject) outranks modifiers. | "a **dashboard** for my Shopify store" → **nextjs-fullstack** (dashboard is the thing; Shopify is context) |
| 3 | **Still ambiguous → ask.** If no rule breaks the tie, do not guess. Offer the options as one question (it counts toward the `core-protocol` question budget) and let the user choose. | "an app for my shop" → ask: web, mobile, or desktop? |

## Existing projects (detect before choosing a template)

| Files present | Project | Action |
|---|---|---|
| `next.config.*` | Next.js | Work in the existing structure; backend inside the app is Route Handlers + Server Actions |
| `nuxt.config.*` | Nuxt | Existing structure; `frontend-specialist` handles Vue/Nuxt when the project already uses it |
| `composer.json` + `artisan` | Laravel | No template: work in the existing structure. New Laravel app: `laravel new <name>` or `composer create-project laravel/laravel <name>`. Laravel paths per agent: the ownership table in `C:/Users/Keith/.gemini/config/plugins/ag-kit-v2/agents/orchestrator.md` |
| `pyproject.toml` / `manage.py` | Python (FastAPI / Django) | Existing structure; `python-fastapi` template only for a new service |
| `app.json` + `expo` dependency, or `pubspec.yaml` | Expo / Flutter | Existing structure; `mobile-developer` |

A request that names a feature for an existing project is `/enhance` work (`feature-building.md`), never a new scaffold.
