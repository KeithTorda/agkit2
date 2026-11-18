# 02 — Master App Shell, Sidebar (`.dlabnav`) & Top Header

Source reference: `reference-template/bootstrap-5-dashboard-pro/empty-page.html` and `index.html`.

---

## 1. Shell Anatomy (`#main-wrapper`)

Every authenticated screen in the template shares 5 top-level siblings inside `#main-wrapper`:

1. **`.nav-header`** — Top-left brand mark + `.nav-control > .hamburger` sidebar collapse button.
2. **`.header`** — Fixed top bar containing `.dashboard_bar` (current page title) on the left and `.header-right` (search input, notifications dropdown, optional theme toggle, primary CTA button) on the right.
3. **`.dlabnav`** — Fixed scrollable vertical sidebar (`ul.metismenu#menu`) starting with `.header-profile` user dropdown followed by route items and collapsible `ul` submenus.
4. **`.content-body > .container-fluid`** — Main responsive page container (starts with optional `.row.page-titles > ol.breadcrumb`, followed by `.row` grid cards).
5. **`.footer > .copyright`** — Clean single-line system footer.

*(Optional 6th sibling: `.chatbox` right slide-over drawer if the project needs live chat/notes/activity drawer).*

---

## 2. Clean Production Shell Blueprint (HTML / Blade Ready)

Sanitized from `empty-page.html` (removed demo switcher, `javascript:void(0)`, and nested invalid tags):

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page Title — System Name</title>
  <link rel="icon" type="image/png" href="/assets/images/favicon.png">
  <link href="/assets/vendor/jquery-nice-select/css/nice-select.css" rel="stylesheet">
  <link href="/assets/css/style.css?v=1.0.0" rel="stylesheet">
</head>
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
  data-primary="color_1"
