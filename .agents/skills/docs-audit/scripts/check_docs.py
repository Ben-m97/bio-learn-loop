#!/usr/bin/env python3
"""Read-only mechanical audit of project decisions, source references, and IDs.

Adapted from Copypaster3000/agent-built; see the repository's UPSTREAM.md and
MIT licence. Run from any working directory with --root, or let the checker
discover an ancestor project. Only the Python standard library is required.

Exit 1 on any FAIL. WARN lines need a reviewer disposition. These checks prove
existence and bookkeeping only; whether a rule matches behavior or has scientific
support is the reviewer's job. Arbitrary scientific prose is not a symbol list.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
import fnmatch
import json
import os
from pathlib import Path, PureWindowsPath
import re
import sys
from urllib.parse import unquote, urlsplit


# Project-specific source paths and exclusions can override these defaults in
# docs/audit-config.json. Root entrypoints participate in the same source scan.
DEFAULT_EXCLUDES = (
    ".git", ".agents", ".github", "docs", "examples", "data", "raw_data", "raw",
    "references", "resources", "results", "work", ".snakemake", ".nextflow",
    ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".cache",
)
TEXT_SUFFIXES = {
    ".nf", ".test", ".config", ".r", ".rmd", ".qmd", ".py", ".smk", ".sh",
    ".bash", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".lock",
    ".wdl", ".cwl", ".groovy", ".jl", ".pl", ".rb",
}
ROOT_SOURCE_NAMES = {"snakefile", "makefile", "dockerfile", ".rprofile"}
MAX_SOURCE_BYTES = 2 * 1024 * 1024
FIELD = re.compile(r"^\s*(?:-\s+)?\*\*([^*]+):\*\*\s*(.*)$")
DECISION_HEADING = re.compile(r"^### (D-\d+):\s*(.*)$")
BACKTICKS = re.compile(r"`([^`]+)`")
MARKER = re.compile(r"\((D-\d+)\)")
LOCAL_LINK = re.compile(
    r"(?<!!)\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[\"'][^)]*[\"'])?\s*\)"
)


@dataclass
class Entry:
    identifier: str
    title: str
    line: int
    fields: dict[str, tuple[int, str]] = field(default_factory=dict)


def markdown_lines(content: str) -> list[tuple[int, str]]:
    """Keep original line numbers while excluding fenced format/examples."""
    visible = []
    fence_char, fence_length = "", 0
    for number, line in enumerate(content.splitlines(), 1):
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence_char:
            if (fence and fence.group(1)[0] == fence_char
                    and len(fence.group(1)) >= fence_length
                    and not fence.group(2).strip()):
                fence_char, fence_length = "", 0
            continue
        if fence:
            fence_char, fence_length = fence.group(1)[0], len(fence.group(1))
            continue
        visible.append((number, line))
    return visible


def find_root(start: Path) -> Path:
    """Git is optional: an initialized document layout also identifies a root."""
    start = start.resolve()
    for candidate in (start, *start.parents):
        if ((candidate / "docs/DECISIONS.md").is_file()
                and (candidate / "docs/CODE_MAP.md").is_file()):
            return candidate
        if (candidate / ".git").exists():
            return candidate
    return start


class Audit:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.failures: list[str] = []
        self.warnings: list[str] = []
        self.sources: list[Path] = []
        self.cache: dict[Path, str | None] = {}
        self.paths_checked = 0
        self.symbols_checked = 0
        self.active: list[Entry] = []
        self.retired: list[str] = []
        self.reserved: list[str] = []
        self.unconfigured = False
        self.technical_brief_unconfigured = False

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def warn(self, message: str) -> None:
        if message not in self.warnings:
            self.warnings.append(message)

    def label(self, path: Path, line: int | None = None) -> str:
        name = path.relative_to(self.root).as_posix()
        return f"{name}:{line}" if line is not None else name

    def read_document(self, relative: str) -> str | None:
        path = self.root / relative
        try:
            if not path.resolve().is_relative_to(self.root):
                self.fail(f"document escapes project root: {relative}")
                return None
            return path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError, RuntimeError) as error:
            self.fail(f"cannot read required document {relative}: {error}")
            return None

    def canonical_id(self, identifier: str, where: str) -> str:
        prefix, number = identifier.split("-", 1)
        value = int(number)
        canonical = f"{prefix}-{value:03d}"
        if value < 1 or identifier != canonical:
            self.fail(f"invalid ID {identifier} at {where}; use positive canonical IDs")
        return canonical

    def load_config(self, config_path: Path | None) -> tuple[list[str], list[str]] | None:
        if config_path is None:
            candidate = self.root / "docs/audit-config.json"
            config_path = candidate if candidate.exists() else None
        if config_path is None:
            return ["."], list(DEFAULT_EXCLUDES)
        if not config_path.is_absolute():
            config_path = self.root / config_path
        try:
            config = json.loads(config_path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError, ValueError) as error:
            self.fail(f"cannot read audit configuration: {error}")
            return None
        if not isinstance(config, dict) or set(config) - {"source_paths", "exclude_paths"}:
            self.fail("configuration must be an object with only source_paths and exclude_paths")
            return None
        paths = config.get("source_paths", ["."])
        excludes = config.get("exclude_paths", list(DEFAULT_EXCLUDES))
        for name, values in (("source_paths", paths), ("exclude_paths", excludes)):
            if not isinstance(values, list) or any(
                    not isinstance(value, str) or not value.strip() for value in values):
                self.fail(f"configuration {name} must be a list of nonempty strings")
                return None
        return paths, excludes

    @staticmethod
    def excluded(relative: Path, patterns: list[str]) -> bool:
        name = relative.as_posix()
        for value in patterns:
            pattern = value.replace("\\", "/").removeprefix("./").rstrip("/")
            if "/" not in pattern and any(fnmatch.fnmatchcase(p, pattern) for p in relative.parts):
                return True
            if name == pattern or name.startswith(pattern + "/") or fnmatch.fnmatchcase(name, pattern):
                return True
        return False

    def collect_sources(self, paths: list[str], excludes: list[str]) -> None:
        collected: set[Path] = set()

        def add_file(path: Path) -> None:
            relative = path.relative_to(self.root)
            if self.excluded(relative, excludes):
                return
            if path.suffix.lower() not in TEXT_SUFFIXES and path.name.lower() not in ROOT_SOURCE_NAMES:
                return
            if path.is_symlink():
                self.warn(f"source symlink skipped: {self.label(path)}; review its provenance separately")
                return
            collected.add(path)

        for name in paths:
            if "\x00" in name:
                self.fail("invalid configured source path: NUL byte")
                continue
            try:
                if Path(name).is_absolute() or PureWindowsPath(name).drive:
                    self.fail(f"source path must be repository-relative: {name}")
                    continue
                path = (self.root / name.replace("\\", "/")).resolve()
            except (OSError, RuntimeError, ValueError) as error:
                self.fail(f"invalid configured source path {name!r}: {error}")
                continue
            if not path.is_relative_to(self.root):
                self.fail(f"source path escapes project root: {name}")
                continue
            if not path.exists():
                self.fail(f"configured source path missing: {name}")
                continue
            if path.is_file():
                add_file(path)
                continue

            def walk_error(error: OSError) -> None:
                self.fail(f"cannot enumerate configured source: {error}")

            for directory, subdirs, filenames in os.walk(path, followlinks=False, onerror=walk_error):
                parent = Path(directory)
                subdirs[:] = sorted(
                    child for child in subdirs
                    if not self.excluded((parent / child).relative_to(self.root), excludes)
                    and not (parent / child).is_symlink()
                )
                for filename in sorted(filenames):
                    add_file(parent / filename)
        self.sources = sorted(collected)

    def source_text(self, path: Path) -> str | None:
        if path not in self.cache:
            try:
                if not path.resolve().is_relative_to(self.root):
                    self.fail(f"source reference escapes project root: {self.label(path)}")
                    self.cache[path] = None
                elif path.stat().st_size > MAX_SOURCE_BYTES:
                    self.warn(f"source too large to inspect: {self.label(path)} (limit {MAX_SOURCE_BYTES} bytes)")
                    self.cache[path] = None
                else:
                    content = path.read_text(encoding="utf-8-sig")
                    if "\x00" in content:
                        self.warn(f"binary source skipped: {self.label(path)}")
                        self.cache[path] = None
                    else:
                        self.cache[path] = content
            except (OSError, UnicodeError, RuntimeError) as error:
                self.warn(f"source not inspected: {self.label(path)}: {error}")
                self.cache[path] = None
        return self.cache[path]

    def check_path(self, token: str, doc: Path, line: int, *, base: Path | None = None) -> Path | None:
        self.paths_checked += 1
        name = token.replace("\\", "/").rstrip("/")
        # A backticked repository reference may include a one-based source line.
        name = re.sub(r":\d+$", "", name)
        if not name or Path(name).is_absolute() or PureWindowsPath(name).drive:
            self.fail(f"reference must be repository-relative: {self.label(doc, line)} `{token}`")
            return None
        try:
            target = ((base or self.root) / name).resolve()
            if not target.is_relative_to(self.root):
                self.fail(f"reference escapes project root: {self.label(doc, line)} `{token}`")
                return None
            if not target.exists():
                self.fail(f"path missing: {self.label(doc, line)} `{token}`")
                return None
        except (OSError, RuntimeError, ValueError) as error:
            self.fail(f"invalid path: {self.label(doc, line)} `{token}`: {error}")
            return None
        return target

    def looks_like_path(self, token: str) -> bool:
        clean = re.sub(r":\d+$", "", token.replace("\\", "/"))
        return ("/" in clean or Path(clean).suffix.lower() in TEXT_SUFFIXES
                or Path(clean).name.lower() in ROOT_SOURCE_NAMES
                or (self.root / clean).exists())

    def check_references(self, value: str, doc: Path, line: int) -> set[Path]:
        paths: set[Path] = set()
        for clause in value.split(";"):
            tokens = BACKTICKS.findall(clause)
            if not tokens:
                if clause.strip():
                    self.fail(f"reference needs a backticked source path: {self.label(doc, line)}")
                continue
            current: Path | None = None
            for index, token in enumerate(tokens):
                if index == 0 or self.looks_like_path(token):
                    current = self.check_path(token, doc, line)
                    if current is not None:
                        paths.add(current)
                    continue
                self.symbols_checked += 1
                if current is None:
                    continue  # The preceding missing path already explains this failure.
                if not re.fullmatch(r"[A-Za-z_]\w*(?:(?:\.|::)[A-Za-z_]\w*)*(?:\(\))?", token):
                    self.fail(f"invalid optional symbol: {self.label(doc, line)} `{token}`")
                    continue
                names = re.findall(r"[A-Za-z_]\w*", token)
                candidates = [current] if current.is_file() else [
                    path for path in self.sources if path.is_relative_to(current)
                ]
                contents = [content for path in candidates if (content := self.source_text(path)) is not None]
                for name in names:
                    if not any(re.search(rf"(?<!\w){re.escape(name)}(?!\w)", content) for content in contents):
                        self.fail(f"symbol missing in cited source: {self.label(doc, line)} `{token}` ({name})")
        return paths

    def check_links(self, doc: Path, lines: list[tuple[int, str]]) -> None:
        for number, line in lines:
            for match in LOCAL_LINK.finditer(line):
                raw = match.group(1).strip("<>")
                try:
                    parsed = urlsplit(raw)
                except ValueError:
                    self.fail(f"invalid Markdown link: {self.label(doc, number)}")
                    continue
                if parsed.scheme or parsed.netloc:
                    if parsed.scheme.lower() == "file":
                        self.fail(f"absolute file link is not portable: {self.label(doc, number)}")
                    continue
                if parsed.path:
                    self.check_path(unquote(parsed.path), doc, number, base=doc.parent)

    def parse_decisions(self, lines: list[tuple[int, str]]) -> None:
        current: Entry | None = None
        section = ""
        for number, line in lines:
            if line.startswith("## "):
                section = line[3:].strip().lower()
                current = None
            heading = DECISION_HEADING.match(line)
            if heading:
                identifier = self.canonical_id(heading.group(1), f"DECISIONS.md:{number}")
                current = Entry(identifier, heading.group(2), number)
                self.active.append(current)
                if section == "retired ids":
                    self.fail(f"active heading {identifier} appears in Retired IDs")
                continue
            if line.startswith("### "):
                current = None
            if section == "retired ids":
                retired = re.match(r"^- (D-\d+):\s*(.*)$", line)
                if retired:
                    self.retired.append(self.canonical_id(retired.group(1), f"DECISIONS.md:{number}"))
                    if not retired.group(2).strip():
                        self.fail(f"retired ID needs a reason: DECISIONS.md:{number}")
            if current and (match := FIELD.match(line)):
                key = match.group(1).lower()
                if key in current.fields:
                    self.fail(f"duplicate {key} field for {current.identifier}")
                current.fields[key] = (number, match.group(2))

    def check_code_map(self, lines: list[tuple[int, str]]) -> None:
        doc = self.root / "docs/CODE_MAP.md"
        in_files = False
        for number, line in lines:
            if line.startswith("#"):
                in_files = False
            if match := FIELD.match(line):
                in_files = match.group(1).lower() == "key files"
                if in_files and match.group(2).strip():
                    self.check_references(match.group(2), doc, number)
                continue
            if in_files and re.match(r"^\s*-\s+", line):
                self.check_references(re.sub(r"^\s*-\s+", "", line), doc, number)

    def check_ids(self, ledger_lines: list[tuple[int, str]]) -> None:
        doc = self.root / "docs/DECISIONS.md"
        active = {entry.identifier for entry in self.active}
        for number, line in ledger_lines:
            if match := re.match(r"^- (D-\d+) is reserved:\s*(.*)$", line):
                self.reserved.append(self.canonical_id(match.group(1), f"LEDGER.md:{number}"))
                if not match.group(2).strip():
                    self.fail(f"reserved ID needs a reason: LEDGER.md:{number}")
        for category, identifiers in (
                ("active", [entry.identifier for entry in self.active]),
                ("retired", self.retired), ("reserved", self.reserved)):
            for identifier, count in Counter(identifiers).items():
                if count > 1:
                    self.fail(f"duplicate {category} ID {identifier}")
        for identifier in sorted(active | set(self.retired) | set(self.reserved)):
            # Membership across categories matters; repetition within one is checked above.
            memberships = sum(identifier in group for group in (active, self.retired, self.reserved))
            if memberships > 1:
                self.fail(f"ID {identifier} is allocated in multiple categories")
        used = sorted(int(identifier.split("-")[1]) for identifier in active | set(self.retired) | set(self.reserved))
        expected = 1
        for value in used:
            if value > expected:
                last = value - 1
                missing = f"D-{expected:03d}" if last == expected else f"D-{expected:03d} through D-{last:03d}"
                self.fail(f"unexplained decision ID gap: {missing}")
            expected = value + 1

        ledger = "\n".join(line for _, line in ledger_lines)
        counter = re.compile(r"next free are \*\*(F-\d+)\*\* and \*\*(D-\d+)\*\*")
        counters = list(counter.finditer(ledger))
        if len(counters) != 1:
            self.fail("ledger must have exactly one 'next free' IDs line")
        else:
            fix, decision = counters[0].groups()
            self.canonical_id(fix, "ledger next free")
            self.canonical_id(decision, "ledger next free")
            highest = max(used, default=0)
            if int(decision.split("-")[1]) != highest + 1:
                self.fail(f"ledger next decision is {decision}; expected D-{highest + 1:03d}")
            without_counter = counter.sub("", ledger)
            fixes = [self.canonical_id(item, "ledger allocation history")
                     for item in re.findall(r"\bF-\d+\b", without_counter)]
            highest_fix = max((int(item.split("-")[1]) for item in fixes), default=0)
            if int(fix.split("-")[1]) != highest_fix + 1:
                self.fail(f"ledger next finding is {fix}; expected F-{highest_fix + 1:03d}")

        # Code markers must point at active decisions. Expectations in unrelated
        # source/test literals must not use the reserved parenthesized marker.
        tagged: dict[str, set[Path]] = {}
        for source in self.sources:
            content = self.source_text(source)
            if content is None:
                continue
            for number, line in enumerate(content.splitlines(), 1):
                for marker in MARKER.findall(line):
                    identifier = self.canonical_id(marker, self.label(source, number))
                    tagged.setdefault(identifier, set()).add(source)
                    if identifier not in active:
                        self.fail(f"source marker {identifier} is not an active decision: {self.label(source, number)}")

        stacks = {entry.identifier for entry in self.active if "rule stack" in entry.title.lower()}
        for entry in self.active:
            code = entry.fields.get("code")
            if code is None:
                self.fail(f"missing Code field for {entry.identifier}")
                continue
            line, value = code
            process_only = re.fullmatch(r"None\s*\((?:process|rule stack)\)\.?", value, re.I) is not None
            if process_only:
                if entry.identifier in tagged:
                    self.warn(f"process-only {entry.identifier} has source markers; review Code coverage")
            else:
                references = self.check_references(value, doc, line)
                if not value.strip():
                    self.fail(f"empty Code field for {entry.identifier}")
                implementations = tagged.get(entry.identifier, set())
                if not implementations:
                    self.warn(f"active decision has no source marker: {entry.identifier}")
                for reference in references:
                    has_tag = reference in implementations if reference.is_file() else any(
                        path.is_relative_to(reference) for path in implementations
                    )
                    if not has_tag:
                        self.warn(f"cited implementation lacks {entry.identifier} marker: {self.label(reference)}")
                for implementation in implementations:
                    if not any(implementation == reference or (reference.is_dir() and implementation.is_relative_to(reference))
                               for reference in references):
                        self.warn(f"{entry.identifier} marker is outside its Code references: {self.label(implementation)}")
            if "since" not in entry.fields:
                self.fail(f"missing Since field for {entry.identifier}")
            elif "(in progress)" in entry.fields["since"][1].lower():
                self.warn(f"{entry.identifier} is in progress")
            if "passes" in entry.fields:
                cited = re.findall(r"\bD-\d+\b", entry.fields["passes"][1])
                if not cited:
                    self.fail(f"{entry.identifier} Passes needs a rule stack ID")
                for identifier in cited:
                    if identifier not in stacks:
                        self.fail(f"{entry.identifier} Passes cites {identifier}, not an active rule stack")

    def run(self, config_path: Path | None) -> int:
        if not self.root.is_dir():
            self.fail(f"project root is not a directory: {self.root}")
            return self.report()
        config = self.load_config(config_path)
        if config is None:
            return self.report()
        decisions = self.read_document("docs/DECISIONS.md")
        code_map = self.read_document("docs/CODE_MAP.md")
        ledger = self.read_document("docs/LEDGER.md")
        if any(content is None for content in (decisions, code_map, ledger)):
            return self.report()
        charter_path = self.root / "docs/PROJECT.md"
        if charter_path.exists():
            charter = self.read_document("docs/PROJECT.md") or ""
            self.unconfigured = bool(re.search(r"\*\*(?:Template|Status):\*\*\s*UNCONFIGURED\b", charter, re.I))
        brief_path = self.root / "docs/PROJECT_BRIEF.md"
        if brief_path.exists():
            brief = self.read_document("docs/PROJECT_BRIEF.md") or ""
            self.technical_brief_unconfigured = bool(re.search(r"\*\*Status:\*\*\s*UNCONFIGURED\b", brief, re.I))
            if not charter_path.exists():
                self.unconfigured = self.technical_brief_unconfigured  # Legacy standalone audit layouts.
        self.collect_sources(*config)
        decision_lines = markdown_lines(decisions)
        map_lines = markdown_lines(code_map)
        self.parse_decisions(decision_lines)
        self.check_code_map(map_lines)
        self.check_links(self.root / "docs/DECISIONS.md", decision_lines)
        self.check_links(self.root / "docs/CODE_MAP.md", map_lines)
        self.check_ids(markdown_lines(ledger))
        return self.report()

    def report(self) -> int:
        print(f"Project: {self.root}")
        print(f"Checked {len(self.sources)} source files, {self.paths_checked} paths, {self.symbols_checked} optional symbols.")
        print(f"Decision IDs: {len(self.active)} active, {len(self.retired)} retired, {len(self.reserved)} reserved.")
        for message in self.failures:
            print(f"FAIL {message}")
        for message in self.warnings:
            print(f"WARN {message}")
        if self.unconfigured:
            print("INFO UNCONFIGURED template: project approvals and scientific evidence are still unset.")
        if self.technical_brief_unconfigured:
            print("INFO Technical brief: UNCONFIGURED; detailed task design is separate from the project charter.")
        outcome = "FAIL" if self.failures else "PASS"
        print(f"RESULT: {outcome} ({len(self.failures)} fail, {len(self.warnings)} warn)")
        print("Mechanical audit only; scientific validity, owner approval, and release readiness are not assessed.")
        return 1 if self.failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="project root (default: discover from current directory)")
    parser.add_argument("--config", type=Path, help="JSON configuration; relative paths use the project root")
    args = parser.parse_args(argv)
    return Audit(args.root or find_root(Path.cwd())).run(args.config)


if __name__ == "__main__":
    sys.exit(main())
