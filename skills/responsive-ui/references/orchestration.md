# Large responsiveness review with subagents

Use when the scope is a whole folder or more (e.g. "review src/components"). For 1–3 files, do it directly, because the cost of spinning up agents does not pay off. The general flow (briefing, short return, verification of findings) is that of the `orchestrate` skill. Only what is specific to responsiveness lives here.

## Roles and models

| Role | Agent | Model | Edits? | Output |
|---|---|---|---|---|
| Supervisor | you (main session) | Opus | Shared files | Product decisions, finding filter, integration |
| Analyst | `responsive-auditor` | Sonnet (Opus if the area is critical or Sonnet gets the math wrong) | No | Findings per file with the exact fix |
| Developer | `implementer` | Sonnet | Only the block's files | Before→after, guard alerts justified |
| Sweeps | `scout` | Haiku | No | File lists, uses of a component, counts |
| Final validator | `goldfish-reviewer` | **Opus** (pass `model: opus` in the call) | No | Ranked findings on the full diff |

Why the final validator is Opus: responsiveness breaks on detail (a missing reset, an `overflow` that clips a dropdown). It is the last barrier before the user, and it is a single call, so the cost is low and the gain is high.

## Steps

1. **Map with `scout`:** list the UI files in scope and the shared components they import.
2. **Split into blocks with no file overlap.** Each dev edits only their block, so they run in parallel without conflict.
3. **Write the shared briefing** in a scratchpad file (the generic template is in the `orchestrate` skill, in `references/briefing.md`; load that skill with the Skill tool so you can read the file; add the responsiveness fields below) and point all agents to it.
4. **Dispatch the analysts in parallel**, one per block.
5. **As each analysis arrives:** discard wrong or cosmetic findings, **decide the product questions** (stacking order, columns to hide), and hand it to the block's dev with the decisions explicit.
6. **Shared files stay with the supervisor:** translation files (devs report key + texts) and components used by several blocks, because changing one of them affects all.
7. **After the devs:** run the compile and `desktop_guard.py` on the whole set, and dispatch the final validator on the full diff together with the guard output.
8. **Apply the confirmed findings** (verify each one in the code) and deliver the summary + browser checklist. Record new project pitfalls with `/orquestra:note`.

## Extra briefing fields (on top of the generic template)

```markdown
Goal: phone (~360–430px) and tablet (768–1023px) good; desktop (≥ lg) identical.
Stack: <framework, Tailwind version, custom breakpoints?, dnd lib, SSR?>.
Layout widths: side menu <N>px or none; page padding <N>px; modal <rule>.
Patterns and pitfalls: <absolute path of the skill>/references/patterns.md and pitfalls.md;
  project pitfalls in .orquestra/memory/ (if it exists).
Translation files: do not edit; report key + texts.
```

## Developer brief (implementer)

```
Read the briefing: <path>. Edit only: <files>.
Apply (with the supervisor's decisions): <list of findings with exact fix>.
Verify each finding in the code; if it is wrong or causes a desktop regression, skip it and say why.
When done: python3 <absolute path of the skill>/scripts/desktop_guard.py <base> -- <your files>
and justify or fix each alert; run <compile command>.
```

## Final validator brief (goldfish-reviewer, model: opus)

```
Review the diff of <files/folder> (git diff is in <file>, or read the files).
desktop_guard output: <file or pasted>. RESTRUCT alerts require manual reading.
Criteria, by priority: 1) desktop regression (base class swapped without reset, order, padding, width);
2) dropdown/popover clipped by new overflow; 3) touch/dnd (selection that depended on the drag, touch-none on the row,
onClick duplicating the drag action); 4) unreachable content, absolute below the breakpoint, wrong order,
conflicting classes; 5) SSR/hydration (window/matchMedia outside effect); 6) behavior change beyond layout.
Anything uncertain goes under "COULD NOT VERIFY" (it becomes a browser checklist item).
```
