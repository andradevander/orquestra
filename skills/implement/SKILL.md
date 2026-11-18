---
name: implement
description: Executes the current feature's tasks.md phase by phase — the supervisor dispatches each task to the designated agent ([H] Haiku, [S] implementer or tester/Sonnet, [O] itself), runs the [P] tasks in parallel, verifies each delivery, marks [X] and stops at checkpoints.
argument-hint: "[feature] [phase or IDs, e.g. 'phase 2' or 'T004-T007']"
disable-model-invocation: true
---

# Implement

**Feature:** the argument ($ARGUMENTS), otherwise the `feature` field of `.orquestra/state.json`. If it is `null` or missing, list `.orquestra/specs/` and ask which one. No phase given = the next one with open tasks. Requires `tasks.md` and `plan.md`.

For briefs and validation, follow the `orchestrate` skill: **load the `orchestrate` skill with the Skill tool** before dispatching agents (only then are its reference files readable). In the plugin, the agents are named `orquestra:scout`, `orquestra:implementer`, `orquestra:tester`, etc.

## Before starting

1. Read `tasks.md`, `plan.md`, the constitution and the spec sections that the phase's tasks cite.
2. **Record the base in the `tasks.md` header** (if still empty): `**Base:** <git rev-parse HEAD>` and `**Pre-existing changes:** <git status --short>`. This is how `/orquestra:review`, even in another session, knows what to review and what is not yours. Without git: write `**Base:** no git` and keep the list of touched files at the end of `tasks.md`.
3. If the plan cites a domain skill (e.g. `responsive-ui`), load it with the Skill tool: its checks (e.g. `desktop_guard.py`) go into the checkpoints.
4. Verification commands: those in the constitution. If they are missing or marked `TODO`, use the cheapest available one (e.g. typecheck) or declare "objective verification unavailable" and carry that warning through the checkpoints.
5. If the phase depends on another one that has open tasks, stop and warn.

## Loop per phase

1. **Build the batches:** the phase's `[P]` tasks with no pending dependency form a parallel batch. The rest follow in order.
2. **Dispatch the batch in a single message**, one Agent call per task:
   - `[S]` code → `implementer`; `[S]` test → `tester`;
   - `[H]` locate → `scout`; `[H]` mechanical edit → `implementer` with `model: haiku`;
   - `[O]` → yourself, after the batch finishes (usually integration or a shared file).
   - Brief: generic template from the `orchestrate` skill (`references/briefing.md`), with ID, files, reference pattern, "done" criterion and verification command.
3. **As each result comes back:**

   | Return | What it means | Action |
   |---|---|---|
   | implementer `DONE` | says it finished | Check the "done" criterion (run the verification or read the snippet); only then mark `[X]` |
   | tester `PASSED` | tests green | Mark `[X]` |
   | tester `FAILED` on a task whose "done" is "fails for the right reason" (test before code) | success | Check the reason for the failure; mark `[X]` |
   | tester `FAILED` in any other situation | bug | Send the failure to the `implementer` of the corresponding task |
   | tester `NO_INFRA` | project has no tests in this layer | Keep the manual script for the checkpoint; mark `[X]` with note "(manual)" |
   | `PARTIAL` / `BLOCKED` | something is missing | Resolve the blocker (decision, shared file) and redispatch **with the corrected brief**, or do it yourself |

   Two failures on the same task → raise the model or do it yourself. Assumptions declared by the worker → check that they match the spec.
4. **A failure in a sequential task** interrupts the phase. In a `[P]` batch, the others continue and the one that failed is handled at the end of the batch.
5. **Phase checkpoint:** run the objective verification and the story's independent test (or show the manual script). Show the user one line per task and the result. Move on to the next phase only if the checkpoint passed. If the user asked for continuous execution, proceed without asking, but stop on failure.

## Rules

- **Scope is `tasks.md`.** New work discovered along the way becomes a new task at the end of the current phase, **in the full format** (`- [ ] T0NN [S] … — files: … — done: … (discovered)`), and not a "while I'm here".
- Never weaken or delete tests to make them pass.
- Stop and ask if a fix would require changing the spec or violating the constitution.
- No commit, unless the user asks.

## End

When all phases are `[X]`: summary (tasks done, final verification, manual items, relevant assumptions, discovered tasks). Next step: `/orquestra:review`.
