#!/usr/bin/env python3
"""
desktop_guard - flags Tailwind class changes in a git diff that may alter the DESKTOP layout.

Mobile-first rule: a responsive fix should only ADD behaviour below a breakpoint. If a class
that applied on desktop is removed or replaced, its old value must come back under a breakpoint
prefix (sm:/md:/lg:/xl:/2xl:), otherwise the desktop computed style changed.

For every changed line pair it reports:
  REMOVED  a base (unprefixed) class disappeared and no prefixed copy restores it
           e.g. `w-[300px]` -> `w-full`            (desktop width changed)
  ADDED    a new base class in a property group the line did not set before, with no
           breakpoint value taking over           e.g. `p-1` added -> applies on desktop too
Additions that change nothing while content fits (min-w-0, shrink-0, truncate, break-words,
flex-wrap, touch-none...) are treated as safe.

It is a heuristic: it reads class-like string literals, pairs -/+ lines in order inside a hunk,
and cannot see the cascade or the parent. Treat each hit as "prove the desktop (>= lg) value is
unchanged, or say why the change is intended" - not as an error.

Usage:
  python desktop_guard.py                    # working tree vs HEAD
  python desktop_guard.py <git-diff-args>    # e.g. --cached | HEAD~1 | main...HEAD | -- src/components
  git diff | python desktop_guard.py -       # read a diff from stdin
"""
import re
import subprocess
import sys

BREAKPOINTS = ("sm", "md", "lg", "xl", "2xl")
SAFE_ADDITIONS = {
    "min-w-0", "min-h-0", "shrink-0", "flex-shrink-0", "truncate", "break-words", "break-all",
    "flex-wrap", "whitespace-normal", "max-w-full", "[overflow-wrap:anywhere]",
    "touch-none", "select-none", "hide-scrollbar",
}
BARE = {
    "flex", "grid", "block", "inline", "hidden", "contents", "relative", "absolute", "fixed",
    "static", "sticky", "truncate", "italic", "underline", "uppercase", "lowercase", "capitalize",
    "visible", "invisible", "grow", "shrink", "border", "rounded", "shadow", "ring", "transition",
}
FLEX_ONLY_GROUPS = {"justify", "items", "content", "gap", "flex-direction", "grid-cols", "grid-rows", "place"}
LITERAL = re.compile(r'"([^"\n]*)"' + r"|'([^'\n]*)'" + r"|`([^`\n]*)`")
TEMPLATE_EXPR = re.compile(r"\$\{[^}]*\}")
UTIL = re.compile(r"^!?(?:[\w\[\]@()&>*.-]+:)*!?-?[a-z\[][\w\[\]()./%#,:'-]*$")


