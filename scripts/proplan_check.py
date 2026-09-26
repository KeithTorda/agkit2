#!/usr/bin/env python3
"""Check a /proplan documentation set for completeness and traceability.

A /proplan set lives in docs/proplan/<slug>/. This script checks that the documents for the
set (full or lite) exist, that their frontmatter and headings are sane, that every ID has the
right syntax and is defined exactly once in its home document, and that the IDs link end to
end: goals -> requirements -> screens/APIs -> tasks -> test cases.

ID conventions (defined as the first token of a heading, the first cell of a table row, or a
bold task id in a checkbox line):
    G-01 DG-01 KPI-01 (01-goals)      R-001 NFR-01 (02-requirements)
    API-01 (05-api; lite: 03)          S-01 (06-ux; lite: 03)          TH-01 (07-security)
    TC-001 (08-quality)                T-001, milestones M1 (10-roadmap)
    RK-01 (11-risks; lite: 10)         DOC-01 (12-documentation)       ADR-001 (adr/ file)
    RV-01 (REVIEW.md)

Usage:
    python proplan_check.py docs/proplan/cafe-pos
    python proplan_check.py docs/proplan/cafe-pos --lite --json
    python proplan_check.py docs/proplan/cafe-pos --write-traceability
    python proplan_check.py docs/proplan/cafe-pos --stage design   # after Phase 3, before 10-13 exist

Exit codes: 0 no errors (warnings allowed unless --strict), 1 errors found, 2 usage error.
Python 3.10+, standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

LITE_FILES = [
    "00-overview.md",
    "01-goals.md",
    "02-requirements.md",
    "03-architecture.md",
    "10-roadmap.md",
    "TRACEABILITY.md",
]
FULL_FILES = [
    "00-overview.md",
    "01-goals.md",
    "02-requirements.md",
    "03-architecture.md",
    "04-data-model.md",
    "05-api.md",
    "06-ux.md",
    "07-security.md",
    "08-quality.md",
    "09-operations.md",
    "10-roadmap.md",
    "11-risks.md",
    "12-documentation.md",
    "13-glossary.md",
    "TRACEABILITY.md",
    "REVIEW.md",
]
FULL_ONLY_MARKERS = ["04-data-model.md", "05-api.md", "07-security.md", "08-quality.md"]
# --stage design (end of Phase 3): these files do not exist yet, and these checks need them.
DESIGN_STAGE_LATER_FILES = {"10-roadmap.md", "11-risks.md", "12-documentation.md", "13-glossary.md", "TRACEABILITY.md", "REVIEW.md"}
DESIGN_STAGE_SKIPPED_CODES = {"trace.must_task", "trace.must_test", "trace.should_task"}
DESIGN_STAGE_LATER_PREFIXES = {"T", "RK"}

# prefix -> (digit count, documents (stems) where it may be defined)
ID_SPEC: dict[str, tuple[int, tuple[str, ...]]] = {
    "G": (2, ("01-goals",)),
    "DG": (2, ("01-goals",)),
    "KPI": (2, ("01-goals",)),
    "R": (3, ("02-requirements",)),
    "NFR": (2, ("02-requirements",)),
    "API": (2, ("05-api", "03-architecture")),
    "S": (2, ("06-ux", "03-architecture")),
    "TH": (2, ("07-security",)),
    "TC": (3, ("08-quality",)),
    "T": (3, ("10-roadmap",)),
    "RK": (2, ("11-risks", "10-roadmap")),
    "DOC": (2, ("12-documentation",)),
    "ADR": (3, ("adr",)),
    "RV": (2, ("REVIEW",)),
}
PREFIX_ALT = "|".join(sorted(ID_SPEC, key=len, reverse=True))
ID_TOKEN = re.compile(rf"(?<![A-Za-z0-9_-])({PREFIX_ALT})-(\d+)(?![A-Za-z0-9_])")
MILESTONE_TOKEN = re.compile(r"(?<![A-Za-z0-9_-])M(\d{1,2})(?![A-Za-z0-9_])")
# A bare "M4" in prose is not a milestone ("Apple M4 laptop"). Count it only in a heading, as a whole
# table cell, or next to the word "milestone".
MILESTONE_NEAR_WORD = re.compile(
    r"\bmilestones?\s*[:(]?\s*\**M(\d{1,2})\b|(?<![A-Za-z0-9_-])M(\d{1,2})\**\s*\)?\s+milestones?\b", re.IGNORECASE)
MILESTONE_CELL = re.compile(r"^\**M(\d{1,2})\**$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
TASK_LINE = re.compile(r"^\s*[-*]\s*\[[ xX~-]\]\s*\*\*(T-\d+)\*\*\s*(.*)$")
TABLE_FIRST_CELL = re.compile(rf"^\|\s*(?:\*\*)?(({PREFIX_ALT})-\d+)(?:\*\*)?\s*\|")
HEADING_ID = re.compile(rf"^(?:\*\*)?(({PREFIX_ALT})-\d+)(?:\*\*)?(?![A-Za-z0-9_-])[\s:.—–-]*(.*)$")
MILESTONE_HEADING = re.compile(r"^M(\d{1,2})\b[\s:.—–-]*(.*)$")
GWT = re.compile(r"\bgiven\b.*\bwhen\b.*\bthen\b", re.IGNORECASE)
PRIORITY = re.compile(r"priority\s*\**\s*:\s*\**\s*(must|should|could|won'?t)", re.IGNORECASE)
FIELD_SEP = r"[^·|;\n]+"
TASK_FIELDS = {
    "owner": re.compile(rf"\bowner\s*:\s*({FIELD_SEP})", re.IGNORECASE),
    "estimate": re.compile(rf"\bestimate\s*:\s*({FIELD_SEP})", re.IGNORECASE),
    "depends": re.compile(rf"\bdepends(?:[- ]on)?\s*:\s*({FIELD_SEP})", re.IGNORECASE),
    "covers": re.compile(rf"\bcovers\s*:\s*({FIELD_SEP})", re.IGNORECASE),
}
VERIFY_FIELD = re.compile(r"\bverify\s*:\s*(.+)", re.IGNORECASE)
ADR_FILE = re.compile(r"^ADR-(\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
ADR_SECTIONS = ("context", "options", "decision", "consequences")
ADR_STATUSES = {"proposed", "accepted", "superseded", "deprecated", "rejected"}
DOC_STATUSES = {"draft", "in-review", "approved", "superseded"}
PLACEHOLDER = re.compile(r"<(?!/?(?:br|sup|sub|kbd|details|summary|b|i|em|strong|code|small|p|div|span)\b)[a-z][a-z0-9 _/.-]{1,40}>", re.IGNORECASE)
GEN_START = "<!-- proplan:traceability:start -->"
GEN_END = "<!-- proplan:traceability:end -->"
NO_DEFS = {"00-overview", "TRACEABILITY", "13-glossary"}


@dataclass
class Finding:
    severity: str  # error | warning
    code: str
    file: str
    line: int
    message: str


@dataclass
class Definition:
    ident: str
    prefix: str
    doc: str
    line: int
    title: str
    kind: str  # heading | row | task | file
    body: str = ""
    body_start: int = 0


@dataclass
class Doc:
    path: Path
    rel: str
    stem: str
    raw: str
    lines: list[str]
    in_fence: list[bool]
    frontmatter: dict[str, str] = field(default_factory=dict)
    has_frontmatter: bool = False


class Report:
    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def error(self, code: str, doc: str, line: int, message: str) -> None:
        self.findings.append(Finding("error", code, doc, line, message))

    def warn(self, code: str, doc: str, line: int, message: str) -> None:
        self.findings.append(Finding("warning", code, doc, line, message))

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]


# --------------------------------------------------------------------------- loading


def strip_comments(text: str) -> str:
    """Remove HTML comments but keep their newlines so line numbers stay right."""
    return re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.DOTALL)


def load_doc(path: Path, root: Path) -> Doc:
    raw = path.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n")
    rel = path.relative_to(root).as_posix()
    stem = "adr" if rel.startswith("adr/") else path.stem
    fm: dict[str, str] = {}
    has_fm = False
    body = raw
    if raw.startswith("---\n"):
        end = raw.find("\n---", 4)
        if end > 0:
            has_fm = True
            block = raw[4:end]
            for line in block.splitlines():
                m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
                if m:
                    fm[m.group(1).lower()] = m.group(2).strip().strip("\"'")
            fm_lines = raw[: end + 4].count("\n")
            rest = raw[end + 4 :]
            body = "\n" * fm_lines + rest
    cleaned = strip_comments(body)
    lines = cleaned.split("\n")
    in_fence: list[bool] = []
    fenced = False
    for line in lines:
        if FENCE.match(line):
            in_fence.append(True)
            fenced = not fenced
            continue
        in_fence.append(fenced)
    return Doc(path, rel, stem, raw, lines, in_fence, fm, has_fm)


def headings(doc: Doc) -> list[tuple[int, int, str]]:
    """(line index, level, text) for headings outside code fences."""
    out = []
    for i, line in enumerate(doc.lines):
        if doc.in_fence[i]:
            continue
        m = HEADING.match(line)
        if m:
            out.append((i, len(m.group(1)), m.group(2)))
    return out


# --------------------------------------------------------------------------- parsing


def collect_definitions(doc: Doc, defs: list[Definition]) -> None:
    if doc.stem in NO_DEFS:
        return
    heads = headings(doc)
    heading_ids: set[str] = set()
    for idx, (i, level, text) in enumerate(heads):
        m = HEADING_ID.match(text)
        if not m or m.group(2) == "ADR":
            continue  # ADR ids are defined by their files; headings and rows only cite them
        heading_ids.add(m.group(1))
        end = len(doc.lines)
        for j, lvl, _ in heads[idx + 1 :]:
            if lvl <= level:
                end = j
                break
        defs.append(
            Definition(m.group(1), m.group(2), doc.rel, i + 1, m.group(3).strip(), "heading",
                       "\n".join(doc.lines[i + 1 : end]), i + 1)
        )
    for i, line in enumerate(doc.lines):
        if doc.in_fence[i]:
            continue
        m = TABLE_FIRST_CELL.match(line)
        if m and m.group(2) != "ADR":
            if not row_defines(doc, i, m.group(2), heading_ids):
                continue  # a table that cites ids in its first column, not a definition
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            title = cells[1] if len(cells) > 1 else ""
            defs.append(Definition(m.group(1), m.group(2), doc.rel, i + 1, title, "row", line, i))
            continue
        m = TASK_LINE.match(line)
        if m:
            block = [line]
            j = i + 1
            while j < len(doc.lines):
                nxt = doc.lines[j]
                if nxt.strip() == "":
                    # blank line ends the block unless an indented line follows
                    if j + 1 < len(doc.lines) and doc.lines[j + 1].startswith((" ", "\t")) and not TASK_LINE.match(doc.lines[j + 1]):
                        j += 1
                        continue
                    break
                if TASK_LINE.match(nxt) or HEADING.match(nxt) or not nxt.startswith((" ", "\t")):
                    break
                block.append(nxt)
                j += 1
            title = re.sub(r"\s+", " ", m.group(2)).strip()
            defs.append(Definition(m.group(1), "T", doc.rel, i + 1, title, "task", "\n".join(block), i))


def table_header(doc: Doc, i: int) -> str:
    """First cell of the header row of the table that contains line i."""
    j = i
    while j > 0 and doc.lines[j - 1].lstrip().startswith("|") and not doc.in_fence[j - 1]:
        j -= 1
    cells = doc.lines[j].strip().strip("|").split("|")
    return cells[0].strip().strip("*` ") if cells else ""


def row_defines(doc: Doc, i: int, prefix: str, heading_ids: set[str]) -> bool:
    """A table row defines its first-cell id when the table's header starts with 'ID', or when the
    row is in the id's home document (and the id is not already defined there by a heading)."""
    header = table_header(doc, i)
    if header.lower() == "id":
        return True
    if doc.stem in ID_SPEC[prefix][1]:
        m = TABLE_FIRST_CELL.match(doc.lines[i])
        return not (m and m.group(1) in heading_ids)
    return False


