"""Draw the three figures of paper/barnette.tex.

    python figures.py            all three
    python figures.py pair       only fig-pair.pdf

Each figure is written as TikZ, compiled with pdflatex in a temporary directory
and copied here as a PDF at its printed size (labels are 8pt Latin Modern, and
the paper includes the PDFs unscaled). Everything drawn is computed from
octahedron.json and running.json by model.py; the functions `recover`,
`two_factors` and the three `fig_*` functions assert what the captions claim.
Labels are placed by search, clear of every drawn object.
"""
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import networkx as nx
import numpy as np

from model import HERE, R, load, und

TEXTWIDTH = 15.92    # cm: A4 with 1in margins
PT = 0.03515         # cm per TeX point
COLLAR = 0.17        # cm, width of the grey collar that shows the outer black face
RING = 0.085         # cm, distance from the outer circle to the vertex of G in t0
WEDGE = 0.23         # cm, radius of a state wedge at a 60 degree corner
CLEAR, MINCLEAR = 1.2, 0.6   # pt of white wanted, and required, around a label

PREAMBLE = r'''\documentclass[10pt,border=1pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{lmodern,amsmath,amssymb}
\usepackage{tikz}
\usetikzlibrary{arrows.meta}
% Okabe-Ito colours; every coloured object also differs in shape, weight or dash.
\definecolor{bfS}{HTML}{0072B2}% the state s and the edges of D(r,s)
\definecolor{bfR}{HTML}{D55E00}% the state r and the sides in Q_s
\definecolor{bfW}{HTML}{009E73}% cycles of a 2-factor of H
\definecolor{bfH}{HTML}{AA3377}% the Hamiltonian cycle of G
\colorlet{bfblack}{black!16}% a black face of T
\colorlet{bftint}{bfS!17}% a white face inside a cycle
\tikzset{
  bf/.style={line cap=round,line join=round,every node/.style={font=\footnotesize,inner sep=0pt}},
  tip/.style={-{Stealth[length=4.6pt,width=4pt]}},
  edge/.style={draw=black!60,line width=.4pt},
  root/.style={draw=black,fill=white,line width=.7pt},
  s/.style={fill=bfS,draw=bfS,line width=.3pt},
  r/.style={fill=white,draw=bfR,line width=.8pt},
  D/.style={draw=bfS,line width=1.1pt},
  Q/.style={draw=bfR,line width=1.1pt,dash pattern=on 3pt off 1.6pt},
  K/.style={Q,line width=1.5pt},
  bold/.style={draw=black,line width=1.5pt},
  G/.style={draw=black!42,line width=.35pt},
  Y/.style={draw=black,line width=.7pt},
  ham/.style={draw=bfH,line width=1.2pt},
  H/.style={draw=black!70,line width=.4pt},
  F/.style={draw=bfW,line width=1.2pt},
  gamma/.style={draw=black,line width=.8pt,dash pattern=on 3.2pt off 1.2pt on .8pt off 1.2pt,rounded corners=2.5pt,tip},
}
\begin{document}%
'''


def pt(p):
    return f'({p[0]:.3f},{p[1]:.3f})'


def ang(p):
    return math.degrees(math.atan2(p[1], p[0]))


def arrow(p, q, style, at=0.6):
    """The segment from p to q with an arrowhead at the given fraction of it."""
    mid = (1 - at) * np.asarray(p) + at * np.asarray(q)
    return rf'\draw[{style},tip] {pt(p)} -- {pt(mid)}; \draw[{style}] {pt(mid)} -- {pt(q)};'


def unit_vec(p):
    return np.asarray(p, float) / np.hypot(*p)


def cross2(a, b):
    return float(a[0] * b[1] - a[1] * b[0])


# -- what is drawn, computed and checked ----------------------------------------
def is_good(m, s):
    """Q_s and the two sides of t0 other than e0 form a spanning tree of T."""
    f = m.F[m.t0]
    sides = [e for e in zip(f, f[1:] + f[:1]) if und(*e) != m.e0]
    g = nx.Graph(m.Q(s) + sides)
    return len(g) == len(m.V) and nx.is_tree(g), m.Q(s) + sides


