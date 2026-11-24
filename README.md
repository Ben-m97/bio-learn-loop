# Codex bioinformatics workflow

A reusable template for learning while building scientifically justified, reproducible bioinformatics pipelines with Codex. Start once with **Stage 0 — Initialise** to articulate the project vision. Each small change then follows **Guide → Learn → Choose → Document → Build → Understand → Reflect**, followed by your **manual Commit**.

The template is analysis- and engine-neutral. Choose Nextflow, Snakemake, WDL, or an appropriate R/Python workflow for each project. It contains development instructions and validation tooling; biological pipeline code is added only after its scope and design are approved.

Adapted from [Copypaster3000/agent-built](https://github.com/Copypaster3000/agent-built), retaining its MIT licence and attribution. See [upstream provenance](UPSTREAM.md).

See [template verification](TEMPLATE_VALIDATION.md) for checks actually run and the remaining execution limits.

## Start a new project

1. Copy a fresh template into a new project directory. Keep AGENTS.md, docs/, scripts/, and .agents/skills/ together; do not copy another project's live state/approved charter as a new project.
2. Open that folder in Codex. Start a fresh chat after adding skills if they are not listed.
3. Authorize **Start Initialise** and describe what you would like to build in your own words. Codex discusses motivation, intended outcomes, learning goals, and known boundaries conversationally and drafts `docs/PROJECT.md`.
4. Approve the description, then explicitly move to Guide. Guide reads the charter before recommending one micro-task. You do not need architecture, tools, exact requirements, or methods to begin.
5. Authorize each transition. Codex writes the documents; you provide context, ask questions, and make informed choices.

Copy-ready starting prompt:

```text
Act as the PM and learning guide. Follow AGENTS.md and the release process.
Read the persistent workflow state, then Start Initialise for this new project.

My initial idea: <what you would like to build, in your own words>

Help me articulate the vision, motivation, eventual outcome, learning goals,
and known boundaries through conversation. Leave unknowns open; do not turn
this into a detailed architecture or implementation plan.
Only my explicit instruction authorizes transitions. I commit manually.
```

## Add the workflow to an existing project

Preserve existing instructions and project records. In an empty staging directory, obtain a copy of this template. Merge its `AGENTS.md` guidance into the existing root instructions, copy missing document templates into `docs/`, and merge the skill directories into `.agents/skills/`. Resolve filename or skill-name conflicts explicitly; do not overwrite existing project decisions or test infrastructure.

Also copy the public scripts/workflow_state.py helper, preserved internal _workflow_state_v1.py and _workflow_state_v2.py validators, and _reflection_assessment.py evidence checker, resolving existing-file conflicts. Preserve live PROJECT.md and WORKFLOW_STATE.json; never replace them with template data. Explicit migration preserves prior histories. The schema-2 snapshot stays intact inside schema 3, with approval/task/stage unchanged.

Establish the charter through Initialise, using existing documentation as context without inventing approval. Keep the technical brief for selected work; inspect existing decisions/code for compatibility. For version-1 workflow state, inspect it read-only and obtain explicit migration approval. Active legacy work stays suspended until initialization and compatibility review. Configure source paths for the checker and reuse suitable existing engine infrastructure.

## How development proceeds

| Stage | What Codex does | Your role |
| --- | --- | --- |
| 0. Initialise — once | Helps articulate vision, motivation, outcome, knowledge/learning, and boundaries; writes a short charter. | Approve the description, then authorize Guide. No architecture agreement is required. |
| Guide | Reads the approved charter and recommends one bounded next step serving its objectives and learning goals. | Discuss direction and authorize the next stage. |
| Learn | Explains concepts, methods, options, assumptions, tradeoffs, and a recommendation. | Ask questions and decide when you are ready to choose. |
| Choose | Presents the scope, design, validation expectations, and consequential decisions. | Make and approve informed choices; authorize moving to Document. |
| Document | Records your choices, scope, and validation plan in the project files. | Review if useful; authorize moving to Build when ready. |
| Build | Implements the approved slice, runs authorized checks, saves evidence, and arranges applicable reviews. | Approve any new consequential choices or challenged fix batches; authorize moving to Understand. |
| Understand | Walks through actual code, data flow, run/debug commands, tests, output meaning, and limits. | Ask questions and acknowledge readiness before authorizing Reflect. |
| Reflect | Tests essential concepts one question at a time, corrects misconceptions in chat, and checks follow-up answers before reflection/audit/handoff. | Explain/apply concepts in your own words; questions stay at the agreed conceptual level. Unresolved gaps keep Reflect incomplete. |
| Commit — manual | Hands back changed files, check results, limitations, and an optional proposed commit message. | Stage and commit yourself. Codex never makes the commit. |

Repeat this cycle for each small change; a pipeline release can contain several cycles. The PM also acts as your learning guide, the Lead owns the current approved implementation, and Workers handle bounded tasks. Engineering, scientific, and reproducibility reviewers work read-only. A different reviewer challenges findings before owner triage and fix approval. These safeguards sit inside the learning cycle; understanding a result does not establish its scientific validity.

Review is bounded: one initial review, focused reviews of approved fixes, and at most one convergence review when needed. A missing independent reviewer is an explicit open gate; the owner must arrange review or record a specific waiver. AI agreement alone is never scientific evidence.

## Persistent state and your control

`docs/PROJECT.md` is the short, stable project charter. `docs/PROJECT_BRIEF.md` holds technical details developed for selected work and may remain unconfigured during Initialise. Undecided directions are not task scope, an approved backlog, or implementation permission.

`docs/WORKFLOW_STATE.json` records initialization, charter approval/revision, active/suspended task, attempt IDs, stage/readiness, and history. It is the only stage authority. Codex reads it on resumption rather than inferring a stage from conversation, the ledger, tests, or Git. The template remains **NOT_STARTED**, with an **UNINITIALIZED** project.

READY does not advance a stage. Start Initialise enters Stage 0; Approve project description records the exact charter revision and leaves Initialise READY. A separate Move to Guide is required. Start Guide then selects one task/attempt there. Charter approval is not approval of architecture, methods, implementation, or budget. Encouragement, silence, and passing tests are never transitions. Codex records your actual instruction/reference; you need not edit JSON.

Finish cycle archives the completed attempt and returns to Guide with no active task. You stage and commit manually. No new task is automatically selected; a local commit never authorizes a release, push, or tag.

| Action | Recorded return point |
| --- | --- |
| Complete cycle | Guide, no active task |
| Restart task | Guide, same task/new attempt; old evidence retained |
| Abandon task | Guide, no active task; files/history retained |
| Entirely new project | Stage 0 in a fresh directory |
| Reopen Initialise | Stage 0, active task suspended and preserved |

Restart/abandon do not repeat Initialise or delete/revert files. Reopening requires explicit approval and preserves earlier charter revisions and decisions. After approval and return to Guide, suspended work waits for explicit restart or abandonment. Previous decisions/task assumptions need owner-reviewed compatibility dispositions before Build; nothing is silently discarded.

The state helper rejects skipped forward stages, stale revisions, missing/corrupt state, and overlapping writes. It records authorization provenance; it cannot itself authenticate a speaker or prove scientific approval. The agent must never fabricate authorization. Inspect the state without changing it with:

```text
python scripts/workflow_state.py --root . status
```

For example, once Guide is ready, you can explicitly instruct:

```text
Move to Learn
```

Codex must wait there until you authorize the next transition, even after it has finished explaining. See the helper's `--help` for its recording interface; normal use only requires your explicit chat instructions.

## What lives where

| Location | Purpose |
| --- | --- |
| `AGENTS.md` | Durable Codex instructions and verification commands |
| `docs/PROJECT.md` | Stable vision, motivation, outcome, learning goals, and boundaries |
| `docs/PROJECT_BRIEF.md` | Evolving technical design for selected work; not needed for Initialise |
| `docs/WORKFLOW_STATE.json` | Project approval, active/suspended tasks and attempts, stage/readiness, history |
| `docs/DECISIONS.md`, `docs/CODE_MAP.md` | Approved rules and the actual workflow |
| `docs/LEDGER.md`, `docs/BACKLOG.md` | Current scope/findings and approved future ideas |
| `docs/VALIDATION.md`, `docs/RUN_RECORD_TEMPLATE.md` | Planned evidence and reproducible run records |
| `docs/RELEASE_PROCESS.md`, `docs/GLOSSARY.md` | Guided stages, release safeguards, and shared terms |
| `.agents/skills/` | Start Lead, scientific review, reproducibility review, Reflect understanding, docs audit |
| `scripts/` | Public state helper and preserved internal v1 validator for explicit migration |
| `examples/` | Illustrative applications across analysis types and engines |

The scientific documents start **UNCONFIGURED**. Placeholder text and illustrative examples are not approved decisions, real runs, or completed validation. Actual run records are created under `docs/runs/` when work is executed.

## Check the template or a project

Python 3.10 or newer is sufficient; the checker and tests have no third-party runtime dependencies. Run the same commands from PowerShell or a POSIX shell:

```text
python .agents/skills/docs-audit/scripts/check_docs.py --root .
python -m unittest discover -s .agents/skills/docs-audit/tests -v
```

If your POSIX environment names Python 3 `python3`, substitute that executable. From another directory, pass the script's absolute path and the project's absolute root, quoting paths containing spaces.

The checker also accepts `--config <path>`; a relative configuration path is relative to the project root. By default it reads `docs/audit-config.json` if present. The configuration has two optional lists:

- `source_paths`: repository-relative files or directories to scan; the default is `["."]`.
- `exclude_paths`: excluded directory names, repository-relative paths, or glob patterns. A plain name matches a component at any depth. Supplying this list replaces the default exclusions.

Default exclusions keep generated data, references, results, environments, caches, template examples, documentation, and the skills themselves out of source scanning. Source scanning recognizes common workflow, R, Python, shell, and configuration text formats, including extensionless `Snakefile` files. A project's pipeline tests remain eligible for scanning.

Repository references in decisions use the **Code** field; code-map references use **Key files**. Put paths in backticks relative to the project root, followed by optional identifier names. Separate groups with semicolons. Inline local Markdown links in either document are checked relative to the document. Other backticks are treated as literal prose, so scientific terms are not mistaken for symbols. Symbol checks are lexical existence checks, not language-aware proof of a declaration or behavior.

The audit reports PASS/FAIL, warnings, charter configuration, and technical-brief configuration separately. An unfinished technical brief does not mean an initialized project must repeat Stage 0. Exit status is 0 without mechanical failures, 1 for audit/configuration failures, and 2 for CLI misuse. Review warnings explicitly; a passing audit does not establish approval, scientific validity, or release readiness.

## Evidence and reproducibility

Use **VERIFIED**, **TRACED**, and **NOT RUN** for the basis of a statement. Scientific claims separately use **SUPPORTED**, **UNSUPPORTED**, or **NEEDS VALIDATION**. Evidence must identify the specific claim, dataset, comparison, environment, command, result, and limitations.

Small public or synthetic tests exercise execution and failure handling. Scientific validation uses appropriate independent expectations, reference data, or justified invariants with predeclared tolerances. Reproducibility can mean agreement of specified scientific metrics rather than identical output bytes when tools are nondeterministic.

See [the release process](docs/RELEASE_PROCESS.md), [examples](examples/README.md), and [engine guidance](examples/engine-guidance.md). No workflow engine, data download, cloud resource, or biological analysis is required to validate this template.

## Reflect is a conceptual dialogue

Reflect checks the general concepts of the current task, not coding expertise. Codex asks a focused question, assesses the actual answer against the approved learning goal, points out mistakes or important omissions in chat, and gives a correction when needed. It then checks a follow-up answer or application scenario. A clarification buried in a handoff and an owner self-report do not establish understanding.

You can decline implementation detail without waiving conceptual questions. If essential gaps remain and you stop, Reflect stays incomplete; no normal waiver marks it passed. Documentation audit success checks documentation, not understanding. After concepts are demonstrated, the agent records reflection and the final handoff.

The reflect-understanding skill documents the per-attempt JSON assessment format. At Reflect, ready requires --assessment; finish independently checks its immutable receipt, task/attempt, charter/learning-goal bindings, and current candidate files. The helper checks mechanics, not the correctness of reasoning or identity of a chat speaker. A legacy READY record cannot close the gate. An explicit Reopen Reflect assessment withdraws it to ACTIVE, preserving the same task and all history. Git staging/commits remain yours.
