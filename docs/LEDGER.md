# Ledger

**Status:** UNCONFIGURED — no pipeline version is approved or in progress.

Release rules are in `RELEASE_PROCESS.md`. This is the open list of findings and the approved current scope. New ideas go to the backlog only after the owner approves keeping them.

Project initialization, charter revision, active/suspended task, attempt, and stage are recorded only in `WORKFLOW_STATE.json`. Link to that record; do not maintain a second current-stage field. The charter in PROJECT.md supplies purpose; this ledger records selected work and outcomes. Charter approval and scope/design/fix approvals are different records.

- **IDs:** next free are **F-001** and **D-001**. Update this line when allocating an ID; never reuse one.
- Scope items and accepted findings use permanent F IDs. Each needs a plain description, done-means, and appropriate evidence references.
- Proposed findings remain unapproved until challenged and triaged. Record the original finding and the challenge outcome so a rejected finding is not lost or silently fixed.
- When a version ships, move completed F IDs to **Closed IDs**, with the version and evidence reference. Retain this small allocation history even without Git metadata. Defer unresolved items under **Open items**. Clear the current scope only after the release action was actually authorized and completed.
- List unused allocated decision IDs under **Reserved decision IDs** using `- D-003 is reserved: <reason>.` Retire superseded decisions in the decisions document. Every allocated decision ID must be active, retired, or reserved.

## Current version

None approved.

Format only:

```markdown
### <version> — <owner's goal>
- **Scope approval:** <date and owner message/reference>
- **Design approval:** <date and owner message/reference; linked design/brief and decisions>
- **F-001 — <item>:** <description>. Done means: <observable engineering and scientific acceptance criteria>.
- **Run additions:** <checks specific to this version>
- **Resource authorization:** <approved platform, limits, cost cap, allowed jobs>
- **Bounded cycle:** <task ID and attempt ID from WORKFLOW_STATE.json, charter relationship, and learning objective; no duplicate stage counter>
```

## Findings awaiting challenge or owner triage

None yet.

```markdown
### F-002: <finding>
- **Origin and evidence:** <review/test; VERIFIED, TRACED, or NOT RUN; file:line and/or run record>
- **Cause and consequence:** <reachable input/path, affected output or claim, severity>
- **Independent challenge:** <reviewer/session; confirmed, partly confirmed, or refuted; evidence>
- **Implications and recommendation:** <affected stages/results/docs; smallest fix or deferral>
- **Owner triage:** <pending, fix now, defer, or reject; approval reference and reason>
- **Approved fix batch:** <scope/approach, done-means, approval reference; pending until approved>
```

## Open items

None yet. Keep deferred findings with their IDs, evidence, disposition, and next required action.

## Gate approvals and waivers

None yet. Record the version, exact gate, approval/waiver, owner reference, scope, rationale, limits, and remaining evidence requirement. A waiver must be explicit and specific; it does not verify an unexecuted test or support a scientific claim.

## Cycle understanding, reflection, and manual handoff

None yet. For each bounded cycle, retain the actual learning objective, implementation/evidence pointers, owner's understanding acknowledgement or open questions, owner's reflections (or explicit exercise skip), separate agent observations, and handoff contents. Do not invent what the owner learned. Read the stage from WORKFLOW_STATE.json rather than putting it here.

Finish cycle archives the completed attempt and returns to Guide with no active task; it is not a Git commit. Restart preserves the task but creates a new attempt at Guide. Abandon records its disposition and returns to Guide without deleting/reverting files. The owner stages/commits manually. Move F IDs to Closed IDs only when released or explicitly dropped/rejected, keeping the disposition.

## Charter revision compatibility

None yet. Reopening Initialise preserves the prior charter and suspends active work. After the revised description is approved, record reviewed earlier decisions/task assumptions, compatible/revise/retire dispositions, required owner choices, and evidence references. Obtain Approve compatibility review before Build. Do not silently discard decisions or resume a suspended task; wait for explicit restart or abandonment after returning to Guide.

## Reserved decision IDs

None.

## Closed IDs

None. Use one line per allocated F ID with disposition, version/date, and evidence or approval reference. Rejected findings also keep their ID here.
