---
name: quick
description: Lean path for small and medium changes (bug, tweak, feature of up to ~5 production files) — quick critique of the request, short checklist, execution restricted to the checklist and one goldfish review of the diff. No formal spec. Use day to day; for large features use /orquestra:specify.
argument-hint: "<what to do>"
disable-model-invocation: true
---

# Quick

Request: $ARGUMENTS

Works with or without `.orquestra/`. If it exists, use the constitution (verification commands) and the memory.

## 1. Critique before touching anything (edit nothing)

- Check the project memory (INDEX in context, if any) for the subject.
- **Domain skill:** if the change touches an area that has its own skill (e.g. layout, CSS or Tailwind classes → `responsive-ui`), **load it now with the Skill tool** and follow its flow, including its checks (e.g. `desktop_guard.py`). Inside a command, it is not triggered on its own.
- If you do not know where to make the change, dispatch a `scout`. If you do, read directly.
- Answer in up to 6 lines: what you understood, where you will make the change (file:line), risks or assumptions, and **questions only if the answer changes what you will do**. Mark unconfirmed assumptions as `[UNVERIFIED]`.
- If the request is bigger than it looks (more than ~5 production files, public contract, data migration, architecture decision), recommend `/orquestra:specify` and stop here.

## 2. Checklist

Write in the chat (not in a file) a checklist of 2–8 items:

```
- [ ] 1. <action> — <file> — done: <criterion>
```

Record the base: `git rev-parse HEAD` and `git status --short` (no git: note the files you will touch).

**Ask the user for an "ok"** only if there is an `[UNVERIFIED]` assumption or a product decision. Otherwise, proceed.

## 3. Execute

- Do it directly if it is 1–2 files. Delegate to the `implementer` if the items are independent in different files (in parallel) or if the work is mechanical and extensive.
- **Scope = the checklist.** Anything new discovered becomes a new, declared item.
- Run the relevant objective verification (or declare that there is none). Stop if the same error repeats or if a fix causes another failure.

## 4. Review with fresh eyes

Trivial tweak (1–3 lines, obvious): you may skip. Anything else: **one** `goldfish-reviewer` with the diff since the base and the checklist items as criteria. If you cannot build a complete diff (no base, no git), pass the whole files and tell the user that coverage is partial.

Finding triage: section 5 of the `orchestrate` skill (load it with the Skill tool if it is not in context). If a P0/P1 was fixed, run **one** new reviewer. **Maximum of 2 rounds** in this mode. If a P0/P1 is still open at the limit, stop, list it and ask the user: accept, continue, or move to `/orquestra:specify`.

## 5. Deliver

Checklist with `[x]`, verification (command and result), findings and decisions, and what to check manually. If something non-obvious was learned, propose `/orquestra:note`. No commit, unless the user asks.
