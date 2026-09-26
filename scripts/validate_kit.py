#!/usr/bin/env python3
"""Validate the AG Kit v2.5 structure and its cross references.

Checks
  layout     plugin.json present, no legacy workflows/ or agent/ folders, VERSION format, JSON valid
  rules      frontmatter (name = file stem, version, trigger, globs for glob rules), no hex colours,
             always-on budget (always_on rules total <= 15000 bytes; model_decision/glob/manual excluded),
             quick-reference is model_decision, every /command in request-routing has a skill,
             every agent in request-routing has a file
  agents     native subagent frontmatter: name = stem, description, model, subagent, kit-skills
             (list of existing skills), version; no `tools:` key; no legacy `skills:` key; sections
             Role, How you work, Build, Repair, Decide, Never, As a subagent, Done - in that order
  skills     SKILL.md with frontmatter; name = folder; description; version
  references every KIT/skills/<x>, KIT/agents/<y>.md, KIT/scripts/<z> path resolves; @[skills/x];
             local markdown links; script paths inside scripts/*.py
  hygiene    no hardcoded user path outside rules/core-protocol.md (and install.ps1, which patches
             it); legacy phrasing; Python syntax; size warnings (skills/*/parts, templates and
             examples exempt); obsolete files (rules/copy.md, rules/design.md, BRIEF-v2.5.md)

Rules are read from KIT/rules in the source repository; in an installed plugin (no rules/
folder) from ~/.gemini/config/rules, limited to the kit's own rule files. --rules overrides.

Usage:
  python validate_kit.py              # the kit this script lives in
  python validate_kit.py --json
  python validate_kit.py <kit-root> --strict
Exit codes: 0 no errors (warnings allowed unless --strict), 1 errors, 2 usage.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - optional
    yaml = None

KIT_DEFAULT = Path(__file__).resolve().parents[1]
USER_PATH_MARKERS = ("C:/Users/" + "Keith", "C:\\Users\\" + "Keith", "C:\\\\Users\\\\" + "Keith")
USER_PATH_ALLOWED = {"rules/core-protocol.md", "install.ps1"}
KIT_RULES = ("core-protocol", "code-rules", "design-rules", "engineering-excellence", "request-routing",
             "universal-rules", "quick-reference")
OBSOLETE = {"rules/copy.md": "removed in v2.5 (content moved to skills/anti-template); the installer deletes it",
            "rules/design.md": "merged into design-rules in v2.5; the installer deletes it",
            "BRIEF-v2.5.md": "worker brief; delete before shipping"}
HISTORY_DOCS = {"CHANGES.md", "DECISIONS.md", "KIT-REVIEW.md"}
TRIGGERS = {"always_on", "model_decision", "glob", "manual"}
ALWAYS_ON_BUDGET = 15000
AGENT_SECTIONS = ("## Role", "## How you work", "## Build", "## Repair", "## Decide", "## Never",
                  "## As a subagent", "## Done")
AGENT_SIZE_WARN = 10000
SKILL_CORE_SIZE_WARN = 16000
SKILL_FILE_SIZE_WARN = 20000
SIZE_EXEMPT_DIRS = {"parts", "templates", "template", "example", "examples"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
HEX_COLOUR = re.compile(r"(?<![\w&/#])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![\w-])")
KIT_REF = re.compile(r"KIT/(skills|agents|scripts|rules)/([^\s`'\"<>{}()*|,;\[\]]*)")
LEGACY_PATTERNS = {
    r"\.agents/agent/": "legacy path .agents/agent/ (use KIT/agents/)",
    r"\.agents/skills/": "legacy path .agents/skills/ (use KIT/skills/)",
    r"\.agents/scripts/": "legacy path .agents/scripts/ (use KIT/scripts/)",
    r"you have FAILED": "banned phrasing",
    r"PROTOCOL VIOLATION": "banned phrasing",
    r"(?i)maestro rules?\b": "stale branding",
    r"Claude Write tool": "non-Antigravity tooling reference",
    r"minimum 3 (strategic )?questions": "removed question floor",
}
TEXT_EXT = {".md", ".py", ".ps1", ".json", ".txt", ".yaml", ".yml", ".toml", ".js", ".ts", ".html", ".css", ".sh"}


@dataclass
class Finding:
    severity: str            # error | warning | info
    code: str
    file: str
    line: int
    message: str


class Validator:
    def __init__(self, root: Path, rules_dir: Path | None = None) -> None:
        self.root = root
        self.findings: list[Finding] = []
        self.is_repo = (root / "rules").is_dir()
        self.rules_dir = rules_dir or self._find_rules_dir()
        self.skills: set[str] = set()
        self.agents: set[str] = set()

    def _find_rules_dir(self) -> Path | None:
        if (self.root / "rules").is_dir():
            return self.root / "rules"
        installed = Path.home() / ".gemini" / "config" / "rules"
        return installed if (installed / "core-protocol.md").is_file() else None

    # ------------------------------------------------------------ helpers
    def add(self, severity: str, code: str, path: Path | str, message: str, line: int = 1) -> None:
        if isinstance(path, Path):
            try:
                path = path.relative_to(self.root).as_posix()
            except ValueError:
                path = path.as_posix()
        self.findings.append(Finding(severity, code, str(path), line, message))

    def rel(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return path.as_posix()

    @staticmethod
    def read(path: Path) -> str:
        try:
            return path.read_text("utf-8", errors="replace")
        except OSError:
            return ""

    # ------------------------------------------------------------ frontmatter
    def frontmatter(self, path: Path) -> tuple[dict | None, str]:
        text = self.read(path).replace("\r\n", "\n")
        raw = extract_frontmatter(text)
        if raw is None:
            self.add("error", "frontmatter.missing", path, "Missing or unterminated YAML frontmatter")
            return None, text
        if yaml is not None:
            try:
                loaded = yaml.safe_load(raw)
            except Exception as exc:  # noqa: BLE001 - any YAML error is a finding
                self.add("error", "frontmatter.invalid_yaml", path, " ".join(str(exc).split())[:200])
                return None, text
            if not isinstance(loaded, dict):
                self.add("error", "frontmatter.not_mapping", path, "Frontmatter must be a YAML mapping")
                return None, text
        for n, line in enumerate(raw.splitlines(), start=2):
            m = re.match(r"^([A-Za-z0-9_-]+):\s+(.*)$", line)
            if m and m.group(2) and m.group(2)[0] not in "\"'[{|>" and re.search(r":\s", m.group(2)):
                self.add("error", "frontmatter.unquoted_colon", path,
                         f"`{m.group(1)}` has an unquoted ': ' - quote the value or YAML parsers reject it", n)
        return parse_frontmatter(raw), text

    # ------------------------------------------------------------ layout
    def check_layout(self) -> None:
        for legacy in ("workflows", "agent"):
            if (self.root / legacy).exists():
                self.add("error", "layout.legacy_dir", legacy, f"'{legacy}/' must not exist in the kit")
        if not (self.root / "plugin.json").is_file():
            self.add("error", "layout.plugin_json", "plugin.json", "plugin.json is required")
        for d in ("agents", "skills", "scripts"):
            if not (self.root / d).is_dir():
                self.add("error", "layout.missing_dir", d, f"'{d}/' is missing")
        version = self.root / "VERSION"
        if not version.is_file():
            self.add("warning", "version.missing", "VERSION", "VERSION file is missing")
        elif not re.fullmatch(r"\d{4}\.\d{1,2}\.\d{1,2}", self.read(version).strip()):
            self.add("warning", "version.format", "VERSION", f"Expected YYYY.M.D, got {self.read(version).strip()!r}")
        for path in self.root.rglob("*.json"):
            if any(p in {"__pycache__", "node_modules", ".git"} for p in path.parts):
                continue
            try:
                json.loads(path.read_text("utf-8"))
            except (OSError, ValueError) as exc:
                self.add("error", "json.invalid", path, str(exc), int(getattr(exc, "lineno", 1)))
        for rel, why in OBSOLETE.items():
            if (self.root / rel).exists():
                self.add("warning", "obsolete.file", rel, why)

    # ------------------------------------------------------------ rules
    def rule_files(self) -> list[Path]:
        if self.rules_dir is None:
            return []
        if self.rules_dir == self.root / "rules":
            return sorted(p for p in self.rules_dir.glob("*.md") if f"rules/{p.name}" not in OBSOLETE)
        return [self.rules_dir / f"{n}.md" for n in KIT_RULES if (self.rules_dir / f"{n}.md").is_file()]

    def check_rules(self) -> None:
        files = self.rule_files()
        if not files:
            self.add("info", "rules.not_found", "rules", "No rules directory found; rule checks skipped")
            return
        always_on = 0
        for path in files:
            data, text = self.frontmatter(path)
            if data is None:
                continue
            if str(data.get("name", "")) != path.stem:
                self.add("error", "rule.name_mismatch", path, f"name={data.get('name')!r}, expected {path.stem!r}")
            if not SEMVER.match(str(data.get("version", ""))):
                self.add("warning", "rule.version", path, f"version {data.get('version')!r} is not x.y.z")
            if not data.get("description"):
                self.add("warning", "rule.description", path, "Missing description")
            trigger = str(data.get("trigger", ""))
            if trigger not in TRIGGERS:
                self.add("error", "rule.trigger", path, f"trigger {trigger!r} is not one of {sorted(TRIGGERS)}")
            if trigger == "glob" and not data.get("globs"):
                self.add("error", "rule.globs", path, "glob rule without globs")
            if path.stem == "quick-reference" and trigger != "model_decision":
                self.add("error", "rule.quick_reference_trigger", path, "quick-reference must be model_decision")
            if trigger == "always_on":
                always_on += len(text.encode("utf-8"))
            for m in HEX_COLOUR.finditer(text):
                self.add("error", "rule.hex_colour", path,
                         f"hex colour {m.group(0)} in a rule - colours come from DESIGN.md", line_of(text, m.start()))
        severity = "error" if always_on > ALWAYS_ON_BUDGET else "info"
        self.add(severity, "rules.always_on_budget", self.rules_dir or "rules",
                 f"always_on rules total {always_on} bytes (budget {ALWAYS_ON_BUDGET})")
        self.check_routing()

    def check_routing(self) -> None:
        routing = (self.rules_dir / "request-routing.md") if self.rules_dir else None
        if routing is None or not routing.is_file():
            return
        text = self.read(routing)
        commands = section(text, "## Commands")
        seen: set[str] = set()
        for m in re.finditer(r"`/([a-z][\w-]*)", commands):
            name = m.group(1)
            if name in seen:
                continue
            seen.add(name)
            if not (self.root / "skills" / name / "SKILL.md").is_file():
                self.add("error", "routing.command_without_skill", routing,
                         f"/{name} is routed but KIT/skills/{name}/SKILL.md does not exist",
                         line_of(text, text.find(commands) + m.start()))
        agents_sec = section(text, "## Agents")
        routed = set()
        for m in re.finditer(r"^\|\s*`([a-z][\w-]*)`\s*\|", agents_sec, re.M):
            routed.add(m.group(1))
            if not (self.root / "agents" / f"{m.group(1)}.md").is_file():
                self.add("error", "routing.agent_missing", routing, f"agent `{m.group(1)}` is routed but has no file",
                         line_of(text, text.find(agents_sec) + m.start()))
        if routed:
            for path in sorted((self.root / "agents").glob("*.md")):
                if path.stem not in routed:
                    self.add("warning", "routing.agent_unrouted", path, "agent is not listed in request-routing")

    # ------------------------------------------------------------ skills
    def check_skills(self) -> None:
        skills_dir = self.root / "skills"
        if not skills_dir.is_dir():
            return
        for folder in sorted(p for p in skills_dir.iterdir() if p.is_dir() and p.name != "__pycache__"):
            self.skills.add(folder.name)
            skill_md = folder / "SKILL.md"
            if not skill_md.is_file():
                self.add("error", "skill.missing_skill_md", folder, "Skill folder without SKILL.md")
                continue
            data, text = self.frontmatter(skill_md)
            if data is None:
                continue
            if str(data.get("name", "")) != folder.name:
                self.add("error", "skill.name_mismatch", skill_md, f"name={data.get('name')!r}, expected {folder.name!r}")
            desc = str(data.get("description", "") or "")
            if not desc:
                self.add("error", "skill.description", skill_md, "Missing description")
            elif len(desc) < 40:
                self.add("warning", "skill.thin_description", skill_md, "Description should say what it does and when to use it")
            self.check_version(skill_md, data)
        for path in sorted(skills_dir.rglob("*.md")):
            rel_parts = path.relative_to(skills_dir).parts
            if any(p in SIZE_EXEMPT_DIRS for p in rel_parts[1:-1]):
                continue
            size = path.stat().st_size
            cap = SKILL_CORE_SIZE_WARN if path.name == "SKILL.md" else SKILL_FILE_SIZE_WARN
            if size > cap:
                self.add("warning", "size.skill", path, f"{size} bytes (over {cap}); move depth into a Read-when file")

    def check_version(self, path: Path, data: dict) -> None:
        version = str(data.get("version", "") or "")
        if not version:
            self.add("warning", "frontmatter.version_missing", path, "Missing version")
        elif not SEMVER.match(version):
            self.add("warning", "frontmatter.version", path, f"Non-semver version {version!r}")
        elif tuple(int(x) for x in version.split(".")[:2]) < (2, 5):
            self.add("warning", "frontmatter.version_old", path, f"version {version} - not yet revised for v2.5")

    # ------------------------------------------------------------ agents
    def check_agents(self) -> None:
        for path in sorted((self.root / "agents").glob("*.md")):
            self.agents.add(path.stem)
        for path in sorted((self.root / "agents").glob("*.md")):
            data, text = self.frontmatter(path)
            if data is None:
                continue
            if str(data.get("name", "")) != path.stem:
                self.add("error", "agent.name_mismatch", path, f"name={data.get('name')!r}, expected {path.stem!r}")
            desc = str(data.get("description", "") or "")
            if not desc:
                self.add("error", "agent.description", path, "Missing description")
            elif "Triggers on" not in desc:
                self.add("warning", "agent.no_triggers", path, "Description should end with 'Triggers on: ...'")
            if not data.get("model"):
                self.add("error", "agent.model", path, "Missing `model` (use `model: inherit`)")
            if data.get("subagent") is not True:
                self.add("error", "agent.subagent", path, "`subagent: true` is required for native subagents")
            if "tools" in data:
                self.add("error", "agent.tools_key", path,
                         "Remove `tools:` - omitted means inherit the parent's tools; a wrong tool name can hang a subagent")
            if "skills" in data:
                self.add("error", "agent.legacy_skills_key", path,
                         "Legacy `skills:` key - Antigravity reads `skills` as skill paths; use `kit-skills: [..]`")
            kit_skills = data.get("kit-skills")
            if not isinstance(kit_skills, list) or not kit_skills:
                self.add("error", "agent.kit_skills", path, "`kit-skills` must be a non-empty list, e.g. [a, b]")
                kit_skills = []
            for skill in kit_skills:
                if str(skill) not in self.skills:
                    self.add("error", "reference.unknown_skill", path, f"kit-skills names a missing skill: {skill}")
            self.check_version(path, data)
            self.check_agent_body(path, text, [str(s) for s in kit_skills])
            if len(text.encode("utf-8")) > AGENT_SIZE_WARN:
                self.add("warning", "size.agent", path, f"{len(text.encode('utf-8'))} bytes (over {AGENT_SIZE_WARN})")

    def check_agent_body(self, path: Path, text: str, kit_skills: list[str]) -> None:
        body = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
        if not re.search(r"^# \S", body, re.M):
            self.add("warning", "agent.title", path, "Missing `# <Title>` heading")
        headings = [(ln.strip(), n) for n, ln in enumerate(body.splitlines(), start=1) if ln.startswith("## ")]

        def matches(heading: str, want: str) -> bool:
            return heading == want or heading.startswith((want + " ", want + "(", want + ":"))

        found = []
        for want in AGENT_SECTIONS:
            hit = next((n for h, n in headings if matches(h, want)), None)
            if hit is None:
                self.add("error", "agent.section_missing", path, f"Missing section `{want}`")
            else:
                found.append((hit, want))
        order = [w for _, w in sorted(found)]
        expected = [w for w in AGENT_SECTIONS if w in order]
        if order != expected:
            self.add("error", "agent.section_order", path, f"Sections out of order: {' / '.join(order)}")
        for h, n in headings:
            if not any(matches(h, w) for w in AGENT_SECTIONS):
                self.add("warning", "agent.extra_section", path, f"Unexpected section `{h}`", n)
        now = re.search(r"^\*\*Read now[^*]*:\*\*(.*)$", body, re.M)
        if now:
            named = re.findall(r"KIT/skills/([\w-]+)/", now.group(1))
            if len(named) > 3:
                self.add("warning", "agent.read_now", path, f"Read now lists {len(named)} skills (max 3)", line_of(body, now.start()))
            for skill in named:
                if kit_skills and skill not in kit_skills:
                    self.add("warning", "agent.read_now_not_in_kit_skills", path,
                             f"Read now names {skill}, which is not in kit-skills", line_of(body, now.start()))

    # ------------------------------------------------------------ references and hygiene
    def markdown_files(self) -> list[Path]:
        out = []
        for path in sorted(self.root.rglob("*.md")):
            rel = self.rel(path)
            if rel in OBSOLETE or any(p in {".git", "node_modules"} for p in path.parts):
                continue
            if path.parent == self.root and (path.name in HISTORY_DOCS or path.name.startswith(("PLAN", "BRIEF"))):
                continue
            out.append(path)
        if self.rules_dir is not None and self.rules_dir != self.root / "rules":
            out += self.rule_files()
        return out

    def check_references(self) -> None:
        skill_ref = re.compile(r"@\[skills/([\w-]+)\]")
        agent_ref = re.compile(r"(?<![\w/-])agents/([\w-]+)\.md")
        link = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)[^)]*\)")
        for path in self.markdown_files():
            text = self.read(path)
            prose = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
            prose = re.sub(r"`[^`\n]*`", lambda m: " " * len(m.group(0)), prose)
            for m in KIT_REF.finditer(text):
                self.check_kit_ref(path, text, m)
            for m in skill_ref.finditer(text):
                if m.group(1) not in self.skills:
                    self.add("error", "reference.unknown_skill", path, f"Unknown skill @[skills/{m.group(1)}]", line_of(text, m.start()))
            for m in agent_ref.finditer(text):
                if m.group(1) not in self.agents and "<" not in m.group(0):
                    self.add("error", "reference.unknown_agent", path, f"Unknown agent {m.group(1)}.md", line_of(text, m.start()))
            for m in link.finditer(prose):
                raw = m.group(1).strip("<>")
                if raw.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:", "C:/", "KIT/")) or "<" in raw:
                    continue
                target_text = unquote(raw.split("#", 1)[0])
                if not target_text:
                    continue
                target = (path.parent / target_text).resolve()
                try:
                    target.relative_to(self.root.resolve())
                except ValueError:
                    continue
                if not target.exists():
                    self.add("error", "markdown.missing_link", path, f"Missing local target: {target_text}", line_of(prose, m.start()))
            if self.rel(path).startswith(("rules/", "agents/", "skills/")) or path.parent == self.rules_dir:
                for pattern, why in LEGACY_PATTERNS.items():
                    for m in re.finditer(pattern, text):
                        self.add("error", "legacy.pattern", path, f"{why}: {m.group(0)!r}", line_of(text, m.start()))

    def check_kit_ref(self, path: Path, text: str, m: re.Match) -> None:
        kind, rest = m.group(1), m.group(2)
        after = text[m.end(): m.end() + 1]
        if not rest or after in "<{*" and after != "" or "..." in rest or "…" in rest:
            return
        rest = rest.rstrip(".:)]'`")
        if not rest:
            return
        if kind == "rules":
            base = self.rules_dir
            if base is None:
                return
            target = base / rest
        else:
            target = self.root / kind / rest
        if kind == "skills" and "/" not in rest:
            ok = (self.root / "skills" / rest).is_dir()
        else:
            ok = target.exists()
        if not ok:
            self.add("error", "reference.missing_path", path, f"KIT/{kind}/{rest} does not exist", line_of(text, m.start()))

    def check_hygiene(self) -> None:
        for path in sorted(self.root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in TEXT_EXT:
                continue
            if any(p in {".git", "node_modules", "__pycache__"} for p in path.parts):
                continue
            rel = self.rel(path)
            if rel in USER_PATH_ALLOWED or rel in OBSOLETE:
                continue
            if path.parent == self.root and (path.name in HISTORY_DOCS or path.name.startswith(("PLAN", "BRIEF"))):
                continue
            text = self.read(path)
            for marker in USER_PATH_MARKERS:
                idx = text.find(marker)
                if idx >= 0:
                    self.add("error", "hygiene.user_path", path,
                             f"hardcoded user path {marker!r} - write KIT/... (defined once in core-protocol)",
                             line_of(text, idx))
                    break
        for path in sorted(self.root.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            try:
                ast.parse(self.read(path), filename=str(path))
            except SyntaxError as exc:
                self.add("error", "python.syntax", path, str(exc), int(exc.lineno or 1))
        script_ref = re.compile(r"""["']((?:skills|scripts)/[^"'\s]+?\.py)["']""")
        for path in sorted((self.root / "scripts").glob("*.py")):
            text = self.read(path)
            for m in script_ref.finditer(text):
                if not (self.root / m.group(1)).is_file():
                    self.add("error", "reference.missing_script", path,
                             f"Referenced script does not exist: {m.group(1)}", line_of(text, m.start()))

    def run(self) -> list[Finding]:
        self.check_layout()
        self.check_skills()
        self.check_agents()
        self.check_rules()
        self.check_references()
        self.check_hygiene()
        return self.findings


# ---------------------------------------------------------------- module-level helpers
def line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, max(idx, 0)) + 1


def section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    nxt = re.search(r"^## ", text[start + len(heading):], re.M)
    return text[start: start + len(heading) + nxt.start()] if nxt else text[start:]


def extract_frontmatter(text: str) -> str | None:
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    return text[4:end]


def _scalar(value: str) -> object:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        inner = value[1:-1]
        return inner.replace('\\"', '"') if value[0] == '"' else inner.replace("''", "'")
    if value.startswith("[") and value.endswith("]"):
        return [_scalar(v) for v in value[1:-1].split(",") if v.strip()]
    low = value.lower()
    if low in {"true", "yes", "on"}:
        return True
    if low in {"false", "no", "off"}:
        return False
    if low in {"null", "~", ""}:
        return None
    return value


def parse_frontmatter(raw: str) -> dict[str, object]:
    """A small YAML subset (scalars, quoted strings, inline and block lists, folded blocks).

    Deterministic without PyYAML, so the kit validates the same on every machine.
    """
    data: dict[str, object] = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
        i += 1
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            block = []
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            data[key] = (" " if value.startswith(">") else "\n").join(block).strip()
        elif value == "":
            items = []
            while i < len(lines) and re.match(r"^\s*-\s+", lines[i]):
                items.append(_scalar(re.sub(r"^\s*-\s+", "", lines[i])))
                i += 1
            data[key] = items if items else None
        else:
            data[key] = _scalar(value)
    return data


# Backwards-compatible names used by older tests and tools.
fallback_frontmatter = parse_frontmatter


def normalize_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = value.strip().strip("[]")
        return [item.strip().strip("\"'") for item in value.split(",") if item.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def validate(root: Path, rules_dir: Path | None = None) -> list[Finding]:
    return Validator(root, rules_dir).run()


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="Validate the AG Kit v2.5 structure and cross references.",
                                     epilog="Exit codes: 0 no errors, 1 errors (or warnings with --strict), 2 usage.")
    parser.add_argument("path", nargs="?", default=None, help="kit root (default: the kit this script is in)")
    parser.add_argument("--rules", type=Path, help="rules directory (default: KIT/rules or ~/.gemini/config/rules)")
    parser.add_argument("--json", action="store_true", dest="as_json", help="print JSON to stdout")
    parser.add_argument("--strict", action="store_true", help="warnings fail too")
    parser.add_argument("--quiet", action="store_true", help="print errors and the summary only")
    args = parser.parse_args(argv)
    root = Path(args.path).resolve() if args.path else KIT_DEFAULT
    if not root.is_dir():
        print(f"validate_kit: not a directory: {root}", file=sys.stderr)
        return 2
    if args.rules and not args.rules.is_dir():
        print(f"validate_kit: rules directory not found: {args.rules}", file=sys.stderr)
        return 2
    findings = validate(root, args.rules.resolve() if args.rules else None)
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    failed = bool(errors) or (args.strict and bool(warnings))
    if args.as_json:
        print(json.dumps({"kit": str(root), "passed": not failed, "errors": len(errors), "warnings": len(warnings),
                          "findings": [asdict(f) for f in findings]}, indent=2, ensure_ascii=False))
    else:
        print(f"AG Kit validation: {root}")
        order = {"error": 0, "warning": 1, "info": 2}
        for item in sorted(findings, key=lambda f: (order[f.severity], f.file, f.line)):
            if args.quiet and item.severity != "error":
                continue
            print(f"[{item.severity.upper()}] {item.file}:{item.line} {item.code} - {item.message}")
        print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)")
        print("[FAIL] Kit validation failed." if failed else "[PASS] Kit is structurally valid.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
