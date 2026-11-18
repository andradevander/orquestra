---
name: responsive-ui
description: Use whenever you write, change, or review web layout (pages, components, forms in modals, panels, tables, lists, drag-and-drop), especially with Tailwind. Premise — every screen works on phone and tablet without breaking the desktop. Trigger when creating a screen or component, when touching layout classes, and when the user reports "breaks on mobile", "have to scroll sideways", "text overflows the button", "leftover space", "overlaps", "can't scroll", "looks different on desktop", or asks for a responsiveness review, even without saying "responsive" (Portuguese triggers - "quebra no mobile", "tem que arrastar para o lado", "texto sai do botão", "sobra espaço", "fica por cima", "não dá para rolar", "no desktop ficou diferente", "responsivo").
---

# Responsive without breaking the desktop

There are two scenarios, and the rule changes:

- **Retrofit** (the screen already exists and is in use on desktop): the desktop **MUST NOT change**; phone and tablet start working *on top of* it. This is the most common scenario and the most dangerous.
- **New screen**: write mobile-first and add the desktop with prefixes (section "Building something new").

Every retrofit change is judged in this order:

1. **Is the desktop (≥ 1024px) identical?** If not, it is a regression, unless the desktop change is the request itself.
2. **Does the phone (360–430px) work?** Nothing leaves the screen, nothing requires sideways scrolling, everything is reachable and tappable.
3. **Does the tablet (768–1023px) work?** This is the most forgotten range: the side menu takes up space and little is left.

Before starting, find out the stack (`package.json`, `tailwind.config.*`): Tailwind version, **custom breakpoints** (the numbers below assume the default sm 640 · md 768 · lg 1024 · xl 1280), drag-and-drop library, whether there is SSR. If the project has memory (`.orquestra/memory/`), look there for layout widths (side menu, usable area) and pitfalls already recorded.

## How not to break the desktop: only add below the breakpoint

The unprefixed class applies at all widths, including desktop. To change the phone, **swap the base class for the phone value and give the old value back with a prefix**. That way the desktop keeps receiving exactly what it received:

```tsx
"w-[300px]"            →  "w-full lg:w-[300px]"
"gap-8"                →  "gap-2 sm:gap-8"
"flex gap-4 h-[90%]"   →  "flex flex-col lg:flex-row gap-4 lg:h-[90%]"
"absolute right-0"     →  "sm:absolute sm:right-0"
```

What does **not** need a reset is whatever only acts when space is lacking: `min-w-0`, `shrink-0`, `truncate`, `break-words`, `flex-wrap` (careful with `w-full` children, see pitfalls), `max-w-full`, `touch-none` on a drag handle.

Everything else changes the desktop: a "harmless" `p-1`, `w-[300px]` → `w-[304px]`, a new `overflow`. These small changes are the main source of regressions.

## How much space there really is

Measure your layout (side menu width, page paddings) and record it in the project memory. The numbers below are **only an example**, for a layout with a 240px side menu and 16px padding. Redo the math with the real layout:

| Width | Page content area | Modal box |
|---|---|---|
| 375px (phone) | ≈ 343px, with the menu becoming a drawer | ≈ 327px |
| 768px (tablet, menu open) | ≈ 496px | ≈ 500px, because the modal is `fixed` and measures by the **window** |
| ≥ 1280px | ~1000px+ | 40–55% of the window |

To answer "does it fit?", add up the minimum widths: icons + paddings + gaps + **the longest word**. A flex item does not shrink below its content until it has `min-w-0`. Do the math before choosing the fix.

## Workflow

1. **Understand the context.** Read the whole file and see where it is rendered (grep the import). The available width depends on the parent: page, modal, side panel, table cell.
2. **Find the cause, not the symptom.** If the same problem shows up on several screens, the cause is usually in a shared component, and fixing it there fixes them all.
3. **Choose the fix** by the type of problem in `references/patterns.md`, writing the phone in the base and giving the desktop back with a prefix.
4. **Go through `references/pitfalls.md`** before calling it done: dropdown clipping, `flex-wrap` with `w-full`, drag on touch, unreachable content.
5. **Prove the desktop did not change.** Run the guard (`scripts/desktop_guard.py`, in this skill's folder; use the absolute path) and justify or fix each alert:
   ```bash
   python3 <skill-folder>/scripts/desktop_guard.py                     # working tree vs HEAD
   python3 <skill-folder>/scripts/desktop_guard.py main -- <paths>     # since a base, only some files
   ```
   If the changes were already committed, **pass the base** (e.g. `main` or the sha from before). Without a base, the guard compares against `HEAD` and wrongly shows zero alerts. It needs git. The guard lists: base class removed or swapped without the old value given back in `sm:`/`md:`/`lg:` (`REMOVED`); new base class that also applies on desktop (`ADDED`); value given back only in `xl:`, which changes the 1024–1279px range (`XL-ONLY`); rebuilt element that requires a manual check (`RESTRUCT`). It is heuristic. It does not see new elements (wrappers, duplicated `lg:hidden` rows) nor the cascade, so zero alerts does not excuse you from reading the diff. An alert can be intentional: say which one and why.
6. **Compile/lint** with the project's commands (e.g. `npx tsc --noEmit`). If the compiler changes versioned cache files (e.g. `tsconfig.tsbuildinfo`), restore them.
7. **Deliver** a per-file summary (what changes on phone/tablet, what stays identical on desktop, guard alerts justified) and a short browser checklist at 375 / 768 / 1280px, with simulated touch in DevTools. Do not commit unless asked.

## Building something new

Write with the phone in mind first and add the desktop with prefixes. That way the rule above comes for free. Before delivering a new screen, check:
- nothing with a fixed width above ~300px without `max-w-full` or a prefix;
- rows with several controls wrap or stack on the phone;
- side-by-side panels stack below lg;
- actions do not depend on hover; dragging does not prevent scrolling;
- action buttons stay right-aligned even when the title disappears;
- tables hide secondary columns on the phone;
- the project's shared components are reused instead of recreating the layout.

## Large reviews

For 1–3 files, do it directly. For a whole folder or more, follow `references/orchestration.md` (it uses the `responsive-auditor` agent and the flow of the `orchestrate` skill).

## Learning

When you discover a new pitfall **of this project** (a shared component that clips a dropdown, a layout width, a custom breakpoint), record it with `/orquestra:note` so the next session does not repeat the mistake. Generic pitfalls, which apply to any project, should become an improvement suggestion for this skill.

## References

| File | When to read |
|---|---|
| `references/patterns.md` | When choosing the fix: patterns by type of problem, with before/after |
| `references/pitfalls.md` | Before calling it done: mistakes that have already caused regressions |
| `references/orchestration.md` | When reviewing several folders: roles, briefing, and prompts |
| `scripts/desktop_guard.py` | Step 5 of the workflow, whenever you change classes |
