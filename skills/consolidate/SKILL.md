---
name: consolidate
description: Performs maintenance and retrospective of the project memory — merges duplicates, fixes or deletes outdated memories, trims the INDEX, promotes recurring patterns to the constitution and turns generic lessons into improvement suggestions for the skills. Run at the end of a feature or when the INDEX goes over ~60 lines.
argument-hint: "[recently completed feature, optional]"
disable-model-invocation: true
---

# Consolidate memory and learn from the feature

Input: $ARGUMENTS

## 1. Retrospective (if there is a feature)

Read `review.md`, the discovery and convergence tasks in `tasks.md` and the spec's clarifications. Ask yourself:
- Which review finding **repeated** or would have been avoided with a rule? → candidate for **pitfall** or **principle**.
- Which wrong assumption cost rework? → **lesson**.
- Which decision will be questioned again in the future? → **decision**.
- Which task was poorly sized or poorly marked `[P]/[H]/[S]`? → **lesson** about planning in this project.

## 2. Memory audit

For memories scoped to code, dispatch a `scout` to check whether the files and symbols cited still exist. Then:
- **Duplicates** → merge into one (keep the clearer name), delete the other and replace the `[[old-name]]` links with `[[new-name]]` across the whole folder (grep).
- **Outdated** → fix with the current state, or delete if no longer valid.
- **Three or more memories pointing to the same rule** → propose a principle in the constitution (MINOR amendment) and replace the memories with a reference.
- **Generic lesson** (applies to any project, not just this one) → it is not project memory. List it as an improvement suggestion for the plugin skill (e.g. a new pitfall in `responsive-ui/references/pitfalls.md`).

## 3. Propose before applying

Show the grouped list of changes (create / update / merge / delete / promote to the constitution / suggest for the skill) and **ask for confirmation**. Deleting and amending the constitution always require an explicit "yes".

## 4. Apply

Make the approved changes, rewrite `INDEX.md` (sections in order, short hooks, under ~60 lines) and update the `reviewed` date of the memories touched. Final summary in 3–5 lines.
