"""Draw the figures open-*.svg of digestions/routes.md, Section 4.

    python digestions/figures/open.py            all of them
    python digestions/figures/open.py descent    only open-descent.svg

Notation is that of paper/barnette.tex; "rainbow tree", "excess" and "exchange"
are defined in routes.md. The drawing code is the paper's (paper/figures), the
examples are the paper's running example, research/instances and the family of
routes.md, and states, pairs and moves come from workings/barnette, rainbow
trees from proofs/sign-free/figures/sf.py. Every function fig_* asserts what
its caption says and returns the numbers quoted there.

Each figure is typeset by pdflatex at the text width of the paper and converted
by pdftocairo to an SVG 720 pixels wide on a white background; nothing but the
SVG files is written here.
"""
import sys
sys.dont_write_bytecode = True
import json
import math
import re
import subprocess
import tempfile
from collections import Counter, deque
from functools import lru_cache
from itertools import product
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'paper/figures'), str(ROOT / 'workings'), str(ROOT / 'proofs/sign-free/figures')]
import networkx as nx
import numpy as np
import sf
from model import ROOT_ANGLES, Model, R, energy, layout, load, tutte, und
from figures import PREAMBLE, TEXTWIDTH, Panel, pt, two_factors
from barnette.pairs import D_cycles, Q_cycles, reverse_D, reverse_Q
from barnette.solve import separating_triangle
from barnette.states import is_good, states
from barnette.triangulation import Triangulation

HERE = Path(__file__).parent
WIDTH = 720           # pixels

# Styles beyond those of the paper: arcs of H^+ in and out of a spanning tree, and two trees on the
# white faces. The bold dashes of the paper's style K get wider gaps, which stay open on a screen.
STYLES = r'''\tikzset{
  kept/.style={draw=black,line width=1pt},
  gone/.style={draw=black!60,line width=.4pt,dash pattern=on 1.2pt off 1.2pt},
  one/.style={draw=bfS,line width=1.1pt},
  two/.style={draw=bfR,line width=1.1pt,dash pattern=on 3pt off 1.6pt},
  K/.append style={dash pattern=on 3pt off 2.8pt},
}%
'''


# -- examples ---------------------------------------------------------------------
def triangulation(m):
    """The triangulation of workings/barnette with the faces of the model m, under the same numbers."""
    return Triangulation(dict(enumerate(m.F)), m.t0, m.e0)


def from_graph(edges, t0):
    """Model, layout and Triangulation of the triangulation with these edges and roots."""
    T = Triangulation.from_graph(nx.Graph(edges), t0, t0[:2])
    assert list(T.faces) == list(range(len(T.faces)))
    m = Model(list(T.faces.values()), T.t0, T.e0)
    assert T.A == m.A and T.X == m.X
    return m, layout(m), T


@lru_cache
def instance(name):
    d = json.loads((ROOT / 'research/instances' / f'{name}.json').read_text())
    return from_graph(d['edges'], d['t0']) + (d,)


def running():
    m, xy = load('running.json')
    return m, xy, triangulation(m)


def tup(m, s):
    """A state of workings/barnette, a dict, as the tuple that the model uses."""
    return tuple(s[t] for t in m.A)


# -- panels -------------------------------------------------------------------------
def cycle_arcs(c):
    return list(zip(c, c[1:] + c[:1]))


def pair_panel(m, xy, unit, r, s):
    """A pair as in fig-example(a) of the paper: r open wedges, s filled wedges, D(r,s)
    solid arrows, the cycles of Q_s dashed arrows."""
    p = Panel(m, xy, unit).base().state(r, 'r').state(s, 's').arrows(m.D(r, s))
    for K in m.directed_cycles(m.Q_directed(r, s)):
        p.arrows(cycle_arcs(K), 'K', 1.5)
    return p


def good_panel(m, xy, unit, s):
    """A good state as in fig-overview(b) of the paper: Q_s dashed, the two sides of t0 other than e0 bold."""
    f = m.F[m.t0]
    sides = [e for e in zip(f, f[1:] + f[:1]) if und(*e) != m.e0]
    g = nx.Graph(m.Q(s) + sides)
    assert m.is_state(s) and len(g) == len(m.V) and nx.is_tree(g)
    return Panel(m, xy, unit).base().state(s, 's').lines(m.Q(s), 'Q', 1.1).lines(sides, 'bold', 1.5)


