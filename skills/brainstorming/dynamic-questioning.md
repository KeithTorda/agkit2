# Dynamic Question Generation

> Questions reveal architectural consequences. Each one connects to a decision that changes cost, complexity, or scope. The rule for *when* to ask lives in the global `core-protocol` rule; [SKILL.md](./SKILL.md) points to it and covers the craft.

## Principles

1. **Consequence, not preference.** Not "Which auth method?" but "Email/password (reset flow, hashing, 2FA) or social login (OAuth providers, profile mapping)? Trade-off: control vs. delivery time."
2. **Context first.** Greenfield → foundation (stack, hosting, scale). Feature → integration points, existing patterns, breaking changes. Refactor → what is broken and why. Debug → symptom → reproduction → cause.
3. **Minimum viable questions.** Before: paths A (5 min) / B (15 min) / C (1 h). After: one path. If a question doesn't reduce implementation paths, delete it.
4. **Data, not assumptions.** "Stripe (best docs, US-centric) or Lemon Squeezy / Paddle (merchant of record, handles VAT)?" beats "probably Stripe".

## Generation

```
1. Parse   → domain, explicit and implied features, scale indicators
2. Decide  → blocking (needed before code) · high-leverage (shapes >30% of the build) · deferable
3. Rank    → blocking first, then high-leverage; deferable points become stated assumptions
4. Format  → question · why it matters · options with trade-offs · default if unanswered
```

Deferable points are not questions; they are assumptions written into the plan.

## Domain question banks

### E-commerce
| Question | Why it matters |
|---|---|
| Single or multi-vendor? | Commission logic, vendor dashboards, split payments |
| Inventory tracking? | Stock tables, reservations, low-stock alerts |
| Digital or physical products? | Download links vs. shipping APIs and tracking |
| Subscription or one-time? | Recurring billing, dunning, proration |

### Authentication
| Question | Why it matters |
|---|---|
| Social login? | OAuth providers vs. password-reset infrastructure |
| Roles and permissions? | RBAC tables, policy enforcement, admin UI |
| 2FA? | TOTP/SMS, backup codes, recovery flow |
| Email verification? | Tokens, email service, resend logic |

### Real-time
| Question | Why it matters |
|---|---|
| WebSocket or polling? | Connection management and scaling vs. simplicity and latency |
| Concurrent users? | <100 single server · >1k pub/sub · >10k dedicated infrastructure |
| Message persistence? | History tables, storage, pagination |

### Content / CMS
| Question | Why it matters |
|---|---|
| Rich text or Markdown? | Sanitization and XSS surface vs. simple rendering |
| Draft/publish workflow? | Status field, scheduling, versioning |
| Media uploads? | Upload endpoints, storage, optimization |
| Multi-language? | i18n tables, translation UI, fallbacks |

## Worked example

Request: "Build an Instagram clone."

```
Parse     → social media; photo sharing, likes, comments, profiles; implied feed, follows, auth; scale may spike
Blocking  → photo storage, feed type, auth method
Leverage  → real-time notifications, media processing
Deferable → video/reels, direct messages (assumption: v2)
```

Message sent (three questions, one round):

```markdown
**1. Photo storage** — Where are photos stored and served?
Why: hosting cost, load speed, CDN complexity (1k users × 10 photos × 2 MB = 20 GB).
Options: Cloudinary (fast, low setup) · S3 + CloudFront (cheapest at scale, more setup) · Supabase Storage (simple, small scale)
Default: Cloudinary.

**2. Feed** — Chronological, follow-only, or algorithmic?
Why: query complexity and caching; algorithmic needs ranking signals and precomputed tables.
Default: follow-only.

**3. Auth** — Email/password, social only, magic link, or hosted (Clerk / Better Auth)?
Why: effort, security posture, sign-up friction.
Default: hosted.

Assumptions unless you object: polling instead of WebSockets for notifications; video and DMs deferred to v2.
```

## Later rounds

Do not front-load everything. When implementation reveals a fork, ask at the moment it matters, in the same format and with a default: "This implies X — handle the edge case now or defer?"
