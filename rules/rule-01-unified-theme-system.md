---
name: rule-01-unified-theme-system
version: 2.0.0
priority: P0
trigger: glob
globs: "**/*.html, **/*.css, **/*.scss, **/*.tsx, **/*.jsx, **/*.vue, **/*.svelte, **/*.astro, **/*.blade.php, **/tailwind.config.*, **/components/**, **/resources/views/**"
description: Rule 01 - Unified Theme System V2.0. One semantic-token design system with Light, Dark and System modes for websites, dashboards, SaaS and web apps.
---

# RULE 01 — UNIFIED THEME SYSTEM (V2.0)
**Priority: CRITICAL | Mandatory | Non-Negotiable**

**Applies to:** Websites, Admin Dashboards, SaaS Platforms, Enterprise Applications, and Web Applications.

## CORE PRINCIPLE

**ONE DESIGN SYSTEM. THREE THEME MODES. ONE SOURCE OF TRUTH. ZERO KNOWN CONFLICTS.**

Build every application using a centralized, scalable, semantic-token-based design system.

Light Mode, Dark Mode, and System Mode must operate through one unified theme architecture.

The application must preserve a consistent premium visual identity, smooth interactions, accessible contrast, and reliable functionality across all supported themes.

Never sacrifice theme consistency, accessibility, or functionality for decorative effects.

---

## SECTION A — THEME ARCHITECTURE

### 1. SINGLE SOURCE OF TRUTH

- Implement one centralized theme management system.
- Use one theme provider where appropriate for the framework.
- Maintain a single authoritative theme preference and resolved appearance.
- Never create multiple competing theme providers.
- Never allow individual components to independently control the application's global theme.
- Avoid mixing incompatible CSS class, attribute, and JavaScript theme strategies.

**Required behavior:** Changing the theme must update every relevant interface component consistently.

### 2. THREE-MODE THEME SUPPORT

The application must support:

- **Light Mode:** Explicit light appearance.
- **Dark Mode:** Explicit dark appearance.
- **System Mode:** Automatically follows the operating system's current appearance.

Maintain two distinct values:

- `themePreference`: `light | dark | system`
- `resolvedTheme`: `light | dark`

System Mode is not a third color palette. It resolves to Light or Dark based on system preference.

### 3. CENTRALIZED SEMANTIC DESIGN TOKENS

Create a centralized token system covering:

**Colors**
- `background`
- `foreground`
- `surface`
- `surface-elevated`
- `surface-muted`
- `primary`
- `primary-foreground`
- `secondary`
- `accent`
- `muted`
- `muted-foreground`
- `border`
- `input`
- `ring`
- `success`
- `warning`
- `error`
- `info`
- `hover`
- `active`
- `disabled`

**Additional system tokens**
- Sidebar background and foreground
- Navigation active and hover states
- Chart series and grid colors
- Shadows and elevation
- Gradient colors
- Glow intensity and color
- Glass transparency and borders
- Border radius
- Spacing
- Typography
- Animation duration and easing
- Z-index layers

**Required architecture:**

Primitive palette → Semantic tokens → Component tokens → UI components.

All components must consume the centralized semantic or component tokens.

### 4. NO HARDCODED THEME-DEPENDENT COLORS

Never use arbitrary theme-dependent colors directly inside UI components.

Prohibited examples:

- Hardcoded white cards intended for both themes
- Fixed black text that becomes invisible in Dark Mode
- Unpaired light-only or dark-only backgrounds
- Fixed hover colors that ignore the current theme
- Hardcoded chart labels or grid colors

Raw color values are permitted inside centralized palette or token definitions.

Brand colors may remain consistent across themes only when contrast and accessibility are preserved.

### 5. UNIFIED COMPONENT ARCHITECTURE

Use the same reusable component architecture in both themes.

Changing the theme must not unnecessarily:

- Rebuild components
- Reset forms
- Reset navigation state
- Clear user selections
- Refetch unrelated data
- Change the overall layout
- Remount the entire application

Only the necessary visual styling should change.

