---
name: init
description: Prepares the current project for the Orquestra workflow — creates .orquestra/ (constitution, memory, specs, reviews), discovers the stack and verification commands, and links the memory to CLAUDE.md. Run once per repository.
argument-hint: "[notes about the project]"
disable-model-invocation: true
---

# Initialize Orquestra in this project

User notes: $ARGUMENTS

Templates: `constitution.md` and `memory-index.md`, at the end of this file. Follow their structure; do not improvise the format.

## Steps

1. **Check the state.** If `.orquestra/` already exists, do not overwrite anything: show what exists and ask what the user wants to update.

2. **Discover the project.** In a small repository (few configuration files), read directly. In a large repository, dispatch **one** `scout` with this request:
   > List: main language and framework with version (package.json, pyproject, go.mod, etc.); build, lint, typecheck and test commands (package.json scripts, Makefile, CI in .github/workflows); test framework; whether it uses Tailwind and whether it has custom breakpoints; main code folders; existing convention files (CLAUDE.md, AGENTS.md, CONTRIBUTING.md, .editorconfig, lint configs). Format: FOUND with file:line.

3. **Create the structure:**
   ```
   .orquestra/
     constitution.md        ← constitution.md template, with stack and commands already filled in
     memory/INDEX.md        ← memory-index.md template
     specs/.gitkeep
     reviews/.gitkeep
     state.json             ← {"feature": null}   (each person's LOCAL state, do not version)
   ```

4. **Draft the constitution** with what you found: stack, verification commands, and constraints visible in the code or docs. For **principles**, propose 3 to 5 deduced from the existing conventions (lint, docs, visible patterns) and mark each one as `(proposed)`. Do not invent a rule the project does not show. Leave `TODO(field): reason` where you do not know (e.g., project without tests → `TODO(tests): project has no automated tests`).

5. **Link the memory to CLAUDE.md.** If a `CLAUDE.md` exists at the root, append to the end (if it is not already there):
   ```markdown
   ## Orquestra
   Workflow and rules: .orquestra/constitution.md. Project memory (read the relevant items before planning):
   @.orquestra/memory/INDEX.md
   ```
   If it does not exist, create a minimal `CLAUDE.md` with only this. **Show the snippet to the user before writing it.**

6. **`.gitignore`:** add `.orquestra/state.json` (it is each person's active feature and would cause conflicts between branches). Warn if any pattern is ignoring the rest of `.orquestra/`: constitution, memory, specs and reviews belong to the team and must be versioned. If the project does not use git, warn that `/orquestra:implement` and `/orquestra:review` depend on a diff and will ask for the list of changed files.

7. **Ask just one thing:** "Review the principles marked as (proposed) in .orquestra/constitution.md. Do you want to adjust any now?" If yes, adjust them, remove the marks and fill in the ratification date.

## Done when

- [ ] `.orquestra/` created with constitution, INDEX.md, specs/, reviews/ and state.json
- [ ] Constitution with real stack and commands; principles reviewed or marked as (proposed)
- [ ] CLAUDE.md importing `@.orquestra/memory/INDEX.md`
- [ ] `.orquestra/state.json` in .gitignore
- [ ] Summary to the user: what was created and the next commands (`/orquestra:quick` for small and medium changes, `/orquestra:specify` for features)

---

## Templates

### constitution.md

````markdown
# Project Constitution

<!-- Non-negotiable project rules. Short (up to ~60 lines): it is read by /plan, /review and by the reviewers.
Each principle is declarative and testable: uses MUST / MUST NOT and gives the why.
Unknown value: write TODO(field): reason. Remove this comment after filling in. -->

## Principles

### 1. <Principle name>
- <Rule with MUST / MUST NOT, verifiable in a diff or a test>
- **Why:** <reason in 1 line>

### 2. <Principle name>
- <Rule>
- **Why:** <reason>

<!-- Examples of common principles (adapt or delete):
- Simplicity: MUST NOT create an abstraction for a single use; MUST NOT prepare for a future requirement that was not requested.
- Test first on business rules: every new business rule MUST have an automated test.
- Responsive without regression: every screen MUST work at 375/768px; the desktop MUST NOT change without an explicit request.
- Security: external input MUST be validated at the boundary; secrets MUST NOT go into code or logs.
- Reuse: MUST use the existing shared components/utilities before creating new ones. -->

## Stack and Constraints

- Language/framework: <...>
- Verification commands: build `<...>` · lint `<...>` · typecheck `<...>` · tests `<...>`
- Constraints: <compliance, compatibility, performance, i18n...>

## Workflow

- Small or medium change (up to ~5 production files, no architecture decision): `/orquestra:quick`.
- Feature: `/orquestra:specify` → `/orquestra:clarify` (if there are doubts) → `/orquestra:plan` → `/orquestra:implement` → `/orquestra:review`.
- Commit and PR only after objective verification and goldfish review with no open P0/P1 (except a trivial 1–3 line adjustment).

## Governance

- A conflict with the constitution is always CRITICAL: adjust the spec, the plan or the tasks. Do not dilute the rule.
- A justified violation goes into "Justified Complexity" in plan.md, with the simpler alternative rejected and the reason.
- Amendments: MAJOR = removes or redefines a principle · MINOR = new principle · PATCH = wording.

**Version:** 1.0.0 · **Ratified:** <YYYY-MM-DD> · **Last amended:** <YYYY-MM-DD>
````

### memory-index.md

````markdown
# Project Memory

<!-- Index loaded in every session via CLAUDE.md (@.orquestra/memory/INDEX.md).
One line per memory: - [Title](file.md) — short hook saying WHEN it matters.
Keep it under ~60 lines; above that, run /orquestra:consolidate.
The content lives in the files, never here. -->

## Pitfalls

## Decisions

## Conventions

## Lessons

## References
````
