# Tailwind landing and auth blocks

Same setup as [tailwind-app.md](tailwind-app.md) (head script with `ATTR = 'data-theme'`, tokens, `components.css`, `ui.js`, Lucide). Copy the sections in this order for the Rule 07 landing recipe. Data from [demo-data.md](demo-data.md).

```css
@layer components {
  .section { padding-block: clamp(4rem, 8vw, 7rem); }
  .container-x { margin-inline: auto; max-width: 80rem; padding-inline: 1rem; } @media (min-width: 640px) { .container-x { padding-inline: 1.5rem; } }
  .eyebrow { display: inline-flex; align-items: center; gap: .4rem; padding: .3rem .8rem; border-radius: 9999px; background: var(--primary-soft); color: var(--primary); font-size: .8rem; font-weight: 600; }
  .text-gradient { background: var(--gradient-brand); -webkit-background-clip: text; background-clip: text; color: transparent; }
  .bg-brand { background: var(--gradient-brand); color: var(--primary-foreground); }
  .glow { box-shadow: var(--shadow-lg), var(--glow); }
  .hero-halo { position: absolute; inset: -30% -10% auto; height: 70%; background: radial-gradient(closest-side, var(--primary-soft), transparent); pointer-events: none; }
  .navbar-blur { background: color-mix(in oklab, var(--background) 82%, transparent); backdrop-filter: blur(12px); }
  .btn-on-brand { color: var(--primary-foreground); box-shadow: inset 0 0 0 1px currentColor; } .btn-on-brand:hover { background: color-mix(in oklab, var(--primary-foreground) 15%, transparent); }
  .link-muted { color: var(--muted-foreground); transition: color var(--dur-fast); } .link-muted:hover, .link-muted:focus-visible { color: var(--primary); }
}
```

## 1. Navbar (mobile menu = drawer)

```html
<header class="navbar-blur sticky top-0 z-40 border-b border-border">
  <nav class="container-x flex h-16 items-center gap-6" aria-label="Main">
    <a href="/" class="flex items-center gap-2 font-bold"><span class="bg-brand grid size-8 place-items-center rounded-lg"><i data-lucide="sparkles" class="size-4" aria-hidden="true"></i></span>Tala Commerce</a>
    <ul class="mx-auto hidden gap-1 text-sm font-medium lg:flex">
      <li><a href="#features" class="rounded-md px-3 py-2 text-muted-foreground hover:bg-surface-muted hover:text-foreground">Features</a></li>
      <li><a href="#pricing" class="rounded-md px-3 py-2 text-muted-foreground hover:bg-surface-muted hover:text-foreground">Pricing</a></li>
      <li><a href="#testimonials" class="rounded-md px-3 py-2 text-muted-foreground hover:bg-surface-muted hover:text-foreground">Customers</a></li>
      <li><a href="#faq" class="rounded-md px-3 py-2 text-muted-foreground hover:bg-surface-muted hover:text-foreground">FAQ</a></li></ul>
    <div class="ml-auto hidden items-center gap-2 lg:flex"><!-- 3-state theme toggle from tokens-and-theme.md --><a href="/login" class="btn btn-ghost">Sign in</a><a href="/register" class="btn btn-primary">Start free</a></div>
    <button class="btn btn-ghost btn-icon ml-auto lg:hidden" data-menu="mobileNav" aria-expanded="false" aria-controls="mobileNav" aria-label="Open menu"><i data-lucide="menu" class="size-5"></i></button>
  </nav>
  <div id="mobileNav" class="menu left-4 right-4 lg:hidden" hidden>
    <a href="#features" class="menu-item">Features</a><a href="#pricing" class="menu-item">Pricing</a><a href="#faq" class="menu-item">FAQ</a>
    <div class="mt-2 grid grid-cols-2 gap-2 border-t border-border pt-3"><a href="/login" class="btn btn-surface">Sign in</a><a href="/register" class="btn btn-primary">Start free</a></div></div>
</header>
```

## 2. Hero (two CTAs + visual)

