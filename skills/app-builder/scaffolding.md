# Scaffold a recoverable foundation

Scaffold only for a genuinely new project or an explicitly chosen new package. Inspect the destination and existing work first. Use a new suitable directory when needed; do not overwrite an existing repository, lockfile or environment file to match a kit example.

## Setup workflow

1. Establish platform, runtime, deployment constraints and package manager from the brief/repository.
2. Read only the relevant template and current official setup instructions for the chosen version. Confirm CLI flags through installed help when necessary.
3. Generate or write the smallest useful starter. Inspect the resulting manifest, scripts and tracked files; remove irrelevant demo surfaces deliberately rather than deleting all examples without checking use.
4. Establish safe configuration: ignored local secrets, a useful `.env.example` with placeholders, documented setup, and appropriate source/build exclusions.
5. Run the baseline command before adding substantial functionality. Keep a recoverable baseline through the project's normal version-control workflow.

## Organize by ownership

Use the framework's conventional routing and build boundaries. Co-locate behavior and UI where it helps. Separate server-only credentials/data access from browser code. Give meaningful domain logic a reusable boundary; avoid empty forwarding layers in a small application.

Example responsibilities, adapted to the selected stack:

| Responsibility | Possible home |
|---|---|
| Routes/layout composition | Framework route directory |
| Reusable controls | Existing component structure |
| Business rules | Domain modules/services when useful |
| Authorized data access | Server-side boundary and database policies |
| Schema changes | Versioned migrations in the supported tool |
| Configuration | Framework-supported files and safe env documentation |
| Tests | Project convention near behavior or in its test tree |

The filenames `proxy.ts`, `middleware.ts`, ORM generator options and router APIs depend on installed versions. Inspect supported conventions rather than requiring a historical example. A gateway/middleware hook alone does not replace authorization at the data boundary.

For a new visual system, complete the short style/reference intake and record accepted decisions with `design-spec` before inventing its look. API-only or CLI work does not need a website token document. Verify the baseline and a complete initial flow, then report the actual run command, local URL or executable and remaining configuration.
