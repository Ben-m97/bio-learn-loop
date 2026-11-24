"""Mechanical assessment evidence checks, not semantic grading or authentication."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PureWindowsPath
import re


class AssessmentError(ValueError):
    pass


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise AssessmentError(f"{label} needs actual nonempty text.")


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def safe_path(root: Path, name: str) -> Path:
    text(name, "Evidence path")
    if Path(name).is_absolute() or PureWindowsPath(name).drive:
        raise AssessmentError("Assessment evidence paths must be project-relative.")
    path = (root / name.replace("\\", "/")).resolve()
    if not path.is_relative_to(root.resolve()):
        raise AssessmentError("Assessment evidence must remain inside the project.")
    return path


def validate_snapshot(state, assessment):
    required = {"schema_version", "task_id", "attempt_id", "charter_revision", "bindings",
                "candidate_files", "concepts", "unresolved_gaps", "summary"}
    if not isinstance(assessment, dict) or set(assessment) != required:
        raise AssessmentError("Assessment fields are missing or unexpected.")
    if type(assessment["schema_version"]) is not int or assessment["schema_version"] != 1:
        raise AssessmentError("Unsupported assessment schema.")
    task = state["active_task"]
    if not task or any(assessment[key] != task[key] for key in ("task_id", "attempt_id", "charter_revision")):
        raise AssessmentError("Assessment belongs to a different task, attempt, or charter revision.")
    if type(assessment["charter_revision"]) is not int:
        raise AssessmentError("Assessment charter revision must be an integer.")
    if assessment["unresolved_gaps"] != []:
        raise AssessmentError("Reflect remains incomplete while conceptual gaps remain unresolved.")
    text(assessment["summary"], "Assessment summary")
    bindings = assessment["bindings"]
    if not isinstance(bindings, dict) or not {"docs/PROJECT.md", "docs/PROJECT_BRIEF.md"} <= set(bindings):
        raise AssessmentError("Bind the approved charter and actual task learning goals.")
    candidates = assessment["candidate_files"]
    if (not isinstance(candidates, list) or not candidates
            or any(not isinstance(name, str) or name not in bindings for name in candidates)
            or set(candidates) <= {"docs/PROJECT.md", "docs/PROJECT_BRIEF.md"}):
        raise AssessmentError("Bind at least one reviewed implementation file.")
    for name, checksum in bindings.items():
        text(name, "Binding path")
        if not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-f]{64}", checksum):
            raise AssessmentError("Every binding needs a SHA-256 digest.")
    concepts = assessment["concepts"]
    if not isinstance(concepts, list) or not concepts:
        raise AssessmentError("Record the essential concepts derived from this task's learning goals.")
    identifiers = set()
    for concept in concepts:
        if not isinstance(concept, dict) or set(concept) != {"id", "goal", "criterion", "status", "exchanges", "resolution"}:
            raise AssessmentError("Each concept needs a goal, criterion, dialogue, and disposition.")
        for key in ("id", "goal", "criterion", "resolution"):
            text(concept[key], f"Concept {key}")
        if concept["id"] in identifiers:
            raise AssessmentError("Concept IDs must be unique.")
        identifiers.add(concept["id"])
        if concept["status"] != "DEMONSTRATED":
            raise AssessmentError("Every essential concept must be demonstrated, not merely explained by the agent.")
        exchanges = concept["exchanges"]
        if not isinstance(exchanges, list) or not exchanges:
            raise AssessmentError("A concept needs actual owner responses and chat feedback.")
        seen_refs = set()
        for exchange in exchanges:
            fields = {"question", "owner_response", "owner_message_ref", "assessment", "feedback",
                      "feedback_message_ref", "gaps"}
            if not isinstance(exchange, dict) or set(exchange) != fields:
                raise AssessmentError("Each exchange needs the actual question/answer, chat feedback, references, and gaps.")
            for key in fields - {"gaps"}:
                text(exchange[key], f"Exchange {key}")
            if exchange["assessment"] not in ("CORRECT", "PARTIAL", "INCORRECT"):
                raise AssessmentError("Unknown answer assessment.")
            if exchange["owner_message_ref"] in seen_refs:
                raise AssessmentError("A correction needs a new owner response, not reuse of the original answer.")
            seen_refs.add(exchange["owner_message_ref"])
            if not isinstance(exchange["gaps"], list) or any(not isinstance(gap, str) or not gap.strip() for gap in exchange["gaps"]):
                raise AssessmentError("Exchange gaps must be explicit text entries.")
            if exchange["assessment"] == "CORRECT" and exchange["gaps"]:
                raise AssessmentError("A correct answer cannot have unresolved gaps.")
            if exchange["assessment"] != "CORRECT" and not exchange["gaps"]:
                raise AssessmentError("Identify the misconception or important missing concept explicitly.")
        if exchanges[-1]["assessment"] != "CORRECT" or exchanges[-1]["gaps"]:
            raise AssessmentError("Agent corrections require a follow-up demonstrating the corrected concept.")
    return assessment


def validate_files(root, assessment):
    for name, checksum in assessment["bindings"].items():
        path = safe_path(root, name)
        if hashlib.sha256(path.read_bytes()).hexdigest() != checksum:
            raise AssessmentError(f"Assessment is stale: {name} changed. Review applicability; do not simply rehash to force a pass.")


def load_assessment(root, name, state):
    assessment = json.loads(safe_path(root, name).read_text(encoding="utf-8-sig"))
    validate_snapshot(state, assessment)
    validate_files(root, assessment)
    return assessment


def validate_receipt(root, state):
    receipt = state.get("reflection")
    if not isinstance(receipt, dict) or set(receipt) != {"path", "sha256", "assessment"}:
        raise AssessmentError("Reflect has no qualifying conceptual assessment receipt; legacy READY/audit evidence cannot close it.")
    validate_snapshot(state, receipt["assessment"])
    current = load_assessment(root, receipt["path"], state)
    if canonical_hash(current) != receipt["sha256"] or current != receipt["assessment"]:
        raise AssessmentError("Assessment artifact no longer matches its recorded receipt.")
