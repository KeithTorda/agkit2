# Demo data (one file, easy to replace)

All blocks read from one module so the page looks real on day one and the swap to live data is a single file. Brands are fictional (`Tala Commerce` and friends); never use real company names or logos.

Rules:
- Philippine context: `₱` amounts via `Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' })`, Filipino names, Cagayan Valley branches, `en-PH` dates.
- Realistic statuses and mixed values (not all "Paid", not round numbers).
- Keys match what the real API will return, so wiring is a fetch swap (see the end of this file).

## JS / TS: `assets/js/demo-data.js` (or `src/lib/demo-data.ts`)

```js
export const DEMO = {
  brand: { name: 'Tala Commerce', tagline: 'Retail operations for growing Filipino stores' },
  user: { name: 'Andrea Reyes', role: 'Branch Manager', email: 'andrea@tala.example', initials: 'AR' },
  branches: ['Cauayan', 'Santiago', 'Tuguegarao', 'Ilagan'],

  kpis: [
    { id: 'revenue',   label: 'Revenue (MTD)',   value: 1284650.75, format: 'currency', trend: 12.4,  icon: 'cash-stack',   spark: [32, 41, 38, 45, 52, 49, 61, 66] },
    { id: 'orders',    label: 'Orders',          value: 3192,       format: 'number',   trend: 8.1,   icon: 'bag-check',    spark: [20, 24, 22, 30, 28, 33, 35, 39] },
    { id: 'customers', label: 'New customers',   value: 418,        format: 'number',   trend: -3.2,  icon: 'people',       spark: [18, 22, 19, 17, 21, 16, 15, 14] },
    { id: 'aov',       label: 'Avg. order value', value: 402.46,    format: 'currency', trend: 4.7,   icon: 'receipt',      spark: [10, 12, 11, 13, 15, 14, 16, 17] },
  ],

  salesByMonth: {
    labels: ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
    series: [
      { name: 'Cauayan',    data: [182400, 196250, 214900, 208300, 231750, 248600] },
      { name: 'Santiago',   data: [154300, 160800, 171200, 186900, 179450, 193100] },
      { name: 'Tuguegarao', data: [121900, 133400, 129800, 141250, 152600, 167300] },
    ],
  },

  orders: [
    { id: 'ORD-10482', customer: 'Maria Santos',      email: 'maria.s@mail.example',   branch: 'Cauayan',    amount: 4850.00,  status: 'paid',       date: '2026-10-26' },
    { id: 'ORD-10481', customer: 'Juan dela Cruz',    email: 'jdc@mail.example',       branch: 'Santiago',   amount: 1275.50,  status: 'pending',    date: '2026-10-26' },
    { id: 'ORD-10480', customer: 'Kristine Bautista', email: 'kbautista@mail.example', branch: 'Tuguegarao', amount: 12940.00, status: 'shipped',    date: '2026-10-25' },
    { id: 'ORD-10479', customer: 'Paolo Mendoza',     email: 'paolo.m@mail.example',   branch: 'Ilagan',     amount: 689.25,   status: 'refunded',   date: '2026-10-25' },
    { id: 'ORD-10478', customer: 'Jasmine Ramos',     email: 'jas.ramos@mail.example', branch: 'Cauayan',    amount: 3320.00,  status: 'paid',       date: '2026-10-24' },
    { id: 'ORD-10477', customer: 'Mark Villanueva',   email: 'markv@mail.example',     branch: 'Santiago',   amount: 8105.75,  status: 'processing', date: '2026-10-24' },
    { id: 'ORD-10476', customer: 'Liza Domingo',      email: 'liza.d@mail.example',    branch: 'Tuguegarao', amount: 2460.00,  status: 'cancelled',  date: '2026-10-23' },
    { id: 'ORD-10475', customer: 'Ramon Castillo',    email: 'rcastillo@mail.example', branch: 'Cauayan',    amount: 15780.40, status: 'paid',       date: '2026-10-22' },
  ],
  ordersTotal: 128,

  activity: [
    { who: 'Carlo Pascual', what: 'restocked 120 units of Arabica 1kg', where: 'Santiago',   when: '2026-10-27T09:12:00+08:00' },
    { who: 'Andrea Reyes',  what: 'approved PO-2291 (₱86,400.00)',       where: 'Cauayan',    when: '2026-10-27T08:40:00+08:00' },
    { who: 'Liza Domingo',  what: 'issued refund for ORD-10479',         where: 'Ilagan',     when: '2026-10-26T17:05:00+08:00' },
  ],

  notifications: [
    { title: 'Low stock: Pandesal Mix 5kg', meta: 'Tuguegarao · 12 left', icon: 'exclamation-triangle', tone: 'warning', unread: true },
    { title: 'Payout of ₱214,900.00 sent',  meta: 'Daloy Pay (demo) · 2h ago', icon: 'bank', tone: 'success', unread: true },
    { title: 'New staff account: M. Villanueva', meta: 'Santiago · yesterday', icon: 'person-plus', tone: 'info', unread: false },
  ],

  testimonials: [
    { name: 'Rhea Manalo',   role: 'Owner, Kawayan Café (demo)',   quote: 'We closed the month in two days instead of a week. Our branches finally see the same numbers.' },
    { name: 'Dennis Tolentino', role: 'Ops Lead, Alon Logistics (demo)', quote: 'Stock transfers between Cauayan and Santiago used to be a spreadsheet war. Not anymore.' },
    { name: 'Grace Lim',     role: 'Finance, Habi Studio (demo)',   quote: 'BIR-ready reports out of the box. Our accountant actually thanked us.' },
  ],

  plans: [
    { name: 'Starter', price: 0,    period: 'month', blurb: 'For a single store getting organized.', features: ['1 branch', '500 orders / mo', 'Email support'], cta: 'Start free' },
    { name: 'Growth',  price: 1490, period: 'month', blurb: 'For multi-branch teams.', features: ['Up to 5 branches', 'Unlimited orders', 'Inventory transfers', 'Priority chat support'], cta: 'Start 14-day trial', highlighted: true },
    { name: 'Scale',   price: 3990, period: 'month', blurb: 'For regional chains.', features: ['Unlimited branches', 'Role-based access', 'API + webhooks', 'Dedicated success manager'], cta: 'Talk to sales' },
  ],

  logos: ['Bituin Labs', 'Kawayan Co.', 'Alon Logistics', 'Habi Studio', 'Liwayway Foods', 'Daloy Pay'],
};

export const STATUS_TONE = {
  paid: 'success', shipped: 'info', processing: 'primary', pending: 'warning', refunded: 'muted', cancelled: 'error',
};

export const fmt = {
  peso: (n) => new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' }).format(n),
  num: (n) => new Intl.NumberFormat('en-PH').format(n),
  date: (d) => new Intl.DateTimeFormat('en-PH', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(d)),
  initials: (name) => name.split(' ').filter(Boolean).map((p) => p[0]).slice(0, 2).join('').toUpperCase(),
};
```