```html
<section class="section relative overflow-hidden"><div class="hero-halo" aria-hidden="true"></div>
  <div class="container-x relative grid items-center gap-12 lg:grid-cols-2">
    <div>
      <span class="eyebrow mb-4"><i data-lucide="zap" class="size-3.5" aria-hidden="true"></i>New: multi-branch inventory</span>
      <h1 class="text-4xl font-bold leading-tight tracking-tight sm:text-5xl lg:text-6xl">Run every branch from <span class="text-gradient">one calm dashboard</span></h1>
      <p class="mt-5 max-w-xl text-lg text-muted-foreground">Sales, stock and BIR-ready reports for Cauayan, Santiago and Tuguegarao in one place. Set up in an afternoon.</p>
      <div class="mt-8 flex flex-wrap gap-3"><a href="/register" class="btn btn-primary h-12 px-6 text-base">Start 14-day trial</a><a href="#demo" class="btn btn-surface h-12 px-6 text-base"><i data-lucide="circle-play" class="size-5"></i>Watch 2-min demo</a></div>
      <div class="mt-8 flex items-center gap-3 text-sm text-muted-foreground"><div class="flex -space-x-2"><span class="avatar ring-2 ring-background">MS</span><span class="avatar ring-2 ring-background">JC</span><span class="avatar ring-2 ring-background">KB</span></div>Trusted by 1,200+ stores across Luzon</div>
    </div>
    <div class="glow rounded-3xl border border-border bg-surface p-4">
      <div class="mb-3 flex gap-1.5" aria-hidden="true"><span class="size-3 rounded-full bg-error"></span><span class="size-3 rounded-full bg-warning"></span><span class="size-3 rounded-full bg-success"></span></div>
      <div class="mb-3 grid grid-cols-2 gap-3">
        <div class="card p-4"><p class="text-xs text-muted-foreground">Revenue</p><p class="text-xl font-bold">₱1,284,650.75</p><span class="badge-soft tone-success mt-1">12.4%</span></div>
        <div class="card p-4"><p class="text-xs text-muted-foreground">Orders</p><p class="text-xl font-bold">3,192</p><span class="badge-soft tone-success mt-1">8.1%</span></div></div>
      <div class="h-44 rounded-xl border border-dashed border-border" style="background:linear-gradient(180deg,var(--primary-soft),transparent)" role="img" aria-label="Sales chart preview"></div>
      <!-- swap for a real screenshot: <img src="/img/dashboard.webp" alt="Tala Commerce dashboard" class="rounded-xl"> -->
    </div>
  </div>
</section>
```

## 3. Logo strip

```html
<section class="border-y border-border py-8" aria-label="Customers"><div class="container-x">
  <p class="mb-5 text-center text-sm text-muted-foreground">Powering stores from Aparri to Baguio</p>
  <ul class="flex flex-wrap justify-center gap-x-10 gap-y-4 text-lg font-bold tracking-tight text-muted-foreground" id="logos"></ul></div></section>
<script>document.getElementById('logos').innerHTML = DEMO.logos.map((l) => `<li class="opacity-80 transition-opacity hover:opacity-100">${l}</li>`).join('');</script>
```

## 4. Features grid + one detail row

