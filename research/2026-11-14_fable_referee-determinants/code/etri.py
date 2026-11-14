"""Independent referee implementation. Standard library only.

A triangulation is stored as a list of oriented triangles (a, b, c). The
orientation is consistent: every directed edge u->v lies on exactly one
triangle, written left[(u, v)]. We read "left" literally, so in the plane
drawing with the root face t0 at infinity every bounded face is
counterclockwise. delta(u, v) = +1 when left[(u, v)] is black. Passing
mirror=True reverses every triangle, which negates delta.

Nothing here imports networkx, sympy or barnette_lab.
"""
from fractions import Fraction
from itertools import combinations, permutations, product


# ---------------------------------------------------------------- linear algebra
def det_int(m):
    """Bareiss fraction-free determinant of an integer matrix."""
    a = [list(r) for r in m]
    n = len(a)
    if n == 0:
        return 1
    sign, prev = 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            for p in range(k + 1, n):
                if a[p][k] != 0:
                    a[k], a[p] = a[p], a[k]
                    sign = -sign
                    break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
        prev = a[k][k]
    return sign * a[n - 1][n - 1]


def det_frac(m):
    """Gaussian elimination over Fractions (a second determinant routine)."""
    a = [[Fraction(x) for x in r] for r in m]
    n = len(a)
    d = Fraction(1)
    for k in range(n):
        p = next((i for i in range(k, n) if a[i][k] != 0), None)
        if p is None:
            return Fraction(0)
        if p != k:
            a[k], a[p] = a[p], a[k]
            d = -d
        d *= a[k][k]
        for i in range(k + 1, n):
            f = a[i][k] / a[k][k]
            if f:
                for j in range(k, n):
                    a[i][j] -= f * a[k][j]
    return d


def perm_sign(p):
    """Sign of a permutation given as a list of images of 0..n-1."""
    seen, sign = [False] * len(p), 1
    for i in range(len(p)):
        if not seen[i]:
            j, length = i, 0
            while not seen[j]:
                seen[j] = True
                j = p[j]
                length += 1
            if length % 2 == 0:
                sign = -sign
    return sign


class UF:
    def __init__(self, items):
        self.p = {x: x for x in items}

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, x, y):
        x, y = self.find(x), self.find(y)
        if x == y:
            return False
        self.p[x] = y
        return True


# ---------------------------------------------------------------- triangulation
def facial_triangles(edges):
    """Faces of a simple sphere triangulation given only its edges.

    For a 3-connected plane graph the faces are the induced non-separating
    cycles, so a triangle is a face exactly when deleting it leaves the rest
    connected (K4 aside, where every triangle is a face).
    """
    adj = {}
    for u, v in edges:
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    verts = sorted(adj)
    tris = [(u, v, w) for u in verts for v in adj[u] if v > u for w in adj[u] & adj[v] if w > v]
    faces = []
    for tri in tris:
        rest = [x for x in verts if x not in tri]
        if not rest:
            faces.append(tri)
            continue
        seen, stack = {rest[0]}, [rest[0]]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in tri and y not in seen:
                    seen.add(y)
                    stack.append(y)
        if len(seen) == len(rest):
            faces.append(tri)
    assert len(faces) == 2 * len(verts) - 4, (len(faces), len(verts))
    return faces


def orient(faces):
    """Orient triangles consistently: each directed edge on exactly one face."""
    by_edge = {}
    for i, f in enumerate(faces):
        for a, b in combinations(f, 2):
            by_edge.setdefault(frozenset((a, b)), []).append(i)
    assert all(len(v) == 2 for v in by_edge.values()), "every edge must lie on two faces"
    out = [None] * len(faces)
    out[0] = tuple(faces[0])
    stack = [0]
    while stack:
        i = stack.pop()
        a, b, c = out[i]
        for u, v in ((a, b), (b, c), (c, a)):
            j = next(k for k in by_edge[frozenset((u, v))] if k != i)
            w = next(x for x in faces[j] if x not in (u, v))
            want = (v, u, w)  # the neighbour carries the reversed edge
            if out[j] is None:
                out[j] = want
                stack.append(j)
            else:
                x, y, z = out[j]
                assert (v, u) in ((x, y), (y, z), (z, x)), "non-orientable gluing"
    return out


