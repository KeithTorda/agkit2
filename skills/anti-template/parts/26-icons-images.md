---
part: 26
title: Icons and Images
covers: icon sets, icon sizes, stroke, icon colour, icon-only controls, emoji as icons, decorative icons, stock photos, AI-generated images, illustrations, placeholder avatars, gradient overlays, aspect ratios, compression, formats, alt text, logos, logo walls, favicons, video backgrounds, local photos
---

# 26 — Icons and Images

Read when: adding icons, photos, illustrations, avatars, logos, favicons, video or any `<img>`, `<svg>`, `<picture>` or `<video>` to a page.

## 26.1 Icon placement

An icon earns its place when it speeds recognition of a repeated action or item. Icons next to text that is already clear add noise.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Icon next to every menu item | Generator adds an icon to each nav entry by reflex | Icons in primary nav only (sidebar of an app). Dropdowns, footers and secondary menus are text only |
| Decorative icon above or beside every heading | "Icon + Title + Sentence" feature block, repeated down the page | Heading alone. See part 05 for feature copy |
| Decorative icons on stat cards (dollar icon on revenue, users icon on members) | Every AI dashboard; the label already says it | Label and number only. See part 22 |
| Icon in a coloured circle or rounded square (`p-3 rounded-full bg-indigo-100 text-indigo-600`) | The "icon badge" template, one per feature card | Remove the container and usually the icon. If kept, icon at text size in `currentColor` |
| Icons in every table cell (calendar icon before each date, mail icon before each email) | Repeats a symbol the column header already explains | Plain values. The column header names the type |
| Icon before every list item instead of a bullet (checkmark list for features) | Checkmark lists are a pricing-page cliché spread everywhere | Plain `<ul>` bullets. Checkmarks only in a comparison where some items are "no" |
| Icon before every form label | Visual noise on a form that must be read top to bottom | Label text only |
| Icon inside every input (envelope in email, lock in password) | Template login form | No icon. Search input may keep a magnifier. See part 17 |
| Icon on every button (`<Plus /> Add`, `<Save /> Save`, `<X /> Cancel`) | Library demo style | Icons on 0–2 buttons per screen where the symbol is standard (add, download, print). Text alone for the rest |
| Arrow icon after every link or CTA ("Learn more →") | AI "Read more" pattern | Link text alone. Arrow only for links that leave the site, and use the external-link symbol |
| Sparkles icon for any "AI" or "smart" feature | Lucide `Sparkles` became the AI logo | Name the feature: "Auto-fill from last entry". No sparkle |
| Rocket, lightning bolt, shield, heart icons on feature cards | Stand-ins for "fast", "secure", "loved" | Delete the icon and the vague claim; state the fact |
| Oversized icons as hero elements (a 200 px Lucide/Heroicon as the main visual) | Filler when there is no real visual | Screenshot, data preview, a real photo, or nothing |
| Icon status columns (coloured icons meaning Active/Inactive) | Meaning hidden in a glyph | Text status ("Active", "Suspended"), optional small dot. See part 19 |
| Icon-only badges (a flame for "popular", a star for "featured") | Unclear meaning | Text badge: "Popular", "Featured" |

## 26.2 Icon sets, style and size

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Mixing icon sets (Lucide + Heroicons + Font Awesome + Material) | Each component copied from a different demo | One set for the whole project, named in DESIGN.md |
| Outline and filled icons mixed | Inconsistent weight | Pick one style. Filled only for a selected/active state if the set supports it |
| Different stroke widths (1.5 and 2 on the same screen) | Lucide default 2, Heroicons 1.5, mixed | One stroke width, set once (e.g. Lucide `strokeWidth={1.75}` via a wrapper or CSS `stroke-width`) |
| Random sizes (`w-4`, `w-5`, `h-6`, `size={18}`, `size={22}`) | No size scale | 2–3 sizes tied to text: 16 px with 14 px text, 20 px with 16 px text, 24 px for standalone controls |
| Icons not aligned to text baseline | Icon sits high or low in the row | `display: inline-flex; align-items: center; gap: 0.5em` on the parent; icon `flex-shrink: 0` |
| Custom icon for common actions (a unique drawing for "delete") | Users do not recognise it | Standard metaphors: trash for delete, pencil for edit, magnifier for search, gear for settings, download arrow for download, printer for print |
| Same icon for two different actions on one screen | Confusion | One icon, one meaning, app-wide |
| Icon meaning changes between pages (gear = settings here, = config there) | No icon inventory | Keep a short icon map in DESIGN.md: action to icon name |
| Hamburger icon used as "more actions" | Hamburger means navigation | Kebab (vertical dots) or "More" for row actions |
| Duotone / gradient-filled icons | AI "premium" look | Single colour, `currentColor` |
| 3D or glossy icon packs (clay icons, isometric icons) | Dribbble-shot look | Flat line icons from the one chosen set |
| Icon font (Font Awesome full CSS, Material Icons font) loaded for 5 icons | 70–150 KB for a handful of glyphs; icon flashes as a box on slow networks | Inline SVG or a tree-shaken import (`import { Trash2 } from "lucide-react"`). See part 34 |
| Font Awesome kit script from CDN in `<head>` | Render-blocking third-party script | Local SVGs |
| Bootstrap Icons + Font Awesome both loaded | Two icon libraries on one site | One |
| Icons drawn with Unicode symbols (★ ✔ ✖ ☰ ➜) | Renders differently per font and OS | SVG icons from the chosen set |