def recover(m, s):
    """Proposition 2.4 for a good state: the tree Y, the matching M and the cycle G - M."""
    good, S = is_good(m, s)
    assert m.is_state(s) and good
    Y = m.G.copy()
    Y.remove_edges_from(m.dual[und(*e)] for e in S)
    assert nx.is_tree(Y)
    parent = nx.predecessor(Y, m.t0)
    M = [und(c, p[0]) for c, p in parent.items() if p and p[0] in m.black]
    assert nx.is_perfect_matching(m.G, set(M)) and m.dual[m.e0] in M
    Mstar = [m.cross[g] for g in M]
    assert nx.is_forest(nx.Graph(Mstar))
    for t, x in zip(m.A, s):                     # the side of t in M* has s(t) as an end
        assert sum(x in e and set(e) <= set(m.F[t]) for e in Mstar) == 1
    cycle = [g for g in m.cross if g not in M]
    C = nx.Graph(cycle)
    assert len(C) == len(m.F) and nx.is_connected(C) and all(d == 2 for _, d in C.degree())
    return dict(S=S, Y=[und(*g) for g in Y.edges()], M=M, Mstar=Mstar, cycle=cycle)


def two_factors(m):
    """The 2-factors of H. For each one: the pair whose cycles of D(r,s) all run
    clockwise, these cycles with their disks, and all pairs with this 2-factor."""
    groups = {}
    for r, s in m.pairs():
        groups.setdefault(frozenset(zip(m.A, r)) | frozenset(zip(m.A, s)), []).append((r, s))
    out = []
    for arcs, pairs in groups.items():
        cw = [(r, s) for r, s in pairs if not any(m.disk(c)['ccw'] for c in m.directed_cycles(m.D(r, s)))]
        assert len(cw) == 1
        disks = sorted((m.disk(c) for c in m.directed_cycles(m.D(*cw[0]))), key=lambda k: -k['W'])
        assert len(pairs) == 2 ** len(disks) and all(k['W'] >= 1 and k['h'] % 2 for k in disks)
        out.append(dict(arcs=arcs, pairs=pairs, r=cw[0][0], s=cw[0][1], disks=disks))
    return sorted(out, key=lambda F: [-k['W'] for k in F['disks']])


