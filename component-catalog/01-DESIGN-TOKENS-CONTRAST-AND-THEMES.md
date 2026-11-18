# 01 — Design Tokens, Contrast Matrix & Zero-Conflict CSS

Portable token core: `../ui-kit/keith-ui-tokens.css`

---

## 1. Universal Semantic Token Contract (Works in Any UI Stack)

Never hardcode raw hex colors (`#000`, `#fff`, `#f8f9fa`) inside components or pages. Bind all surfaces, borders, text, and accents to semantic CSS variables:

| Token | Light Mode Default | Dark Mode Default | Purpose |
|---|---|---|---|
| `--ui-canvas` | `#f5f7fa` | `#11131a` | Page background canvas |
| `--ui-surface` | `#ffffff` | `#1a1d27` | Cards, modals, tables, drawers |
| `--ui-surface-subtle` | `#eef2f6` | `#151821` | Subtle info boxes, hover rows, code/note blocks |
| `--ui-border` | `#d5dbe3` | `#2a2f3f` | Card, input, and table dividers (`>= 3:1` interactive border contrast) |
| `--ui-ink` | `#000000` | `#ffffff` | Pure high-contrast primary text & headings |
| `--ui-ink-muted` | `#18181b` | `#e4e4e7` | Crisp secondary labels & subtitles (never washed-out grey) |
| `--ui-primary` | `#5bcfc5` (or `preset_1..15`) | Adapts per preset | Primary brand fill |
| `--on-primary` | `#000000` or `#ffffff` | Auto-matched `>= 4.5:1` | Text/icons sitting **on** `--ui-primary` solid fills |
| `--primary-ink` | Deepened shade `>= 4.5:1` | Lightened shade `>= 4.5:1` | Links, outline buttons, and soft badges sitting on `--ui-surface` |
| `--on-sidebar` / `--on-header` | `#000000` or `#ffffff` | Auto-matched `>= 4.5:1` | Text/icons on customizable sidebar & top header surfaces |

---

## 2. How to Connect Tokens to Any Stack Without CSS Conflicts

### A. Tailwind CSS v3 / v4 + shadcn/ui (React, Next.js, Blade, Vue)
- Map Tailwind semantic tokens (`background`, `card`, `muted`, `border`, `foreground`, `primary`, `primary-foreground`) to `:root` and `.dark` / `[data-ui-theme="dark"]` CSS variables.
- **Forbidden in JSX/Blade:** Hardcoded light-only classes (`bg-white`, `bg-gray-50`, `text-black`, `text-gray-900`) without semantic tokens — they break immediately in Dark Mode! Use `bg-card text-card-foreground`, `bg-muted text-foreground`, `border-border`, `bg-primary text-primary-foreground`.

### B. Vanilla CSS / Custom Design System
- Declare `@layer tokens, base, components, utilities;` at line 1 (or import `ui-kit/keith-ui-tokens.css`).
- Scope project-specific widgets under `.app-*` inside `@layer components` consuming `var(--ui-*)` — zero `!important`, zero raw hex outside `@layer tokens`.

### C. Bootstrap 5 Projects
- Load vendor `bootstrap.min.css` untouched → load token bridge CSS → keep custom project CSS strictly `.app-*` scoped with zero `!important` and zero `text-dark` / `bg-white` / `bg-light` in markup.

---

## 3. All 15 WCAG AA Verified Accent Presets (`preset_1..15`)

| Preset | Brand Hex | `--on-primary` (Solid Button Ink) | Light `--primary-ink` | Dark `--primary-ink` |
|---|---|---|---|---|
| `preset_1` (Mint Teal) | `#5bcfc5` | `#000000` (`11.2:1`) | `#0f5e57` (`7.6:1`) | `#6fe3d9` (`10.3:1`) |
| `preset_2` (Indigo) | `#6610f2` | `#ffffff` (`7.2:1`) | `#520dc2` (`9.6:1`) | `#b48bf8` (`6.0:1`) |
| `preset_3` (Sky Blue) | `#0ea5e9` | `#000000` (`7.5:1`) | `#035388` (`8.1:1`) | `#7dd3fc` (`9.8:1`) |
| `preset_4` (Deep Purple) | `#4d06a5` | `#ffffff` (`11.1:1`) | `#4d06a5` (`11.1:1`) | `#c29ffa` (`7.3:1`) |
| `preset_5` (Crimson) | `#dc3545` | `#ffffff` (`4.53:1`) | `#b02a37` (`6.5:1`) | `#ff8590` (`6.8:1`) |
| `preset_6` (Orange) | `#fd7e14` | `#000000` (`8.2:1`) | `#9e4700` (`6.3:1`) | `#ffa94d` (`8.3:1`) |
| `preset_7` (Amber) | `#ffc107` | `#000000` (`12.9:1`) | `#7a5a00` (`6.4:1`) | `#ffd43b` (`11.1:1`) |
| `preset_8` (Obsidian) | `#18181b` | `#ffffff` (`17.7:1`) | `#18181b` (`17.7:1`) | `#ffffff` (`15.8:1`) |
| `preset_9` (Emerald) | `#20c997` | `#000000` (`9.9:1`) | `#0d684d` (`6.8:1`) | `#51e3b8` (`9.8:1`) |
| `preset_10` (Cyan) | `#17a2b8` | `#000000` (`6.9:1`) | `#0c6370` (`6.9:1`) | `#5cd6e8` (`9.2:1`) |
| `preset_11` (Plum) | `#94618e` | `#ffffff` (`4.8:1`) | `#74496f` (`7.2:1`) | `#d7afd2` (`8.3:1`) |
| `preset_12` (Slate) | `#343a40` | `#ffffff` (`11.5:1`) | `#212529` (`15.4:1`) | `#ced4da` (`10.6:1`) |
| `preset_13` (Royal Blue) | `#2563eb` | `#ffffff` (`5.2:1`) | `#1d4ed8` (`6.7:1`) | `#93c5fd` (`8.9:1`) |
| `preset_14` (Cobalt) | `#4885ed` | `#000000` (`5.9:1`) | `#1d56b8` (`6.8:1`) | `#8ab4f8` (`7.5:1`) |
| `preset_15` (Forest Green) | `#4cb32b` | `#000000` (`7.8:1`) | `#286814` (`6.8:1`) | `#7ee05e` (`9.6:1`) |
