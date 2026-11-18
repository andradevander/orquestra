# Brief templates

The brief is everything the subagent knows. A good brief is short, points to paths, and defines the output. A bad brief causes rework, and rework costs more than delegating saved.

## Generic brief (implementer / tester)

```
OBJECTIVE: <1–2 sentences: what and why>
TASK: <tasks.md ID, if any> <imperative description>
FILES (edit only these): <paths>
PATTERN REFERENCE: <file:line of a similar example in the project>
CONTEXT: <relevant spec/plan, with path and section, e.g.: .orquestra/specs/004-x/spec.md#FR-003>
DECIDED (do not reopen): <product/architecture decisions already made>
DISCARDED: <approaches already evaluated and rejected, and why, in 1 line>
DONE WHEN: <verifiable criterion, e.g.: Given/When/Then>
VERIFICATION: <exact command>
RETURN: use your agent's output format. No diffs in the text.
```

## Scout brief

```
SEARCH FOR: <what, with likely synonyms>
WHERE: <folders> (ignore <node_modules, build, ...>)
I WANT BACK: file:line + 1 line on what it is. <Patterns: yes/no>
```

For several scouts in parallel, split by area (one folder or one question per scout).

## goldfish-reviewer brief

```
REVIEW: the diff of <files> against <base, e.g.: HEAD | main>.
  (If the reviewer has no shell: save `git diff` to <file in the scratchpad> and pass the path.)
ACCEPTANCE CRITERIA: <list, or path of spec.md + FR/SC IDs>
PROJECT RULES: <path of the constitution / relevant conventions>
EXTRA FOCUS: <optional: security, concurrency, data migration...>
```

**Do not include:** the conversation history, why you implemented it this way, your opinion on the quality, or findings from previous reviews (each reviewer starts clean).

## goldfish-reader brief

```
READ: <path of spec.md | plan.md | tasks.md>
CITED CODE: you may open the files the document mentions.
```

That's all. The less context, the better the "stands on its own" test.

## Shared briefing (block-based work)

When several agents work on the same front, write a briefing file in the scratchpad and point all of them to it. Without it, each agent reinvents patterns and the changes end up inconsistent.

```markdown
# <front>: briefing
Repo: <path>. Objective: <1 sentence>.
Stack: <relevant>.
## Already done (do not redo)
## Patterns to reuse (file:line)
## Rules
- Edit only the files in your block. Shared files: report, do not edit.
- Verify in the code before applying. No commit, no reformatting.
```
