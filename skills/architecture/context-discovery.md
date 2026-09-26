# Context Discovery

Establish this context before proposing a structure. Infer it from the brief, the code, `docs/plans/`, `docs/proplan/`, and project memory; ask only for the items that would change the design (at most 3 questions, each with a recommended default, per `core-protocol`).

## Context to establish

1. **Users and scale** - who uses it (public, staff, admins, several roles), how many (10, 1K, 100K+), peak moments (enrolment week, election day, payday sales), data volume.
2. **Team and operations** - solo developer or team; who maintains it after handover; the client's ability to run a server (shared hosting, VPS, managed platform).
3. **Timeline** - prototype, MVP with a deadline, or long-lived system.
4. **Domain** - CRUD-heavy or rule-heavy; money (sales, VAT, receipts); government or personal data (Data Privacy Act of 2012 obligations); audit trail needs; real-time needs.
5. **Environment** - connectivity (offline or flaky internet at the point of use?), devices (phones, shared desktop, POS terminal, printers), languages (English, Filipino).
6. **Constraints** - budget, hosting the client already pays for, legacy systems or spreadsheets to import, required integrations (payment gateways, SMS, e-mail, BIR requirements), stack preferences.

## Project classification

| | Small site / portal | Business system | SaaS | Larger platform |
|---|---|---|---|---|
| Examples | Barangay or school site, LGU info portal, landing page | POS, inventory, enrolment, records system for one client | Multi-tenant product sold to many clients | Many teams, 100K+ active users |
| Users | Public, few editors | Staff with roles | Tenants with roles | Many audiences |
| Team | Solo | Solo or 2-3 | 2-10 | 10+ |
| Structure | Static or server-rendered site | Monolith (Laravel or Next.js) | Modular monolith | Modular monolith, services where proven |
| Patterns | Minimal | Transactions, audit log, roles | Tenant isolation, background jobs | Chosen per domain |

Most of Nikko's work sits in the first two columns: design for correctness, maintainability and cheap hosting before scale.
