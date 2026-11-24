# Glossary

Use one shared term per concept in briefs, code comments, reports, and user documentation. Add or change project-specific meanings with the owner's approval; record consequential rules as decisions.

## Project terms

UNCONFIGURED. Add the project's scientific entities, units, references, and output terms when agreed. Do not assume that every project analyzes samples, reads, genes, or patients.

## Process terms

- **Initialise:** one-time conversational Stage 0 establishing project identity, vision, motivation, intended outcome, learning goals, and initial boundaries, without requiring a technical specification.
- **Project charter:** short, stable PROJECT.md description approved for a specific revision; approval does not authorize architecture, methods, task scope, or implementation.
- **Technical brief:** evolving technical context and approved design for selected work, developed after task selection; not an Initialise prerequisite.
- **Task:** one selected bounded unit of work with a permanent identity.
- **Attempt:** one pass through the development cycle for a task; restarting keeps the task ID and creates a unique attempt ID.
- **Suspended task:** a preserved active-task checkpoint held while Initialise is reopened, pending explicit restart or abandonment.
- **Compatibility review:** owner-reviewed dispositions for prior decisions/task assumptions after a charter revision; required before Build and separate from description approval.

- **Guide:** read the approved charter, orient the owner, and recommend one bounded step serving project and learning objectives; no active task is required to recommend a direction.
- **Learn:** explain relevant concepts, options, assumptions, and tradeoffs before the owner chooses.
- **Choose:** obtain the owner's informed decisions and required scope/design/fix approvals.
- **Document:** Codex records actual approved choices, scope, and validation expectations before implementation.
- **Build:** implement and test the current approved slice, with applicable reviews and evidence.
- **Understand:** explain the actual code, data flow, checks, results, and limitations, and obtain the owner's real acknowledgement.
- **Reflect:** required conceptual understanding dialogue with chat feedback and follow-up demonstration, followed by reflection/audit/manual handoff; incomplete while essential concepts remain unassessed or mistaken.
- **Commit:** the owner's manual Git staging/commit action after handoff, outside the agent-run stages.
- **Workflow state:** authoritative initialization, charter approval, active/suspended task, attempt, stage/status, and history in WORKFLOW_STATE.json; conversation is not a stage source.
- **READY:** current-stage work has completion evidence, but the stage has not advanced. Only an explicit owner instruction authorizes the next transition.
- **Stage transition:** an explicitly owner-authorized start/move/finish recorded in state history, distinct from methodological approval.
- **Release:** an explicitly approved distribution/version milestone with completed applicable review/validation/audit gates; a local commit is not a release.

- **Owner:** person approving scope, design, triage, fix batches, resource limits, and releases.
- **PM:** coordinating agent that keeps project memory, checks claims, and brings owner decisions.
- **Lead:** agent responsible for one approved implementation and its evidence.
- **Worker:** agent handling one bounded task within the Lead's brief.
- **Independent reviewer:** a separate agent/session or qualified person who did not implement the reviewed change and reviews it read-only.
- **Finding:** a possible defect or unsupported claim, challenged before owner triage.
- **Oracle:** independently justified expectation or comparator used to assess an output.
- **Run record:** versioned account of exactly what ran, with provenance, results, and limitations.
- **VERIFIED:** an executed check supports the specific stated claim, within the recorded conditions.
- **TRACED:** source inspection supports the statement; execution has not established it.
- **NOT RUN:** execution is planned or unavailable, with reason and consequence stated.
- **SUPPORTED:** scientific claim has appropriate evidence within stated limits.
- **UNSUPPORTED:** the cited evidence does not justify the scientific claim.
- **NEEDS VALIDATION:** evidence is insufficient or an appropriate validation remains pending.

These process definitions describe the template. They are not recorded owner approvals for a new project's scientific choices.

- **Conceptual assessment:** task-proportionate explanation/application questions against approved learning goals; no code mastery or memorization unless explicitly part of those goals.
- **Demonstrated concept:** an actual owner response meets the declared criterion; the agent's own correction is not evidence of this.
- **Assessment receipt:** a preserved structured dialogue assessment bound to task/attempt, charter, learning goals, and implementation identity, required for Reflect readiness/completion.
