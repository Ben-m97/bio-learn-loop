---
name: start-lead
description: Start or update the implementation Lead for an owner-approved bounded bioinformatics change in the recorded Build stage. Check scope, design, resource authorization, isolation, and learning handoff; do not advance stages or make Git commits.
---

# Start a Lead

Use after the owner approves scope and design, following root `AGENTS.md` and `docs/RELEASE_PROCESS.md`. Existing approval in the active conversation counts; record it rather than asking again. This skill does not grant release, publication, or unbudgeted compute permission.

Read `docs/WORKFLOW_STATE.json` first. Pipeline implementation requires the recorded Build stage, after the owner explicitly authorized moving there and the Choose/Document approvals/records exist. Do not infer the stage from chat, completed documents, or a request to use this skill. If the state is elsewhere/missing/invalid, report the unmet gate rather than advancing it. Maintenance of this template is a separately authorized task and leaves its biological-cycle state unchanged.

Also read the approved `docs/PROJECT.md` charter. Project initialization/charter approval must exist, an active task/attempt must be selected, and any compatibility review required by a revised charter must be approved. The technical brief develops for this task; its absence during Initialise is valid and does not authorize premature specification. Never replace suspended work with a new task or resume its old stage automatically. Restart/abandon return to Guide without repeating Initialise; the owner controls those actions.

## Pre-start checks

- Inspect the brief, ledger current version, affected decisions/code map, and validation criteria. Every item has a done-means and a scope/design approval reference. Pending consequential scientific choices go to the owner first.
- Check actual engine/runtime, data access, reference/environment availability, and approved CPU/RAM/storage/time/cost. Report a missing capability before committing to a run.
- Give the Lead a unique project-local label, using the ledger and available branch/commit records to avoid reuse. Record its session/subagent identity in the current version.
- One writer uses each checkout. A parallel writer needs an isolated worktree; prefer the current suitable checkout when no concurrent writer exists.
- Use the available Codex delegation tools for the Lead and reviewers. Do not assume model names or create user-owned sidebar chats without a request. Workers receive bounded tasks and do not delegate further.

## Lead brief

Include:

- **Goal and scope:** version, exact approved F IDs and done-means; exclusions and approval references.
- **Cycle and learning handoff:** active task ID, attempt ID, approved charter revision, relationship to project objectives, learning objective, concepts already discussed, and material for Understand. Do not maintain another stage field in the brief.
- **Pointers:** relevant brief sections, decisions/rule stacks, source-map sections, validation checks, and inspected evidence.
- **Design and contracts:** chosen approach, data/metadata/reference contracts, methods/parameters, error/QC behavior, outputs, and accepted limitations.
- **Permissions and budget:** allowed paths, environment/data access, compute/resource limits; actions requiring further approval.
- **Gates:** independent engineering/scientific/reproducibility reviews, finding challenge, owner triage/fix approval, actual validation, record audit, and release approval.
- **Findings and uncertainty:** new design choices return to the PM; findings enter the ledger and are challenged before owner triage. Never widen scope or silently change a method/reference.
- **Evidence and stopping:** commands/results/artifacts, run-record requirements, VERIFIED/TRACED/NOT RUN, scientific claim status, and precise blockers. Stop when approved work is complete or a consequential missing decision prevents progress.
- **Report:** changed behavior, acceptance evidence/limits, findings, candidate revision and dirty state, branch/commit/push state, and the next open gate. Do not publish a release on the PM's behalf without owner authorization.
- **Manual Git:** do not stage files, create/amend commits, initialize Git, or advance stages. Return the bounded implementation and evidence to the PM; the owner handles commits after Understand and Reflect.

## While work runs and when it returns

Do non-overlapping coordination or wait for completion events. Do not duplicate the Lead's investigation. Add work to a running version only after the owner approves the added scope/design; update the ledger and brief the same Lead unless parallel work was requested.

Verify returned claims against actual artifacts, code, decisions, and acceptance criteria. A proposed command is NOT RUN; source reading is TRACED. Arrange independent read-only reviews and a separate challenge for findings. If those capabilities are missing, report the open gate for owner direction or a specific recorded waiver. Self-review does not satisfy independence.

Build completion can be recorded as READY with actual evidence; it does not authorize Understand. Wait for the owner's explicit named transition. The PM then teaches the actual code/results in Understand and records the owner's acknowledgement, followed by owner-authorized Reflect and a manual-commit handoff. Do not silently continue the next pipeline slice.