def corners(p, chosen, style):
    """A wedge of the paper in the corner v of the face t, for every (t, v) in `chosen`.
    Unlike a state, this may have several corners in one face and none in another."""
    m = p.m
    p.m = SimpleNamespace(A=[t for t, _ in chosen], F=m.F)
    try:
        p.state([v for _, v in chosen], style)
    finally:
        p.m = m
    return p


def face_label(p, face, text, w=6.5, h=6.5):
    """A label at the middle of a white face."""
    i = next(i for i, f in enumerate(p.m.F) if set(f) == set(face))
    assert i in p.m.white
    return p.label(p.cen[i], text, w, h, hi=0.25)


class Plus(Panel):
    """A panel with a wide collar, in which the point of t0 and its three arcs of H^+ fit."""

    def __init__(self, m, xy, unit):
        super().__init__(m, xy, unit)
        self.collar = 0.42 / unit
        ext = R + self.collar + 0.02 / unit
        self.box = [-ext, -ext, ext, ext]
        self.rho = [R + 0.14 / unit, R + 0.29 / unit]
        self.cen[m.t0] = np.array([0.0, -self.rho[0]])

    def tree(self, removed):
        """H^+ without the arcs (t, x) in `removed`, bold; the removed arcs thin and dotted."""
        m = self.m
        arcs = [(t, v) for t in m.A for v in m.F[t]]
        assert set(removed) <= set(arcs)
        for t, v in sorted(arcs, key=lambda a: a not in removed):
            gone = (t, v) in removed
            self.add(rf'\draw[{"gone" if gone else "kept"}] {pt(self.cen[t])} -- {pt(self.xy[v])};')
            self.ob_seg(self.cen[t], self.xy[v], .4 if gone else 1)
        # The arcs from the point of t0 to the roots run in the collar, the one to the far root outside the others.
        for v in m.roots:
            th = math.degrees(math.atan2(self.xy[v][1], self.xy[v][0]))
            far = abs(th - 90) < 1
            rho = self.rho[far]
            end = th if far else (th + 180) % 360 - 180
            self.add(rf'\draw[kept] {pt(self.cen[m.t0])} -- (0,{-rho:.3f}) '
                     rf'arc[start angle=-90,end angle={end:.2f},radius={rho:.3f}] -- {pt(self.xy[v])};')
            for a in np.linspace(-90, end, 60):
                self.ob_disc(rho * np.array([math.cos(math.radians(a)), math.sin(math.radians(a))]), .5)
        return self.points(m.A + [m.t0])


def in_polygon(poly, q):
    """For each row of q, whether this point lies in the polygon."""
    inside = np.zeros(len(q), bool)
    for a, b in zip(poly, poly[1:] + poly[:1]):
        with np.errstate(divide='ignore', invalid='ignore'):
            inside ^= ((a[1] > q[:, 1]) != (b[1] > q[:, 1])) & (q[:, 0] < a[0] + (q[:, 1] - a[1]) * (b - a)[0] / (b - a)[1])
    return inside


