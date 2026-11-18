# Getting started

From zero to your first delivered feature. It takes about 15 minutes of reading, and you do not need to know the theory to begin.

## 1. Install

```bash
claude plugin marketplace add andradevander/orquestra
claude plugin install orquestra@orquestra
```

Check: open Claude Code and type `/orquestra:`. The list of commands should appear.

Recommended: allow reading the plugin folder to avoid permission prompts (see [Troubleshooting](troubleshooting.md#recommended-permissions)).

## 2. Set up the project (once)

Inside your project's repository:

```
/orquestra:init
```

What happens:

1. Claude discovers the stack and the build, lint, typecheck, and test commands.
2. It creates the `.orquestra/` folder:
   - `constitution.md`: the project's non-negotiable rules and the verification commands;
   - `memory/INDEX.md`: the memory index, loaded in every session;
   - `specs/` and `reviews/`: where features and reviews live;
   - `state.json`: the feature **you** are working on (goes into `.gitignore`).
3. It adds a line to `CLAUDE.md` that imports the memory index. It shows the snippet before writing.
4. It asks whether you want to adjust the principles it proposed.

**Review the constitution carefully.** It is short (up to ~60 lines) and worth it: it is the yardstick the reviewers use. A good principle is verifiable in a diff ("every new business rule MUST have a test"), not a vague wish ("clean code").

Commit `.orquestra/`. Memory and specs belong to the team.

## 3. First small change

For a bug, tweak, or small feature (up to ~5 production files):

```
/orquestra:quick the "Save" button on the signup form disappears on mobile
```

What to expect:

1. **Critique (edits nothing):** up to 6 lines saying what it understood, where it will make changes, and the assumptions. If the request is bigger than it looks, it recommends the feature workflow and stops.
2. **Checklist:** 2 to 8 items, with file and done criterion. It only asks for an "ok" if there is an unverified assumption or a decision for you.
3. **Execution:** does it directly if it is 1-2 files, or delegates to subagents in parallel. Runs the project's verification.
4. **Clean-context review:** a reviewer who did not see the conversation reads the diff and points out problems. The supervisor checks each finding and fixes what holds up.
5. **Delivery:** checked checklist, verification result, findings and decisions, and what to check manually.

It does not commit. You review and commit.

## 4. First feature

For something bigger (several screens, new business rule, integration):

### 4.1 Specify: what and why

```
/orquestra:specify let the manager export the month's sales report as CSV
```

Generates `.orquestra/specs/001-export-sales-csv/spec.md` with:
- prioritized **user stories** (P1 is the minimum that already delivers value);
- **acceptance scenarios** in the *Given / When / Then* format;
- numbered **requirements** (`FR-001`…) and measurable **success criteria** (`SC-001`…);
- at most 3 questions marked `[NEEDS CLARIFICATION]`. It assumes the rest and lists them under "Assumptions".

The spec **does not talk about technology**: no tables, APIs, or components. Any product person should be able to read it and agree. A clean-context reader tests whether it stands on its own before handing it to you.

**Your role:** read the spec and the assumptions. If an assumption is wrong, say so.

### 4.2 Clarify: settle the questions

```
/orquestra:clarify
```

At most 5 questions, **one at a time**, each with a recommended option. Answer with the letter, with "yes" (accepts the recommended one), or with your own answer. Each answer is saved to the spec right away.

### 4.3 Plan: the how

```
/orquestra:plan
```

Generates two files:
- `plan.md`: technical approach, files that will be created or changed, contracts, decisions with the rejected alternatives, and the check against the constitution;
- `tasks.md`: small tasks, each with exact file, done criterion, and two markers:
  - `[P]`: can run in parallel with others;
  - `[H]`/`[S]`/`[O]`: who executes (Haiku, Sonnet, or the supervisor itself).

```
- [ ] T003 [P] [S] [US1] Create export endpoint — files: src/api/export.ts — done: returns CSV with header
```

**Your role:** approve the plan. This is the cheapest moment to change your mind.

### 4.4 Implement

```
/orquestra:implement
```

The supervisor dispatches the tasks phase by phase, in parallel when possible, checks each delivery, and marks `[X]`. At the end of each phase there is a **checkpoint**: project verification and a test of the user story. It stops if anything fails.

You can implement one phase at a time (`/orquestra:implement phase 2`) if you want to follow closely.

### 4.5 Review

```
/orquestra:review
```

1. Runs build, lint, and tests.
2. Clean-context reviewers read the full diff (for risky changes, with Opus or two reviewers with different focuses).
3. The supervisor checks each finding and decides: fix, contest with evidence, escalate to you, or decline.
4. Checks that each spec requirement was met. Whatever is missing becomes a new task.
5. Writes everything to `review.md`.

### 4.6 Close and learn

```
/orquestra:consolidate
```

Retrospective: what did the review find that could have been avoided? Which wrong assumption cost rework? What is worth turning into a rule? The proposals appear before any change.

## 5. Teach the project to Claude

When you discover something the next developer (or the next session) needs to know:

```
/orquestra:note the Modal component clips dropdowns because it has overflow-hidden; use Popover with a portal
```

Before touching an area:

```
/orquestra:recall payments module
```

More in [Project memory](memory.md).

## Which command to use?

```
Is it a bug or tweak of up to ~5 files, with no architecture decision?
├── yes → /orquestra:quick
└── no → /orquestra:specify → clarify → plan → implement → review
```

Details and special cases in [Workflows and commands](workflows.md).
