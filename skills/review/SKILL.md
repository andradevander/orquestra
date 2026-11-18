---
name: review
description: Goldfish review of the current diff (feature or standalone change) — objective verification first, then clean-context reviewers, supervisor triage of each finding and rounds until convergence, writing review.md. With an active feature, it also checks whether the spec was fully met and generates convergence tasks.
argument-hint: "[diff base, e.g. main | HEAD~3] [extra focus, e.g. security]"
disable-model-invocation: true
---

# Review

Input: $ARGUMENTS. **Requires the subagent tool.** Without it, tell the user that a goldfish review is not possible and stop. Reviewing in your own context is not the same thing.

Finding triage and convergence follow **section 5 of the `orchestrate` skill**: **load the `orchestrate` skill with the Skill tool** before dispatching agents (only then are its reference files readable). In the plugin, the agent is `orquestra:goldfish-reviewer`.

## 0. Scope

- **Feature:** if `.orquestra/state.json` has a non-null `feature` **and** its `tasks.md` has marked tasks, it is a feature review (includes spec coverage). If the user pointed to something else, it is a standalone review.
- **Diff base**, in this order: user argument → `**Base:**` in the feature's `tasks.md` header → `HEAD` (uncommitted changes only).
- **Empty diff** (e.g. everything was already committed and the base fell back to `HEAD`): ask the user for the base (e.g. `main`). Do not review "nothing".
- **No git:** diff review is impossible. Ask for the list of changed files and pass the whole files to the reviewer.
- Files listed under `**Pre-existing changes:**` do not belong to this feature: exclude them from the diff or warn the reviewer.

## 1. Objective verification

Run build, lint, typecheck and tests (commands from the constitution). If anything fails, fix it or have it fixed **before** calling reviewers. If there are no commands, record "objective verification unavailable" in `review.md`.

## 2. Prepare the material

- Save `git diff <base>` (with `--stat`) to a scratchpad file, including new untracked files (`git add -N` or list them).
- Criteria: the spec's FRs/scenarios (path + IDs) or, for a standalone change, the user's request rewritten as criteria.
- UI with changed Tailwind classes: load the `responsive-ui` skill (Skill tool) and run its `desktop_guard.py` **with the base** (`desktop_guard.py <base> -- <paths>`) and attach the output.

## 3. Reviewers

- Default: **one** `goldfish-reviewer` (Sonnet).
- Large or risky change (auth, payment, data, migration, concurrency, more than ~15 files): `goldfish-reviewer` with `model: opus`, **or** two Sonnet reviewers in parallel with distinct focuses (e.g. "correctness and edge cases" and "security and regression").
- Brief: the goldfish-reviewer template from the `orchestrate` skill. **Never** include the conversation, your justification or findings from previous rounds.

## 4. Triage and convergence

Follow `orchestrate` §5: verify each finding in the code, decide FIX / CONTEST / ESCALATE / DECLINE, fix, verify again, and run a **new** reviewer if there was a P0/P1. Maximum of 3 rounds. Churn or limit exceeded: stop and ask.

## 5. Spec coverage (feature review only)

For each FR and acceptance scenario: met, partial or not met, with file:line. Claims of "done" are not evidence: check the code. Whatever is missing becomes a new task in `tasks.md`, in a `## Phase N: Convergence` section, **in the full format** (`- [ ] T0NN [S] <action> per FR-xxx (missing|partial|contradicts) — files: … — done: …`), only appending, without renumbering anything. If nothing is missing, do not touch `tasks.md`.

## 6. Record and close

- Write `review.md` in the feature folder (or `.orquestra/reviews/YYYY-MM-DD-<subject>.md` for a standalone change; create the folder if missing) from the `review.md` template (at the end of this file), without improvising the format. A reviewer that failed twice appears as **not run**, never as 0 findings.
- **Clean** feature review **with no convergence tasks**: change the spec's Status to **Implemented** and write `{"feature": null}` to `.orquestra/state.json`.
- In the chat: status (clean / with pending items), count by severity and decision, items for manual checking, path of `review.md`. If a pitfall that applies to the project came up, propose `/orquestra:note`. When closing a feature, suggest `/orquestra:consolidate`.

---

## Templates

### review.md

````markdown
# Review: <feature or change name>

**Date:** <YYYY-MM-DD> · **Diff base:** <commit/branch> · **Rounds:** <n>/3

## Objective Verification

| Command | Result |
|---|---|
| <build/lint/typecheck/tests> | passed / failed (<summary>) |

## Reviewers

| Reviewer | Model | Focus | Status | Findings (P0/P1/P2/P3) |
|---|---|---|---|---|
| goldfish-reviewer #1 | sonnet | correctness | completed / not run | 0/1/2/0 |

<!-- "not run" is different from "0 findings". Clean round = no open P0/P1. -->

## Findings

| ID | Sev. | Location | Summary | Decision | Evidence / action |
|---|---|---|---|---|---|
| R1-1 | P1 | file:line | <...> | FIX / CONTEST / ESCALATE / DECLINE | <what was done, or evidence for the contest> |

## Spec Coverage

| Requirement | Met? | Where |
|---|---|---|
| FR-001 | Yes / Partial / No | file:line |

## Pending and Manual Checks

- [ ] <item for the user to check>
````
