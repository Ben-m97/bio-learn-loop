# Template verification

Checked on 2026-11-19 in Windows PowerShell with Python 3.14.3. These results concern the template and its audit tooling. The scientific project documents remain UNCONFIGURED; no biological pipeline, scientific result, owner-approved pipeline release, or independent scientific review is represented here.

## Executed checks — VERIFIED

| Check | Observed result | Limits |
| --- | --- | --- |
| `python -m unittest discover -s .agents/skills/docs-audit/tests -v` | 40 tests passed | Isolated synthetic project fixtures plus distribution checks; Windows/Python 3.14.3 execution |
| `python .agents/skills/docs-audit/scripts/check_docs.py --root .` | PASS; 0 failures, 0 warnings; explicit UNCONFIGURED notice | Scaffold has no pipeline sources or active project decisions; fixture tests exercise populated projects |
| Bundled Codex `skill-creator/scripts/quick_validate.py` | All four skills passed | Frontmatter/instruction scaffold validation, not agent behavioral proof |
| Parse CI configuration using PyYAML | Expected triggers, read-only repository permission, two OS choices and two Python versions present | YAML structure checked; GitHub Actions execution NOT RUN |
| Parse the three Python files with `ast.parse(..., feature_version=(3, 10))` | Python 3.10 syntax accepted | Syntax compatibility only; local Python 3.10 runtime execution NOT RUN |

The bundled validator initially could not start because PyYAML was absent. PyYAML 6.0.3 was installed into a temporary target directory solely to execute that validator and inspect the CI YAML. It is not a template runtime dependency or a global Python installation.

The fixture tests cover projects without Git, working-directory independence, paths with spaces/Unicode, root workflow entrypoints, multiple source languages, explicit path/symbol checks, scientific prose, fenced examples, ID collisions/gaps/retirement/reservations, finding history and stale counters, process-only entries, rule stacks, configuration, exclusions, unreadable/binary sources, and invalid paths. Distribution checks cover required files, skill discovery metadata, local document links, and the scaffold audit.

## Gate walkthrough — TRACED

This is a tabletop review by the implementing agent against the written instructions. It is not an independently executed agent evaluation.

This subsection records the original 2026-11-19 review of the then-current ten-step release process. The current guided stages and persistent state were added and checked on 2026-11-22, as recorded below; the earlier step numbers are historical.

| Scenario | Required route in the implemented workflow | Inspected instructions |
| --- | --- | --- |
| New project starts without a configured brief | Inspect existing state, prepare brief/validation expectations, obtain scope and design approvals before pipeline implementation | [Repository instructions](AGENTS.md); [release steps 1–3](docs/RELEASE_PROCESS.md) |
| A smoke test passes but a biological claim lacks an appropriate comparator | Keep the observed execution claim bounded; classify the scientific claim as unsupported or needing validation; record a finding and keep the scientific gate open or explicitly limit the approved release and its claims | [Scientific Review](.agents/skills/scientific-review/SKILL.md); [validation plan](docs/VALIDATION.md); [release step 8](docs/RELEASE_PROCESS.md) |
| A reviewer reports a reference mismatch and another reviewer disputes it | Independently challenge reachability/evidence; retain confirmed, partial, or refuted disposition; present the batched result for owner triage and fix approval | [Finding gate](docs/RELEASE_PROCESS.md); [ledger format](docs/LEDGER.md) |
| Independent review cannot be arranged by the current Codex environment | Report the missing gate; owner arranges review or explicitly records a specific waiver with limits; self-review never becomes independent evidence | [Start Lead](.agents/skills/start-lead/SKILL.md); [roles and authorization](docs/RELEASE_PROCESS.md) |
| A method/reference changes after validation or documentation audit | Reopen affected evidence, reviews, and audits; preserve old run records; obtain approval for the consequential change and any new costly run | [Reproducibility Review](.agents/skills/reproducibility-review/SKILL.md); [Docs Audit](.agents/skills/docs-audit/SKILL.md); [release steps 8–10](docs/RELEASE_PROCESS.md) |
| A small scripted project is chosen instead of a workflow engine | Record the approved project-specific choice and apply the same contracts, evidence, reviews, and release gates | [Project brief](docs/PROJECT_BRIEF.md); [engine guidance](examples/engine-guidance.md) |

## Remaining execution limits — NOT RUN

- GitHub Actions, Linux runtime execution, and the Python 3.10 CI job. The [CI workflow](.github/workflows/template-checks.yml) is configured for Windows/Linux and Python 3.10/3.14 with pinned action revisions.
- Fresh-session Codex skill discovery and live multi-agent behavior. The skill files passed validation; a new project chat should discover repository skills through the normal Codex mechanism.
- Any biological pipeline, public-data download, cluster/cloud job, scientific validation, or publication. These are intentionally project-specific future work requiring the workflow's approvals and evidence.

