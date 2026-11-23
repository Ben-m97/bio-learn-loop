"""Behavioral CLI tests using isolated, synthetic projects, not biological data."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest


TEMPLATE_ROOT = Path(__file__).resolve().parents[4]
CHECKER = TEMPLATE_ROOT / ".agents/skills/docs-audit/scripts/check_docs.py"


class AuditCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="bio audit ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project with spaces"
        self.root.mkdir()
        self.write("docs/DECISIONS.md", self.decision())
        self.write("docs/CODE_MAP.md", "# Code map\n\n## Stage\n**Key files:**\n- `src/stage.py` `transform`\n")
        self.write("docs/LEDGER.md", self.ledger())
        self.write("src/stage.py", "# Preserve entity identity (D-001).\ndef transform(value):\n    return value\n")

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    @staticmethod
    def decision(identifier="D-001", code="`src/stage.py` `transform`", title="Preserve identity"):
        return f"""# Decisions

## Active decisions

### {identifier}: {title}
- **Rule:** Preserve input identity in the output.
- **Why:** Synthetic fixture rule for the test project.
- **Approval:** Synthetic test fixture, not an actual owner approval.
- **Code:** {code}
- **Since:** test-version

"""

    @staticmethod
    def ledger(fix="F-001", decision="D-002", extra=""):
        return f"# Ledger\n\n- **IDs:** next free are **{fix}** and **{decision}**.\n\n{extra}\n"

    def run_audit(self, *extra, cwd=None, discover=False):
        command = [sys.executable, str(CHECKER)]
        if not discover:
            command += ["--root", str(self.root)]
        command += list(extra)
        environment = dict(os.environ, PYTHONUTF8="1")
        result = subprocess.run(command, cwd=cwd or self.root, capture_output=True,
                                text=True, encoding="utf-8", env=environment, timeout=20)
        self.assertNotIn("Traceback", result.stderr + result.stdout)
        return result

    def assert_pass(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("RESULT: PASS", result.stdout)

    def assert_failure(self, result, diagnostic):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(diagnostic, result.stdout)

    def test_valid_project_without_git_and_with_spaces(self):
        self.assertFalse((self.root / ".git").exists())
        self.assert_pass(self.run_audit(cwd=Path(self.temp.name)))

    def test_discovers_root_from_nested_directory_without_git(self):
        nested = self.root / "src/nested"
        nested.mkdir()
        result = self.run_audit(cwd=nested, discover=True)
        self.assert_pass(result)
        self.assertIn(str(self.root), result.stdout)

    def test_root_workflow_files_and_multiple_languages_are_scanned(self):
        references = []
        for name in ("main.nf", "nextflow.config", "Snakefile", "analysis.R", "helper.py", "rules/check.smk"):
            self.write(name, "# Approved behavior (D-001).\nstep_name = 1\n")
            references.append(f"`{name}` `step_name`")
        references.append("`src/stage.py` `transform`")
        self.write("docs/DECISIONS.md", self.decision(code="; ".join(references)))
        result = self.run_audit()
        self.assert_pass(result)
        self.assertNotIn("WARN", result.stdout)

    def test_unapproved_marker_in_root_entrypoint_is_detected(self):
        self.write("Snakefile", "# Changed method (D-009).\n")
        self.assert_failure(self.run_audit(), "source marker D-009 is not an active decision")

    def test_missing_explicit_source_path_fails(self):
        self.write("docs/DECISIONS.md", self.decision(code="`src/absent.py` `transform`"))
        self.assert_failure(self.run_audit(), "path missing")

    def test_missing_symbol_cannot_be_satisfied_by_substring(self):
        self.write("src/stage.py", "# Identity (D-001).\ndef transform_counts(value):\n    return value\n")
        self.assert_failure(self.run_audit(), "symbol missing in cited source")

    def test_symbol_in_another_file_does_not_rescue_wrong_reference(self):
        self.write("src/stage.py", "# Identity (D-001).\nother = 1\n")
        self.write("src/other.py", "def transform(value):\n    return value\n")
        self.assert_failure(self.run_audit(), "symbol missing in cited source")

    def test_scientific_literals_and_runtime_outputs_are_not_symbols(self):
        self.write("docs/CODE_MAP.md", """# Code map
            ## Stage
            **Does:** Calculate `TP53`, `log2 fold change`, and `p.adjust` values.
            **Key files:**
            - `src/stage.py` `transform`
            **Outputs:** `results/not-created.tsv` and `reference/genome.fa` are runtime products.
            """)
        self.assert_pass(self.run_audit())

    def test_fenced_format_examples_do_not_allocate_ids_or_paths(self):
        content = self.decision() + """## Format
