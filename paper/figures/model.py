"""An Eulerian triangulation with an outer black face, and its disk layout.

Notation follows paper/barnette.tex.

A triangulation is a list of faces, each a triple of vertices. All faces are
listed with the same orientation, so every directed edge (u, v) lies in exactly
one face. The layout draws every bounded face counterclockwise in this order,
so "the face of (u, v)" is the face on the left of the directed edge u -> v.
"""
import json
import math
from pathlib import Path

import networkx as nx
import numpy as np

HERE = Path(__file__).parent


def und(u, v):
    return (u, v) if u < v else (v, u)


class Model:
    def __init__(self, faces, t0, e0=None):
        self.F = [tuple(f) for f in faces]
        self.V = sorted({v for f in self.F for v in f})
        self.left = {}
        for i, f in enumerate(self.F):
            for a, b in zip(f, f[1:] + f[:1]):
                assert (a, b) not in self.left, 'faces are not consistently oriented'
                self.left[a, b] = i
        self.E = sorted({und(a, b) for a, b in self.left})
        assert all((b, a) in self.left for a, b in self.left)
        self.T = nx.Graph(self.E)
        # Primal cubic graph G: one vertex per face, one edge per edge of T.
        self.G = nx.Graph()
        self.G.add_nodes_from(range(len(self.F)))
        self.cross = {}                      # edge of G  ->  edge of T it crosses
        self.dual = {}                       # edge of T  ->  edge of G
        for a, b in self.E:
            g = und(self.left[a, b], self.left[b, a])
            self.G.add_edge(*g)
            self.cross[g] = (a, b)
            self.dual[a, b] = g
        col = nx.bipartite.color(self.G)
        self.t0 = t0
        self.black = sorted(i for i in self.G if col[i] == col[t0])
        self.white = sorted(i for i in self.G if col[i] != col[t0])
        self.roots = list(self.F[t0])
        self.A = [t for t in self.black if t != t0]
        self.X = [v for v in self.V if v not in self.roots]
        assert len(self.A) == len(self.X)
        self.e0 = und(*e0) if e0 else und(*self.roots[:2])
        assert set(self.e0) < set(self.roots)

    # -- local structure ----------------------------------------------------
    def black_face(self, u, v):
        """The unique black face containing the edge uv."""
        a, b = self.left[u, v], self.left[v, u]
        return a if a in self.black else b

    def white_face(self, u, v):
        a, b = self.left[u, v], self.left[v, u]
        return a if a in self.white else b

    def delta(self, u, v):
        """+1 if the black face of uv is on the left of u -> v (the sign delta_t).

        The outer face t0 is drawn as the unbounded region, and it also lies on
        the left of its own boundary in the stored order, so no special case.
        """
        return 1 if self.left[u, v] in self.black else -1

    def third(self, t, a, b):
        return next(v for v in self.F[t] if v not in (a, b))

    # -- states and pairs ---------------------------------------------------
    def states(self):
        out, X = [], set(self.X)

        def rec(s, used):
            if len(s) == len(self.A):
                out.append(tuple(s))
                return
            for v in self.F[self.A[len(s)]]:
                if v in X and v not in used:
                    rec(s + [v], used | {v})
        rec([], set())
        return out

    def is_state(self, s):
        return (len(s) == len(self.A) and sorted(s) == sorted(self.X)
                and all(v in self.F[t] for t, v in zip(self.A, s)))

    def is_pair(self, r, s):
        return self.is_state(r) and self.is_state(s) and all(a != b for a, b in zip(r, s))

    def pairs(self, states=None):
        states = states or self.states()
        return [(r, s) for r in states for s in states if all(a != b for a, b in zip(r, s))]

    def Q(self, s):
        """Edges opposite s(t), one per t in A, in the order of A."""
        return [tuple(v for v in self.F[t] if v != x) for t, x in zip(self.A, s)]

    def Q_graph(self, s):
        g = nx.Graph()
        g.add_nodes_from(self.V)
        g.add_edges_from(self.Q(s))
        return g

    def Q_is_forest(self, s):
        return nx.is_forest(self.Q_graph(s))

    def Q_directed(self, r, s):
        """Q_s oriented r(t) -> u(t)."""
        return [(a, self.third(t, a, b)) for t, a, b in zip(self.A, r, s)]

    def D(self, r, s):
        return list(zip(r, s))

    @staticmethod
    def directed_cycles(arcs):
        return [c for c in nx.simple_cycles(nx.DiGraph(arcs))]

    # -- disks ----------------------------------------------------------------
    def disk(self, cycle):
        """Data of the disk bounded by a directed cycle that avoids the roots.

        Returns faces inside, interior vertices, the counts B, W, I, h, l, the
        delta-sum, and whether the cycle runs counterclockwise (disk on its left).
        """
        arcs = list(zip(cycle, cycle[1:] + cycle[:1]))
        barrier = {und(a, b) for a, b in arcs}
        g = self.G.copy()
        g.remove_edges_from(e for e, te in self.cross.items() if und(*te) in barrier)
        outside = nx.node_connected_component(g, self.t0)
        inside = sorted(set(g) - outside)
        assert inside, 'cycle does not bound a disk away from t0'
        vin = {v for f in inside for v in self.F[f]} - set(cycle)
        B = [f for f in inside if f in self.black]
        W = [f for f in inside if f in self.white]
        inner_black = [(a, b) for a, b in arcs if self.black_face(a, b) in inside]
        ccw = self.left[arcs[0]] in inside
        assert all((self.left[a] in inside) == ccw for a in arcs)
        return dict(cycle=list(cycle), faces=inside, interior=sorted(vin),
                    black=B, white=W, B=len(B), W=len(W), I=len(vin), h=len(cycle),
                    l=len(inner_black), inner_black_edges=inner_black,
                    delta_sum=sum(self.delta(a, b) for a, b in arcs), ccw=ccw)