## 26.3 Icon colour

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Colored icons matching each card (blue icon on blue card, green on green) | Rainbow dashboard | One neutral icon colour: `currentColor` inheriting text colour |
| Each nav icon a different colour | Colour used as decoration | Nav icons share the text colour; active item uses `var(--color-primary)` |
| Status colours on decorative icons (green check on a feature list) | Green means success; nothing succeeded | Neutral colour. Status colours only on real status |
| Icon colour hard-coded with hex in SVG (`fill="#6366F1"`) | Breaks dark mode and theming | `fill="currentColor"` or `stroke="currentColor"`; colour set by CSS token |
| Low-contrast grey icons as the only content of a control | Fails WCAG 1.4.11 (3:1 for UI graphics) | Icon colour at 3:1 or more against its background |
| Gradient fill on icons (`url(#gradient)`) | Neon/AI look | Solid token colour |
| Glow on icons (`drop-shadow(0 0 8px …)`) | Neon look | None |

## 26.4 Icon-only controls

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Icon-only buttons with no name | Screen readers announce "button"; sighted users guess | Visible text label, or `aria-label` plus a tooltip showing the same text |
| Icon-only nav without tooltips | Users hover each icon to learn the app | Text labels in nav. Collapsed sidebar shows tooltips on hover and focus. See part 16 |
| Eye icon for show password without label | Unclear, often not keyboard reachable | "Show password" checkbox, or a button with `aria-label="Show password"` and `aria-pressed`. See part 23 |
| Icon-only row actions (pencil, trash, eye) with no names | Screen readers read nothing useful; trash next to pencil causes mis-taps | `aria-label="Edit {name}"`, `aria-label="Delete {name}"`; separate destructive action by 8 px+ or move into a menu |
| Icon-only button smaller than 24x24 CSS px | Fails WCAG 2.5.8 target size | 24x24 minimum; 44x44 on touch screens |
| `title` attribute as the only name | Not shown on touch, not reliable for screen readers | `aria-label` or visually hidden text; tooltip component for visual users |
| Tooltip that only appears on hover | Keyboard and touch users never see it | Show on focus too; on touch, prefer a visible label |
| Social icons with no accessible name | "link, link, link" to a screen reader | `aria-label="Facebook page of Barangay San Isidro"` or visible text |
| Decorative icon inside a labelled button announced twice | SVG has a `<title>` and the button has text | Add `aria-hidden="true"` and `focusable="false"` to decorative SVGs |

```html
<!-- Banned -->
<div class="icon-btn" onclick="del(12)"><i class="fa fa-trash"></i></div>

<!-- Use -->
<button type="button" class="icon-btn" aria-label="Delete receipt 000123">
  <svg aria-hidden="true" focusable="false" width="20" height="20"><use href="#icon-trash"/></svg>
</button>
```

## 26.5 Emoji as icons

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Emoji as feature icons (🚀 Fast, 🔒 Secure, ⚡ Powerful) | The top AI landing tell | Remove emoji. Plain heading, or one icon from the chosen set |
| Emoji in nav labels (🏠 Home, 📊 Dashboard, ⚙️ Settings) | Renders differently on each OS; looks like a chat app | SVG icons or text only |
| Emoji in headings, buttons, toasts, badges | Unprofessional on business and government sites | None. See parts 02 and 03 |
| Emoji as status indicator (✅ Paid, ❌ Unpaid, ⏳ Pending) | Screen readers read "check mark button Paid"; colours vary by platform | Text status plus optional dot token. See part 19 |
| Emoji in empty states (📭, 🔍, 🎉) | Chat-style cheer | Text only. See part 04 |
| Emoji flags for language or country pickers (🇵🇭 🇺🇸) | Windows shows letter pairs ("PH"), not flags | Language names in their own language: "English", "Filipino" |
| Emoji in `<title>` or favicon | Tab looks like spam | Plain title; real favicon. See part 08 |
| Emoji in alt text | Read aloud literally | Plain description |

