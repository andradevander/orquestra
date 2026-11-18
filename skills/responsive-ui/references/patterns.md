# Patterns by type of problem

Each pattern: the symptom, why it happens, and the class swap — always with the phone in the base and the desktop given back in the prefix.

## Contents
1. Row of elements that overflows the width
2. Side-by-side panels (content + panel/preview)
3. Fixed widths
4. Tab or segment bars
5. Grids with a fixed number of columns
6. Long text pushing the layout
7. Fields in pairs
8. Tables
9. Alignment when an element disappears on the phone
10. `absolute` elements when stacking
11. Actions that only appear on hover
12. Drag and drop on touch
13. Screen heights and modals
14. Popovers and menus near the edge

---

## 1. Row of elements that overflows the width
**Symptom:** "I have to scroll the screen sideways", "the button disappears", "the text leaves the box".
**Why:** `flex` without wrapping, children that do not shrink below their content (`min-width: auto`), large gaps.

Choose by the shape of the row:
```tsx
// options/cards of equal weight → stack on the phone, equal columns from sm
"flex justify-between gap-8"   →  "flex flex-col sm:flex-row sm:justify-between gap-2 sm:gap-8"
item "w-full"                  →  "w-full sm:flex-1 sm:min-w-0"     // flex-1 = same equal columns
item text                      +  "min-w-0 break-words";  icons  +  "shrink-0"

// fields + small controls (color, trash) → let them wrap
"flex gap-2 items-center"      →  "flex flex-wrap sm:flex-nowrap gap-2 items-center"
field "flex-1"                 →  "flex-1 min-w-[40%] sm:min-w-0"

// w-full field + field + button → stack (flex-wrap would send the w-full to another row on desktop)
"flex w-full items-center gap-2" → "flex flex-col sm:flex-row w-full sm:items-center gap-2"
```
Often `min-w-0` on the `flex-1` child alone solves it. Between sm and lg the space is still tight: if a long word breaks in the middle, reduce the gap only in that range (`sm:gap-4 lg:gap-8`).

## 2. Side-by-side panels (content + panel/preview)
**Symptom:** "the preview overlaps", "the card gets squeezed".
**Why:** fixed row with a panel of minimum width (`min-w-[300px]`, `w-[35%]`) that does not fit next to the content.
```tsx
<div className="flex flex-col lg:flex-row gap-4 lg:h-[90%]">
  <div className="flex-1 min-w-0 …">…content…</div>
  <div className="w-full h-[640px] lg:h-auto lg:w-[35%] lg:min-w-[300px] …">…preview…</div>
</div>
```
- Break at **lg** (not md): at 768px with the side menu open, ~496px are left.
- A height that came from the parent (`h-full`, `h-[90%]`) now applies only on desktop (`lg:h-…`). A preview sized by height (`h-full` + `aspect-ratio`) needs a **fixed height** when stacked.
- Three columns (list · center · settings): 3×300px + center only fit from ~1000px of content — stack below **xl** or transform the sides: the list becomes a horizontal scrolling strip; settings open on top (`absolute inset-0 lg:static`) with a close button.
- Order on the phone: use `order-*` with a reset (`order-first lg:order-none`) to put first what the user needs to see.

## 3. Fixed widths
```tsx
"w-[535px]"   →  "w-full max-w-[535px]"   // can shrink; on desktop it stays the same (parent ≥ 535)
"w-[300px]"   →  "w-full lg:w-[300px]"    // on desktop it is the exact width
"w-[250px]"   →  "w-[250px] max-w-full"   // + on the inner text "min-w-0 truncate"
```
Exception: content designed for a fixed frame (e.g. a preview inside a phone mockup) is fixed on purpose. Do not make it fluid.

## 4. Tab or segment bars
```tsx
bar     "flex border-b …"  →  "flex border-b … overflow-x-auto hide-scrollbar"
item    "px-4 py-2 …"      →  "shrink-0 whitespace-nowrap px-3 md:px-4 py-2 …"
```
If the active tab can change through buttons (Next/Back), scroll to it: `el.scrollIntoView({ block: "nearest", inline: "nearest" })`.