# -- layout ------------------------------------------------------------------
# The outer black face t0 is the unbounded region. Its three edges are drawn as
# arcs of one circle of radius R with the roots on it, 120 degrees apart, so the
# bounded faces fill a disk and each root has a half-plane of directions for its
# edges. (Inside a straight outer triangle a root has only 60 degrees, which is
# what made the first layout full of slivers.)
#
# Interior coordinates start from a Tutte embedding and are then relaxed to
# minimise
#
#     sum over corners of 1/sin(angle/2)^2  +  AREA_WEIGHT * sum over faces of log(area/mean)^2,
#
# with the true angles and areas of the three faces that have an arc as a side.
# The search is a plain coordinate descent that never accepts a flipped face.

R = 5.0
ROOT_ANGLES = (210.0, 330.0, 90.0)          # e0 = first two roots is the bottom arc
AREA_WEIGHT = 6.0
CAP = 3.0                                    # target area of the three faces on the outer arcs, in units of the others
SEGMENT = R * R / 2 * (2 * math.pi / 3 - math.sin(2 * math.pi / 3))   # area between a chord and its arc


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def tutte(m, fixed):
    inner = [v for v in m.V if v not in fixed]
    L = nx.laplacian_matrix(m.T, nodelist=inner + list(fixed)).toarray().astype(float)
    k = len(inner)
    sol = np.linalg.solve(L[:k, :k], -L[:k, k:] @ np.array([fixed[v] for v in fixed]))
    return {**{v: np.array(p) for v, p in fixed.items()}, **dict(zip(inner, sol))}


def face_measures(m, xy):
    """For every bounded face: (area, [three corner angles in radians]).

    A face with an outer edge has a circular arc as that side: its area gains
    the circular segment, and its two root corners gain 60 degrees each.
    Returns None if some straight triangle with no outer side is flipped.
    """
    roots = set(m.roots)
    out = {}
    for i, f in enumerate(m.F):
        if i == m.t0:
            continue
        p = [xy[v] for v in f]
        area = cross(p[1] - p[0], p[2] - p[0]) / 2
        outer = sum(v in roots for v in f) == 2
        ang = []
        for k in range(3):
            a, b, c = p[k], p[(k + 1) % 3], p[(k + 2) % 3]
            th = math.atan2(cross(b - a, c - a), float(np.dot(b - a, c - a)))   # signed
            if outer and f[k] in roots:
                th += math.pi / 3
            elif outer and th < 0:
                th += 2 * math.pi                                    # reflex corner inside the segment
            ang.append(th)
        if outer:
            area += SEGMENT
        if area <= 0 or min(ang) <= 0.02:
            return None
        out[i] = (area, ang)
    return out


def energy(m, xy):
    fm = face_measures(m, xy)
    if fm is None:
        return math.inf
    if any(np.hypot(*xy[v]) > R * 0.985 for v in m.X):
        return math.inf
    roots = set(m.roots)
    unit = math.pi * R * R / (len(fm) - 3 + 3 * CAP)
    e = 0.0
    for i, (area, ang) in fm.items():
        cap = sum(v in roots for v in m.F[i]) == 2
        e += AREA_WEIGHT * math.log(area / (unit * (CAP if cap else 1))) ** 2
        e += sum(1 / math.sin(min(a, math.pi - 1e-3) / 2) ** 2 for a in ang) / 10
    return e


def relax(m, xy, rounds=400):
    xy = {v: p.copy() for v, p in xy.items()}
    best = energy(m, xy)
    assert math.isfinite(best), 'start layout is not a valid drawing'
    step = 0.4
    dirs = [np.array([math.cos(t), math.sin(t)]) for t in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
    for _ in range(rounds):
        moved = False
        for v in m.X:
            for d in dirs:
                old = xy[v].copy()
                xy[v] = old + step * d
                e = energy(m, xy)
                if e < best - 1e-12:
                    best, moved = e, True
                else:
                    xy[v] = old
        if not moved:
            step /= 2
            if step < 1e-4:
                break
    return xy, best


def layout(m):
    """Coordinates of the vertices: roots on the circle of radius R, e0 at the bottom."""
    third = next(v for v in m.roots if v not in m.e0)
    a, b = m.e0
    if m.left[a, b] == m.t0:            # outer face on the left of a -> b means a -> b runs clockwise
        a, b = b, a
    fixed = {v: R * np.array([math.cos(math.radians(t)), math.sin(math.radians(t))])
             for v, t in zip((a, b, third), ROOT_ANGLES)}
    xy = tutte(m, fixed)
    for i, f in enumerate(m.F):
        if i != m.t0:
            assert cross(xy[f[1]] - xy[f[0]], xy[f[2]] - xy[f[0]]) > 0, 'drawing is mirrored'
    return relax(m, xy)[0]


def load(name):
    d = json.loads((HERE / name).read_text())
    m = Model(d['faces'], d['t0'], d.get('e0'))
    return m, layout(m)