class Tri:
    def __init__(self, edges, root, mirror=False):
        edges = sorted({tuple(sorted(e)) for e in edges})
        self.edges = edges
        self.V = sorted({v for e in edges for v in e})
        faces = orient(facial_triangles(edges))
        if mirror:
            faces = [(a, c, b) for a, b, c in faces]
        self.faces = faces
        self.left = {}
        for i, (a, b, c) in enumerate(faces):
            for u, v in ((a, b), (b, c), (c, a)):
                assert (u, v) not in self.left
                self.left[u, v] = i
        assert len(self.left) == 2 * len(edges)
        # proper two-colouring of the faces
        colour = {0: 0}
        stack = [0]
        while stack:
            i = stack.pop()
            a, b, c = faces[i]
            for u, v in ((a, b), (b, c), (c, a)):
                j = self.left[v, u]
                if j not in colour:
                    colour[j] = 1 - colour[i]
                    stack.append(j)
                else:
                    assert colour[j] != colour[i], "not Eulerian"
        self.t0 = next(i for i, f in enumerate(faces) if set(f) == set(root))
        self.black = [i for i in range(len(faces)) if colour[i] == colour[self.t0]]
        self.white = [i for i in range(len(faces)) if colour[i] != colour[self.t0]]
        self.isblack = [colour[i] == colour[self.t0] for i in range(len(faces))]
        self.R = set(faces[self.t0])
        self.X = [v for v in self.V if v not in self.R]
        self.A = [t for t in self.black if t != self.t0]
        self.n = len(self.A)
        assert len(self.X) == self.n and len(self.white) == self.n + 1
        assert len(self.V) == self.n + 3 and len(edges) == 3 * (self.n + 1)
        self.corners = {t: [v for v in faces[t] if v not in self.R] for t in self.A}
        self._states = None
        self._weights = None

    # ------------------------------------------------------------ local data
    def delta(self, u, v):
        return 1 if self.isblack[self.left[u, v]] else -1

    def black_face_of(self, u, v):
        f = self.left[u, v]
        return f if self.isblack[f] else self.left[v, u]

    def white_face_of(self, u, v):
        f = self.left[u, v]
        return f if not self.isblack[f] else self.left[v, u]

    def nxt(self, t, v):
        """Corner after v in the counterclockwise order of face t."""
        f = self.faces[t]
        return f[(f.index(v) + 1) % 3]

    def prv(self, t, v):
        f = self.faces[t]
        return f[(f.index(v) - 1) % 3]

    def spoke_sides(self, t, v):
        """White faces to the left and right of the spoke walked from centre t to corner v."""
        return self.white_face_of(v, self.nxt(t, v)), self.white_face_of(self.prv(t, v), v)

    # ------------------------------------------------------------ states and pairs
    def states(self):
        if self._states is None:
            out = []

            def rec(i, used, cur):
                if i == self.n:
                    out.append(tuple(cur))
                    return
                for v in self.corners[self.A[i]]:
                    if v not in used:
                        used.add(v)
                        cur.append(v)
                        rec(i + 1, used, cur)
                        cur.pop()
                        used.discard(v)

            rec(0, set(), [])
            self._states = out
        return self._states

    def K(self, w=None):
        """Incidence matrix, rows A, columns X; optional weights w[t, v]."""
        return [[(1 if w is None else w[t, v]) if v in self.corners[t] else 0 for v in self.X] for t in self.A]

    def state_sign(self, s):
        ix = {v: i for i, v in enumerate(self.X)}
        return perm_sign([ix[v] for v in s])

    def pairs(self):
        ss = self.states()
        return [(r, s) for r in ss for s in ss if all(a != b for a, b in zip(r, s))]

    def eps(self, r, s):
        """Real pair sign: the product of delta(r(t), s(t))."""
        e = 1
        for a, b in zip(r, s):
            e *= self.delta(a, b)
        return e

    def J(self, r, s):
        d = sum(self.delta(a, b) for a, b in zip(r, s))
        assert d % 3 == 0, "delta sum of a pair is not divisible by three"
        return d // 3

    def dcycles(self, r, s):
        """Cycles of D(r, s) as lists of (face, tail, head) in walking order."""
        out_of = {a: (t, b) for t, a, b in zip(self.A, r, s) if a != b}
        seen, cycles = set(), []
        for start in sorted(out_of):
            if start in seen:
                continue
            cyc, v = [], start
            while v not in seen:
                seen.add(v)
                t, w = out_of[v]
                cyc.append((t, v, w))
                v = w
            assert v == start
            cycles.append(cyc)
        return cycles

    def outside_faces(self, cyc_edges):
        """Faces reachable from t0 without crossing the given undirected edges."""
        blocked = {frozenset(e) for e in cyc_edges}
        seen, stack = {self.t0}, [self.t0]
        while stack:
            i = stack.pop()
            a, b, c = self.faces[i]
            for u, v in ((a, b), (b, c), (c, a)):
                if frozenset((u, v)) in blocked:
                    continue
                j = self.left[v, u]
                if j not in seen:
                    seen.add(j)
                    stack.append(j)
        return seen

    def is_ccw(self, directed_edges):
        """Geometric test: the disk not containing t0 lies on the left of every edge."""
        out = self.outside_faces(directed_edges)
        sides = {self.left[u, v] in out for u, v in directed_edges}
        assert len(sides) == 1, "cycle is not a simple closed curve"
        return not sides.pop()

    def disk_data(self, directed_edges):
        """Return h, I, B, W, l for the disk bounded by a directed simple cycle."""
        out = self.outside_faces(directed_edges)
        inside = [i for i in range(len(self.faces)) if i not in out]
        on = {u for u, v in directed_edges}
        interior = {v for i in inside for v in self.faces[i]} - on
        B = sum(self.isblack[i] for i in inside)
        W = len(inside) - B
        l = sum(self.black_face_of(u, v) not in out for u, v in directed_edges)
        return len(directed_edges), len(interior), B, W, l

    # ------------------------------------------------------------ Q_s and trees
    def Q(self, s):
        """Edge opposite s(t) in each t of A, as (face, u, v)."""
        out = []
        for t, v in zip(self.A, s):
            u, w = [x for x in self.faces[t] if x != v]
            out.append((t, u, w))
        return out

    def q_components(self, s):
        uf = UF(self.V)
        edges = {}
        for t, u, w in self.Q(s):
            uf.union(u, w)
        comp = {}
        for v in self.V:
            comp.setdefault(uf.find(v), [set(), 0])[0].add(v)
        for t, u, w in self.Q(s):
            comp[uf.find(u)][1] += 1
        return [(vs, m) for vs, m in comp.values()]

    def is_tree_state(self, s):
        """H - s is a tree: Q_s is a forest whose three components hold one root each."""
        comps = self.q_components(s)
        return all(m == len(vs) - 1 and len(vs & self.R) == 1 for vs, m in comps)

    def predicted_mates(self, s):
        comps = self.q_components(s)
        k = 0
        for vs, m in comps:
            roots = len(vs & self.R)
            if m == len(vs) - 1 and roots == 1:
                continue
            if m == len(vs) and roots == 0:
                k += 1
                continue
            return 0
        return 2 ** k

    def white_tree(self, choice):
        """Do the duals of the spokes (t, choice[t]) form a spanning tree on the white faces?"""
        uf = UF(self.white)
        for t, v in zip(self.A, choice):
            y, z = self.spoke_sides(t, v)
            if not uf.union(y, z):
                return False
        return True  # n acyclic edges on n + 1 vertices

    # ------------------------------------------------------------ spoke weights
    def weights(self):
        """Integer spoke weights a[t, v], t in A, v any corner, with circulation one
        around every white triangle that does not touch t0 (Lemma 5.3)."""
        if self._weights is not None:
            return self._weights
        merged = {y for y in self.white if any(self.left[v, u] == self.t0 for (u, v), f in self.left.items() if f == y)}
        assert len(merged) == 3
        INF = 'inf'
        node = lambda y: INF if y in merged else y
        adj = {}
        for t in self.A:
            for v in self.faces[t]:
                yl, yr = map(node, self.spoke_sides(t, v))
                if yl != yr:
                    adj.setdefault(yl, []).append((yr, t, v, +1))  # yl is on the left of t->v
                    adj.setdefault(yr, []).append((yl, t, v, -1))
        parent, order, stack = {INF: None}, [], [INF]
        while stack:
            y = stack.pop()
            order.append(y)
            for z, t, v, sgn in adj.get(y, []):
                if z not in parent:
                    parent[z] = (y, t, v, -sgn)  # sign seen from the child z
                    stack.append(z)
        assert len(parent) == len(self.white) - 2
        sub = {y: (0 if y == INF else 1) for y in parent}
        a = {(t, v): 0 for t in self.A for v in self.faces[t]}
        for y in reversed(order):
            if parent[y] is None:
                continue
            p, t, v, sgn = parent[y]
            a[t, v] += sgn * sub[y]
            sub[p] += sub[y]
        # check the circulation around every face of H0
        for y in parent:
            c = 0
            for t in self.A:
                for v in self.faces[t]:
                    yl, yr = map(node, self.spoke_sides(t, v))
                    c += a[t, v] * ((yl == y) - (yr == y))
            assert c == (1 if y != INF else -(len(parent) - 1)), (y, c)
        self._weights = a
        return a

    def circulations(self, a):
        """Circulation of arbitrary spoke weights around each white face of H0."""
        merged = {y for y in self.white if any(self.left[v, u] == self.t0 for (u, v), f in self.left.items() if f == y)}
        out = {}
        for t in self.A:
            for v in self.faces[t]:
                yl, yr = self.spoke_sides(t, v)
                yl = 'inf' if yl in merged else yl
                yr = 'inf' if yr in merged else yr
                out[yl] = out.get(yl, 0) + a.get((t, v), 0)
                out[yr] = out.get(yr, 0) - a.get((t, v), 0)
        return out

    def gap(self, cyc, a):
        """L+ - L- for a D cycle given in some orientation: head weights minus tail weights
        of the counterclockwise orientation."""
        g = sum(a[t, h] - a[t, tl] for t, tl, h in cyc)
        return g if self.is_ccw([(tl, h) for t, tl, h in cyc]) else -g

    # ------------------------------------------------------------ the polynomial F
    def F_by_pairs(self, w):
        """F(w) = sum over pairs of eps(r, s) prod_t w[t, s(t)]."""
        tot = 0
        for r, s in self.pairs():
            term = self.eps(r, s)
            for t, v in zip(self.A, s):
                term *= w[t, v]
            tot += term
        return tot

    def local_matrix(self, t, w, lam=0):
        """M_t[u, v] = delta(u, v) w[t, v] for distinct nonroot corners u, v of t;
        diagonal lam * w[t, u]."""
        ix = {v: i for i, v in enumerate(self.X)}
        m = [[0] * self.n for _ in range(self.n)]
        for u in self.corners[t]:
            for v in self.corners[t]:
                m[ix[u]][ix[v]] = lam * w[t, u] if u == v else self.delta(u, v) * w[t, v]
        return m

    def F_by_polarization(self, w, lam=0, det=det_int):
        ms = [self.local_matrix(t, w, lam) for t in self.A]
        n, tot = self.n, 0
        for mask in range(1 << n):
            m = [[0] * n for _ in range(n)]
            for k in range(n):
                if mask >> k & 1:
                    mk = ms[k]
                    for i in range(n):
                        for j in range(n):
                            if mk[i][j]:
                                m[i][j] += mk[i][j]
            tot += (-1) ** (n - bin(mask).count('1')) * det(m)
        return tot

    def raw_det(self, w, det=det_int):
        ms = [self.local_matrix(t, w) for t in self.A]
        n = self.n
        return det([[sum(m[i][j] for m in ms) for j in range(n)] for i in range(n)])

    # ------------------------------------------------------------ recovery (Section 6)
    def recover(self, s, e0):
        """Tree matching -> white tree -> P -> two induced trees -> dual Hamiltonian cycle."""
        assert self.is_tree_state(s)
        e0 = tuple(e0)
        assert set(e0) <= self.R
        y0 = self.white_face_of(*e0)
        nb = {y: [] for y in self.white}
        for t, v in zip(self.A, s):
            yl, yr = self.spoke_sides(t, v)
            # the side of t incident with v that borders yl is (v, nxt), bordering yr is (prv, v)
            nb[yl].append((yr, (self.prv(t, v), v)))
            nb[yr].append((yl, (v, self.nxt(t, v))))
        P, seen, stack = [e0], {y0}, [y0]
        while stack:
            y = stack.pop()
            for z, e in nb[y]:
                if z not in seen:
                    seen.add(z)
                    stack.append(z)
                    P.append(e)  # the edge bordering the child z
        assert len(seen) == len(self.white), "selected spokes do not give a white tree"
        P = sorted({tuple(sorted(e)) for e in P})
        assert len(P) == self.n + 1
        for f in self.faces:
            assert sum(set(e) <= set(f) for e in P) == 1, "one selected edge per face"
        uf = UF(self.V)
        for u, v in P:
            assert uf.union(u, v), "P has a cycle"
        classes = {}
        for v in self.V:
            classes.setdefault(uf.find(v), []).append(v)
        classes = sorted(classes.values())
        assert len(classes) == 2
        for cl in classes:
            inside = [e for e in self.edges if e[0] in cl and e[1] in cl]
            assert len(inside) == len(cl) - 1 and all(e in P for e in inside), "class is not an induced tree"
        cyc = self.dual_cycle(P)
        return {'P': P, 'classes': classes, 'cycle': cyc}

    def dual_cycle(self, P):
        Pset = set(P)
        nb = {i: [] for i in range(len(self.faces))}
        for (u, v), f in self.left.items():
            if tuple(sorted((u, v))) not in Pset:
                nb[f].append(self.left[v, u])
        assert all(len(x) == 2 for x in nb.values())
        cyc, prev, cur = [0], None, 0
        while True:
            a, b = nb[cur]
            step = a if a != prev else b
            if step == 0:
                break
            cyc.append(step)
            prev, cur = cur, step
        assert len(cyc) == len(self.faces) and len(set(cyc)) == len(cyc), "dual subgraph is not one cycle"
        return cyc


