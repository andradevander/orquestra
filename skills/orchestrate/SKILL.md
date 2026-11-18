---
name: orchestrate
description: Supervisor playbook for splitting work across subagents (scout/Haiku locates, implementer and tester/Sonnet execute, goldfish-reviewer/goldfish-reader review with clean context) while keeping planning, decisions, and validation in the main session. Use when the user asks to "use subagents", "delegate", "orchestrate", "save tokens", or "review with fresh eyes", when an /orquestra command says to follow this skill, or for a task that clearly splits into independent parts across several files. Do not use for changes to 1–2 files.
---

# Orchestrate: the supervisor plans and validates, subagents execute

You, in the main session, are the **supervisor** (the "elephant"): you hold the context, make the decisions, write the briefs, and validate what comes back. Subagents are **cheap, focused hands** and **unbiased eyes** (the "goldfish"). They only know what is in the brief and only return what the output contract asks for.

## 1. Delegate or do it directly?

Delegate when you gain at least one of these:
- **Parallelism:** independent jobs that can run together.
- **Clean context:** reading many files to reach a short conclusion (you keep only the conclusion).
- **Fresh eyes:** review without the author's bias. In this case, delegating is mandatory.
- **Cost:** mechanical work that a smaller model does just as well.

Do it directly when it takes 2–3 tool calls, when you already know exactly where to change things, or when writing the brief would take more work than the task. Starting a subagent has a fixed cost. **If you cannot write a clear brief, you do not yet understand the task well enough to delegate.**

## 2. Who does what

| Role | Agent | Model | When |
|---|---|---|---|
| Supervisor | you | Opus | Understand the request, plan, decide trade-offs, verify findings, integrate, talk to the user |
| Locate | `scout` | Haiku | Find files, usages, patterns; sweeps and counts |
| Execute | `implementer` | Sonnet | One code task with defined files and acceptance criterion |
| Prove | `tester` | Sonnet | Tests for the acceptance criteria; run the verification |
| Review code | `goldfish-reviewer` | Sonnet (Opus for critical changes or large final validation) | Diff + criteria, without the conversation |
| Review document | `goldfish-reader` | Sonnet | Spec, plan, or tasks: "can this be executed without asking the author?" |
| Responsiveness | `responsive-auditor` | Sonnet | See the `responsive-ui` skill |

In the plugin, the agents appear with a prefix: `orquestra:scout`, `orquestra:implementer`, etc. Use that name in `subagent_type`.

**Escalation:** start with the cheapest model that can handle it. If the agent gets the same thing wrong twice, or returns something shallow, go up one level (pass `model` in the Agent call) or do it yourself. Do not insist on the same brief.

## 3. The brief

The brief is the only thing the subagent knows. Use the template in `references/briefing.md` (if reading it fails due to permissions, assemble the brief with these fields): objective, target files ("edit only these"), reference pattern (file:line), decided/discarded, done criterion, verification command, and return format.

Golden rules:
- **Point, don't paste.** Pass file paths and lines, not the content.
- **Explicit, narrow scope.** "Edit only X and Y."
- **For a reviewer: give the code and the criteria, never your conclusion.** "I think it's right, check it" produces confirmation, not review. Do not pass the conversation history or the justification for why you did it this way.
- **Product decisions go in already decided.** The subagent must not choose between options that belong to the user or to you.

## 4. Parallelism without conflict

- Parallel tasks **never** touch the same file. Same file means sequential.
- Shared files (translations, global types, components used by several blocks, configs) stay with the supervisor. Workers report what needs to change.
- Launch all independent agents **in the same message**, so they run together.
- While they run, do not redo their work. Prepare the next step or wait.

## 5. Validation ladder (cheap → expensive)

1. **Objective first:** build, lint, typecheck, tests (`tester` or you). An LLM reviewing code that does not compile is a waste.
2. **Goldfish:** `goldfish-reviewer` with the diff and the acceptance criteria. One reviewer is enough for an ordinary change. Use two, with different focuses (e.g., correctness and security), only for large or risky changes.
3. **You verify each finding** in the code before acting. For each one, decide:
   - **FIX:** the finding holds. Fix it yourself (if trivial) or send it to the `implementer`.
   - **CONTEST:** only with evidence the reviewer could have read (file:line, test). "It was intentional" is not evidence.
   - **ESCALATE:** the evidence is outside the reviewer's reach, or it is a product decision. Take it to the user.
   - **DECLINE:** P3 with no cost-benefit, with the reason recorded.
   You wrote the code. Wanting to contest does not prove the reviewer was wrong. Never downgrade the severity to get rid of a finding.
4. **Convergence:** after fixing P0/P1, run **a new reviewer** (never resume the previous one). A clean round = no open P0/P1. Limit of **3 rounds**. If it overruns, or if a new finding appears exactly where you just fixed something (churn), stop, list what is open, and ask the user.

## 6. Guardrails

- **Without a subagent tool, there is no goldfish review.** Reviewing in the same context is not a substitute. Tell the user so instead of pretending.
- **An agent that failed is not "zero findings".** Try once more. If it fails again, record it as "not run" in the report.
- **Long outputs go to a file**, not to the chat. The chat gets the path and the summary.
- **No sycophancy:** no "great question", no agreeing before verifying. Critique first.
- **Claims of completion are not evidence.** A worker's "DONE" needs verification (a command that passed, a file you checked).

## 7. Memory

- **At the start:** if the project has `.orquestra/memory/INDEX.md`, it is already in context via CLAUDE.md. Open the items relevant to the task before planning. For a larger search, use `/orquestra:recall`.
- **At the end:** if you learned something **non-obvious** and reusable (a pitfall, a decision, a convention the code does not show), propose recording it with `/orquestra:note`. Do not record what git or the code already say.

## 8. Delivery to the user

Short summary: what changed (per file or per task), how it was verified (commands and actual result), review findings and what was done with each, what remains pending or needs manual checking. No commit, unless the user asks.

## References

| File | When to read |
|---|---|
| `references/briefing.md` | When writing any subagent brief |
| `references/token-economy.md` | When sizing a large task, or when cost matters |