## 5. Grids with a fixed number of columns
```tsx
"grid grid-cols-5"  →  "grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5"
// cells with a known minimum size
"flex flex-wrap" + cells "w-[10%]"  →  "grid grid-cols-[repeat(auto-fill,minmax(56px,1fr))]"
```
When switching from flex to grid, ensure the same cell size on desktop (e.g. `md:grid-cols-[repeat(auto-fill,minmax(336px,1fr))]` to keep 320px thumbnails).

## 6. Long text pushing the layout
| Case | Class |
|---|---|
| Title in a row with actions | title `truncate min-w-0`; actions `shrink-0` |
| File name, id, slug (no spaces) | wrappers `min-w-0` + `truncate` |
| URL or link | `[overflow-wrap:anywhere]` (`break-words` does not break URLs) |
| Technical key/value | `break-all min-w-0`; grid `grid-cols-1 sm:grid-cols-3` |

## 7. Fields in pairs
**Symptom (desktop):** "the second field does not reach the edge, there is leftover space on the right".
**Why:** half-width fields (`md:w-[47%]`) in a row without `justify-between`.
```tsx
"flex flex-wrap gap-4"  →  "flex flex-wrap justify-between gap-4"
```
On the phone the fields are already `w-full` and stack.

## 8. Tables
- Hide secondary columns on the phone **in both the `<th>` and the `<td>`**: `hidden md:table-cell`. Keep the identifier, the status, and the actions.
- Wrap in `overflow-x-auto` as a safety net (only if no row has an `absolute` menu).
- Fixed column widths: reduce only on the phone (`w-[72px] md:w-[100px]`, `p-2 md:p-4`).
- Search/filter hidden on the phone (`hidden md:flex`) when it is the only way to find an item is a bug — keep it visible.

## 9. Alignment when an element disappears on the phone
**Symptom:** "the create button went to the left".
**Why:** `justify-between` with the title `hidden md:block` — only one child is left, which aligns to the left.
```tsx
button wrapper  +  "ml-auto"
```
Applies to any row in which one of the sides disappears on the phone.

## 10. `absolute` elements when stacking
A positioned element (list, selector, toolbar) goes on top of the rest when the layout stacks. Position only on desktop:
```tsx
"absolute h-[80%] w-[65%] overflow-scroll"  →  "w-full lg:absolute lg:h-[80%] lg:w-[65%] lg:overflow-scroll"
```

## 11. Actions that only appear on hover
On touch there is no hover: the button stays invisible (and sometimes clickable on top of another).
```tsx
"opacity-0 group-hover:opacity-100"
  →  "opacity-0 group-hover:opacity-100 focus-visible:opacity-100 [@media(hover:none)]:opacity-100"
```

## 12. Drag and drop on touch
Find out **where the dnd-kit listeners are**:
- **On a dedicated handle:** keep the sensors and put `touch-none` on the handle (without it the browser treats the gesture as scrolling). Bigger area without touching the layout: `p-1 -m-1`.
- **On the whole row/card:** change the sensors so that swiping scrolls and press-and-hold drags:
  ```ts
  useSensor(MouseSensor),
  useSensor(TouchSensor, { activationConstraint: { delay: 250, tolerance: 8 } }),
  useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates }),
  ```
  First, check whether anything depends on the drag start (e.g. selecting in `onDragStart`). If it does, add an `onClick` with the same action.
- **Dragging from one list to another area** is impractical on the phone: offer "tap to add" on a separate element visible only below the breakpoint.

## 13. Screen heights and modals
`vh` includes the browser bar on the phone — the footer with the buttons ends up underneath it.
```tsx
"h-screen"                                 →  "h-[100dvh]"
"max-h-[85vh]"                             →  "max-h-[85dvh] md:max-h-[85vh]"
"w-screen h-screen absolute left-0 top-0"  →  "fixed inset-0"     // w-screen counts the scrollbar
modal box  "w-[80%]"                       →  "w-full md:w-[80%]"  and overlay "p-2 md:p-4"
```
If the stacked content does not fit, ensure a container that scrolls **only below the breakpoint** (`overflow-y-auto md:overflow-visible`) — on desktop a new `overflow` clips dropdowns.

## 14. Popovers and menus near the edge
An `absolute` popover with a fixed width (`w-72`) anchored to the right or center goes off screen on the phone. Anchor from the side that has space (`left-0`/`right-0`), limit with `max-w-[calc(100vw-2rem)]`, or open as a bottom sheet (`fixed inset-x-0 bottom-0`) below the breakpoint.
