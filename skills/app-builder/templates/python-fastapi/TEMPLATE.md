# FastAPI service

## Fit and inspection

Use when FastAPI is chosen or already present. Inspect Python version, environment/lockfile, settings, schema library and deployment model.

Inspect existing work before scaffolding. For a new foundation, use current official setup guidance and compatible versions; do not copy historical CLI flags blindly. Preserve the requested package manager, deployment constraints and user changes.

## Implementation decisions

- Define typed request/response contracts and validation without returning internal records or secrets accidentally.

- Use async only with compatible nonblocking work; blocking DB/CPU operations need an appropriate boundary. Manage startup/shutdown and connection lifecycles.

- Keep auth, configuration, data access and domain rules understandable. A package layout should clarify responsibilities rather than force empty layers.

For new visual design, complete the shared short style/reference intake and wait unless already answered or delegated. Reuse accepted tokens and design components; this template does not select an aesthetic or install a styling package. API/CLI-only work needs no visual questionnaire.

## Verify and hand off

Run project tests/type/lint checks relevant to the change and call representative endpoints, including denied/invalid paths. Confirm actual startup and documented environment requirements.

Report the actual run command, implemented outcome, checks performed and concrete remaining setup. Starter code, a mocked integration or a successful dependency install is not proof of a working end-to-end product.
