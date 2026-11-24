---
name: docs-audit
description: Audit a bioinformatics project's decisions and code map using the read-only checker and a review of documentation coverage and meaning. Use during Reflect, final release checks, or a requested audit; it does not advance workflow stages or establish scientific validity.
---

# Docs audit

Read root `AGENTS.md`, the Reflect stage, and final record/audit safeguard in `docs/RELEASE_PROCESS.md`. Audit the exact candidate; any later relevant code/method/reference change reopens affected audits and evidence. Within a pipeline cycle, read `docs/WORKFLOW_STATE.json` rather than inferring the stage. An ad hoc audit does not authorize a transition, and a clean audit must not advance the stage or cause a Git commit.

## Mechanical check

From the project root:

```text
python .agents/skills/docs-audit/scripts/check_docs.py --root .
```

The checker uses Python 3.10+ and the standard library. It accepts an absolute root from another working directory and optional `--config`; relative config paths are relative to that root. The default config is `docs/audit-config.json` if present. Configure `source_paths` and `exclude_paths` there; the README explains the scan and exclusions. Do not scan large/raw/generated data as source.

It checks source references in decision **Code** and code-map **Key files** fields, inline local Markdown links in those two documents, lexical optional symbols, active/retired/reserved decision IDs, parenthesized decision markers in source, and ledger counters. Arbitrary scientific terms in other backticks are prose. Decision markers are reserved even inside source/test string literals. It handles root entrypoints, workflow/R/Python/shell/configuration text, paths with spaces, and projects without Git metadata.

Exit 1 means mechanical/configuration failure, 2 CLI misuse. Fix mechanical errors within the already-authorized task, and report them; a finding that changes approved behavior or needs a code fix goes through challenge/owner triage. Judge each warning explicitly. A missing code tag or in-progress decision may prevent release even though warnings do not change the tool's exit status. The Lead runs the checker before the Reflect handoff and final release audit; the PM runs it on the candidate too. Neither run authorizes a stage transition.

A new unconfigured PROJECT.md is a charter scaffold. An UNCONFIGURED technical brief is separate and may be valid during/after Initialise until task design develops. The checker reports them separately, retaining fallback support for older standalone audit layouts. Only workflow state records actual charter approval. A passing checker never establishes approval, complete documentation, scientific validity, or release readiness. When auditing charter changes, check preserved prior revisions, suspended work, and owner-reviewed compatibility dispositions.

## Human/agent review for coverage and meaning

- Establish the previous release and actual candidate, using available version-control diffs or an explicit supplied change inventory/archive when Git is unavailable. Include uncommitted changes in the identity; do not pretend HEAD describes them.
- For every changed source, identify its code-map stage and governing decisions, and confirm the records changed or explain why no change was needed. The script cannot detect missing documentation.
- Check each affected rule against actual behavior, approved owner wording, sources, parameters, implementation places/tags, and Since status. Rule stacks and their dependent decisions must remain consistent. A process-only Code field cannot hide an implemented rule.
- Check flows, contracts, units, reference compatibility, invariants, QC/error behavior, runtime outputs, and debug pointers. Verify record/evidence links and distinguish proposed, inspected, and executed work.
- Check validation and run provenance for the same candidate. Changing a method, reference, configuration, or scientific claim may reopen earlier gates.
- Check glossary meaning against owner-approved terminology. Mechanical wording/path corrections need no new scientific approval; consequential meaning changes do.

## Report

Give the candidate identity, checker command/result and warning dispositions, inspected coverage, and substantive mismatches/missing evidence. Cite file/line or artifacts. Return findings through the challenge/triage gate; report owner decisions with recommendations. Say “documentation audit clean” only when both mechanical and semantic reviews are clean, and state that this is not scientific validation or release approval.

## Reflect assessment coverage

When auditing a final Reflect handoff, verify that it links the current structured conceptual assessment and faithfully distinguishes owner responses from agent feedback. Corrections must have occurred in chat and, when needed, a later owner response must demonstrate the correction. A code-detail preference is not a waiver. Report missing or unresolved assessment evidence; a clean documentation audit does not mark Reflect READY or authorize Finish cycle. Preserve historical handoffs/audits and append corrections rather than rewriting old owner statements.
