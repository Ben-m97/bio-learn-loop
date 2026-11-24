#!/usr/bin/env python3
"""Schema-3 owner-controlled workflow with required conceptual Reflect evidence.

The JSON state is the stage authority, not conversation. A ready event never
advances a stage. Recorded owner references are provenance, not authentication.
Historical v1/v2 transitions retain their original rules in preserved engines.
The owner manages all Git staging and commits manually.
"""
from __future__ import annotations
import argparse
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

import _workflow_state_v1 as v1
import _workflow_state_v2 as v2
import _reflection_assessment as assessment

STAGES = v2.STAGES
STATE_PATH = v2.STATE_PATH
StateError = v2.StateError
OWNER_COMMANDS = {**v2.OWNER_COMMANDS, "reopen-reflection": "Reopen Reflect assessment"}


def initial_state():
    # Replay baseline only, never a fallback for missing on-disk state.
    return {**v2.initial_state(), "schema_version": 3, "reflection": None, "legacy_v2": None}


def authorize(value, command):
    if (not isinstance(value, dict) or set(value) != {"command", "reference"}
            or value["command"] != command):
        raise StateError(f"This operation requires the owner's explicit instruction: {command}")
    v2.nonempty(value["reference"], "Actual owner-message reference")


def custom_event(state, action, payload, authorization, before):
    state["revision"] += 1
    if authorization is not None:
        state["last_authorization"] = copy.deepcopy(authorization)
    state["history"].append({
        "revision": state["revision"], "at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "event": action, "from": before, "to": state["current_stage"], "status": state["stage_status"],
        "payload": copy.deepcopy(payload), "owner_authorization": copy.deepcopy(authorization),
    })


def apply(state, action, payload, authorization):
    if not isinstance(payload, dict):
        raise StateError("Event payload must be an object.")
    before = state["current_stage"]
    if action == "migrate":
        authorize(authorization, "Migrate workflow state")
        if state["revision"] != 0 or set(payload) != {"legacy_state", "migration_at_utc"}:
            raise StateError("Migration must be the first schema-3 event with an intact legacy snapshot.")
        v2.nonempty(payload["migration_at_utc"], "Recorded migration timestamp")
        old = copy.deepcopy(payload["legacy_state"])
        if old.get("schema_version") == 1:
            v1.validate_state(old)
            imported = v2.initial_state()
            v2.apply(imported, "migrate", {"legacy_state": old}, authorization)
            # The intermediate v1->v2 import is part of this recorded migration,
            # not a new wall-clock event whenever history is replayed.
            imported["history"][-1]["at_utc"] = payload["migration_at_utc"]
        elif old.get("schema_version") == 2:
            imported = v2.validate_state(old)
        else:
            raise StateError("Only schema 1/2 can migrate into schema 3.")
        state.update({key: copy.deepcopy(value) for key, value in imported.items()
                      if key not in {"schema_version", "revision", "history"}})
        state["legacy_v2"] = copy.deepcopy(imported)
        custom_event(state, action, payload, authorization, before)
        return
    if action == "reopen-reflection":
        authorize(authorization, "Reopen Reflect assessment")
        if set(payload) != {"reason"}:
            raise StateError("Reflection reopening needs its actual reason.")
        v2.nonempty(payload["reason"], "Reopen reason")
        v2.require_project(state)
        if before != "Reflect" or not state["active_task"] or state["stage_status"] not in {"ACTIVE", "READY"}:
            raise StateError("Reopen only the current Reflect assessment; do not restart or replace its task.")
        state.update(stage_status="ACTIVE", stage_evidence=None, reflection=None)
        custom_event(state, action, payload, authorization, before)
        return
    if action == "ready" and before == "Reflect":
        if authorization is not None or set(payload) != {"evidence", "assessment", "assessment_path"}:
            raise StateError("Reflect readiness requires a structured conceptual assessment, not free-text or an audit.")
        if not state["active_task"] or state["stage_status"] not in {"ACTIVE", "READY"}:
            raise StateError("No active Reflect assessment.")
        v2.nonempty(payload["evidence"], "Completion evidence")
        v2.nonempty(payload["assessment_path"], "Assessment artifact path")
        assessment.validate_snapshot(state, payload["assessment"])
        state["reflection"] = {"path": payload["assessment_path"],
                               "sha256": assessment.canonical_hash(payload["assessment"]),
                               "assessment": copy.deepcopy(payload["assessment"])}
        state.update(stage_status="READY", stage_evidence=payload["evidence"])
        custom_event(state, action, payload, None, before)
        return
    if action == "finish":
        receipt = state.get("reflection")
        if not receipt:
            raise StateError("Finish requires a current conceptual assessment receipt; legacy READY or audit success is insufficient.")
        assessment.validate_snapshot(state, receipt["assessment"])
    # Retain existing lifecycle semantics and comments in the v2 engine. Every
    # schema-3 event is still replayed through these exact public transition rules.
    v2.apply(state, action, payload, authorization)
    if action not in {"ready", "compatibility"}:
        state["reflection"] = None


