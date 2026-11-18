---
name: recall
description: Searches the project memory (.orquestra/memory/), the specs and previous reviews for everything relevant to a subject or task, and returns a short summary with pointers. Use before planning or touching an area, or when the user asks "did we already decide this?", "is there a pitfall in X?", "what do we know about Y?".
argument-hint: "<subject, area or path>"
---

# Recall

Subject: $ARGUMENTS

1. Read `.orquestra/memory/INDEX.md` (it may already be in context) and open the memories whose hook or scope matches the subject.
2. If the subject is broad or the folder is large (more than ~30 memories, or if you also need to search `.orquestra/specs/**` and `.orquestra/reviews/**`), dispatch a `scout`:
   > Search .orquestra/ (memory, specs, reviews) for <terms and synonyms>. Return file:line + 1 line of what it says. Include decisions ("Decision", "Clarifications" sections) and related review findings.
3. **Check validity:** a memory reflects what was true when it was written. If it cites a file, function or flag, confirm it still exists before using it. If it is outdated, say so and propose fixing it with `/orquestra:note`.

## Output

```
RELEVANT:
- [type] title — what it says in 1 line (file) [ok | outdated?]
PREVIOUS DECISIONS: (from specs/reviews) — 1 line each, with path
NOTHING ON: <aspects of the subject with no record>
```

Short. It is context for the work, not a report.
