# Code map

**Status:** UNCONFIGURED — no biological pipeline is implemented by this template.

Describe the actual source and workflow, not the proposed design. Update affected sections from the final release candidate and audit them before release. Leave unknown facts unset. A factual correction needs no new approval unless it reveals a change in approved behavior.

Maintain the factual map as Build changes the code, use it for the owner's Understand walkthrough, and audit it during Reflect and final release checks. It does not record the current learning-cycle stage; read WORKFLOW_STATE.json for that.

## Section format

Create one concise section per stage or subsystem. Source references belong under **Key files**, with repository-relative paths and optional identifiers in backticks. A semicolon starts another reference group. Other backticks are literal prose. Local Markdown links are checked relative to this document, so they can also cite source locations in a flow description.

```markdown
## <Stage or subsystem>
**Does:** <purpose and boundaries>
**Flow:**
1. <actual transformation and dependency>
2. <how outputs reach the next stage>
**Key files:**
- `path/to/source.py` `function_name`; `path/to/config.yaml`
**Inputs:** <formats, metadata, units, identity and reference requirements>
**Outputs:** <runtime products and their consumers; these need not exist in Git>
**Must hold:** <invariants, relevant approved decision IDs, failure/QC rules>
**Debug from:** <observed message or symptom and where to investigate>
```

Runtime outputs are not committed source references. Do not cite an uncreated result under **Key files**. The checker verifies lexical symbol presence; a human reviewer checks that the symbol, flow, and invariant mean what this document says.

## Implemented workflow

None yet. The template's own audit tool is documented in the README and its Docs Audit skill; it is not a biological pipeline stage.