The workspace was initially empty and has no Git metadata. No commit, tag, push, or publication was performed.

## Guided stages and persistent state update — 2026-11-22

This section records the historical schema-1 implementation. Stage 0, separate task/attempt identity, and the revised return-to-Guide semantics are recorded in the 2026-11-23 update below.

The owner requested Guide → Learn → Choose → Document → Build → Understand → Reflect, with guided explanations and pauses, and owner-managed manual Git commits. They also required the current stage to be explicitly persisted and every transition to require their authorization.

Implemented [authoritative state](docs/WORKFLOW_STATE.json), a [state recording helper](scripts/workflow_state.py), and aligned root instructions, project documents, skills, onboarding, and CI. The template's actual state remains **NOT_STARTED**, revision **0**; no biological cycle was started and no Git staging/commit was performed.

| Check | Observed result | Limits |
| --- | --- | --- |
| Full standard-library unittest suite | **57 tests passed** on Windows/Python 3.14.3 | Includes the original 40 tooling/distribution cases and 17 synthetic state-CLI cases; no real project transitions |
| Documentation checker | PASS; **0 failures, 0 warnings**; explicit UNCONFIGURED notice | One template helper source scanned; no biological pipeline or approved project decisions |
| State helper `status` against the actual scaffold | NOT_STARTED, revision 0, empty history | Read-only inspection; actual stage was not changed |
| Bundled skill validator | All four updated skills passed | PyYAML was isolated temporarily and removed; no project/global dependency added |
| Independent read-only agent source review and simulated responses | Five scenarios produced the intended hold/transition/handoff responses | TRACED behavioral dry-run, not execution of agent-controlled stage writes or scientific validation |

State tests exercise explicit start/move/finish authorization records, READY without advancement, rejected generic encouragement, required message references, no forward skipping, stale revisions, owner-authorized backtracking, resumption from state despite contrary ledger/conversation text, missing/corrupt state, conflicting snapshots, locks, empty evidence, new-cycle identity, and completion at Reflect without Git initialization. Tests construct their own initial state rather than borrowing a live project's stage.

The independent review identified that the original history validator did not replay every legal transition. The helper now replays the full history using the same transition rules, and an executed regression test rejects a structurally consistent history that illegally jumps from Guide to Build. The release process also now describes owner-directed recovery/reset when authoritative state is unavailable.

Authorization remains a recorded owner instruction/reference, not authentication of a speaker. The helper enforces state mechanics, but Codex must still verify actual owner permission, scope/design approval, understanding acknowledgement, and reflection. It must never fabricate those records. Manual edits can be rejected as inconsistent but are not cryptographically prevented.

Linux/Python 3.10 execution and GitHub Actions remain NOT RUN locally. CI includes a read-only persisted-state check. No biological analysis or external publication was performed.

## Stage 0 and project/task lifecycle update — 2026-11-23

Added [PROJECT.md](docs/PROJECT.md) as a short, conversationally developed charter. It separates project vision, motivation, intended outcome, knowledge/learning, and known boundaries from the technical brief. Initialise accepts unknown tools, architecture, requirements, and methods. Undecided directions remain unapproved ideas; description approval authorizes neither a technical design nor implementation.

The [schema-2 state helper](scripts/workflow_state.py) records initialization, approved charter revisions/snapshots, active/suspended tasks, distinct attempt identity, explicit transitions, and preserved attempt outcomes. Completion/abandonment return to Guide without an active task; restart preserves the task with a new attempt at Guide. Reopening Initialise suspends active work, and revised-purpose implementation requires owner-reviewed compatibility dispositions. All Git staging/commits remain manual.

The template's actual state is **schema 2, revision 0, NOT_STARTED / UNINITIALIZED**, without a task or charter approval. The previous empty scaffold was updated as template data; no real initialization, migration, task transition, scientific analysis, or Git mutation was performed.

| Executed check | Observed result | Limits |
| --- | --- | --- |
| Complete unittest suite | **71 tests passed** on Windows/Python 3.14.3 | Synthetic temporary projects; no real task transitions |
| Stage 0/lifecycle/migration cases | **30 tests passed**, included in the complete suite | Charter approval is tested as explicit recorded authorization, not speaker authentication or semantic approval of science |
| Documentation checker | PASS; **0 failures, 0 warnings** | Reports unconfigured charter and technical brief separately; mechanical checks are not scientific evidence |
| Bundled skill validator | All four updated skills passed | PyYAML was installed only in an isolated temporary target and removed afterwards |
| Python 3.10 syntax parsing | Accepted for six Python files | Python 3.10 runtime and Linux execution remain NOT RUN locally |
| Independent read-only source/behavioral walkthrough | Six initialization/redefinition/completion scenarios matched the intended owner-controlled behavior; no actionable findings established | Includes bounded synthetic in-memory checks reported by the reviewer; not a biological validation or full multi-agent CLI execution |

