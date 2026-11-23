---
name: reproducibility-review
description: Independently audit a bioinformatics pipeline's recorded provenance, dependency/reference pinning, execution evidence, and reproducibility comparisons. Review read-only and identify missing evidence; executing a new or costly run requires separate existing authorization.
---

# Reproducibility review

Follow root `AGENTS.md` and the release process. Inspect the exact candidate, approved reproducibility target, validation plan, run records, execution configuration, dependency locks/container digests, logs, and artifact references. Review read-only; never rewrite an old run record to make it match the current code.

Within a guided pipeline cycle, read `docs/WORKFLOW_STATE.json` rather than inferring the stage. Give the PM evidence for Build, an explanation of repeatability/limits for Understand, and unresolved questions for Reflect. This review never advances stages, starts a new cycle, stages files, or commits. Owner understanding and scientific validity remain separate from reproducibility evidence.

Use the approved PROJECT.md charter for intended purpose and task/attempt identity from state. Charter approval is not evidence of a reproducible implementation. Preserve prior run records and suspended-task checkpoints across reinitialization, restarts, and abandonment; classify their applicability to the revised charter rather than deleting or relabeling them. A technical brief is not required during Initialise.

## Checks

- Can another authorized user identify the exact code, dirty diff/archive, engine/runtime, tools, environment, inputs, reference releases, resolved parameters, and command?
- Are dependencies pinned sufficiently for the target (resolved environment/lock or immutable container digest), and are reference/database builds, annotation compatibility, checksums or permitted opaque provenance available?
- Are raw inputs immutable, identities traceable, partial failures reported, outputs attributed to the correct run, and resume/cache provenance documented?
- Are resource limits, nondeterminism, seeds, relevant hardware/parallelism, logs, artifact locations, and retention recorded?
- Does an actual clean-environment rerun or approved independent comparison meet the predeclared target? Compare scientifically meaningful metrics/tolerances when byte identity is inappropriate. Source inspection is not an executed reproducibility check.
- Can the required provenance be retained without exposing protected data, identifiers, credentials, or sensitive output? Use permitted opaque references and approved storage where needed.

Do not download data, start jobs, or execute a rerun merely because this skill is invoked. Check the existing run authorization and budget; route missing authorization through the PM/owner. If a permitted run is requested as a separate task, the Lead records it as a new attempt using `docs/RUN_RECORD_TEMPLATE.md`.

## Report

Identify candidate and reviewer, inspected artifacts, each check and its evidence label (VERIFIED/TRACED/NOT RUN), observed agreement/differences, and limitations. Findings name the exact missing or inconsistent provenance, practical consequence, and smallest remedy. State whether the reproducibility gate has adequate evidence or which checks remain open. Send findings for independent challenge and owner triage; do not edit implementation, approve fixes, or certify scientific correctness from repeatability alone.
