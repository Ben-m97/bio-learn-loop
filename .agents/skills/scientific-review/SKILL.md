---
name: scientific-review
description: Independently review the methods, data contracts, validation evidence, and scientific claims of a bioinformatics pipeline candidate. Produce read-only findings and bounded claim assessments; use for scientific review or finding challenge, not implementation or clinical interpretation.
---

# Scientific review

Review read-only. Read root `AGENTS.md`, relevant approved brief/decisions, the ledger scope, affected source, and `docs/VALIDATION.md` with linked run records. Review the exact supplied candidate; ask for its identity if it cannot be established. Do not edit code, thresholds, results, evidence, or approved decisions.

Within a guided pipeline cycle, read `docs/WORKFLOW_STATE.json` for the stage. Findings/evidence support Build and the owner's Understand walkthrough, then Reflect; they never authorize a transition. Return new choices/fixes to the PM for owner decisions and explicitly owner-authorized moves. An ad hoc review does not start a cycle. Do not claim that the owner understood the science or commit any files.

## Review the applicable science

- Match the method and outputs to the question and intended use. Verify consequential contracts and claims against primary documentation/papers; distinguish a source's result from an inference for this project.
- Trace identity through joins, transformations, exclusions, and aggregation. Check metadata requirements, units, missingness, experimental units, and reference/database/build/annotation compatibility where relevant.
- Examine selection and QC rules, parameter justification, confounding, leakage, model assumptions, replication, uncertainty, and multiple testing where applicable. State why a check is inapplicable rather than imposing sequencing or statistical requirements on every project.
- Compare evidence with the approved validation design: independently justified expectations, appropriate datasets/controls, metrics, tolerances, and scope of generalization. A clean exit, existing file, code snapshot, or second agent's agreement is not scientific validation.
- Check that failures, exclusions, contradictory evidence, untested situations, and unsupported interpretations remain visible. Do not expand a bounded software check into a general biological conclusion.

Consult `docs/PROJECT_BRIEF.md` for the actual analysis and engine. The examples are illustrative and do not select methods or thresholds for the project.

Read `docs/PROJECT.md` for the approved high-level purpose and the technical brief only for selected-work details. Initialising a vague project does not require scientific method or architecture choices. After a charter revision, assess earlier decisions/task assumptions for compatibility without silently discarding them; report dispositions for owner approval. Review findings do not initialize a project, restart suspended work, or advance stages.

## Report

Return:

1. Candidate revision/artifact identity, review scope, reviewer identity, and evidence inspected.
2. For each relevant claim: **SUPPORTED**, **UNSUPPORTED**, or **NEEDS VALIDATION**, with the specific basis, independent comparator/source, and limits.
3. For each finding: file/line or run/artifact reference, cause-to-consequence path, reachability, affected claims/stages, severity, smallest proposed remedy, and whether evidence is VERIFIED, TRACED, or NOT RUN.
4. Required owner decisions and missing checks, including what prevents the scientific gate from closing.

Send findings to the PM for independent challenge and owner triage. Do not implement a remedy or approve it yourself. If no findings survive your review, say what was inspected and its limits; do not declare the whole pipeline scientifically valid without the required evidence.

## Finding challenge mode

When asked to challenge another reviewer's finding, independently trace its strongest counterexample and evidence. Classify **confirmed**, **partly confirmed**, or **refuted**; explain actual reachability and residual implications. Do not treat a lack of reproduction under different conditions as a refutation. Return the challenge to the PM; the owner decides the disposition and fix batch.