---

## SECTION B — THEME INITIALIZATION AND PERSISTENCE

### 6. ZERO UNWANTED THEME FLASHING

Initialize the correct resolved theme before the first visible render whenever technically possible.

For server-rendered applications:

- Use a server-readable preference when available.
- Apply an early theme initialization strategy.
- Avoid server/client hydration mismatches.
- Do not render the wrong theme and correct it afterward.

For client-rendered applications:

- Resolve the saved preference before displaying the application.
- Prevent unnecessary flashes during initial loading.

Do not hide the entire application indefinitely while waiting for theme initialization.

### 7. PERSISTENT THEME PREFERENCES

- Save the user's explicit theme selection.
- Restore the preference on reload.
- Default to System Mode when no selection exists, unless product requirements specify otherwise.
- Listen for operating-system appearance changes while System Mode is selected.
- Do not override an explicit Light or Dark selection when system settings change.
- Synchronize preference changes across tabs when practical.
- Handle unavailable or restricted browser storage gracefully.

### 8. NATIVE BROWSER THEME INTEGRATION

Use the appropriate CSS `color-scheme` behavior.

Ensure native elements respond correctly, including:

- Scrollbars
- Form inputs
- Date and time controls
- Select menus
- Browser-provided UI
- Autofill states

The browser's native appearance must remain consistent with the resolved theme.

---

## SECTION C — PREMIUM USER INTERFACE

### 9. COMPLETE THEME-AWARE COMPONENT COVERAGE

All applicable components must use the active theme, including:

- Sidebars and navigation
- Top navigation bars
- KPI cards and dashboard widgets
- Data tables and pagination
- Charts and analytics
- Forms and validation states
- Dropdowns and context menus
- Dialogs and modals
- Popovers and tooltips
- Notifications and toast messages
- Command palettes
- Search components
- Empty states
- Loading skeletons
- Authentication screens
- Settings panels
- Mobile navigation
- Date pickers and calendars
- Third-party UI components

Components rendered through portals must inherit or explicitly receive the correct theme.

No visible component may remain incorrectly styled after a theme change.

### 10. PREMIUM SIDEBAR DESIGN AND MOTION

Sidebars must support polished, purposeful interactions.

Where appropriate, implement:

- Smooth sidebar collapse and expansion
- Animated active navigation indicators
- Subtle icon hover transformations
- Refined background and color transitions
- Expandable navigation groups
- Animated submenu disclosure
- Clear active route highlighting
- Consistent icon sizing and alignment
- Accessible tooltips in collapsed mode
- Responsive mobile drawer behavior

**Recommended motion defaults:**

- Icon hover: 120–200 ms
- Navigation indicator: 180–260 ms
- Sidebar expansion: 220–320 ms
- Page transitions: 180–300 ms
- Staggered card entrance: 250–450 ms

These are design defaults, not rigid timing requirements.

Use purposeful motion and avoid unnecessary animations that distract from the content.

### 11. PREMIUM VISUAL EFFECTS

Support modern visual treatments when appropriate:

- Glassmorphism
- Soft ambient glows
- Gradient accents
- Subtle shadows
- Layered surfaces
- Hover elevation
- Interactive icon animations
- Smooth state transitions
- Refined loading effects
- Animated data visualizations

All visual effects must be theme-aware.

**Light Mode:**
- Controlled shadows
- Refined borders
- Soft accent treatments
- Subtle transparency
- Minimal glow intensity

**Dark Mode:**
- Layered dark surfaces
- Controlled luminous accents
- Clear surface separation
- Balanced gradients
- Restrained ambient glows

Never directly reuse an effect's intensity across themes if it reduces readability or produces inconsistent visual quality.

### 12. DATA VISUALIZATION THEME SUPPORT

Charts must dynamically adapt:

- Axis labels
- Legends
- Grid lines
- Tooltips
- Plot backgrounds
- Data series
- Hover indicators
- Selection states
- Reference lines
- Empty and loading states

Use centralized chart tokens with distinguishable data-series colors.

