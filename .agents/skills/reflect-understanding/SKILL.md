---
name: reflect-understanding
description: Conduct the required conceptual understanding dialogue in the recorded Reflect stage before manual handoff. Probe approved learning goals, correct misconceptions in chat, and verify follow-up answers; do not use for code quizzes or silently advance stages.
---

# Reflect understanding

Read AGENTS.md, the recorded state, the approved task learning goals, and the actual implementation/usage/claim limits. Use only the active task and attempt. An ad hoc explanation does not authorize entering Reflect. Within Reflect, this assessment is required, not an optional exercise.

## Establish the conceptual scope

Identify a small, task-proportionate set of essential concepts from the approved goals and what was built. Usually two to four concepts are enough. Cover the purpose, relevant data model, outcome meaning, and important limits where applicable. Record a plain-language success criterion for each before assessing the answer. Do not turn every undocumented detail into a required concept or introduce untaught requirements. Assess general concepts; coding syntax, memorized exit-code values, package versions, test counts, and implementation mastery are not required unless the owner explicitly chose those learning goals.

## Dialogue, one question at a time

1. Ask a focused question requiring explanation in the owner's words or application to a small scenario. A generic “what did you learn?” may open the conversation but cannot establish readiness.
2. Evaluate the actual response against the criterion. Say in chat what is correct, what is mistaken, and what important concept is still unassessed. An omission is not proof of ignorance; ask about it. Do not require details the question never elicited.
3. If needed, explain the correction in plain language **in chat**, then ask a targeted follow-up or a new application scenario. Wait for the owner's response. Your correction, an “OK,” or an expression of confidence does not itself demonstrate the concept.
4. Record the actual question, owner answer/reference, assessment, feedback/reference, gaps, and later answer that resolves them. Never invent dialogue, mastery, or a learning outcome from your own explanation.
5. Continue adaptively until essential concepts are demonstrated. Revisit only unresolved concepts; do not mechanically repeat correct answers or demand an exhaustive examination.

“I do not want more code detail” changes the level of discussion, not the conceptual gate. Respect that preference while continuing the conceptual dialogue. If the owner wants to stop, pause Reflect ACTIVE with gaps recorded. There is no normal waiver that marks unassessed or incorrect understanding complete. Do not pressure the owner, proceed to handoff, or infer Finish cycle.

For a structural input check, useful conceptual probes include why input validation precedes downstream work and what a structurally accepted file does or does not establish. Use the task's actual approved contract; do not claim broader scientific quality merely because execution succeeded.

## Evidence and handoff

Maintain a per-attempt JSON record under docs/reflections using [the assessment format](references/assessment-format.md). Bind its charter, task learning goals, and actual reviewed implementation files. Keep chat feedback separate from private assessment notes. Draft assessments may remain NOT_ASSESSED/PARTIAL with unresolved gaps; they must not pass readiness validation.

Only after the dialogue succeeds: summarize what the owner demonstrated, discuss learning/uncertainties, finalize the handoff and documentation audit, and call the state helper ready with the assessment file. The helper validates structured evidence and file identity, not conceptual truth or speaker identity. Do not simply change statuses or rehash changed files to force a pass.

Readiness is not a transition. Wait for the owner's explicit Finish cycle. The owner commits manually. A copied project with legacy Reflect READY must explicitly migrate and reopen its assessment, preserving its prior handoff and history; do not restart the task, silently reset stages, or rewrite past owner statements.