def looks_like_classes(text: str) -> bool:
    toks = text.split()
    if not toks or not all(UTIL.match(t) for t in toks):
        return False
    tw = [t for t in toks if "-" in t or ":" in t or t in BARE]
    return len(tw) >= max(1, (len(toks) + 1) // 2)


def split_classes(line: str):
    """Class-like tokens from the string literals of a line (className strings, ternary branches, constants)."""
    stripped = line.strip()
    if stripped.startswith(("//", "/*", "*", "{/*")):
        return []
    out = []
    for m in LITERAL.finditer(line):
        text = next(g for g in m.groups() if g is not None)
        text = TEMPLATE_EXPR.sub(" ", text)
        if looks_like_classes(text):
            out.extend(text.split())
    return out


def group_of(cls: str) -> str:
    """Rough property group, so `w-full` and `w-[300px]` count as the same property."""
    c = cls.lstrip("!-")
    if c in ("flex", "grid", "block", "inline", "inline-flex", "inline-block", "hidden", "contents", "table-cell"):
        return "display"
    if c in ("absolute", "relative", "fixed", "static", "sticky"):
        return "position"
    if c.startswith("whitespace-"):
        return "whitespace"
    if c.startswith(("flex-row", "flex-col")):
        return "flex-direction"
    if c in ("flex-1", "flex-auto", "flex-none", "flex-initial"):
        return "flex"
    m = re.match(
        r"(min-w|max-w|min-h|max-h|w|h|size|gap-x|gap-y|gap|p[xytrbl]?|m[xytrbl]?|space-[xy]|inset|top|left|right|"
        r"bottom|order|col-span|row-span|grid-cols|grid-rows|basis|text|leading|rounded|z|overflow-[xy]|overflow|"
        r"justify|items|self|content|place)(?:-|$)",
        c,
    )
    if not m:
        return c
    g = m.group(1)
    if g.startswith("gap"):
        return "gap"
    if g.startswith("overflow"):
        return "overflow"  # overflow-y-auto is reset by xl:overflow-visible
    return g


UI_EXTENSIONS = (".tsx", ".jsx", ".ts", ".js", ".html", ".vue", ".svelte")
TEXT_SIZES = {"xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl", "7xl", "8xl", "9xl"}
TEXT_ALIGN = {"left", "center", "right", "justify", "start", "end"}
DESKTOP_RESTORE = ("sm", "md", "lg")  # values that already hold at 1024px
NON_FLEX_DISPLAY = ("block", "inline", "inline-block", "hidden", "contents", "table-cell")


def prop_of(cls: str) -> str:
    """Exact property key: `w-[90%]` -> w, `gap-x-8` -> gap-x, `rounded-t-none` -> rounded-t.
    Finer than group_of(), so a kept `md:` value only vouches for its own property."""
    c = cls.lstrip("!-")
    g = group_of(c)
    if g in ("display", "position", "flex-direction", "flex"):
        return g
    if c.startswith("text-"):
        v = c[5:]
        if v in TEXT_SIZES or (v.startswith("[") and any(u in v for u in ("px", "rem", "em"))):
            return "font-size"
        return "text-align" if v in TEXT_ALIGN else "text-color"
    return re.sub(r"-(\[[^\]]*\]|[^-]+)$", "", c) or c


def analyse(old: str, new: str):
    old_c, new_c = split_classes(old), split_classes(new)
    if not old_c and not new_c:
        return []
    old_set, new_set = set(old_c), set(new_c)
    old_base = {c for c in old_c if ":" not in c}
    new_base = {c for c in new_c if ":" not in c}
    new_prefixed = {}
    for c in new_c:
        parts = c.split(":")
        if len(parts) > 1 and parts[-2] in BREAKPOINTS:
            new_prefixed.setdefault(parts[-1], set()).add(parts[-2])

    def restored(util):
        """'desktop' if a sm/md/lg copy brings it back, 'xl' if only xl/2xl does, else None."""
        bps = new_prefixed.get(util, set())
        if bps & set(DESKTOP_RESTORE):
            return "desktop"
        return "xl" if bps else None

    desktop_props = {prop_of(u) for u, bps in new_prefixed.items() if bps & set(DESKTOP_RESTORE)}
    xl_props = {prop_of(u) for u, bps in new_prefixed.items() if not bps & set(DESKTOP_RESTORE)}
    # Display at >= 1024px: the widest of sm/md/lg wins; an xl value applies from 1280 on.
    display_at = {}
    for u, bps in new_prefixed.items():
        if prop_of(u) == "display":
            for bp in bps:
                display_at[bp] = u
    lg_display = next((display_at[bp] for bp in ("lg", "md", "sm") if bp in display_at), None)
    desktop_not_flex = lg_display in NON_FLEX_DISPLAY and all(
        display_at[bp] in NON_FLEX_DISPLAY for bp in ("xl", "2xl") if bp in display_at)

    hits = []
    # Layout-neutral equivalences:
    #   w-[N] -> w-full max-w-[N]   same width whenever the parent is at least N wide (desktop)
    #   p-N + -m-N added together    bigger hit area, same box position
    neutral = set()
    for c in old_base - new_set:
        m = re.match(r"^(w|h)-\[(.+)\]$", c)
        if m and f"{m.group(1)}-full" in new_base and f"max-{m.group(1)}-[{m.group(2)}]" in new_base:
            neutral |= {c, f"{m.group(1)}-full", f"max-{m.group(1)}-[{m.group(2)}]"}
    # p-N / m-N split into the x and y halves, each half kept at the base or restored at sm/md/lg:
    # `p-2` -> `px-2 py-3 md:py-2` is still p-2 on desktop.
    for c in old_base - new_set:
        m = re.match(r"^(-?)([pm])-(\d+(?:\.\d+)?|px|\[[^\]]+\])$", c)
        if not m:
            continue
        neg, kind, val = m.groups()
        halves = [f"{neg}{kind}{axis}-{val}" for axis in ("x", "y")]
        if all(h in new_base or restored(h) == "desktop" for h in halves):
            neutral.add(c)
            neutral.update(h for h in halves if h in new_base)
            for h in halves:
                for other in new_base - old_set:
                    if prop_of(other) == prop_of(h):
                        neutral.add(other)  # the phone-only value of that half (e.g. py-3)
    for c in new_base - old_set:
        m = re.match(r"^(p[xytrbl]?)-(\d+(?:\.\d+)?)$", c)
        if m and f"-m{m.group(1)[1:]}-{m.group(2)}" in new_base:
            neutral |= {c, f"-m{m.group(1)[1:]}-{m.group(2)}"}
    # A base value already overridden at sm/md/lg by a prefixed class that the new line keeps
    # never reached the desktop: `w-[90%] md:w-[70%]` -> `w-full md:w-[70%]` is phone-only.
    old_overridden = set()
    for c in old_c:
        parts = c.split(":")
        if len(parts) == 2 and parts[0] in DESKTOP_RESTORE and c in new_set:
            old_overridden.add(prop_of(parts[1]))

    removed_props = set()
    for c in sorted(old_base - new_set):
        if c in neutral or prop_of(c) in old_overridden:
            continue
        r = restored(c)
        if r == "desktop":
            continue  # restored under a breakpoint that already holds at 1024px
        removed_props.add(prop_of(c))
        if r == "xl":
            hits.append(("XL-ONLY", c, ["restored only from 1280px - the 1024-1279px band changes"]))
            continue
        repl = sorted(x for x in new_base - old_set if prop_of(x) == prop_of(c))
        hits.append(("REMOVED", c, repl))
    for c in sorted(new_base - old_set):
        p = prop_of(c)
        if c in neutral or c in SAFE_ADDITIONS or p in removed_props or p in old_overridden:
            continue  # safe helper, or already reported as the replacement of a removed class
        if p in desktop_props or (p in ("overflow-x", "overflow-y") and "overflow" in desktop_props):
            continue  # e.g. `mb-3 sm:mb-0`, `overflow-y-auto md:overflow-visible` - reset on desktop
        if desktop_not_flex and (c in ("flex", "grid") or group_of(c) in FLEX_ONLY_GROUPS):
            continue  # e.g. `flex justify-center lg:block` - inert once display is block on desktop
        if p in xl_props:
            hits.append(("XL-ONLY", c, ["reset only from 1280px - the 1024-1279px band changes"]))
            continue
        hits.append(("ADDED", c, []))
    return hits


def read_diff(argv):
    if argv and argv[0] == "-":
        return sys.stdin.read()
    cmd = ["git", "diff", "-U0", "--no-color"] + argv
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    diff = read_diff(sys.argv[1:])
    state = {"file": None, "line": 0, "minus": [], "plus": [], "findings": 0}

    def similarity(a, b):
        # Max of Jaccard and containment: a short old class list ("relative") that reappears
        # inside a long rebuilt one is still the same element.
        a, b = set(a), set(b)
        if not a or not b:
            return 0.0
        return max(len(a & b) / len(a | b), len(a & b) / len(a))

    def flush():
        # Pair each removed class-bearing line with the most similar added line of the hunk
        # (by shared classes), so inserted comments/wrappers don't shift the comparison.
        minus = [(m, split_classes(m)) for m in state["minus"]]
        plus = [(p, ln, split_classes(p)) for p, ln in state["plus"]]
        used = set()
        for old, old_c in minus:
            if not old_c:
                continue
            best, best_sim = None, 0.0
            for j, (_, _, new_c) in enumerate(plus):
                if j in used or not new_c:
                    continue
                sim = similarity([c.split(":")[-1] for c in old_c], [c.split(":")[-1] for c in new_c])
                if sim > best_sim:
                    best, best_sim = j, sim
            if best is None or best_sim < 0.5:
                state["findings"] += 1
                print(f"{state['file']}:?  RESTRUCT element with \"{' '.join(old_c[:6])}{' ...' if len(old_c) > 6 else ''}\" "
                      "was removed or rebuilt - compare its desktop rendering by hand")
                continue
            used.add(best)
            new, ln, _ = plus[best]
            for kind, cls, repl in analyse(old, new):
                state["findings"] += 1
                extra = f"  ->  {' '.join(repl)}" if repl else ""
                print(f"{state['file']}:{ln or '?'}  {kind:<8} {cls}{extra}")
        state["minus"], state["plus"] = [], []

    for raw in diff.splitlines():
        if raw.startswith("+++ "):
            flush()
            state["file"] = raw[6:] if raw.startswith("+++ b/") else raw[4:]
            state["skip"] = not state["file"].endswith(UI_EXTENSIONS)
        elif raw.startswith("@@"):
            flush()
            m = re.search(r"\+(\d+)", raw)
            state["line"] = int(m.group(1)) if m else 0
        elif state.get("skip"):
            continue
        elif raw.startswith("-") and not raw.startswith("---"):
            state["minus"].append(raw[1:])
        elif raw.startswith("+"):
            state["plus"].append((raw[1:], state["line"]))
            state["line"] += 1
    flush()

    if state["findings"] == 0:
        print("desktop_guard: no unguarded class changes found.")
    else:
        print(f"\ndesktop_guard: {state['findings']} change(s) to justify - for each, show the desktop (>= lg) "
              "value is unchanged, or that the change is intended.")


if __name__ == "__main__":
    main()
