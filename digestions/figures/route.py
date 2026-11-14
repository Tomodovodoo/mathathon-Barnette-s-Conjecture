"""Draw the figures for Section 1 of digestions/routes.md, the route of the paper.

    python route.py            all six
    python route.py disk       only route-disk.svg

All six take a few minutes, most of it in the layout of the two examples.

    route-construction.svg   Figure 1 of the paper: matching, dual, good state, cycle, pair
    route-disk.svg           the disk identity (Lemma 2.9) on three cycles
    route-cancel.svg         reversing a cycle of Q_s (Lemmas 3.4 and 3.5)
    route-count.svg          the eight pairs of the example and Z(z) (Lemma 4.7, Proposition 4.9)
    route-pair.svg           the flow network and the edge count (Lemmas 5.1 and 5.3, Proposition 5.5)
    route-induction.svg      cutting along a separating triangle (Theorem 5.6)

The drawing code, the layout and the style are those of paper/figures (figures.py,
model.py), imported from there; this file only adds what the six figures need
beyond the paper's three. Everything drawn is computed from paper/figures/running.json
(the example of Figure 2 of the paper) and from two octahedra glued along a face
(barnette.examples.two_cubes), with workings/barnette for signs, weights, the flow
and the cut; every number in a label is asserted here.

Each figure is written as TikZ, compiled with pdflatex in a temporary directory and
converted to SVG with PyMuPDF, text as outlines, at one scale for all figures, on a
white background 720 px wide.
"""
import copy
import functools
import itertools
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / 'paper' / 'figures'), str(ROOT / 'workings')]

import barnette as bn                                    # noqa: E402
import figures as pf                                     # noqa: E402
from figures import Panel, pt                            # noqa: E402
from model import Model, layout, load, und               # noqa: E402

WIDTH = 720                              # px, the width of every SVG
MARGIN = 12                              # px of white around the drawing
SCALE = (WIDTH - 2 * MARGIN) / (pf.TEXTWIDTH / 2.54 * 72)    # px per TeX point: the text width of the paper fills the SVG

EXTRA = r'''\colorlet{rtdark}{black!30}% a black face that is singled out
\colorlet{rttint}{bfS!40}% a white face inside two cycles
\tikzset{
  U/.style={draw=black,line width=1.15pt},
  ring/.style={draw=black,line width=.7pt},
}
'''


# -- helpers on top of the paper's Panel ---------------------------------------
def fill(p, faces, colour):
    """Fill some bounded faces again, in another colour, and redraw their sides."""
    for i in faces:
        p.add(rf'\fill[{colour}] {p.face_path(i)};')
    sides = sorted({und(a, b) for i in faces for a, b in zip(p.m.F[i], p.m.F[i][1:] + p.m.F[i][:1])})
    for a, b in sides:
        p.add(rf'\draw[edge] {p.edge_path(a, b)};')
    return p


def wedges(p, state, style, faces):
    """Panel.state for some of the faces in A only."""
    q, q.m = copy.copy(p), copy.copy(p.m)            # q shares the layers and obstacles of p
    q.m.A = list(faces)
    q.state([state[p.m.A.index(t)] for t in faces], style)
    return p


def ring(p, vertices):
    for v in vertices:
        p.add(rf'\draw[ring] {pt(p.xy[v])} circle[radius=3.3pt];')
        p.ob_disc(p.xy[v], 3.7)
    return p


def table(rows, sep):
    """Rows of (panel, label) cells, all panels in one common bounding box, the
    labels below. A row may also be a string, which is set as a line of its own."""
    panels = [c for row in rows if not isinstance(row, str) for c, _ in row if isinstance(c, Panel)]
    box = [f(p.box[k] for p in panels) for k, f in enumerate((min, min, max, max))]
    width = max(len(row) for row in rows if not isinstance(row, str))
    out = [r'\begin{tabular}{@{}' + ('c@{\\hspace{' + sep + '}}') * (width - 1) + 'c@{}}']
    for row in rows:
        if isinstance(row, str):
            out.append(rf'\multicolumn{{{width}}}{{@{{}}c@{{}}}}{{\footnotesize {row}}}\\[2.2mm]')
        else:
            out.append(' &\n'.join(c.tex(box) if isinstance(c, Panel) else c for c, _ in row) + r'\\[.6mm]')
            out.append(' & '.join(rf'\footnotesize {label}' for _, label in row) + r'\\[1.6mm]')
    return '\n'.join(out + [r'\end{tabular}'])


