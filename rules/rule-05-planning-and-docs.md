---
name: rule-05-planning-and-docs
version: 3.0.0
priority: P1
trigger: always_on
description: Rule 05 - every plan is a .md file in docs/plans; plan format; documentation minimum.
---

# RULE 05 — PLANNING AND DOCS

## Every plan is a file

- Save plans to `docs/plans/<yyyy-mm-dd>-<short-slug>.md` in the project (create the folder if needed). If the user names another location, use it.
- The chat reply gives a 3–6 line summary and the file path. The file is the source of truth.
- Update the same file when the plan changes; add a short "Changes" note at the bottom instead of creating `plan-v2-final.md`.

## Plan format

```markdown
# <Title>
Date: <yyyy-mm-dd>   Status: Draft | Approved | Done

## Goal
What will be true when this is finished (1–3 sentences).

## Scope
In: ...
Out: ...

## Decisions
| Decision | Choice | Why |

## Steps
| # | Step | Owner agent | Files/areas | Done when |

## Risks
| Risk | Impact | Mitigation |

## Open questions
- ...
```

- "Done when" is checkable ("POST /api/v1/sales returns 201 and creates an outbox row"), not vague ("sales works").
- Small change (one feature, under ~1 day): use `/plan` — one file in this format.
- New system or large module: use `/proplan` — the numbered document set (goals, requirements, architecture, data model, API, UX, security, quality, operations, roadmap, risks).
- New systems follow `rule-04-system-integration`; the plan's architecture section states table ownership and sync design.

## Project docs minimum

Every project keeps these up to date when behavior changes:

- `README.md`: what it is, requirements, setup, env variables (names only), how to run, how to deploy.
- `CHANGELOG.md` (if the project has releases): one line per user-visible change.
- `docs/api/` or `05-api.md` when the project exposes an API.

Write docs from the actual code. Mark features that do not exist yet as "Planned".

## Before you answer, check

- [ ] The plan is saved at `docs/plans/<yyyy-mm-dd>-<slug>.md` and the chat links it.
- [ ] Every step has an owner agent and a checkable "Done when".
- [ ] README/API docs match any behavior I changed.