Emoji belong only in user-generated content (comments, chat, posts), never in system UI.

## 26.6 Stock photos

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Stock photos of smiling people at laptops, handshakes, pointing at screens | Instantly recognisable filler | Real screenshot of the product, a real photo of the client's place, or no image |
| Unsplash hot-linked images (`images.unsplash.com/photo-…`) | Placeholder left in production; external dependency | Client-supplied photos stored in the project and optimised |
| Diverse-team-in-glass-office stock on a barangay or small-business site | Wrong country, wrong setting | Photos of the actual barangay hall, school, store, staff (with consent), or none |
| Western stock on a Philippine site (snowy streets, US school buses, dollar bills) | Context mismatch the audience notices at once | Local photos, or none |
| Stock photo of a doctor/teacher/police officer used as if it were real staff | Misleading on official and clinic sites | Real staff photos with consent, or names without photos |
| Generic "technology" images (blue circuit boards, globe with network lines, binary rain) | Tech-cliché filler | Remove |
| Same stock image reused across several sections | Visible repetition | One image per purpose, or none |
| Photo with a watermark ("Shutterstock", "iStock") | Unlicensed placeholder | Licensed image with the licence recorded, or none |
| `picsum.photos` or `placehold.co` URLs left in | Placeholder shipped | Real image, or remove the `<img>` and its layout slot |
| Photo of a laptop showing a fake dashboard | Mockup of a product that does not exist | Real screenshot at native resolution |

## 26.7 AI-generated images and illustrations

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| AI-generated hero art (glossy 3D shapes, glowing orbs, abstract swirls) | Midjourney/DALL-E look; nothing to learn from it | Screenshot, real photo, or no visual |
| AI-generated people (smooth skin, odd hands, garbled text on signs) | Readers spot it and trust the site less; on government sites it misrepresents | Real photos with consent, or no people |
| AI images of real places (a barangay hall that does not exist, a school building "in the style of") | Fabricated depiction of a real place | Photograph the actual place, or none |
| AI-generated portrait of an official, teacher or captain | Impersonation risk; misleading | Official photo supplied by the office, or name and position only |
| Illustrations from unDraw, Storyset, Humaaans, Open Peeps | Flat-person illustrations on every AI SaaS page | Remove. Real screenshot or plain text |
| Isometric illustrations (isometric servers, desks, cities) | 2019 SaaS template look | Remove |
| 3D blobs, clay 3D characters, floating 3D icons | Spline/Blender template look | Remove |
| SVG illustration per empty state | Decoration where one line of text works | Text: "No receipts yet." plus an action. See part 04 |
| Illustration on 404, 500, maintenance pages (lost astronaut, broken robot) | Joke error page | Plain message and links. See part 04 |
| Illustration on login/register side panel | Split auth page filler | Centered form, no illustration. See part 23 |
| Abstract gradient mesh image as section background | AI "premium" look | Flat background token |
| Illustrations in mixed styles (flat, 3D, line art on one page) | Collected from different sources | One style, or none |
| Garbled pseudo-text inside generated images | Clear AI artefact | Never ship generated images with text. Put text in HTML |

## 26.8 Avatars

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Avatars from `i.pravatar.cc`, `randomuser.me`, `ui-avatars.com`, Unsplash faces | Placeholder people shipped to production | Real user uploads; fallback to initials generated in-app |
| Fake avatars on testimonials, team pages or "trusted by" rows | Invented people | Remove, or real people with consent. See part 05 |
| Stacked avatar row "Join 2,000+ users" with stock faces | Fake social proof | Remove |
| DiceBear / Boring Avatars cartoon faces as defaults for a government or school system | Playful look on a formal record | Initials on a neutral token background, or a plain person silhouette |
| Initials with a random bright colour per user | Rainbow list | One neutral background token; or a small fixed palette from DESIGN.md chosen by a stable hash |
| Online-status dot on every avatar when there is no presence system | Fake liveness | Dot only with real presence data. See part 04 |
| Avatars with gradient rings (Instagram-story style) | Decoration | No ring; 1px border token if needed on busy backgrounds |
| Avatars of different sizes in one list | No size scale | 24, 32, 40 px; one size per context |
| Avatar `<img>` without dimensions | Layout shift as it loads | `width`/`height` attributes and `object-fit: cover` |
| Avatar alt text "avatar" or "profile picture" | Useless to screen readers | `alt=""` when the name is next to it; `alt="{Name}"` when it stands alone |
| Broken image icon when upload is missing | No fallback | `onerror` or server check falls back to initials |

