---
name: plan
description: Generates plan.md (technical approach, files, contracts, constitution check) and tasks.md (small tasks with exact file, parallelism marker [P] and executor marker [H]/[S]/[O]) for the current spec, and checks spec↔plan↔tasks consistency before implementing.
argument-hint: "[feature, if not the current one] [technical notes]"
disable-model-invocation: true
---

# Plan

**Feature:** the argument ($ARGUMENTS), otherwise the `feature` field of `.orquestra/state.json`. If it is `null` or does not exist, list `.orquestra/specs/` and ask which one. Requires `spec.md`. If there are still `[NEEDS CLARIFICATION]` markers, warn that it will cause rework and ask whether to proceed or run `/orquestra:clarify`.

Templates: `plan.md` and `tasks.md`, at the end of this file. Follow their structure; do not improvise the format.

## 1. Understand the code (cheap)

Dispatch `scout`s **in parallel**, one per question, for example:
- "where is something similar to <feature> implemented? patterns to follow"
- "which files handle <entity/route/screen>?"
- "how are the <layer> tests written?"

If the feature touches an area with a domain skill (e.g., UI/layout → `responsive-ui`), load it with the Skill tool and include its rules and checks in the plan and in the "done" criteria of the tasks.

Read **yourself** only the core files the scouts point to. This is where the supervisor's model is worth the cost.

## 2. Write `plan.md`

The minimum for the tasks to be executable without asking questions: files, contracts, data, decisions with rejected alternatives.

**Constitution gate:** fill in the check table. A violation without justification = stop and adjust the design. A justified violation goes into "Justified Complexity", with the simpler alternative and the reason for rejecting it. Always prefer the design that does not need the justification.

For a small feature, a short `plan.md` is enough. Do not create extra documents.

## 3. Write `tasks.md`

Each line follows the template format **exactly**:

```
- [ ] T005 [P] [S] [US1] Imperative description — files: a.ts, b.ts — done: <criterion> (depends: T003)
```

- **Size:** each task fits in one agent session with only spec + plan + the cited files. If you need "and also…", split it.
- **[P]** only if the files do not overlap with any other `[P]` in the same phase and there is no pending dependency. **Same file = sequential.**
- **Who executes:**
  - `[H]` mechanical: locating (goes to `scout`) or mechanical editing, such as renaming, moving or generating boilerplate from an example (goes to `implementer` with `model: haiku`);
  - `[S]` ordinary implementation or test (`implementer` / `tester`);
  - `[O]` decision, shared file, integration between parts, or something that requires the full context (supervisor).
- Phases: Foundation (blocking) → one phase per story, in priority order, each with a **Checkpoint** → Polish (only if there is cross-cutting work).
- Tests before code when the constitution requires it or the business rule is critical.
- Do not create a "goldfish review" task: that is `/orquestra:review`.

## 4. Consistency check (read-only)

Do it yourself, quickly, and show only what fails:
- every FR and every acceptance scenario has at least one task (and every task serves some FR or story);
- same terms across spec, plan and tasks;
- no conflict with the constitution (conflict = CRITICAL; adjust the artifacts, not the rule);
- `[P]` markings without a shared file; every line in the format.

For a large feature (more than ~15 tasks or more than 3 stories), also dispatch `goldfish-reader` on `tasks.md` and handle BLOCKER/MAJOR. **At most 2 rounds** of reader; whatever remains goes as a pending item in the delivery.

## 5. Deliver

Show the technical summary (2–4 lines), the task count per phase (how many `[P]`, how many `[H]/[S]/[O]`), decisions the user must validate and problems from the check. **Ask for approval of the plan** before `/orquestra:implement` if there is an architecture decision or a relevant trade-off. Once approved, change the spec's Status to **Approved**.

---

## Templates

### plan.md

````markdown
# Plan: <feature name>

**Spec:** ./spec.md · **Date:** <YYYY-MM-DD>

## Technical Summary

<2–4 sentences: the chosen approach and why>

## Codebase Context

<!-- Scout findings: what already exists and will be reused or changed. Always file:line. -->
- <file:line> — <what it is / how it will be used>

## Constitution Check

<!-- GATE: must pass before generating tasks. One line per relevant principle. -->
| Principle | Complies? | Note |
|---|---|---|
| <1. name> | Yes / No (justified below) | |

## Design

<!-- Only what is needed for the tasks to be executable without asking questions: modules/files, contracts (signatures, payloads),
data model, flow. Prefer lists and tables over prose. -->

### Files

| File | Action | Responsibility |
|---|---|---|
| <path> | create / change | <...> |

### Contracts

<signatures, routes, payloads, events>

### Data

<entities, fields, migrations>

## Risks and Decisions

- **Decision:** <what> · **Rejected alternatives:** <which and why>
- **Risk:** <what> · **Mitigation:** <how>

## Justified Complexity

<!-- Fill in only if some constitution principle was violated. -->
| Violation | Why needed | Simpler alternative rejected because |
|---|---|---|

## Verification Strategy

- Objective: <build/lint/test commands>
- New tests: <which acceptance scenarios become tests>
- Manual: <what to check in the browser/environment, if applicable>
````

### tasks.md

````markdown
# Tasks: <feature name>

**Plan:** ./plan.md · **Spec:** ./spec.md
**Base:** <filled in by /orquestra:implement: HEAD sha at the start> · **Pre-existing changes:** <files modified before starting, or "none">

<!-- MANDATORY format for every task line, including those added later (discovered, convergence):
- [ ] T001 [P] [S] [US1] Imperative description — files: path/a.ts, path/b.ts — done: <criterion> (depends: T000)

[P]          = parallelizable: different files from all other [P] in the same phase AND no pending dependency.
[H]/[S]/[O]  = who executes:
               H = mechanical and cheap: locating (scout) or mechanical editing (implementer with model: haiku);
               S = implementer (code) or tester (tests), Sonnet;
               O = supervisor (decision, shared file, integration between parts).
[US1]        = user story from the spec (only in the story phases).
Rules: IDs in execution order; every task has exact file(s); same file = sequential;
each task fits in one agent session with no context beyond spec + plan + cited files.
Mark [X] only after verified. Goldfish review is NOT a task here: it is /orquestra:review, afterwards. -->

## Phase 1: Foundation

<!-- Prerequisites that block all stories. No story starts before this phase is finished. Remove if there are none. -->
- [ ] T001 [O] <...> — files: <...> — done: <...>

## Phase 2: User Story 1 (P1) — <title>

**Goal:** <...>
**Independent test:** <...>

- [ ] T002 [P] [S] [US1] <test for scenario 1> — files: <...> — done: test exists and fails for the right reason
- [ ] T003 [P] [S] [US1] <...> — files: <...> — done: <...>
- [ ] T004 [S] [US1] <...> — files: <...> — done: <...> (depends: T003)

**Checkpoint:** <verification that proves User Story 1 on its own>

## Phase 3: User Story 2 (P2) — <title>

...

## Final Phase: Polish

<!-- Only code/documentation work that cuts across stories (cleanup, i18n, docs). Remove if there is none. -->
- [ ] T0NN [S] <...> — files: <...> — done: <...>

## Dependencies

<!-- Only what is not obvious from the phase order. -->
````