No bundler? Drop `export` and assign `window.DEMO = { ... }`, `window.fmt = { ... }`, `window.STATUS_TONE = { ... }`, then load it with a plain `<script src="assets/js/demo-data.js">` before the page script.

TypeScript: add `export type Order = (typeof DEMO.orders)[number];` and type the API response with the same shape.

## PHP / Laravel / Blade: `app/Support/DemoData.php` (or `config/demo.php`)

```php
<?php
return [
    'brand' => ['name' => 'Tala Commerce', 'tagline' => 'Retail operations for growing Filipino stores'],
    'user'  => ['name' => 'Andrea Reyes', 'role' => 'Branch Manager', 'initials' => 'AR'],
    'branches' => ['Cauayan', 'Santiago', 'Tuguegarao', 'Ilagan'],
    'kpis' => [
        ['label' => 'Revenue (MTD)',    'value' => 1284650.75, 'format' => 'currency', 'trend' => 12.4, 'icon' => 'cash-stack'],
        ['label' => 'Orders',           'value' => 3192,       'format' => 'number',   'trend' => 8.1,  'icon' => 'bag-check'],
        ['label' => 'New customers',    'value' => 418,        'format' => 'number',   'trend' => -3.2, 'icon' => 'people'],
        ['label' => 'Avg. order value', 'value' => 402.46,     'format' => 'currency', 'trend' => 4.7,  'icon' => 'receipt'],
    ],
    'orders' => [
        ['id' => 'ORD-10482', 'customer' => 'Maria Santos',      'branch' => 'Cauayan',    'amount' => 4850.00,  'status' => 'paid',      'date' => '2026-10-26'],
        ['id' => 'ORD-10481', 'customer' => 'Juan dela Cruz',    'branch' => 'Santiago',   'amount' => 1275.50,  'status' => 'pending',   'date' => '2026-10-26'],
        ['id' => 'ORD-10480', 'customer' => 'Kristine Bautista', 'branch' => 'Tuguegarao', 'amount' => 12940.00, 'status' => 'shipped',   'date' => '2026-10-25'],
        ['id' => 'ORD-10479', 'customer' => 'Paolo Mendoza',     'branch' => 'Ilagan',     'amount' => 689.25,   'status' => 'refunded',  'date' => '2026-10-25'],
        ['id' => 'ORD-10476', 'customer' => 'Liza Domingo',      'branch' => 'Tuguegarao', 'amount' => 2460.00,  'status' => 'cancelled', 'date' => '2026-10-23'],
    ],
    'status_tone' => ['paid' => 'success', 'shipped' => 'info', 'processing' => 'primary', 'pending' => 'warning', 'refunded' => 'muted', 'cancelled' => 'error'],
];
```

Blade usage:

```blade
@php($demo = require app_path('Support/DemoData.php'))
@foreach ($demo['orders'] as $o)
  <tr>
    <td>{{ $o['customer'] }}</td>
    <td class="text-end">₱{{ number_format($o['amount'], 2) }}</td>
    <td><span class="badge-soft badge-soft-{{ $demo['status_tone'][$o['status']] }}">{{ ucfirst($o['status']) }}</span></td>
    <td>{{ \Carbon\Carbon::parse($o['date'])->format('M j, Y') }}</td>
  </tr>
@endforeach
```

## Wiring to real data

1. Keep the render functions; change only the source: `const orders = await fetch('/api/orders?page=1').then(r => r.json());` (or the controller passes `$orders` instead of `$demo['orders']`).
2. Show the skeleton block while the request runs, the empty state when the list is empty, and an error alert with a Retry button on failure.
3. Delete `demo-data.*` (or keep it behind a `?demo=1` / `APP_DEMO=true` flag for screenshots) once every screen reads live data.
