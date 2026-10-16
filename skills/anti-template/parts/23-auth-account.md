---
part: 23
title: Authentication and account experience
covers: sign-in, registration, verification, reset, MFA, profile, sessions, deletion, onboarding, invites, billing
---

# 23 - Authentication and account experience

Read when designing account access or account management. Centered forms, split layouts, illustration, gradients, video, and branded scenes can all fit the chosen direction. The layout should help users recognize the service and complete the real task.

## Sign-in and registration

Provide clear labels, useful autocomplete, password-manager support, paste, visible focus, error recovery, and a sensible submit state. A show-password control needs a name and state. Avoid fake auth that merely sets a browser flag in a production implementation. Use the project's supported identity system and server-side authorization.

Offer social or alternative sign-in only when configured and functional. Explain account linking where an email may already exist. Registration should ask for necessary information and state relevant terms or consent accurately. Do not imply a newsletter opt-in is needed to create an account unless that is an explicit, justified product requirement.

Errors should be actionable without leaking unnecessary account existence or security detail. Consistency with the actual threat model matters; avoid inventing a security policy from a visual reference.

## Verification, reset, and MFA

Verification and password reset links need an actual lifecycle: secure generation, appropriate expiration, one-time use where required, resend, invalid/expired handling, and clear success state. Server-side rate limits and abuse handling are separate from client countdowns.

OTP and MFA input should support paste, autofill, keyboard, accessible naming, and real recovery. State the actual destination in appropriately masked form. Do not expose complete phone or email details unnecessarily. Explain recovery codes or alternate factors if supported, without promising a recovery path that does not exist.

Allow password managers and accessible authentication. Do not block paste or require a memory puzzle merely to fit a custom UI. Challenge alternatives and anti-abuse requirements should follow the security and accessibility needs of the product.

## Profile, settings, and sessions

Profile updates should identify what is public, private, or used for account recovery. Handle long or international names without a narrow character assumption. Changing a sensitive email, password, or factor may need reauthentication and notification according to the identity system.

Sessions and device lists should show real, useful information and offer revocation where implemented. Do not invent a precise device location from rough IP data. A revoked session should actually lose access server-side.

Account deletion and export need real scope, retention constraints, processing state, and recovery rules. Clearly distinguish deactivation from deletion. Do not claim all data is erased if contractual, legal, backup, or system requirements mean otherwise; determine the actual policy before presenting the promise.

## Invites and onboarding

Invites need an intended organization/role, secure token lifecycle, already-used/expired states, and a reliable route for the recipient. Do not trust a role copied from a client URL. Onboarding should collect or teach what is needed for the next useful action, with skipping or return paths where appropriate. It need not be a fixed-length wizard.

## Billing

Use authoritative subscription, invoice, and payment states. Explain currency, interval, renewal, taxes/fees where applicable, plan limits, trial, cancellation, and effective dates. A UI-only plan selection is not a completed subscription. Verify gateway callbacks and make changes idempotent. Payment failure, pending confirmation, refund, and cancellation are distinct states.

## Review

Test real auth integration where authorized, success, invalid input, expired tokens, network failure, duplicate actions, keyboard and mobile operation, and session/permission boundaries affected by the change. Preserve the visual direction while correcting functional and accessibility issues.