def lines(*text):
    return r'\begin{tabular}[t]{@{}c@{}}' + r'\\[-.2mm]'.join(text) + r'\end{tabular}'


# -- the two examples -----------------------------------------------------------
def triangulation(m):
    """The triangulation of a Model as workings/barnette has it, with the same face numbers."""
    return bn.Triangulation(dict(enumerate(m.F)), m.t0, m.e0)


@functools.lru_cache(None)
def running():
    """The example of Figure 2 of the paper, and its two pairs with the same second state
    s that is not good: (r, s), the pair of Figure 2(a), and (r^K, s) for the cycle K of Q_s."""
    m, xy = load('running.json')
    T = triangulation(m)
    assert T.A == m.A
    Fs = pf.two_factors(m)
    assert len(Fs) == 2 and [[k['W'] for k in F['disks']] for F in Fs] == [[6, 1], [3, 1]]
    seconds = [s for F in Fs for _, s in F['pairs']]
    bad, = [s for s in set(seconds) if not pf.is_good(m, s)[0]]
    (r, s), = [q for q in Fs[0]['pairs'] if q[1] == bad]
    (rK, _), = [q for q in Fs[1]['pairs'] if q[1] == bad]
    K, = m.directed_cycles(m.Q_directed(r, s))
    i = K.index(min(K))
    K = K[i:] + K[:i]
    assert K == [1, 9, 8]
    d = lambda state: dict(zip(m.A, state))                                   # noqa: E731
    faces, = bn.Q_cycles(T, d(r), d(s))
    assert bn.reverse_Q(T, d(r), d(s), faces)[0] == d(rK)                      # r^K as in the paper
    return dict(m=m, xy=xy, T=T, Fs=Fs, r=r, s=s, rK=rK, K=K, Kfaces=sorted(faces), d=d)


@functools.lru_cache(None)
def glued():
    """Two octahedra glued along a face: the dual of two cubes joined by three edges.
    With t0 as chosen here the three faces along the inner side of the separating
    triangle are black, and there is no pair. Vertices are renumbered: 0, 1, 2 the roots
    with e0 = {0, 1}; 2, 3, 4 the separating triangle; 6, 7, 8 the vertices inside it."""
    G = bn.examples.two_cubes()
    T0 = bn.dual_triangulation(G, next(iter(G.edges())))
    delta = bn.separating_triangle(T0)
    t0 = next(t for t, f in T0.faces.items()
              if len(set(f) & set(delta)) == 1 and bn.first_pair(bn.Triangulation(T0.faces, t, f[:2])) is None)
    top, = set(T0.faces[t0]) & set(delta)
    a, b = (v for v in T0.faces[t0] if v != top)
    first, _ = bn.pieces(bn.Triangulation(T0.faces, t0, (a, b)), delta)
    outer = {v for f in first.values() for v in f}
    rest = sorted(set(delta) - {top}) + sorted(outer - set(delta) - {a, b}) + sorted(set(T0.vertices) - outer)
    name = dict(zip([a, b, top] + rest, range(9)))
    faces = [tuple(name[v] for v in f) for f in T0.faces.values()]
    m = Model(faces, list(T0.faces).index(t0), (0, 1))
    T = triangulation(m)
    assert bn.first_pair(T) is None and set(bn.separating_triangle(T)) == {2, 3, 4}
    return m, layout(m), T


# -- Figure: the construction (Figure 1 of the paper) ------------------------------
def fig_construction():
    return pf.fig_overview()


