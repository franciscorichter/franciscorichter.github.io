#!/usr/bin/env python3
"""Simulate a birth-death tree and inject it into index.html.

The tree is a real forward simulation of a constant-rate birth-death process.
Lineages that leave no descendant at the present are drawn in the "dead" class;
a tree of living species would keep only the "alive" ones. The SVG is written
between <!-- tree:start --> and <!-- tree:end --> in index.html.

    python3 tools/make_tree.py            # uses the fixed seed below
    python3 tools/make_tree.py --search   # print seeds with a good balance
"""
import pathlib
import random
import re
import sys

LAM, MU, T = 1.0, 0.55, 5.4          # speciation rate, extinction rate, duration
SEED = 222
W, H = 1000, 300                      # SVG viewBox
X0, X1 = 6, 930                       # time 0 and the present, in viewBox units
PAD = 10

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"


class Node:
    __slots__ = ("t0", "t1", "kids", "fate", "y", "alive")

    def __init__(self, t0):
        self.t0, self.t1, self.kids, self.fate, self.y, self.alive = t0, None, [], None, None, False


def simulate(rng, cap=110):
    root = Node(0.0)
    active, t, count = [root], 0.0, 1
    while active:
        t += rng.expovariate(len(active) * (LAM + MU))
        if t >= T:
            for n in active:
                n.t1, n.fate = T, "present"
            return root
        n = active.pop(rng.randrange(len(active)))
        n.t1 = t
        if rng.random() < LAM / (LAM + MU):
            n.fate, n.kids = "split", [Node(t), Node(t)]
            active += n.kids
            count += 2
            if count > cap:
                return None
        else:
            n.fate = "death"
    return root


def mark(n):
    n.alive = n.fate == "present" or any([mark(k) for k in n.kids])
    return n.alive


def tips(n):
    return [n] if not n.kids else [t for k in n.kids for t in tips(k)]


def census(root):
    ts = tips(root)
    alive = sum(t.fate == "present" for t in ts)
    return alive, len(ts) - alive


def ladderize(n):
    for k in n.kids:
        ladderize(k)
    n.kids.sort(key=lambda k: len(tips(k)), reverse=True)


def layout(root):
    ts = tips(root)
    step = (H - 2 * PAD) / max(len(ts) - 1, 1)
    for i, t in enumerate(ts):
        t.y = PAD + i * step

    def place(n):
        if n.kids:
            for k in n.kids:
                place(k)
            n.y = sum(k.y for k in n.kids) / len(n.kids)
    place(root)


def x(t):
    return X0 + (X1 - X0) * t / T


def paths(root):
    seg = {True: [], False: []}

    def walk(n):
        seg[n.alive].append(f"M{x(n.t0):.1f} {n.y:.1f}H{x(n.t1):.1f}")
        for k in n.kids:
            seg[k.alive].append(f"M{x(n.t1):.1f} {n.y:.1f}V{k.y:.1f}")
            walk(k)
    walk(root)
    return " ".join(seg[True]), " ".join(seg[False])


def svg(root):
    alive_d, dead_d = paths(root)
    # Tip dots as zero-length round-capped strokes: they stay round when the
    # SVG is stretched vertically on narrow screens (preserveAspectRatio="none").
    dots = " ".join(f"M{x(T):.1f} {t.y:.1f}h0.001"
                    for t in tips(root) if t.fate == "present")
    stem = f"M0 {root.y:.1f}H{X0}"
    return (
        f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="none" role="img" aria-labelledby="tree-title">'
        f'<title id="tree-title">A simulated birth-death tree: lineages that survive to the present, '
        f'and faded lineages that went extinct</title>'
        f'<line class="present" x1="{x(T):.1f}" y1="0" x2="{x(T):.1f}" y2="{H}"/>'
        f'<path class="dead" d="{dead_d}"/>'
        f'<path class="alive" d="{stem} {alive_d}"/>'
        f'<path class="tips" d="{dots}"/>'
        f'</svg>'
    )


def build(seed):
    root = simulate(random.Random(seed))
    if root is None:
        return None
    mark(root)
    return root


def main():
    if "--search" in sys.argv:
        for s in range(1, 400):
            r = build(s)
            if r is None or not r.alive:
                continue
            a, d = census(r)
            if 18 <= a <= 28 and 16 <= d <= 34:
                print(s, "alive", a, "extinct", d)
        return
    root = build(SEED)
    assert root is not None and root.alive, "seed gives no surviving tree"
    ladderize(root)
    layout(root)
    page = PAGE.read_text(encoding="utf-8")
    new, n = re.subn(r"(<!-- tree:start -->).*?(<!-- tree:end -->)",
                     lambda m: m.group(1) + svg(root) + m.group(2), page, flags=re.S)
    assert n == 1, "tree markers not found in index.html"
    PAGE.write_text(new, encoding="utf-8")
    a, d = census(root)
    print(f"seed {SEED}: {a} surviving lineages, {d} extinct")


if __name__ == "__main__":
    main()