## 26.9 Image treatment

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Gradient overlay on hero image (`bg-gradient-to-t from-black/80`) | Template hero; muddies the photo | Solid dark background with text beside the image, or a clean image with text below. If text must sit on a photo, use a solid scrim token and check 4.5:1 |
| Purple/blue colour tint overlay on photos | AI brand wash | Untinted image |
| Same radius on all images | Thumbnails, heroes and screenshots all `rounded-2xl` | Match context: 0 for full-bleed and screenshots in docs, the card radius token for thumbnails, 9999px for avatars |
| Screenshots with huge drop shadows and 3D tilt | Mockup styling | Flat screenshot with a 1px border token |
| Screenshots inside fake browser/macOS window chrome | Decoration; see part 10 | Screenshot with a 1px border |
| Screenshot inside a phone mockup frame | Template look, shrinks the content | Screenshot at readable size; frame only on an app-store listing |
| Inconsistent aspect ratios in a grid | Uneven cards | `aspect-ratio: 4 / 3` (or 1 / 1, 16 / 9) plus `object-fit: cover` per grid |
| Images stretched (`width: 100%; height: 300px` without `object-fit`) | Distorted faces and logos | `object-fit: cover` for photos, `object-fit: contain` for logos |
| Blur-up placeholder on small, fast images | Effect with no benefit | Plain `<img>` with dimensions; blur-up only for large images on slow pages |
| Grayscale-to-colour on hover | Portfolio gimmick | Full colour always |
| Image zoom on hover | See part 25 | Static |
| Full-width hero image on every page | Landing-page pattern copied to inner pages | Hero image on landing page only; inner pages start with the heading |
| Image carousel of 8 photos on a homepage | Users see one | Grid of 3–6 photos, or a link to a gallery page |
| Decorative background image behind body text | Contrast failures | Plain background token behind text |

## 26.10 Formats, size and loading

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| 3–6 MB hero JPEG straight from the phone or stock site | Slow on PH mobile data | Resize to the largest display size (e.g. 1600 px wide), export WebP or AVIF at quality 70–80; target under 200 KB for heroes |
| PNG for photographs | 5–10x larger than needed | WebP/AVIF for photos; PNG only for screenshots with flat colour or transparency |
| No `width` and `height` attributes | Layout shift (CLS) | Always set intrinsic `width` and `height`; CSS handles responsive size |
| One image size for all screens | Phones download desktop images | `srcset` with 2–4 widths and `sizes`, or the framework image component (`next/image`, `astro:assets`) |
| `loading="lazy"` on the hero / LCP image | Delays the largest paint | `loading="eager"` and `fetchpriority="high"` on the LCP image; `lazy` on everything below the fold |
| No lazy loading on long galleries | Dozens of images load at once | `loading="lazy"` and `decoding="async"` below the fold |
| SVG exported from Figma with editor junk (ids, `data-name`, empty groups) | Bloated markup | Run through SVGO. See part 28 |
| Base64 images inlined in CSS or HTML | Larger than the file; blocks render | Separate files, cached |
| Images served from the original upload without processing | 12 MP photos on a list page | Resize on upload; store thumbnail, medium, large |
| GIFs for screen recordings | Huge and low quality | `<video>` MP4/WebM, muted, with `controls` and a poster |
| `<img src="">` or missing `src` placeholders | Broken image icons | Remove the element until the image exists |
| Upload accepts any file as image | Security and size risk | Accept `image/jpeg,image/png,image/webp`, cap size (e.g. 5 MB), re-encode server-side |

## 26.11 Alt text