>
  <div id="main-wrapper">
    <!-- 1. Brand & Sidebar Toggle -->
    <div class="nav-header">
      <a href="/dashboard" class="brand-logo" aria-label="Dashboard Home">
        <span class="logo-abbr fw-bold fs-3 text-primary">S</span>
        <span class="brand-title fw-bold fs-4 text-dark ms-2">SystemName</span>
      </a>
      <button type="button" class="nav-control border-0 bg-transparent" aria-label="Toggle navigation sidebar">
        <span class="hamburger">
          <span class="line"></span><span class="line"></span><span class="line"></span>
        </span>
      </button>
    </div>

    <!-- 2. Top Header -->
    <header class="header">
      <div class="header-content">
        <nav class="navbar navbar-expand">
          <div class="collapse navbar-collapse justify-content-between">
            <div class="header-left">
              <h1 class="dashboard_bar mb-0">Dashboard Overview</h1>
            </div>
            <ul class="navbar-nav header-right align-items-center">
              <li class="nav-item">
                <form action="/search" method="GET" class="input-group search-area">
                  <input type="search" name="q" class="form-control" placeholder="Search records..." aria-label="Search records">
                  <button type="submit" class="input-group-text border-0" aria-label="Submit search">
                    <i class="flaticon-381-search-2" aria-hidden="true"></i>
                  </button>
                </form>
              </li>
              <li class="nav-item dropdown notification_dropdown">
                <button type="button" class="nav-link ai-icon border-0 bg-transparent" data-bs-toggle="dropdown" aria-label="Notifications">
                  <i class="las la-bell fs-24" aria-hidden="true"></i>
                  <span class="badge light text-white bg-primary rounded-circle tabular-nums">3</span>
                </button>
                <div class="dropdown-menu dropdown-menu-end">
                  <div class="widget-media dlab-scroll p-3" style="max-height: 340px;">
                    <ul class="timeline">
                      <li>
                        <div class="timeline-panel">
                          <div class="media me-2 media-primary"><i class="las la-check" aria-hidden="true"></i></div>
                          <div class="media-body">
                            <h6 class="mb-1">Payment verified for INV-2026-014</h6>
                            <small class="d-block">10 minutes ago</small>
                          </div>
                        </div>
                      </li>
                    </ul>
                  </div>
                  <a class="all-notification" href="/notifications">View all notifications <i class="ti-arrow-end" aria-hidden="true"></i></a>
                </div>
              </li>
            </ul>
          </div>
        </nav>
      </div>
    </header>

    <!-- 3. Sidebar Navigation (.dlabnav) -->
    <aside class="dlabnav" aria-label="Primary Sidebar">
      <div class="dlabnav-scroll">
        <ul class="metismenu" id="menu">
          <!-- Profile Dropdown Header -->
          <li class="dropdown header-profile">
            <a class="nav-link" href="#profileMenu" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <img src="/assets/images/profile/pic1.jpg" width="20" alt="Admin avatar">
              <div class="header-info ms-3">
                <span class="font-w600"><b>Juan Dela Cruz</b></span>
                <small class="text-end font-w400">Administrator</small>
              </div>
            </a>
            <div class="dropdown-menu dropdown-menu-end">
              <a href="/profile" class="dropdown-item ai-icon">
                <i class="las la-user-circle text-primary fs-18" aria-hidden="true"></i>
                <span class="ms-2">My Profile</span>
              </a>
              <form action="/logout" method="POST" class="m-0">
                <button type="submit" class="dropdown-item ai-icon text-danger">
                  <i class="las la-sign-out-alt text-danger fs-18" aria-hidden="true"></i>
                  <span class="ms-2">Sign Out</span>
                </button>
              </form>
            </div>
          </li>

          <!-- Direct Single Link (Active state uses class="mm-active" on <li>) -->
          <li class="mm-active">
            <a href="/dashboard" class="ai-icon" aria-current="page">
              <i class="flaticon-025-dashboard" aria-hidden="true"></i>
              <span class="nav-text">Dashboard</span>
            </a>
          </li>

          <!-- Collapsible Group -->
          <li>
            <a class="has-arrow ai-icon" href="#inventorySubmenu" aria-expanded="false">
              <i class="flaticon-043-menu" aria-hidden="true"></i>
              <span class="nav-text">Inventory</span>
            </a>
            <ul aria-expanded="false">
              <li><a href="/inventory/products">Product List</a></li>
              <li><a href="/inventory/stock-movements">Stock Movements</a></li>
              <li><a href="/inventory/categories">Categories</a></li>
            </ul>
          </li>
        </ul>

        <div class="copyright mt-auto">
          <p><strong>SystemName</strong> &copy; 2026 All Rights Reserved</p>
        </div>
      </div>
    </aside>

    <!-- 4. Main Content Body -->
    <main class="content-body">
      <div class="container-fluid">
        <!-- Breadcrumb Row -->
        <div class="row page-titles">
          <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/dashboard">Home</a></li>
            <li class="breadcrumb-item active" aria-current="page">Dashboard Overview</li>
          </ol>
        </div>

        <!-- Page Rows Go Here -->
        <div class="row">
          <div class="col-12">
            <!-- Cards -->
          </div>
        </div>
      </div>
    </main>

    <!-- 5. Footer -->
    <footer class="footer">
      <div class="copyright">
        <p>&copy; 2026 SystemName. All rights reserved.</p>
      </div>
    </footer>
  </div>

  <script src="/assets/vendor/global/global.min.js"></script>
  <script src="/assets/vendor/jquery-nice-select/js/jquery.nice-select.min.js"></script>
  <script src="/assets/js/custom.min.js?v=1.0.0"></script>
  <script src="/assets/js/dlabnav-init.js?v=1.0.0"></script>
  <script src="/assets/js/demo.js?v=1.0.0"></script>
  <script src="/assets/js/styleSwitcher.js?v=1.0.0"></script>
</body>
</html>
```

---

## 3. Sidebar & Responsive Rules (React / SPA Adaptation Notes)

When implementing `.dlabnav` in React/Next.js without jQuery MetisMenu:
1. Toggle `#main-wrapper.menu-toggle` via React state (`isSidebarCollapsed` on desktop `>=768px`, `isMobileDrawerOpen` on `<768px`).
2. Keep navigation items in a single typed array (`sidebarNavigationItems`) with `id`, `label`, `iconClass`, `href`, and optional `children`.
3. Never nest `<button>` inside `<Link>`; render parent submenu headers as `<button type="button" className="has-arrow ai-icon w-100 text-start border-0 bg-transparent">` when they only expand submenus.
4. When collapsed (`menu-toggle` / mini rail), allow horizontal submenu/tooltip popouts (`overflow: visible` on the collapsed rail) so labels are never clipped.
