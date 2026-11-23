# Illustrative applications

These are unexecuted planning examples. They contain no approved project decisions, real datasets, validated thresholds, or reported biological findings. Choose suitable methods and acceptance criteria for the actual question with the owner.

## Sequencing workflow

Possible first slice: validate input identities/metadata, run one agreed quality-control stage, and produce a traceable report. Inputs could be reads, assembled sequences, or another agreed representation; do not assume a layout or organism.

Engineering checks exercise malformed inputs, identity preservation, stage failures, and report content. Scientific checks need justified expected properties or independent reference comparisons appropriate to that stage. A tiny fixture demonstrates execution but cannot establish downstream biological validity. Quantification, inference, and additional preprocessing remain outside the first release unless approved.

## Variant analysis

Possible first slice: validate an existing variant dataset and its reference compatibility, apply one approved normalization/filtering step, and report exactly which records changed and why.

Review coordinate conventions, genome build, contig naming, allele representation, sample metadata, and applicability of the selected method. With an appropriate truth set, define comparison regions, matching policy, metrics, and acceptance tolerances before evaluation. Callset concordance alone does not establish clinical utility or validate all variant classes.

## Single-cell analysis

Possible first slice: validate a supplied count matrix and metadata, perform approved per-cell QC, and preserve a complete inclusion/exclusion record.

Review matrix orientation, feature and cell identity, count units, donor/sample structure, QC rationale, and batch/confounding information. Later modeling or annotation needs appropriate independent expectations and donor-aware validation when relevant. A plausible embedding or stable cluster count is insufficient evidence of a biological interpretation. This example does not impose a particular toolkit or assay.

## Applying the template

Begin any new project with Initialise and a short PROJECT.md charter; tools and exact requirements can remain unknown. Guide reads that approved purpose before recommending a slice. Develop the technical brief, decisions, ledger, validation plan, and run records only as the selected tasks need them. The method-specific review and oracle change; the approval/evidence process stays consistent. See [engine guidance](engine-guidance.md) for later implementation choices.

Apply Guide → Learn → Choose → Document → Build → Understand → Reflect to one small slice from any example. Codex teaches before choices and explains actual code/results afterwards, writes the records, and pauses at the stage in WORKFLOW_STATE.json until the owner explicitly authorizes a move. The owner commits manually after the handoff; these examples do not authorize transitions or implementation.
