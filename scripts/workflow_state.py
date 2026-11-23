#!/usr/bin/env python3
"""Record project initialization and explicitly owner-authorized task transitions.

The JSON file, not the conversation, is the source of the current stage. A ready
event records completion evidence without advancing. Owner-command/reference
fields record authorization; this local helper cannot authenticate a chat speaker.
Codex must never invent those fields or call a transition without the actual
owner instruction. The owner manages all Git staging and commits manually.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

import _workflow_state_v1 as legacy


STAGES = ("Guide", "Learn", "Choose", "Document", "Build", "Understand", "Reflect")
STATE_PATH = Path("docs/WORKFLOW_STATE.json")
CHARTER_PATH = Path("docs/PROJECT.md")
OWNER_COMMANDS = {
    "initialise": "Start Initialise", "approve-project": "Approve project description",
    "reopen-project": "Reopen Initialise", "start": "Start Guide",
    "restart": "Restart task", "abandon": "Abandon task", "finish": "Finish cycle",
    "compatibility": "Approve compatibility review", "migrate": "Migrate workflow state",
}


class StateError(ValueError):
    """Invalid persisted state or an unauthorized/inapplicable operation."""


def initial_state() -> dict:
    """Replay baseline only, never a fallback for a missing on-disk state."""
    return {
        "schema_version": 2, "revision": 0,
        "project": {
            "status": "UNINITIALIZED", "charter_revision": 0, "approved_charter": None,
            "compatibility_review_required": False, "compatibility_review": None,
        },
        "current_stage": "NOT_STARTED", "stage_status": "NOT_STARTED", "stage_evidence": None,
        "active_task": None, "suspended_task": None, "attempts": [],
        "legacy_import": None, "last_authorization": None, "history": [],
    }


def nonempty(value, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StateError(f"{label} must be nonempty text.")
    return value.strip()


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def require_project(state: dict) -> None:
    if state["project"]["status"] != "APPROVED":
        raise StateError("Initialise and explicit charter approval are required before task work.")


def checkpoint(state: dict) -> dict:
    return {"task": copy.deepcopy(state["active_task"]), "stage": state["current_stage"],
            "status": state["stage_status"], "evidence": state["stage_evidence"]}


def archive(state: dict, saved: dict, disposition: str, reason: str) -> None:
    state["attempts"].append({**copy.deepcopy(saved), "disposition": disposition,
                              "reason": reason, "at_revision": state["revision"] + 1})


def guide(state: dict) -> None:
    state.update(current_stage="Guide", stage_status="ACTIVE", stage_evidence=None)


def unique_attempt(state: dict, attempt_id: str) -> None:
    tasks = [item["task"] for item in state["attempts"]]
    tasks += [state["active_task"]]
    if state["suspended_task"]:
        tasks.append(state["suspended_task"]["task"])
    if any(task and task["attempt_id"] == attempt_id for task in tasks):
        raise StateError("Attempt IDs must not be reused.")


def apply(state: dict, action: str, payload: dict, authorization: dict | None) -> None:
    """Apply one event in memory; the same rules validate every historical event."""
    if not isinstance(payload, dict):
        raise StateError("Event payload must be an object.")
    required_payload = {
        "initialise": set(), "approve-project": {"charter_text"}, "reopen-project": {"reason"},
        "start": {"task_id", "attempt_id", "title"}, "ready": {"evidence"}, "move": {"to"},
        "restart": {"attempt_id", "reason"}, "abandon": {"reason"}, "finish": set(),
        "compatibility": {"evidence"}, "migrate": {"legacy_state"},
    }
    if action not in required_payload or set(payload) != required_payload[action]:
        raise StateError("Unknown operation or invalid event payload fields.")
    expected_command = f"Move to {payload['to']}" if action == "move" else OWNER_COMMANDS.get(action)
    if action == "ready":
        if authorization is not None:
            raise StateError("Ready events cannot authorize a stage transition.")
    elif (not isinstance(authorization, dict) or set(authorization) != {"command", "reference"}
          or authorization["command"] != expected_command):
        raise StateError(f"This operation requires the owner's exact instruction: {expected_command}")
    else:
        nonempty(authorization["reference"], "Actual owner-message reference")

    before = state["current_stage"]
    project = state["project"]
    if action == "migrate":
        if state["revision"] != 0:
            raise StateError("Migration must be the first version-2 event.")
        original = copy.deepcopy(payload["legacy_state"])
        try:
            legacy.validate_state(original)
        except (ValueError, TypeError, KeyError, AttributeError) as error:
            raise StateError(f"Invalid legacy state: {error}") from error
        state["legacy_import"] = original
        # Preserve the original history intact; derived checkpoints remain clearly
        # legacy records and never imply an approved project charter.
        for event in original["history"]:
            if event["event"] == "finish":
                task = {"task_id": f"legacy:{event['cycle_id']}", "title": event["step_title"],
                        "attempt_id": event["cycle_id"], "attempt_number": 1, "charter_revision": None}
                archive(state, {"task": task, "stage": "Reflect", "status": "COMPLETE",
                                "evidence": event["evidence"]}, "LEGACY_COMPLETE", "Imported v1 completed cycle")
        if original["stage_status"] in ("ACTIVE", "READY"):
            task = {"task_id": f"legacy:{original['cycle_id']}", "title": original["step_title"],
                    "attempt_id": original["cycle_id"], "attempt_number": 1, "charter_revision": None}
            state["suspended_task"] = {"task": task, "stage": original["current_stage"],
                                       "status": original["stage_status"], "evidence": original["stage_evidence"]}
        project["compatibility_review_required"] = bool(original["history"])
    elif action == "initialise":
        if project["status"] != "UNINITIALIZED" or before != "NOT_STARTED":
            raise StateError("Initialise runs once; use an explicit Reopen Initialise for an existing project.")
        project.update(status="INITIALISING", charter_revision=1)
        state.update(current_stage="Initialise", stage_status="ACTIVE", stage_evidence=None)
    elif action == "approve-project":
        if before != "Initialise" or project["status"] != "INITIALISING":
            raise StateError("Approve the charter only during Initialise.")
        text = payload["charter_text"]
        nonempty(text, "Project description")
        if re.search(r"\*\*(?:Template|Status):\*\*\s*UNCONFIGURED\b", text, re.I):
            raise StateError("Replace the unconfigured charter prompts with the owner's description first.")
        project.update(status="APPROVED", approved_charter={
            "revision": project["charter_revision"], "text": text,
            "sha256": digest(text), "authorization": copy.deepcopy(authorization),
        })
        state.update(stage_status="READY", stage_evidence="Owner approved this project description; no architecture or task work is authorized.")
    elif action == "reopen-project":
        require_project(state)
        nonempty(payload["reason"], "Reopen reason")
        if state["active_task"]:
            state["suspended_task"] = checkpoint(state)
            state["active_task"] = None
        project.update(status="INITIALISING", charter_revision=project["charter_revision"] + 1,
                       compatibility_review_required=True, compatibility_review=None)
        state.update(current_stage="Initialise", stage_status="ACTIVE", stage_evidence=None)
    elif action == "start":
        require_project(state)
        if before != "Guide" or state["active_task"] or state["suspended_task"]:
            raise StateError("Start a new task only at Guide with no active or suspended task.")
        task_id = nonempty(payload["task_id"], "Task ID")
        attempt_id = nonempty(payload["attempt_id"], "Attempt ID")
        title = nonempty(payload["title"], "Task title")
        if any(item["task"]["task_id"] == task_id for item in state["attempts"]):
            raise StateError("Task IDs must not be reused; restart preserves the existing task instead.")
        unique_attempt(state, attempt_id)
        state["active_task"] = {"task_id": task_id, "title": title, "attempt_id": attempt_id,
                                "attempt_number": 1, "charter_revision": project["charter_revision"]}
        guide(state)
    elif action == "ready":
        if state["stage_status"] not in ("ACTIVE", "READY"):
            raise StateError("Only an active stage can be marked ready.")
        state.update(stage_status="READY", stage_evidence=nonempty(payload["evidence"], "Completion evidence"))
    elif action == "move":
        target = payload["to"]
        if target not in STAGES:
            raise StateError("Use explicit Initialise/reopen operations for Stage 0.")
        if before == "Initialise":
            require_project(state)
            if target != "Guide" or state["stage_status"] != "READY":
                raise StateError("Leave approved Initialise only for Guide, with a separate explicit transition.")
        else:
            require_project(state)
            if before not in STAGES or not state["active_task"]:
                raise StateError("Select a task at Guide before progressing through development stages.")
            current, destination = STAGES.index(before), STAGES.index(target)
            if destination == current:
                raise StateError("Already at that stage; no transition is needed.")
            if destination > current:
                if destination != current + 1:
                    raise StateError("Forward transitions cannot skip stages.")
                if state["stage_status"] != "READY":
                    raise StateError("Current work must be ready; readiness never authorizes the move.")
            if target == "Build" and project["compatibility_review_required"]:
                raise StateError("Owner-approved compatibility review is required before Build under the revised charter.")
        state.update(current_stage=target, stage_status="ACTIVE", stage_evidence=None)
    elif action in ("restart", "abandon"):
        require_project(state)
        if before == "Initialise":
            raise StateError("Approve the project and move to Guide before resolving suspended work.")
        saved = checkpoint(state) if state["active_task"] else copy.deepcopy(state["suspended_task"])
        if not saved:
            raise StateError("No active or suspended task to restart or abandon.")
        reason = nonempty(payload["reason"], "Task disposition reason")
        if action == "restart":
            attempt_id = nonempty(payload["attempt_id"], "New attempt ID")
            unique_attempt(state, attempt_id)
            archive(state, saved, "RESTARTED", reason)
            state["active_task"] = {**saved["task"], "attempt_id": attempt_id,
                                    "attempt_number": saved["task"]["attempt_number"] + 1,
                                    "charter_revision": project["charter_revision"]}
        else:
            archive(state, saved, "ABANDONED", reason)
            state["active_task"] = None
        state["suspended_task"] = None
        guide(state)
    elif action == "finish":
        require_project(state)
        if before != "Reflect" or state["stage_status"] != "READY" or not state["active_task"]:
            raise StateError("Finish only after Reflect is ready and the owner accepts the handoff.")
        archive(state, checkpoint(state), "COMPLETE", "Owner accepted the manual-commit handoff")
        state["active_task"] = None
        guide(state)
    elif action == "compatibility":
        require_project(state)
        if before not in STAGES[:4] or not project["compatibility_review_required"]:
            raise StateError("Record pending compatibility review in Guide, Learn, Choose, or Document.")
        project.update(compatibility_review_required=False, compatibility_review={
            "charter_revision": project["charter_revision"],
            "evidence": nonempty(payload["evidence"], "Compatibility dispositions/evidence"),
            "authorization": copy.deepcopy(authorization),
        })
    state["revision"] += 1
    if authorization is not None:
        state["last_authorization"] = copy.deepcopy(authorization)
    state["history"].append({
        "revision": state["revision"], "at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "event": action, "from": before, "to": state["current_stage"], "status": state["stage_status"],
        "payload": copy.deepcopy(payload), "owner_authorization": copy.deepcopy(authorization),
    })


def validate_state(state: dict) -> dict:
    if not isinstance(state, dict) or set(state) != set(initial_state()):
        raise StateError("State fields are missing or unexpected; restore the authoritative file with the owner.")
    if type(state["schema_version"]) is not int or state["schema_version"] != 2:
        raise StateError("Unsupported state schema version; migration is explicit.")
    if type(state["revision"]) is not int or not isinstance(state["history"], list) or state["revision"] != len(state["history"]):
        raise StateError("State revision and transition history disagree.")
    # Replay the entire persisted history through the same transition rules.
    # A plausible final snapshot must not conceal an impossible earlier jump.
    replayed = initial_state()
    fields = {"revision", "at_utc", "event", "from", "to", "status", "payload", "owner_authorization"}
    for index, event in enumerate(state["history"], 1):
        if not isinstance(event, dict) or set(event) != fields or type(event["revision"]) is not int or event["revision"] != index:
            raise StateError("Transition history is malformed or out of order.")
        nonempty(event["at_utc"], "Recorded event timestamp")
        try:
            apply(replayed, event["event"], event["payload"], event["owner_authorization"])
        except (ValueError, KeyError, TypeError, AttributeError) as error:
            raise StateError(f"Invalid historical transition at revision {index}: {error}") from error
        generated = replayed["history"][-1]
        if any(generated[key] != event[key] for key in fields - {"at_utc"}):
            raise StateError(f"Historical transition fields disagree at revision {index}.")
        replayed["history"][-1] = event
    if replayed != state:
        raise StateError("Current project/task/stage fields disagree with transition history; ask the owner to reconcile.")
    return state


def load_state(path: Path) -> dict:
    try:
        state = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(state, dict) and state.get("schema_version") == 1:
            return legacy.validate_state(state)
        return validate_state(state)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        raise StateError(f"Cannot read {STATE_PATH.as_posix()}: {error}. Do not infer a stage from chat.") from error


def read_charter(root: Path) -> str:
    path = root / CHARTER_PATH
    if not path.resolve().is_relative_to(root):
        raise StateError("Charter must remain inside the project root.")
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        raise StateError(f"Cannot read project charter: {error}") from error


def require_current_charter(root: Path, state: dict) -> None:
    require_project(state)
    if digest(read_charter(root)) != state["project"]["approved_charter"]["sha256"]:
        raise StateError("Charter differs from the approved description. Restore it or explicitly reopen Initialise; do not infer approval.")


def write_atomic(path: Path, state: dict) -> None:
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=path.parent,
                                         prefix=".workflow-state-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(state, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root; default current directory")
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("status", help="read state without migrating or changing it")
    operations = {}
    for action in ("initialise", "approve-project", "reopen-project", "start", "ready", "move",
                   "restart", "abandon", "finish", "compatibility", "migrate"):
        command = operations[action] = commands.add_parser(action)
        command.add_argument("--expected-revision", type=int, required=True)
        if action != "ready":
            command.add_argument("--owner-command", required=True)
            command.add_argument("--authorization-ref", required=True)
    operations["start"].add_argument("--task-id", required=True)
    operations["start"].add_argument("--attempt-id", "--cycle-id", dest="attempt_id", required=True)
    operations["start"].add_argument("--title", required=True)
    operations["restart"].add_argument("--attempt-id", required=True)
    for action in ("reopen-project", "restart", "abandon"):
        operations[action].add_argument("--reason", required=True)
    for action in ("ready", "compatibility"):
        operations[action].add_argument("--evidence", required=True)
    operations["move"].add_argument("--to", choices=("Initialise", *STAGES), required=True)
    args = parser.parse_args(argv)
    lock_path = None
    lock_fd = None
    try:
        root = args.root.resolve()
        path = root / STATE_PATH
        if not path.resolve().is_relative_to(root):
            raise StateError("State file must remain inside the project root.")
        if args.action == "status":
            state = load_state(path)
            if state["schema_version"] == 1:
                print("INFO schema 1 requires explicit migration; no charter approval has been inferred.", file=sys.stderr)
        else:
            if not path.is_file():
                raise StateError("State file is missing; restore it with the owner, never infer a stage from chat.")
            lock_path = path.with_suffix(".json.lock")
            try:
                lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError as error:
                raise StateError("State is locked by another update; do not overwrite or automatically break the lock.") from error
            state = load_state(path)
            if args.expected_revision != state["revision"]:
                raise StateError(f"Stale revision: expected {args.expected_revision}, current is {state['revision']}. Re-read state.")
            authorization = None if args.action == "ready" else {
                "command": args.owner_command, "reference": args.authorization_ref,
            }
            if state["schema_version"] == 1:
                if args.action != "migrate":
                    raise StateError("Version 1 is read-only until an explicitly authorized migrate operation.")
                payload = {"legacy_state": copy.deepcopy(state)}
                state = initial_state()
            else:
                if args.action == "migrate":
                    raise StateError("State is already version 2.")
                payload = {}
                for key in ("task_id", "attempt_id", "title", "reason", "evidence", "to"):
                    if hasattr(args, key):
                        payload[key] = getattr(args, key)
                if args.action == "approve-project":
                    payload = {"charter_text": read_charter(root)}
                if args.action in ("start", "move", "restart", "abandon", "finish", "compatibility"):
                    require_current_charter(root, state)
            apply(state, args.action, payload, authorization)
            validate_state(state)
            write_atomic(path, state)
        print(json.dumps(state, indent=2, ensure_ascii=False))
        return 0
    except (StateError, OSError, RuntimeError, ValueError, TypeError, KeyError, AttributeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    finally:
        if lock_fd is not None:
            os.close(lock_fd)
            if lock_path is not None:
                lock_path.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
