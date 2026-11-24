# Conceptual assessment record

Use one project-relative JSON file per attempt, preserving earlier completed records. This is an in-progress format example, not an executed or passed assessment:

```json
{
  "schema_version": 1,
  "task_id": "<actual task ID>",
  "attempt_id": "<actual attempt ID>",
  "charter_revision": 1,
  "bindings": {
    "docs/PROJECT.md": "<SHA-256 of actual file bytes>",
    "docs/PROJECT_BRIEF.md": "<SHA-256 of actual file bytes>",
    "scripts/example.py": "<SHA-256 of reviewed implementation>"
  },
  "candidate_files": ["scripts/example.py"],
  "concepts": [
    {
      "id": "C1",
      "goal": "<approved conceptual learning goal>",
      "criterion": "<what the owner should be able to explain or apply>",
      "status": "NOT_ASSESSED",
      "exchanges": [],
      "resolution": "Not yet assessed"
    }
  ],
  "unresolved_gaps": ["C1 not yet assessed"],
  "summary": "In progress; no demonstration inferred"
}
```

Each exchange has exactly these fields: question, owner_response, owner_message_ref, assessment, feedback, feedback_message_ref, gaps. Assessment is CORRECT, PARTIAL, or INCORRECT; gaps is a list of actual misconceptions/missing essential concepts. Feedback must have been delivered in chat. Message references may identify the real dated message/quotation; never fabricate IDs or responses.

A concept becomes DEMONSTRATED only after an actual adequate response. Its final exchange must be CORRECT with no gaps, and its resolution explains why the criterion was met. Earlier partial/incorrect exchanges stay in the record. After a correction, a distinct owner-message reference and follow-up response are required. The final unresolved_gaps list must be empty for readiness. Unasked concepts remain unassessed, not automatically incorrect or passed.

The bindings must include PROJECT.md, PROJECT_BRIEF.md, and the reviewed candidate files (at least one implementation file). Avoid mutable workflow state, assessment, handoff, and reflection-ledger files as bindings: recording the dialogue must not invalidate its own identity. If relevant learning goals, charter, or implementation changes, assess applicability again rather than blindly updating digests. Restart/backtracking/reopening invalidates the current readiness receipt; historical evidence remains in history.

At Reflect use the normal state helper ready operation with --assessment followed by this file's project-relative path, in addition to actual completion evidence and expected revision. Finish independently rechecks the receipt, artifact, and current bound files. No “passed” field or documentation audit can substitute for the owner dialogue.
