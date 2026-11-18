# 01 — Theme Tokens, Color Presets & Typography

Extracted directly from `reference-template/bootstrap-5-dashboard-pro/css/style.css` and `js/dlabnav-init.js`.

---

## 1. Body Data Attributes (Single Source of Layout & Theme Truth)

The template controls its entire appearance via `data-*` attributes on `<body>`:

```html
<body
  data-typography="cairo"
  data-theme-version="light"
  data-layout="vertical"
  data-nav-headerbg="color_1"
  data-headerbg="color_1"
  data-sidebar-style="full"
  data-sibebarbg="color_1"
  data-sidebar-position="fixed"
  data-header-position="fixed"
  data-container="wide"
  direction="ltr"
  data-primary="color_1"
>
```

> **Note:** Notice the template's CSS spells sidebar background attribute as `data-sibebarbg` (`b` instead of `d`). Keep that exact attribute name if using original `style.css`.

---

## 2. Semantic Surface & Text Tokens (Light vs. Dark)

| Token Role | Light Mode (`data-theme-version="light"`) | Dark Mode (`data-theme-version="dark"`) | CSS Variable / Usage |
|---|---|---|---|
| **Page Canvas (`body`)** | `#f6f6f6` | `#171622` | Main app background behind cards |
| **Elevated Surface (`.card`, `.dlabnav`, `.nav-header`)** | `#ffffff` | `#212130` | Cards, sidebar, modals, dropdowns |
| **Input Fill (`.form-control`)** | `#f6f6f6` (border `#f5f5f5`) | `#171622` (border `#2e2e42`) | Text inputs, selects, textareas |
| **Subtle Border / Divider** | `#f0f1f5` / `rgba(0,0,0,0.125)` | `#2e2e42` | Card headers, table borders, dividers |
| **Heading / Primary Text** | `#000000` / `#212529` | `#ffffff` | `.card-title`, `h1`–`h6`, metric numbers |
| **Body / Muted Text** | `#7e7e7e` / `#969ba0` | `#828690` | Subtitles, timestamps, helper labels |
| **Corner Radius (Cards & Inputs)** | `0.75rem` (`12px`) | `0.75rem` (`12px`) | `.card`, `.form-control`, `.dropdown-menu` |
| **Pill Radius** | `50rem` / `9999px` | `50rem` / `9999px` | `.btn-rounded`, `.input-rounded`, `.badge-rounded` |

### Status Semantic Palette
- **Success:** `#68e365` (for WCAG AA text contrast on white, pair with `.badge.light.badge-success` or `#1f7a1c` text)
- **Info:** `#b48dd3` / `#17a2b8`
- **Warning:** `#ffa755` (always use dark text `#3d2800` on solid warning or `.badge.light.badge-warning`)
- **Danger:** `#f72b50`
- **Secondary:** `#709fba`

---

## 3. Built-In Primary Accent Presets (`data-primary="color_X"`)

Pick **one** primary color preset per project so each client app has its own brand identity while reusing the exact same components:

| Preset | `--primary` | `--primary-hover` | `--primary-dark` | Best Domain Fit |
|---|---|---|---|---|
| `color_1` / `color_3` (Default) | `#5bcfc5` (Teal) | `#38bfb3` | `#217069` | Finance, Billing, Clinic / Medical, General Admin |
| `color_14` | `#4885ed` (Royal Blue) | `#1a66e8` | `#0e3d8e` | Government / LGU, School / University, HRIS, Queueing |
| `color_9` | `#20c997` (Emerald) | `#199d76` | `#0b4534` | Pharmacy, RHU Health, Accounting, Inventory |
| `color_15` | `#4cb32b` (Forest Green) | `#3b8a21` | `#18380d` | Agriculture, Cooperative, Supply Office |
| `color_2` | `#6610f2` (Indigo) | `#510bc4` | `#290564` | SaaS Portal, Creator Tools, Tech Dashboard |
| `color_10` | `#17a2b8` (Cyan) | `#117a8b` | `#062a30` | Water District, Logistics, Ticketing |
| `color_5` | `#dc3545` (Crimson) | `#bd2130` | `#66121a` | Emergency / Incident Reporting, Motorparts / Automotive |
| `color_6` | `#fd7e14` (Amber Orange) | `#dc6502` | `#773701` | Retail POS, Food / Restaurant, Delivery |
| `color_12` | `#343a40` (Slate Charcoal) | `#1d2124` | `#000000` | Executive / Legal / Minimal Enterprise |

> **Never use `color_8` (`#ffffff`) as `data-primary`** in light mode because primary buttons turn white-on-white.

---

## 4. Portable CSS Variables Starter (For React / Next.js / Custom Builds)

When adapting this template into a React/Next.js or standalone CSS module without loading the entire 1.3 MB `style.css`, include these core variables and flash-free theme script:

```css
:root,
[data-theme-version="light"] {
  --primary: #5bcfc5;
  --primary-hover: #38bfb3;
  --primary-dark: #217069;
  --secondary: #709fba;
  --rgba-primary-1: rgba(91, 207, 197, 0.12);
  --rgba-primary-2: rgba(91, 207, 197, 0.2);

  --bg-canvas: #f6f6f6;
  --bg-surface: #ffffff;
  --bg-input: #f6f6f6;
  --border-subtle: #f0f1f5;
  --text-heading: #192236;
  --text-body: #6e757c;
  --radius-card: 0.75rem;
  --radius-control: 0.75rem;
  color-scheme: light;
}

[data-theme-version="dark"] {
  --bg-canvas: #171622;
  --bg-surface: #212130;
  --bg-input: #171622;
  --border-subtle: #2e2e42;
  --text-heading: #ffffff;
  --text-body: #828690;
  color-scheme: dark;
}

.metric-value,
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
```

### Flash-Free Theme Initialization (`<head>` Inline Script)
Include only when the application offers a Light/Dark toggle:

```html
<script>
  (function () {
    try {
      var saved = localStorage.getItem('theme_version');
      var resolved = (saved === 'dark' || saved === 'light')
        ? saved
        : (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.setAttribute('data-theme-version', resolved);
      document.addEventListener('DOMContentLoaded', function () {
        document.body.setAttribute('data-theme-version', resolved);
      });
    } catch (e) {}
  })();
</script>
```
