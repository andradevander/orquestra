---
name: clarify
description: Resolves ambiguities in the current spec with at most 5 questions, one at a time, each with a recommended option, writing each answer into the spec right away. Run after /orquestra:specify and before /orquestra:plan.
argument-hint: "[feature, if not the current one]"
disable-model-invocation: true
---

# Clarify

**Feature:** the argument ($ARGUMENTS), otherwise the `feature` field of `.orquestra/state.json`. If it is `null` or does not exist, list the folders in `.orquestra/specs/` and ask which one. If there is no `spec.md`, tell the user to run `/orquestra:specify` and stop.

## 1. Build the queue (without showing it to the user)

Read `spec.md`. Gather the candidates:
- the `[NEEDS CLARIFICATION]` markers;
- gaps that change architecture, tests, UX or security: scope, data, error flow, permissions, integrations, limits, ambiguous terms, adjectives without a metric.

Order by **impact × uncertainty**. Cut at **5**. Do not ask anything about stack, how to implement, or task breakdown.

## 2. Ask one at a time

Show **exactly one** question per message and never reveal the next ones:

```
**Question:** <direct question>? (FR-00X)
<1 sentence: why this matters>

**Recommended:** Option B — <reason in 1 line>

| Option | Description |
|---|---|
| A | ... |
| B | ... |
| C | ... |

Reply with the letter, "yes" to accept the recommended one, or with your own answer.
```

For a short, open answer, replace the table with `**Suggestion:** <up to 5 words>`. If the AskUserQuestion tool is available, you may use it with the same options (recommended first).

## 3. Write each answer right away

After **each** answer, before the next question:
1. In `spec.md`, in section `## Clarifications` → `### Session YYYY-MM-DD`, append `- Q: … → A: …`.
2. Apply the answer to the right section (FR, scenario, edge case, SC, entity). Remove the marker and replace the contradictory text. Keep a single term for each concept.
3. Save the file.

## 4. Stop

Stop when the user says that is enough, when you reach 5 questions, or when no relevant ambiguity remains. High-impact items that were left out go into the `## Deferred` section. Change the spec's Status to **Clarified**.

Deliver: how many questions were asked, the sections changed and what was deferred. Next step: `/orquestra:plan`.
