"""Structural distribution checks; these do not validate a scientific pipeline."""
from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[4]


class TemplateTests(unittest.TestCase):
    def test_expected_distribution_is_present(self):
        required = [
            "AGENTS.md", "README.md", "LICENSE", "UPSTREAM.md",
            "docs/PROJECT_BRIEF.md", "docs/DECISIONS.md", "docs/CODE_MAP.md",
            "docs/LEDGER.md", "docs/RELEASE_PROCESS.md", "docs/VALIDATION.md",
            "docs/RUN_RECORD_TEMPLATE.md", "docs/GLOSSARY.md", "docs/BACKLOG.md",
            "docs/audit-config.json", "examples/README.md", "examples/engine-guidance.md",
            ".github/workflows/template-checks.yml",
            "docs/WORKFLOW_STATE.json", "scripts/workflow_state.py",
            "docs/PROJECT.md", "scripts/_workflow_state_v1.py",
        ]
        for name in required:
            with self.subTest(path=name):
                self.assertTrue((ROOT / name).is_file())

    def test_repository_skills_have_valid_discovery_frontmatter(self):
        skills = sorted((ROOT / ".agents/skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 4)
        for skill in skills:
            with self.subTest(skill=skill.parent.name):
                content = skill.read_text(encoding="utf-8")
                self.assertTrue(content.startswith("---\n"))
                parts = content.split("---", 2)
                self.assertEqual(len(parts), 3)
                name = re.search(r"(?m)^name: ([a-z0-9-]+)$", parts[1])
                description = re.search(r"(?m)^description: (.+)$", parts[1])
                self.assertIsNotNone(name)
                self.assertEqual(name.group(1), skill.parent.name)
                self.assertLess(len(name.group(1)), 64)
                self.assertIsNotNone(description)
                self.assertTrue(parts[2].strip())

    def test_distribution_has_no_broken_local_markdown_links(self):
        for doc in ROOT.rglob("*.md"):
            if ".git" in doc.relative_to(ROOT).parts:
                continue
            content = doc.read_text(encoding="utf-8")
            for match in re.finditer(r"\[[^\]]+\]\((<[^>]+>|[^\s)]+)\)", content):
                raw = match.group(1).strip("<>")
                link = urlsplit(raw)
                if link.scheme or link.netloc or not link.path:
                    continue
                with self.subTest(doc=doc.relative_to(ROOT), target=raw):
                    target = (doc.parent / unquote(link.path)).resolve()
                    self.assertTrue(target.is_relative_to(ROOT))
                    self.assertTrue(target.exists(), f"{doc}: {raw}")

    def test_unconfigured_template_passes_only_the_mechanical_audit(self):
        checker = ROOT / ".agents/skills/docs-audit/scripts/check_docs.py"
        result = subprocess.run([sys.executable, str(checker), "--root", str(ROOT)],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("INFO UNCONFIGURED", result.stdout)
        self.assertIn("0 fail, 0 warn", result.stdout)


if __name__ == "__main__":
    unittest.main()
