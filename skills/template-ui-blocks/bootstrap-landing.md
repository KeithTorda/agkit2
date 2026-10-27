# Bootstrap 5.3 landing and auth blocks

Same `<head>` as [bootstrap-app.md](bootstrap-app.md) (head script, Bootstrap, Bootstrap Icons, tokens + bridge, `kit.css`). Copy the sections in this order for the Rule 07 landing recipe. Text and plans come from [demo-data.md](demo-data.md).

```css
/* landing.css (tokens only) */
.lp-nav { position: sticky; top: 0; z-index: 1030; background: color-mix(in oklab, var(--background) 82%, transparent); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); }
.lp-nav .nav-link { color: var(--muted-foreground); font-weight: 500; border-radius: var(--radius-sm); }
.lp-nav .nav-link:hover, .lp-nav .nav-link:focus-visible { color: var(--foreground); background: var(--surface-muted); }
.lp-section { padding: clamp(4rem, 8vw, 7rem) 0; }
.eyebrow { display: inline-flex; align-items: center; gap: .4rem; padding: .3rem .8rem; border-radius: 999px; background: var(--primary-soft); color: var(--primary); font-size: .8rem; font-weight: 600; }
.text-gradient { background: var(--gradient-brand); -webkit-background-clip: text; background-clip: text; color: transparent; }
.hero { position: relative; overflow: hidden; }
.hero::before { content: ""; position: absolute; inset: -30% -10% auto; height: 70%; background: radial-gradient(closest-side, var(--primary-soft), transparent); pointer-events: none; }
.hero-visual { border-radius: var(--radius-lg); border: 1px solid var(--border); background: var(--surface); box-shadow: var(--shadow-lg), var(--glow); padding: 1rem; }
.logo-strip span { color: var(--muted-foreground); font-weight: 700; font-size: 1.15rem; letter-spacing: -.01em; opacity: .8; transition: opacity var(--dur) var(--ease); }
.logo-strip span:hover { opacity: 1; }
.stats-band { background: var(--gradient-brand); color: var(--primary-foreground); border-radius: var(--radius-lg); }
.price-card.featured { border: 2px solid var(--primary); box-shadow: var(--shadow-lg), var(--glow); }
.lp-footer { background: var(--surface); border-top: 1px solid var(--border); }
.lp-footer a { color: var(--muted-foreground); text-decoration: none; }
.lp-footer a:hover, .lp-footer a:focus-visible { color: var(--primary); }
.avatar-stack .avatar { box-shadow: 0 0 0 2px var(--background); }
.avatar-stack .avatar + .avatar { margin-left: -.6rem; }
.auth-visual { background: var(--gradient-brand); color: var(--primary-foreground); }
```

## 1. Navbar

```html
<nav class="navbar navbar-expand-lg lp-nav" aria-label="Main">
  <div class="container">
    <a class="navbar-brand d-flex align-items-center gap-2 fw-bold" href="/"><span class="brand-mark"><i class="bi bi-stars" aria-hidden="true"></i></span>Tala Commerce</a>
    <button class="navbar-toggler border-0" type="button" data-bs-toggle="offcanvas" data-bs-target="#lpMenu" aria-controls="lpMenu" aria-label="Open menu"><i class="bi bi-list fs-3"></i></button>
    <div class="offcanvas offcanvas-end" tabindex="-1" id="lpMenu" aria-label="Menu">
      <div class="offcanvas-header"><span class="fw-bold">Menu</span><button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button></div>
      <div class="offcanvas-body align-items-lg-center">
        <ul class="navbar-nav mx-lg-auto gap-lg-1">
          <li class="nav-item"><a class="nav-link px-3" href="#features">Features</a></li><li class="nav-item"><a class="nav-link px-3" href="#pricing">Pricing</a></li>
          <li class="nav-item"><a class="nav-link px-3" href="#testimonials">Customers</a></li><li class="nav-item"><a class="nav-link px-3" href="#faq">FAQ</a></li></ul>
        <div class="d-flex gap-2 mt-3 mt-lg-0"><div class="theme-toggle"><!-- 3-state toggle from tokens-and-theme.md --></div>
          <a class="btn btn-ghost" href="/login">Sign in</a><a class="btn btn-primary" href="/register">Start free</a></div>
      </div>
    </div>
  </div>
</nav>
```

## 2. Hero (two CTAs + visual)