```html
<section id="features" class="section"><div class="container-x">
  <div class="mx-auto mb-14 max-w-2xl text-center"><span class="eyebrow mb-4">Features</span><h2 class="text-3xl font-bold tracking-tight sm:text-4xl">Everything a growing store needs</h2><p class="mt-3 text-muted-foreground">No spreadsheets, no end-of-day guesswork.</p></div>
  <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
    <!-- repeat x6: store/POS, package/Inventory, arrow-left-right/Transfers, file-text/BIR reports, shield-check/Roles, smartphone/Mobile -->
    <article class="card card-hover p-6"><span class="icon-chip mb-4"><i data-lucide="package" class="size-5" aria-hidden="true"></i></span>
      <h3 class="text-lg font-semibold">Live inventory</h3><p class="mt-2 text-muted-foreground">Stock levels update the second a sale rings up, across every branch.</p></article>
  </div>
  <div class="mt-20 grid items-center gap-12 lg:grid-cols-2"><!-- next row: add lg:order-2 to the visual -->
    <div class="glow h-72 rounded-3xl border border-border bg-surface" role="img" aria-label="Stock transfer screen"></div>
    <div><span class="eyebrow mb-4">Transfers</span><h3 class="text-3xl font-bold tracking-tight">Move stock between branches in two taps</h3>
      <ul class="mt-5 space-y-3 text-muted-foreground"><li class="flex gap-2"><i data-lucide="circle-check" class="size-5 text-success" aria-hidden="true"></i>Approval flow per branch manager</li><li class="flex gap-2"><i data-lucide="circle-check" class="size-5 text-success" aria-hidden="true"></i>Delivery receipts with photos</li></ul></div>
  </div>
</div></section>
```

## 5. Stats band

```html
<section class="pb-16"><div class="container-x"><dl class="bg-brand grid grid-cols-2 gap-8 rounded-3xl p-10 text-center lg:grid-cols-4">
  <div class="flex flex-col-reverse"><dt class="opacity-80">Stores</dt><dd class="text-4xl font-bold">1,200+</dd></div>
  <div class="flex flex-col-reverse"><dt class="opacity-80">Sales processed</dt><dd class="text-4xl font-bold">₱2.4B</dd></div>
  <div class="flex flex-col-reverse"><dt class="opacity-80">Uptime</dt><dd class="text-4xl font-bold">99.9%</dd></div>
  <div class="flex flex-col-reverse"><dt class="opacity-80">Average rating</dt><dd class="text-4xl font-bold">4.8/5</dd></div>
</dl></div></section>
```

## 6. Testimonials

```html
<section id="testimonials" class="section bg-surface-muted"><div class="container-x">
  <h2 class="mb-12 text-center text-3xl font-bold tracking-tight sm:text-4xl">Loved by store owners</h2>
  <div id="quotes" class="grid gap-6 md:grid-cols-3"></div></div></section>
<script>
document.getElementById('quotes').innerHTML = DEMO.testimonials.map((t) => `<figure class="card flex flex-col p-6">
  <div class="mb-4 flex gap-0.5 text-warning" aria-label="5 out of 5 stars">${'<i data-lucide="star" class="size-4 fill-current"></i>'.repeat(5)}</div>
  <blockquote class="flex-1">“${t.quote}”</blockquote>
  <figcaption class="mt-6 flex items-center gap-3"><span class="avatar">${fmt.initials(t.name)}</span><span><strong class="block text-sm">${t.name}</strong><span class="text-xs text-muted-foreground">${t.role}</span></span></figcaption></figure>`).join('');
lucide.createIcons();
</script>
```

## 7. Pricing (three tiers, highlighted plan)

```html
<section id="pricing" class="section"><div class="container-x">
  <div class="mb-12 text-center"><h2 class="text-3xl font-bold tracking-tight sm:text-4xl">Simple pricing in pesos</h2><p class="mt-3 text-muted-foreground">VAT inclusive. Cancel anytime.</p></div>
  <div id="plans" class="grid items-stretch gap-6 lg:grid-cols-3"></div></div></section>
<script>
document.getElementById('plans').innerHTML = DEMO.plans.map((p) => `<div class="card flex flex-col p-7 ${p.highlighted ? 'glow border-2 border-primary lg:-translate-y-3' : ''}">
  ${p.highlighted ? '<span class="badge-soft tone-primary mb-3 self-start">Most popular</span>' : ''}
  <h3 class="text-lg font-semibold">${p.name}</h3><p class="mt-1 text-sm text-muted-foreground">${p.blurb}</p>
  <p class="my-6"><span class="text-4xl font-bold tracking-tight">${p.price ? fmt.peso(p.price).replace('.00', '') : 'Free'}</span>${p.price ? `<span class="text-muted-foreground">/${p.period}</span>` : ''}</p>
  <ul class="mb-8 flex-1 space-y-3 text-sm">${p.features.map((f) => `<li class="flex gap-2"><i data-lucide="check" class="size-4 text-success" aria-hidden="true"></i>${f}</li>`).join('')}</ul>
  <a href="/register" class="btn ${p.highlighted ? 'btn-primary' : 'btn-surface'}">${p.cta}</a></div>`).join('');
lucide.createIcons();
</script>
```

