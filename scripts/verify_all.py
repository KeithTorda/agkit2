#!/usr/bin/env python3
"""Release verification (code-rules tier 3): everything checklist.py --full runs, plus a
production build, dependency analysis, bundle size, React performance, mobile, API and GEO
heuristics, and runtime checks (Lighthouse, Playwright smoke) when --url is given.

Required: security high+, type errors, failing tests, a failing production build.
Everything else is advisory unless --strict.

Exit codes: 0 no required failure, 1 required failure (or advisory with --strict), 2 usage.

Usage:
  python "KIT/scripts/verify_all.py" .
  python "KIT/scripts/verify_all.py" . --url http://localhost:3000 --json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checklist import (  # noqa: E402
    build_steps,
    detect_stack,
    kit_step,
    package_manager,
    which,
)
from validation_runner import (  # noqa: E402
    Console,
    Step,
    execute,
    report_payload,
    suite_success,
    summary_table,
    utf8_stdio,
    verdict_line,
    write_report,
)

EXTRA_AUDITS = (
    ("Dependency analysis", "skills/vulnerability-scanner/scripts/dependency_analyzer.py"),
    ("GEO check", "skills/seo-fundamentals/scripts/geo_checker.py"),
    ("React performance", "skills/nextjs-react-expert/scripts/react_performance_checker.py"),
    ("Mobile audit", "skills/mobile-design/scripts/mobile_audit.py"),
    ("API validation", "skills/api-patterns/scripts/api_validator.py"),
)


def build_step(project: Path) -> Step:
    step = Step("Production build", "build", required=True, cwd=project, timeout=1200)
    stack = detect_stack(project)
    scripts = (stack.node or {}).get("scripts", {})
    pm = package_manager(project)
    if stack.node is None:
        step.skip_reason = "no package.json build"
    elif "build" not in scripts:
        step.skip_reason = "package.json has no build script"
    elif not which(pm):
        step.missing_reason = f"{pm} is not on PATH"
    else:
        step.name = f"Production build ({pm} run build)"
        step.commands = [[which(pm), "run", "build"]]  # type: ignore[list-item]
    return step


def release_steps(project: Path, url: str | None, no_build: bool, no_e2e: bool) -> list[Step]:
    steps = build_steps(project, "full", None, url)
    runtime = [s for s in steps if s.category == "runtime"]
    steps = [s for s in steps if s.category != "runtime"]
    if not no_build:
        steps.append(build_step(project))
    for name, rel in EXTRA_AUDITS:
        steps.append(kit_step(name, rel, "audit", project))
    steps.append(kit_step("Bundle analysis", "skills/performance-profiling/scripts/bundle_analyzer.py", "audit", project))
    for step in runtime:
        if no_e2e and step.name.startswith("Playwright"):
            step.commands, step.skip_reason = [], "--no-e2e"
        steps.append(step)
    return steps


def main(argv: list[str] | None = None) -> int:
    utf8_stdio()
    parser = argparse.ArgumentParser(description="Release verification (tier 3).",
                                     epilog="Exit codes: 0 ok, 1 required failure, 2 usage.")
    parser.add_argument("project", nargs="?", default=".", help="project directory (default: .)")
    parser.add_argument("--url", help="running app URL for Lighthouse and Playwright")
    parser.add_argument("--no-build", action="store_true", help="skip the production build")
    parser.add_argument("--no-e2e", action="store_true", help="skip the Playwright smoke test")
    parser.add_argument("--no-runtime", action="store_true", help="skip all URL-based checks")
    parser.add_argument("--strict", action="store_true", help="advisory findings fail the run too")
    parser.add_argument("--stop-on-fail", action="store_true", help="stop after the first required failure")
    parser.add_argument("--json", action="store_true", help="print a JSON report to stdout")
    parser.add_argument("--report", type=Path, help="also write the JSON report to this file")
    args = parser.parse_args(argv)

    project = Path(args.project).resolve()
    if not project.is_dir():
        print(f"verify_all: not a directory: {project}", file=sys.stderr)
        return 2

    console = Console(sys.stderr if args.json else sys.stdout)
    started = datetime.now(timezone.utc)
    stack = detect_stack(project)
    console.line(f"verify_all (release) | {project}")
    console.line(f"stack: {', '.join(stack.names) or 'unknown'} | url: {args.url or 'none'}")

    steps = release_steps(project, None if args.no_runtime else args.url, args.no_build, args.no_e2e)
    results = execute(steps, console, args.stop_on_fail)
    ok = suite_success(results, args.strict)
    payload = report_payload("verify_all", project, "release", results, started, args.strict,
                             {"stack": stack.names, "url": args.url})
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        console.line()
        console.line(summary_table(results))
        console.line()
        console.line(verdict_line(results, args.strict))
    if args.report:
        write_report(args.report.resolve(), payload)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