```html
<header class="hero lp-section">
  <div class="container position-relative"><div class="row align-items-center g-5">
    <div class="col-lg-6">
      <span class="eyebrow mb-3"><i class="bi bi-lightning-charge-fill" aria-hidden="true"></i>New: multi-branch inventory</span>
      <h1 class="display-4 fw-bold lh-1 mb-3">Run every branch from <span class="text-gradient">one calm dashboard</span></h1>
      <p class="lead text-body-secondary mb-4">Sales, stock and BIR-ready reports for Cauayan, Santiago and Tuguegarao in one place. Set up in an afternoon.</p>
      <div class="d-flex flex-wrap gap-2 mb-4"><a href="/register" class="btn btn-primary btn-lg px-4">Start 14-day trial</a><a href="#demo" class="btn btn-surface btn-lg px-4"><i class="bi bi-play-circle me-2"></i>Watch 2-min demo</a></div>
      <div class="d-flex align-items-center gap-3 small text-body-secondary"><div class="avatar-stack d-flex"><span class="avatar">MS</span><span class="avatar">JC</span><span class="avatar">KB</span></div>Trusted by 1,200+ stores across Luzon</div>
    </div>
    <div class="col-lg-6"><div class="hero-visual">
      <div class="d-flex gap-2 mb-3" aria-hidden="true"><span class="rounded-circle" style="width:.7rem;height:.7rem;background:var(--error)"></span><span class="rounded-circle" style="width:.7rem;height:.7rem;background:var(--warning)"></span><span class="rounded-circle" style="width:.7rem;height:.7rem;background:var(--success)"></span></div>
      <div class="row g-2 mb-2"><div class="col-6"><div class="card p-3"><small class="text-body-secondary">Revenue</small><strong class="fs-5">₱1,284,650.75</strong><span class="badge-soft badge-soft-success mt-1 align-self-start">12.4%</span></div></div>
        <div class="col-6"><div class="card p-3"><small class="text-body-secondary">Orders</small><strong class="fs-5">3,192</strong><span class="badge-soft badge-soft-success mt-1 align-self-start">8.1%</span></div></div></div>
      <div class="rounded-3" style="height:11rem;background:linear-gradient(180deg,var(--primary-soft),transparent);border:1px dashed var(--border)" role="img" aria-label="Sales chart preview"></div>
      <!-- swap with a real product screenshot: <img src="assets/img/dashboard.webp" class="img-fluid rounded-3" alt="Tala Commerce dashboard"> -->
    </div></div>
  </div></div>
</header>
```

## 3. Logo strip

```html
<section class="py-4 border-top border-bottom" aria-label="Customers">
  <div class="container"><p class="text-center small text-body-secondary mb-3">Powering stores from Aparri to Baguio</p>
    <div class="logo-strip d-flex flex-wrap justify-content-center gap-4 gap-md-5"><span>Bituin Labs</span><span>Kawayan Co.</span><span>Alon Logistics</span><span>Habi Studio</span><span>Liwayway Foods</span><span>Daloy Pay</span></div></div>
</section>
```

## 4. Features grid + one detail row

```html
<section class="lp-section" id="features"><div class="container">
  <div class="text-center mx-auto mb-5" style="max-width:40rem"><span class="eyebrow mb-3">Features</span><h2 class="display-6 fw-bold">Everything a growing store needs</h2><p class="text-body-secondary">No spreadsheets, no end-of-day guesswork.</p></div>
  <div class="row g-4">
    <!-- repeat x6: cash-register/POS, box-seam/Inventory, arrow-left-right/Transfers, file-earmark-text/BIR reports, people/Roles, phone/Mobile -->
    <div class="col-md-6 col-lg-4"><div class="card card-hover h-100 p-4"><span class="icon-chip mb-3"><i class="bi bi-box-seam" aria-hidden="true"></i></span>
      <h3 class="h5">Live inventory</h3><p class="text-body-secondary mb-0">Stock levels update the second a sale rings up, across every branch.</p></div></div>
  </div>
  <div class="row align-items-center g-5 mt-5"><!-- alternate: add order-lg-2 to the image column on the next row -->
    <div class="col-lg-6"><div class="hero-visual" style="height:18rem" role="img" aria-label="Stock transfer screen"></div></div>
    <div class="col-lg-6"><span class="eyebrow mb-3">Transfers</span><h3 class="h2 fw-bold">Move stock between branches in two taps</h3>
      <ul class="list-unstyled vstack gap-2 mt-3 text-body-secondary"><li><i class="bi bi-check-circle-fill me-2" style="color:var(--success)"></i>Approval flow per branch manager</li><li><i class="bi bi-check-circle-fill me-2" style="color:var(--success)"></i>Delivery receipts with photos</li></ul></div>
  </div>
</div></section>
```

## 5. Stats band

