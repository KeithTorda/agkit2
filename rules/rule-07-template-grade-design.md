---
name: rule-07-template-grade-design
version: 4.0.0
priority: P2
trigger: glob
globs: "**/*.html, **/*.css, **/*.scss, **/*.tsx, **/*.jsx, **/*.vue, **/*.svelte, **/*.astro, **/*.blade.php, **/*.dart, **/components/**, **/resources/views/**, **/app/**/page.*, **/pages/**"
description: Rule 07 - design guide. UI should feel finished and intentional. You choose the visual direction; these are suggestions, not a checklist.
---

# RULE 07 - DESIGN GUIDE

This is guidance, not a checklist. You have creative freedom. Use judgment about what fits the product, the audience and the request.

## The bar

- The result should feel finished and intentional, something the user would be happy to show a client. Not a bare wireframe, and not cluttered either.
- Pick a clear visual direction for the product and commit to it. Restraint is a valid choice; so is bold. Match the purpose.
- An existing project's design wins. Fit in with what is there before adding anything new.
- If the user asks for a specific style (minimal, bold, playful, corporate), follow that.

## Things that usually help

Use what fits; skip what does not.

- Clear hierarchy: one obvious primary action per screen, readable type, good spacing.
- Consistent components and one icon set.
- Handle the states people will actually hit (loading, empty, error) in a way that looks designed.
- Hover and focus feedback on interactive elements; subtle motion that respects `prefers-reduced-motion`.
- Realistic content instead of "Lorem ipsum" or "Item 1, Item 2" when demo data is needed (Philippine context is a good default: peso amounts, local names).
- Colors and spacing from the project's tokens so Light and Dark both work (Rule 01).

## Ideas, not requirements

Common sections for reference only. Do not add a section just because it is on this list.

- Landing page: navbar, hero, features, social proof, pricing, FAQ, CTA, footer.
- Dashboard: sidebar or top nav, page header, key numbers, a main chart or table, recent activity.
- Data table: search/filters, table with status badges and row actions, pagination.
- Form: grouped fields with helper text, inline validation, clear save/cancel.
- Auth: focused form card, optional brand visual.

`KIT/skills/template-ui-blocks/SKILL.md` has ready blocks if they help. Adapt them freely.

## Avoid

- Filling space with decoration, gradients or sections that serve no purpose.
- The same generic "AI template" look on every project. Give each product its own character.
