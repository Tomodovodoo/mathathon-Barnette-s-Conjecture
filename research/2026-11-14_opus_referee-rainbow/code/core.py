"""Core objects for the referee checks. Written from scratch for this referee.

Only external input: plantri's ASCII rotation systems (plantri -b -a V gives the
Eulerian triangulations on V vertices). Nothing is imported from other folders.

Notation follows research/BRIEF.md: T the triangulation, t0 the outer black face,
R its corners (roots), A the other black faces, X the non-roots, n = |A| = |X|.
"""
import subprocess, itertools, random
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PLANTRI = REPO / 'workings' / 'barnette_lab' / 'vendor' / 'plantri.exe'


def plantri(v):
    out = subprocess.run([str(PLANTRI), '-b', '-a', str(v)], capture_output=True, text=True).stdout
    res = []
    for line in out.splitlines():
        line = line.strip()
        if not line or not line[0].isdigit():
            continue
        nv, rest = line.split(' ', 1)
        rot = [[ord(c) - 97 for c in w] for w in rest.split(',')]
        assert len(rot) == int(nv)
        res.append(rot)
    return res


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, a):
        p = self.p
        while p[a] != a:
            p[a] = p[p[a]]
            a = p[a]
        return a

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        self.p[a] = b
        return True


class Tri:
    """A sphere triangulation from a rotation system, with its two face classes."""

    def __init__(self, rot):
        self.rot = rot
        V = self.V = len(rot)
        pos = [{u: i for i, u in enumerate(rot[v])} for v in range(V)]
        seen = {}
        faces = []
        for u in range(V):
            for v in rot[u]:
                if (u, v) in seen:
                    continue
                # face on one fixed side of u->v
                a, b = u, v
                cyc = []
                while (a, b) not in seen:
                    seen[(a, b)] = len(faces)
                    cyc.append(a)
                    w = rot[b][(pos[b][a] - 1) % len(rot[b])]
                    a, b = b, w
                assert len(cyc) == 3, cyc
                faces.append(tuple(cyc))
        self.faces = faces
        self.dface = seen  # directed edge -> face on its fixed side
        assert len(faces) == 2 * V - 4
        self.edges = sorted({(min(u, v), max(u, v)) for u in range(V) for v in rot[u]})
        assert len(self.edges) == 3 * V - 6
        # 2-colour faces: faces across an edge get opposite colours
        col = [None] * len(faces)
        col[0] = 0
        stack = [0]
        while stack:
            f = stack.pop()
            a, b, c = faces[f]
            for (x, y) in ((a, b), (b, c), (c, a)):
                g = seen[(y, x)]
                if col[g] is None:
                    col[g] = 1 - col[f]
                    stack.append(g)
                else:
                    assert col[g] != col[f], 'not Eulerian'
        self.col = col
        self.adj = [set(r) for r in rot]


