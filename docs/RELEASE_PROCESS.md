# Guided development and release process

Begin a new project with the one-time **Stage 0 — Initialise**. Then use **Guide → Learn → Choose → Document → Build → Understand → Reflect**, followed by the owner's **manual Commit**, for each small change. Several cycles can contribute to one release. Template maintenance does not initialize a biological project or start its task work.

Codex actively teaches before choices and explains the actual implementation afterwards, with pauses controlled by the owner. Codex writes the project documents. Learning and owner understanding are distinct from scientific validation, and a local commit is distinct from release approval.

## Persistent workflow state

`WORKFLOW_STATE.json` is the only authority for initialization, approved charter revision, active/suspended task, attempt, stage, and history. PROJECT.md supplies project purpose; the ledger holds scope and outcomes. Neither is a second stage record. Read state and the approved charter when resuming; never infer stage from conversation, files, tests, or Git.

The initial state is NOT_STARTED with an UNINITIALIZED project. The owner starts Initialise, approves the description, and separately moves to Guide. Task selection, each named move, completion/restart/abandonment, and reopening Initialise require actual owner instructions/references. Description approval is not architecture, method, task, budget, or implementation approval. Encouragement and silence are never transitions.

The helper `scripts/workflow_state.py` has read-only status and evidence-only ready operations, plus the owner-authorized operations below. READY does not advance stages. Normal forward moves are adjacent and require readiness; explicit finish/restart/abandon operations return to Guide. Every update checks the expected revision, replays full history, locks concurrent writes, and writes atomically. Missing/corrupt state stops the action; never reconstruct it from chat.

| Operation | Required actual owner instruction | Result |
| --- | --- | --- |
| initialise | Start Initialise | Enter Stage 0 once, without selecting a task. |
| approve-project | Approve project description | Record exact charter text/revision/reference; remain Initialise READY. |
| move --to Guide | Move to Guide | Leave approved Initialise without approving implementation. |
| start | Start Guide | Select one task at Guide, with a task ID, unique attempt ID, and title. |
| move | Move to the named stage | Record the normal transition; method approvals remain separate. |
| finish | Finish cycle | Archive the completed attempt; Guide with no active task. |
| restart | Restart task | Preserve task identity; archive the old attempt and start a new attempt at Guide. |
| abandon | Abandon task | Archive the abandoned attempt; Guide with no active task. |
| reopen-project | Reopen Initialise | Start the next charter revision, suspending active work at its exact checkpoint. |
| compatibility | Approve compatibility review | Record owner-reviewed decision/task dispositions; no stage change. |
| migrate | Migrate workflow state | Upgrade valid v1/v2 state to schema 3, preserving project/task/stage and complete original histories; no conceptual mastery is inferred. |
| reopen-reflection | Reopen Reflect assessment | Preserve the same Reflect task/attempt, withdraw readiness to ACTIVE, retain the previous handoff and evidence. |

All mutations require --expected-revision; owner operations also require the exact --owner-command and actual --authorization-ref. Restart/reopen/abandon need a reason; restart needs a new attempt ID; compatibility needs dispositions/evidence. The start operation requires --task-id and --attempt-id (--cycle-id remains an alias for --attempt-id). These are recording interfaces for Codex; the owner normally uses chat instructions. The helper never edits the charter, decisions, source, outputs, or Git.

Approved charter text, revision, and digest remain in history. Unexpected charter changes stop task progression pending owner reconciliation. Status reads never migrate. Schema-1 imports retain their original initialization/compatibility requirements; schema-2 migration preserves its approved project, task, attempt and current stage/readiness. A legacy Reflect READY has no qualifying new assessment receipt and cannot finish under schema 3. Only explicit Reopen Reflect assessment withdraws readiness; migration alone never resets a stage. Historical completed cycles are preserved under their original rules, not retroactively labelled as conceptually assessed.

The helper records authorization provenance but cannot authenticate a chat speaker or prove that a method was approved. Codex must provide the actual owner instruction/reference and verify the separate design, budget, and evidence gates. State completion must never fabricate owner understanding, reflections, approvals, or a manual commit.

### Recovering missing or invalid state

Stop stage-specific work and report the actual file/read/validation problem. With the owner's direction, look for an identified authoritative backup or versioned copy, inspect it with the helper, and restore that exact record only after explicit owner authorization. Preserve the damaged record where applicable; never pick the most plausible stage from chat or silently discard its history.

