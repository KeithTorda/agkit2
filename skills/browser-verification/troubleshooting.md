# When browser verification cannot run

Check the precondition that failed before changing application code. Confirm the project directory, normal command, port, route, server readiness and required environment configuration. An occupied port can belong to another app; do not kill unrelated processes to free it.

Inspect relevant server output and browser errors. A missing dependency, unauthorized API, unavailable database, certificate issue, unsupported tool or failed asset path needs its own remedy. Avoid disabling authentication, security policy or certificate checks to make the preview appear healthy.

If output is stale, confirm the served build and route, cache/service worker and actual running project before restarting. Preserve useful logs. A new page screenshot of an error or a stale site is not evidence that the intended design rendered.

Use available supported browser tools. Do not imply that an unavailable Playwright, browser subagent or screenshot command ran. When the app cannot run, continue useful source/build checks and clearly separate those from the missing render/interaction inspection.

Record the exact block, any partial output, the checks completed and what remains unverified. Evidence files should honestly say skipped/incomplete when appropriate. The evidence helper can validate that record; it cannot repair the environment or turn a skipped inspection into a visual pass.
