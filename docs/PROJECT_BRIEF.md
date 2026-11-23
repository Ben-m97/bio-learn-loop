# Technical brief for selected work

**Status:** UNCONFIGURED

The stable project charter is in PROJECT.md. This brief develops technical details progressively for selected micro-tasks through Learn, Choose, and Document; it is not a prerequisite for Initialise. Leave unknown or irrelevant fields unset rather than specifying the whole project prematurely. Examples are not defaults or approvals. Use DRAFT for proposals and APPROVED only for the actual bounded technical choices the owner approved; that approval does not authorize an entire implementation roadmap.

## Current task context

- **Charter relationship:** <how this selected task serves the approved PROJECT.md objectives>
- **Question:** <scientific or analytical question for this task>
- **Audience and use:** <relevant users and limits for this slice>
- **Outputs and claims:** <deliverables and what they can support>
- **Out of scope:** <explicit exclusions for the project and first release>
- **Existing implementation:** <reuse candidates and inspected project state>

## Learning and guidance

- **Learning goals:** <what this task contributes to the learning goals in PROJECT.md>
- **Relevant starting point:** <use the owner's already-known background; clarify only what this task needs>
- **Guidance:** Guided learning with explanations and pauses. Teach concepts/options before choices and actual code/results after Build; adapt depth to the owner without skipping owner-authorized transitions.
- **Workflow state:** Read `WORKFLOW_STATE.json` for the current stage. Do not duplicate it here or infer it from conversation.
- **Manual Git:** The owner stages and commits. Codex hands off after Reflect and records completion only after Finish cycle.

A plain-language vision is enough to begin Initialise. These technical fields are developed later, only as useful for the chosen task. The owner need not fill in either document manually.

## Input and output contracts

- **Inputs:** <formats, required fields, units, schemas, encodings, and missing-data rules>
- **Identity and metadata:** <sample/entity identifiers, joins, uniqueness, required covariates, batch information>
- **Experimental unit:** <independent unit, technical/biological replicates, or reason inapplicable>
- **References:** <databases/builds/annotations, releases, compatibility, licences, identifiers/checksums>
- **Outputs:** <formats, schemas, units, identifiers, expected multiplicity, and downstream consumers>
- **Failure and QC policy:** <reject/warn/exclude rules and how affected entities remain visible>
- **Data access:** <public/synthetic/protected, permitted storage, handling and sharing restrictions>

## Methods and assumptions

- **Proposed methods:** <stages, alternatives considered, rationale, primary sources>
- **Parameters:** <scientifically meaningful defaults, thresholds, and how they are chosen>
- **Design and statistics:** <confounding, leakage, model assumptions, multiple testing, or justified inapplicability>
- **Limitations:** <known constraints, unresolved uncertainty, limits on interpretation>
- **Decision references:** <approved decision IDs once assigned; leave pending choices unapproved>

## Engineering and execution

- **Engine and languages:** <chosen per project with rationale; no mandatory engine>
- **Dependencies:** <pinned container digests or locked environments; tool/runtime versions>
- **Target platform:** <local, WSL/Linux, HPC scheduler, cloud, or other environment>
- **Resources and budget:** <CPU/RAM/storage/time limits, cost cap, approval needed before exceeding them>
- **Execution entrypoints:** <run/test commands and configuration locations after design approval>
- **Failure recovery:** <partial outputs, resume/retry semantics, idempotency, safe cleanup>
- **Reproducibility target:** <bitwise or agreed metrics/tolerances; seeds and nondeterminism>

## Selected task and release context

- **Goal:** <one small useful deliverable>
- **Proposed scope:** <items and acceptance criteria; approved scope belongs in the ledger>
- **Validation:** <link to the validation plan and required scientific evidence>
- **Approval:** <date and owner message/reference approving the brief; none yet>

An approved brief does not itself approve a release or waive later gates.