def milestone_refs(line: str, is_heading: bool) -> list[str]:
    """Milestone ids referenced on a line, under the heading / table cell / 'milestone' word rule."""
    found: list[str] = []
    if is_heading:
        found += [m.group(1) for m in MILESTONE_TOKEN.finditer(line)]
    else:
        if line.lstrip().startswith("|"):
            for cell in line.strip().strip("|").split("|"):
                m = MILESTONE_CELL.match(cell.strip())
                if m:
                    found.append(m.group(1))
        for m in MILESTONE_NEAR_WORD.finditer(line):
            found.append(m.group(1) or m.group(2))
    out: list[str] = []
    for num in found:
        name = f"M{int(num)}"
        if name not in out:
            out.append(name)
    return out


def milestone_defs(doc: Doc) -> dict[str, tuple[int, int]]:
    """M-number -> (line, heading index) from 10-roadmap headings."""
    out: dict[str, tuple[int, int]] = {}
    for i, _level, text in headings(doc):
        m = MILESTONE_HEADING.match(text)
        if m:
            out[f"M{int(m.group(1))}"] = (i + 1, i)
    return out


def ids_in(text: str, prefixes: tuple[str, ...] | None = None) -> list[str]:
    found = []
    for m in ID_TOKEN.finditer(text):
        if prefixes is None or m.group(1) in prefixes:
            ident = f"{m.group(1)}-{m.group(2)}"
            if ident not in found:
                found.append(ident)
    return found