# -- one panel: a triangulation in the disk layout ---------------------------------
class Panel:
    """Layers are drawn in call order. Every layer registers what it draws as
    sample disks, and labels are then placed clear of all of them."""

    def __init__(self, m, xy, unit):
        self.m, self.xy, self.unit = m, xy, unit
        self.roots = set(m.roots)
        self.collar, self.ring = COLLAR / unit, RING / unit
        ext = R + self.collar + 0.02 / unit
        self.box = [-ext, -ext, ext, ext]
        self.cen = {i: self.centre(i) for i in range(len(m.F))}
        self.out, self.obs = [], []

    def u(self, points):
        """TeX points to layout units."""
        return points * PT / self.unit

    def add(self, s):
        self.out.append(s)
        return self

    # geometry ---------------------------------------------------------------------
    def outer(self, a, b):
        return a in self.roots and b in self.roots

    def arcmid(self, a, b):
        return R * unit_vec(self.xy[a] + self.xy[b])

    def mid(self, a, b):
        return self.arcmid(a, b) if self.outer(a, b) else (self.xy[a] + self.xy[b]) / 2

    def inside(self, i, p, margin=0.0):
        """Is p in the bounded face i, at least margin away from its sides?"""
        f = self.m.F[i]
        if sum(v in self.roots for v in f) == 2 and np.hypot(*p) > R - margin:
            return False
        for a, b in zip(f, f[1:] + f[:1]):
            if not self.outer(a, b):
                e = self.xy[b] - self.xy[a]
                if cross2(e, p - self.xy[a]) / np.hypot(*e) < margin:
                    return False
        return True

    def centre(self, i):
        """Where the vertex of G in face i is drawn; for a black face this is p_t."""
        m, f = self.m, self.m.F[i]
        if i == m.t0:
            return np.array([0.0, -(R + self.ring)])
        if i in m.black:
            return sum(self.xy[v] for v in f) / 3
        if sum(v in self.roots for v in f) < 2:            # incentre
            a, b, c = (self.xy[v] for v in f)
            w = np.array([np.hypot(*(b - c)), np.hypot(*(c - a)), np.hypot(*(a - b))])
            return (w[0] * a + w[1] * b + w[2] * c) / w.sum()
        # A white face with an outer arc as a side: centre of its largest inscribed disk.
        best, lo, hi = None, 0.0, R
        for _ in range(30):
            rho = (lo + hi) / 2
            found = next((np.array([x, y]) for x in np.linspace(-R, R, 81) for y in np.linspace(-R, R, 81)
                          if self.inside(i, np.array([x, y]), rho)), None)
            if found is None:
                hi = rho
            else:
                best, lo = found, rho
        return best

    def seg(self, a, b):
        if not self.outer(a, b):
            return f' -- {pt(self.xy[b])}'
        t1 = ang(self.xy[a])
        d = (ang(self.xy[b]) - t1 + 180) % 360 - 180
        return f' arc[start angle={t1:.2f},end angle={t1 + d:.2f},radius={R}]'

    def edge_path(self, a, b):
        return pt(self.xy[a]) + self.seg(a, b)

    def face_path(self, i):
        f = self.m.F[i]
        return pt(self.xy[f[0]]) + ''.join(self.seg(a, b) for a, b in zip(f, f[1:] + f[:1])) + ' -- cycle'

    def grey(self, p):
        rad = float(np.hypot(*p))
        if rad >= R:
            return rad <= R + self.collar
        return any(self.inside(i, p) for i in self.m.A)

    # obstacles --------------------------------------------------------------------
    def ob_disc(self, p, r_pt):
        self.obs.append((float(p[0]), float(p[1]), self.u(r_pt)))

    def ob_seg(self, p, q, w_pt):
        p, q = np.asarray(p, float), np.asarray(q, float)
        for t in np.linspace(0, 1, int(np.hypot(*(q - p)) / 0.04) + 2):
            self.ob_disc(p + t * (q - p), w_pt / 2)

    def ob_edge(self, a, b, w_pt):
        if not self.outer(a, b):
            return self.ob_seg(self.xy[a], self.xy[b], w_pt)
        t1, t2 = (math.radians(ang(self.xy[v])) for v in (a, b))
        d = (t2 - t1 + math.pi) % (2 * math.pi) - math.pi
        for t in np.linspace(0, 1, int(abs(d) * R / 0.04) + 2):
            self.ob_disc(R * np.array([math.cos(t1 + t * d), math.sin(t1 + t * d)]), w_pt / 2)

    def ob_curve(self, pieces, w_pt):
        for a, b, c, d in pieces:
            for t in np.linspace(0, 1, 30):
                self.ob_disc((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * d, w_pt / 2)

    # layers -----------------------------------------------------------------------
    def base(self, tint=()):
        """T: black faces and the collar shaded, the given white faces tinted."""
        m = self.m
        self.add(rf'\fill[bfblack,even odd rule] (0,0) circle[radius={R + self.collar:.3f}] (0,0) circle[radius={R}];')
        for i in m.A:
            self.add(rf'\fill[bfblack] {self.face_path(i)};')
        for i in tint:
            assert i in m.white
            self.add(rf'\fill[bftint] {self.face_path(i)};')
        self.add(rf'\draw[edge] (0,0) circle[radius={R}];')
        for a, b in m.E:
            self.ob_edge(a, b, .4)
            if not self.outer(a, b):
                self.add(rf'\draw[edge] {self.edge_path(a, b)};')
        return self

    def vertices(self):
        for v in self.m.V:
            if v in self.roots:
                self.add(rf'\draw[root] {pt(self.xy[v])} circle[radius=2pt];')
                self.ob_disc(self.xy[v], 2.35)
            else:
                self.add(rf'\fill {pt(self.xy[v])} circle[radius=1.3pt];')
                self.ob_disc(self.xy[v], 1.3)
        return self

    def state(self, s, style):
        """A wedge in the corner s(t) of every face t in A."""
        for t, v in zip(self.m.A, s):
            f = self.m.F[t]
            k = f.index(v)
            o, p, q = self.xy[v], self.xy[f[(k + 1) % 3]], self.xy[f[(k + 2) % 3]]
            a1 = ang(p - o)
            sweep = (ang(q - o) - a1) % 360
            alt = abs(cross2(p - o, q - o)) / np.hypot(*(q - p))
            rho = min(0.42 * min(np.hypot(*(p - o)), np.hypot(*(q - o))), 0.7 * alt,
                      WEDGE / self.unit * min(1.25, math.sqrt(60 / sweep)))
            for rr in np.arange(rho, 0.02, -0.05):
                for th in np.linspace(a1, a1 + sweep, int(math.radians(sweep) * rr / 0.04) + 2):
                    self.ob_disc(o + rr * np.array([math.cos(math.radians(th)), math.sin(math.radians(th))]), 1.0)
            self.add(rf'\begin{{scope}}\clip {self.face_path(t)};\path[{style}] {pt(o)} -- ++({a1:.2f}:{rho:.3f}) '
                     rf'arc[start angle={a1:.2f},end angle={a1 + sweep:.2f},radius={rho:.3f}] -- cycle;\end{{scope}}')
        return self

    def arrows(self, arcs, style='D', w=1.1):
        """Directed edges of T, with the arrowhead past the middle."""
        for a, b in arcs:
            assert und(a, b) in self.m.dual and not self.outer(a, b)
            self.add(arrow(self.xy[a], self.xy[b], style))
            self.ob_seg(self.xy[a], self.xy[b], w)
            self.ob_disc(0.42 * self.xy[a] + 0.58 * self.xy[b], 2.4)
        return self

    def lines(self, edges, style, w):
        """Edges of T."""
        for a, b in edges:
            assert und(a, b) in self.m.dual
            self.add(rf'\draw[{style}] {self.edge_path(a, b)};')
            self.ob_edge(a, b, w)
        return self

    def dual_curve(self, g, tangent=None):
        """The edge g of G as cubic pieces through the midpoint of the edge of T it crosses.
        `tangent` may give the direction of the curve at the centres of the two faces."""
        i, j = g
        a, b = self.m.cross[und(i, j)]
        mid = self.mid(a, b)
        if i == self.m.t0:                       # leave the disk radially; an arc in the collar follows
            i, j = j, i
            pts = [self.cen[i], mid, mid * (R + self.ring) / R]
            normal = unit_vec(mid)
        else:
            pts = [self.cen[i], mid, self.cen[j]]
            e = self.xy[b] - self.xy[a]
            normal = unit_vec([-e[1], e[0]])
        if np.dot(normal, pts[2] - pts[0]) < 0:
            normal = -normal
        tan = [unit_vec(pts[1] - pts[0]), normal, unit_vec(pts[2] - pts[1])]
        for k, f in ((0, i), (2, j)):
            if tangent and f in tangent and not (self.m.t0 in g and k == 2):
                tan[k] = tangent[f] if np.dot(tangent[f], tan[k]) > 0 else -tangent[f]
        h = 0.35 * min(np.hypot(*(pts[1] - pts[0])), np.hypot(*(pts[2] - pts[1])))
        return [(pts[k], pts[k] + h * tan[k], pts[k + 1] - h * tan[k + 1], pts[k + 1]) for k in range(2)]

    def graphG(self, edges, style, w, smooth=False):
        """Edges of G. With smooth, they form cycles and paths, drawn without corners."""
        tangent = {}
        if smooth:
            for i, nb in nx.Graph(edges).adj.items():
                if len(nb) == 2 and i != self.m.t0:
                    p, q = (self.mid(*self.m.cross[und(i, j)]) for j in nb)
                    tangent[i] = unit_vec(q - p)
        for g in edges:
            assert self.m.G.has_edge(*g)
            if g[1] == self.m.t0:
                g = g[::-1]
            pieces = self.dual_curve(g, tangent)
            s = pt(pieces[0][0]) + ''.join(f' .. controls {pt(b)} and {pt(c)} .. {pt(d)}' for a, b, c, d in pieces)
            if self.m.t0 in g:
                rr, t = R + self.ring, ang(pieces[-1][3])
                d = (-90 - t + 180) % 360 - 180
                if abs(d) > 1:
                    s += f' arc[start angle={t:.2f},end angle={t + d:.2f},radius={rr:.3f}]'
                    for x in np.linspace(0, 1, int(abs(math.radians(d)) * rr / 0.04) + 2):
                        th = math.radians(t + x * d)
                        self.ob_disc(rr * np.array([math.cos(th), math.sin(th)]), w / 2)
            self.add(rf'\draw[{style}] {s};')
            self.ob_curve(pieces, w)
        return self

    def dotsG(self, radius=1.2):
        """The vertices of G: filled in black faces, hollow in white faces."""
        for i in self.m.G:
            fill = 'black' if i in self.m.black else 'white'
            self.add(rf'\draw[line width=.45pt,fill={fill}] {pt(self.cen[i])} circle[radius={radius}pt];')
            self.ob_disc(self.cen[i], radius + .25)
        return self

    def graphH(self, bold=()):
        """The arcs of H from p_t to the corners of t in X; those in `bold` in the style F."""
        m = self.m
        arcs = [(t, v) for t in m.A for v in m.F[t] if v in m.X]
        assert set(bold) <= set(arcs)
        for t, v in sorted(arcs, key=lambda a: a in bold):
            self.add(rf'\draw[{"F" if (t, v) in bold else "H"}] {pt(self.cen[t])} -- {pt(self.xy[v])};')
            self.ob_seg(self.cen[t], self.xy[v], 1.2 if (t, v) in bold else .4)
        return self.points(m.A)

    def points(self, faces):
        for t in faces:
            self.add(rf'\fill {pt(self.cen[t])} ++(-1.5pt,-1.5pt) rectangle ++(3pt,3pt);')
            self.ob_disc(self.cen[t], 2.1)
        return self

    # labels -----------------------------------------------------------------------
    def clearance(self, c, hw, hh):
        o = np.array(self.obs)
        dx = np.maximum(np.abs(o[:, 0] - c[0]) - hw, 0)
        dy = np.maximum(np.abs(o[:, 1] - c[1]) - hh, 0)
        return float(np.min(np.hypot(dx, dy) - o[:, 2]))

    def label(self, anchor, text, w, h, lo=0.0, hi=0.7, grey_ok=False, avoid=(), inside=False):
        """Write text, a box of w by h points, as near to the anchor as possible (between
        lo and hi cm away) such that it keeps clear of everything drawn so far and lies
        on white (and on none of the faces in `avoid`; with `inside`, in the disk).
        Fails if there is no such place."""
        hw, hh = self.u(w / 2), self.u(h / 2)
        anchor = np.asarray(anchor, float)
        corners = [np.array(q) for q in [(0, 0), (hw, hh), (-hw, hh), (hw, -hh), (-hw, -hh)]]
        best = None
        for dcm in np.arange(lo, hi + 1e-9, 0.02):
            for th in (range(0, 360, 5) if dcm else [0]):
                c = anchor + dcm / self.unit * np.array([math.cos(math.radians(th)), math.sin(math.radians(th))])
                cl = self.clearance(c, hw, hh)
                bad = (not grey_ok and any(self.grey(c + q) for q in corners)
                       or any(self.inside(i, c + q) for i in avoid for q in corners)
                       or inside and any(np.hypot(*(c + q)) > R - self.u(1.5) for q in corners))
                val = min(cl, self.u(CLEAR)) - 4 * max(0, self.u(MINCLEAR) - cl) - self.u(4) * bad - self.u(2) * dcm
                if best is None or val > best[0]:
                    best = (val, cl, bad, c)
        val, cl, bad, c = best
        assert cl >= self.u(MINCLEAR) and not bad, f'no room for the label {text}'
        for x in np.linspace(-hw, hw, 6):
            for y in np.linspace(-hh, hh, 5):
                self.ob_disc(c + np.array([x, y]), 0)
        self.box = [min(self.box[0], c[0] - hw), min(self.box[1], c[1] - hh), max(self.box[2], c[0] + hw), max(self.box[3], c[1] + hh)]
        return self.add(rf'\node at {pt(c)} {{{text}}};')

    def vertex_labels(self, only=None):
        for v in self.m.V:
            if only is None or v in only:
                w = 4.25 * len(str(v))
                if v in self.roots:                 # outside the collar
                    self.label(self.xy[v] * (R + self.collar) / R, f'${v}$', w, 5.4, lo=0.1)
                else:
                    self.label(self.xy[v], f'${v}$', w, 5.4, lo=0.16)
        return self

    def tex(self, box=None):
        x0, y0, x1, y1 = box or self.box
        return '\n'.join([rf'\begin{{tikzpicture}}[bf,x={self.unit}cm,y={self.unit}cm]',
                          rf'\path[use as bounding box] ({x0:.3f},{y0:.3f}) rectangle ({x1:.3f},{y1:.3f});']
                         + self.out + [r'\end{tikzpicture}'])


def row(panels, sep):
    """Panels side by side in one common bounding box, with (a), (b), ... below."""
    box = [f(p.box[k] for p in panels if isinstance(p, Panel)) for k, f in enumerate((min, min, max, max))]
    cells = [p.tex(box) if isinstance(p, Panel) else p for p in panels]
    cols = '@{}' + ('c@{\\hspace{' + sep + '}}') * (len(cells) - 1) + 'c@{}'
    letters = ' & '.join(rf'\footnotesize ({chr(97 + k)})' for k in range(len(cells)))
    return rf'\begin{{tabular}}{{{cols}}}' + '\n' + ' &\n'.join(cells) + r'\\[.6mm]' + '\n' + letters + '\n' + r'\end{tabular}'


# -- the figures ------------------------------------------------------------------
def fig_overview():
    """The construction on the octahedron."""
    m, xy = load('octahedron.json')
    states = m.states()
    assert len(states) == 2 and m.is_pair(*states)
    r, s = states
    rec = recover(m, s)
    cycles = m.directed_cycles(m.D(r, s))
    assert len(cycles) == 1 and sorted(cycles[0]) == m.X

    def P():
        return Panel(m, xy, 0.262)
    a = P().base().graphG(m.G.edges(), 'G', .35).dotsG().vertices()
    a.label(a.arcmid(*m.e0), '$e_0$', 8, 6.5, lo=0.12, inside=True)
    a.label((R + a.collar) * unit_vec([-1, -1]), '$t_0$', 7.5, 7, lo=0.1)
    b = P().base().state(s, 's').lines(m.Q(s), 'Q', 1.1).lines(rec['S'][len(m.A):], 'bold', 1.5).vertices()
    b.label(b.arcmid(*m.e0), '$e_0$', 8, 6.5, lo=0.12, inside=True)
    c = P().base().graphG(rec['Y'], 'Y', .7).graphG(rec['M'], 'bold', 1.5).dotsG().vertices()
    d = P().base().lines(rec['Mstar'], 'bold', 1.5).graphG(rec['cycle'], 'ham', 1.2, smooth=True).vertices()
    e = P().base().state(r, 'r').state(s, 's').arrows(m.D(r, s)).vertices()
    return row([a, b, c, d, e], '1.9mm')


def one_face(m, xy, r, s, t, height):
    """Figure 2(a): the face t of the pair (r, s), turned so that r(t) -> s(t) points to the right."""
    k = m.A.index(t)
    vr, vs = r[k], s[k]
    vu = m.third(t, vr, vs)
    d = unit_vec(xy[vs] - xy[vr])
    rot = np.array([[d[0], d[1]], [-d[1], d[0]]])
    scale = 3.7 / max(np.hypot(*(xy[a] - xy[b])) for a, b in ((vr, vs), (vs, vu), (vu, vr)))
    q = {v: scale * rot @ (xy[v] - xy[vr]) for v in (vr, vs, vu)}
    p = sum(q.values()) / 3
    L = [r'\fill[bfblack] ' + ' -- '.join(pt(q[v]) for v in q) + ' -- cycle;',
         r'\draw[edge] ' + ' -- '.join(pt(q[v]) for v in q) + ' -- cycle;']
    for v, style in ((vr, 'r'), (vs, 's')):
        a, b = sorted((ang(q[w] - q[v]) for w in q if w != v))
        if b - a > 180:
            a, b = b, a + 360
        L.append(rf'\path[{style}] {pt(q[v])} -- ++({a:.2f}:.42) arc[start angle={a:.2f},end angle={b:.2f},radius=.42] -- cycle;')
    L += [rf'\draw[H] {pt(p)} -- {pt(q[v])};' for v in q]
    L += [arrow(q[vr], q[vs], 'D'), arrow(q[vr], q[vu], 'Q')]
    L += [rf'\fill {pt(q[v])} circle[radius=1.3pt];' for v in q]
    L.append(rf'\fill {pt(p)} ++(-1.5pt,-1.5pt) rectangle ++(3pt,3pt);')
    for v, name in ((vr, 'r(t)'), (vs, 's(t)'), (vu, 'u(t)')):
        L.append(rf'\node at {pt(q[v] + 0.36 * unit_vec(q[v] - p))} {{${name}$}};')
    L.append(rf'\node at {pt(p + 0.33 * unit_vec(p - q[vr]))} {{$p_t$}};')          # between the arcs to s(t) and u(t)
    L.append(rf'\node at {pt((p + q[vr] + q[vu]) / 3 + 0.1 * unit_vec(p - q[vr]))} {{$t$}};')
    ys = [x[1] for x in q.values()]
    y0 = (min(ys) + max(ys) - height) / 2
    x0, x1 = min(x[0] for x in q.values()) - 0.75, max(x[0] for x in q.values()) + 0.75
    return '\n'.join([r'\begin{tikzpicture}[bf,x=1cm,y=1cm]',
                      rf'\path[use as bounding box] ({x0:.3f},{y0:.3f}) rectangle ({x1:.3f},{y0 + height:.3f});'] + L + [r'\end{tikzpicture}'])


def fig_pair():
    """One face of a pair, and the curve Gamma of a clockwise cycle of D(r,s)."""
    m, xy = load('running.json')
    F = two_factors(m)[0]
    r, s, k = F['r'], F['s'], F['disks'][0]
    C = k['cycle']
    arcs = list(zip(C, C[1:] + C[:1]))
    assert m.is_pair(r, s) and k['h'] == 7 and not k['ccw'] and set(arcs) <= set(m.D(r, s))
    faces = [m.A[m.D(r, s).index(e)] for e in arcs]                 # the faces with a side on C
    p = Panel(m, xy, 0.62)
    p.base(tint=k['white'])
    p.arrows(arcs)
    gamma = set()
    for t, (a, b) in zip(faces, arcs):                               # Gamma runs s(t) -> p_t -> r(t)
        mid = 0.45 * p.cen[t] + 0.55 * xy[a]
        p.add(rf'\draw[F] {pt(xy[b])} -- {pt(p.cen[t])};')
        p.add(rf'\draw[F,tip] {pt(p.cen[t])} -- {pt(mid)};')
        p.add(rf'\draw[F] {pt(mid)} -- {pt(xy[a])};')
        p.ob_seg(xy[b], p.cen[t], 1.2)
        p.ob_seg(p.cen[t], xy[a], 1.2)
        p.ob_disc(mid, 2.2)
        gamma |= {(t, a), (t, b)}
    # Gamma is pushed off C into the black faces, so no white face changes sides.
    assert all(m.left[b, a] == t or m.left[a, b] == t for t, (a, b) in zip(faces, arcs))

    # gamma_y: a path of faces from a white face y inside C to t0, through the midpoints
    # of the edges it crosses. In a black face t it passes between p_t and the corner v
    # common to the two edges, so it crosses exactly the arc from p_t to v.
    def crossings(path):
        return sum((t, (set(m.F[a]) & set(m.F[t]) & set(m.F[b])).pop()) in gamma
                   for a, t, b in zip(path, path[1:], path[2:]) if t in m.black)

    def route(path):
        pts = [p.cen[path[0]]] + [p.mid(*m.cross[und(a, b)]) for a, b in zip(path, path[1:])]
        return pts + [pts[-1] * (R + 0.8 * p.collar) / R]

    def room(path):                              # the least distance from the route to a vertex or a point p_t
        marks = [xy[v] for v in m.V] + [p.cen[t] for t in faces]
        pts = route(path)
        return min(np.hypot(*(a + x * (b - a) - q)) for a, b in zip(pts[1:], pts[2:]) for x in np.linspace(0, 1, 40) for q in marks)
    paths = [q for y in k['white'] for q in nx.all_simple_paths(m.G, y, m.t0, cutoff=5) if crossings(q) == 1]
    path = max(paths, key=room)
    pts = route(path)
    p.add(r'\draw[gamma] ' + ' -- '.join(pt(q) for q in pts) + ';')
    for a, b in zip(pts, pts[1:]):
        p.ob_seg(a, b, .8)
    p.add(rf'\fill {pt(pts[0])} circle[radius=1pt];')
    p.ob_disc(pts[0], 1)
    p.points(faces).vertices()
    p.label(pts[0], '$y$', 4.5, 6.5, lo=0.12, hi=0.4)
    p.label((pts[2] + pts[3]) / 2, r'$\gamma_y$', 8.5, 7, lo=0.14)
    # C is named at an edge where Gamma is inside C and a white face outside
    a, b = next(e for e in k['inner_black_edges'] if m.white_face(*e) not in path)
    p.label(p.mid(a, b), '$C$', 6.5, 6, lo=0.14, avoid=k['white'])
    p.label(p.cen[faces[1]], r'$\Gamma$', 5.5, 6, lo=0.14, grey_ok=True)
    p.label((R + p.collar) * unit_vec([-1, -1]), '$t_0$', 7.5, 7, lo=0.1)
    def roundness(t):                            # the least sine of a corner angle
        a, b, c = (xy[v] for v in m.F[t])
        side = [np.hypot(*(b - c)), np.hypot(*(c - a)), np.hypot(*(a - b))]
        return cross2(b - a, c - a) / (side[0] * side[1] * side[2]) * min(side)
    t = max((t for t in faces if set(m.F[t]) <= set(m.X)), key=roundness)
    return row([one_face(m, xy, r, s, t, (p.box[3] - p.box[1]) * p.unit), p], '9mm')


def fig_example():
    """The 13-vertex example: a pair with a second state that is not good, and the two 2-factors of H."""
    m, xy = load('running.json')
    Fs = two_factors(m)
    assert len(m.A) == 10 and len(m.states()) == 12 and len(Fs) == 2
    assert [[k['W'] for k in F['disks']] for F in Fs] == [[6, 1], [3, 1]]
    seconds = [s for F in Fs for _, s in F['pairs']]
    bad = [s for s in set(seconds) if not is_good(m, s)[0]]
    assert len(seconds) == 8 and len(set(seconds)) == 7 and len(bad) == 1 and seconds.count(bad[0]) == 2
    r, s = next((r, s) for r, s in Fs[0]['pairs'] if s == bad[0])
    K = m.directed_cycles(m.Q_directed(r, s))
    assert len(K) == 1 and sorted(K[0]) == [1, 8, 9]
    K = list(zip(K[0], K[0][1:] + K[0][:1]))

    def P():
        return Panel(m, xy, 0.435)
    a = P().base().state(r, 'r').state(s, 's').arrows(m.D(r, s)).arrows(K, 'K', 1.5).vertices().vertex_labels()
    panels = [a]
    for F in Fs:
        p = P().base(tint={w for k in F['disks'] for w in k['white']}).graphH(F['arcs']).vertices()
        for k in F['disks']:                 # a(C), written in a white face inside C and inside no smaller cycle
            own = [w for w in k['white'] if not any(w in j['white'] for j in F['disks'] if j['W'] < k['W'])]
            w = max(own, key=lambda w: min(np.hypot(*(p.cen[w] - xy[v])) for v in m.F[w]))
            p.label(p.cen[w], f'${k["W"]}$', 4.25, 5.4, hi=0.1)
        panels.append(p)
    return row(panels, '2.5mm')


FIGURES = {'overview': (fig_overview, 1.0), 'pair': (fig_pair, 0.82), 'example': (fig_example, 0.93)}


def main(names):
    import fitz
    with tempfile.TemporaryDirectory() as tmp:
        for name in names or FIGURES:
            make, share = FIGURES[name]
            Path(tmp, f'fig-{name}.tex').write_text(PREAMBLE + make() + '%\n\\end{document}\n', encoding='utf-8')
            z = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', f'fig-{name}.tex'],
                               cwd=tmp, capture_output=True, text=True, errors='replace')
            if z.returncode:
                raise SystemExit(z.stdout[-3000:])
            width = fitz.open(Path(tmp, f'fig-{name}.pdf'))[0].rect.width / 72 * 2.54
            assert width <= share * TEXTWIDTH, f'fig-{name} is {width:.2f} cm wide'
            shutil.copy(Path(tmp, f'fig-{name}.pdf'), HERE / f'fig-{name}.pdf')
            print(f'fig-{name}.pdf  {width:.2f} cm = {width / TEXTWIDTH:.3f} of the text width')


if __name__ == '__main__':
    main(sys.argv[1:])