If no authoritative copy can be recovered, the owner may explicitly authorize reset to the original NOT_STARTED template. Record the lost-state incident, approval, and limits in the ledger and preserve available evidence. Reset is not inferred continuity. Start Initialise and re-establish project approval; existing decisions remain available for compatibility review. Never automatically break locks or reset after a failed command.

## Roles and authorization

- **Owner:** approves scope, design, scientific choices not already settled, finding triage, fix batches, resource limits, and releases. Only the owner widens frozen scope.
- **PM:** inspects the project, keeps memory, writes bounded briefs, checks claims against actual artifacts, and brings owner decisions with recommendations.
- **Learning guide:** the PM also teaches relevant concepts, recommends small steps, answers questions, and explains implementation/results without taking the owner's choices or transitions away.
- **Lead:** owns one approved implementation, integration, verification, and evidence in one checkout.
- **Workers:** execute bounded tasks; they do not expand scope or spawn more agents.
- **Reviewers:** independent from the implementation, read-only, with distinct engineering/scientific/reproducibility briefs. A second reviewer challenges findings it did not raise.

Use available Codex subagents when separate agents are needed. Do not assume a particular model or create user-owned chats automatically. Parallel writers use separate worktrees. If independent review is unavailable, keep the gate open and ask the owner to arrange it or explicitly waive that specific review with its limitations recorded. Do not relabel self-review as independent.

An approval in chat is valid authorization; record its date/reference and exact scope. Do not request it again unless the proposed action materially changes. Waivers are specific, explicit owner decisions recorded in the ledger. A waiver cannot make a test pass, create missing evidence, or support an unsupported claim.

## Stages, outputs, and pauses

At every stage, report its recorded name, the bounded task, what was completed, what is still open, and the next possible transition. Mark readiness separately, then wait for the owner to name the next stage. Shortening an explanation at the owner's request does not authorize changing stages.

### 0. Initialise — once per project

Help articulate the owner's vision, motivation, eventual successful outcome, current knowledge/learning goals, and known boundaries. Follow the conversation with short responsive questions instead of a fixed questionnaire. Vague ideas and unknown tools/requirements are acceptable.

Codex drafts a concise PROJECT.md charter in the owner's words with explicit unknowns and optional undecided directions. It must not become an architecture, detailed specification, large implementation plan, approved backlog, or permission to build future ideas. The technical brief can remain unconfigured. **Output:** a short project description. **Gate:** owner approval of that exact description/revision. **Pause:** approval leaves Initialise READY; wait for Move to Guide.

The charter supplies stable direction; the technical brief develops selected-task design; workflow state says where the owner actually is. Read the approved charter before recommending work in Guide.

### 1. Guide

Read the approved PROJECT.md charter and inspect actual code, decisions, evidence, and available technical context. Recommend one small useful change and explain how it serves the overall project and learning goals. Guide may have no active task; it does not require a complete technical brief. Record a task only after the owner selects that direction using Start Guide, with separate task and attempt IDs. Scope remains provisional until Choose. **Output:** a bounded recommendation and learning goal. **Pause:** owner authorizes the next transition.

### 2. Learn

Explain the relevant biological and computational concepts in plain language before implementation: input/output meaning, method assumptions, alternatives and tradeoffs, validation expectations, and a recommendation with reasons. Verify consequential method contracts against primary sources. Adapt depth to the owner's background, answer questions, and offer optional examples rather than an unsolicited exam. **Output:** an informed owner and explicit remaining questions. **Pause:** ask whether the owner is ready to move to Choose; never infer readiness from silence.

### 3. Choose

Bring the exact proposed scope/design, methods, references, parameters, QC/error behavior, dependencies, validation oracle/metrics/tolerances, resource budget, and limits for approval. Existing approved decisions settle already-approved choices; unresolved consequential choices remain with the owner. For findings, obtain triage and fix-batch approval after the finding gate. **Output:** actual owner choices and approval references; unresolved choices remain pending. **Gate:** do not mark ready until the required approvals exist. **Pause:** the owner separately authorizes moving to Document.

### 4. Document