class Whites(Panel):
    """A panel with the graph on the white faces: the plane dual of H^+ without the point of t0."""

    def __init__(self, m, xy, unit):
        super().__init__(m, xy, unit)
        self.poly = {}
        self.at = {y: self.place(y) for y in m.white}

    def place(self, y):
        """Where the white face y is drawn as a vertex: at its centre, and in a face with a side
        on the outer circle at a point that also keeps away from the corners."""
        f = self.m.F[y]
        if sum(v in self.roots for v in f) < 2:
            return self.cen[y]
        # The face as a polygon; its corner in X may be reflex, so half-planes do not describe it.
        poly = []
        for a, b in zip(f, f[1:] + f[:1]):
            poly.append(self.xy[a])
            if self.outer(a, b):
                t1 = math.atan2(self.xy[a][1], self.xy[a][0])
                d = (math.atan2(self.xy[b][1], self.xy[b][0]) - t1 + math.pi) % (2 * math.pi) - math.pi
                poly += [R * np.array([math.cos(t1 + k * d / 24), math.sin(t1 + k * d / 24)]) for k in range(1, 24)]
        self.poly[y] = poly
        q = np.array([(u, w) for u in np.linspace(-R, R, 201) for w in np.linspace(-R, R, 201)])
        margin = np.full(len(q), np.inf)
        for a, b in zip(poly, poly[1:] + poly[:1]):
            along = np.clip(((q - a) @ (b - a)) / ((b - a) @ (b - a)), 0, 1)
            margin = np.minimum(margin, np.hypot(*(q - a - np.outer(along, b - a)).T))
        near = np.min([np.hypot(*(q - self.xy[v]).T) for v in f], axis=0)
        return q[np.argmax(np.where(in_polygon(poly, q), np.minimum(margin, 0.3 * near), -1))]

    def leg(self, y, x, end):
        """Points to pass from the vertex of the white face y to the point `end` on a side of y at
        its corner x without leaving y: if x is a reflex corner, by way of a point between x and the circle."""
        if y in self.poly:
            way = np.array([self.at[y] + k / 20 * (end - self.at[y]) for k in range(1, 20)])
            if not in_polygon(self.poly[y], way).all():
                return [self.at[y], self.xy[x] * (np.hypot(*self.xy[x]) + R) / (2 * np.hypot(*self.xy[x]))]
        return [self.at[y]]

    def duals(self, arcs, style):
        """The duals of the arcs (t, x) of H: the dual of (t, x) joins the white faces across the
        two sides of t at x, and is drawn across these two sides, near x."""
        m = self.m
        for t, x in arcs:
            reach = 0.42 * np.hypot(*(self.cen[t] - self.xy[x]))
            ends = []
            for w in (w for w in m.F[t] if w != x):
                side = self.xy[w] - self.xy[x]
                cut = self.xy[x] + min(reach / np.hypot(*side), 0.45) * side
                ends.append([cut] + self.leg(m.white_face(x, w), x, cut)[::-1])
            pts = ends[0][::-1] + ends[1]
            self.add(rf'\draw[{style}] plot[smooth,tension=.6] coordinates {{{" ".join(pt(q) for q in pts)}}};')
            for a, b in zip(pts, pts[1:]):
                self.ob_seg(a, b, 1.6)
        return self

    def white_points(self):
        for q in self.at.values():
            self.add(rf'\draw[line width=.5pt,fill=white] {pt(q)} circle[radius=1.5pt];')
            self.ob_disc(q, 1.8)
        return self


def row(panels, notes, sep):
    """Panels side by side in one common bounding box, with a line of text below each."""
    box = [f(p.box[k] for p in panels) for k, f in enumerate((min, min, max, max))]
    cols = '@{}' + ('c@{\\hspace{' + sep + '}}') * (len(panels) - 1) + 'c@{}'
    below = ' & '.join(rf'\footnotesize ({chr(97 + k)}) {note}' for k, note in enumerate(notes))
    return (rf'\begin{{tabular}}{{{cols}}}' + '\n' + ' &\n'.join(p.tex(box) for p in panels)
            + r'\\[.8mm]' + '\n' + below + '\n' + r'\end{tabular}')


