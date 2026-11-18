---
trigger: model_decision
description: Apply when writing feature/system plans in docs/plans/, updating project README/API documentation, or designing cross-system API/ERP synchronization (outbox + webhooks).
---

# RULE 04 — PLANNING, DOCUMENTATION & CROSS-SYSTEM INTEGRATION

## 1. Lightweight Feature & System Plans

When planning a new system, multi-module feature, or user-requested `/plan`:
- Save the plan to `docs/plans/YYYY-MM-DD-<short-slug>.md` (update the existing plan file instead of creating `-v2-final.md` duplicates).
- Keep the plan concise and actionable:
  1. **Goal:** 1–3 sentences stating what will work when finished.
  2. **UI Stack & Component Types:** Chosen UI stack + which screen/component types from `component-catalog/00-MASTER-SCREEN-AND-COMPONENT-TYPES.md` will be built.
  3. **Data & API Summary:** Tables/columns and endpoints touched.
  4. **Implementation Steps:** Ordered steps with concrete, verifiable completion criteria.
  5. **Risks / Backups:** Any migration, auth, or VPS considerations.

## 2. Project Documentation Minimum

Keep `README.md` accurate to the real code (stack, required `.env` variable names without secrets, local setup, build/deploy commands). Update `CHANGELOG.md` / `CHANGES.md` when cutting versioned releases.

## 3. Architecture Fit: Standalone vs. Cross-System Sync

- **Default (Standalone App):** Keep standalone apps simple and self-contained with one clean database and modular services. Do **not** add unused outbox tables or sync workers unless external system integration is required.
- **Cross-System / ERP Integration (When Requested):**
  1. **Separate Databases & Single Table Ownership:** Each system owns its tables; never do cross-database writes.
  2. **Transactional Outbox:** Write outbound events to an `outbox` table in the same DB transaction as the business record, processed asynchronously with exponential backoff and an `Idempotency-Key` header.
  3. **Signed Webhooks & Versioned Endpoints:** Verify HMAC signatures on inbound webhooks, make handlers idempotent, and version integration APIs under `/api/v1/...`.
