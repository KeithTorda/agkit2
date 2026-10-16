---
part: 03
title: Product microcopy
covers: buttons, labels, hints, validation, feedback, confirmations, consent, payment text
---

# 03 - Product microcopy

Read when writing controls, field text, dialogs, and small feedback messages. Follow the agreed brand voice while making action, consequence, and state clear.

## Actions and navigation

Labels should predict the next step. Use "Save changes," "Send invitation," or "Export CSV" when that distinction matters. "Continue," "Get started," "Learn more," and "Try it free" are valid if the surrounding context clearly explains where they lead, what starts, or what trial terms apply. There is no word-count limit; fit the language and screen without losing meaning.

Use one term for each action throughout the product. Distinguish saving a draft from publishing, deleting from archiving, and signing in from creating an account. Link labels should make sense in context and provide specific accessible context where many identical links appear.

## Fields, hints, and validation

- Associate a persistent label with every input. A placeholder may show an example; it must not be the sole label.
- Explain a format or constraint before the user has to guess it. Match examples to the actual validation and accepted locales.
- Mark required or optional inputs consistently. A visual asterisk needs an explanation; required state also needs machine-readable semantics.
- Validate at useful moments, usually on blur or submit. Avoid announcing a new error on every character while a user is still typing.
- Explain what failed and how to correct it: "Enter a date after 16 October" rather than "Invalid value."
- Attach errors and hints with `aria-describedby`, mark invalid inputs with `aria-invalid`, and focus the first invalid field or a linked error summary on submit failure.
- Preserve valid entries when another field fails. Do not reset the form after a network error.

## Feedback that reflects reality

| Situation | Useful example |
|---|---|
| Saved successfully | "Changes saved" |
| Still sending | "Sending invitation..." |
| Offline while saving | "You're offline. Your draft is saved on this device. Retry when connected." Only claim local saving if implemented. |
| Permission denied | "You need an administrator to change billing details." |
| Server failure | "We couldn't save the changes. Try again." Add a reference ID if support can use it. |
| A meaningful brand celebration | "You're booked!" with the real date, location, and next steps |

Tone can be warm, playful, or formal. Emoji and punctuation are optional brand choices; critical facts cannot depend on them. A warning should state the actual consequence rather than use guilt or exaggerated urgency.

## Confirmations and destructive actions

State the affected object and outcome: "Delete draft invoice 104?" Explain whether recovery is possible. Label actions "Delete draft" and "Keep draft" when clearer than generic "Yes/No." Do not add confirmations to every harmless action; undo can be more useful for reversible changes. Require appropriate confirmation for irreversible or high-impact actions.

## Loading, consent, and money

Use indeterminate progress when progress is unknown; percentages need a real basis. Avoid claiming completion before the server confirms it. A cancellation control must actually cancel or clearly explain its limited effect.

Consent needs a meaningful choice and clear purpose. Do not claim permission from an unrelated click. Payment copy should identify currency, amount, billing interval, fees, and recurring terms before commitment. A pending payment is not a successful payment. Do not imply a trial is free if an immediate charge or unmentioned requirement applies.

## Review

Read labels in their actual screens, with keyboard focus, error states, loading states, and longer translations. Check comprehension, accessible names, truthful state, and recovery. See part 04 for state patterns and part 17 for form behavior.