# -- the figures ------------------------------------------------------------------
def fig_descent():
    """The two moves on pairs, and a descent that needs a move which does not lower q."""
    m, xy, T, d = instance('2-factor-without-good-state-16')
    q = lambda r, s: len(Q_cycles(T, r, s))
    key = lambda pair: (tup(m, pair[0]), tup(m, pair[1]))
    pairs = [(r, s) for r in states(T) for s in states(T, avoid=r)]
    assert len(m.V) == 16 and len(pairs) == 18 and Counter(q(*p) for p in pairs) == {0: 12, 1: 6}

    def moves(r, s):
        return ([('D', C, reverse_D(T, r, s, C)) for C in D_cycles(T, r, s)]
                + [('Q', K, reverse_Q(T, r, s, K)) for K in Q_cycles(T, r, s)])

    # The 2-factor of the instance file: one cycle, of length 13, and neither pair has a good second state.
    left_out = {frozenset(f): u for f, u in zip(d['black_faces'], d['unused'])}
    first = [(r, s) for r, s in pairs if all(left_out[frozenset(m.F[t])] not in (r[t], s[t]) for t in m.A)]
    assert len(first) == 2 and all(len(D_cycles(T, r, s)) == 1 and q(r, s) == 1 for r, s in first)
    stuck = [p for p in pairs if q(*p) and all(q(*b) >= q(*p) for _, _, b in moves(*p))]
    assert sorted(map(key, stuck)) == sorted(map(key, first))       # exactly these two have no move that lowers q
    # Start from the one whose cycle runs clockwise.
    r, s = next((r, s) for r, s in first if not m.disk(m.directed_cycles(m.D(tup(m, r), tup(m, s)))[0])['ccw'])

    # A shortest sequence of moves, none of which raises q, to a pair with good second state.
    seen, queue = {key((r, s)): None}, deque([(r, s)])
    while queue:
        a = queue.popleft()
        if q(*a) == 0:
            break
        for kind, cyc, b in moves(*a):
            if q(*b) <= q(*a) and key(b) not in seen:
                seen[key(b)] = (a, kind, cyc)
                queue.append(b)
    path = [(a, None, None)]
    while seen[key(path[0][0])]:
        before, kind, cyc = seen[key(path[0][0])]
        path[0] = (path[0][0], kind, cyc)
        path.insert(0, (before, None, None))
    assert [kind for _, kind, _ in path] == [None, 'Q', 'D']
    (p0, _, _), (p1, _, K), (p2, _, C) = path
    assert p1[1] == p0[1] and [q(*p) for p in (p0, p1, p2)] == [1, 1, 0] and is_good(T, p2[1])
    assert sorted(len(c) for c in D_cycles(T, *p1)) == [3, 3, 7] and len(K) == 3 and len(C) == 3
    Kface = {v for t in K for v in m.F[t] if v != s[t]}             # the vertices of K
    Cface = {p1[0][t] for t in C}                                   # the vertices of C

    panels = [pair_panel(m, xy, 0.47, *key(p)).vertices() for p in (p0, p1, p2)]
    face_label(panels[0], Kface, '$K$', 8, 6.5)
    face_label(panels[1], Kface, '$K$', 8, 6.5)
    face_label(panels[1], Cface, '$C$', 6.5, 6.5)
    notes = ['$(r,s)$:\\ \\ $q(s)=1$', '$(r^K,s)$:\\ \\ $q(s)=1$', '$C$ reversed:\\ \\ $q=0$']
    return row(panels, notes, '3mm'), dict(pairs=len(pairs), stuck=len(stuck), q=[q(*p) for p in (p0, p1, p2)])


def fig_rainbow():
    """A rainbow tree of excess 2 and the exchange that brings it to excess 0."""
    m, xy, T = running()
    I = sf.Inst(m.F, m.t0)
    assert I.A == [tuple(sorted(m.F[t])) for t in m.A]
    trees = I.rainbow_trees()
    assert len(trees) == 1792 and Counter(map(I.excess, trees)) == {0: 6, 2: 168, 4: 692, 6: 776, 8: 150}
    assert all(len(I.alts(sig, x)) == 1 for sig in trees for x in I.X)          # one exchange for each x
    inverse = lambda sig: {m.A[i]: x for x, i in sig.items()}
    good = sorted(tup(m, s) for s in states(T) if is_good(T, s))
    assert good == sorted(tup(m, inverse(sig)) for sig in trees if I.excess(sig) == 0)

    # The exchange of Figure 1 of the note sign-free: the vertex 2 moves from the face {1,2,9} to the face {0,2,3}.
    x, old, new = 2, I.A.index((1, 2, 9)), I.A.index((0, 2, 3))
    sig = min((sig for sig in trees if I.excess(sig) == 2 and sig[x] == old and I.alt(sig, x) == new
               and I.excess({**sig, x: new}) == 0), key=lambda sig: sf.key(I, sig))
    after = {**sig, x: new}
    assert I.load(sig)[old] == 2 and I.load(sig)[new] == 0 and tup(m, inverse(after)) in good
    change = Counter(I.excess({**sig, y: I.alt(sig, y)}) - 2 for y in I.X)

    panels = []
    for g in (sig, after):
        chosen = [(m.A[i], y) for y, i in g.items()]
        assert I.is_rainbow(g)
        p = Plus(m, xy, 0.66).base()
        corners(p, chosen, 's').tree(chosen).vertices()
        p.label(xy[x], '$x$', 5.5, 5, lo=0.16)
        for name, i in (('$t$', old), ("$t'$", new)):
            p.label(p.cen[m.A[i]], name, 6, 7, lo=0.1, hi=0.9, grey_ok=True)
        panels.append(p)
    return row(panels, ['excess $2$', 'excess $0$'], '8mm'), dict(change=dict(change))


