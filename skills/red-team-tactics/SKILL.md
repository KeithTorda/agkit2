---
name: red-team-tactics
description: Plan and assess authorized adversary simulations with scoped objectives, safe evidence, detection validation and cleanup. Use for requested penetration tests or red-team exercises; ordinary development does not trigger an offensive engagement.
version: 2.8.2
---

# Authorized Adversary Simulation

Use a threat scenario to evaluate real exposure and defensive visibility. Begin from the engagement's existing authorization, objectives and rules of engagement. A framework/tool catalog does not establish permission or justify unnecessary intrusive activity.

## Bound the engagement

Establish target systems, identities, allowed methods, testing window, evidence handling and stop conditions. Infer already documented scope; clarify only a consequential gap. Distinguish a local code audit, laboratory validation and active production testing. Use the least disruptive method that can answer the objective.

Specify where test accounts, data and cleanup records live. Define escalation for service degradation, unexpected sensitive data, scope ambiguity or an uncontrolled side effect. Avoid collecting credentials/data beyond the evidence required to establish impact.

## Threat-led hypotheses

Map the relevant entry point, trust boundary, identity privilege and asset. Form a concrete hypothesis such as: a tenant-scoped token may access another tenant's export because authorization is applied only in the UI. Compare benign explanations and existing compensating controls before assuming exploitability.

ATT&CK and similar catalogs can organize coverage, but tactics are not a mandatory linear lifecycle. Select only techniques relevant to the scenario and authorized environment. Verify current technique identifiers/tool behavior from official sources when the report needs exact mapping; do not copy dated version inventories.

## Progress from evidence

Start with documentation, architecture, existing logs and code where available. Validate exposure/version/configuration before attempting an exploit. Prefer a contained proof that establishes the boundary failure. If active validation is warranted, use explicit request/rate/resource limits, monitored conditions and the agreed rollback/cleanup plan.

Identity and directory assessments should establish the actual privilege relationship and prerequisites. A reachable service, known CVE name or graph edge is not proof of a viable attack path. Record the conditions needed and controls that blocked progress.

Persistence, credential access, lateral movement, evasion and phishing are distinct high-impact techniques, not automatic next steps. Apply only those required by the approved objective and permitted scope. Do not expand targets because an initial result suggests an interesting path.

## Test detection as well as prevention

Correlate timestamps and test identities with the defender's telemetry. Separate attack blocked, activity logged, alert generated, alert triaged and response completed; one does not prove another. Missing telemetry in the tester's view does not prove no detection exists.

Keep evidence minimal and redacted, with a reproducible timeline and clear provenance. Track modified accounts/configuration/artifacts and verify cleanup. Explain any irreversible or uncertain residual effects directly.

## Report actionable results

For each supported finding include scope, prerequisites, reproduction/evidence, impacted asset, plausible consequence, controls encountered and a targeted remediation/detection improvement. Mark code-reasoned hypotheses separately from observed exploitation. Severity depends on exposure and impact, not technique prestige or tool output alone.

Conclude with tested coverage, limitations, cleanup status and retest criteria. Use `vulnerability-scanner` for source/dependency triage and `api-patterns/security-testing.md` for application API access tests. A clean exercise proves only the scenarios and controls actually exercised.