Tests cover vague visions without technical decisions, READY without charter approval, separate approval/transition, one-time initialization, content drift, task/attempt identity, completion/restart/abandonment, file/evidence preservation, exact suspended checkpoints, revised-charter compatibility gates, and explicit v1 migration. Legacy tests preserve original snapshots/history and hold active legacy work until initialization and review. Existing stale-revision, illegal-transition/history replay, locking, missing/corrupt-state, source-reference, and ID bookkeeping checks remain covered. Relevant original state-engine comments and semantics are retained in the [internal v1 validator](scripts/_workflow_state_v1.py).

README onboarding and stage/lifecycle tables, repository instructions, technical/project documents, glossary, examples, and skill handoffs were aligned. The technical brief may remain unconfigured during Initialise. Existing standalone checker layouts still use the older brief-status fallback when no charter is present.

Owner approval, understanding, scientific decisions, and compatibility meaning remain responsibilities of the agent/owner interaction. The helper enforces mechanics and records actual message references; it cannot independently authenticate the speaker or decide whether methodological reasoning is valid. CI is configured but has not been executed on GitHub in this task.


## Required Reflect conceptual assessment — 2026-11-24

The owner requested a conceptual teaching dialogue before the manual commit handoff, with corrections in chat and follow-up evidence rather than a passive reflection summary. Added the [Reflect skill](.agents/skills/reflect-understanding/SKILL.md), [assessment format](.agents/skills/reflect-understanding/references/assessment-format.md), and [schema-3 helper](scripts/workflow_state.py). Prior dated schema-1/2 reports above remain historical records.

The helper requires per-concept actual owner responses and chat-feedback references, unresolved-gap clearance, task/attempt/charter identity, and current charter/learning-goal/candidate file bindings. Reflect `ready --assessment` stores an immutable receipt; `finish` independently rechecks it and the approved charter. Corrections require a distinct owner follow-up. The helper validates evidence mechanics, not semantic correctness or speaker identity; truthful conceptual assessment and complete selection of essential goals remain agent responsibilities. A clean documentation audit cannot substitute.

Explicit migration retains complete original v1/v2 histories under their preserved rules. Existing completed cycles are not retroactively assessed. Legacy READY alone cannot finish. Owner-authorized `reopen-reflection` withdraws readiness without changing task/attempt or deleting old evidence. Git staging/commits remain manual. The actual reusable scaffold remains schema 3, revision 0, NOT_STARTED / UNINITIALIZED, with no charter approval or task.

| Executed check | Actual result | Limits |
| --- | --- | --- |
| `python -m unittest discover -s .agents/skills/docs-audit/tests -q` | **89 tests passed**, Windows / Python 3.14.3, 45.821 s | Synthetic temporary state projects; no biological validation |
| `python .agents/skills/docs-audit/scripts/check_docs.py --root .` | PASS, **0 failures / 0 warnings** | Unconfigured charter and unfinished technical brief reported separately |
| Bundled `quick_validate.py` with `python -X utf8` | **All five skills passed** | PyYAML 6.0.3 installed only in an isolated temporary target and removed; first default-encoding invocation failed on Unicode, corrected with UTF-8 mode |
| Python `ast.parse(..., feature_version=(3,10))` | Nine maintained Python files accepted | Syntax compatibility only; Linux/Python 3.10 runtime and GitHub Actions NOT RUN |
| Independent read-only source/behavioral walkthrough | Same-task reopening and generic-readiness rejection checked in memory; conceptual response scenarios met the protocol; no remaining actionable findings | TRACED source/behavioral evidence, not a real owner assessment |

The reviewer found that a rehashed unapproved charter could initially pass Reflect readiness (finish was already blocked). The Reflect ready CLI now checks the approved charter first; a regression test rejects rebinding unapproved text. Additional tests cover incomplete/unassessed concepts, correction without follow-up, reused owner references, wrong identities, missing actual answers/feedback, stale goals/candidate files, modified receipt artifacts, legacy migration, preserved historical completion, and same-task reopening. Existing locking, stale revision, full history replay, initialization and manual-Git cases remain covered. The copied project's earlier isolated-scaffold test fix is preserved/backported.

The approved RNA-seq rollout is recorded separately in that project's docs/maintenance/2026-11-24-reflect-gate/record.md. It preserves scientific implementation, approved goals/charter, fixtures, dependencies and prior evidence, and prepares an unassessed record. No new scientific claim, code quiz, Git mutation, external release or compute job is part of this maintenance.