def contraction(m, v, a, b):
    """The triangulation left when the vertex v of degree four is removed and its opposite
    neighbours a and b are identified; None if it is not simple. The new vertex is called a
    (b if b is a root). Also returns, for each face of the new triangulation, the face of T it was."""
    if b in m.roots:
        a, b = b, a
    assert m.T.degree(v) == 4 and not m.T.has_edge(a, b) and b not in m.roots
    was = [i for i, f in enumerate(m.F) if v not in f]
    faces = [tuple(a if w == b else w for w in m.F[i]) for i in was]
    arcs = [e for f in faces for e in zip(f, f[1:] + f[:1])]
    if len(set(arcs)) < len(arcs):
        return None
    return Model(faces, was.index(m.t0), tuple(a if w == b else w for w in m.e0)), a, b, was


def extension(m, v, a, b, small, was, s):
    """The extension to T of the state s of the contraction: the other faces keep their corners,
    and the two black faces at v take v and whichever of a, b is still free."""
    out = {}
    for t, x in zip(small.A, s):
        out[was[t]] = b if x == a and b in m.F[was[t]] else x
    free, = {a, b} - set(out.values()) - set(m.roots)
    for t in m.A:
        if v in m.F[t]:
            out[t] = free if free in m.F[t] else v
    return tuple(out[t] for t in m.A)


