---
name: frontend-design
description: "Use when building, extending or redesigning a web page, site, dashboard, form or product screen. Native mobile screens use mobile-design instead."
version: 3.2.0
---

# Web Interface Design

Ship web screens with a clear visual direction, real content and complete behavior, at the level set by rule-07-template-grade-design.

## Steps

1. Read the project first: routes, layout files, theme tokens, existing components, icons, fonts and any `DESIGN.md`.
2. Name the screen's audience, main task and the content that matters most.
3. Pick the direction. Existing approved design system: match it. No brief or reference: choose one, state it in one line, and continue. Ask one style question only if the direction truly cannot be inferred.
4. For a new design system, record it with `KIT/skills/design-spec/SKILL.md`.
5. Start from the matching page recipe in rule-07-template-grade-design. Use the `template-ui-blocks` skill for ready-made sections and chrome.
6. Fill the screen with realistic demo data from one `demo-data` file and neutral demo brands.
7. Build every control with hover, focus, disabled, open and error states, keyboard access and labels.
8. Style only through tokens so Light, Dark and System all work (rule-01-unified-theme-system).
9. Lay out from the content: check narrow, mid and wide widths, long labels and tables.
10. Add motion for feedback and continuity; honor `prefers-reduced-motion`.

## Supporting guidance

| Task | Reference |
|---|---|
| Direction intake and styles | [directions.md](directions.md) |
| Marketing, portfolio, imagery | [marketing-layout.md](marketing-layout.md) |
| Product screens, data, states | [app-ui.md](app-ui.md) |
| Components, assets, themes | [design-systems.md](design-systems.md) |
| Custom controls and popups | [components.md](components.md) |
| Motion and scroll | [motion.md](motion.md) |
| Redesign keeping behavior | [redesign.md](redesign.md) |
| Style examples | [dark dashboard](style-dark-dashboard.md), [glass/aurora](style-glass-aurora.md), [brutalist](style-brutalist.md), [minimal](style-minimalist.md) (only on request) |

## Stack notes

- Keep the project's framework, CSS system (Bootstrap 5.3 or Tailwind), icon set and font pipeline.
- Blade: put repeated chrome in layouts and components. Next.js: keep server and client components separate.
- Add a package only for a concrete need the project cannot cover.

## Checks on request

When the user asks for checks, use `KIT/skills/browser-verification/SKILL.md` for rendered review. `scripts/ux_audit.py` and `scripts/accessibility_checker.py` flag source issues only; they do not prove visual quality. Optional reviews: `KIT/skills/web-design-guidelines/SKILL.md`.

Craft ideas adapted from [taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT); keep attribution when redistributing.

## Before you finish, check

- [ ] Every section of the matching Rule 07 recipe is present or skipped by request.
- [ ] Loading, empty, error and success states exist where data loads.
- [ ] Colors, spacing and shadows come from tokens and work in Light and Dark.
- [ ] Copy makes no fake real-world claims.
- [ ] Unrun browser or build checks are reported as "not run".
