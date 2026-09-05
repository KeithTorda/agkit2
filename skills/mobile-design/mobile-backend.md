# Mobile Backend Patterns

> Backend and API patterns specific to mobile clients. Generic backend guidance is in `@[skills/nodejs-best-practices]` and `@[skills/api-patterns]`; this file covers what mobile changes.

Mobile clients differ from web: unreliable networks (2G, subway, elevator), battery limits, small storage, interrupted sessions, a wide device range, and slow binary updates (store review). The backend must compensate.

AI defaults to avoid: one API shared with web returning full objects (mobile needs compact, field-selectable responses), no offline consideration, WebSocket for everything (battery drain: prefer push plus polling fallback), no app versioning, generic error messages, session cookies (mobile apps restart: use tokens), and ignoring device info in headers.

---

## 1. Push Notifications

Send through FCM (Android) and APNs (iOS, directly or via FCM); FCM alone does not guarantee iOS delivery. Types: display (banner), silent (background sync), and data (app-handled).

Rules: never put sensitive data in a push (send "New message", let the app fetch content); batch, dedupe, and respect quiet hours; segment by preference and timezone; clean up invalid tokens.

Token lifecycle: the app registers and sends the token to the backend, re-registers on start because tokens rotate, and the backend removes tokens that error as invalid; store multiple tokens per user for multiple devices.

---

## 2. Offline Sync and Conflict Resolution

Choose a strategy by data type: read-only data uses a cache plus TTL with ETag/Last-Modified; user-owned data uses last-write-wins or timestamp merge; collaborative data needs CRDT or OT (consider Firebase/Supabase); critical data (payments, inventory) keeps the server authoritative with optimistic UI plus confirmation.

| Strategy | How it works | Best for |
|----------|--------------|----------|
| Last-write-wins | Latest timestamp overwrites | Simple, single-user data |
| Server-wins | Server is authoritative | Critical transactions |
| Client-wins | Offline changes win | Offline-heavy apps |
| Merge | Field-by-field | Documents, rich content |
| CRDT | Conflict-free by construction | Real-time collaboration |

Sync queue: write the change to the local DB, enqueue `{ action, data, timestamp, retries }`, process FIFO when online, remove on success, retry with backoff (cap ~5), and apply the conflict strategy on the server's response.

---

## 3. Mobile API Optimization

Shrink responses: field selection (`?fields=id,name,thumbnail`), gzip/brotli, cursor pagination, image variants (`/image?w=200&q=80`), and delta sync (only records changed since a timestamp).

Prefer cursor pagination over offset: offset duplicates rows when items are inserted and slows on large offsets; a cursor (`?limit=20&after=abc123`) stays consistent and fast. Batch related reads into one request instead of many round trips.

---

## 4. App Versioning

Expose a config endpoint that reads `X-App-Version`, `X-Platform`, and `X-Device-ID` and returns `minimum_version`, `latest_version`, `force_update`, `update_url`, `feature_flags`, and a maintenance flag. If the client is below the minimum, block with a forced-update screen; below latest, prompt optionally. Feature flags let you toggle features and run gradual rollouts without a store release.

---

## 5. Authentication for Mobile

Short-lived access token held in memory; long-lived refresh token in SecureStore/Keychain, rotated on each use; a device token so the user can log out all devices. On a 401, silently call the refresh endpoint and retry the original request; force logout only when refresh fails. The user should not notice a routine token expiry.

---

## 6. Error Handling for Mobile

Return a code, a user-safe message, an optional recovery action, and retry guidance:

```json
{
  "error": {
    "code": "PAYMENT_DECLINED",
    "message": "Your payment was declined",
    "user_message": "Please check your card details or try another method",
    "action": { "type": "navigate", "destination": "payment_methods" },
    "retry": { "allowed": true, "after_seconds": 5 }
  }
}
```

Handle by category: 400s need user action; 401 triggers silent refresh or re-login; 403 shows an upgrade/permission screen; 404 removes the item from local cache; 409 shows a sync-conflict UI; 429 honors `Retry-After`; 500s retry with backoff; no connection falls back to cached data and queues for sync.

---

## 7. Media and Binary Handling

Serve resized, cached images (`?w=400&h=300&q=80&format=webp`; WebP on Android, HEIC where supported, JPEG fallback; long `Cache-Control`). Upload large files in resumable chunks (init returns an upload id and chunk size, PUT each 1-5 MB chunk, POST complete to assemble). Stream audio/video with HLS (iOS) or DASH/HLS (Android), adaptive bitrate, range requests for seeking, and downloadable chunks for offline.

---

## 8. Security for Mobile

Attest real devices (iOS DeviceCheck, Android Play Integrity) and fail closed. Sign sensitive requests with an HMAC over timestamp, path, and body plus `X-Timestamp` and `X-Device-ID`, and reject stale or mismatched signatures. Rate-limit per device and per user, stricter on auth and expensive endpoints, and return the IETF `RateLimit` headers (with legacy `X-RateLimit-*` if clients need them) plus `Retry-After` on 429.

---

## 9. Monitoring and Analytics

Have mobile send `X-App-Version`, `X-Platform`, `X-OS-Version`, `X-Device-Model`, `X-Device-ID`, `X-Request-ID`, `Accept-Language`, and `X-Timezone`. Log endpoint, method, status, latency, error details, and user id. Alert on error rate over ~5 % per version, p95 latency over ~2 s, a version-specific crash spike, an auth-failure spike, and push-delivery failures.

---
> Mobile backends must survive bad networks, respect battery, and handle interrupted sessions. The client cannot be trusted, but it also cannot be left hanging: give it offline capability and clear error recovery.
