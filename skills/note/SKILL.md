---
name: note
description: Records a non-obvious learning in the project's versioned memory (.orquestra/memory/) — pitfall, decision, convention, lesson or reference — with frontmatter and a line in INDEX.md. Use when the user asks "note this", "remember this", "record this", or at the end of a task in which something reusable and non-obvious was discovered (propose before writing).
argument-hint: "[what to record]"
---

# Note in the project memory

What to record: $ARGUMENTS (empty = propose, from the conversation, 1–3 candidates and ask which to write).

If `.orquestra/memory/` does not exist, suggest `/orquestra:init` (or create only `memory/INDEX.md` from the template, if the user prefers).

## Filter: is it worth recording?

Record only what is **non-obvious and reusable**:
- ✅ a pitfall that already caused a bug or regression ("component X clips the dropdown because it has overflow-hidden");
- ✅ a decision with a reason the code does not show ("we use polling instead of websocket because the corporate proxy drops long connections");
- ✅ a team convention that is not in the lint;
- ✅ an external reference (dashboard, doc, ticket) and what it is for.
- ❌ what the code, the git log or the constitution already say;
- ❌ detail that only matters for this conversation;
- ❌ generic good-practice instruction (that belongs in the skill, not in the project memory).

If the user asks to remember something that does not pass the filter, ask which part was non-obvious and record that part.

## Write

1. **Look for a duplicate:** grep the subject in `.orquestra/memory/`. If a memory about it already exists, **update** the existing one (and the `reviewed` date) instead of creating another. If the old memory is wrong, fix or delete it.
2. **Create** `.orquestra/memory/<type>-<slug>.md` from the `memory-entry.md` template (at the end of this file): one fact per file, concrete, with **Why** and **How to apply**. The `name` field is the file name without `.md` (with the type prefix), and the `[[...]]` links use that same name. Absolute dates (never "yesterday").
3. **Index:** add a line in the right section of `INDEX.md`:
   `- [Title](type-slug.md) — hook that says when this matters`
4. **Do not write secrets**, tokens, personal data or customer data. The folder is versioned.

Confirm to the user in 1 line: the file created or updated and the index line. If the INDEX goes over ~60 lines, suggest `/orquestra:consolidate`.

---

## Templates

### memory-entry.md

````markdown
---
name: <type>-<slug>        # same as the file name without .md, e.g.: pitfall-overflow-clips-dropdown
type: pitfall | decision | convention | lesson | reference
summary: <1 line; it is what decides whether this memory is relevant>
scope: <folders, modules or technology it applies to, e.g.: src/components/**, tailwind, payments api>
created: <YYYY-MM-DD>
reviewed: <YYYY-MM-DD>
source: <spec, PR, incident or conversation that produced this (optional)>
---

<The fact, in 1–5 lines, concrete. With file:line or an example when it helps.>

**Why:** <the reason or the incident that showed this>
**How to apply:** <what to do differently next time, in actionable terms>

Related: [[decision-other-slug]]   <!-- always the full file name, without .md -->
````
