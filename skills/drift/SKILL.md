---
name: drift
description: Drift report — compares approved or implemented specs (.orquestra/specs/) with the current code and lists only the divergences (missing functionality, incomplete model, logic shortcut, different architecture, code without a spec). Run periodically or before touching an old area. Read-only.
argument-hint: "[feature or specs folder, optional]"
disable-model-invocation: true
---

# Drift between spec and code

Scope: $ARGUMENTS (empty = all features in `.orquestra/specs/` whose spec Status is **Approved** or **Implemented**).

**Read-only.** This command does not edit code, specs or tasks.

## Steps

1. List the features in scope. For each one, extract from `plan.md` and `tasks.md` the files and symbols cited.
2. Dispatch **one `scout` per feature**, all in parallel:
   > For each of the following items, say whether the file/symbol exists and where (file:line): <list>. Also list files changed after <spec date> in those folders (git log --since).
3. **You** read the code at the central points and compare it with the FRs and acceptance scenarios. Do not trust memory or tasks marked as done.
4. Classify only what **diverges**:
   - **missing:** requirement with no implementation;
   - **incomplete:** partially implemented;
   - **shortcut:** implemented in a way that does not fulfill the scenario (e.g. validation only on the client);
   - **architecture:** structure different from the plan's;
   - **no spec:** relevant behavior in the code that no spec describes.

## Output

Write `.orquestra/reviews/YYYY-MM-DD-drift.md` (create the folder if missing):

```markdown
## <NNN-feature>
- [missing] FR-003 — <1 line> — where it should be: file
- [shortcut] scenario US1.2 — <1 line> — file:line
(or "No drift.")
```

In the chat: count per feature and per type, and the report path. To fix it, suggest `/orquestra:review` on the feature (which generates convergence tasks) or updating the spec, if the code is the desired behavior. If a spec does not cite files, suggest adding them: this makes the next detection cheaper.
