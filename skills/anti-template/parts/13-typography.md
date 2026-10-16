---
part: 13
title: Typography and readable expression
covers: font selection, hierarchy, type scale, leading, line length, wrapping, numerals, loading, bilingual content
---

# 13 - Typography and readable expression

Read when choosing fonts or refining type. Begin with the user's style and references, actual content, language support, and existing product system. A familiar font is not a design failure; an unusual font is not automatically distinctive in a useful way.

## Choose roles, then fonts

Select type for the experience: editorial, technical, welcoming, expressive, institutional, luxurious, playful, or another chosen direction. Test the actual headline, body text, numbers, names, and controls. Check character coverage, licensing, available weights, visual fit, and loading cost.

Use as many font families and weights as the composition needs, with clear roles. A display face, readable text face, and mono face can be valid. One well-chosen family may be sufficient. Do not impose a universal font-count limit or reject Inter, system fonts, Space Grotesk, or any other face by name.

Load only resources used by the design. A variable font can reduce payload but still needs inspection of its actual file and subsets. Preserve characters needed for names and languages, including accents. If web fonts fail, the fallback should remain readable and keep controls usable.

## Hierarchy, size, and rhythm

Build a hierarchy from content importance and the selected composition. A large hero headline is appropriate for some campaigns; a compact utility heading is appropriate for a task screen. Do not shrink display type merely to satisfy a line-count rule. Four lines can be intentional and beautiful; one oversized unbalanced line can be wrong.

Choose line height and measure by reading actual text. Dense numerical UI, prose, short labels, and display headings need different treatment. A readable paragraph measure is a starting point rather than a hard character count. Use responsive sizing that retains user zoom and minimum readability.

Use letter spacing and case deliberately. Wide uppercase labels can reinforce an identity; long all-caps paragraphs may impair reading. Tight display tracking can create impact but must not collide or clip. Italics, bold, underline, and gradients can support expression; ensure links and emphasis remain distinguishable.

## Wrapping and alignment

Let text adapt to content and viewport. Use `text-wrap: balance` or `pretty` where supported if it improves the result, with normal wrapping as a useful fallback. A deliberate `<br>` in a controlled campaign headline is fine; revisit it for mobile and localization instead of accumulating viewport-specific break hacks.

Long names, translated labels, email addresses, codes, and prices need explicit overflow behavior. Do not clip essential text with fixed-height boxes. A truncated table field needs a way to reveal and copy the complete value. Use `overflow-wrap` where it helps; avoid breaking a currency amount or identifier into unreadable fragments.

Centering, left alignment, right alignment, and justified display treatment can all serve the direction. Long body text usually benefits from a stable reading edge. The visual hierarchy should correspond to semantic headings; a visually large price does not need to be a heading.

## Numerals and accessibility

Use tabular numerals for aligned data where they improve comparison; proportional numerals may fit narrative text. Preserve meaningful precision, separators, currency, and units. Use semantic markup and accessible names rather than encoding essential words solely in an image.

Allow zoom and text spacing changes. Keep visible focus and useful link distinctions. Test font fallback, delayed loading, multiline buttons, and diacritics. Mixed-language content should retain natural phrasing and appropriate language metadata, rather than forcing English-only line lengths.

## Review

Inspect desktop and relevant small sizes with real content. Judge headline composition, hierarchy, spacing, contrast, reading comfort, glyph rendering, and fallback behavior. Fix observed typography problems without enforcing arbitrary font or headline quotas.

Inspect supporting labels, chart axes, status explanations and secondary actions at actual render size as well as display text. Quiet styling should preserve their usefulness. If a dense screen becomes microcopy-heavy, revisit available content space and hierarchy before shrinking more text; use the app UI guidance for task/data priorities. Passing layout and interaction checks does not establish reading comfort.