```html
<section class="pb-5"><div class="container"><div class="stats-band p-5"><div class="row text-center g-4">
  <div class="col-6 col-lg-3"><div class="display-6 fw-bold">1,200+</div><div class="opacity-75">Stores</div></div>
  <div class="col-6 col-lg-3"><div class="display-6 fw-bold">₱2.4B</div><div class="opacity-75">Sales processed</div></div>
  <div class="col-6 col-lg-3"><div class="display-6 fw-bold">99.9%</div><div class="opacity-75">Uptime</div></div>
  <div class="col-6 col-lg-3"><div class="display-6 fw-bold">4.8/5</div><div class="opacity-75">Average rating</div></div>
</div></div></div></section>
```

## 6. Testimonials

```html
<section class="lp-section bg-body-tertiary" id="testimonials"><div class="container">
  <h2 class="display-6 fw-bold text-center mb-5">Loved by store owners</h2>
  <div class="row g-4" id="quotes"></div></div></section>
<script>
document.getElementById('quotes').innerHTML = DEMO.testimonials.map((t) => `<div class="col-md-4"><figure class="card h-100 p-4 mb-0">
  <div class="mb-3" style="color:var(--warning)" aria-label="5 out of 5 stars">${'<i class="bi bi-star-fill"></i>'.repeat(5)}</div>
  <blockquote class="mb-4">“${t.quote}”</blockquote>
  <figcaption class="d-flex align-items-center gap-2 mt-auto"><span class="avatar">${fmt.initials(t.name)}</span><span><strong class="d-block">${t.name}</strong><small class="text-body-secondary">${t.role}</small></span></figcaption></figure></div>`).join('');
</script>
```

## 7. Pricing (three tiers, highlighted plan)

```html
<section class="lp-section" id="pricing"><div class="container">
  <div class="text-center mb-5"><h2 class="display-6 fw-bold">Simple pricing in pesos</h2><p class="text-body-secondary">VAT inclusive. Cancel anytime.</p></div>
  <div class="row g-4 align-items-stretch" id="plans"></div></div></section>
<script>
document.getElementById('plans').innerHTML = DEMO.plans.map((p) => `<div class="col-lg-4"><div class="card price-card h-100 p-4 ${p.highlighted ? 'featured' : ''}">
  ${p.highlighted ? '<span class="badge-soft badge-soft-primary align-self-start mb-2">Most popular</span>' : ''}
  <h3 class="h5">${p.name}</h3><p class="text-body-secondary small">${p.blurb}</p>
  <div class="mb-3"><span class="display-6 fw-bold">${p.price ? fmt.peso(p.price).replace('.00', '') : 'Free'}</span>${p.price ? `<span class="text-body-secondary">/${p.period}</span>` : ''}</div>
  <ul class="list-unstyled vstack gap-2 mb-4">${p.features.map((f) => `<li><i class="bi bi-check2 me-2" style="color:var(--success)" aria-hidden="true"></i>${f}</li>`).join('')}</ul>
  <a href="/register" class="btn ${p.highlighted ? 'btn-primary' : 'btn-surface'} mt-auto">${p.cta}</a></div></div>`).join('');
</script>
```

## 8. FAQ accordion

```html
<section class="lp-section pt-0" id="faq"><div class="container" style="max-width:48rem">
  <h2 class="display-6 fw-bold text-center mb-4">Frequently asked questions</h2>
  <div class="accordion" id="faqAcc">
    <div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1" aria-expanded="true" aria-controls="f1">Does it work offline?</button></h3>
      <div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body text-body-secondary">Yes. Sales queue on the device and sync when the connection returns.</div></div></div>
    <div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2" aria-expanded="false" aria-controls="f2">Can I import my existing products?</button></h3>
      <div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body text-body-secondary">Upload a CSV or Excel file; we map the columns for you.</div></div></div>
    <!-- 4 to 6 items total -->
  </div></div></section>
```

## 9. CTA band + footer