# -- Figure: the disk identity -------------------------------------------------------
def fig_disk():
    """Lemma 2.9 on three cycles of the example: the long cycles of D(r,s) and of
    D(r^K,s), and the cycle K of Q_s."""
    e = running()
    m, xy = e['m'], e['xy']
    longest = lambda state: max(m.directed_cycles(m.D(state, e['s'])), key=len)   # noqa: E731
    cases = [(e['r'], longest(e['r']), 'D', 1.1), (e['rK'], longest(e['rK']), 'D', 1.1), (e['r'], e['K'], 'K', 1.5)]
    row, seen = [], []
    for n, (state, C, style, w) in enumerate(cases):
        k = m.disk(C)
        arcs = list(zip(C, C[1:] + C[:1]))
        on = [m.black_face(a, b) for a, b in arcs]              # the faces t_f
        assert len(set(on)) == k['h'] and set(on) <= set(m.A)
        assert all(state[m.A.index(t)] == a for t, (a, b) in zip(on, arcs))     # r(t_f) is the tail of f
        assert k['B'] == k['I'] + k['l'] and k['W'] == k['B'] + 1 and k['h'] == 2 * k['l'] + 3
        p = Panel(m, xy, 0.47).base(tint=k['white'])
        fill(p, k['black'], 'rtdark')
        wedges(p, state, 'r', sorted(set(on) | set(k['black'])))
        p.arrows(arcs, style, w).vertices().vertex_labels()
        seen.append((k['h'], k['l'], k['I'], k['B'], k['W']))
        row.append((p, rf'({chr(97 + n)}) $h={k["h"]}$, $\ell={k["l"]}$, $I={k["I"]}$, $B={k["B"]}$, $W={k["W"]}$'))
    assert seen == [(7, 2, 3, 5, 6), (7, 2, 0, 2, 3), (3, 0, 0, 0, 1)]
    return table([row], '2.5mm')


# -- Figure: the cancellation ---------------------------------------------------------
def fig_cancel():
    """The two pairs (r, s) and (r^K, s): the same second state, opposite signs."""
    e = running()
    m, xy, T, d = e['m'], e['xy'], e['T'], e['d']
    K = list(zip(e['K'], e['K'][1:] + e['K'][:1]))
    inside, = m.disk(e['K'])['white']
    row = []
    for n, (state, name, k_arcs) in enumerate([(e['r'], 'r', K), (e['rK'], 'r^K', [(b, a) for a, b in K])]):
        assert set(k_arcs) <= set(m.Q_directed(state, e['s']))
        eps = bn.sign(T, d(state), d(e['s']))
        assert eps == (-1) ** (n + 1)
        moved = [t for t in m.A if e['r'][m.A.index(t)] != e['rK'][m.A.index(t)]]
        assert moved == e['Kfaces'] and len(moved) == 3
        p = Panel(m, xy, 0.66).base()
        fill(p, moved, 'rtdark')
        p.state(state, 'r').state(e['s'], 's').arrows(m.D(state, e['s'])).arrows(k_arcs, 'K', 1.5)
        p.vertices().vertex_labels()
        p.label(p.cen[inside], '$K$', 8, 6.5, hi=0.25)
        row.append((p, rf'({chr(97 + n)}) the pair $({name},s)$, with $\varepsilon({name},s)={eps:+d}$'))
    cyc = [sorted(m.disk(c)['W'] for c in m.directed_cycles(m.D(q, e['s']))) for q in (e['r'], e['rK'])]
    assert cyc == [[1, 6], [1, 3]]
    return table([row], '5mm')


# -- Figure: the count ------------------------------------------------------------------
def poly_add(p, q):
    out = dict(p)
    for k, c in q.items():
        out[k] = out.get(k, 0) + c
    return {k: c for k, c in out.items() if c}


def poly_mul(p, q):
    out = {}
    for (i, a), (j, b) in itertools.product(p.items(), q.items()):
        out[i + j] = out.get(i + j, 0) + a * b
    return {k: c for k, c in out.items() if c}


def power(k):
    return '1' if k == 0 else 'z' if k == 1 else f'z^{{{k}}}'