Never communicate information through color alone. Use labels, symbols, line patterns, or other supporting indicators where necessary.

Prevent chart reinitialization or lost interaction state during theme changes unless required by the chart library.

---

## SECTION D — ACCESSIBILITY AND PERFORMANCE

### 13. ACCESSIBILITY IS MANDATORY

Target WCAG 2.2 Level AA for applicable interfaces.

Required minimum contrast:

- Normal text: 4.5:1
- Large text: 3:1
- Relevant non-text interface indicators: 3:1

Apply the relevant WCAG exceptions where appropriate.

Additional requirements:

- Visible keyboard focus
- Keyboard-accessible controls
- Clear selected and active states
- Accessible labels
- Readable error messages
- Accessible icon-only buttons
- No color-only status communication
- Support for high-contrast and forced-colors environments where applicable
- Support for zoom and text resizing
- Respect `prefers-reduced-motion`

Accessibility requirements take priority over decorative effects.

### 14. PERFORMANCE-FIRST ANIMATIONS

Prefer efficient animations based on:

- `transform`
- `opacity`
- GPU-friendly compositing where beneficial

Avoid unnecessary layout-triggering animation properties.

Additional requirements:

- Prevent excessive simultaneous animations.
- Avoid continuous decorative animations without purpose.
- Do not use expensive blur or backdrop-filter effects indiscriminately.
- Prevent unnecessary React component rerenders.
- Keep theme switching responsive.
- Respect device limitations and reduced-motion preferences.
- Never block important user interactions during a theme transition.

Where appropriate, disable decorative animations for reduced-motion users while retaining essential interaction feedback.

### 15. RESPONSIVE DESIGN CONSISTENCY

Both themes must work across:

- Mobile phones
- Tablets
- Laptops
- Desktop monitors
- Large dashboard displays

Ensure consistent navigation, surface colors, modal behavior, readable tables, and accessible controls at supported breakpoints.

Theme switching must not cause unexpected overflow, layout shifts, clipped text, or hidden interactive elements.

---

## SECTION E — CSS AND COMPONENT INTEGRATION

### 16. CSS ARCHITECTURE CONTROL

- Use one documented theme application strategy.
- Maintain a clear CSS cascade and styling hierarchy.
- Avoid unnecessary `!important` declarations.
- Do not introduce duplicate token definitions without a documented reason.
- Avoid conflicting global styles and component overrides.
- Define component variants consistently.
- Keep theme-specific CSS centralized.
- Eliminate obsolete styles after refactoring.

If using Tailwind CSS, use one configuration-compatible theme strategy consistently throughout the project.

### 17. THIRD-PARTY COMPONENT COMPATIBILITY

All third-party libraries must integrate with the centralized design system.

For charts, editors, maps, calendars, data grids, and UI libraries:

- Use supported theming APIs.
- Map semantic tokens to library theme settings.
- Synchronize theme changes.
- Avoid conflicting built-in themes.
- Verify overlays and portals.
- Test focus, hover, selected, and disabled states.

Never add an independent theme provider solely to fix one component if it can be integrated into the existing system.

---

## SECTION F — AI DEVELOPMENT WORKFLOW

### 18. MANDATORY THEME ARCHITECTURE AUDIT

Before generating or modifying code, the AI must:

1. Inspect the existing framework and styling system.
2. Identify the current theme provider or theme mechanism.
3. Locate existing design tokens.
4. Review global CSS and component styling.
5. Identify third-party theme dependencies.
6. Check for existing theme inconsistencies.
7. Reuse the existing architecture when it is sound.
8. Refactor conflicting patterns rather than adding another theme system.

**Never blindly introduce a new theme provider, styling framework, or color architecture into an existing project.**

### 19. NON-REGRESSION REQUIREMENT

When adding, modifying, or removing a feature:

- Preserve existing theme functionality.
- Reuse established semantic tokens.
- Verify both Light and Dark Modes.
- Avoid modifying unrelated components.
- Prevent regressions in responsive behavior.
- Preserve existing animation and accessibility behavior.
- Update tests when component behavior changes.

