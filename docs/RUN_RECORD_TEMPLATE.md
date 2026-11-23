# Run record template

This is an unexecuted format. Copy it to a new file in `docs/runs/` only for an actual run. Record failed attempts too. Keep protected paths, identities, and artifacts in approved storage and use permitted opaque references here. Never include secrets.

## Identity and purpose

- **Run ID and UTC start/end:** <unique ID; actual times>
- **Operator and environment:** <person/agent; approved machine/platform/executor>
- **Purpose and validation checks:** <ledger IDs, validation check IDs, specific claims>
- **Task and attempt:** <recorded task ID, attempt ID, and charter revision from workflow state; do not duplicate the current-stage field>
- **Authorization:** <scope/design and compute-budget approval references>
- **Execution status:** <RUNNING / COMPLETED / FAILED / PARTIAL / CANCELLED; actual observed state>

## Exact provenance

- **Code revision:** <commit; branch; clean/dirty; saved diff/checksum if dirty; archive/checksum if not using Git>
- **Entrypoint and command:** <exact command with secrets removed; safe configuration reference>
- **Resolved parameters:** <all relevant values, configuration order, overrides, approved decision IDs>
- **Inputs:** <permitted identifiers, releases/locations, size and checksums where allowed; access restrictions>
- **References:** <database/build/annotation releases, compatibility, identifiers/checksums>
- **Software:** <engine/runtime and tool versions; container digests or resolved dependency locks>
- **Environment:** <OS/architecture, executor, hardware where material, environment lock/configuration artifact>
- **Randomness:** <seeds, nondeterministic steps, parallelism, reproducibility target>
- **Resources:** <requested and observed CPU/RAM/time/storage/cost, budget outcome>
- **Recovery/cache:** <fresh/resumed run; cache identity, provenance, retry details>

## Observations and artifacts

- **Exit status and stage outcomes:** <actual status; failures and partial products>
- **Logs and execution reports:** <permitted artifact references, retention, checksums where appropriate>
- **Outputs:** <artifact inventory, provenance and checksums/identifiers>
- **QC/exclusions:** <affected opaque identities/counts, thresholds, reasons, downstream consequences>

| Check ID | Predeclared expectation | Observed result | Pass/fail/unresolved | Evidence location |
| --- | --- | --- | --- | --- |
| <check> | <metric/tolerance from approved validation plan> | <actual value> | <outcome> | <artifact/log> |

## Interpretation and follow-up

- **Evidence:** <VERIFIED for specific executed observations; TRACED for inspection; NOT RUN for unexecuted checks>
- **Scientific claim status:** <SUPPORTED / UNSUPPORTED / NEEDS VALIDATION, or justified inapplicability>
- **Independent comparison:** <oracle/reviewer, metric agreement, differences, limits>
- **Limitations:** <missing checks, deviations, uncertainty, interpretation limits>
- **Findings:** <ledger IDs; do not silently fix or discard results>
- **Next required gate:** <review, owner triage, approved rerun, documentation, etc.>

Release approval is recorded separately. Completing this record does not authorize publication.