def task_fields(defn: Definition) -> dict[str, str]:
    text = defn.body
    out: dict[str, str] = {}
    for name, rx in TASK_FIELDS.items():
        m = rx.search(text)
        if m:
            out[name] = m.group(1).strip().strip("`* ")
    m = VERIFY_FIELD.search(text)
    if m:
        out["verify"] = m.group(1).strip()
    return out


def sort_key(ident: str) -> tuple[str, int]:
    prefix, _, num = ident.partition("-")
    return (prefix, int(num) if num.isdigit() else 0)


# --------------------------------------------------------------------------- checks


def detect_set(root: Path, docs: dict[str, Doc], forced: str | None) -> str:
    if forced:
        return forced
    overview = docs.get("00-overview.md")
    if overview and overview.frontmatter.get("set", "").lower() in {"lite", "full"}:
        return overview.frontmatter["set"].lower()
    return "full" if any((root / name).exists() for name in FULL_ONLY_MARKERS) else "lite"


def check_files(root: Path, plan_set: str, rep: Report, stage: str = "final") -> None:
    required = FULL_FILES if plan_set == "full" else LITE_FILES
    if stage == "design":
        required = [n for n in required if n not in DESIGN_STAGE_LATER_FILES]
    for name in required:
        if not (root / name).is_file():
            rep.error("file.missing", name, 0, f"required for the {plan_set} set but missing")
    adr_dir = root / "adr"
    if plan_set == "full" and not (adr_dir.is_dir() and any(adr_dir.glob("ADR-*.md"))):
        rep.error("adr.missing", "adr/", 0, "the full set needs at least one ADR (adr/ADR-001-<slug>.md)")