def validate_state(state):
    if not isinstance(state, dict) or set(state) != set(initial_state()) or type(state["schema_version"]) is not int or state["schema_version"] != 3:
        raise StateError("Unsupported or malformed schema-3 state; migration is explicit.")
    if type(state["revision"]) is not int or not isinstance(state["history"], list) or state["revision"] != len(state["history"]):
        raise StateError("State revision and transition history disagree.")
    replayed = initial_state()
    fields = {"revision", "at_utc", "event", "from", "to", "status", "payload", "owner_authorization"}
    for index, event in enumerate(state["history"], 1):
        if not isinstance(event, dict) or set(event) != fields or type(event["revision"]) is not int or event["revision"] != index:
            raise StateError("Malformed or out-of-order transition history.")
        v2.nonempty(event["at_utc"], "Recorded event timestamp")
        try:
            apply(replayed, event["event"], event["payload"], event["owner_authorization"])
        except (ValueError, TypeError, KeyError, AttributeError) as error:
            raise StateError(f"Invalid historical transition at revision {index}: {error}") from error
        generated = replayed["history"][-1]
        if any(generated[key] != event[key] for key in fields - {"at_utc"}):
            raise StateError(f"Historical transition fields disagree at revision {index}.")
        replayed["history"][-1] = event
    if replayed != state:
        raise StateError("Current project/task/stage/assessment fields disagree with history.")
    return state


def load_state(path):
    try:
        state = json.loads(path.read_text(encoding="utf-8-sig"))
        if state.get("schema_version") in (1, 2):
            return v2.load_state(path)
        return validate_state(state)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        raise StateError(f"Cannot read state: {error}. Do not infer a stage from chat.") from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("status", help="read state without changing or migrating it")
    operations = {}
    for action in (*OWNER_COMMANDS, "ready", "move"):
        command = operations[action] = commands.add_parser(action)
        command.add_argument("--expected-revision", type=int, required=True)
        if action != "ready":
            command.add_argument("--owner-command", required=True)
            command.add_argument("--authorization-ref", required=True)
    operations["start"].add_argument("--task-id", required=True)
    operations["start"].add_argument("--attempt-id", "--cycle-id", dest="attempt_id", required=True)
    operations["start"].add_argument("--title", required=True)
    operations["restart"].add_argument("--attempt-id", required=True)
    for action in ("reopen-project", "restart", "abandon", "reopen-reflection"):
        operations[action].add_argument("--reason", required=True)
    for action in ("ready", "compatibility"):
        operations[action].add_argument("--evidence", required=True)
    operations["ready"].add_argument("--assessment", help="project-relative conceptual assessment JSON; required at Reflect")
    operations["move"].add_argument("--to", choices=("Initialise", *STAGES), required=True)
    args = parser.parse_args(argv)
    lock_fd = None
    lock_path = None
    try:
        root = args.root.resolve()
        path = root / STATE_PATH
        if not path.resolve().is_relative_to(root):
            raise StateError("State file must remain inside the project root.")
        if args.action == "status":
            state = load_state(path)
            if state["schema_version"] != 3:
                print("INFO legacy state is read-only until explicitly migrated to schema 3.", file=sys.stderr)
            elif state["current_stage"] == "Reflect" and state["stage_status"] == "READY":
                try:
                    assessment.validate_receipt(root, state)
                except (ValueError, OSError) as error:
                    print(f"WARN Reflect completion is BLOCKED: {error}", file=sys.stderr)
        else:
            if not path.is_file():
                raise StateError("State file is missing; restore it with the owner, never infer a stage from chat.")
            lock_path = path.with_suffix(".json.lock")
            try:
                lock_fd = v2.os.open(lock_path, v2.os.O_CREAT | v2.os.O_EXCL | v2.os.O_WRONLY)
            except FileExistsError as error:
                raise StateError("State is locked by another update; never automatically break the lock.") from error
            state = load_state(path)
            if args.expected_revision != state["revision"]:
                raise StateError(f"Stale revision: expected {args.expected_revision}, current is {state['revision']}.")
            authorization = None if args.action == "ready" else {"command": args.owner_command, "reference": args.authorization_ref}
            if state["schema_version"] in (1, 2):
                if args.action != "migrate":
                    raise StateError("Legacy state is read-only until explicitly migrated.")
                payload = {"legacy_state": copy.deepcopy(state),
                           "migration_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
                state = initial_state()
            else:
                if args.action == "migrate":
                    raise StateError("State is already schema 3.")
                payload = {key: getattr(args, key) for key in ("task_id", "attempt_id", "title", "reason", "evidence", "to") if hasattr(args, key)}
                if args.action == "approve-project":
                    payload = {"charter_text": v2.read_charter(root)}
                if args.action in {"start", "move", "restart", "abandon", "finish", "compatibility"}:
                    v2.require_current_charter(root, state)
                if args.action == "ready" and state["current_stage"] == "Reflect":
                    v2.require_current_charter(root, state)
                    if not args.assessment:
                        raise StateError("Reflect ready requires --assessment; a handoff, acknowledgement, or audit alone is insufficient.")
                    payload.update(assessment=assessment.load_assessment(root, args.assessment, state), assessment_path=args.assessment)
                if args.action == "finish":
                    assessment.validate_receipt(root, state)
            apply(state, args.action, payload, authorization)
            validate_state(state)
            v2.write_atomic(path, state)
        print(json.dumps(state, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, RuntimeError, TypeError, KeyError, AttributeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    finally:
        if lock_fd is not None:
            v2.os.close(lock_fd)
            lock_path.unlink(missing_ok=True)

if __name__ == "__main__":
    sys.exit(main())