def settle(m, target, weight=4.0):
    """A layout of m with its vertices near the places `target`: the descent of model.relax, started
    from the Tutte embedding, on the energy of the paper plus the squared distances to the targets."""
    third, = set(m.roots) - set(m.e0)
    a, b = m.e0 if m.left[m.e0] != m.t0 else m.e0[::-1]
    xy = tutte(m, {v: R * np.array([math.cos(math.radians(t)), math.sin(math.radians(t))])
                   for v, t in zip((a, b, third), ROOT_ANGLES)})
    cost = lambda: energy(m, xy) + weight * sum(float(np.sum((xy[v] - target[v]) ** 2)) for v in m.X)
    best, step = cost(), 0.4
    assert math.isfinite(best)
    dirs = [np.array([math.cos(t), math.sin(t)]) for t in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
    while step > 1e-4:
        moved = False
        for v in m.X:
            for d in dirs:
                old = xy[v].copy()
                xy[v] = old + step * d
                c = cost()
                if c < best - 1e-12:
                    best, moved = c, True
                else:
                    xy[v] = old
        if not moved:
            step /= 2
    return xy


def fig_contraction():
    """Removing a vertex of degree four, and a good state that extends."""
    m, xy, T = running()
    good = lambda mm, s: is_good(triangulation(mm), dict(zip(mm.A, s)))
    assert sum(good(m, s) for s in m.states()) == 6
    v = 10
    link = [m.F[i][(m.F[i].index(v) + 1) % 3] for i in range(len(m.F)) if v in m.F[i]]
    assert m.T.degree(v) == 4 and sorted(link) == [4, 8, 9, 11]
    counts = {}
    for a, b in ((9, 11), (4, 8)):
        small, a, b, was = contraction(m, v, a, b)
        gs = [s for s in small.states() if good(small, s)]
        ext = [extension(m, v, a, b, small, was, s) for s in gs]
        assert all(m.is_state(e) for e in ext)
        counts[a, b] = (len(small.V), len(small.pairs()), len(gs), sum(good(m, e) for e in ext))
    assert counts == {(9, 11): (11, 4, 4, 3), (4, 8): (11, 4, 4, 2)}

    small, a, b, was = contraction(m, v, 9, 11)
    s = next(s for s in small.states() if good(small, s) and good(m, extension(m, v, a, b, small, was, s)))
    e = extension(m, v, a, b, small, was, s)
    xy2 = settle(small, {w: xy[v] if w == a else xy[w] for w in small.V})

    unit = 0.47
    at_v = [i for i in range(len(m.F)) if v in m.F[i]]
    p0 = Panel(m, xy, unit).base(tint=[i for i in at_v if i in m.white]).lines([(v, a), (v, b)], 'bold', 1.5).vertices()
    p0.label(xy[v], '$v$', 5.5, 5, lo=0.16)
    p0.label(xy[a], '$a$', 5.5, 5, lo=0.16)
    p0.label(xy[b], '$b$', 5, 7, lo=0.16)
    p1 = good_panel(small, xy2, unit, s).vertices()
    p1.label(xy2[a], '$a{=}b$', 19, 7, lo=0.16)
    p2 = good_panel(m, xy, unit, e).vertices()
    p2.label(xy[v], '$v$', 5.5, 5, lo=0.16)
    notes = ['$T$', "$T'$ and a good state", 'its extension to $T$']
    return row([p0, p1, p2], notes, '3mm'), {f'{a}={b}': c for (a, b), c in counts.items()}


def family(j):
    """The triangulation T_j with 3j+2 vertices: a double pyramid with apices 0 and 1 over the
    2j-gon x_0 y_0 x_1 y_1 ..., in which every edge from 1 to x_i is subdivided by z_i and z_i is
    joined to y_(i-1) and y_i. The roots are 0, x_0, y_0, and 0 is drawn at the top."""
    x, y, z = (lambda i, k=k: k + 3 * (i % j) for k in (2, 3, 4))
    edges = [e for i in range(j) for e in ((0, x(i)), (0, y(i)), (x(i), y(i)), (x(i), y(i - 1)),
                                           (1, y(i)), (1, z(i)), (z(i), y(i)), (z(i), y(i - 1)), (z(i), x(i)))]
    return from_graph(edges, (x(0), y(0), 0))


def fig_family():
    """The family with one 2-factor of H, with j - 1 cycles."""
    panels, notes, facts = [], [], {}
    for j in (3, 4, 5):
        m, xy, T = family(j)
        Fs = two_factors(m)
        g = sum(is_good(T, s) for s in states(T))
        assert len(m.V) == 3 * j + 2 and separating_triangle(T) is None and len(Fs) == 1
        F, = Fs
        assert sorted((k['h'], k['W']) for k in F['disks']) == [(3, 1)] * (j - 2) + [(5, 2)]
        assert len(F['pairs']) == g == 2 ** (j - 1) and all(is_good(T, dict(zip(m.A, s))) for _, s in F['pairs'])
        p = Panel(m, xy, 0.47).base(tint={w for k in F['disks'] for w in k['white']}).graphH(F['arcs']).vertices()
        for k in F['disks']:
            w = max(k['white'], key=lambda w: min(np.hypot(*(p.cen[w] - xy[u])) for u in m.F[w]))
            p.label(p.cen[w], f'${k["W"]}$', 4.25, 5.4, hi=0.1)
        panels.append(p)
        notes.append(f'$j={j}$:\\ \\ $m={j - 1}$,\\ \\ $g={g}$')
        facts[j] = dict(V=len(m.V), m=len(F['disks']), g=g)
    return row(panels, notes, '3mm'), facts


def fig_trees():
    """The two trees in a 2-factor of H, and a tree with one edge at every face."""
    m, xy, T, d = instance('2-factor-without-good-state-16')
    I = sf.Inst(m.F, m.t0)
    assert I.A == [tuple(sorted(m.F[t])) for t in m.A]
    n = len(m.A)
    left_out = {frozenset(f): u for f, u in zip(d['black_faces'], d['unused'])}
    F = [(i, x) for i in range(n) for x in I.A[i] if x != left_out[frozenset(I.A[i])]]
    at = {x: [i for i, y in F if y == x] for x in m.X}
    assert len(F) == 2 * n and all(len(at[x]) == 2 for x in m.X)
    tree = lambda arcs: I.w_tree(arcs) and I.h_tree(set(arcs))
    # Splits into two spanning trees with one edge at every x: one face of F at each x, and the other.
    splits = []
    for bits in product((0, 1), repeat=n - 1):
        one = [(at[x][b], x) for x, b in zip(m.X, (0,) + bits)]
        two = [a for a in F if a not in one]
        if tree(one) and tree(two):
            splits.append((one, two))
    # Spanning trees with one edge at every t.
    per_face = []
    for bits in product((0, 1), repeat=n):
        arcs = [[a for a in F if a[0] == i][b] for i, b in enumerate(bits)]
        if tree(arcs):
            per_face.append(arcs)
    excess = lambda arcs: sum(abs(sum(a[1] == x for a in arcs) - 1) for x in m.X)
    assert splits and per_face and min(map(excess, per_face)) == 2          # no tree meets both conditions
    load = lambda arcs: [sum(a[0] == i for a in arcs) for i in range(n)]
    excess_t = lambda arcs: sum(abs(c - 1) for c in load(arcs))
    one, two = min(splits, key=lambda s: (excess_t(s[0]), sorted(s[0])))
    third = min((a for a in per_face if excess(a) == 2), key=sorted)
    twice, = [x for x in m.X if sum(a[1] == x for a in third) == 2]
    never, = [x for x in m.X if sum(a[1] == x for a in third) == 0]

    face = lambda arcs: [(m.A[i], x) for i, x in arcs]
    unit = 0.7
    p0 = Whites(m, xy, unit).base().duals(face(one), 'one').duals(face(two), 'two').white_points().vertices()
    p1 = Whites(m, xy, unit).base().duals(face([a for a in third if a in one]), 'one')
    p1.duals(face([a for a in third if a in two]), 'two').white_points().vertices()
    p1.label(xy[twice], '$x$', 5.5, 5, lo=0.16, hi=1.2, grey_ok=True)
    p1.label(xy[never], "$x'$", 7.5, 7, lo=0.16, hi=1.2, grey_ok=True)
    notes = ['two trees, one edge of each at every $x$', 'a tree with one edge at every $t$']
    return row([p0, p1], notes, '8mm'), dict(splits=len(splits), per_face=len(per_face),
                                                     loads=(load(one), load(two)), twice=twice, never=never)


FIGURES = {'descent': fig_descent, 'rainbow': fig_rainbow, 'contraction': fig_contraction,
           'family': fig_family, 'trees': fig_trees}


def document(body):
    """The figure centred in a box as wide as the text of the paper, so that all figures have one scale."""
    return (PREAMBLE + STYLES + r'\setbox0\hbox{%' + '\n' + body + '%\n}%\n'
            + rf'\ifdim\wd0>{TEXTWIDTH}cm\errmessage{{The figure is wider than the text}}\fi' + '\n'
            + rf'\hbox to {TEXTWIDTH}cm{{\hss\box0\hss}}%' + '\n\\end{document}\n')


def main(names):
    for name in names or FIGURES:
        body, facts = FIGURES[name]()
        tex = document(body)
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'fig.tex').write_text(tex, encoding='utf-8')
            z = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'fig.tex'],
                               cwd=tmp, capture_output=True, text=True, errors='replace')
            if z.returncode or 'Overfull' in z.stdout:
                raise SystemExit(z.stdout[-3000:])
            subprocess.run(['pdftocairo', '-svg', 'fig.pdf', 'fig.svg'], cwd=tmp, check=True, capture_output=True)
            svg = Path(tmp, 'fig.svg').read_text(encoding='utf-8')
        x, y, w, h = map(float, re.search(r'viewBox="([^"]+)"', svg).group(1).split())
        svg = re.sub(r'width="[^"]+" height="[^"]+"', f'width="{WIDTH}" height="{WIDTH * h / w:.0f}"', svg, count=1)
        end = svg.index('>', svg.index('<svg')) + 1
        svg = svg[:end] + f'\n<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white"/>' + svg[end:]
        (HERE / f'open-{name}.svg').write_text(svg, encoding='utf-8')
        print(f'open-{name}.svg', facts)


if __name__ == '__main__':
    main(sys.argv[1:])
