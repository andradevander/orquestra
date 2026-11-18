# Workflows and commands

Usage reference: which command to use, what it requires, what it produces, and where it stops.

## Choosing the workflow

| Situation | Workflow |
|---|---|
| Bug, visual tweak, small improvement (up to ~5 files) | `quick` |
| Feature with a new business rule, several screens, public contract, data migration | `specify` → `clarify` → `plan` → `implement` → `review` |
| I already have finished code and want a review | `review` (standalone) |
| I am going to touch an old area and want to know whether the code still matches the spec | `drift` |
| Trivial tweak of 1–3 lines | Ask directly, no command |

`quick` recommends switching to the feature workflow when it notices the request is bigger than it looks.

## Feature pipeline

```
 specify ──► clarify ──► plan ──► implement ──► review ──► consolidate
  spec.md    (spec.md)   plan.md    [X] on       review.md    memory
                         tasks.md   the tasks
```

| Command | Requires | Produces | Gate to proceed |
|---|---|---|---|
| `specify` | `.orquestra/` | `spec.md` (Status: Draft) | ≤ 3 questions; clean-context reader with no blocker |
| `clarify` | `spec.md` | updated `spec.md` (Status: Clarified) | Answers saved; big questions under "Deferred" |
| `plan` | `spec.md` | `plan.md`, `tasks.md` (Status: Approved) | Constitution satisfied; every requirement has a task; your approval |
| `implement` | `tasks.md`, `plan.md` | Code + `[X]` tasks + recorded base | Each phase's checkpoint passing |
| `review` | Diff | `review.md` (Status: Implemented if clean) | No open P0/P1; spec covered |
| `consolidate` | — | Memory and constitution updated | Your confirmation |

### The active feature

`.orquestra/state.json` stores the feature you are on (`{"feature": ".orquestra/specs/004-..."}`). Commands use that feature when you do not pass another. To switch, pass the name as an argument (`/orquestra:plan 003-coupon-signup`). The file is local, stays out of git, and each person has their own.

### Spec status

`Draft` → `Clarified` → `Approved` → `Implemented`. `drift` only looks at Approved or Implemented specs.

## Task format

```
- [ ] T005 [P] [S] [US1] Imperative description — files: a.ts, b.ts — done: <criterion> (depends: T003)
```

| Part | Meaning |
|---|---|
| `T005` | ID in execution order |
| `[P]` | Parallelizable: does not touch any file of another `[P]` in the phase and has no pending dependency |
| `[H]` | Mechanical and cheap: locate (scout/Haiku) or edit mechanically (implementer with Haiku) |
| `[S]` | Implementation or test (implementer/tester, Sonnet) |
| `[O]` | Supervisor: decision, shared file, integration |
| `[US1]` | User story from the spec |
| `files:` | Exact files. **Same file = sequential** |
| `done:` | Verifiable criterion |

Phases: **Foundation** (blocks everything) → one phase per story, in priority order, each with a **Checkpoint** → **Polish** (if any).

## How the supervisor handles review findings

| Decision | When |
|---|---|
| FIX | The finding holds up |
| CONTEST | Only with evidence the reviewer could have read (file:line, test). "It was intentional" does not count |
| ESCALATE | Product decision, or evidence outside the reviewer's reach → goes to you |
| DECLINE | P3 without cost-benefit, with the reason recorded |

Code severities: **P0** breaks production or loses data · **P1** bug in a common flow · **P2** edge case or clear risk · **P3** low-risk improvement.
Document severities: **BLOCKER** prevents implementing · **MAJOR** causes rework · **MINOR** is clarity.

Convergence: after fixing P0/P1, a **new** reviewer reviews again. At most 3 rounds (2 in `quick`). If it runs over, or if a new finding appears exactly where there was a fix, it stops and asks you.

## Support commands

| Command | Use |
|---|---|
| `note <fact>` | Records a pitfall, decision, convention, lesson, or reference in memory |
| `recall <topic>` | Searches memory, specs, and reviews |
| `consolidate` | Merges duplicates, fixes or deletes what went stale, promotes recurring rules to the constitution |
| `drift` | Report of what diverged between spec and code (read-only) |

## Responsiveness

Touched layout or Tailwind classes? The `responsive-ui` skill kicks in (commands load it explicitly when the change touches UI). Core rule: **mobile goes in the base class and the old desktop value comes back with a prefix** (`w-[300px]` → `w-full lg:w-[300px]`). The `desktop_guard.py` script lists every desktop class that changed without a reset.

## What never happens unless you ask

- Commit or push.
- Deleting memory or amending the constitution (`consolidate` always asks).
- Weakening or deleting tests to make them pass.
