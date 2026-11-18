# Pitfalls

Mistakes that often cause regressions. Read before calling a fix done. Project-specific pitfalls live in the project memory (`.orquestra/memory/`).

## Breaking the desktop without noticing

1. **Swapping the base class without giving the value back at the breakpoint.** This is the most common mistake. `gap-8` → `gap-2` without `sm:gap-8`; `w-[300px]` → `w-full` without `lg:w-[300px]`; `p-4` → `p-3` without `md:p-4`. Small differences count: 4px of width or a `p-1` that widens each row by 16px is already a visible regression. `scripts/desktop_guard.py` exists to catch this.
2. **`flex-wrap` with a `w-full` child.** The `w-full` child goes alone to the next row **on desktop too**. To stack only on the phone, use `flex-col sm:flex-row`.
3. **Height that came from the parent in the stacked layout.** `h-full`/`h-[90%]` make sense side by side; stacked, they squeeze the content. Move it to the breakpoint (`lg:h-full`).
4. **`order-*`, `hidden`, and phone-only wrappers without a reset.** `order-first` needs `lg:order-none`; an extra wrapper must disappear on desktop (`lg:contents`) or change nothing there. Check that the order and structure on desktop are what they were before.
5. **New gap in a container that has flexible spacers** (`flex-1`) on desktop: it narrows the spacers. Give back `lg:gap-0`/`xl:gap-0`.
6. **"Improving" the desktop along the way.** If the request is the phone, do not take the chance to change desktop sizes, colors, or spacing. If you think it is worth it, propose it separately.

## Clipping what should not be clipped

7. **New `overflow-*` on a container that has an `absolute` dropdown** (selects, font selector, filters, color picker) clips the list. Use `overflow` only below the breakpoint where it is needed (`max-h-full overflow-y-auto md:max-h-none md:overflow-visible`). Remember that `overflow-x-auto` makes the y axis `auto` too.
8. **Stacked content without a scroll container.** Inside a fixed-height modal or panel, stacking without something that scrolls leaves the end unreachable on the phone.

## Touch and drag

9. **Action that depended on the drag start.** If selecting/opening happens in `onDragStart`, a `TouchSensor` with a delay makes a simple tap stop working. Add an `onClick` with the same action.
10. **Duplicated mouse + click action.** On a draggable item with an unconstrained `MouseSensor`, a click fires drag start/end **and** `onClick`. An `onClick` that *selects* is idempotent; one that *adds* duplicates — use a separate element only for touch.
11. **`touch-none` on the whole row** prevents scrolling the list. Only on the handle.

## Layout

12. **`min-width: auto` of a flex item.** The content (the longest word, an icon) becomes the minimum width. Missing `min-w-0` → the row overflows instead of shrinking.
13. **Measuring from the wrong place.** A `fixed` modal measures by the window, not by the content area; a table cell, by the column. Redo the math with the real parent.
14. **Element stays `absolute` after stacking** and goes on top of the rest. Use `lg:absolute`.
15. **Fixed-width popover anchored to the right/center** goes off screen on the phone.

## React / SSR (if applicable)

16. **`window`/`matchMedia` outside `useEffect`** breaks SSR and hydration. Start with the server value and read it in the effect.
17. **Scrolling to a panel:** `scrollIntoView({ block: "nearest" })` on an element larger than the screen aligns the **bottom** edge. To bring a panel into view use `block: "start"`. Trigger it by the item key (id), not by the object, so it does not scroll on every keystroke.

## Process

18. **Fixing the symptom on N screens** when the cause is a shared component. Look for the common denominator first.
19. **Trusting a line number or a third party's premise** (analyst, another agent, ticket) without checking it in the code.
20. **"Still the same" after the fix.** If the user's screenshot shows exactly the old behavior, the new code is not running: change not deployed to the tested environment, or dev server/cache not reloaded (Ctrl+Shift+R; if it persists, stop the dev server, delete the build cache, e.g. `.next`, and start it again). Confirm this before "fixing" again.
21. **Compiler changing a versioned file.** Some `tsc` setups rewrite `tsconfig.tsbuildinfo`; restore it with `git checkout -- <file>` so it does not dirty the diff.
