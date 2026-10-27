---
name: template-ui-blocks
description: "Copy-ready, template-grade UI blocks (Bootstrap 5.3 and Tailwind) for every Rule 07 recipe: tokens + theme script, app shell, KPI cards, charts, data table, forms, auth, landing sections, empty states. Use when building any page or screen."
version: 3.2.0
---

# Template UI blocks

Finished, copy-ready blocks so every page looks like a premium bought template (ThemeForest / Tailwind UI / CoreUI / Metronic level), never a bare page. Every block uses only Rule 01 tokens, works in Light / Dark / System, has hover, focus-visible, active and disabled states, aria labels, reduced-motion support, and a mobile layout. Copy the block, then adapt it; do not rewrite it from memory.

## Steps

1. Pick the Rule 07 recipe for the screen (table below).
2. Detect the project's CSS stack (Bootstrap or Tailwind, and the Tailwind version). If the project already has tokens or a theme provider, keep them and map the block's token names onto them.
3. Once per project, copy [tokens-and-theme.md](tokens-and-theme.md): `tokens.css`, the head script, the 3-state toggle (plus the Bootstrap bridge for Bootstrap).
4. Open the block file for the stack and copy every block the recipe lists, in order.
5. Put all sample content in one file from [demo-data.md](demo-data.md) (₱, Filipino names, Cauayan / Santiago / Tuguegarao branches, fictional brands). Blocks render from it.
6. Wire to real data: swap the demo source for the API or controller data, keep the skeleton, empty and error states.

## Recipe → blocks

| Recipe | Bootstrap 5.3 | Tailwind |
|---|---|---|
| Every page | [tokens-and-theme.md](tokens-and-theme.md) | same |
| Admin dashboard | [bootstrap-app.md](bootstrap-app.md): app shell, page header, KPI row, chart card; [bootstrap-data.md](bootstrap-data.md): table, toast | [tailwind-app.md](tailwind-app.md): setup, shell, page header; [tailwind-data.md](tailwind-data.md): KPI + chart, table, toast |
| Data table page | shell + [bootstrap-data.md](bootstrap-data.md) block 5 (toolbar, table, pagination, empty + skeleton rows) | shell + [tailwind-data.md](tailwind-data.md) block 2 |
| Form page | shell + [bootstrap-data.md](bootstrap-data.md) block 6 (sectioned card, sticky actions) | shell + [tailwind-data.md](tailwind-data.md) block 3 |
| Auth pages | [bootstrap-landing.md](bootstrap-landing.md) block 10 | [tailwind-landing.md](tailwind-landing.md) block 10 |
| Landing page | [bootstrap-landing.md](bootstrap-landing.md) blocks 1-9 | [tailwind-landing.md](tailwind-landing.md) blocks 1-9 |
| States | empty state, toast, skeleton in [bootstrap-data.md](bootstrap-data.md) | same in [tailwind-data.md](tailwind-data.md) |

React / Next / Vue / Blade: keep markup and classes, convert syntax, use the project's theme provider (tokens file, section 5).

## Before you finish, check

- [ ] Every section of the recipe is on the page (or the user asked to skip it).
- [ ] No raw color outside `tokens.css`; charts read `--chart-*` and re-theme on `themechange`.
- [ ] Light, Dark and System all look finished; no flash on reload; the choice persists.
- [ ] Sidebar becomes a drawer below 992px; nothing scrolls sideways at 360px.
- [ ] Every control has hover, focus-visible, active and disabled styling and an accessible name.
- [ ] Loading skeleton, empty state and error state exist for every data block.
- [ ] Sample content comes from one `demo-data.*` file; no lorem ipsum, no real company names.
