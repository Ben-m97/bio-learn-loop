# Upstream provenance

This template adapts [Copypaster3000/agent-built](https://github.com/Copypaster3000/agent-built) at commit [`21a367f4330a55aaf4229f5c1e007f35d820784a`](https://github.com/Copypaster3000/agent-built/tree/21a367f4330a55aaf4229f5c1e007f35d820784a), inspected on 2026-11-19.

Upstream author and copyright holder: Drake Wheeler. The upstream MIT notice is retained in `LICENSE`.

Adapted material includes the repository instructions, release process, decisions/code-map/ledger/glossary/backlog formats, Start Lead skill, Docs Audit skill, and documentation-checker behavior. The checker is reworked for engine-neutral source layouts and portable execution; relevant explanatory comments are retained or updated to describe the new behavior.

The adaptation uses root `AGENTS.md` and repository `.agents/skills/`, removes Claude-specific session/model assumptions, and adds scientific validation, reproducibility, and explicit evidence records. There is one canonical set of project documents and skills, rather than separate installable and example copies that can drift.

On 2026-11-22 the owner specified the primary learning cycle: Guide → Learn → Choose → Document → Build → Understand → Reflect, followed by the owner's manual Commit. The owner also required explicit persistent stage state and owner-only authorization of transitions. The adaptation now records stages in WORKFLOW_STATE.json with a deterministic recording helper; upstream review/release safeguards remain within the learning cycle. These stage requirements come from the owner and are not attributed to the upstream repository.

Implementation references:

- [Codex repository instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [nf-core testing specification](https://nf-co.re/docs/specifications/components/subworkflows/testing): distinguishes execution checks from meaningful scientific output.
- [Snakemake distribution and reproducibility](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html)

Engine-specific guidance is conditional. These sources do not constitute validation of any pipeline subsequently built with this template.

On 2026-11-23 the owner added Stage 0 — Initialise: a one-time conversational charter before the existing eight-stage development sequence, with manual Git commits unchanged. The adaptation now separates PROJECT.md purpose from task-level technical design and records initialization, charter revisions, task/attempt lifecycle, and suspended work in schema-2 workflow state. The original schema-1 transition rules/comments are retained in an internal validator for explicit migration; legacy histories are preserved rather than silently reinterpreted.