def check_structure(doc: Doc, rep: Report) -> None:
    if doc.stem not in {"TRACEABILITY"}:
        if not doc.has_frontmatter:
            rep.error("frontmatter.missing", doc.rel, 1, "no YAML frontmatter (--- block at the top)")
        else:
            keys = ("adr", "title", "status", "date") if doc.stem == "adr" else ("doc", "project", "version", "status")
            for key in keys:
                if not doc.frontmatter.get(key):
                    rep.error("frontmatter.key", doc.rel, 1, f"frontmatter is missing '{key}'")
            if doc.stem == "adr":
                status = doc.frontmatter.get("status", "").lower()
                if status and status not in ADR_STATUSES:
                    rep.warn("frontmatter.status", doc.rel, 1, f"ADR status '{status}' is not one of {sorted(ADR_STATUSES)}")
            else:
                status = doc.frontmatter.get("status", "").lower()
                if status and status not in DOC_STATUSES:
                    rep.warn("frontmatter.status", doc.rel, 1, f"status '{status}' is not one of {sorted(DOC_STATUSES)}")
                declared = doc.frontmatter.get("doc", "")
                if declared and declared != doc.stem:
                    rep.warn("frontmatter.doc", doc.rel, 1, f"frontmatter doc '{declared}' does not match the file name '{doc.stem}'")
            if doc.stem == "00-overview" and doc.frontmatter.get("set", "").lower() not in {"lite", "full"}:
                rep.error("frontmatter.key", doc.rel, 1, "00-overview frontmatter needs 'set: full' or 'set: lite'")
    heads = headings(doc)
    h1 = [h for h in heads if h[1] == 1]
    if not heads or heads[0][1] != 1:
        rep.error("heading.h1", doc.rel, (heads[0][0] + 1) if heads else 1, "the first heading must be a single '# Title'")
    elif len(h1) > 1:
        rep.error("heading.h1", doc.rel, h1[1][0] + 1, "more than one H1 heading")
    for (i, level, text), nxt in zip(heads, heads[1:] + [(len(doc.lines), 0, "")]):
        j, nlevel, _ = nxt
        if nlevel > level + 1 and j < len(doc.lines):
            rep.warn("heading.skip", doc.rel, j + 1, f"heading level jumps from H{level} to H{nlevel}")
        between = [ln for ln in doc.lines[i + 1 : j] if ln.strip()]
        if not between and nlevel <= level and level > 1:
            rep.warn("section.empty", doc.rel, i + 1, f"section '{text}' is empty (unfilled template?)")
    for i, line in enumerate(doc.lines):
        if doc.in_fence[i]:
            continue
        if re.search(r"\b(TBD|TODO)\b", line):
            rep.warn("content.tbd", doc.rel, i + 1, "TBD/TODO left in the document")
        stripped = re.sub(r"`[^`]*`", "", line)
        m = PLACEHOLDER.search(stripped)
        if m:
            rep.warn("content.placeholder", doc.rel, i + 1, f"unfilled template placeholder {m.group(0)}")


def check_id_syntax(doc: Doc, rep: Report) -> None:
    for i, line in enumerate(doc.lines):
        for m in ID_TOKEN.finditer(line):
            prefix, num = m.group(1), m.group(2)
            width = ID_SPEC[prefix][0]
            if len(num) != width:
                fixed = f"{prefix}-{int(num):0{width}d}"
                rep.error("id.syntax", doc.rel, i + 1, f"'{prefix}-{num}' should be '{fixed}' ({width} digits)")


def check_adrs(root: Path, docs: dict[str, Doc], rep: Report) -> list[Definition]:
    adr_defs: list[Definition] = []
    adr_dir = root / "adr"
    if not adr_dir.is_dir():
        return adr_defs
    numbers: list[int] = []
    for path in sorted(adr_dir.iterdir()):
        rel = path.relative_to(root).as_posix()
        if path.is_dir() or path.suffix.lower() != ".md":
            continue
        m = ADR_FILE.match(path.name)
        if not m:
            rep.error("adr.name", rel, 0, "ADR files are named ADR-NNN-kebab-slug.md (e.g. ADR-001-offline-first.md)")
            continue
        num = int(m.group(1))
        ident = f"ADR-{m.group(1)}"
        numbers.append(num)
        doc = docs[rel]
        heads = headings(doc)
        h1 = next((h for h in heads if h[1] == 1), None)
        if h1 and ident not in h1[2]:
            rep.error("adr.title", rel, h1[0] + 1, f"H1 should start with '{ident}'")
        if doc.frontmatter.get("adr") and doc.frontmatter["adr"] != ident:
            rep.error("adr.frontmatter", rel, 1, f"frontmatter adr '{doc.frontmatter['adr']}' does not match the file ({ident})")
        found = {h[2].strip().lower() for h in heads if h[1] == 2}
        for section in ADR_SECTIONS:
            if not any(s.startswith(section) for s in found):
                rep.error("adr.section", rel, 1, f"ADR is missing the '## {section.title()}' section")
        adr_defs.append(Definition(ident, "ADR", rel, 1, h1[2] if h1 else "", "file", "\n".join(doc.lines), 0))
    if numbers:
        dupes = sorted({n for n in numbers if numbers.count(n) > 1})
        for n in dupes:
            rep.error("adr.number", "adr/", 0, f"ADR-{n:03d} is used by more than one file")
        expected = list(range(1, max(numbers) + 1))
        missing = [n for n in expected if n not in numbers]
        if missing:
            rep.error("adr.number", "adr/", 0, "ADR numbering has gaps: missing " + ", ".join(f"ADR-{n:03d}" for n in missing))
    return adr_defs