Codex records approved choices in decisions, scope/done-means/approval references in the ledger, learning objective and project context in the brief, and expected checks in the validation plan. Update agreed glossary terms. Use in-progress status while implementation differs; do not describe planned code as existing code. Preserve the owner authorization in the state history, not a second stage counter. **Output:** a clear approved implementation brief with testable acceptance. **Pause:** marking documents ready does not permit implementation; wait for the owner's Move to Build instruction.

### 5. Build

Start the Lead using Start Lead only when the persisted stage is Build and scope/design approvals exist. Implement this approved slice with meaningful tests, safe failure handling, and approved actual execution. Record unique run evidence including failures, update the factual code map, and assess scientific/reproducibility expectations. Routine internal choices remain with the Lead when they do not change approved behavior, science, or constraints. Failed work-in-progress acceptance checks can guide completion of the already-approved implementation; a new defect, method choice, or scope change enters the finding/decision gates. Applicable independent reviewers assess the candidate; the PM challenges findings and requests owner triage before fixes. Do not change the stage automatically when this requires returning to Learn/Choose. **Output:** an inspected implementation, actual check results, findings, and explicit unmet criteria. **Pause:** stop after this slice and wait for Move to Understand. Do not stage or commit files.

### 6. Understand

Walk the owner through the actual changed files and data flow, key code, approved choices, how to run/debug the slice, tests performed, output meaning, and limitations. Explain what is VERIFIED, TRACED, NOT RUN, scientifically supported, or still unvalidated. Use actual artifacts rather than a generic tutorial. Invite questions and offer an optional small exercise; never invent understanding or force a quiz. **Output:** walkthrough plus the owner's actual acknowledgement/questions. **Gate:** owner acknowledgement is needed for readiness and does not replace scientific evidence. **Pause:** wait for the owner's Move to Reflect instruction.

### 7. Reflect

Use the reflect-understanding skill for a required conceptual assessment before personal reflection or final handoff. Derive a small set of essential concepts/criteria from the approved learning goals, actual implementation, and interpretation limits. Ask one focused explanation/application question at a time. Say in chat what is right, mistaken, or importantly unassessed. An omission is not proof of ignorance: ask about it. Do not demand coding syntax, implementation mastery, memorized numbers, or untaught details.

Give corrective feedback in chat, then ask a targeted follow-up or new scenario and wait for an actual response demonstrating the corrected concept. The agent's clarification, owner confidence, or an acknowledgement alone is insufficient. Requests to avoid code narrow the discussion to concepts; they do not waive it. If the owner stops before essential gaps are resolved, pause Reflect ACTIVE. Do not offer normal completion by waiver.

Record actual questions, owner answers/message references, assessments, feedback/message references, gaps, and follow-ups in a per-attempt JSON assessment using the reflect-understanding skill's reference format. Bind it to task/attempt, charter revision, learning goals, and reviewed implementation files. Only demonstrated concepts can pass; never infer learning from the agent's own correction. Changed relevant files or a restarted/backtracked attempt invalidate applicability.

After the conceptual dialogue succeeds, discuss learning/outcomes/limits, record actual reflections separately from agent observations, and finalize the handoff/audit. The helper ready operation at Reflect requires --assessment with the project-relative JSON path as well as completion evidence/revision. It validates structure and file integrity, not semantic truth or speaker identity. Finish independently rechecks the receipt/artifact/bindings; neither a clean audit nor historical generic READY can substitute. **Output:** demonstrated conceptual understanding, a faithful dialogue record, reflection, and manual handoff. **Pause:** wait for explicit Finish cycle; no automated Git action.

### 8. Commit — owner only

The owner stages and commits manually. Codex hands off after Reflect and never runs Git staging, commit, amend, or repository-initialization commands. Finish cycle archives the completed attempt and returns to Guide with no active task. It does not commit or automatically select another task. Read-only Git inspection is permitted; publishing remains separate authorization.

## Restart, abandon, and redefine

| Owner action | Return point | What is preserved |
| --- | --- | --- |
| Complete cycle | Guide, no active task | Completed attempt, handoff, decisions, evidence |
| Restart task | Guide, same task/new attempt | Old checkpoint, files, results, reason |
| Abandon task | Guide, no active task | Abandoned attempt and artifacts; no automatic rollback |
| Entirely new project | Stage 0 in a fresh directory | Existing projects stay intact |
| Reopen Initialise | Stage 0, active task suspended | Prior charter revision, decisions, checkpoint, evidence |

