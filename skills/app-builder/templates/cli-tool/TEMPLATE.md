# Command-line product

## Fit and inspection

Use when the deliverable is a command-line tool. Select language/runtime and parser from the existing environment, distribution path and command complexity; Commander is an option.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Define inputs, help, exit codes, output and noninteractive behavior. Keep machine-readable output separate from progress/log output.

- Validate paths/options, protect secrets and handle cancellation. Avoid overwriting files or performing remote mutations merely because a parser accepted a flag.

- Support the relevant operating systems and shell quoting. Use the project packaging model; test an installed or built entrypoint where appropriate.

For new visual design, complete the shared short style/reference intake and wait unless already answered or delegated. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Exercise help, success, invalid input, failure exit codes and relevant filesystem behavior in an isolated task directory. Test idempotency or dry-run behavior when the command offers it.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