Full rules for screen readers are in part 27. This table covers what to write.

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| `<img>` without `alt` | Screen readers read the file name | Every `<img>` has `alt`. Descriptive for content, `alt=""` for decoration |
| `alt="image"`, `alt="photo"`, `alt="picture of"` | Says nothing; screen readers already announce "image" | Describe the content: `alt="Barangay hall front entrance on Rizal Street"` |
| `alt="hero image"`, `alt="banner"` | Describes layout, not content | Describe what is shown, or `alt=""` if decorative |
| Alt text stuffed with keywords ("best affordable school Manila enrolment 2025") | SEO spam | Plain description, 5–20 words |
| Alt text that repeats the caption or adjacent text | Read twice | `alt=""` when the caption fully describes it |
| Alt on logos: "logo" | Unhelpful | Organisation name: `alt="Municipality of Bauang"`; when the logo is the home link: `alt="Municipality of Bauang, home"` |
| Charts as images with `alt="chart"` | Data lost | Alt states the finding ("Enrolment rose from 820 in 2022 to 1,040 in 2024") and a data table sits nearby. See part 20 |
| Screenshots of text (announcements posted as JPEG) | Unreadable to screen readers and search; common on LGU Facebook reposts | Post the text as HTML; image optional with short alt |
| Alt text on decorative SVG icons | Clutter | `aria-hidden="true"` |
| Alt text written by AI: "A vibrant image showcasing…" | Hype in alt | Flat description. No "vibrant", "stunning", "showcasing". See part 01 |

## 26.12 Logos

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Fake logo walls ("Trusted by" with Google, Microsoft, Stripe logos) | Invented clients; possibly trademark misuse | Real clients with permission, or remove the section. See part 05 |
| Generic placeholder logos (Logoipsum, "ACME", "Company") | Template left in | Remove |
| Logo wall in greyscale at 40% opacity in a scrolling marquee | Template social-proof strip | Remove, or a static row of real logos. See parts 10 and 25 |
| AI-generated logo for the client (gradient hexagon, abstract swoosh, letter in a rounded square) | Recognisable generator mark | Use the client-supplied logo. If none exists, set the name in text using the heading font; do not invent a logo |
| Text logo with gradient fill | AI brand look | Solid token colour |
| Sparkle or lightning glyph next to the product name | AI "brand" cliché | Name alone |
| Official seals redrawn or approximated (barangay, municipality, DepEd, COMELEC, Republic seal) | Misrepresents an official mark; see part 09 | Official file from the office only. If not provided, leave it out and flag it in the report |
| Seal of a government agency used on a site that is not that agency | Implies endorsement | Remove. Link to the agency in text if relevant |
| Logo as a low-res JPEG with white box on coloured header | Unprepared asset | SVG, or PNG with transparency at 2x size |
| Logo without dimensions in the header | Header jumps on load | Set `width`/`height` |
| Logo image with no link to home | Users expect it | Header logo links to `/`. See part 16 |

## 26.13 Favicons and app icons

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Default framework favicon left in (`vite.svg`, Next.js triangle, React atom, Laravel icon) | Clear template leftover | Client favicon; see part 33 for the leftover files |
| No favicon at all (browser shows a blank page icon, 404 in console) | Unfinished | Provide `favicon.ico` (32x32) and an SVG favicon |
| Emoji favicon (`data:image/svg+xml,<svg><text>🚀</text></svg>`) | Hack from a tweet; AI tell | Real icon from the logo mark |
| 20 favicon sizes from a generator plus `browserconfig.xml` and `msapplication-*` tags | Boilerplate bloat | `favicon.ico`, `icon.svg`, `apple-touch-icon.png` (180x180), and `manifest.webmanifest` with 192 and 512 icons if it is a PWA. See part 28 |
| Favicon is the full wordmark shrunk to 16 px | Illegible | Symbol or first letter only |
| Favicon with transparent background that disappears on dark tabs | Invisible in dark mode | Solid shape, or SVG favicon with a `prefers-color-scheme` style block |
| Official seal as favicon at 16 px | Unreadable detail | Simplified mark approved by the office, or the initial letter |

## 26.14 Video

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Background video looping behind the hero | Heavy, distracting, costly on mobile data | Static image or none |
| Autoplay video with sound | Hostile; blocked by browsers anyway | No autoplay. `controls`, `preload="none"`, poster image |
| Autoplaying muted product demo on loop | Motion while reading; fails WCAG 2.2.2 without pause | Poster with play button; user starts it |
| YouTube embed loaded on page load | 500 KB+ of third-party script | Lite embed: thumbnail image that loads the iframe on click; `loading="lazy"` on the iframe |
| Video without captions | Deaf users and people in quiet places miss it | `<track kind="captions" srclang="en">` (and `srclang="fil"` where the speech is Filipino) |
| Promo video as the only source of key info (office hours, requirements) | Hidden in a video | Put the info in text; the video is extra |
| Facebook video embed as the main content of an LGU page | Heavy, requires Facebook scripts | Text summary on the page; link to the Facebook post |