## 8. FAQ accordion (native `<details>`, keyboard accessible)

```html
<section id="faq" class="section pt-0"><div class="container-x max-w-3xl">
  <h2 class="mb-8 text-center text-3xl font-bold tracking-tight">Frequently asked questions</h2>
  <div class="card divide-y divide-border">
    <details class="group p-5" open><summary class="flex cursor-pointer list-none items-center justify-between gap-4 rounded-md font-semibold focus-visible:outline-2">Does it work offline?<i data-lucide="chevron-down" class="size-5 text-muted-foreground transition-transform group-open:rotate-180" aria-hidden="true"></i></summary>
      <p class="mt-3 text-muted-foreground">Yes. Sales queue on the device and sync when the connection returns.</p></details>
    <details class="group p-5"><summary class="flex cursor-pointer list-none items-center justify-between gap-4 rounded-md font-semibold">Can I import my existing products?<i data-lucide="chevron-down" class="size-5 text-muted-foreground transition-transform group-open:rotate-180" aria-hidden="true"></i></summary>
      <p class="mt-3 text-muted-foreground">Upload a CSV or Excel file; we map the columns for you.</p></details>
    <!-- 4 to 6 items total -->
  </div></div></section>
```

## 9. CTA band + footer

```html
<section class="pb-20"><div class="container-x"><div class="bg-brand rounded-3xl px-6 py-14 text-center">
  <h2 class="text-3xl font-bold tracking-tight sm:text-4xl">Ready to close the month in two days?</h2><p class="mt-3 opacity-80">Free for 14 days. No credit card.</p>
  <div class="mt-8 flex flex-wrap justify-center gap-3"><a href="/register" class="btn btn-surface h-12 px-6">Start free trial</a><a href="/contact" class="btn btn-on-brand h-12 px-6">Talk to sales</a></div>
</div></div></section>

<footer class="border-t border-border bg-surface pt-16 pb-8"><div class="container-x">
  <div class="grid gap-10 lg:grid-cols-12">
    <div class="lg:col-span-4"><a href="/" class="mb-3 flex items-center gap-2 font-bold"><span class="bg-brand grid size-8 place-items-center rounded-lg"><i data-lucide="sparkles" class="size-4"></i></span>Tala Commerce</a>
      <p class="mb-4 text-sm text-muted-foreground">Retail operations for growing Filipino stores.</p>
      <form class="flex gap-2" aria-label="Newsletter"><input type="email" class="input" placeholder="you@store.ph" aria-label="Email" required><button class="btn btn-primary">Subscribe</button></form></div>
    <div class="lg:col-span-2 lg:col-start-6"><h3 class="mb-3 text-sm font-semibold">Product</h3><ul class="space-y-2 text-sm"><li><a class="link-muted" href="#features">Features</a></li><li><a class="link-muted" href="#pricing">Pricing</a></li><li><a class="link-muted" href="/changelog">Changelog</a></li></ul></div>
    <div class="lg:col-span-2"><h3 class="mb-3 text-sm font-semibold">Company</h3><ul class="space-y-2 text-sm"><li><a class="link-muted" href="/about">About</a></li><li><a class="link-muted" href="/careers">Careers</a></li><li><a class="link-muted" href="/contact">Contact</a></li></ul></div>
    <div class="lg:col-span-3"><h3 class="mb-3 text-sm font-semibold">Support</h3><ul class="space-y-2 text-sm"><li><a class="link-muted" href="/help">Help center</a></li><li><a class="link-muted" href="/status">System status</a></li><li><a class="link-muted" href="mailto:hello@tala.example">hello@tala.example</a></li></ul></div>
  </div>
  <div class="mt-12 flex flex-wrap items-center justify-between gap-4 border-t border-border pt-6 text-sm text-muted-foreground">
    <p>© 2026 Tala Commerce (demo). Cauayan City, Isabela.</p>
    <!-- Lucide has no brand logos: paste Simple Icons SVGs for the provider/social glyphs -->
    <div class="flex items-center gap-4"><a class="link-muted" href="/privacy">Privacy</a><a class="link-muted" href="/terms">Terms</a>
      <a class="link-muted" href="#" aria-label="Facebook"><i data-lucide="message-circle" class="size-4"></i></a><a class="link-muted" href="#" aria-label="LinkedIn"><i data-lucide="briefcase" class="size-4"></i></a><a class="link-muted" href="#" aria-label="YouTube"><i data-lucide="circle-play" class="size-4"></i></a></div>
  </div></div></footer>
```

