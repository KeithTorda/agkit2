---
name: mcp-builder
description: Build interoperable MCP servers or clients using the actual peer, SDK, transport and negotiated protocol revision. Use for tool/resource/prompt contracts, transport integration and protocol migrations; verify revision-specific features before adoption.
version: 2.8.2
---

# MCP Builder

Build a service a real host can discover, invoke and recover from. Inspect host revisions, installed SDK, existing configuration and transport before writing registration code. The official [MCP specification](https://modelcontextprotocol.io/specification) is the protocol authority; installed SDK documentation defines concrete APIs.

## Compatibility first

Record supported protocol revision and optional features. Read the relevant revision instead of assuming host, server and SDK share a contract. Keep adapters explicit and test supported peer combinations.

The 2026-07-28 specification uses self-contained requests, per-request version/capability metadata and `server/discover`. Its Tasks, Skills and Apps extensions are opt-in. Adopt these with verified SDK/host support. Older supported revisions may have a different initialization/session model: do not combine old handshakes with newer request semantics by guesswork. Exact metadata keys, errors and result shapes come from the selected revision.

Durable work needs explicit identifiers, ownership, expiry and cleanup. A connection/shared process alone is not authorization or a safe user/conversation boundary. Test interleaved work and reconnection under the selected revision's semantics.

## Contracts before adapters

- Tools have clear operations, bounded inputs, predictable output and visible side effects. Prefer narrow useful operations to unrestricted command execution.
- Resources have stable URI/MIME contracts and access checks. Discovery metadata must not reveal protected content.
- Prompts are templates, not permission authority. Treat external tool/resource/prompt content as untrusted data.
- Validate schemas and payloads using the chosen revision's dialect. State required fields, bounds and allowed values; schema defaults/annotations do not enforce behavior automatically.
- When supported, validate typed structured results as well as inputs. Follow the selected SDK/revision's distinction between protocol errors and tool operational failures.

Use real registration APIs documented for the installed SDK. Keep domain logic separate from transport so it is testable without a host.

## Transport and security

For stdio, protocol output uses stdout and diagnostics use stderr. Set process environment, working directory, lifecycle and credential access deliberately. For HTTP, follow the selected revision's authorization/origin/transport rules; exercise the real host/proxy. A custom WebSocket bridge is not automatically a standard transport.

Enforce actor/tenant/resource authorization in the service. Tool annotations and self-reported metadata are hints, not identity/permission evidence. Follow host authorization policy instead of requiring new confirmation for every invocation.

Validate paths, symlinks, redirects, URL destinations, response sizes and deadlines at actual trust boundaries. Disable automatic network schema-reference fetching unless necessary and constrained. Keep secrets out of descriptions, arguments, logs and errors. Use redacted correlation IDs for diagnosis.

## Long operations and migration

Use only negotiated behavior for task handles, progress, cancellation and UI. When absent, offer a supported fallback or state the limitation. Define whether cancellation stops work or only waiting. Reconcile status or use idempotency before retrying a write with unknown outcome.

Compare old/target revisions, change adapter boundaries and retain needed compatibility. Do not remove working legacy behavior merely because a newer spec exists.

## Prove interoperability

Exercise discovery/capability mismatch, valid calls, invalid arguments, denied access, upstream failure, timeout, reconnect and malformed output. Check stdout integrity and secret-safe errors. Test duplicate writes/retries and cross-user isolation where relevant. Report the real host/SDK/revision tested and material gaps; schema validation alone is not interoperability.
