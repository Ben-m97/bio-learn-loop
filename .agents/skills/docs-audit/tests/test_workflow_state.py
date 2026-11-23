"""Synthetic CLI tests for project initialization, task lifecycle, and migration.

These test recording constraints, not a real chat speaker or scientific approval.
No actual project state or Git is mutated.
"""
from __future__ import annotations
import argparse
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[4]
HELPER = ROOT / "scripts/workflow_state.py"
sys.path.insert(0, str(ROOT / "scripts"))
import workflow_state as engine
import _workflow_state_v1 as legacy
sys.path.pop(0)
STAGES = ("Guide", "Learn", "Choose", "Document", "Build", "Understand", "Reflect")
CHARTER = "# Project\nExplore biological data and learn to build reliable pipelines.\nTools, architecture and detailed requirements are undecided.\n"

class TemporaryProject(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="guided workflow ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "project with spaces"
        (self.root / "docs").mkdir(parents=True)
        self.path = self.root / "docs/WORKFLOW_STATE.json"
        self.charter = self.root / "docs/PROJECT.md"
        self.charter.write_text(CHARTER, encoding="utf-8")
        # Fixtures must not inherit or mutate a real project's live stage.
        self.path.write_text(json.dumps(engine.initial_state()), encoding="utf-8")

    def state(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def call(self, action, *extra, code=0, command=None, reference="synthetic-owner-message", revision=None):
        args = [sys.executable, str(HELPER), "--root", str(self.root), action]
        if action != "status":
            args += ["--expected-revision", str(self.state()["revision"] if revision is None else revision)]
            if action != "ready":
                args += ["--owner-command", engine.OWNER_COMMANDS.get(action, "") if command is None else command,
                         "--authorization-ref", reference]
        result = subprocess.run(args + list(extra), capture_output=True, text=True, encoding="utf-8",
                                timeout=20, env=dict(os.environ, PYTHONUTF8="1"))
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def ready(self):
        return self.call("ready", "--evidence", "Synthetic completion evidence; no biological result.")

    def move(self, stage, **kwargs):
        kwargs.setdefault("command", f"Move to {stage}")
        return self.call("move", "--to", stage, **kwargs)

    def prepare_project(self):
        self.call("initialise")
        self.call("approve-project")
        self.move("Guide")

    def start(self, task="T-001", attempt="A-001", **kwargs):
        return self.call("start", "--task-id", task, "--attempt-id", attempt,
                         "--title", "Synthetic input validation", **kwargs)

    def reach(self, stage):
        current = self.state()["current_stage"]
        for target in STAGES[STAGES.index(current) + 1:STAGES.index(stage) + 1]:
            self.ready()
            self.move(target)

    def reopen_and_approve(self):
        self.call("reopen-project", "--reason", "Synthetic change in purpose")
        self.charter.write_text("# Project\nBuild a general workflow framework. Methods undecided.\n", encoding="utf-8")
        self.call("approve-project")
        self.move("Guide")

class InitialiseTests(TemporaryProject):
    def test_read_only_status_preserves_not_started_state(self):
        original = self.path.read_bytes()
        self.assertEqual(json.loads(self.call("status").stdout)["current_stage"], "NOT_STARTED")
        self.assertEqual(original, self.path.read_bytes())

    def test_task_cannot_start_before_initialise(self):
        self.start(code=1)
        self.move("Guide", code=1)
        self.assertIsNone(self.state()["active_task"])

    def test_vague_vision_needs_no_technical_decisions(self):
        self.prepare_project()
        state = self.state()
        self.assertEqual(state["project"]["status"], "APPROVED")
        self.assertEqual(state["current_stage"], "Guide")
        self.assertIsNone(state["active_task"])
        self.assertEqual(state["project"]["approved_charter"]["text"], CHARTER)
        self.assertFalse((self.root / "docs/PROJECT_BRIEF.md").exists())
        self.assertFalse((self.root / "docs/DECISIONS.md").exists())

    def test_ready_without_approval_cannot_exit_initialise(self):
        self.call("initialise")
        self.ready()
        self.move("Guide", code=1)
        self.assertEqual(self.state()["current_stage"], "Initialise")

    def test_charter_approval_does_not_advance_or_select_task(self):
        self.call("initialise")
        self.call("approve-project")
        state = self.state()
        self.assertEqual(state["current_stage"], "Initialise")
        self.assertEqual(state["stage_status"], "READY")
        self.assertIsNone(state["active_task"])
        self.move("Build", code=1)
        self.start(code=1)
        self.move("Guide")
        self.move("Learn", code=1)

    def test_unconfigured_charter_cannot_be_approved(self):
        self.charter.write_text("# Project\n**Template:** UNCONFIGURED\n", encoding="utf-8")
        self.call("initialise")
        self.call("approve-project", code=1)
        self.assertEqual(self.state()["project"]["status"], "INITIALISING")

    def test_initialise_once_and_reopen_requires_explicit_instruction(self):
        self.prepare_project()
        self.call("initialise", code=1)
        self.move("Initialise", code=1)
        self.call("reopen-project", "--reason", "New purpose", command="continue", code=1)
        self.assertEqual(self.state()["project"]["charter_revision"], 1)

    def test_charter_drift_does_not_silently_approve_changes(self):
        self.prepare_project()
        self.charter.write_text("# Project\nDifferent purpose.\n", encoding="utf-8")
        original = self.path.read_bytes()
        self.start(code=1)
        self.assertEqual(original, self.path.read_bytes())
        self.call("reopen-project", "--reason", "Owner redefines purpose")
        self.assertEqual(self.state()["current_stage"], "Initialise")

    def test_missing_charter_prevents_approval(self):
        self.call("initialise")
        self.charter.unlink()
        self.call("approve-project", code=1)

class WorkflowStateTests(TemporaryProject):
    def setUp(self):
        super().setUp()
        # Prepare approved context in memory; the CLI still validates its history.
        state = engine.initial_state()
        for action, payload, command in (
            ("initialise", {}, "Start Initialise"),
            ("approve-project", {"charter_text": CHARTER}, "Approve project description"),
            ("move", {"to": "Guide"}, "Move to Guide"),
        ):
            engine.apply(state, action, payload, {"command": command, "reference": "synthetic-setup"})
        self.path.write_text(json.dumps(state), encoding="utf-8")

    def test_separate_task_and_attempt_identity(self):
        self.start()
        task = self.state()["active_task"]
        self.assertEqual((task["task_id"], task["attempt_id"], task["charter_revision"]), ("T-001", "A-001", 1))

    def test_ready_and_generic_encouragement_never_advance(self):
        self.start()
        self.ready()
        original = self.path.read_bytes()
        for command in ("continue", "go ahead", "Looks good", "", "Move to Build"):
            self.move("Learn", command=command, code=1)
            self.assertEqual(original, self.path.read_bytes())
        self.assertEqual(self.state()["current_stage"], "Guide")

    def test_missing_reference_and_stale_revision_fail(self):
        self.start()
        self.ready()
        original = self.path.read_bytes()
        self.move("Learn", reference=" ", code=1)
        self.move("Learn", revision=0, code=1)
        self.assertEqual(original, self.path.read_bytes())

    def test_no_forward_skip_or_move_before_ready(self):
        self.start()
        self.move("Learn", code=1)
        self.ready()
        self.move("Build", code=1)
        self.move("Learn")

    def test_resume_uses_state_instead_of_ledger_or_chat(self):
        self.start()
        self.reach("Learn")
        (self.root / "docs/LEDGER.md").write_text("Current stage: Build", encoding="utf-8")
        (self.root / "conversation.txt").write_text("We finished Reflect; go ahead.", encoding="utf-8")
        self.assertEqual(json.loads(self.call("status").stdout)["current_stage"], "Learn")

    def test_backtrack_does_not_repeat_initialise(self):
        self.start()
        self.reach("Choose")
        self.move("Learn")
        self.assertEqual(self.state()["project"]["charter_revision"], 1)

    def test_finish_returns_guide_no_task_and_no_git(self):
        self.start()
        self.call("finish", code=1)
        self.reach("Reflect")
        self.call("finish", code=1)
        self.ready()
        self.call("finish", command="Looks good", code=1)
        self.call("finish")
        state = self.state()
        self.assertEqual(state["current_stage"], "Guide")
        self.assertIsNone(state["active_task"])
        self.assertEqual(state["attempts"][-1]["disposition"], "COMPLETE")
        self.assertFalse((self.root / ".git").exists())
        self.start(task="T-002", attempt="A-002")
        self.assertEqual(self.state()["project"]["charter_revision"], 1)

    def test_restart_preserves_task_evidence_and_files(self):
        self.start()
        self.reach("Build")
        self.ready()
        artifact = self.root / "existing-output.txt"
        artifact.write_text("Keep this evidence", encoding="utf-8")
        self.call("restart", "--attempt-id", "A-002", "--reason", "Reconsider approach")
        state = self.state()
        self.assertEqual(state["current_stage"], "Guide")
        self.assertEqual(state["active_task"]["task_id"], "T-001")
        self.assertEqual(state["active_task"]["attempt_number"], 2)
        self.assertEqual(state["attempts"][-1]["task"]["attempt_id"], "A-001")
        self.assertIn("Synthetic completion", state["attempts"][-1]["evidence"])
        self.assertEqual(artifact.read_text(encoding="utf-8"), "Keep this evidence")

    def test_abandon_preserves_files_and_returns_guide(self):
        self.start()
        self.reach("Build")
        artifact = self.root / "pipeline.py"
        artifact.write_text("existing_code = True\n", encoding="utf-8")
        self.call("abandon", "--reason", "Owner drops task")
        self.assertEqual(self.state()["current_stage"], "Guide")
        self.assertIsNone(self.state()["active_task"])
        self.assertEqual(self.state()["attempts"][-1]["disposition"], "ABANDONED")
        self.assertEqual(artifact.read_text(encoding="utf-8"), "existing_code = True\n")

    def test_reopen_suspends_exact_checkpoint_and_preserves_prior_charter(self):
        self.start()
        self.reach("Build")
        self.ready()
        old = copy.deepcopy(self.state())
        self.call("reopen-project", "--reason", "Different overall objective")
        state = self.state()
        self.assertEqual(state["current_stage"], "Initialise")
        self.assertIsNone(state["active_task"])
        self.assertEqual(state["suspended_task"]["task"], old["active_task"])
        self.assertEqual(state["suspended_task"]["stage"], "Build")
        self.assertEqual(state["suspended_task"]["evidence"], old["stage_evidence"])
        self.assertEqual(state["project"]["approved_charter"], old["project"]["approved_charter"])
        self.start(task="T-002", attempt="A-002", code=1)

    def test_revised_charter_requires_restart_and_compatibility_review(self):
        self.start()
        self.reach("Build")
        self.reopen_and_approve()
        self.assertIsNotNone(self.state()["suspended_task"])
        self.assertIsNone(self.state()["active_task"])
        self.start(task="T-002", attempt="A-002", code=1)
        self.call("restart", "--attempt-id", "A-002", "--reason", "Review revised vision")
        self.assertEqual(self.state()["active_task"]["charter_revision"], 2)
        self.reach("Document")
        self.ready()
        self.move("Build", code=1)
        self.call("compatibility", "--evidence", "Synthetic owner-reviewed dispositions for earlier decisions")
        self.assertEqual(self.state()["current_stage"], "Document")
        self.move("Build")

    def test_abandon_suspended_task_after_reinitialisation(self):
        self.start()
        self.reopen_and_approve()
        self.call("abandon", "--reason", "No longer fits project")
        self.assertIsNone(self.state()["suspended_task"])
        self.assertIsNone(self.state()["active_task"])
        self.assertEqual(self.state()["current_stage"], "Guide")

    def test_ids_not_reused_and_empty_task_actions_fail(self):
        self.call("restart", "--attempt-id", "A-002", "--reason", "No task", code=1)
        self.call("abandon", "--reason", "No task", code=1)
        self.start()
        self.call("restart", "--attempt-id", "A-001", "--reason", "Reuse attempt", code=1)
        self.call("abandon", "--reason", "Stop")
        self.start(attempt="A-002", code=1)
        self.start(task="T-002", attempt="A-001", code=1)

    def test_missing_corrupt_conflicting_state_never_reconstructed(self):
        saved = self.path.read_bytes()
        self.path.unlink()
        self.call("status", code=1)
        self.assertFalse(self.path.exists())
        self.path.write_text("{broken JSON", encoding="utf-8")
        self.call("status", code=1)
        self.assertEqual(self.path.read_text(encoding="utf-8"), "{broken JSON")
        self.path.write_bytes(saved)
        state = self.state()
        state["current_stage"] = "Build"
        self.path.write_text(json.dumps(state), encoding="utf-8")
        self.call("status", code=1)

    def test_impossible_history_rejected_with_consistent_snapshot(self):
        self.start()
        self.reach("Learn")
        state = self.state()
        event = state["history"][-1]
        event["payload"]["to"] = event["to"] = "Build"
        event["owner_authorization"]["command"] = "Move to Build"
        state["current_stage"] = "Build"
        state["last_authorization"]["command"] = "Move to Build"
        self.path.write_text(json.dumps(state), encoding="utf-8")
        self.assertIn("Invalid historical transition", self.call("status", code=1).stderr)

    def test_overlapping_writes_and_empty_evidence_fail_unchanged(self):
        original = self.path.read_bytes()
        lock = self.path.with_suffix(".json.lock")
        lock.write_text("another writer", encoding="utf-8")
        self.call("ready", "--evidence", "fixture", code=1)
        self.assertEqual(lock.read_text(encoding="utf-8"), "another writer")
        self.assertEqual(original, self.path.read_bytes())
        lock.unlink()
        self.call("ready", "--evidence", " ", code=1)
        self.assertEqual(original, self.path.read_bytes())
        self.assertEqual(list(self.path.parent.glob(".workflow-state-*.tmp")), [])

class MigrationTests(TemporaryProject):
    def legacy_fixture(self, stage="NOT_STARTED", completed=False):
        state = legacy.initial_state()
        if stage != "NOT_STARTED":
            def operation(action, target=None):
                command = f"Move to {target}" if action == "move" else {"start": "Start Guide", "finish": "Finish cycle"}.get(action)
                legacy.change(state, argparse.Namespace(action=action, expected_revision=state["revision"],
                    owner_command=command, authorization_ref="synthetic-legacy-owner", cycle_id="legacy-001",
                    title="Existing task", to=target, evidence="Existing evidence"))
            operation("start")
            for target in STAGES[1:STAGES.index(stage) + 1]:
                operation("ready")
                operation("move", target)
            operation("ready")
            if completed:
                operation("finish")
        self.path.write_text(json.dumps(state), encoding="utf-8")
        return copy.deepcopy(state)

    def test_v1_status_not_migration_and_writes_require_explicit_upgrade(self):
        original = self.legacy_fixture()
        saved = self.path.read_bytes()
        self.assertEqual(json.loads(self.call("status").stdout), original)
        self.assertEqual(saved, self.path.read_bytes())
        self.call("initialise", code=1)
        self.call("migrate", command="continue", code=1)
        self.assertEqual(saved, self.path.read_bytes())

    def test_empty_v1_migrates_without_inventing_charter_approval(self):
        original = self.legacy_fixture()
        self.call("migrate")
        state = self.state()
        self.assertEqual(state["legacy_import"], original)
        self.assertEqual(state["history"][0]["payload"]["legacy_state"], original)
        self.assertEqual(state["project"]["status"], "UNINITIALIZED")
        self.assertEqual(state["current_stage"], "NOT_STARTED")
        self.start(code=1)
        self.call("migrate", code=1)

    def test_active_legacy_work_held_until_initialisation_and_review(self):
        original = self.legacy_fixture("Build")
        self.call("migrate")
        state = self.state()
        self.assertEqual(state["legacy_import"], original)
        self.assertEqual(state["suspended_task"]["stage"], "Build")
        self.assertEqual(state["suspended_task"]["evidence"], "Existing evidence")
        self.assertIsNone(state["active_task"])
        self.assertTrue(state["project"]["compatibility_review_required"])
        self.prepare_project()
        self.call("restart", "--attempt-id", "new-attempt", "--reason", "Review legacy task")
        self.reach("Document")
        self.ready()
        self.move("Build", code=1)

    def test_completed_legacy_cycle_keeps_original_history(self):
        original = self.legacy_fixture("Reflect", completed=True)
        self.call("migrate")
        state = self.state()
        self.assertEqual(state["legacy_import"]["history"], original["history"])
        self.assertEqual(state["attempts"][0]["disposition"], "LEGACY_COMPLETE")
        self.assertIsNone(state["suspended_task"])
        self.assertIsNone(state["project"]["approved_charter"])

    def test_corrupt_legacy_history_is_not_upgraded(self):
        state = self.legacy_fixture("Learn")
        state["current_stage"] = "Build"
        self.path.write_text(json.dumps(state), encoding="utf-8")
        saved = self.path.read_bytes()
        self.call("migrate", code=1)
        self.assertEqual(saved, self.path.read_bytes())

if __name__ == "__main__":
    unittest.main()
