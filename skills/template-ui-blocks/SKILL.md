---
name: template-ui-blocks
description: "Optional reference UI blocks (Tailwind) and a tokens + theme script starter: app shell, KPI cards, charts, data table, forms, auth, landing sections, empty states. Borrow only what fits the chosen design."
version: 4.0.0
---

# Template UI blocks

Optional starting points, not a required look. Use a block only when it fits the design direction you chose; adapt or ignore freely. Blocks use Rule 01 tokens and work in Light / Dark / System.

## Steps

1. Decide your visual direction first. Then borrow blocks that fit (table below), or skip this skill.
2. Detect the project's CSS approach. The blocks are written in Tailwind; for plain CSS, CSS modules or a component library, use them as layout reference and rewrite in the project's style. If the project already has tokens or a theme provider, keep them.
3. If the project has no theme setup, [tokens-and-theme.md](tokens-and-theme.md) has a `tokens.css`, head script and 3-state toggle you can adapt.
4. Demo content, when needed, can come from [demo-data.md](demo-data.md).
5. Wire to real data and keep loading, empty and error states.

## Blocks

| Area | File |
|---|---|
| Theme starter | [tokens-and-theme.md](tokens-and-theme.md) |
| App shell, page header | [tailwind-app.md](tailwind-app.md) |
| KPI + chart, table, form, toast, states | [tailwind-data.md](tailwind-data.md) |
| Landing sections, auth | [tailwind-landing.md](tailwind-landing.md) |

React / Next / Vue / Blade: convert syntax, use the project's theme provider.

## Before you finish, check

- [ ] Only blocks that fit the design were used; nothing added to fill space.
- [ ] The result looks like this product, not a copied template.
