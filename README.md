# Orquestra

A plugin for [Claude Code](https://claude.com/claude-code) that organizes development like a well-coordinated team:

- **one supervisor** (the main session, Opus) that understands the request, plans, decides, and validates;
- **cheap, focused subagents** (Haiku to locate, Sonnet to implement and test) that do small tasks and return short answers;
- **clean-context reviewers** ("goldfish") that look at the code or the spec without the bias of whoever wrote it;
- **specs, plans, and tasks** as gates between the request and the code;
- **versioned project memory**, which learns from every review;
- **responsiveness with no desktop regression**, with a script that proves the desktop did not change.

Instructions are written in English; Claude still answers in your language.

The result: fewer tokens spent on the expensive model, less rework from misunderstandings, and reviews that actually find problems.

## Installation

```bash
claude plugin marketplace add andradevander/orquestra
claude plugin install orquestra@orquestra
```

Or, inside Claude Code:

```
/plugin marketplace add andradevander/orquestra
/plugin install orquestra@orquestra
```

Requirements: Claude Code **2.1.271+** and `python3` (for the responsiveness guard). See the [recommended permissions](docs/troubleshooting.md#recommended-permissions) to avoid permission prompts on every use.

## In 2 minutes

```
/orquestra:init                                            # once per project
/orquestra:quick fix the button that disappears on mobile  # day to day
```

For a bigger feature:

```
/orquestra:specify export sales report as CSV
/orquestra:clarify
/orquestra:plan
/orquestra:implement
/orquestra:review
```

The complete walkthrough, with what to expect from each command, is in the **[Getting started guide](docs/getting-started.md)**.

## Documentation

| Document | For whom | What it has |
|---|---|---|
| [Getting started](docs/getting-started.md) | Everyone, first | Installation, first project, first change, first feature |
| [Workflows and commands](docs/workflows.md) | Day-to-day users | Which command to use when, what each produces, task format |
| [Project memory](docs/memory.md) | Those who want Claude to learn | What to record, how, and how to keep it clean |
| [Theory](docs/theory.md) | Those who want to understand why | Supervisor and workers, clean-context review, spec-driven, token economy |
| [Extending](docs/extending.md) | Those who will create skills and agents | Templates, conventions, and how to test |
| [Troubleshooting](docs/troubleshooting.md) | When something does not work | Permissions, versions, unexpected behavior |
| [Contributing](CONTRIBUTING.md) | Those who will send a PR | How to test locally and checklist |

## Commands

| Command | Purpose |
|---|---|
| `/orquestra:init` | Sets up the project (once): constitution, memory, specs |
| `/orquestra:quick <request>` | **Day to day.** Change of up to ~5 files: critique, checklist, execution, one review |
| `/orquestra:specify <feature>` | Writes `spec.md` (what and why) and tests it with a clean-context reader |
| `/orquestra:clarify` | Up to 5 questions, one at a time, with a recommendation, saved to the spec |
| `/orquestra:plan` | `plan.md` + `tasks.md` with `[P]` parallelism and who executes `[H]/[S]/[O]` |
| `/orquestra:implement [phase]` | The supervisor dispatches tasks to subagents, verifies, and marks `[X]` |
| `/orquestra:review [base]` | Objective verification → clean-context review → triage → `review.md` |
| `/orquestra:drift` | What in the code diverged from the approved specs |
| `/orquestra:note <fact>` | Saves a non-obvious lesson to project memory |
| `/orquestra:recall <topic>` | Searches memory, decisions, and previous reviews |
| `/orquestra:consolidate` | Retrospective: cleans memory and promotes rules to the constitution |

Automatically triggered skills: `orchestrate` (the supervisor's playbook) and `responsive-ui` (web/Tailwind layout).

## Agents

| Agent | Model | Does | Edits? |
|---|---|---|---|
| `scout` | Haiku | Locates files, usages, and patterns | No |
| `implementer` | Sonnet | One code task with a closed scope | Only the task's files |
| `tester` | Sonnet | Tests for the acceptance criteria, runs verification | Only tests |
| `goldfish-reviewer` | Sonnet (Opus on demand) | Reviews the diff without the conversation | No |
| `goldfish-reader` | Sonnet | Tests whether spec, plan, and tasks stand on their own | No |
| `responsive-auditor` | Sonnet | Analyzes responsiveness at 375/768/1280px | No |

## Repository structure

```
.claude-plugin/   plugin.json, marketplace.json
agents/           the 6 subagents
skills/           13 skills (commands embed their own templates)
docs/             guides and theory
```

## Credits

Ideas adapted from [google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model) (Apache-2.0) and [github/spec-kit](https://github.com/github/spec-kit) (MIT). The text here is original. No files were copied from those projects.

## License

[MIT](LICENSE)