def fig_count():
    """All eight pairs, one row for each 2-factor of H, each with its term of Z(z)."""
    e = running()
    m, xy, T, d = e['m'], e['xy'], e['T'], e['d']
    n = len(m.A)
    w0 = min(bn.weight(T, d(F['s'])) for F in e['Fs'])
    rows, Z, framed = [], {}, []
    for F in e['Fs']:
        c = len(F['disks'])
        wF = bn.weight(T, d(F['s']))
        product = {wF - w0: (-1) ** ((n + c) // 2)}
        for k in F['disks']:
            product = poly_mul(product, {0: 1, k['W']: -1})
        cells, total = [], {}
        for r, s in sorted(F['pairs'], key=lambda q: bn.weight(T, d(q[1]))):
            disks = [m.disk(C) for C in m.directed_cycles(m.D(r, s))]
            ccw = [k for k in disks if k['ccw']]
            eps, w = bn.sign(T, d(r), d(s)), bn.weight(T, d(s))
            assert eps == (-1) ** ((n + c) // 2 + len(ccw))                       # (4.3)
            assert w == wF + sum(k['W'] for k in ccw)                             # Lemma 4.6
            depth = {y: sum(y in k['white'] for k in ccw) for y in m.white}
            assert sum(depth.values()) == w - wF
            p = Panel(m, xy, 0.335).base(tint=[y for y in depth if depth[y] == 1])
            fill(p, [y for y in depth if depth[y] == 2], 'rttint')
            p.state(s, 's').arrows(m.D(r, s))
            Ks = m.directed_cycles(m.Q_directed(r, s))
            assert bool(Ks) == (not pf.is_good(m, s)[0])
            for C in Ks:
                p.arrows(list(zip(C, C[1:] + C[:1])), 'K', 1.5)
            p.vertices()
            term = f'${"+" if eps > 0 else "-"}{power(w - w0)}$'
            if Ks:
                framed.append((eps, w - w0, s))
                term = r'\setlength{\fboxsep}{1.6pt}\fbox{' + term + '}'
            cells.append((p, term))
            total = poly_add(total, {w - w0: eps})
        assert total == product
        Z = poly_add(Z, total)
        factors = ''.join(f'(1-{power(k["W"])})' for k in sorted(F['disks'], key=lambda k: k['W']))
        sign = '' if (-1) ** ((n + c) // 2) > 0 else '-'
        lead = '' if wF == w0 else power(wF - w0)
        rows += [cells, rf'the four terms add up to ${sign}{lead}{factors}$']
    assert Z == {0: 1, 1: -1, 2: 1, 3: -1, 5: -1, 7: 1} and w0 == -5              # the polynomial of the paper
    assert len(framed) == 2 and framed[0][1:] == framed[1][1:] and framed[0][0] == -framed[1][0]
    assert sum(pf.is_good(m, s)[0] for s in m.states()) == 6
    return table(rows, '2mm')


# -- Figure: a pair exists ----------------------------------------------------------------
def network(m, T, height):
    """The flow network of Lemma 5.1 with the maximum flow found by workings/barnette."""
    r, s = bn.first_pair(T)
    cycles = bn.D_cycles(T, r, s)
    assert sorted(t for C in cycles for t in C) == sorted(T.A) and len(cycles) == 2
    flow = {(t, x) for state in (r, s) for t, x in state.items()}
    assert len(flow) == 2 * T.n
    xs, xa, dy, gap = 1.15, 3.55, 0.385, 0.3
    fs, fa = xs - 0.5, xa + 1.13                  # where the edges at the source and at the sink fan out
    xq = fa + fs
    yx, ya, y = {}, {}, 0.0
    for C in sorted(cycles, key=len, reverse=True):
        for t in C:                              # the cycle runs r(t) - t - s(t) = r(t') - t' - ...
            yx[r[t]], ya[t] = y, y
            y -= dy
        y -= gap
    mid = (y + dy + gap) / 2
    src, snk = (0.0, mid), (xq, mid)
    L = []
    for x in T.X:
        L.append(rf'\draw[H] {pt(src)} -- {pt((fs, yx[x]))} -- {pt((xs, yx[x]))};')
    for t in T.A:
        L.append(rf'\draw[H] {pt((xa, ya[t]))} -- {pt((fa, ya[t]))} -- {pt(snk)};')
    arcs = [(t, x) for t in T.A for x in T.faces[t] if x not in T.roots]
    for t, x in sorted(arcs, key=lambda a: a in flow):
        L.append(rf'\draw[{"F" if (t, x) in flow else "H"}] {pt((xs, yx[x]))} -- {pt((xa, ya[t]))};')
    for x in T.X:
        L.append(rf'\fill {pt((xs, yx[x]))} circle[radius=1.3pt];')
        L.append(rf'\node[anchor=east,fill=white,inner sep=1.2pt] at {pt((xs - 0.07, yx[x]))} {{${x}$}};')
    for t in T.A:
        L.append(rf'\fill {pt((xa, ya[t]))} ++(-1.5pt,-1.5pt) rectangle ++(3pt,3pt);')
        name = r'\,'.join(str(v) for v in sorted(T.faces[t]))
        L.append(rf'\node[anchor=west,fill=white,inner sep=1.2pt] at {pt((xa + 0.07, ya[t]))} {{${name}$}};')
    for q in (src, snk):
        L.append(rf'\draw[root] {pt(q)} circle[radius=2pt];')
    top, bottom = 0.42, y + gap + dy - 0.42
    L.append(rf'\node at {pt((xs, top))} {{$X$}};')
    L.append(rf'\node at {pt((xa, top))} {{$A$}};')
    for x, c in ((fs / 2, 2), ((xs + xa) / 2, 1), ((fa + xq) / 2, 2)):
        L.append(rf'\node at {pt((x, bottom))} {{${c}$}};')
    y0 = (top + 0.2 + bottom - 0.2 - height) / 2
    return '\n'.join([r'\begin{tikzpicture}[bf,x=1cm,y=1cm]',
                      rf'\path[use as bounding box] (-0.1,{y0:.3f}) rectangle ({xq + 0.1:.3f},{y0 + height:.3f});']
                     + L + [r'\end{tikzpicture}'])


def cut_panel(m, xy, unit, S):
    """A set S as in (5.2) (ringed), the number min(2, |V(t) & S|) in every
    face t of A that has a corner in S, and the edges with both ends in U = V(T) - S."""
    S = set(S)
    U = set(m.V) - S
    assert S <= set(m.X)
    nums = {t: min(2, len(set(m.F[t]) & S)) for t in m.A}
    eU = [e for e in m.E if set(e) <= U]
    bU = sum(set(m.F[t]) <= U for t in m.black)
    assert len(eU) - bU == 2 * len(m.A) + 2 - sum(nums.values())                  # the identity in the proof
    p = Panel(m, xy, unit).base().lines(eU, 'U', 1.15).vertices()
    ring(p, S)
    for t in m.A:
        if nums[t]:
            p.label(p.cen[t], f'${nums[t]}$', 4.25, 5.4, hi=0.12, grey_ok=True)
    return p, dict(S=len(S), U=len(U), sum=sum(nums.values()), terms=[k for k in nums.values() if k], e=len(eU), b=bU)


def compare(a, b):
    """'a < b', 'a > b', or just 'a' if the two are equal."""
    return f'{a}' if a == b else f'{a}{"<" if a < b else ">"}{b}'


def fig_pair():
    """The network, a set S for which the cut condition is tight, and one for which it fails."""
    e = running()
    m, xy, T = e['m'], e['xy'], e['T']
    g, gxy, gT = glued()
    unit = 0.44
    a, da = cut_panel(m, xy, unit, {6, 7, 12})
    b, db = cut_panel(g, gxy, unit, {6, 7, 8})
    assert (da['sum'], 2 * da['S'], da['e'] - da['b'], 2 * da['U'] - 4) == (6, 6, 16, 16)
    assert (db['sum'], 2 * db['S'], db['e'] - db['b'], 2 * db['U'] - 4) == (5, 6, 9, 8)
    assert bn.first_pair(T) is not None and bn.separating_triangle(T) is None
    assert bn.first_pair(gT) is None and set(bn.separating_triangle(gT)) == {2, 3, 4}
    a.vertex_labels(only={6, 7, 12})
    b.vertex_labels(only={2, 3, 4})
    cells = [(network(m, T, (a.box[3] - a.box[1]) * unit), '(a)')]
    for n, d in enumerate((da, db)):
        cells.append(((a, b)[n], lines(
            rf'({chr(98 + n)}) ${"+".join(map(str, d["terms"]))}={compare(d["sum"], 2 * d["S"])}=2|S|$,',
            rf'$e(U)-b(U)={compare(d["e"] - d["b"], 2 * d["U"] - 4)}=2|U|-4$')))
    return table([cells], '3mm')


# -- Figure: the induction -------------------------------------------------------------------
def white_outside(p):
    """Panel.base for a triangulation that is drawn with a white face as the unbounded face."""
    p.base()
    assert p.out[0].startswith(r'\fill[bfblack,even odd rule]')
    del p.out[0]
    return p


def fig_induction():
    """Theorem 5.6 on the two glued octahedra: G_1 and G_2 with their Hamiltonian
    cycles, and the Hamiltonian cycle of G that they give."""
    m, xy, T = glued()
    delta = (2, 3, 4)
    sides = [und(2, 3), und(3, 4), und(2, 4)]
    first, second = bn.pieces(T, delta)
    cap = ('cap', delta)

    def piece(faces, t0, e0):
        keys = list(faces)
        return Model([faces[k] for k in keys], keys.index(t0), e0), keys

    # T_1: the side of t0. The cycle C_1 avoids the dual of e0 and uses two of f_1, f_2, f_3.
    m1, keys1 = piece(first, m.t0, m.e0)
    v1 = keys1.index(cap)
    assert v1 in m1.black and pf.is_good(m1, m1.states()[0])[0]
    C1 = pf.recover(m1, m1.states()[0])['cycle']
    used = sorted((m1.cross[g] for g in C1 if v1 in g), key=sides.index)
    f3, = [s for s in sides if s not in used]
    f = dict(zip(used + [f3], (1, 2, 3)))                           # the names f_1, f_2, f_3 of the duals of the sides
    # T_2: the other side. Its new face is white in the colouring of T. Exchanging the two
    # colours makes it the black face t0 of T_2 at the side dual to f_3, and the cycle C_2 avoids f_3.
    m2, keys2 = piece(second, cap, f3)
    v2 = m2.t0
    good = [s for s in m2.states() if pf.is_good(m2, s)[0]]
    C2 = pf.recover(m2, good[0])['cycle']
    assert sorted(m2.cross[g] for g in C2 if v2 in g) == sorted(used)
    # The cycle of G: C_1 - v_1, C_2 - v_2, f_1 and f_2.
    glue = [m.dual[m1.cross[g]] for g in C1 if v1 not in g] + [m.dual[m2.cross[g]] for g in C2 if v2 not in g]
    glue += [m.dual[s] for s in used]
    H = nx.Graph(glue)
    order = [m.t0] + [b for _, b in nx.dfs_edges(H, m.t0)]
    assert bn.is_hamiltonian_cycle(m.G, order, avoid=m.dual[m.e0]) and len(glue) == len(m.F)
    assert (len(m.V), len(m1.V), len(m2.V), len(m.F), len(m1.F), len(m2.F)) == (9, 6, 6, 14, 8, 8)

    def names(p, model, outside=False):                             # f_1, f_2, f_3 where they cross the triangle
        for side in sides:
            g = model.dual[side]
            a, _, _, b = p.dual_curve(g if g[1] != model.t0 else g[::-1])[0]
            p.label(0.45 * a + 0.55 * b if outside else b, f'$f_{f[side]}$', 8.5, 8, lo=0.16, hi=0.8, grey_ok=True)

    def panel(model, coords):
        return Panel(model, coords, 0.46)

    # (a) T_1, in its place in T, with G_1 and C_1
    a = panel(m1, {v: xy[v] for v in m1.V}).base().lines(sides, 'U', 1.15)
    a.graphG(m1.G.edges(), 'G', .35).graphG(C1, 'ham', 1.2, smooth=True).dotsG().vertices()
    names(a, m1)
    a.label(a.cen[v1], '$v_1$', 8.5, 6.5, lo=0.14, hi=0.5, grey_ok=True)
    # (b) T_2 with G_2 and C_2, drawn with its new face outside and the corner 2 on top
    md = copy.copy(m2)
    md.e0 = und(3, 4)
    xy2 = layout(md)
    md.black, md.white = m2.white, m2.black                          # back to the colours of T
    md.A = list(md.black)
    assert all((keys2[i] in T.black) == (i in md.black) for i in range(len(keys2)) if i != v2)
    b = panel(md, xy2)
    for i in md.black:                           # a black face at the circle: place its vertex of G as in a white one
        md.black = []
        b.cen[i] = b.centre(i)
        md.black = list(md.A)
    white_outside(b).lines(sides, 'U', 1.15)
    b.graphG(m2.G.edges(), 'G', .35).graphG(C2, 'ham', 1.2, smooth=True).dotsG()
    corners, b.roots = b.roots, set(m.roots) & set(delta)            # the vertices as they are drawn in T
    b.vertices()
    b.roots = corners
    names(b, md, outside=True)
    b.label(b.cen[v2], '$v_2$', 8.5, 6.5, lo=0.14, hi=0.5)
    # (c) T with G and the cycle put together
    c = panel(m, xy).base().lines(sides, 'U', 1.15)
    c.graphG(m.G.edges(), 'G', .35).graphG(glue, 'ham', 1.2, smooth=True).dotsG().vertices()
    names(c, m)
    for p in (a, c):
        p.label(p.arcmid(*m.e0), '$e_0$', 8, 6.5, lo=0.12, inside=True)
    for p in (a, b, c):
        p.vertex_labels(only=set(delta))
    return table([[(a, '(a) $T_1$, $G_1$ and $C_1$'), (b, '(b) $T_2$, $G_2$ and $C_2$'),
                   (c, '(c) $T$, $G$ and the cycle obtained')]], '3mm')


# -- building -----------------------------------------------------------------------------------
FIGURES = {'construction': fig_construction, 'disk': fig_disk, 'cancel': fig_cancel,
           'count': fig_count, 'pair': fig_pair, 'induction': fig_induction}


def svg(pdf):
    """The page of a PDF as an SVG that is WIDTH px wide, with a white background."""
    import fitz
    with fitz.open(pdf) as doc:
        body = doc[0].get_svg_image(matrix=fitz.Matrix(SCALE, SCALE), text_as_path=True)
    head = re.match(r'<svg[^>]*>', body)
    w, h = (float(re.search(rf'{k}="([\d.]+)', head[0])[1]) for k in ('width', 'height'))
    assert w <= WIDTH - 2 * MARGIN + 1, f'the figure is {w:.0f} px wide'
    H = round(h + 2 * MARGIN)
    inner = body[head.end():body.rindex('</svg>')]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" '
            f'width="{WIDTH}" height="{H}" viewBox="0 0 {WIDTH} {H}">\n'
            f'<rect width="{WIDTH}" height="{H}" fill="#ffffff"/>\n'
            f'<g transform="translate({(WIDTH - w) / 2:.2f},{MARGIN})">{inner}</g>\n</svg>\n')


def main(names):
    assert r'\begin{document}' in pf.PREAMBLE
    preamble = pf.PREAMBLE.replace(r'\begin{document}', EXTRA + r'\begin{document}')
    with tempfile.TemporaryDirectory() as tmp:
        for name in names or FIGURES:
            Path(tmp, f'{name}.tex').write_text(preamble + FIGURES[name]() + '%\n\\end{document}\n', encoding='utf-8')
            z = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', f'{name}.tex'],
                               cwd=tmp, capture_output=True, text=True, errors='replace')
            if z.returncode:
                raise SystemExit(z.stdout[-3000:])
            out = HERE / f'route-{name}.svg'
            out.write_text(svg(Path(tmp, f'{name}.pdf')), encoding='utf-8', newline='\n')
            print(out.name)


if __name__ == '__main__':
    main(sys.argv[1:])