## 10. Auth split page

```html
<main class="grid min-h-screen lg:grid-cols-2">
  <section class="bg-brand hidden flex-col justify-between p-12 lg:flex" aria-label="About Tala Commerce">
    <a href="/" class="flex items-center gap-2 font-bold"><i data-lucide="sparkles" class="size-5"></i>Tala Commerce</a>
    <div><h2 class="text-4xl font-bold tracking-tight">Every branch, one login.</h2><p class="mt-4 text-lg opacity-80">“We closed the month in two days instead of a week.”</p><p class="mt-2 text-sm opacity-80">Rhea Manalo, Kawayan Café (demo)</p></div>
    <p class="text-sm opacity-80">© 2026 Tala Commerce (demo)</p>
  </section>
  <section class="flex items-center justify-center p-6">
    <div class="w-full max-w-sm">
      <div class="mb-8 flex justify-end"><!-- 3-state theme toggle --></div>
      <h1 class="text-2xl font-bold tracking-tight">Welcome back</h1><p class="mt-1 text-muted-foreground">Sign in to your store dashboard.</p>
      <div class="mt-6 grid gap-2"><button class="btn btn-surface"><span class="font-bold" aria-hidden="true">G</span>Continue with Google</button><button class="btn btn-surface"><span class="font-bold" aria-hidden="true">M</span>Continue with Microsoft</button></div>
      <div class="my-6 flex items-center gap-3 text-xs text-muted-foreground"><span class="h-px flex-1 bg-border"></span>or<span class="h-px flex-1 bg-border"></span></div>
      <form id="loginForm" class="space-y-4" novalidate>
        <div><label class="label" for="le">Email</label><input id="le" type="email" class="input h-11" autocomplete="email" required aria-describedby="le-err"><p id="le-err" class="mt-1 hidden text-xs text-error">Enter your email.</p></div>
        <div><div class="flex justify-between"><label class="label" for="lp">Password</label><a href="/forgot-password" class="text-sm font-medium text-primary hover:underline">Forgot password?</a></div>
          <div class="relative"><input id="lp" type="password" class="input h-11 pr-11" autocomplete="current-password" required minlength="8" aria-describedby="lp-err">
            <button type="button" class="btn btn-ghost btn-icon absolute right-0.5 top-0.5" aria-label="Show password" aria-pressed="false" onclick="const i=document.getElementById('lp');i.type=i.type==='password'?'text':'password';this.setAttribute('aria-pressed',i.type==='text')"><i data-lucide="eye" class="size-4"></i></button></div>
          <p id="lp-err" class="mt-1 hidden text-xs text-error">At least 8 characters.</p></div>
        <label class="flex items-center gap-2 text-sm"><input type="checkbox" class="check">Remember me for 30 days</label>
        <button type="submit" class="btn btn-primary h-11 w-full">Sign in</button>
      </form>
      <p class="mt-6 text-center text-sm text-muted-foreground">No account yet? <a href="/register" class="font-medium text-primary hover:underline">Create one free</a></p>
    </div>
  </section>
</main>
```

Validation and loading state: reuse the submit handler from block 3 of [tailwind-data.md](tailwind-data.md) (point it at `#loginForm`).
