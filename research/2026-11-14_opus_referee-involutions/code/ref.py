"""Independent referee implementation of the two involutions of proofs/involutions/.

Written from the text of involutions.pdf only. It does not import the author's verify.py
or the lab's li.py. Input triangulations come from plantri (rotation systems); faces,
colouring, layout, states, pairs, cycles, rays, signs and both maps are computed here.

Exact arithmetic throughout (fractions.Fraction).
"""
from fractions import Fraction as Fr
from itertools import combinations
from math import comb, factorial
import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLANTRI = ROOT / 'workings/barnette_lab/vendor/plantri.exe'


# ---------------------------------------------------------------- input
def plantri(nv):
    """All Eulerian triangulations on nv vertices (plantri -b, i.e. 3-connected = simple)."""
    out = subprocess.run([str(PLANTRI), '-b', '-a', str(nv)], capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        k, data = line.split()
        yield {v: [ord(c) - 97 for c in ns] for v, ns in enumerate(data.split(','))}


def faces_from_rotation(rot):
    """Trace faces of the rotation system. Returns sorted list of vertex triples (as tuples)."""
    seen, faces = set(), []
    for u in rot:
        for v in rot[u]:
            if (u, v) in seen:
                continue
            f, (a, b) = [], (u, v)
            while (a, b) not in seen:
                seen.add((a, b))
                f.append(a)
                nb = rot[b]
                c = nb[(nb.index(a) - 1) % len(nb)]
                a, b = b, c
            faces.append(tuple(f))
    assert all(len(f) == 3 for f in faces), faces
    return faces


def faces_from_list(faces):
    return [tuple(f) for f in faces]


# ---------------------------------------------------------------- geometry helpers
def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def orient(a, b, c):
    return cross(sub(b, a), sub(c, a))


def solve_linear(M, rhs):
    """Exact Gauss-Jordan; M list of lists of Fractions, rhs list of vectors (lists)."""
    n = len(M)
    A = [row[:] + list(r) for row, r in zip(M, rhs)]
    w = len(A[0])
    for col in range(n):
        piv = next(i for i in range(col, n) if A[i][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        p = A[col][col]
        A[col] = [x / p for x in A[col]]
        for i in range(n):
            if i != col and A[i][col] != 0:
                f = A[i][col]
                A[i] = [x - f * y for x, y in zip(A[i], A[col])]
    return [row[n:] for row in A]


# ---------------------------------------------------------------- instance
class Inst:
    def __init__(self, faces, t0, root_pos=None, direction=(0, 1), shear_search=True, min_shear=0):
        self.faces = faces
        self.t0 = t0
        V = sorted({v for f in faces for v in f})
        self.V = V
        # face adjacency via shared edges, bipartite colouring
        edge_faces = {}
        for i, f in enumerate(faces):
            for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
                edge_faces.setdefault(frozenset((a, b)), []).append(i)
        assert all(len(x) == 2 for x in edge_faces.values())
        self.edge_faces = edge_faces
        col = {t0: 0}
        stack = [t0]
        while stack:
            i = stack.pop()
            f = faces[i]
            for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
                for j in edge_faces[frozenset((a, b))]:
                    if j not in col:
                        col[j] = 1 - col[i]
                        stack.append(j)
                    elif j != i:
                        assert col[j] != col[i], 'not properly 2-colourable'
        self.black = sorted(i for i in col if col[i] == 0)
        self.white = sorted(i for i in col if col[i] == 1)
        self.R = list(faces[t0])
        self.X = sorted(set(V) - set(self.R))
        self.A = [t for t in self.black if t != t0]
        self.n = len(self.A)
        assert self.n == len(self.X)
        self.layout(root_pos, direction, shear_search, min_shear)
        # black face of each edge
        self.black_of = {e: next(i for i in fs if col[i] == 0) for e, fs in edge_faces.items()}

    # ---- layout: Tutte barycentric, exact; then pick a generic ray direction
    def layout(self, root_pos, direction, shear_search, min_shear=0):
        R = self.R
        if root_pos is None:
            root_pos = [(Fr(0), Fr(0)), (Fr(100), Fr(0)), (Fr(0), Fr(100))]
        fixed = {R[i]: tuple(map(Fr, root_pos[i])) for i in range(3)}
        nbr = {v: set() for v in self.V}
        for f in self.faces:
            for a in f:
                for b in f:
                    if a != b:
                        nbr[a].add(b)
        xs = self.X
        idx = {v: i for i, v in enumerate(xs)}
        M = [[Fr(0)] * len(xs) for _ in xs]
        rhs = [[Fr(0), Fr(0)] for _ in xs]
        for v in xs:
            i = idx[v]
            M[i][i] = Fr(len(nbr[v]))
            for w in nbr[v]:
                if w in idx:
                    M[i][idx[w]] -= 1
                else:
                    rhs[i][0] += fixed[w][0]
                    rhs[i][1] += fixed[w][1]
        sol = solve_linear(M, rhs) if xs else []
        pos = dict(fixed)
        for v in xs:
            pos[v] = tuple(sol[idx[v]])
        cen = {i: (sum(pos[v][0] for v in f) / 3, sum(pos[v][1] for v in f) / 3) for i, f in enumerate(self.faces)}
        self.pos0, self.cen0 = pos, cen
        # planarity sanity: every inner face has the same orientation sign opposite... just nondegenerate
        for i, f in enumerate(self.faces):
            assert orient(*(pos[v] for v in f)) != 0
        d = tuple(map(Fr, direction))
        shear = min_shear
        while True:
            # shear transform x -> x + shear*y applied to points == using direction unchanged
            P = {v: (p[0] + shear * p[1], p[1]) for v, p in pos.items()}
            C = {i: (p[0] + shear * p[1], p[1]) for i, p in cen.items()}
            if self.generic(P, C, d):
                break
            if not shear_search:
                raise ValueError('nongeneric direction')
            shear += 1
        self.shear = shear
        self.pos, self.cen, self.d = P, C, d

    def generic(self, P, C, d):
        pts = list(P.values()) + [C[t] for t in self.black if t != self.t0]
        for w in self.white:
            wp = C[w]
            for p in pts:
                if cross(d, sub(p, wp)) == 0:
                    return False
        return True

    # ---- combinatorics
    def states(self):
        A, out = self.A, []
        def rec(i, used, cur):
            if i == len(A):
                out.append(tuple(cur))
                return
            for v in self.faces[A[i]]:
                if v in self.X and v not in used:
                    used.add(v); cur.append(v)
                    rec(i + 1, used, cur)
                    used.discard(v); cur.pop()
        rec(0, set(), [])
        return out

    def pairs(self, S=None):
        S = self.states() if S is None else S
        return [(r, s) for r in S for s in S if all(a != b for a, b in zip(r, s))]

    def delta(self, u, v):
        t = self.black_of[frozenset((u, v))]
        w = next(x for x in self.faces[t] if x not in (u, v))
        o = orient(self.pos[u], self.pos[v], self.pos[w])
        return 1 if o > 0 else -1  # black face to the left of u->v

    def dcycles(self, p):
        """Cycles of D_p as lists of face indices i (index into A) in traversal order r->s."""
        r, s = p
        by_tail = {r[i]: i for i in range(self.n)}
        seen, cyc = set(), []
        for i0 in range(self.n):
            if i0 in seen:
                continue
            c, i = [], i0
            while i not in seen:
                seen.add(i); c.append(i)
                i = by_tail[s[i]]
            assert i == i0
            cyc.append(c)
        return cyc

    def J(self, p):
        r, s = p
        tot = sum(self.delta(r[i], s[i]) for i in range(self.n))
        assert tot % 3 == 0
        return tot // 3

    def J_geometric(self, p):
        """#cw - #ccw of the vertex polygons of D_p, from signed area (independent of delta)."""
        r, s = p
        J = 0
        for c in self.dcycles(p):
            poly = [self.pos[r[i]] for i in c]
            area = sum(cross(poly[k], poly[(k + 1) % len(poly)]) for k in range(len(poly)))
            assert area != 0
            J += 1 if area < 0 else -1
        return J

    def spoke_crossings(self, w, i, x):
        """Crossing parameter lambda of ray from white point w with spoke centre(A[i]) -> x, or None."""
        wp, d = self.cen[w], self.d
        a, b = self.cen[self.A[i]], self.pos[x]
        e = sub(b, a)
        den = cross(d, e)
        if den == 0:
            return None
        lam = cross(sub(a, wp), e) / den
        mu = cross(sub(wp, a), d) / cross(e, d)
        if lam > 0 and 0 < mu < 1:
            return lam
        return None

    def left(self, w, pt):
        return cross(self.d, sub(pt, self.cen[w])) > 0

    def dir(self, p, w, i):
        """d(w,t)=0 if spoke t->s(t) crosses ray left to right, else 1."""
        s = p[1]
        return 0 if self.left(w, self.cen[self.A[i]]) else 1

    def tokens(self, p):
        s = p[1]
        return sorted((w, i) for w in self.white for i in range(self.n) if self.spoke_crossings(w, i, s[i]) is not None)

    def sign(self, p, M):
        return (-1) ** ((self.J(p) // 2) + sum(self.dir(p, w, i) for w, i in M))

    def ray_list(self, p, cyc, w):
        """Crossings of ray from w with spoke cycle cyc: sorted list of (lambda, i, kind) kind 0=r,1=s."""
        out = []
        for i in cyc:
            for kind in (0, 1):
                lam = self.spoke_crossings(w, i, p[kind][i])
                if lam is not None:
                    out.append((lam, i, kind))
        out.sort()
        return out

    def inside_poly(self, poly, q):
        """Winding-number point-in-polygon with horizontal test ray (independent of self.d)."""
        wn = 0
        for k in range(len(poly)):
            a, b = poly[k], poly[(k + 1) % len(poly)]
            if a[1] <= q[1] < b[1] and orient(a, b, q) > 0:
                wn += 1
            elif b[1] <= q[1] < a[1] and orient(a, b, q) < 0:
                wn -= 1
        return wn != 0

    def reverse(self, p, cyc):
        r, s = list(p[0]), list(p[1])
        for i in cyc:
            r[i], s[i] = s[i], r[i]
        return (tuple(r), tuple(s))

    # ---- Q_s
    def q_cycles(self, s):
        """Cycles of Q_s (undirected), each as sorted tuple of A-indices supplying its sides."""
        edges = []
        for i in range(self.n):
            f = self.faces[self.A[i]]
            a, b = [v for v in f if v != s[i]]
            edges.append((a, b, i))
        adj = {v: [] for v in self.V}
        for a, b, i in edges:
            adj[a].append((b, i)); adj[b].append((a, i))
        deg = {v: len(adj[v]) for v in self.V}
        alive_e = set(range(self.n))
        stack = [v for v in self.V if deg[v] <= 1]
        removed = set()
        while stack:
            v = stack.pop()
            if v in removed:
                continue
            removed.add(v)
            for u, i in adj[v]:
                if i in alive_e:
                    alive_e.discard(i)
                    deg[u] -= 1
                    if deg[u] <= 1:
                        stack.append(u)
        # remaining edges form disjoint cycles (each component unicyclic after peeling, degree 2)
        comps, seen = [], set()
        for i in sorted(alive_e):
            if i in seen:
                continue
            comp, st = set(), [i]
            while st:
                j = st.pop()
                if j in comp:
                    continue
                comp.add(j)
                a, b, _ = edges[j]
                for v in (a, b):
                    for u, k in adj[v]:
                        if k in alive_e and k not in comp:
                            st.append(k)
            seen |= comp
            comps.append(tuple(sorted(comp)))
        return comps

    def q_forest(self, s):
        return not self.q_cycles(s)


# ---------------------------------------------------------------- the two maps (as written in the note)
class Maps:
    def __init__(self, I, pairs, order_key=None, m=None):
        self.I = I
        self.pairs = pairs
        self.m = min(len(I.dcycles(p)) for p in pairs) if m is None else m
        # fixed total order on unoriented cycles: default = lexicographic on sorted supplying faces
        self.key = order_key or (lambda c: tuple(sorted(c)))
        self._tok = {}

    def toks(self, p):
        if p[1] not in self._tok:
            self._tok[p[1]] = self.I.tokens(p)
        return self._tok[p[1]]

    def objects(self, k=None):
        k = self.m if k is None else k
        for p in self.pairs:
            for M in combinations(self.toks(p), k):
                yield (p, frozenset(M))

    def iota1(self, o):
        I = self.I
        p, M = o
        cs = I.q_cycles(p[1])
        if not cs:
            return o
        K = min(cs, key=self.key)
        r, s = list(p[0]), p[1]
        tails = []
        for i in K:
            f = I.faces[I.A[i]]
            u = next(v for v in f if v not in (r[i], s[i]))
            tails.append(r[i])
            r[i] = u
        assert len(set(tails)) == len(K)  # directed cycle: distinct tails
        return ((tuple(r), s), M)

    def iota2(self, o):
        I = self.I
        p, M = o
        cyc = I.dcycles(p)
        cyc_sorted = sorted(cyc, key=self.key)
        of = {}
        for c in cyc:
            for i in c:
                of[i] = tuple(c)
        marked = {}
        for (w, i) in M:
            marked.setdefault(of[i], []).append((w, i))
        unmarked = [c for c in cyc_sorted if tuple(c) not in marked]
        if unmarked:
            return (I.reverse(p, unmarked[0]), M), 'case1'
        assert len(cyc) == self.m == len(M) and all(len(v) == 1 for v in marked.values())
        info = []
        for c in cyc_sorted:
            (w, i), = marked[tuple(c)]
            rl = I.ray_list(p, c, w)
            k = next(j for j, (_, ii, kind) in enumerate(rl) if ii == i and kind == 1)
            info.append((c, w, i, rl, k))
        chosen = next((x for x in info if len(x[3]) % 2 == 0), None)
        if chosen is None:
            chosen = next((x for x in info if x[4] != 0), None)
        if chosen is None:
            return o, 'fixed'
        c, w, i, rl, k = chosen
        if len(rl) % 2 == 0:
            partner = k ^ 1
        else:
            partner = ((k - 1) ^ 1) + 1
        _, i2, kind = rl[partner]
        newM = (M - {(w, i)}) | {(w, i2)}
        newp = p if kind == 1 else I.reverse(p, c)
        return (newp, frozenset(newM)), 'case2-keep' if kind == 1 else 'case2-reverse'
