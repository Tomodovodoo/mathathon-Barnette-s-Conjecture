"""Rooted Eulerian triangulations: states, tree matchings, pairs.

Notation follows research/BRIEF.md.  R = corners of the outer black face t0,
A = other black faces, X = nonroot vertices.  A state is a bijection s: A -> X
with s(t) a corner of t, stored as a dict.  Q_s = edges opposite s(t).
A tree matching is a state with Q_s a forest having one root per component,
equivalently H - s a spanning tree of the spoke graph H.
"""
from tri import Tri, canon_face


class UF:
    def __init__(self, items):
        self.p = {x: x for x in items}

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        self.p[a] = b
        return True


class Rooted:
    def __init__(self, T: Tri, t0):
        self.T = T
        t0 = [canon_face(g) for g in T.faces() if set(g) == set(t0)][0]
        self.t0 = t0
        col = T.face_colouring(t0)
        self.col = col
        self.black = [f for f in col if col[f] == 0]
        self.white = [f for f in col if col[f] == 1]
        self.A = [f for f in self.black if f != t0]
        self.R = list(t0)
        self.X = [v for v in T.V if v not in t0]
        self.n = len(self.A)
        assert self.n == len(self.X)
        # black face of each undirected edge
        self.bf = {}
        for f in self.black:
            for i in range(3):
                self.bf[frozenset((f[i], f[(i + 1) % 3]))] = f
        self.wf = {}
        for f in self.white:
            for i in range(3):
                self.wf[frozenset((f[i], f[(i + 1) % 3]))] = f
        Xs = set(self.X)
        self.corners = {t: [v for v in t if v in Xs] for t in self.A}
        self.faces_at = {x: [t for t in self.A if x in t] for x in self.X}

    @staticmethod
    def opp(t, v):
        return tuple(sorted(w for w in t if w != v))

    # ---------- enumeration ----------
    def states(self):
        A = sorted(self.A, key=lambda t: len(self.corners[t]))
        used = set()
        cur = {}
        out = []

        def rec(i):
            if i == len(A):
                out.append(dict(cur))
                return
            t = A[i]
            for v in self.corners[t]:
                if v not in used:
                    used.add(v)
                    cur[t] = v
                    rec(i + 1)
                    used.discard(v)
                    del cur[t]
        rec(0)
        return out

    def Q(self, s):
        return [self.opp(t, s[t]) for t in self.A]

    def is_tree_matching(self, s):
        uf = UF(self.T.V)
        r = self.R
        uf.union(r[0], r[1])
        uf.union(r[1], r[2])
        for e in self.Q(s):
            if not uf.union(*e):
                return False
        return True

    def mates(self, s):
        """all states r with r(t) != s(t) for all t (disjoint mates)"""
        out = []
        A = self.A
        used = set()
        cur = {}

        def rec(i):
            if i == len(A):
                out.append(dict(cur))
                return
            t = A[i]
            for v in self.corners[t]:
                if v != s[t] and v not in used:
                    used.add(v)
                    cur[t] = v
                    rec(i + 1)
                    used.discard(v)
                    del cur[t]
        rec(0)
        return out

    def has_pair(self):
        """does B have two edge-disjoint perfect matchings (2-factor test by flow)"""
        import networkx as nx
        G = nx.DiGraph()
        for x in self.X:
            G.add_edge("S", ("x", x), capacity=2)
        for t in self.A:
            G.add_edge(("t", t), "K", capacity=2)
            for v in self.corners[t]:
                G.add_edge(("x", v), ("t", t), capacity=1)
        val, _ = nx.maximum_flow(G, "S", "K")
        return val == 2 * self.n

    def black_inner_sep_triangles(self):
        """separating triangles whose three edges have their black face on the side
        not containing t0"""
        out = []
        for tri in self.T.separating_triangles():
            side = self.side_of_triangle(tri)  # vertices strictly on the t0-free side
            ok = True
            for i in range(3):
                for j in range(i + 1, 3):
                    e = frozenset((tri[i], tri[j]))
                    t = self.bf[e]
                    w = [v for v in t if v not in tri][0]
                    if w not in side:
                        ok = False
            if ok:
                out.append(tri)
        return out

    def side_of_triangle(self, tri):
        """vertices strictly on the side of the 3-cycle tri not containing t0 corners
        (t0 corners lie in closed side; t0 may share vertices with tri)"""
        trs = set(tri)
        start = [v for v in self.t0 if v not in trs]
        seen = set(start)
        stack = list(start)
        while stack:
            u = stack.pop()
            for w in self.T.rot[u]:
                if w not in trs and w not in seen:
                    seen.add(w)
                    stack.append(w)
        if not start:
            # t0 == tri: impossible for separating triangles (t0 is a face)
            raise ValueError
        return set(self.T.V) - seen - trs


def rooted_instances(T, both_colours=True):
    """one Rooted per face (all faces: colour of t0 is declared black)"""
    out = []
    for f in T.faces():
        out.append(Rooted(T, f))
    return out
