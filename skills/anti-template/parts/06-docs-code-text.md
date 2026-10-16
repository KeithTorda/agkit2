---
part: 06
title: Technical writing
covers: README, guides, API docs, release notes, commits, pull requests, issues, comments, logs, CLI
---

# 06 - Technical writing

Read when writing project documentation, code comments, release notes, logs, or repository messages. Follow the project's existing conventions; decorative choices such as badges or emoji do not determine technical quality.

## README and guides

Help the intended reader understand what the project does, whether it is relevant, and how to run the supported path. Use actual commands, prerequisite versions, configuration names, and known limitations. Separate local development from production deployment. Provide `.env.example` with placeholders, not real secrets. Do not invent a license, compliance status, architecture, or supported environment.

Organize a guide around a task with prerequisites, steps, expected output, and recovery for likely failures. Code snippets should fit the installed version and have necessary context. Explain when an operation mutates or deletes data. Avoid pasting an entire vendor manual into the project; link to the relevant source and document project-specific choices.

## API documentation

Describe authentication, parameters, validation, response shapes, status codes, pagination, and error behavior as actually implemented. Show representative examples with obviously fictional data. Explain idempotency and webhook verification for operations where callers need them. An example must not expose real credentials or personal records. Document compatibility changes and deprecations.

## Release notes, commits, and PRs

Describe the actual change and its effect. Follow the repository's commit format rather than imposing another one. Release notes help users understand added behavior, fixes, migration needs, and known limits. Do not mark unreleased work as shipped.

A PR description should explain the problem, resulting behavior, relevant implementation choice, validation performed, and material risks. Include required repository template fields. A bug report needs reproduction conditions, expected and observed behavior, environment, and useful sanitized evidence. Omit unsupported claims such as "fully secure" or "all edge cases covered."

## Comments and placeholders

Comment the reason, invariant, surprising constraint, or external compatibility requirement. Avoid mechanically narrating every obvious statement. API docstrings are useful when they clarify contracts and examples; a small local helper may explain itself. Keep comments synchronized with behavior.

Use actionable TODOs with an issue or useful context where the project supports tracking. Temporary mock implementations should be visible as mocks and scoped to development or an explicit prototype. Do not create a fake success path and describe it as implemented.

## Logs and CLI output

Use event names, operation context, IDs, and actionable error information. Follow the project's logging format and level policy. Preserve original error causes internally where useful; show users a safe message and support reference. Do not log passwords, API keys, session tokens, OTPs, authorization headers, or unnecessary personal data. Redaction belongs in the logging mechanism as well as call-site judgment.

CLI output should distinguish success, partial completion, and failure; return useful exit codes. Progress decoration and color are optional; text must remain useful without ANSI color or emoji. Never print a secret merely to prove that configuration exists.

## Review

Run documented commands when practical for the changed path. Check links, examples, names, and the difference between intended and verified behavior. Documentation must not imply that a deployment, migration, test, or review happened when it did not.