def find_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for nxt in graph.get(node, []):
            if nxt not in graph:
                continue
            if state.get(nxt) == 1:
                cycle = stack[stack.index(nxt) :] + [nxt]
                cycles.append(cycle)
            elif state.get(nxt) is None:
                visit(nxt)
        stack.pop()
        state[node] = 2

    for node in sorted(graph, key=sort_key):
        if state.get(node) is None:
            visit(node)
    return cycles


class PlanModel:
    def __init__(self, root: Path, plan_set: str, docs: dict[str, Doc], defs: dict[str, Definition],
                 milestones: dict[str, tuple[int, int]], agents: set[str]):
        self.root = root
        self.plan_set = plan_set
        self.docs = docs
        self.defs = defs
        self.milestones = milestones
        self.agents = agents
        self.tasks: dict[str, dict[str, object]] = {}
        self.req_goals: dict[str, list[str]] = {}
        self.req_priority: dict[str, str] = {}
        self.cover_tasks: dict[str, list[str]] = {}
        self.cover_tests: dict[str, list[str]] = {}
        self.cover_design: dict[str, list[str]] = {}
        self.dg_trace: dict[str, list[str]] = {}

    def of(self, prefix: str) -> list[Definition]:
        return sorted((d for d in self.defs.values() if d.prefix == prefix), key=lambda d: sort_key(d.ident))


def task_milestone(defn: Definition, milestones: dict[str, tuple[int, int]]) -> str:
    best = ""
    best_line = -1
    for name, (line, _idx) in milestones.items():
        if line <= defn.line and line > best_line:
            best, best_line = name, line
    return best


