# The theory behind Orquestra

This document explains **why** the package works the way it does. The skills say what to do. This is the reasoning, so you can adapt it with judgment instead of following it on autopilot.

Orquestra combines three ideas:

1. **Elephant and goldfish** (from the [Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model)): whoever has the context creates, and whoever doesn't reviews.
2. **Spec-driven development** (from [Spec Kit](https://github.com/github/spec-kit)): first the what and why, then the how, with tasks as the unit of execution.
3. **Supervisor and workers with tiered models**, which neither project does: the expensive model decides, the cheap ones execute.

---

## 1. Elephant and goldfish

**The problem:** whoever wrote a piece of code or a document reads what they meant, not what is written. Assumptions are invisible to the author, because they have them in their head. A Claude session is the same: after 40 messages, the context "knows" things that no file says.

**The solution:** separate the roles.

- **Elephant** (the main session): remembers everything, talks to you, creates, decides.
- **Goldfish** (a new subagent for each review): remembers nothing. It receives only the artifact (the diff, the spec) and the criteria. If it doesn't understand something, someone else won't either. If it finds a bug, the bug is in the text, not in the intent.

**Practical consequences**, which show up in the skills:

- **Never hand your conclusion to the reviewer.** "I think this is right, check it" anchors the answer. Pass the code and the criteria.
- **A new reviewer every round.** Resuming the previous reviewer brings along the bias it built up.
- **`omitClaudeMd: true`** on the goldfish: they don't even load the project's CLAUDE.md. They receive only what the brief points to. This keeps the outside view.
- **Paraphrase before criticizing** (`goldfish-reader`): if the reader can't say in its own words what the spec proposes, the spec failed, even with no specific "error".
- **Reviewing in the same context is not a goldfish review.** Without an available subagent, the package stops and warns you instead of pretending.

## 2. Spec-driven

**The problem:** asking for code straight from one sentence makes the model fill the gaps with silent guesses. You only discover the guesses in review, or in production.

**The solution:** intermediate artifacts, each with a gate.

| Artifact | Answers | Gate |
|---|---|---|
| `constitution.md` | Which rules are never negotiable? | A conflict with it is always critical |
| `spec.md` | What and why? (no how) | ≤ 3 open questions, goldfish reader understands it |
| clarifications | What was ambiguous? | Answers recorded in the spec immediately |
| `plan.md` | How, and which alternatives were discarded? | Constitution check |
| `tasks.md` | In which small steps, by whom, in what order? | Every requirement has a task |
| `review.md` | Is it right? Is it complete? | No open P0/P1, spec coverage |

Ideas adopted from Spec Kit:

- **Informed guess instead of a question:** at most 3 `[NEEDS CLARIFICATION]`. The rest becomes a stated assumption. Asking everything tires the human, and asking nothing hides decisions.
- **One question at a time, with a recommendation.** Answering "B" is cheap. A list of 10 open questions is not.
- **Independent stories:** each one, alone, delivers value. This lets you stop at the MVP and parallelize.
- **Strict task format** (`T005 [P] [S] [US1] … — files: … — done: …`): this is what turns a plan into something dispatchable.
- **"A completion claim is not evidence":** the review checks the code, not the `[X]`.
- **Convergence by addition only:** what is missing becomes a new task at the end, without rewriting history.

What was **not** brought over (excess for a lean package): per-platform shell scripts, an extension and preset system, separate `research.md`/`contracts/`/`quickstart.md`, requirement checklists as their own command. For a small feature, a short `plan.md` is enough. For a small change, no spec at all: `/orquestra:quick`.

## 3. Tiered supervisor and workers

**The problem:** using the most expensive model for everything is wasteful, and using the cheapest for everything fails where it matters.

**The solution:** divide by **type of reasoning**, not by task size.

| Needs… | Model | Why |
|---|---|---|
| Judgment, trade-offs, integration, checking whether a finding holds | Opus (supervisor) | An error here propagates to everything |
| Implementing something already specified, writing tests, reviewing a diff | Sonnet | Good execution with a closed scope |
| Locating, listing, counting, mechanical transformation | Haiku | No decision involved; speed and cost |

**Where the money really goes** (details in `skills/orchestrate/references/token-economy.md`):

1. **What comes back to the supervisor.** Every subagent result enters Opus's context and is re-read on every turn. That is why all agents have a **short, fixed output contract**. This is the saving that weighs the most.
2. **Rework caused by a vague brief.** The brief is everything the worker knows.
3. **An LLM reviewing what doesn't even compile.** The validation ladder goes from cheap to expensive: build and tests, then goldfish, then the supervisor verifies each finding.

**Escalate, don't insist:** start cheap. If the worker fails twice, move up a model or do it yourself. Repeating the same brief on the same model means paying twice for the same error.

## 4. Verifying the reviewer (the supervisor errs too)

Reviewers err too, sometimes with great confidence. That is why each finding gets an explicit decision:

- **FIX**: it holds.
- **CONTEST**: only with evidence the reviewer could have read. "It was intentional" doesn't count.
- **ESCALATE**: a product decision, or evidence outside the reviewer's reach. It goes to the human.
- **DECLINE**: a P3 with no cost-benefit, with the reason recorded.

And two honesty rules: **never lower the severity** to get rid of a finding, and a reviewer that failed shows up as **"not run"**, never as "0 findings".

**Convergence:** after fixing P0/P1, a new reviewer. At most 3 rounds. If a new finding appears exactly where you just fixed something (churn), the problem is design, not code: stop and ask.

## 5. Memory that learns

**The problem:** every session starts from zero and repeats the project's same mistakes.

**The solution**, in layers with different costs:

| Layer | Where | Loaded | Content |
|---|---|---|---|
| Constitution | `.orquestra/constitution.md` | By the commands | Non-negotiable rules, verification commands |
| Index | `.orquestra/memory/INDEX.md` | **Every session** (import in CLAUDE.md) | One line per memory, with the hook for when it matters |
| Local state | `.orquestra/state.json` | By the commands | Each person's active feature (outside git) |
| Memories | `.orquestra/memory/*.md` | On demand | One fact per file, with **Why** and **How to apply** |

The index is cheap (≈ 60 lines) and always present. The content only enters when it is relevant. It is the same principle as the subagents: **pointers in the expensive context, content on demand**.

**The learning cycle:**

```
work → review finds something → /note (pitfall, decision, lesson)
    ↑                                         ↓
constitution ← /consolidate (3+ similar memories become a principle)
                     ↓
       generic lesson → improvement suggestion for the plugin skill
```

- **Project memory** holds what is specific to the project ("component X clips dropdowns").
- **Plugin skill** holds what holds for any project ("a new overflow clips an absolute dropdown").
- This is how the package stays generic and each project gets smart.

**Filter for what to record:** only what is non-obvious and reusable. What the code, git or the constitution already say doesn't go in. Memory grows easily and rots fast. That is why `/consolidate` audits and deletes, and `/recall` checks that the cited file still exists before using it.

**Why versioned in the repo** and not only in Claude's personal memory: personal memory (`~/.claude/projects/.../memory/`) belongs to the individual. The one in `.orquestra/` belongs to the team and goes through code review, like any file.

## 6. Responsiveness as an example of a domain skill

`responsive-ui` shows how to write a domain skill that works with the rest:

- **A testable central rule** ("only add below the breakpoint") and a **script that checks it** (`desktop_guard.py`). A rule you can check with a script is cheaper than a rule that depends on review.
- **References loaded on demand** (`patterns.md`, `pitfalls.md`), not in SKILL.md.
- **Its own orchestration** for large scope, using the same generic agents.
- **Ties into memory:** project pitfalls go to `.orquestra/memory/`, and generic pitfalls go back to the skill.

To create another domain skill (accessibility, performance, REST API, migrations), follow the same mold: central rule, patterns, pitfalls, a verifier script when possible, and the touchpoint with memory.
