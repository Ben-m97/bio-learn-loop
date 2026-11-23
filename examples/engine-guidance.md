# Conditional engine guidance

Select tooling for the actual project, existing implementation, scale, team expertise, and target execution environment. Record the approved choice in the brief/decisions. These are options, not required scaffolds or claims of nf-core compliance.

| Project choice | Reuse and implementation considerations | Verification to plan |
| --- | --- | --- |
| Nextflow | Prefer suitable established workflows/modules. If creating a workflow, use current supported DSL2 conventions, explicit channel contracts, pinned software, and local/HPC/cloud profiles as required. Reuse nf-core infrastructure when it fits. | Appropriate nf-test/component tests, a small actual workflow run, expected output content, failure/QC paths, provenance, and scientific comparisons beyond smoke execution. |
| Snakemake | Reuse suitable workflows/wrappers. Follow the project's supported Snakemake version and rule/input/output contracts; preserve an existing workflow layout. Pin environments/containers and document executor profiles. | Applicable rule/integration tests, input/metadata validation, an actual small run, output content checks, dependency provenance, and independent scientific expectations. A dry run verifies planning only. |
| R or Python | A small project may use explicit scripts or packages with clear entrypoints and structured configuration. Keep transformations testable and record the execution order, data contracts, and locked environment. | Appropriate language tests, a small end-to-end invocation, input/QC/failure checks, recorded resolved dependencies, and scientific/reproducibility comparisons. |
| Another engine | Preserve established project conventions where suitable. Specify entrypoints, stage contracts, dependency pinning, and provenance rather than translating unnecessarily. | Engine-appropriate checks with the same engineering, scientific, and reproducibility acceptance requirements. |

An engine's own template supplies execution infrastructure; this repository supplies the agent development workflow. Do not rewrite functioning scientific infrastructure merely to match one example.

Use the real execution platform. Some engines/tools need Linux, WSL, containers, or HPC facilities; a Windows host does not imply native support. Confirm prerequisites and resource authorization before promising a run. Keep instructions for PowerShell and POSIX shells distinct when engine commands or quoting differ.

Primary references to verify for the selected versions:

- [Nextflow documentation](https://www.nextflow.io/docs/latest/)
- [nf-core development documentation](https://nf-co.re/docs/developing-pipelines)
- [nf-core test scope](https://nf-co.re/docs/specifications/components/subworkflows/testing)
- [Snakemake reproducibility and distribution](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html)
