# Native typography and text expansion

Use a hierarchy suited to the task, brand and actual platform. System text styles offer a useful foundation; licensed custom fonts can also work. Do not equate CSS px, iOS pt and Android sp or impose a universal body-size/font-count recipe.

## Choose and ship fonts

Inspect the platform's supported text APIs and the project's font pipeline. System fonts avoid an extra asset but do not automatically make every custom component scale accessibly. Custom fonts need actual platform-supported formats, family/weight registration, language/glyph coverage, license and fallback; WOFF2 is a web format, not a universal native-font packaging instruction.

Load only useful faces/subsets while preserving user names and languages. A variable font can reduce or increase payload depending on the actual file and chosen range. Avoid claiming a fixed file count or size is always optimal.

## Use semantic roles and scaling

Use platform/brand roles for display, headings, body, labels, numeric data or captions. Preserve distinction through scale, weight, spacing and composition. System Dynamic Type and Android text scaling should remain supported through the actual component implementation. For example, a supported SwiftUI body style scales, and a custom font can be defined relative to that role; verify behavior on the deployment target.

Do not disable scaling globally to preserve a screenshot. Use flexible heights, appropriate wrapping, adaptive rows/columns and scroll where content needs it. Test meaningful large accessibility sizes and supported scripts; avoid truncating critical names, amounts or actions. Dynamic font scaling can be nonlinear on some platforms, so “sp multiplied by percentage” is not a universal model.

## Readability and accessibility

Select line height, measure, tracking and weight for the real face/content. There is no universal maximum headline line count or fixed total number of styles. Contrast should be checked against actual surfaces. Light text on dark backgrounds may need optical care, but a required white ban or heavier dark-mode font is not a standard.

Distinguish authored spacing from accessibility override resilience. WCAG text-spacing criteria do not universally require every design to author paragraph line height and letter spacing at the override values. For web-based content, verify it remains usable when relevant user spacing changes are applied; native text has its own platform/settings behavior.

Ensure screen readers receive meaningful text/order and correct language/context when needed. Do not duplicate a visible label through redundant accessibility text or announce animated digits frame by frame.

Inspect actual native output at target widths, supported text sizes, font fallback and relevant localized/long content. Report the devices and settings checked; a source list of point sizes does not establish readable typography.