class Rooted:
    """A rooted instance: face f0 of T is t0 and its colour class is black."""

    def __init__(self, tri, f0):
        self.T = tri
        self.f0 = f0
        V = tri.V
        bc = tri.col[f0]
        self.black = [f for f in range(len(tri.faces)) if tri.col[f] == bc]
        self.white = [f for f in range(len(tri.faces)) if tri.col[f] != bc]
        self.t0 = f0
        self.A = [f for f in self.black if f != f0]
        self.R = set(tri.faces[f0])
        self.X = [v for v in range(V) if v not in self.R]
        self.n = len(self.A)
        assert self.n == len(self.X) == V - 3
        # edge -> its black face and its white face
        self.bface, self.wface = {}, {}
        for f, (a, b, c) in enumerate(tri.faces):
            for x, y in ((a, b), (b, c), (c, a)):
                e = (min(x, y), max(x, y))
                (self.bface if f in set(self.black) else self.wface)[e] = f
        bset = set(self.black)
        self.isblack = [f in bset for f in range(len(tri.faces))]
        self.corners = {f: tri.faces[f] for f in range(len(tri.faces))}
        # black faces at each vertex
        self.bat = {v: [] for v in range(V)}
        for f in self.black:
            for v in tri.faces[f]:
                self.bat[v].append(f)
        self.widx = {w: i for i, w in enumerate(self.white)}
        self.cidx = {t: V + i for i, t in enumerate(self.black)}  # spoke graph node of a centre
        self.NH = V + len(self.black)

    # ---- white-face graph W = H* ----
    def wedge(self, t, v):
        """W-edge of spoke (t, v): the white faces across the two sides of t at v."""
        a, b = [c for c in self.T.faces[t] if c != v]
        w1 = self.wface[(min(v, a), max(v, a))]
        w2 = self.wface[(min(v, b), max(v, b))]
        return self.widx[w1], self.widx[w2]

    def w_is_forest(self, spokes):
        uf = UF(len(self.white))
        for (t, v) in spokes:
            a, b = self.wedge(t, v)
            if not uf.union(a, b):
                return False
        return True

    def H_minus_is_tree(self, removed):
        """H minus the spoke set `removed` is a spanning tree (union-find on H)."""
        rem = set(removed)
        uf = UF(self.NH)
        cnt = 0
        for t in self.black:
            for v in self.T.faces[t]:
                if (t, v) in rem:
                    continue
                if not uf.union(self.cidx[t], v):
                    return False
                cnt += 1
        return cnt == self.NH - 1

    def all_spokes(self):
        return [(t, v) for t in self.black for v in self.T.faces[t]]

    # ---- separating triangles ----
    def separating_triangles(self):
        """List (tri, inner vertex set, inner faces along sides, black-inner flag)."""
        T = self.T
        facesets = {frozenset(f) for f in T.faces}
        res = []
        V = T.V
        for a in range(V):
            for b in T.adj[a]:
                if b <= a:
                    continue
                for c in T.adj[a] & T.adj[b]:
                    if c <= b:
                        continue
                    if frozenset((a, b, c)) in facesets:
                        continue
                    # components of T - {a,b,c}
                    rest = set(range(V)) - {a, b, c}
                    comps = []
                    while rest:
                        s = rest.pop()
                        comp = {s}
                        st = [s]
                        while st:
                            x = st.pop()
                            for y in T.adj[x]:
                                if y in rest:
                                    rest.discard(y)
                                    comp.add(y)
                                    st.append(y)
                        comps.append(comp)
                    assert len(comps) == 2
                    t0v = set(T.faces[self.t0]) - {a, b, c}
                    inner = [cp for cp in comps if not (cp & t0v)]
                    assert len(inner) == 1
                    inner = inner[0]
                    along = []
                    for x, y in ((a, b), (b, c), (a, c)):
                        for f in (T.dface[(x, y)], T.dface[(y, x)]):
                            third = [z for z in T.faces[f] if z not in (x, y)][0]
                            if third in inner:
                                along.append(f)
                    assert len(along) == 3
                    res.append(((a, b, c), inner, along, all(self.isblack[f] for f in along)))
        return res

    def has_black_inner(self):
        return any(s[3] for s in self.separating_triangles())

    # ---- incidence graph B and 2-factors ----
    def two_factor_exists(self):
        """max flow: source->t (cap 2), t->x (cap 1, x corner of t in X), x->sink (cap 2)."""
        n = self.n
        A, X = self.A, self.X
        xi = {x: i for i, x in enumerate(X)}
        N = 2 + 2 * n
        S, Tt = 0, 1
        cap = {}
        g = [[] for _ in range(N)]

        def add(u, v, c):
            if (u, v) not in cap:
                g[u].append(v); g[v].append(u)
                cap[(u, v)] = 0; cap.setdefault((v, u), 0)
            cap[(u, v)] += c
        for i, t in enumerate(A):
            add(S, 2 + i, 2)
            for v in self.T.faces[t]:
                if v in xi:
                    add(2 + i, 2 + n + xi[v], 1)
        for j in range(n):
            add(2 + n + j, Tt, 2)
        flow = 0
        while True:
            par = {S: None}
            st = [S]
            while st and Tt not in par:
                u = st.pop()
                for v in g[u]:
                    if v not in par and cap[(u, v)] > 0:
                        par[v] = u
                        st.append(v)
            if Tt not in par:
                break
            v = Tt
            while par[v] is not None:
                u = par[v]
                cap[(u, v)] -= 1
                cap[(v, u)] += 1
                v = u
            flow += 1
        return flow == 2 * n

    def two_factors(self, limit=None):
        """All 2-factors of B, as dict t -> deleted corner u(t) (a corner of t; may be a root).
        A 2-factor is determined by u; it is valid iff every x in X is a non-deleted corner
        of exactly two faces of A (roots: the deleted corner must be the root if t has one)."""
        A = self.A
        Rs = self.R
        choices = []
        for t in A:
            cs = self.T.faces[t]
            rts = [c for c in cs if c in Rs]
            choices.append(rts if rts else list(cs))
        # backtracking with degree bound
        deg = {x: 0 for x in self.X}
        res = []
        u = {}
        order = list(range(len(A)))

        def rec(i):
            if limit is not None and len(res) >= limit:
                return
            if i == len(A):
                if all(d == 2 for d in deg.values()):
                    res.append(dict(u))
                return
            t = A[order[i]]
            for c in choices[order[i]]:
                others = [v for v in self.T.faces[t] if v != c]
                if any(v in Rs for v in others):
                    continue
                if all(deg[v] < 2 for v in others):
                    for v in others:
                        deg[v] += 1
                    u[t] = c
                    rec(i + 1)
                    for v in others:
                        deg[v] -= 1
            u.pop(t, None)
        rec(0)
        return res

    # ---- states ----
    def states(self):
        """All states s: dict t -> corner in X, bijective."""
        A = self.A
        Xs = set(self.X)
        res = []
        used = set()
        s = {}

        def rec(i):
            if i == len(A):
                res.append(dict(s))
                return
            t = A[i]
            for v in self.T.faces[t]:
                if v in Xs and v not in used:
                    used.add(v); s[t] = v
                    rec(i + 1)
                    used.discard(v)
            s.pop(t, None)
        rec(0)
        return res

    def is_good_state(self, s):
        return self.H_minus_is_tree([(t, v) for t, v in s.items()])


def all_rooted(V, every_face=True):
    """Every face of every Eulerian triangulation on V vertices as t0."""
    for idx, rot in enumerate(plantri(V)):
        tri = Tri(rot)
        for f in range(len(tri.faces)):
            yield idx, f, Rooted(tri, f)
