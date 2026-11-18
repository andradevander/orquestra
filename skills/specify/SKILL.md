---
name: specify
description: Turns a feature request into spec.md (the what and why, without the how) with prioritized stories, Given/When/Then scenarios, FR-xxx requirements and success criteria, and tests the spec with a goldfish reader. First step of the feature workflow.
argument-hint: "<feature description>"
disable-model-invocation: true
---

# Specify

Request: $ARGUMENTS

If the request is empty, ask what the feature is and stop. If `.orquestra/` does not exist, suggest `/orquestra:init` and stop.

## Steps

1. **Minimal context.** Read `.orquestra/constitution.md` and the items in `.orquestra/memory/INDEX.md` related to the subject. If you need to understand what already exists in the code so you do not specify something that already exists, dispatch a `scout`. Do not read the code yourself in this phase.

2. **Create the feature folder.** Next free number in `.orquestra/specs/` (3 digits) + a short name of 2–4 words in kebab-case, in verb-noun form (e.g., `004-export-sales-csv`). Write `{"feature": ".orquestra/specs/004-export-sales-csv"}` to `.orquestra/state.json`.

3. **Write `spec.md`** from the `spec.md` template (at the end of this file), following its structure. Rules:
   - **The what and why, never the how.** No stack, no API, no file names. The reader is someone from product.
   - **Independent** stories: each one, on its own, delivers value and can be tested. P1 is the MVP.
   - Each acceptance scenario is observable: **Given / When / Then**.
   - Requirements `FR-001…` with MUST. Success criteria `SC-001…` measurable and technology-free.
   - **Informed guess instead of a question.** Use `[NEEDS CLARIFICATION: question]` only when the doubt changes scope, security or UX and there is no reasonable default. **At most 3.** The rest goes into Assumptions.
   - Remove sections that do not apply (including Clarifications/Deferred, which belong to `/clarify`).

4. **Test with fresh eyes.** Dispatch `goldfish-reader` with the path to `spec.md` and nothing else.
   - Compare its paraphrase with your intent. If it diverges, the text is leading to the wrong reading: rewrite that part.
   - For each BLOCKER or MAJOR: fix the text, or turn it into `[NEEDS CLARIFICATION]` if it is the user's decision (respecting the limit of 3).
   - Do not add text just to please the reviewer. Fix what would cause an error for whoever executes.
   - If there was a BLOCKER, run **one** new reader after fixing. **At most 2 rounds**; whatever remains goes into the delivery as a pending item.

5. **Deliver** in a few lines: the file path, the stories (title + priority), the assumptions you made and the open questions. The next step is `/orquestra:clarify` if there are markers, otherwise `/orquestra:plan`.

## Done when

- [ ] `spec.md` without implementation details, Status: Draft
- [ ] Every story has an independent test and Given/When/Then scenarios
- [ ] Every FR is testable; every SC is measurable
- [ ] At most 3 `[NEEDS CLARIFICATION]`
- [ ] Reviewed by `goldfish-reader`, with no open BLOCKER (or a declared pending item)

---

## Templates

### spec.md

````markdown
# Spec: <feature name>

**ID:** <NNN-short-name> · **Status:** Draft · **Created:** <YYYY-MM-DD>
**Original request:** "<user's text, verbatim>"

<!-- Status: Draft (/specify) → Clarified (/clarify) → Approved (/plan, when the user approves the plan) → Implemented (/review clean).
Rules: describe the WHAT and WHY, never the HOW (no stack, no API, no code structure).
Remove sections that do not apply (do not leave "N/A"). At most 3 markers [NEEDS CLARIFICATION: question]; the rest becomes an informed guess in Assumptions. -->

## User Stories

### User Story 1: <title> (Priority: P1)
<journey in plain language>

**Why this priority:** <value>
**Independent test:** <how to prove this story alone delivers value>

**Acceptance scenarios:**
1. **Given** <state>, **when** <action>, **then** <observable result>
2. **Given** ..., **when** ..., **then** ...

### User Story 2: <title> (Priority: P2)
...

## Edge Cases

- What happens when <boundary/error condition>?

## Functional Requirements

- **FR-001**: The system MUST <capability>
- **FR-002**: The user MUST be able to <action>
- **FR-003**: The system MUST <...> [NEEDS CLARIFICATION: <specific question>]

## Entities (if there is data)

- **<Entity>**: what it represents, main attributes (no database types)

## Success Criteria

<!-- Measurable, from the user/business point of view, technology-free. -->
- **SC-001**: <e.g., "user completes sign-up in under 2 minutes">

## Assumptions

- <informed guess that replaced a low-impact doubt>

## Out of Scope

- <what will explicitly not be done in this feature>

## Clarifications

<!-- Filled in by /orquestra:clarify. Remove if empty. -->
### Session <YYYY-MM-DD>
- Q: <question> → A: <answer>

## Deferred

<!-- High-impact doubts that remained unanswered. Remove if empty. -->
````
