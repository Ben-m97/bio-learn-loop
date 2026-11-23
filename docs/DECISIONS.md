# Decisions

**Status:** UNCONFIGURED — no project decisions have been approved.

The owner-approved scientific, engineering, and process rules that apply today. Write an entry when the owner approves it, and change its meaning only with owner approval. An owner's approval in chat is the decision; record its reference without requesting the same approval again.

The Choose stage obtains decisions; Document records them before Build. A stage transition does not approve an unresolved method or scope item. Learning notes, understanding acknowledgements, and reflections go in the ledger; authoritative stage transitions go only in WORKFLOW_STATE.json.

Initialise approves only the high-level PROJECT.md description; do not invent methodological decisions to complete it. Reopening the charter preserves existing entries. Review their compatibility, record dispositions in the ledger, and change or retire consequential rules only with owner approval.

IDs are permanent and never reused or renumbered. Replace a superseded entry by retiring its ID and identifying the replacement. Preserve details in version control. Record proposed choices in the ledger or brief, not as approved decisions.

## Format and use

The following fenced example is a format, not an actual decision:

```markdown
### D-001: <short imperative or statement of the rule>
- **Rule:** <what is required, including relevant parameters and thresholds>
- **Why:** <reason, methodological rationale, and limitations>
- **Sources:** <primary documentation/paper links or NOT APPLICABLE with a reason>
- **Approval:** <date and owner message/reference>
- **Code:** `path/to/source.py` `function_name`; `other/source.R` `function_name`
- **Since:** <version/date; add (in progress) while implementation differs>
```

- Keep one independently changeable decision per entry. Update it in place; working notes and evidence belong in the ledger, validation plan, or run records.
- **Code** paths are relative to the repository root. Optional symbols are identifiers in the cited file or directory, not arbitrary prose. Separate reference groups with semicolons. Use **Code:** None (process) for a process-only rule, or None (rule stack) for a stack.
- Every source location implementing a decision carries a relevant one-line comment with `(D-001)` using that source language's comment syntax. Keep the rationale here. The checker treats this parenthesized marker as reserved across scanned sources, including tests; do not use it for unrelated literal data.
- A scientific decision records the method, reference compatibility, thresholds, assumptions, and sources that matter. Changing a method/reference reopens affected validation and evidence. Do not change a threshold after inspecting results merely to make a test pass.
- Mechanical corrections such as a moved path do not change the approved rule, but report them. Never infer owner approval from a placeholder or an illustrative example.

## Rule stacks

Use a stack only when several related rules need a shared principle and explicit exceptions. It does not replace individual decisions or owner judgment.

```markdown
### D-010: <Area> rule stack
- **Rule:** Level 1: <base principle>. Level 2, but: <explicit limits>. Level 2, and: <additional requirements>. Protected: <other decision IDs>.
- **Why:** <owner's reason>
- **Approval:** <approval reference>
- **Code:** None (rule stack)
- **Since:** <version/date>

### D-011: <behavior already settled by the approved stack>
- **Passes:** D-010 1, 2
- **Code:** `path/to/source.py` `function_name`
- **Since:** <version/date>
```

Check each affected case against every level. A settled choice cites the existing stack; a choice the stack does not settle goes to the owner. A chosen entry uses the full format plus **Passes**. A stack conflict needs owner resolution. Recheck dependent decisions when a level changes.

## Active decisions

None yet. Add approved entries grouped by area here.

## Retired IDs

None yet. List each retired ID once as `- D-007: replaced by D-012, <reason>.` Do not put active entries in this section.