A new feature is not complete if it breaks another component's appearance or functionality.

### 20. AUTOMATED AND MANUAL QUALITY ASSURANCE

Test the application using an appropriate combination of automated checks and manual review.

**Required test scenarios:**

- Fresh visit with no saved preference
- Explicit Light Mode
- Explicit Dark Mode
- System Mode with light OS preference
- System Mode with dark OS preference
- System appearance changes during an open session
- Reload after selecting a preference
- Client-side navigation
- Server-rendered hydration where applicable
- Mobile and desktop layouts
- Sidebar expansion and collapse
- Modals and dropdowns
- Forms and validation states
- Charts and tooltips
- Keyboard focus
- Reduced-motion preference
- Loading and error states

Use accessibility checks and visual regression testing where tooling is available.

Do not claim tests passed unless they were actually executed.

### 21. DEFINITION OF DONE

A theme implementation is complete only when:

- [ ] One authoritative theme architecture is used.
- [ ] Light, Dark, and System modes function correctly.
- [ ] Components consume semantic theme tokens.
- [ ] No unintended hardcoded theme colors remain.
- [ ] Theme preferences persist correctly.
- [ ] System Mode responds to OS appearance changes.
- [ ] No unwanted first-render theme flash occurs.
- [ ] No hydration errors are introduced.
- [ ] Sidebar and premium visual effects work in both themes.
- [ ] Charts, modals, portals, and third-party components follow the theme.
- [ ] Applicable accessibility contrast requirements are met.
- [ ] Reduced-motion preferences are respected.
- [ ] Theme changes preserve application state.
- [ ] Responsive layouts remain functional.
- [ ] No known theme-related regressions remain.
- [ ] Required tests have been executed, or unverified checks are clearly identified.

---

## STRICT ENFORCEMENT POLICY

**NEVER CONSIDER AN APPLICATION COMPLETE IF THEME SWITCHING CAUSES:**

- Inconsistent colors
- Invisible or unreadable text
- Broken component styling
- Poorly contrasted charts
- Missing icons or incorrect icon colors
- Conflicting shadows, gradients, or glow effects
- Incorrect sidebar appearance
- Unstyled third-party components
- Broken modals or dropdowns
- Layout shifts or visual flashing
- Hydration mismatches
- Lost application state
- Inconsistent interaction states
- Accessibility regressions
- Significant performance degradation

Fix all detected critical theme issues before final delivery.

If an issue cannot be resolved, document the limitation and do not claim full compliance.

---

## REQUIRED AI DELIVERY REPORT

After implementation, provide:

1. **Theme Architecture:** Identify the provider, state management, and token system used.
2. **Modified Files:** List important files created or changed.
3. **Component Coverage:** Identify components verified in both themes.
4. **Testing Results:** Report which tests were actually run and their outcomes.
5. **Known Limitations:** Disclose any unresolved theme or accessibility issues.

Do not fabricate testing results or report unverified functionality as completed.

---

## FINAL DESIGN STANDARD

Every application must maintain a premium, modern, polished, and professional visual identity across all supported themes.

The interface must feel like one cohesive product rather than two independently styled applications.

Theme switching must be seamless, accessible, responsive, performant, and reliable.

Animations, glow effects, glassmorphism, charts, sidebars, and interactive components must remain visually consistent and functionally stable.

**This rule overrides aesthetic preferences, animation choices, and component-level styling decisions whenever they introduce theme conflicts, accessibility problems, or functional regressions.**

**FINAL DIRECTIVE TO AI DEVELOPERS:**

Before writing code, understand the existing design system. During implementation, reuse its architecture and tokens. After implementation, verify both themes, inspect interactive states, and report any unresolved issues.

**DO NOT BUILD TWO SEPARATE THEMES. BUILD ONE UNIFIED SYSTEM THAT SUPPORTS TWO VISUAL APPEARANCES AND THREE USER SELECTION MODES.**

**END OF RULE 01 — UNIFIED THEME SYSTEM V2.0**