# ---------------------------------------------------------------- graph library
def octahedron():
    return [(a, b) for a, b in combinations(range(6), 2) if a + b != 5]


def bipyramid(m):
    """Bipyramid over an m-cycle, m even. Vertices 0..m-1 on the rim, m and m+1 apexes."""
    e = [(i, (i + 1) % m) for i in range(m)]
    e += [(i, m) for i in range(m)] + [(i, m + 1) for i in range(m)]
    return e


def tetrakis_hexahedron():
    """Dual of the truncated octahedron: cube plus a centre on every face."""
    cube = list(product((0, 1), repeat=3))
    ix = {c: i for i, c in enumerate(cube)}
    e = [(ix[a], ix[b]) for a, b in combinations(cube, 2) if sum(x != y for x, y in zip(a, b)) == 1]
    k = 8
    for axis in range(3):
        for val in (0, 1):
            e += [(k, ix[c]) for c in cube if c[axis] == val]
            k += 1
    return e


def disdyakis_dodecahedron():
    """Dual of the truncated cuboctahedron: barycentric subdivision of the cube surface."""
    cube = list(product((0, 1), repeat=3))
    cube_edges = [(a, b) for a, b in combinations(cube, 2) if sum(x != y for x, y in zip(a, b)) == 1]
    cube_faces = [(axis, val) for axis in range(3) for val in (0, 1)]
    name = {}
    for obj in [('v', c) for c in cube] + [('e', e) for e in cube_edges] + [('f', f) for f in cube_faces]:
        name[obj] = len(name)
    e = []
    for ce in cube_edges:
        e += [(name['v', ce[0]], name['e', ce]), (name['v', ce[1]], name['e', ce])]
        for axis, val in cube_faces:
            if ce[0][axis] == val and ce[1][axis] == val:
                e.append((name['e', ce], name['f', (axis, val)]))
    for axis, val in cube_faces:
        e += [(name['v', c], name['f', (axis, val)]) for c in cube if c[axis] == val]
    return e


def glue(edges_a, face_a, edges_b, face_b):
    """Connected sum along two facial triangles (identified in the given order)."""
    m = dict(zip(face_b, face_a))
    nxt = max(v for e in edges_a for v in e) + 1
    for v in sorted({v for e in edges_b for v in e}):
        if v not in m:
            m[v] = nxt
            nxt += 1
    return sorted({tuple(sorted(e)) for e in edges_a} | {tuple(sorted((m[u], m[v]))) for u, v in edges_b})


def parse_plantri(line):
    n, data = line.split()
    e = set()
    for v, ns in enumerate(data.split(',')):
        for ch in ns:
            e.add(tuple(sorted((v, ord(ch) - ord('a')))))
    assert len({v for x in e for v in x}) == int(n)
    return sorted(e)
