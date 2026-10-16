# Worked architecture choices

These examples illustrate reasoning, not templates to impose. No specific framework, hosting provider, country or organization size follows from a project label.

## Public information site with editors

Outcome: fast public pages, occasional publishing, a few searchable records. Compare repository-managed content/static output with a managed CMS or a small server-rendered application. The decisive question is who must publish and how quickly changes must appear.

If editors can use the current publishing workflow and data is refreshed in batches, static output plus indexed lookup data may be sufficient. If editors need approval/history or live records, a CMS/database boundary may justify its operating cost. Validate content update time, preview, accessibility and recovery from a bad publication. Revisit when publishing or data freshness requirements change.

## Sales and inventory with unreliable connectivity

Invariant: one accepted sale reserves stock once and totals remain exact. A single application/database transaction can enforce local consistency. Choose conditional writes/locking based on the actual database and concurrent checkout behavior.

Offline sales introduce a separate business choice: allow provisional orders, partition stock by terminal, or accept bounded oversell and reconciliation? A local queue alone cannot preserve a global stock invariant while terminals are disconnected. Record client operation IDs, retry/deduplication, pending state and explicit conflict handling. Validate duplicate delivery and a failure between sale and stock updates. Receipt/tax requirements come from the actual business/legal context, not the example.

## Multi-tenant product

Invariant: an actor accesses only permitted tenant data. Compare shared tables with scoped constraints/queries, separate schemas and separate databases against isolation, operating cost, recovery and residency requirements. Database row policies can add protection where supported; application authorization remains a real boundary.

Check tenant scoping in joins, background jobs, exports, caches and files, not only primary requests. Include tenant scope in relevant uniqueness and references. Exercise cross-tenant negative tests and a tenant-level recovery scenario. Revisit isolation when a concrete contractual or load requirement changes.

## Independent teams or distinct workloads

A service boundary may help when release/scale/runtime isolation is necessary and ownership is clear. Compare it with an internal module and a separate worker deployment. Splitting one shared database across services without ownership can increase coordination instead of reducing it.

Define the authoritative data owner, synchronous/event contract, schema evolution, timeout/retry and compensation. Validate a dependency outage and duplicate/out-of-order events. Measure whether the chosen boundary resolves the original bottleneck. Revisit when evidence shows the operational cost exceeds its benefit.
