# Repository instructions

This is a reusable, engine-neutral template for developing bioinformatics pipelines with Codex. Read `docs/PROJECT.md` for the owner's project charter and `docs/PROJECT_BRIEF.md` for evolving technical details of selected work. These instructions define agent behavior, not a project's scientific objectives.

## Stage 0 — Initialise

- A new project begins with an owner-authorized **Start Initialise** before any task cycle. Through short, responsive conversation, help articulate vision, motivation, intended outcome, current knowledge/learning goals, and known boundaries. Follow the owner's answers rather than delivering a rigid questionnaire.
- Codex drafts a short, stable `docs/PROJECT.md` in the owner's words. Unknowns are acceptable. Do not demand architecture, tools, detailed requirements, methods, or an implementation plan. Possible future directions remain explicitly undecided and authorize no work.
- Only the owner can approve the project description. Record **Approve project description** and the exact charter revision/text in state; this marks Initialise READY but does not advance it or approve any architecture, method, task, or budget. A separate **Move to Guide** is required.
- Guide reads the approved charter and relates each proposed micro-task to its objectives. The technical brief grows through Learn, Choose, and Document for selected tasks; it need not be completed during Initialise.
- Initialise runs once unless the owner explicitly says **Reopen Initialise**. Preserve previous charter revisions, decisions, and evidence; suspend any active task at its recorded checkpoint. After the revised description is approved, return to Guide only on authorization. Do not automatically resume the suspended task.
- Before Build under a revised charter, review earlier decisions and task assumptions for compatibility, retain dispositions, and obtain **Approve compatibility review** with actual evidence/reference. Do not silently discard rules or equate charter approval with approval of their scientific consequences.

## Owner-controlled learning cycle

Use **Guide → Learn → Choose → Document → Build → Understand → Reflect** for one small, bounded change at a time. **Commit is the owner's manual step after the handoff.** Codex does not stage files or create/amend Git commits.

- **Guide:** read the approved charter, inspect the project, and recommend the next small step with its purpose, relationship to the project objectives, and learning goal.
- **Learn:** teach the relevant concepts, methods, alternatives, assumptions, and tradeoffs before asking for a choice. Use concise explanations and pause for questions; adapt depth to the owner.
- **Choose:** bring recommendations and unresolved choices for owner approval of scope, design, methods, validation expectations, and budget. Do not treat learning or discussion as approval.
- **Document:** Codex records the actual approved decisions, current scope, and validation plan. The owner need not fill in documents. Unsettled choices stay explicitly provisional.
- **Build:** implement and test only that approved slice, with the applicable independent reviews and scientific/reproducibility checks. Do not silently start another slice.
- **Understand:** walk the owner through the changed code/data flow, how to run and debug it, the outputs, tests, scientific meaning, and limits. Pause until the owner explicitly says they are ready to move on; never invent understanding or require an unsolicited exam.
- **Reflect:** discuss what worked, what was learned, limitations, and the next useful question. Record only the owner's actual reflections or explicitly identified agent observations. Hand back the reviewed work for the owner's manual commit.

### Persistent state and transitions

- `docs/WORKFLOW_STATE.json` is the sole source of initialization/charter approval, active or suspended task, attempt, stage, and transition history. Read it at the start/resumption of pipeline work and before stage-specific actions. Never determine the stage by interpreting conversation, the ledger, test results, or Git history.
- The template starts **NOT_STARTED**, with an UNINITIALIZED project. Begin with **Start Initialise**. After charter approval and **Move to Guide**, Guide may recommend work without an active task; **Start Guide** selects one named task/attempt there. General encouragement, passed tests, completed work, silence, or method approval never authorize transitions.
- Record the actual owner instruction and message reference with the state helper in `scripts/workflow_state.py`. Codex may record that instruction, but must not invent authorization, pre-authorize future transitions, or advance multiple stages from a blanket “continue.” The helper records provenance; it cannot authenticate the speaker by itself.
- Codex can mark stage work **READY** with real completion evidence; this leaves the current stage unchanged. Wait for the owner's next explicit transition. Marking Choose ready also requires the necessary scope/design approvals; marking Understand ready requires the owner's actual acknowledgement. A transition alone does not approve unresolved scientific choices or fixes.
- If the state file is missing, invalid, stale, or inconsistent, stop stage-specific work and ask the owner to reconcile it. Never reconstruct it from conversation. Use revision checks and the helper rather than hand-editing stage/history fields.
- The ledger may link to a cycle's outcomes but must not maintain a second current-stage field. All pauses, including between Document and Build, respect the persisted stage. Read-only status/diff checks do not authorize Git mutations or a transition.
- After Reflect is ready and the owner says **Finish cycle**, archive the completed attempt and return to Guide with no active task. **Restart task** returns to Guide with the same task and a new attempt; **Abandon task** returns to Guide with no active task. Preserve all histories, decisions, files, and evidence; never delete/revert code as a side effect. The owner stages/commits manually.
- Reopening Initialise preserves active work as suspended. After approval and return to Guide, wait for explicit restart or abandonment; do not replace it with a new task or resume the previous stage. Neither task restart nor abandonment repeats Initialise.
- The helper validates schema-2 history. Version-1 status reads are read-only; an explicit **Migrate workflow state** preserves the complete old snapshot/history and holds legacy active work pending initialization and compatibility review. Never silently upgrade or infer charter approval.

The full stage outputs and release safeguards are in `docs/RELEASE_PROCESS.md`. Template maintenance requests authorize their scoped edits/checks without starting or advancing a biological pipeline cycle; leave the scaffold state NOT_STARTED.

