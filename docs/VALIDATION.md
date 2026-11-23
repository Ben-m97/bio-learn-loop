# Validation plan and evidence index

**Status:** UNCONFIGURED — no project claims or validation results exist.

This technical validation plan develops for selected tasks after the project charter. It is not required to complete Initialise, and charter approval establishes no scientific claim or validation result.

Approve the validation design before judging outputs. Each release's ledger done-means links to the checks below. Save actual execution in separate run records, keeping planned expectations distinct from observations. Do not replace a failed result or tune its tolerance after the fact; document the cause and obtain approval for a material change.

Teach the basis of these checks in Learn, approve them in Choose, and document them before Build. Execute only authorized checks in Build, explain actual evidence and limitations in Understand, and assess unresolved questions in Reflect. Owner understanding or a stage transition is not scientific evidence. The authoritative stage is read from WORKFLOW_STATE.json, not inferred from this matrix's completion.

## Evidence matrix

Populate one row per meaningful claim or acceptance check. Rows below are field descriptions, not executed tests.

| Check ID | Claim or behavior | Layer | Dataset/oracle and independence | Expected result, metric, tolerance | Command/environment | Run record/result | Evidence | Scientific status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <check> | <specific claim> | <contract / engineering / scientific / reproducibility> | <source/version/checksum; why the expectation is justified> | <predeclared acceptance criteria and rationale> | <exact entrypoint/configuration once approved> | <pending; later link to actual record> | NOT RUN | NEEDS VALIDATION or NOT APPLICABLE with reason |

## Required coverage to consider

- **Contracts:** malformed and empty inputs; missing/duplicate identities; incompatible metadata, units, or references; missing files; explicit QC failure/exclusion behavior. Select applicable cases for the project.
- **Engineering:** stages and interfaces, small end-to-end execution, expected output structure/content, meaningful failure paths, and resume/recovery where supported. A successful exit or existing file is only an execution check.
- **Scientific validity:** appropriate known expectations, validated reference comparisons, simulated truth, controls, or independently justified invariants. Assess experimental units, confounding, leakage, assumptions, and interpretation where applicable.
- **Reproducibility:** recorded software and reference versions, immutable inputs, resolved parameters, seeds, clean-environment re-execution, and the agreed reproducibility target. Identify nondeterministic outputs and compare agreed metrics with justified tolerances.
- **Limitations:** what small fixtures cannot assess, untested environments, missing truth sets, underpowered comparisons, and the claims each limitation prevents.

Use primary sources for method contracts and independent expectations. Synthetic fixtures generated to exercise a branch are useful engineering tests; describe their limits as scientific evidence. Expectations produced solely by the code being tested are not independent validation.

## Review records

- **Engineering review:** pending; identity/session, exact candidate revision, scope, findings, and evidence.
- **Scientific review:** pending; identity/session, claims assessed, SUPPORTED/UNSUPPORTED/NEEDS VALIDATION, sources, and limits.
- **Reproducibility review:** pending; identity/session, run provenance, re-execution and comparison evidence.
- **Finding challenges:** pending; ledger references for each independently assessed finding.
- **Owner approvals:** pending; scope/design, triage/fix batches, waivers, and release references.

## Evidence handling

- Create a fresh run record from `RUN_RECORD_TEMPLATE.md` under `docs/runs/` for each actual attempt, including failures and partial runs. Use a unique UTC timestamp plus a descriptive suffix; do not overwrite earlier records.
- Cite records and approved artifact storage rather than embedding large data in documents. Use checksums for permitted public/non-sensitive artifacts and opaque permitted identifiers for protected data.
- A changed candidate, method, reference, or parameter invalidates affected conclusions until the relevant checks and reviews are repeated. Unaffected evidence can be reused only with a documented reason.
- Documentation audits and reviewer agreement are supporting process evidence, not proof of biological correctness.