Restart and abandonment never repeat Initialise or delete/revert/stage/commit files. Reopen requires explicit approval and a reason. Preserve approved charter snapshots while drafting the next revision. After approval and Move to Guide, suspended work stays held until explicit restart or abandonment; never resume its previous stage or replace it with a new task silently.

Review previous decisions/task assumptions for compatibility, retain compatible/revise/retire dispositions, and obtain approval for consequential changes. Record Approve compatibility review with evidence before Build. Charter approval alone does not close this gate. The review may be the next bounded task; it must not force a full technical design during Initialise.

## Release-level safeguards across cycles

- **Scope and design:** the owner approves the bounded release and each consequential addition. Cycles do not silently widen it.
- **Independent reviews:** reviewers assess the exact candidate. Engineering checks contracts/failure paths/tests/dependencies; science checks methods/identity/reference compatibility/design/QC/claims; reproducibility checks provenance and repeatability. Findings are challenged and triaged; code reading does not replace actual validation.
- **Fix rounds:** owner-approved batches get regression checks and focused review. New findings return to triage. After multiple fix rounds or mid-version scope additions, one fresh convergence review checks interactions across changes since initial review. At most one convergence review; remaining blocking uncertainty goes to the owner.
- **Actual validation:** execute the approved checklist in the intended or justified representative environment within budget. Record actual scientific comparisons and the agreed clean-environment repeat or independent reproducibility comparison. Acceptance must be met or a specific owner-approved exception must limit the release and its claims. Unsupported claims cannot become supported by waiver. After this gate, only show-stoppers reopen implementation.
- **Final record/audit:** decisions and source tags, factual code map, glossary, validation index, and run evidence must match the exact candidate. The Lead runs the checker; the PM independently checks changed docs/code, missing coverage, and rule stacks. No mechanical failures or unresolved warning dispositions. A passing script is insufficient, and any relevant later change reopens affected checks/reviews.
- **Release approval:** present the exact candidate, release notes, evidence, limits, open findings/waivers, and proposed external actions. Obtain explicit owner authorization before tagging, pushing, or publishing. Owner-controlled stage transitions do not authorize these actions. Record actual completion; close released F IDs with evidence and preserve allocation history. A manual local commit is not a release.

## Scoping rule

For each proposed item, trace the current implementation and decisions, list affected input/behavior/scientific cases, check applicable rule stacks, and identify downstream effects. Recommend the smallest useful change, including reuse of established tools. Separate settled choices, owner choices, and contradictions. Record an observable done-means for every approved item. Findings and interesting adjacent ideas never widen frozen scope by themselves.

## Finding gate

Every potential defect from review, audit, actual execution, or inspection passes through:

1. **Disprove:** a different reviewer tries to refute it. Record confirmed, partly confirmed, or refuted, with actual reachability and evidence.
2. **Implications:** identify affected stages, scientific claims, stored outputs, references, docs, tests, and the smallest remedy.
3. **Batch:** the PM brings one list per round, including rejected/deferred recommendations, for owner triage and fix approval.

If challenge is unavailable, leave that gate open or obtain an explicit, recorded owner waiver. Never silently drop a finding because another agent disagrees.

## Triage and stopping rules

- Recommend current-version fixes for defects introduced by the version or reachable defects causing false results, data loss, harmful interpretation, or a blocked core flow. Defer other work with reasons; the owner makes the decision.
- One initial review, focused fix reviews, and at most one convergence review. Avoid open-ended re-review and unrelated cleanup.
- After the actual validation gate, only show-stoppers justify reopening implementation. Reopen all affected evidence when they do.
- If a gate cannot be met, report the precise missing evidence or decision. Do not claim release readiness.
- Hotfixes get a separately scoped minimal release with the same applicable gates; they do not expand another active version.

## Evidence rules

Every finding cites file/line and causal steps, or an actual run/artifact reference. **VERIFIED** means executed evidence for the stated claim; **TRACED** means inspection only; **NOT RUN** identifies missing execution and its impact. Scientific status is separately **SUPPORTED**, **UNSUPPORTED**, or **NEEDS VALIDATION**, always bounded by the actual evidence. Independent AI agreement and successful execution do not, by themselves, validate a biological interpretation.
