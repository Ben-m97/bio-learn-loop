"""Conceptual gate mechanics with explicitly synthetic dialogue and candidates."""
import copy
import json
import unittest
from test_workflow_state import TemporaryProject, CHARTER, STAGES, engine
import _workflow_state_v2 as v2


class ReflectionTests(TemporaryProject):
    def setUp(self):
        super().setUp()
        state = engine.initial_state()
        def event(action, payload, command=None):
            auth = None if action == "ready" else {"command": command or engine.OWNER_COMMANDS[action], "reference": "synthetic-setup"}
            engine.apply(state, action, payload, auth)
        event("initialise", {})
        event("approve-project", {"charter_text": CHARTER})
        event("move", {"to": "Guide"}, "Move to Guide")
        event("start", {"task_id": "T-001", "attempt_id": "A-001", "title": "Synthetic conceptual task"})
        for stage in STAGES[1:]:
            event("ready", {"evidence": "Synthetic earlier-stage evidence"})
            event("move", {"to": stage}, f"Move to {stage}")
        self.path.write_text(json.dumps(state), encoding="utf-8")
        self.name = self.make_assessment()
        self.record_path = self.root / self.name

    def record(self):
        return json.loads(self.record_path.read_text(encoding="utf-8"))

    def save(self, record):
        self.record_path.write_text(json.dumps(record), encoding="utf-8")

    def assess_ready(self, code=0):
        return self.call("ready", "--evidence", "Synthetic chat-based assessment", "--assessment", self.name, code=code)

    def test_free_text_or_clean_audit_cannot_mark_reflect_ready(self):
        original = self.path.read_bytes()
        self.call("ready", "--evidence", "Audit passed with zero warnings; owner says understands", code=1)
        self.assertEqual(original, self.path.read_bytes())
        self.assertEqual(self.state()["stage_status"], "ACTIVE")

    def test_absent_assessment_artifact_fails(self):
        self.record_path.unlink()
        self.assess_ready(code=1)

    def test_partial_or_unassessed_concepts_cannot_pass(self):
        original = self.record()
        for status in ("PARTIAL", "NOT_ASSESSED"):
            record = copy.deepcopy(original)
            record["concepts"][0]["status"] = status
            self.save(record)
            self.assess_ready(code=1)

    def test_actual_owner_answer_and_chat_feedback_references_required(self):
        original = self.record()
        for key in ("owner_response", "owner_message_ref", "feedback", "feedback_message_ref"):
            record = copy.deepcopy(original)
            record["concepts"][0]["exchanges"][0][key] = ""
            self.save(record)
            self.assess_ready(code=1)

    def test_agent_correction_alone_is_insufficient_but_follow_up_can_pass(self):
        record = self.record()
        exchange = record["concepts"][0]["exchanges"][0]
        correct = copy.deepcopy(exchange)
        exchange.update(assessment="PARTIAL", owner_response="Acceptance means the data are good.",
                        feedback="It establishes structure, not scientific quality. Explain that distinction.",
                        gaps=["Conflates structural acceptance with scientific quality"])
        self.save(record)
        self.assess_ready(code=1)
        correct.update(question="Could structurally accepted data still be unsuitable for analysis?",
                       owner_message_ref="synthetic-owner-follow-up", feedback_message_ref="synthetic-feedback-follow-up")
        record["concepts"][0]["exchanges"].append(correct)
        self.save(record)
        self.assess_ready()
        self.assertEqual(self.state()["stage_status"], "READY")

    def test_reusing_the_original_owner_message_after_a_correction_fails(self):
        record = self.record()
        correct = copy.deepcopy(record["concepts"][0]["exchanges"][0])
        record["concepts"][0]["exchanges"][0].update(assessment="INCORRECT", gaps=["Missing core distinction"])
        record["concepts"][0]["exchanges"].append(correct)
        self.save(record)
        self.assess_ready(code=1)

    def test_global_unresolved_gaps_prevent_readiness(self):
        record = self.record()
        record["unresolved_gaps"] = ["An essential concept has not been asked about"]
        self.save(record)
        self.assess_ready(code=1)

    def test_wrong_task_attempt_or_charter_revision_fails(self):
        original = self.record()
        for key, value in (("task_id", "other"), ("attempt_id", "other"), ("charter_revision", 9)):
            record = copy.deepcopy(original)
            record[key] = value
            self.save(record)
            self.assess_ready(code=1)

    def test_changed_learning_goals_prevent_readiness(self):
        (self.root / "docs/PROJECT_BRIEF.md").write_text("Different conceptual scope", encoding="utf-8")
        self.assess_ready(code=1)

    def test_rebinding_an_unapproved_charter_cannot_authorize_readiness(self):
        import hashlib
        charter = self.root / "docs/PROJECT.md"
        charter.write_text("Changed without owner approval", encoding="utf-8")
        record = self.record()
        record["bindings"]["docs/PROJECT.md"] = hashlib.sha256(charter.read_bytes()).hexdigest()
        self.save(record)
        self.assess_ready(code=1)
        self.assertEqual(self.state()["stage_status"], "ACTIVE")

    def test_changed_candidate_prevents_finish_even_after_readiness(self):
        self.assess_ready()
        (self.root / "scripts/candidate.py").write_text("changed = True", encoding="utf-8")
        self.call("finish", code=1)
        self.assertEqual(self.state()["current_stage"], "Reflect")

    def test_modified_assessment_receipt_prevents_finish(self):
        self.assess_ready()
        record = self.record()
        record["summary"] = "Modified after readiness"
        self.save(record)
        self.call("finish", code=1)

    def test_valid_dialogue_allows_ready_then_explicit_finish(self):
        self.assess_ready()
        self.assertEqual(self.state()["current_stage"], "Reflect")
        self.call("finish", command="continue", code=1)
        self.call("finish")
        self.assertEqual(self.state()["current_stage"], "Guide")
        self.assertIsNone(self.state()["active_task"])
        self.assertIsNone(self.state()["reflection"])

    def test_backtracking_invalidates_current_readiness_receipt(self):
        self.assess_ready()
        self.move("Understand")
        self.assertIsNone(self.state()["reflection"])
        self.ready()
        self.move("Reflect")
        self.call("finish", code=1)

    def legacy_ready(self, complete=False):
        state = {key: copy.deepcopy(self.state()[key]) for key in v2.initial_state()}
        state["schema_version"] = 2
        v2.apply(state, "ready", {"evidence": "Historical audit and self-report"}, None)
        if complete:
            v2.apply(state, "finish", {}, {"command": "Finish cycle", "reference": "synthetic-historical-owner"})
        v2.validate_state(state)
        self.path.write_text(json.dumps(state), encoding="utf-8")
        return copy.deepcopy(state)

    def test_migration_keeps_legacy_ready_but_blocks_finish_until_assessed(self):
        original = self.legacy_ready()
        self.call("migrate")
        self.assertEqual(self.state()["legacy_v2"], original)
        self.assertEqual(self.state()["stage_status"], "READY")
        self.call("finish", code=1)
        self.assertEqual(self.state()["stage_status"], "READY")

    def test_explicit_reopen_keeps_task_attempt_and_prior_evidence(self):
        old = self.legacy_ready()
        self.call("migrate")
        self.call("reopen-reflection", "--reason", "Owner requests conceptual assessment", command="continue", code=1)
        self.call("reopen-reflection", "--reason", "Owner requests conceptual assessment")
        state = self.state()
        self.assertEqual(state["stage_status"], "ACTIVE")
        self.assertEqual(state["current_stage"], "Reflect")
        self.assertEqual(state["active_task"], old["active_task"])
        self.assertEqual(state["legacy_v2"]["history"], old["history"])

    def test_historical_completed_cycles_are_not_rewritten_as_new_assessments(self):
        old = self.legacy_ready(complete=True)
        self.call("migrate")
        self.assertEqual(self.state()["legacy_v2"], old)
        self.assertEqual(self.state()["attempts"], old["attempts"])
        self.assertIsNone(self.state()["reflection"])

    def test_assessment_path_must_be_inside_the_project(self):
        self.call("ready", "--evidence", "fixture", "--assessment", "../outside.json", code=1)


if __name__ == "__main__":
    unittest.main()
