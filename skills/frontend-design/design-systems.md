# Design systems, stack, and themes

Read when selecting or extending components, fonts, icons, or theme support. Start with [SKILL.md](./SKILL.md) and inspect the project's real dependency manifest and styling system.

## 2.A Existing systems and named references
Use and extend the system already installed. If the user explicitly requests a particular component system or a platform contract requires it, use its supported implementation and verify compatibility. Do not infer an installation requirement from "Microsoft-like", "Google feel", "Linear-style", or another visual reference. Ask what quality matters only when unclear; typography and layout inspiration often need no package.

Examples of systems one may deliberately select include Fluent, Material, Carbon, Polaris, Atlassian, Primer, GOV.UK Frontend, USWDS, Bootstrap, Radix, and shadcn. These are choices, not a brief-to-package lookup table. A public-service site outside a mandated system does not automatically require GOV.UK or USWDS.

Prefer one coherent component foundation. A focused utility or specialized widget may coexist when it solves a real need without introducing competing resets, themes, or interaction models. Do not install a second full system just for one visual effect.

Custom-styled web components should extend that foundation and the approved project identity. Native semantics and custom appearance are compatible. For open surfaces, fallback decisions and the complete interaction contract, read [components.md](components.md); a styled trigger does not prove its browser-owned popup is custom-styled.

## 2.B Visual aesthetics
Glass, bento, brutalism, editorial type, dark surfaces, aurora fields, and kinetic text are visual techniques; none requires a particular framework. Use project-native CSS, SVG, canvas, or existing animation tools where appropriate. Read the matching style reference as a palette of techniques, then adapt to the approved direction.

## 3.A Implementation choices
- Keep the existing framework, router, styling version, token pipeline, state approach, and font setup. Check real versions before editing configuration.
- For a new project, honor the user's stack or project instructions; otherwise choose a suitable small foundation. Static HTML/CSS may suit a simple page; an interactive product may justify an application framework. A visual design skill must not force Next.js, Tailwind, a state store, or an animation library.
- In React server/client frameworks, isolate browser APIs and interactive state at the appropriate client boundary. Do not make the whole page client-only merely for one effect.
- Reuse existing form/data mechanisms. Styled native inputs and local state may suffice; include open choice popups in the custom treatment by default while preserving intentional platform/system exceptions from components.md. Introduce a form library, state store, or schema package only for a concrete requirement.
- For animation use CSS/native APIs or the installed library first. Motion and GSAP are optional tools for their respective needs; inspect package versions and actual exports before importing them.

## 3.B State and continuous input
Keep transient local state local. Shared state should follow the existing architecture. Avoid rerendering an entire tree for every pointer/scroll frame; use animation values, refs, CSS scroll timelines, or an appropriately scoped event handler. Use passive listeners where suitable and clean up listeners/observers on teardown.

## 3.C Type and icons
Use brand or project fonts first. Check language coverage, license, available weights, fallback metrics, and transfer size. A display/body pairing is an option; a mono face for actual code or numeric data is a purposeful third role when useful. Do not add a face just because a style recipe lists one. Use the framework's font loader or the existing self-hosted pipeline when appropriate.

Reuse the project's icon family and consistent optical weight. New icons may use an installed library, simple SVG, or an original mark when needed. Do not add an entire icon package for one easily drawn shape. Icon-only controls need accessible names; decorative icons should not add redundant screen-reader output. Emoji can suit playful, chat, or social content when the brief supports them.

## 3.D Responsive mechanics
Choose widths and breakpoints from the content instead of forcing one `max-width` or a collapse at `md`. Use fluid grids, `minmax()`, container queries, and wrapping where supported. Preserve usable reading order at all sizes. Full-height scenes may use `min-height: 100svh` or `100dvh` as suitable, with fallbacks; avoid fixed viewport heights that clip real content. Test long labels, zoom, and intermediate widths when affected.

## 3.E Dependencies
Check the manifest and lockfile before imports. If a dependency is necessary and within the authorized implementation scope, add it using the project's package manager and compatibility constraints, then run the relevant build/check. Do not report an install command as if installation succeeded. Avoid opportunistic migrations or upgrades while doing visual work.

## 4.9 Color scheme
- Ship the requested or existing scheme(s). For a new unspecified design, choose one appropriate scheme after intake and state it in `DESIGN.md`. Do not default to both or add a toggle without a user need.
- Section-level light/dark contrast is allowed for composition and visual rhythm. Define section foreground/background roles and verify contrast, focus, media, and controls locally. It does not require a second site-wide theme.
- When both themes ship, use the project's single theme mechanism and semantic tokens. Preserve system preference/manual choice behavior and avoid hydration flashes. Test both; do not merely invert every color.
- A named style does not force light-only or dark-only operation. Brand direction, usability, and the brief choose theme scope.
- Check contrast on the actual rendered background, especially transparent panels and gradients. Keep selected, success, warning, and error states understandable without color alone.
