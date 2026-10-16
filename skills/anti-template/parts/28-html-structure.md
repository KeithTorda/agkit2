---
part: 28
title: HTML semantics and structure
covers: landmarks, headings, lists, tables, controls, head, inline content, IDs, SVG, embeds, email, validity
---

# 28 - HTML semantics and structure

Read when writing markup or reviewing rendered HTML. Use semantics to expose content relationships and behavior. An expressive design does not require weak structure, and semantic HTML does not require a plain aesthetic.

## Choose elements by meaning

Use a main region, appropriate header/footer/navigation landmarks, headings that reflect the content hierarchy, lists for related items, tables for tabular relationships, and form controls for input. A `<section>` represents a thematic grouping, usually with a heading; a generic styling wrapper can remain a `<div>`. Do not add landmarks to every visual box.

Wrapper count is not a correctness metric. Remove redundant layers when they complicate layout or semantics; retain wrappers needed for masks, overlap, animation, responsive grouping, or component behavior. A fixed maximum nesting depth can damage legitimate composition and is not required here.

Use headings for actual headings and style size separately. A price, label, or slogan does not automatically become an `<h2>` because it is large. Inline emphasis should convey meaning and match the brand; there is no "one bold phrase" quota. Preserve sensible reading order when CSS moves items.

## Links, buttons, and forms

Navigation needs a real `href`; actions need a button or a correctly implemented specialized control. Avoid nested links and buttons. An anchor with `href="#"` is not a useful placeholder for a production action. In forms, set button type explicitly and associate labels with controls. Use fieldsets/legends, autocomplete, hints, and error relationships as appropriate.

Build accordions, menus, tabs, and dialogs with native behavior or accessible tested primitives, then verify the full interaction. Adding a `role` alone does not supply keyboard behavior. Avoid redundant or contradictory ARIA.

## Tables and media

Use table structure and header associations for comparison data. Provide an accessible name or caption where needed. Sort controls must be focusable and expose state. Do not use layout tables for normal web layout; email clients are a distinct environment where presentation tables can be appropriate and should be marked accordingly.

Images need alt attributes with meaningful text or an empty value for decoration. Set dimensions or aspect ratio to reduce shift. SVGs need a useful viewBox when scaling, unique IDs for referenced gradients/masks in repeated components, and an appropriate accessible name or decorative hidden state. Gradient SVGs and complex vectors are valid design assets.

Iframes need meaningful titles, suitable permissions/sandbox restrictions for their content, safe loading behavior, and an accessible alternative when the embedded tool is essential. Keep captions, transcripts, and relevant controls for media.

## Head, IDs, and embedded content

Set actual page title, character encoding, language, responsive viewport that allows zoom, and relevant metadata. Public shareable pages may need canonical/OG information; private app pages need suitable indexing controls. Do not publish template titles or preview hosts by accident.

IDs must be unique in the rendered document and match their labels, anchors, and ARIA references. Use framework ID helpers where repeated components or server rendering make collisions likely. Data attributes can be useful behavior hooks; do not force every state into generic class names.

Inline styles can encode dynamic values or intentionally scoped presentation. Inline scripts can have valid use under the project's security model. Check content security policy, escaping, injection risks, and framework conventions rather than imposing an absolute inline-content ban. Never insert untrusted HTML without an appropriate sanitization strategy.

## Review

Inspect the rendered DOM rather than only component source. Check validity, duplicate IDs, invalid nesting, semantic outline, names, controls, focus, links, and media alternatives. Use relevant validators or accessibility tools when useful. Markup validity alone does not establish good behavior or visual quality.
