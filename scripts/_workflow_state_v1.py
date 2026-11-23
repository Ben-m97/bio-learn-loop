#!/usr/bin/env python3
"""Validate preserved version-1 snapshots for explicit migration only.

The JSON file, not the conversation, is the source of the current stage. A ready
event records completion evidence without advancing. Owner-command/reference
fields record authorization; this local helper cannot authenticate a chat speaker.
Codex must never invent those fields or call a transition without the actual
owner instruction. The owner manages all Git staging and commits manually.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path


STAGES = ("Guide", "Learn", "Choose", "Document", "Build", "Understand", "Reflect")
STATE_PATH = Path("docs/WORKFLOW_STATE.json")
REQUIRED = {
    "schema_version", "revision", "cycle_id", "step_title", "current_stage",
    "stage_status", "stage_evidence", "last_authorization", "history",
}


class StateError(ValueError):
    """Invalid persisted state or an unauthorized/inapplicable operation."""


def initial_state() -> dict:
    """Replay baseline only, never a fallback for a missing on-disk state."""
    return {
        "schema_version": 1, "revision": 0, "cycle_id": None, "step_title": None,
        "current_stage": "NOT_STARTED", "stage_status": "NOT_STARTED",
        "stage_evidence": None, "last_authorization": None, "history": [],
    }


def load_state(path: Path) -> dict:
    try:
        state = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, ValueError) as error:
        raise StateError(f"Cannot read {STATE_PATH.as_posix()}: {error}. Do not infer a stage from chat.") from error
    return validate_state(state)


def validate_state(state: dict) -> dict:
    """Validate original v1 history without altering or upgrading its meaning."""
    if not isinstance(state, dict) or set(state) != REQUIRED:
        raise StateError("State fields are missing or unexpected; restore the authoritative file with the owner.")
    if state["schema_version"] != 1 or type(state["schema_version"]) is not int:
        raise StateError("Unsupported state schema version.")
    if type(state["revision"]) is not int or state["revision"] < 0:
        raise StateError("State revision must be a nonnegative integer.")
    if not isinstance(state["history"], list) or len(state["history"]) != state["revision"]:
        raise StateError("State revision and transition history disagree.")
    if state["current_stage"] not in ("NOT_STARTED", *STAGES):
        raise StateError("Unknown current stage; do not infer a replacement.")
    if state["stage_status"] not in ("NOT_STARTED", "ACTIVE", "READY", "COMPLETE"):
        raise StateError("Unknown stage status.")
    if state["current_stage"] == "NOT_STARTED":
        if (state["revision"] != 0 or state["stage_status"] != "NOT_STARTED"
                or state["cycle_id"] is not None or state["step_title"] is not None
                or state["stage_evidence"] is not None or state["last_authorization"] is not None):
            raise StateError("NOT_STARTED state is inconsistent.")
    else:
        if not state["history"]:
            raise StateError("An active or completed stage needs its recorded transition history.")
        if any(not isinstance(state[key], str) or not state[key].strip() for key in ("cycle_id", "step_title")):
            raise StateError("An active or completed cycle needs its recorded ID and title.")
        if state["stage_status"] == "NOT_STARTED":
            raise StateError("A recorded stage cannot have NOT_STARTED status.")
        if state["stage_status"] == "COMPLETE" and state["current_stage"] != "Reflect":
            raise StateError("Only the final agent stage Reflect can complete a cycle.")
        if not isinstance(state["last_authorization"], dict):
            raise StateError("An active or completed cycle needs owner authorization provenance.")
    if state["stage_evidence"] is not None and not isinstance(state["stage_evidence"], str):
        raise StateError("Stage evidence must be text or null.")
    if state["stage_status"] in ("READY", "COMPLETE") and not state["stage_evidence"]:
        raise StateError("Ready/completed work needs recorded completion evidence.")
    # Replay the entire persisted history through the same transition rules.
    # A plausible final snapshot must not conceal an impossible earlier jump.
    replayed = initial_state()
    event_fields = {"revision", "at_utc", "event", "cycle_id", "step_title", "from", "to",
                    "status", "owner_authorization", "evidence"}
    for index, event in enumerate(state["history"], 1):
        if (not isinstance(event, dict) or set(event) != event_fields
                or type(event.get("revision")) is not int or event["revision"] != index):
            raise StateError("Transition history is malformed or out of order.")
        if not isinstance(event["at_utc"], str) or not event["at_utc"].strip():
            raise StateError("Transition history needs recorded event timestamps.")
        authorization = event["owner_authorization"]
        if event["event"] == "ready":
            if authorization is not None:
                raise StateError("Ready events must not authorize a stage transition.")
            authorization = {}
        elif (not isinstance(authorization, dict) or set(authorization) != {"command", "reference"}
              or not all(isinstance(value, str) for value in authorization.values())):
            raise StateError("A stage transition lacks explicit owner authorization provenance.")
        replay_args = argparse.Namespace(
            action=event["event"], expected_revision=index - 1,
            cycle_id=event["cycle_id"], title=event["step_title"], to=event["to"],
            evidence=event["evidence"], owner_command=authorization.get("command", ""),
            authorization_ref=authorization.get("reference", ""),
        )
        try:
            change(replayed, replay_args)
        except (StateError, TypeError, AttributeError, ValueError) as error:
            raise StateError(f"Invalid historical transition at revision {index}: {error}") from error
        generated = replayed["history"][-1]
        if any(generated[key] != event[key] for key in event_fields - {"at_utc"}):
            raise StateError(f"Historical transition fields disagree at revision {index}.")
        replayed["history"][-1] = event
    if any(replayed[key] != state[key] for key in REQUIRED - {"history"}):
        raise StateError("Current stage/status disagree with transition history; ask the owner to reconcile.")
    return state


def owner_authorization(args: argparse.Namespace, command: str) -> dict:
    if args.owner_command != command:
        raise StateError(f"This operation requires the owner's exact instruction: {command}")
    if not args.authorization_ref.strip():
        raise StateError("An actual owner-message reference is required; do not invent authorization.")
    return {"command": command, "reference": args.authorization_ref.strip()}


def change(state: dict, args: argparse.Namespace) -> dict:
    if args.expected_revision != state["revision"]:
        raise StateError(f"Stale revision: expected {args.expected_revision}, current is {state['revision']}. Re-read state.")
    before = state["current_stage"]
    authorization = None
    if args.action == "start":
        authorization = owner_authorization(args, "Start Guide")
        if state["stage_status"] not in ("NOT_STARTED", "COMPLETE"):
            raise StateError("A cycle is already active; do not silently start another.")
        if not args.cycle_id.strip() or not args.title.strip():
            raise StateError("Starting a cycle requires a nonempty ID and step title.")
        if any(event.get("cycle_id") == args.cycle_id for event in state["history"]):
            raise StateError("Cycle IDs must not be reused.")
        state.update(cycle_id=args.cycle_id, step_title=args.title,
                     current_stage="Guide", stage_status="ACTIVE", stage_evidence=None)
    elif args.action == "ready":
        if state["stage_status"] not in ("ACTIVE", "READY"):
            raise StateError("Only an active stage can be marked ready.")
        if not args.evidence.strip():
            raise StateError("Record what was completed and its actual evidence before marking ready.")
        state.update(stage_status="READY", stage_evidence=args.evidence.strip())
    elif args.action == "move":
        authorization = owner_authorization(args, f"Move to {args.to}")
        if state["stage_status"] not in ("ACTIVE", "READY") or before not in STAGES:
            raise StateError("There is no active cycle to move.")
        current, target = STAGES.index(before), STAGES.index(args.to)
        if target == current:
            raise StateError("Already at that stage; no transition is needed.")
        if target > current:
            if target != current + 1:
                raise StateError("Forward transitions cannot skip stages.")
            if state["stage_status"] != "READY":
                raise StateError("Current work must be ready before a forward transition; readiness never authorizes the move.")
        state.update(current_stage=args.to, stage_status="ACTIVE", stage_evidence=None)
    elif args.action == "finish":
        authorization = owner_authorization(args, "Finish cycle")
        if before != "Reflect" or state["stage_status"] != "READY":
            raise StateError("Finish only after Reflect is ready and the owner accepts the handoff.")
        state["stage_status"] = "COMPLETE"
    else:
        raise StateError("Unknown state operation.")
    state["revision"] += 1
    if authorization is not None:
        state["last_authorization"] = authorization
    state["history"].append({
        "revision": state["revision"],
        "at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "event": args.action,
        "cycle_id": state["cycle_id"],
        "step_title": state["step_title"],
        "from": before,
        "to": state["current_stage"],
        "status": state["stage_status"],
        "owner_authorization": authorization,
        "evidence": state["stage_evidence"],
    })
    return state


