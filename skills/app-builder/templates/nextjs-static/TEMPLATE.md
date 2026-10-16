# Next.js site with deliberate rendering

## Fit and inspection

Use when Next.js is the chosen foundation for a content or marketing site. Distinguish static export from a hosted Next runtime; a page that is statically rendered is not necessarily a standalone export.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Use the installed router conventions and keep browser-only interactions scoped. Do not make an entire site client-rendered for one animation.

- If output is a static export, check compatibility of dynamic routes, images, server functions, redirects and asset paths against current official docs.

- Motion, Tailwind, a CMS and a component library are optional. Add only what the selected content and interaction require.

For new visual design, complete the shared short style/reference intake and wait unless already answered or delegated. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Run the actual production build/export, serve its output when possible, inspect routes and responsive composition, and test real navigation and forms.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
