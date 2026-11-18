# Project memory

How to make Claude stop repeating the same mistakes in your project.

## Three layers

| Layer | File | When it is read | What it holds |
|---|---|---|---|
| Constitution | `.orquestra/constitution.md` | By the commands and reviewers | Non-negotiable rules and verification commands |
| Index | `.orquestra/memory/INDEX.md` | **Every session** (imported in `CLAUDE.md`) | One line per memory, with the hook for when it matters |
| Memories | `.orquestra/memory/<type>-<slug>.md` | Only when relevant | One fact per file, with the why and how to apply |

The index is cheap and always present. The content only enters when the subject comes up. The same logic applies to subagents: pointers in the expensive context, content on demand.

## Memory types

| Type | Example |
|---|---|
| `pitfall` | "`Modal` has `overflow-hidden`: a dropdown inside it gets clipped. Use `Popover` with a portal." |
| `decision` | "Polling instead of websockets because the customer's proxy drops long connections (incident of 2026-03)." |
| `convention` | "Dates travel as UTC ISO-8601; timezone conversion only in the presentation layer." |
| `lesson` | "Data migration tasks are never `[P]`: two ran together and locked the table." |
| `reference` | "Production error dashboard: <url>. Use it to confirm whether a reported bug has already occurred." |

## What to record (and what not to)

Record only what is **non-obvious and reusable**:

- ✅ a pitfall that already caused a bug or regression;
- ✅ a decision whose reason the code doesn't show;
- ✅ a team convention that isn't in the lint;
- ✅ where to find something outside the repository.

Do not record:

- ❌ what the code, the git log or the constitution already say;
- ❌ detail that only matters for the current conversation;
- ❌ generic good practice ("write tests"). That is a skill matter, not the project's;
- ❌ **secrets, tokens, personal or customer data**. The folder is versioned.

## How to use

```
/orquestra:note <the fact>      # writes (or updates, if something similar exists)
/orquestra:recall <subject>     # searches before touching an area
/orquestra:consolidate          # maintenance, when closing a feature or when the index is large
```

You can also speak naturally: "note that…", "remember this", "have we already decided something about X?". The `note` and `recall` skills are triggered automatically.

At the end of `quick` and `review`, the supervisor proposes recording what it learned. It proposes and you decide.

## Memory format

```markdown
---
name: pitfall-modal-clips-dropdown
type: pitfall
summary: A dropdown inside a Modal is clipped by overflow-hidden
scope: src/components/Modal/**, dropdowns, selects
created: 2026-11-18
reviewed: 2026-11-18
source: review of feature 004
---

`Modal` (src/components/Modal/Modal.tsx:12) uses `overflow-hidden` for the rounded corners.
Any `absolute` dropdown inside it is clipped.

**Why:** the rounding of the borders depends on the overflow.
**How to apply:** inside a modal, use `Popover` with a portal (`src/components/Popover`).

Related: [[decision-popover-with-portal]]
```

The `name` equals the file name without `.md`, and the `[[...]]` links use that name.

## Maintenance: memory rots

Memory grows easily and ages fast. That is why:

- `/orquestra:recall` checks that the cited files still exist before using a memory;
- `/orquestra:consolidate`:
  - merges duplicates;
  - fixes or deletes what became stale;
  - promotes to the constitution a rule that appears in 3 or more memories;
  - separates generic lessons, which become improvement suggestions for the plugin skills.

Keep `INDEX.md` under ~60 lines.

## Project memory × Claude's personal memory

Claude Code also has a personal memory (`~/.claude/projects/.../memory/`). It is **yours**, doesn't go through code review and doesn't reach the rest of the team. The `.orquestra/` memory is **the team's**: it goes in git, shows up in PRs and everyone benefits.

Rule of thumb: your own preference ("I prefer short answers") goes in personal memory. Project knowledge goes in `.orquestra/`.
