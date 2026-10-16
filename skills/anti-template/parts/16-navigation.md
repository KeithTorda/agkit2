---
part: 16
title: Navigation and orientation
covers: headers, menus, sidebars, breadcrumbs, tabs, pagination, back links, search, user menus, footer
---

# 16 - Navigation and orientation

Read when designing a header, sidebar, menu, tabs, pagination, or footer. Follow the chosen visual direction while making destinations, current location, and interaction clear.

## Headers and primary navigation

Choose navigation from the site's actual information architecture and common tasks. A solid, glass, transparent, image-overlay, sticky, or fixed header can work. Test readable contrast across the real backdrop, focus visibility, anchor offsets, and mobile space. Do not require a plain header to avoid a visual trend.

Use real links for destinations so users can copy, open in a new tab, and navigate without scripted click handling. A menu toggle is a button with an accessible name and `aria-expanded`; connect it to the controlled region where useful. A logo link needs a useful home name. Mark the current destination with `aria-current="page"` rather than relying solely on color.

Avoid hiding important links in a dropdown just to preserve a reference screenshot. Mega menus can help large sites when grouped and labeled clearly. Use an accessible disclosure or navigation pattern; not every group of links needs application `menu` roles.

## Mobile menus and sidebars

Select a drawer, full-screen menu, inline disclosure, bottom navigation, or another pattern based on destination count and workflow. If the menu is modal, manage focus, background interaction, scroll, and close behavior. If it is nonmodal, do not trap keyboard users unnecessarily. Closed regions should not leave invisible focusable links.

Sidebars can use labels, icons, groups, compact modes, and branded surfaces. Icon-only navigation needs understandable names and visible help on focus as well as hover. Preserve an obvious current state. Do not impose a ban on colored icons or decorative treatments; test whether the hierarchy remains legible.

## Breadcrumbs, tabs, and back navigation

Use breadcrumbs for a meaningful hierarchy, not every page by reflex. A named `<nav>` with an ordered list and current-page state is a useful structure. Avoid fabricated ancestors or clickable separators.

Tabs switch related panels; route navigation should generally remain links. Custom tab widgets need tablist/tab/tabpanel relationships, selection state, keyboard behavior, and sensible focus handling. Activation strategy should consider panel latency. A segmented control may instead be a radio group or button group depending on behavior.

A "Back" link should have a reliable destination. Browser history may not contain a useful previous page for direct entry; provide a meaningful fallback. Preserve filters and scroll when that helps the return workflow.

## Search, pagination, and account controls

Search should have an accessible name, clear scope, submission or debounce behavior, loading, no-results, and recovery. A command palette supplements navigation rather than replacing discoverable essential actions. Shortcuts need visibility and must not interfere with assistive technology.

Pagination should identify the current page, explain range or total when known, and preserve sorting/filter state. "Load more" and infinite scroll can fit discovery flows; deep record work may need stable URLs and return positions. Ensure a footer or primary action does not become unreachable under endless loading.

Account and notification menus require real content and state. A count should reflect actual notifications, with a readable accessible label. Do not fabricate online presence or unread counts.

## Footer and review

A footer can be minimal or elaborate according to the design. Include the real links and organizational details the product needs; avoid invented policies, addresses, newsletters, or social accounts. Inspect keyboard traversal, small-screen operation, long labels, active states, close behavior, and real destinations. A familiar layout is acceptable when it serves orientation.