~~~markdown
### D-999: Illustrative only
- **Code:** `missing.py` `missing`
```
[missing](missing.py)
```
~~~
"""
        self.write("docs/DECISIONS.md", content)
        self.assert_pass(self.run_audit())

    def test_duplicate_active_ids_fail(self):
        self.write("docs/DECISIONS.md", self.decision() + self.decision())
        self.assert_failure(self.run_audit(), "duplicate active ID D-001")

    def test_retired_and_reserved_ids_fill_gaps(self):
        self.write("docs/DECISIONS.md", self.decision("D-003") + "## Retired IDs\n- D-001: replaced by D-003.\n")
        self.write("src/stage.py", "# Identity (D-003).\ndef transform(value):\n    return value\n")
        self.write("docs/LEDGER.md", self.ledger(decision="D-004", extra="- D-002 is reserved: pending choice.\n"))
        self.assert_pass(self.run_audit())

    def test_unexplained_decision_id_gap_fails(self):
        self.write("docs/DECISIONS.md", self.decision("D-003") + "## Retired IDs\n- D-001: replaced.\n")
        self.write("src/stage.py", "# Identity (D-003).\ndef transform(value):\n    return value\n")
        self.write("docs/LEDGER.md", self.ledger(decision="D-004"))
        self.assert_failure(self.run_audit(), "unexplained decision ID gap: D-002")

    def test_same_id_cannot_be_active_and_retired(self):
        self.write("docs/DECISIONS.md", self.decision() + "## Retired IDs\n- D-001: replaced.\n")
        self.assert_failure(self.run_audit(), "allocated in multiple categories")

    def test_duplicate_retired_and_reserved_ids_fail(self):
        self.write("docs/DECISIONS.md", self.decision() + "## Retired IDs\n- D-002: first.\n- D-002: repeated.\n")
        self.write("docs/LEDGER.md", self.ledger(decision="D-004", extra=(
            "- D-003 is reserved: first.\n- D-003 is reserved: repeated.\n")))
        result = self.run_audit()
        self.assert_failure(result, "duplicate retired ID D-002")
        self.assertIn("duplicate reserved ID D-003", result.stdout)

    def test_retired_id_in_source_is_not_active(self):
        self.write("docs/DECISIONS.md", self.decision() + "## Retired IDs\n- D-002: obsolete.\n")
        self.write("docs/LEDGER.md", self.ledger(decision="D-003"))
        self.write("src/old.R", "# Old method (D-002).\n")
        self.assert_failure(self.run_audit(), "source marker D-002 is not an active decision")

    def test_counter_uses_persistent_closed_finding_history(self):
        self.write("docs/LEDGER.md", self.ledger(fix="F-005", extra="## Closed IDs\n- F-004: released in test-version.\n"))
        self.assert_pass(self.run_audit())
        self.write("docs/LEDGER.md", self.ledger(fix="F-004", extra="## Closed IDs\n- F-004: released in test-version.\n"))
        self.assert_failure(self.run_audit(), "ledger next finding is F-004; expected F-005")

    def test_stale_or_missing_decision_counters_fail(self):
        self.write("docs/LEDGER.md", self.ledger(decision="D-001"))
        self.assert_failure(self.run_audit(), "ledger next decision is D-001; expected D-002")
        self.write("docs/LEDGER.md", "# Ledger\nNo counter.\n")
        self.assert_failure(self.run_audit(), "exactly one 'next free' IDs line")

    def test_process_entry_does_not_hide_another_missing_marker(self):
        self.write("src/stage.py", "def transform(value):\n    return value\n")
        self.write("docs/DECISIONS.md", self.decision() + self.decision("D-002", "None (process)", "Approval rule"))
        self.write("docs/LEDGER.md", self.ledger(decision="D-003"))
        result = self.run_audit()
        self.assert_pass(result)
        self.assertIn("active decision has no source marker: D-001", result.stdout)

    def test_marker_outside_code_references_warns(self):
        self.write("src/extra.R", "# Same identity rule (D-001).\n")
        result = self.run_audit()
        self.assert_pass(result)
        self.assertIn("marker is outside its Code references", result.stdout)

    def test_in_progress_is_a_warning(self):
        self.write("docs/DECISIONS.md", self.decision().replace("test-version", "test-version (in progress)"))
        result = self.run_audit()
        self.assert_pass(result)
        self.assertIn("D-001 is in progress", result.stdout)

    def test_passes_must_cite_active_rule_stack(self):
        self.write("docs/DECISIONS.md", self.decision() + "- **Passes:** D-001 1\n")
        self.assert_failure(self.run_audit(), "not an active rule stack")
        self.write("docs/DECISIONS.md", self.decision(title="Identity rule stack", code="None (rule stack)")
                   + self.decision("D-002") + "- **Passes:** D-001 1\n")
        self.write("src/stage.py", "# Identity (D-002).\ndef transform(value):\n    return value\n")
        self.write("docs/LEDGER.md", self.ledger(decision="D-003"))
        self.assert_pass(self.run_audit())

    def test_relative_config_uses_project_root_from_another_cwd(self):
        self.write("custom/settings.json", json.dumps({"source_paths": ["src"], "exclude_paths": []}))
        self.write("ignored.py", "# Ignore this root source for this configured run (D-999).\n")
        self.assert_pass(self.run_audit("--config", "custom/settings.json", cwd=Path(self.temp.name)))

    def test_default_exclusions_keep_data_results_examples_and_skills_out(self):
        for name in ("data/raw.py", "results/output.R", "work/task.nf", "examples/demo.py",
                     ".agents/skills/demo/script.py", "resources/genome.config"):
            self.write(name, "# Illustrative/generated content (D-999).\n")
        self.assert_pass(self.run_audit())

    def test_custom_source_and_exclusion_lists_are_honored(self):
        self.write("src/generated/artifact.py", "# Generated literal (D-999).\n")
        self.write("docs/audit-config.json", json.dumps({"source_paths": ["src"], "exclude_paths": ["src/generated/**"]}))
        self.assert_pass(self.run_audit())
        self.write("docs/audit-config.json", json.dumps({"source_paths": ["src"], "exclude_paths": []}))
        self.assert_failure(self.run_audit(), "source marker D-999")

    def test_invalid_config_and_missing_sources_fail_cleanly(self):
        for config in ({"source_paths": "src"}, {"source_path": ["src"]}, {"source_paths": [None]}):
            with self.subTest(config=config):
                self.write("docs/audit-config.json", json.dumps(config))
                self.assert_failure(self.run_audit(), "configuration")
        self.write("docs/audit-config.json", json.dumps({"source_paths": ["absent"]}))
        self.assert_failure(self.run_audit(), "configured source path missing")

    def test_source_paths_cannot_escape_root(self):
        self.write("docs/audit-config.json", json.dumps({"source_paths": [".."]}))
        self.assert_failure(self.run_audit(), "source path escapes project root")

    def test_invalid_source_path_values_fail_without_a_traceback(self):
        self.write("docs/audit-config.json", json.dumps({"source_paths": ["bad\x00path"]}))
        self.assert_failure(self.run_audit(), "invalid configured source path")
        self.write("docs/audit-config.json", json.dumps({"source_paths": ["C:drive-relative.py"]}))
        self.assert_failure(self.run_audit(), "source path must be repository-relative")

    def test_binary_and_non_utf8_sources_are_explicitly_uninspected(self):
        self.write("src/binary.py", b"a\x00b")
        self.write("src/encoding.R", b"\xff\xfe\x80")
        result = self.run_audit()
        self.assert_pass(result)
        self.assertIn("binary source skipped", result.stdout)
        self.assertIn("source not inspected", result.stdout)

    def test_missing_required_document_fails_cleanly(self):
        (self.root / "docs/CODE_MAP.md").unlink()
        self.assert_failure(self.run_audit(), "cannot read required document")

    def test_windows_style_source_reference_and_source_line(self):
        self.write("docs/DECISIONS.md", self.decision(code="`src\\stage.py:2` `transform`"))
        self.assert_pass(self.run_audit())

    def test_source_filename_with_spaces_and_unicode(self):
        self.write("src/my étape.R", "# Identity (D-001).\nnormalize_counts <- function(x) x\n")
        self.write("docs/DECISIONS.md", self.decision(code="`src/stage.py` `transform`; `src/my étape.R` `normalize_counts`"))
        self.assert_pass(self.run_audit())

    def test_local_markdown_links_are_document_relative_and_support_spaces(self):
        self.write("src/my step.R", "value <- 1\n")
        self.write("docs/CODE_MAP.md", "# Code map\n\n## Stage\n"
                   "**Flow:** [source](../src/stage.py#L2), [R step](<../src/my step.R>), "
                   "[encoded](../src/my%20step.R), [external](https://example.org/docs).\n")
        self.assert_pass(self.run_audit())
        self.write("docs/CODE_MAP.md", "# Code map\n\n## Stage\n[source](../missing.py)\n")
        self.assert_failure(self.run_audit(), "path missing")

    def test_local_references_cannot_escape_root(self):
        self.write("docs/DECISIONS.md", self.decision(code="`../external.py`"))
        self.assert_failure(self.run_audit(), "reference escapes project root")

    def test_directory_reference_checks_its_scanned_source(self):
        self.write("docs/DECISIONS.md", self.decision(code="`src/` `transform`"))
        self.assert_pass(self.run_audit())

    def test_unconfigured_status_does_not_claim_release_readiness(self):
        self.write("docs/PROJECT_BRIEF.md", "# Brief\n\n**Status:** UNCONFIGURED\n")
        result = self.run_audit()
        self.assert_pass(result)
        self.assertIn("INFO UNCONFIGURED", result.stdout)
        self.assertIn("release readiness are not assessed", result.stdout)

    def test_missing_root_fails_cleanly(self):
        result = self.run_audit("--root", str(self.root / "not here"))
        self.assert_failure(result, "project root is not a directory")

    def test_charter_configuration_is_distinct_from_technical_design(self):
        self.write("docs/PROJECT.md", "# Project\nExplore biological data and learn. Tools undecided.\n")
        self.write("docs/PROJECT_BRIEF.md", "# Technical brief\n**Status:** UNCONFIGURED\n")
        result = self.run_audit()
        self.assert_pass(result)
        self.assertNotIn("INFO UNCONFIGURED template", result.stdout)
        self.assertIn("Technical brief: UNCONFIGURED", result.stdout)


if __name__ == "__main__":
    unittest.main()