## 26.15 Philippine context

| AI pattern | Why it reads as generated | Use instead |
|---|---|---|
| Western stock for Filipino audiences (suburban houses, snow, US flags, dollar bills) | Wrong place | Local photos: the actual office, school, market, jeepney stop; or none |
| Beach, rice terraces or jeepney stock on every PH site | Tourism cliché on a POS or school portal | Photos of the actual client and their work, or none |
| Peso shown as a dollar-sign icon (`DollarSign` from Lucide on a ₱ amount) | Wrong currency glyph | Text "₱" or a peso icon if the set has one (Lucide `PhilippinePeso`); usually no icon at all |
| GCash/Maya logos drawn or recoloured | Brand misuse; payment trust issue | Official brand assets as supplied by GCash/Maya guidelines, unaltered, or the name in text |
| Bank logos on a payment page without permission | Implied partnership | Bank names in text |
| Photos of minors on school sites without consent | Privacy (Data Privacy Act of 2012) | Photos only with written consent on file; otherwise group shots from behind, facilities, or none |
| Barangay officials shown with AI-smoothed or AI-generated portraits | Misrepresentation | Official photos from the barangay, or name and position only |
| DepEd, CHED, COMELEC, DOH logos used as decoration | Implied endorsement | Only when the site is that agency or has written permission |
| Philippine flag waving GIF or sun-and-stars clip art in the header | Decoration | Official seal of the LGU or school only, supplied by them |
| Images sized for fast fibre only | Many users on prepaid data | Hero under 200 KB, thumbnails under 40 KB; test on Slow 3G |

## 26.16 Check
- [ ] One icon set, one style (outline or filled), one stroke width, named in DESIGN.md.
- [ ] Icon sizes come from a 2–3 step scale tied to text size.
- [ ] Icons use `currentColor`; no per-card colours, no gradients, no glow.
- [ ] No icons on secondary menus, footers, form labels, or every table cell.
- [ ] No icon-in-coloured-circle feature blocks.
- [ ] No sparkles, rocket, lightning or shield icons standing in for claims.
- [ ] No oversized icon as a hero visual.
- [ ] Standard metaphors for common actions; one icon per meaning app-wide.
- [ ] Every icon-only control has an accessible name and a tooltip on hover and focus.
- [ ] Icon-only targets are at least 24x24 CSS px (44x44 on touch).
- [ ] Decorative SVGs have `aria-hidden="true"` and `focusable="false"`.
- [ ] No emoji in nav, headings, buttons, badges, status, empty states, titles or alt text.
- [ ] No icon font loaded for a handful of icons; icons are tree-shaken SVG.
- [ ] No Unicode symbols used as icons.
- [ ] No stock photos of people at laptops, handshakes, circuit boards or Western settings.
- [ ] No hot-linked Unsplash, picsum, placehold, pravatar or randomuser URLs.
- [ ] No AI-generated people, places, officials or logos.
- [ ] No unDraw, Storyset, isometric or 3D-blob illustrations.
- [ ] No illustrations on empty states, error pages or auth pages.
- [ ] Avatars: real uploads or initials on a neutral token background; fixed size scale; dimensions set.
- [ ] No gradient or colour-tint overlay on photos; text on photos passes 4.5:1.
- [ ] No fake browser chrome or phone frames around screenshots.
- [ ] Image grids use `aspect-ratio` and `object-fit`.
- [ ] Every `<img>` has `width`, `height` and `alt`.
- [ ] Alt text describes content; `alt=""` for decoration; no "image of", no hype, no keywords.
- [ ] Logos have the organisation name as alt.
- [ ] Hero image is WebP/AVIF, under 200 KB, `fetchpriority="high"`, not lazy.
- [ ] Below-the-fold images use `loading="lazy"` and `srcset`.
- [ ] SVGs are SVGO-cleaned.
- [ ] No fake logo walls, Logoipsum, or invented client logos.
- [ ] No invented or redrawn official seals; missing seals flagged, not faked.
- [ ] Favicon is the client's mark; framework default favicon removed; no emoji favicon.
- [ ] Favicon set is minimal: `.ico`, SVG, apple-touch-icon, manifest icons if PWA.
- [ ] No background video; no autoplay; videos have controls, poster and captions.
- [ ] YouTube embeds load on click.
- [ ] Peso amounts use "₱", never a dollar icon.
- [ ] No photos of minors without consent on file.
- [ ] Agency and payment logos used only with permission and unaltered.
