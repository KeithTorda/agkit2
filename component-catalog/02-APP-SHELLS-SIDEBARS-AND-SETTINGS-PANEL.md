# 02 — App Shells, Sidebars, Headers & Theme Settings Drawer

Portable drawer script: `../ui-kit/keith-ui-settings.js`

---

## 1. App Shell Types (3 Layout Archetypes)

1. **`VerticalSidebarShell` (Default Admin / SaaS / ERP):**
   - Left viewport-locked sticky sidebar (`100dvh`, `flex-col`, `shrink-0`) + Right column (`TopHeader` + scrollable `MainContent` + `Footer`).
2. **`HorizontalTopbarShell` (Analytics / Portal):**
   - Sticky top brand + primary horizontal nav bar + centered or fluid `MainContent`.
3. **`SplitStudioShell` (Video/Design Editors, POS Register, Inbox):**
   - Compact icon rail + Left control/list pane + Right live preview/canvas pane (`100dvh` locked workspace).

---

## 2. Sidebar Navigation Modes (5 Variants)

Centralize navigation items in a single config array (`id`, `label`, `href`, `icon`, `badge`, `children`). Support clean responsive parity:

| Mode | Width | Behavior |
|---|---|---|
| **`full` (Expanded Desktop)** | `248px` (`w-60`–`w-64`) | Brand header at top, scrollable middle `<nav>`, pinned user/footer block at bottom. |
| **`mini` (Collapsed Icon Rail)** | `76px` (`min-w-[76px] max-w-[76px]`) | Centered `24x24` icons; set `<nav>` to `overflow-visible` when collapsed so right-side hover tooltips are never clipped. |
| **`compact` (Stacked Icon + Label)** | `104px` | Centered icon above short 1-word label. |
| **`floating` (Elevated Island)** | `248px` with `12px` outer margin | Rounded `16px` floating card surface (`--ui-sidebar-bg`) with soft elevation shadow. |
| **`overlay` (Mobile `<768px` Drawer)** | `280px` slide-over | Backdrop scrim, focus trap, `Escape` to close, explicit `isMobileDrawer: true` close button (`X`). |

**Mandatory HTML Rules:**
- Never nest `<button>` inside `<a>` or `<Link>`; keep collapsible submenu chevrons as sibling buttons or row handlers.
- Match active routes accurately without query-string or parent-prefix false positives.

---

## 3. Top Header Bar Anatomy

- **Left:** Mobile menu button (`<768px` synchronized with sidebar breakpoint) + Current Page Title (`h1` / bar title) + optional Breadcrumb.
- **Right:** Debounced `SearchInput` pill + Primary Quick Action CTA + `NotificationPopover` + `ThemeModeToggle` + `UserProfileDropdown`.

---

## 4. Right-Side Live Theme & Layout Settings Drawer (`ThemeSettingsDrawer`)

For admin dashboards and workspace portals, include a right-edge slide-over customizer (`ui-kit/keith-ui-settings.js` or a React `<ThemeSettingsDrawer />`) sharing **one single state store** (`keith_ui_preferences_v1` — never split across competing cookies and `localStorage` keys):
1. **Color Mode:** `Light Mode` / `Dark Mode`
2. **15 Color Swatches (`preset_1..15`):** Independent pickers for `Primary Color`, `Sidebar Color`, and `Top Header Color` (auto-computing `--on-primary`, `--on-sidebar`, `--on-header`)
3. **Menu Layout:** `Side Menu (Vertical)` / `Top Menu (Horizontal)`
4. **Sidebar Size:** `Full Width` / `Collapsed Icons (Mini)` / `Compact` / `Floating Island`
5. **Container Width & Font:** `Fluid` vs `Boxed` + clean sans-serif font switcher (`Plus Jakarta Sans`, `Inter`, `DM Sans`, `Cairo`)
6. **Reset Button:** Instant 1-click restore to default settings.