## Starting work

- If the owner requests a project, inspect its actual state first. An uninitialized project needs Initialise and charter approval; missing technical details alone do not require reinitialization. Propose and approve each selected task's scope/design before pipeline code.
- Editing this template or its tooling is maintenance, not the start of a scientific pipeline release. A direct maintenance request authorizes the scoped edits and relevant checks; keep the scientific project documents unconfigured.
- Current user instructions and actual session permissions take precedence over repository documents. Within the project documents, approved decisions govern intended behavior; code and run evidence establish observed behavior. Report material conflicts rather than silently reconciling them.
- Read only relevant sections. Use file pointers in briefs instead of copying entire documents.

## Persistent project memory

- `docs/PROJECT.md`: short approved project vision, motivation, intended outcomes, learning goals, and initial boundaries.
- `docs/PROJECT_BRIEF.md`: evolving technical context, contracts, methods, tooling, and acceptance for selected work; not a prerequisite for Initialise.
- `docs/WORKFLOW_STATE.json`: authoritative project approval/revision, active/suspended task, attempts, stage, evidence, and transition history.
- `docs/DECISIONS.md`: approved rules and scientific choices, with permanent IDs, rationale, sources, and implementation references.
- `docs/CODE_MAP.md`: the actual workflow, source references, invariants, outputs, and debugging routes.
- `docs/RELEASE_PROCESS.md`: mandatory steps and approval gates.
- `docs/LEDGER.md`: current scope, findings, approvals, and permanent finding-ID bookkeeping.
- `docs/VALIDATION.md`: planned checks, expectations, scientific claims, evidence, and limitations.
- `docs/RUN_RECORD_TEMPLATE.md`: format for new run records under `docs/runs/`.
- `docs/GLOSSARY.md` and `docs/BACKLOG.md`: agreed vocabulary and owner-approved future ideas.

## Owner approval and delegation

- Follow the strict gates in the release process. Scope, design, finding triage, fix batches, and release require owner approval. An existing approval need not be requested again unless the proposal materially changes.
- The PM coordinates; the Lead implements the approved scope. Delegate bounded implementation or investigation to Workers when useful. Use independent read-only engineering, scientific, and reproducibility reviewers for a pipeline release, and a second reviewer to challenge findings. These are roles, not fixed model names or a requirement to run every role simultaneously.
- Use available Codex subagent capabilities when these roles need separate agents. Give each a bounded brief, relevant pointers, permissions, acceptance criteria, and stopping conditions. Workers do not delegate further. Do not create sidebar chats as a substitute without an owner request.
- One writer per checkout. Parallel writers need isolated worktrees and explicit integration. Reviewers do not edit implementation or evidence.
- Check capabilities before delegating. If independent review is unavailable, report the missing gate and ask the owner to arrange it or explicitly record a waiver. Self-review is not independent review. A waiver never turns unexecuted work into verified evidence.
- Do not publish, tag, push, submit compute jobs beyond the approved budget, or perform external releases without the applicable explicit authorization. Discussion is not approval.
- Git staging and commits are managed manually by the owner. A commit handoff is not a commit, a push, or a release. Do not ask for permission to make an agent commit as a routine stage.

## Scientific and engineering discipline

- Choose the workflow engine, languages, dependencies, and execution platform per project. Reuse suitable established pipelines or components before creating new infrastructure.
- Validate input structure, sample identity, required metadata, and reference compatibility before costly analysis. Define missing-data and QC failure behavior explicitly.
- Record reference/database releases, genome and annotation compatibility where relevant, tool versions, resolved dependencies, and non-default parameters. Use pinned containers or appropriately locked environments; do not silently update them.
- Use public or synthetic fixtures for shared tests. Keep raw sensitive data, identifiers, secrets, and sensitive output out of prompts, examples, repositories, and external services. Record protected provenance through permitted opaque identifiers in approved storage.
- Separate software execution from scientific validity. A successful exit, snapshot, second agent's agreement, or passing documentation audit does not establish a biological conclusion.
- Define expected results, independent comparators, metrics, and justified tolerances before evaluating a run. Do not validate a new implementation only against expectations generated by that same implementation.
- Consider experimental units, confounding, leakage, statistical assumptions, and multiple testing where applicable. Record a reason when a scientific check is inapplicable.
- Keep raw inputs immutable, avoid destructive output replacement, and make partial failures visible. Test meaningful behavior and failure paths in proportion to risk.
- Preserve relevant existing comments. Edit comments when necessary to keep them accurate; remove them only when their subject no longer exists or they are no longer relevant.

## Evidence and reporting

- **VERIFIED**: an executed check supports the specific stated claim; cite command, environment, result, and saved evidence.
- **TRACED**: supported by source inspection only; cite file and line.
- **NOT RUN**: planned or unavailable execution; state the reason and consequence.
- Scientific claims separately use **SUPPORTED**, **UNSUPPORTED**, or **NEEDS VALIDATION**, with the dataset/comparator and limitations. Never invent approvals, citations, test results, or biological findings.
- Report outcome, changed behavior, checks actually run, limitations, open owner decisions, and Git/publication state. Any method, reference, or code change reopens affected validation and documentation gates.

## Local verification

```text
python .agents/skills/docs-audit/scripts/check_docs.py --root .
python -m unittest discover -s .agents/skills/docs-audit/tests -v
python scripts/workflow_state.py --root . status
```

The checker is read-only and uses the Python standard library. The tests create isolated temporary fixture projects. Passing these checks validates template tooling, not a scientific pipeline release.