def analyse(model: PlanModel, rep: Report) -> None:
    defs = model.defs
    full = model.plan_set == "full"

    # Requirements
    for d in model.of("R"):
        goals = ids_in(d.body, ("G",))
        model.req_goals[d.ident] = goals
        m = PRIORITY.search(d.body)
        if not m:
            rep.error("req.priority", d.doc, d.line, f"{d.ident}: no MoSCoW priority (add 'Priority: Must|Should|Could|Won't')")
            prio = "?"
        else:
            prio = m.group(1).capitalize().replace("Wont", "Won't")
        model.req_priority[d.ident] = prio
        if not any(GWT.search(line) for line in d.body.splitlines()):
            rep.error("req.acceptance", d.doc, d.line, f"{d.ident}: no acceptance criterion (need a 'Given ... when ... then ...' line)")
        if not goals and prio != "Won't":
            rep.warn("req.goal", d.doc, d.line, f"{d.ident}: traces to no business goal G-xx (scope creep, or a missing goal?)")
    for d in model.of("NFR"):
        if not re.search(r"\d", d.body):
            rep.warn("nfr.measurable", d.doc, d.line, f"{d.ident}: no number in the requirement; state a measurable target")

    # Tasks
    for d in model.of("T"):
        f = task_fields(d)
        covers = ids_in(f.get("covers", ""), ("R", "NFR", "DG"))
        depends = ids_in(f.get("depends", ""), ("T",))
        ms = task_milestone(d, model.milestones)
        model.tasks[d.ident] = {"fields": f, "covers": covers, "depends": depends, "milestone": ms}
        owner = f.get("owner", "")
        if not owner:
            rep.error("task.owner", d.doc, d.line, f"{d.ident}: no owner (add 'owner: <agent>')")
        elif model.agents and owner.split()[0].lower() not in model.agents and "human" not in owner.lower():
            rep.warn("task.owner", d.doc, d.line, f"{d.ident}: owner '{owner}' is not a kit agent (mark people as 'owner: Name (human)')")
        if not f.get("verify") or len(f.get("verify", "")) < 8:
            rep.error("task.verify", d.doc, d.line, f"{d.ident}: no verify line (add 'verify: <command or observation that can fail>')")
        if not f.get("estimate"):
            rep.warn("task.estimate", d.doc, d.line, f"{d.ident}: no estimate")
        if "covers" not in f or not covers:
            rep.error("task.covers", d.doc, d.line, f"{d.ident}: covers no requirement (add 'covers: R-001' or NFR-/DG- ids)")
        if not ms and model.milestones:
            rep.warn("task.milestone", d.doc, d.line, f"{d.ident}: not under a milestone heading (### M1 ...)")
        for ident in covers:
            model.cover_tasks.setdefault(ident, []).append(d.ident)
            if ident.startswith("DG-"):
                model.dg_trace.setdefault(ident, []).append(d.ident)
        if d.ident in depends:
            rep.error("task.depends", d.doc, d.line, f"{d.ident}: depends on itself")
    graph = {t: [x for x in info["depends"] if x != t] for t, info in model.tasks.items()}  # type: ignore[index]
    seen_cycles: set[frozenset[str]] = set()
    for cycle in find_cycles(graph):
        key = frozenset(cycle)
        if key in seen_cycles:
            continue
        seen_cycles.add(key)
        first = defs[cycle[0]]
        rep.error("task.cycle", first.doc, first.line, "circular dependency: " + " -> ".join(cycle))
    order = {f"M{n}": n for n in range(1, 100)}
    for t, info in model.tasks.items():
        for dep in info["depends"]:  # type: ignore[union-attr]
            if dep in model.tasks:
                mine, theirs = order.get(info["milestone"], 0), order.get(model.tasks[dep]["milestone"], 0)  # type: ignore[arg-type]
                if mine and theirs and theirs > mine:
                    d = defs[t]
                    rep.warn("task.order", d.doc, d.line, f"{t} ({info['milestone']}) depends on {dep} in a later milestone ({model.tasks[dep]['milestone']})")

    # Test cases
    for d in model.of("TC"):
        covered = ids_in(d.body, ("R", "NFR"))
        if not covered:
            rep.error("test.covers", d.doc, d.line, f"{d.ident}: maps to no requirement (add the R-/NFR- id it verifies)")
        for ident in covered:
            model.cover_tests.setdefault(ident, []).append(d.ident)
    for d in model.of("TC") + model.of("NFR"):
        for dg in ids_in(d.body, ("DG",)):
            model.dg_trace.setdefault(dg, []).append(d.ident)

    # Screens and APIs
    for prefix in ("S", "API"):
        for d in model.of(prefix):
            reqs = ids_in(d.body, ("R",))
            if not reqs:
                rep.warn("design.covers", d.doc, d.line, f"{d.ident}: serves no requirement R-xxx")
            for ident in reqs:
                model.cover_design.setdefault(ident, []).append(d.ident)

    # Coverage
    for d in model.of("R"):
        prio = model.req_priority.get(d.ident)
        tasks = model.cover_tasks.get(d.ident, [])
        tests = model.cover_tests.get(d.ident, [])
        if prio == "Must":
            if not tasks:
                rep.error("trace.must_task", d.doc, d.line, f"{d.ident} (Must) is not covered by any task T-xxx")
            if full and not tests:
                rep.error("trace.must_test", d.doc, d.line, f"{d.ident} (Must) is not covered by any test case TC-xxx")
        elif prio == "Should" and not tasks:
            rep.warn("trace.should_task", d.doc, d.line, f"{d.ident} (Should) has no task; schedule it or move it to Could/Won't")
        elif prio == "Won't" and tasks:
            rep.warn("trace.wont_task", d.doc, d.line, f"{d.ident} is Won't but tasks cover it: {', '.join(tasks)}")
    for d in model.of("NFR"):
        if not model.cover_tasks.get(d.ident) and not model.cover_tests.get(d.ident):
            rep.warn("trace.nfr", d.doc, d.line, f"{d.ident}: no task or test case covers it")
    all_goal_refs = {g for goals in model.req_goals.values() for g in goals}
    for d in model.of("G"):
        if d.ident not in all_goal_refs:
            rep.error("trace.goal", d.doc, d.line, f"{d.ident} is not traced by any requirement R-xxx")
    for d in model.of("DG"):
        if not model.dg_trace.get(d.ident):
            rep.warn("trace.dev_goal", d.doc, d.line, f"{d.ident}: no NFR, task or test case refers to it")

    # Roadmap buffer
    roadmap = model.docs.get("10-roadmap.md")
    if roadmap and not re.search(r"\bbuffer|contingency\b", "\n".join(roadmap.lines), re.IGNORECASE):
        rep.warn("roadmap.buffer", roadmap.rel, 1, "no buffer or contingency stated for the estimates")

    # Review blockers
    review = model.docs.get("REVIEW.md")
    if review:
        for i, line in enumerate(review.lines):
            if re.match(r"^\|\s*\**RV-\d+", line):
                cells = [c.strip().strip("*").lower() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 3 and cells[1] == "blocker" and cells[-1].startswith("open"):
                    rep.error("review.blocker", review.rel, i + 1, f"{cells[0].upper()} is an open blocker; fix it or record why it is accepted")


LITE_ONLY_HOMES = {"API": "03-architecture", "S": "03-architecture", "RK": "10-roadmap"}


def check_definitions(all_defs: list[Definition], plan_set: str, rep: Report) -> dict[str, Definition]:
    defs: dict[str, Definition] = {}
    for d in all_defs:
        home = ID_SPEC[d.prefix][1]
        if plan_set == "full" and d.prefix in LITE_ONLY_HOMES:
            home = tuple(h for h in home if h != LITE_ONLY_HOMES[d.prefix])
        stem = "adr" if d.doc.startswith("adr/") else Path(d.doc).stem
        if stem not in home:
            if d.kind == "row" and stem in {"REVIEW"}:
                continue  # tables in REVIEW.md cite ids; only RV rows define
            rep.error("id.home", d.doc, d.line, f"{d.ident} is defined here but {d.prefix}- ids belong in {' or '.join(h + '.md' if h != 'adr' else 'adr/' for h in home)}")
            continue
        if d.ident in defs:
            first = defs[d.ident]
            rep.error("id.duplicate", d.doc, d.line, f"{d.ident} is defined twice (first at {first.doc}:{first.line})")
            continue
        defs[d.ident] = d
    return defs


def check_references(docs: dict[str, Doc], defs: dict[str, Definition], milestones: dict[str, tuple[int, int]],
                     rep: Report, stage: str = "final") -> None:
    design = stage == "design"
    for doc in docs.values():
        if doc.stem == "TRACEABILITY":
            continue
        for i, line in enumerate(doc.lines):
            for m in ID_TOKEN.finditer(line):
                prefix, num = m.group(1), m.group(2)
                if len(num) != ID_SPEC[prefix][0]:
                    continue  # reported by the syntax check
                if design and prefix in DESIGN_STAGE_LATER_PREFIXES:
                    continue  # tasks and risks are written in Phase 4
                ident = f"{prefix}-{num}"
                if ident not in defs:
                    rep.error("id.dangling", doc.rel, i + 1, f"{ident} is referenced but never defined")
            if not design and (milestones or "10-roadmap.md" in docs):
                for name in milestone_refs(line, bool(HEADING.match(line)) and not doc.in_fence[i]):
                    if name not in milestones:
                        rep.error("id.dangling", doc.rel, i + 1, f"milestone {name} is referenced but 10-roadmap.md has no '### {name} ...' heading")


# --------------------------------------------------------------------------- traceability


def build_traceability(model: PlanModel) -> str:
    overview = model.docs.get("00-overview.md")
    title = (overview.frontmatter.get("title") if overview else "") or model.root.name
    project = (overview.frontmatter.get("project") if overview else "") or model.root.name
    version = (overview.frontmatter.get("version") if overview else "") or "0.1.0"
    full = model.plan_set == "full"

    def join(items: list[str]) -> str:
        return ", ".join(sorted(dict.fromkeys(items), key=sort_key)) or "-"

    def task_cell(items: list[str]) -> str:
        cells = []
        for t in sorted(dict.fromkeys(items), key=sort_key):
            ms = model.tasks.get(t, {}).get("milestone")
            cells.append(f"{t} ({ms})" if ms else t)
        return ", ".join(cells) or "-"

    out = [
        "# Traceability",
        "",
        GEN_START,
        "<!-- Generated by proplan_check.py --write-traceability. Do not edit by hand; edit the source documents and regenerate. -->",
        "",
        f"Plan: **{title}** (`{project}`), version {version}, {model.plan_set} set.",
        "",
        "Chain: goal (01) -> requirement (02) -> screen / API (06, 05; lite: 03) -> task (10) -> test case (08).",
        "",
        "## Functional requirements",
        "",
    ]
    if full:
        out += ["| Goal | Requirement | Priority | Screens / APIs | Tasks | Tests | Status |", "|---|---|---|---|---|---|---|"]
    else:
        out += ["| Goal | Requirement | Priority | Screens / APIs | Tasks | Status |", "|---|---|---|---|---|---|"]
    gaps = 0
    for d in model.of("R"):
        prio = model.req_priority.get(d.ident, "?")
        tasks = model.cover_tasks.get(d.ident, [])
        tests = model.cover_tests.get(d.ident, [])
        if prio == "Won't":
            status = "not planned"
        elif not tasks:
            status = "GAP: no task"
        elif full and not tests:
            status = "GAP: no test"
        else:
            status = "covered"
        if status.startswith("GAP"):
            gaps += 1
        req = f"{d.ident} {d.title}".strip()
        row = [join(model.req_goals.get(d.ident, [])), req, prio, join(model.cover_design.get(d.ident, [])), task_cell(tasks)]
        if full:
            row.append(join(tests))
        row.append(status)
        out.append("| " + " | ".join(row) + " |")
    out += ["", "## Non-functional requirements", ""]
    nfrs = model.of("NFR")
    if nfrs:
        out += ["| Dev goal | NFR | Tasks | Tests | Status |", "|---|---|---|---|---|"] if full else ["| Dev goal | NFR | Tasks | Status |", "|---|---|---|---|"]
        for d in nfrs:
            tasks = model.cover_tasks.get(d.ident, [])
            tests = model.cover_tests.get(d.ident, [])
            status = "covered" if (tasks or tests) else "GAP: nothing covers it"
            cells = [join(ids_in(d.body, ("DG",))), f"{d.ident} {d.title}", task_cell(tasks)] + ([join(tests)] if full else []) + [status]
            out.append("| " + " | ".join(cells) + " |")
    else:
        out.append("No NFR ids defined.")
    out += ["", "## Goals", "", "| Goal | Requirements |", "|---|---|"]
    for d in model.of("G"):
        reqs = [r for r, goals in model.req_goals.items() if d.ident in goals]
        out.append(f"| {d.ident} {d.title} | {join(reqs)} |")
    for d in model.of("DG"):
        out.append(f"| {d.ident} {d.title} | {join(model.dg_trace.get(d.ident, []))} |")
    out += [
        "",
        f"Summary: {len(model.of('G'))} goals, {len(model.of('DG'))} development goals, {len(model.of('R'))} requirements, "
        f"{len(model.of('NFR'))} NFRs, {len(model.of('T'))} tasks, {len(model.of('TC'))} test cases, {gaps} gaps.",
        "",
        GEN_END,
        "",
    ]
    return "\n".join(out)


def extract_generated(text: str) -> str:
    text = text.replace("\r\n", "\n")
    start, end = text.find(GEN_START), text.find(GEN_END)
    if start < 0 or end < 0:
        return ""
    return text[start : end + len(GEN_END)].strip()


# --------------------------------------------------------------------------- main


def find_agents() -> set[str]:
    agents_dir = Path(__file__).resolve().parent.parent / "agents"
    if not agents_dir.is_dir():
        return set()
    return {p.stem.lower() for p in agents_dir.glob("*.md")}


def run(root: Path, forced_set: str | None, write_trace: bool, stage: str = "final") -> tuple[Report, dict[str, object]]:
    rep = Report()
    paths = sorted(p for p in root.glob("*.md")) + sorted((root / "adr").glob("*.md") if (root / "adr").is_dir() else [])
    docs = {p.relative_to(root).as_posix(): load_doc(p, root) for p in paths}
    plan_set = detect_set(root, docs, forced_set)
    check_files(root, plan_set, rep, stage)
    for doc in docs.values():
        check_structure(doc, rep)
        check_id_syntax(doc, rep)
    adr_defs = check_adrs(root, docs, rep)
    raw_defs: list[Definition] = []
    for doc in docs.values():
        if doc.stem != "adr":
            collect_definitions(doc, raw_defs)
    defs = check_definitions(raw_defs + adr_defs, plan_set, rep)
    roadmap = docs.get("10-roadmap.md")
    milestones = milestone_defs(roadmap) if roadmap else {}
    check_references(docs, defs, milestones, rep, stage)
    model = PlanModel(root, plan_set, docs, defs, milestones, find_agents())
    analyse(model, rep)
    if stage == "design":
        rep.findings = [f for f in rep.findings if f.code not in DESIGN_STAGE_SKIPPED_CODES]

    trace_path = root / "TRACEABILITY.md"
    generated = build_traceability(model)
    wrote = False
    if write_trace:
        if trace_path.exists():
            current = trace_path.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n")
            if GEN_START in current and GEN_END in current:
                before = current[: current.find(GEN_START)]
                after = current[current.find(GEN_END) + len(GEN_END) :]
                body = extract_generated(generated)
                new_text = before + body + after
            else:
                new_text = generated
        else:
            new_text = generated
        trace_path.write_text(new_text, encoding="utf-8", newline="\n")
        wrote = True
        rep.findings = [f for f in rep.findings if not (f.file == "TRACEABILITY.md" and f.code == "file.missing")]
    elif trace_path.exists():
        current = trace_path.read_text(encoding="utf-8-sig", errors="replace")
        if extract_generated(current) != extract_generated(generated):
            rep.error("trace.stale", "TRACEABILITY.md", 1, "out of date with the documents; run with --write-traceability")

    stats = {
        "set": plan_set,
        "documents": len(docs),
        "ids": {p: len(model.of(p)) for p in ID_SPEC if model.of(p)},
        "milestones": len(milestones),
        "traceability_written": wrote,
        "stage": stage,
    }
    return rep, stats


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(
        prog="proplan_check.py",
        description="Check a /proplan documentation set (docs/proplan/<slug>/): files, frontmatter, ID syntax and end-to-end traceability.",
    )
    parser.add_argument("path", help="plan folder, e.g. docs/proplan/cafe-pos")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--lite", action="store_true", help="check as a lite set (default: 'set' in 00-overview, else auto-detect)")
    group.add_argument("--full", action="store_true", help="check as a full set")
    parser.add_argument("--write-traceability", action="store_true", help="regenerate TRACEABILITY.md from the documents, then check")
    parser.add_argument("--stage", choices=("design", "final"), default="final",
                        help="design: check after Phase 3 (skips task/test coverage, T-/RK-/milestone references and the "
                             "10-13, TRACEABILITY, REVIEW files that are written later); final (default): everything")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="print a JSON report")
    args = parser.parse_args(argv)

    root = Path(args.path).expanduser().resolve()
    if not root.is_dir():
        parser.print_usage(sys.stderr)
        print(f"proplan_check.py: error: not a folder: {root}", file=sys.stderr)
        return 2
    if not any(root.glob("*.md")):
        print(f"proplan_check.py: error: no .md files in {root}; is this a docs/proplan/<slug> folder?", file=sys.stderr)
        return 2

    forced = "lite" if args.lite else "full" if args.full else None
    rep, stats = run(root, forced, args.write_traceability, args.stage)
    rep.findings.sort(key=lambda f: (0 if f.severity == "error" else 1, f.file, f.line))
    failed = bool(rep.errors) or (args.strict and bool(rep.warnings))

    if args.json:
        print(json.dumps({
            "path": str(root),
            "ok": not failed,
            "stats": stats,
            "errors": [asdict(f) for f in rep.errors],
            "warnings": [asdict(f) for f in rep.warnings],
        }, indent=2, ensure_ascii=False))
    else:
        ids = ", ".join(f"{n} {p}" for p, n in stats["ids"].items())  # type: ignore[union-attr]
        print(f"proplan_check: {root}")
        print(f"Set: {stats['set']} | stage: {stats['stage']} | documents: {stats['documents']} | milestones: {stats['milestones']} | ids: {ids or 'none'}")
        if stats["traceability_written"]:
            print("Wrote TRACEABILITY.md")
        for f in rep.findings:
            where = f"{f.file}:{f.line}" if f.line else f.file
            label = "ERROR" if f.severity == "error" else "WARN "
            print(f"{label} {where}  {f.message}  [{f.code}]")
        verdict = "FAIL" if failed else "PASS"
        print(f"Result: {verdict} - {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