```html
<section class="pb-5"><div class="container"><div class="stats-band p-5 text-center">
  <h2 class="display-6 fw-bold">Ready to close the month in two days?</h2><p class="opacity-75 mb-4">Free for 14 days. No credit card.</p>
  <div class="d-flex justify-content-center flex-wrap gap-2"><a href="/register" class="btn btn-lg btn-surface">Start free trial</a><a href="/contact" class="btn btn-lg btn-ghost" style="--bs-btn-color:var(--primary-foreground);--bs-btn-hover-color:var(--primary-foreground);--bs-btn-hover-bg:color-mix(in oklab,var(--primary-foreground) 15%,transparent)">Talk to sales</a></div>
</div></div></section>

<footer class="lp-footer pt-5 pb-4"><div class="container">
  <div class="row g-4">
    <div class="col-lg-4"><a class="d-flex align-items-center gap-2 fw-bold mb-3 text-reset" href="/"><span class="brand-mark"><i class="bi bi-stars"></i></span>Tala Commerce</a>
      <p class="small text-body-secondary">Retail operations for growing Filipino stores.</p>
      <form class="d-flex gap-2" aria-label="Newsletter"><input type="email" class="form-control" placeholder="you@store.ph" aria-label="Email" required><button class="btn btn-primary">Subscribe</button></form></div>
    <div class="col-6 col-lg-2 offset-lg-1"><h3 class="h6">Product</h3><ul class="list-unstyled vstack gap-2 small"><li><a href="#features">Features</a></li><li><a href="#pricing">Pricing</a></li><li><a href="/changelog">Changelog</a></li></ul></div>
    <div class="col-6 col-lg-2"><h3 class="h6">Company</h3><ul class="list-unstyled vstack gap-2 small"><li><a href="/about">About</a></li><li><a href="/careers">Careers</a></li><li><a href="/contact">Contact</a></li></ul></div>
    <div class="col-6 col-lg-3"><h3 class="h6">Support</h3><ul class="list-unstyled vstack gap-2 small"><li><a href="/help">Help center</a></li><li><a href="/status">System status</a></li><li><a href="mailto:hello@tala.example">hello@tala.example</a></li></ul></div>
  </div>
  <div class="d-flex flex-wrap justify-content-between align-items-center gap-3 pt-4 mt-4 border-top small text-body-secondary">
    <span>© 2026 Tala Commerce (demo). Cauayan City, Isabela.</span>
    <div class="d-flex gap-3"><a href="/privacy">Privacy</a><a href="/terms">Terms</a>
      <a href="#" aria-label="Facebook"><i class="bi bi-facebook"></i></a><a href="#" aria-label="LinkedIn"><i class="bi bi-linkedin"></i></a><a href="#" aria-label="YouTube"><i class="bi bi-youtube"></i></a></div>
  </div></div></footer>
```

## 10. Auth split page

```html
<main class="row g-0 min-vh-100">
  <section class="col-lg-6 auth-visual d-none d-lg-flex flex-column justify-content-between p-5" aria-label="About Tala Commerce">
    <a class="d-flex align-items-center gap-2 fw-bold text-reset text-decoration-none" href="/"><i class="bi bi-stars fs-4"></i>Tala Commerce</a>
    <div><h2 class="display-6 fw-bold mb-3">Every branch, one login.</h2><p class="opacity-75 fs-5">“We closed the month in two days instead of a week.”</p><p class="small opacity-75">Rhea Manalo, Kawayan Café (demo)</p></div>
    <small class="opacity-75">© 2026 Tala Commerce (demo)</small>
  </section>
  <section class="col-lg-6 d-flex align-items-center justify-content-center p-4">
    <div class="w-100" style="max-width:24rem">
      <div class="d-flex justify-content-end mb-4"><div class="theme-toggle"><!-- 3-state toggle --></div></div>
      <h1 class="h3 fw-bold">Welcome back</h1><p class="text-body-secondary">Sign in to your store dashboard.</p>
      <div class="d-grid gap-2 mb-3"><button class="btn btn-surface"><i class="bi bi-google me-2"></i>Continue with Google</button><button class="btn btn-surface"><i class="bi bi-microsoft me-2"></i>Continue with Microsoft</button></div>
      <div class="d-flex align-items-center gap-2 my-3 small text-body-secondary"><hr class="flex-grow-1">or<hr class="flex-grow-1"></div>
      <form class="needs-validation vstack gap-3" novalidate>
        <div><label class="form-label" for="le">Email</label><input type="email" id="le" class="form-control form-control-lg" autocomplete="email" required><div class="invalid-feedback">Enter your email.</div></div>
        <div><div class="d-flex justify-content-between"><label class="form-label" for="lp">Password</label><a class="small" href="/forgot-password">Forgot password?</a></div>
          <div class="input-group has-validation"><input type="password" id="lp" class="form-control form-control-lg" autocomplete="current-password" required minlength="8">
            <button class="btn btn-surface" type="button" aria-label="Show password" onclick="const i=document.getElementById('lp');i.type=i.type==='password'?'text':'password';this.setAttribute('aria-pressed',i.type==='text')"><i class="bi bi-eye"></i></button>
            <div class="invalid-feedback">At least 8 characters.</div></div></div>
        <div class="form-check"><input class="form-check-input" type="checkbox" id="rm"><label class="form-check-label" for="rm">Remember me for 30 days</label></div>
        <button class="btn btn-primary btn-lg" type="submit"><span class="spinner-border spinner-border-sm me-1" hidden aria-hidden="true"></span>Sign in</button>
      </form>
      <p class="text-center small text-body-secondary mt-4">No account yet? <a href="/register">Create one free</a></p>
    </div>
  </section>
</main>
```

Validation and loading state: reuse the `.needs-validation` submit script from [bootstrap-data.md](bootstrap-data.md).
