"""Independent implementation of the objects of the OpenAI Barnette paper.

Written by the referee (Claude Fable 5.2) from the paper text and the glossary.
It does not import workings/barnette_lab. It uses networkx only for the planar
embedding of a 3-connected planar graph (unique up to reflection).

Objects: rooted Eulerian triangulation, states, covers (undirected D), pairs,
good states, m, delta, J, epsilon, spoke weights a(t,v) with unit circulation,
heights per inner white face, and Hamiltonian cycles of the primal graph.
"""
import subprocess
from collections import defaultdict, deque
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).resolve().parents[3]
PLANTRI = ROOT / 'workings/barnette_lab/vendor/plantri.exe'


# ---------------------------------------------------------------- families
def bipyramid(p):
    """Dual of the p-prism. Cycle 0..p-1, poles N=p, S=p+1."""
    g = nx.Graph()
    for i in range(p):
        g.add_edge(i, (i + 1) % p)
        g.add_edge(p, i)
        g.add_edge(p + 1, i)
    return g


def tube(p, L):
    """Rings v(j,i)=j*p+i, 0<=j<=L. Poles A=(L+1)p on ring 0, B=(L+1)p+1 on ring L.
    Quadrilateral i: diagonal v(j,i)v(j+1,i+1) for i even, v(j,i+1)v(j+1,i) for i odd."""
    g = nx.Graph()
    v = lambda j, i: j * p + (i % p)
    for j in range(L + 1):
        for i in range(p):
            g.add_edge(v(j, i), v(j, i + 1))
    for j in range(L):
        for i in range(p):
            g.add_edge(v(j, i), v(j + 1, i))
            if i % 2 == 0:
                g.add_edge(v(j, i), v(j + 1, i + 1))
            else:
                g.add_edge(v(j, i + 1), v(j + 1, i))
    A, B = (L + 1) * p, (L + 1) * p + 1
    for i in range(p):
        g.add_edge(A, v(0, i))
        g.add_edge(B, v(L, i))
    return g


def glue(g, tri_g, h, tri_h):
    """Identify triangle tri_g of g with triangle tri_h of h (in the given order).
    Returns the union and the map of h's vertices."""
    out = g.copy()
    m = {b: a for a, b in zip(tri_g, tri_h)}
    nxt = max(g.nodes()) + 1
    for x in h.nodes():
        if x not in m:
            m[x] = nxt
            nxt += 1
    for a, b in h.edges():
        out.add_edge(m[a], m[b])
    return out, m


def prism_chain(q, pole_to=2):
    """q hexagonal bipyramids. Piece j+1 is glued by its face (N,v0,v1) into the
    face (v4,v5,S) of piece j. pole_to in {0,1,2} says which of (v4,v5,S) receives
    the new pole N; the other two receive v0,v1 (their order is immaterial, the
    bipyramid has a reflection fixing N and swapping v0,v1).
    Returns graph and root triangle (N,v0,v1) of the first piece."""
    base = bipyramid(6)
    g = base.copy()
    cur = {x: x for x in base.nodes()}
    for _ in range(q - 1):
        out_face = [cur[4], cur[5], cur[7]]
        target = [None, None, None]
        target[pole_to] = 6                       # N
        rest = [i for i in range(3) if i != pole_to]
        target[rest[0]], target[rest[1]] = 0, 1
        g, cur = glue(g, out_face, base, target)
    return g, (6, 0, 1)


def plantri_eulerian(n):
    """All Eulerian triangulations with n vertices (plantri -b), as graphs."""
    out = subprocess.run([str(PLANTRI), '-b', '-a', str(n)], capture_output=True, text=True).stdout
    graphs = []
    for line in out.splitlines():
        line = line.strip()
        if not line or not line[0].isdigit():
            continue
        _, rest = line.split(' ', 1)
        g = nx.Graph()
        for i, nb in enumerate(rest.split(',')):
            for ch in nb:
                g.add_edge(i, ord(ch) - 97)
        graphs.append(g)
    return graphs


# ---------------------------------------------------------------- instance
def oriented_faces(g):
    ok, emb = nx.check_planarity(g)
    assert ok
    seen = set()
    faces = []
    for u, v in emb.edges():
        if (u, v) in seen:
            continue
        f = emb.traverse_face(u, v, mark_half_edges=seen)
        assert len(f) == 3, 'not a triangulation'
        faces.append(tuple(f))
    return faces


class Inst:
    """Rooted Eulerian triangulation. root = index into self.faces, or a vertex set."""

    def __init__(self, g, root=0, faces=None):
        self.g = g
        self.faces = faces if faces is not None else oriented_faces(g)
        if not isinstance(root, int):
            root = next(i for i, f in enumerate(self.faces) if set(f) == set(root))
        self.t0 = root
        F = self.faces
        self.dart = {}                      # directed edge -> face having it in its orientation
        for i, f in enumerate(F):
            for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
                assert (a, b) not in self.dart
                self.dart[(a, b)] = i
        col = {root: 0}
        dq = deque([root])
        while dq:
            i = dq.popleft()
            f = F[i]
            for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
                j = self.dart[(b, a)]
                if j not in col:
                    col[j] = 1 - col[i]
                    dq.append(j)
                else:
                    assert col[j] != col[i], 'faces not 2-colourable'
        self.col = col
        self.black = [i for i in range(len(F)) if col[i] == 0]
        self.white = [i for i in range(len(F)) if col[i] == 1]
        self.R = set(F[root])
        self.A = [i for i in self.black if i != root]
        self.X = sorted(set(g.nodes()) - self.R)
        self.n = len(self.A)
        assert len(self.X) == self.n
        self.bface = {}                     # undirected edge -> its black face
        for i in self.black:
            f = F[i]
            for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
                self.bface[frozenset((a, b))] = i
        self.corners = {t: [v for v in F[t] if v not in self.R] for t in self.A}
        self._weights = None

    # delta(v,w)=+1 if (v,w) is a dart of its black face in the stored orientation
    def delta(self, v, w):
        t = self.bface[frozenset((v, w))]
        return 1 if self.dart.get((v, w)) == t else -1

    # ------------------------------------------------------------ states
    def face_order(self):
        """Faces of A in BFS order of the dual from t0 (keeps the frontier small)."""
        F = self.faces
        order, seen = [], {self.t0}
        dq = deque([self.t0])
        while dq:
            i = dq.popleft()
            if self.col[i] == 0 and i != self.t0:
                order.append(i)
            f = F[i]
            for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
                j = self.dart[(b, a)]
                if j not in seen:
                    seen.add(j)
                    dq.append(j)
        return order

    def states(self, forbid=None, order=None):
        """Yield states as dict face->vertex. forbid: dict face->vertex not allowed."""
        order = order or self.face_order()
        remaining = defaultdict(int)
        for t in order:
            for v in self.corners[t]:
                remaining[v] += 1
        used = set()
        s = {}

        def rec(k):
            if k == len(order):
                yield dict(s)
                return
            t = order[k]
            cs = self.corners[t]
            for v in cs:
                remaining[v] -= 1
            dead = any(remaining[v] == 0 and v not in used for v in cs)
            # a corner that becomes exhausted must be taken now
            must = [v for v in cs if remaining[v] == 0 and v not in used]
            if len(must) <= 1:
                for v in (must if must else cs):
                    if v in used or (forbid is not None and forbid.get(t) == v):
                        continue
                    used.add(v)
                    s[t] = v
                    yield from rec(k + 1)
                    used.discard(v)
                    del s[t]
            for v in cs:
                remaining[v] += 1

        yield from rec(0)

    def opposite(self, t, v):
        return tuple(x for x in self.faces[t] if x != v)

    def is_good(self, s):
        """Q_s with the three roots identified is a tree (n edges, n+1 vertices)."""
        par = {}

        def find(x):
            while par.get(x, x) != x:
                par[x] = par.get(par[x], par[x])
                x = par[x]
            return x
        r0 = min(self.R)
        for t, v in s.items():
            a, b = self.opposite(t, v)
            a = r0 if a in self.R else a
            b = r0 if b in self.R else b
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            par[ra] = rb
        return True

    def q_cycles(self, s):
        """Cycle rank of Q_s (roots not identified) and whether it is acyclic."""
        par = {}
        rank = 0

        def find(x):
            while par.get(x, x) != x:
                x = par[x]
            return x
        for t, v in s.items():
            a, b = self.opposite(t, v)
            ra, rb = find(a), find(b)
            if ra == rb:
                rank += 1
            else:
                par[ra] = rb
        return rank

    def good_states(self, order=None):
        """Good states by DFS that prunes as soon as Q (roots identified) closes a cycle."""
        order = order or self.face_order()
        remaining = defaultdict(int)
        for t in order:
            for v in self.corners[t]:
                remaining[v] += 1
        used = set()
        s = {}
        r0 = min(self.R)
        par = {}
        hist = []

        def find(x):
            while par.get(x, x) != x:
                x = par[x]
            return x

        def rec(k):
            if k == len(order):
                yield dict(s)
                return
            t = order[k]
            cs = self.corners[t]
            for v in cs:
                remaining[v] -= 1
            must = [v for v in cs if remaining[v] == 0 and v not in used]
            if len(must) <= 1:
                for v in (must if must else cs):
                    if v in used:
                        continue
                    a, b = self.opposite(t, v)
                    a = r0 if a in self.R else a
                    b = r0 if b in self.R else b
                    ra, rb = find(a), find(b)
                    if ra == rb:
                        continue
                    par[ra] = rb
                    used.add(v)
                    s[t] = v
                    yield from rec(k + 1)
                    used.discard(v)
                    del s[t]
                    del par[ra]
            for v in cs:
                remaining[v] += 1

        yield from rec(0)

    # ------------------------------------------------------------ covers and pairs
    def covers(self, order=None):
        """Yield covers: dict face -> (a,b), the undirected edge of D in that face.
        Each vertex of X has degree exactly two."""
        order = order or self.face_order()
        remaining = defaultdict(int)
        for t in order:
            for v in self.corners[t]:
                remaining[v] += 1
        deg = defaultdict(int)
        d = {}

        def rec(k):
            if k == len(order):
                yield dict(d)
                return
            t = order[k]
            cs = self.corners[t]
            for v in cs:
                remaining[v] -= 1
            opts = []
            if len(cs) == 2:
                opts = [tuple(cs)]
            elif len(cs) == 3:
                opts = [(cs[0], cs[1]), (cs[1], cs[2]), (cs[0], cs[2])]
            for a, b in opts:
                if deg[a] >= 2 or deg[b] >= 2:
                    continue
                deg[a] += 1
                deg[b] += 1
                if all(deg[v] + remaining[v] >= 2 for v in cs):
                    d[t] = (a, b)
                    yield from rec(k + 1)
                    del d[t]
                deg[a] -= 1
                deg[b] -= 1
            for v in cs:
                remaining[v] += 1

        yield from rec(0)

    def cover_cycles(self, d):
        """Cycles of a cover as lists of (face, a, b) directed a->b along one orientation."""
        inc = defaultdict(list)
        for t, (a, b) in d.items():
            inc[a].append((t, b))
            inc[b].append((t, a))
        seen = set()
        cycles = []
        for v0 in self.X:
            if v0 in seen:
                continue
            cyc = []
            v, prev_t = v0, None
            while True:
                seen.add(v)
                (t1, w1), (t2, w2) = inc[v]
                t, w = (t1, w1) if t1 != prev_t else (t2, w2)
                cyc.append((t, v, w))
                v, prev_t = w, t
                if v == v0:
                    break
            cycles.append(cyc)
        return cycles

    def orientations(self, d):
        """Yield (r, s, eps, Jsum3) for the 2^c orientations of cover d.
        Jsum3 is the sum of delta(r(t),s(t)), equal to 3J."""
        cycles = self.cover_cycles(d)
        c = len(cycles)
        data = []
        for cyc in cycles:
            ds = sum(self.delta(a, b) for _, a, b in cyc)
            pr = 1
            for _, a, b in cyc:
                pr *= self.delta(a, b)
            ln = len(cyc)
            data.append((ds, pr, ln))
        for mask in range(1 << c):
            r, s = {}, {}
            eps, js = 1, 0
            for i, cyc in enumerate(cycles):
                ds, pr, ln = data[i]
                if mask >> i & 1:
                    for t, a, b in cyc:
                        r[t], s[t] = b, a
                    js -= ds
                    eps *= pr * (-1) ** ln
                else:
                    for t, a, b in cyc:
                        r[t], s[t] = a, b
                    js += ds
                    eps *= pr
            yield r, s, eps, js

    # ------------------------------------------------------------ weights
    def weights(self):
        """a[(t,v)] and kappa[y][(t,v)]: path cochains of Lemma 5.3 of the paper.
        Returns (a, kappa, inner_white)."""
        if self._weights:
            return self._weights
        F = self.faces
        # white faces adjacent to t0 form the unbounded face of H_0
        f0 = F[self.t0]
        outer = set(self.dart[(b, a)] for a, b in ((f0[0], f0[1]), (f0[1], f0[2]), (f0[2], f0[0])))
        # dual adjacency of H_0: white y, side i (edge x_i x_{i+1}) with black t=across;
        # spoke (t,x_{i+1}) crossed with sign +1, spoke (t,x_i) with sign -1.
        nbrs = defaultdict(list)
        for y in self.white:
            f = F[y]
            for i in range(3):
                xi, xj = f[i], f[(i + 1) % 3]
                t = self.dart[(xj, xi)]
                if t == self.t0:
                    continue
                for v, sg in ((xj, 1), (xi, -1)):
                    # other white face at spoke (t,v): across the other side of t at v
                    third = next(x for x in F[t] if x not in (xi, xj))
                    # sides of t at v are {v, other-of-(xi,xj)} (ours) and {v, third}
                    a, b = v, third
                    y2 = self.dart[(a, b)] if self.dart[(a, b)] != t else self.dart[(b, a)]
                    nbrs[y].append((y2, (t, v), sg))
        # BFS from the outer node
        parent = {}
        dq = deque()
        for y in outer:
            parent[y] = None
            dq.append(y)
        while dq:
            y = dq.popleft()
            for y2, spoke, sg in nbrs[y]:
                if y2 not in parent:
                    # step from y2 to y crosses the same spoke; find its sign as seen from y2
                    sg2 = next(s2 for (z, sp, s2) in nbrs[y2] if sp == spoke and z == y)
                    parent[y2] = (y, spoke, sg2)
                    dq.append(y2)
        inner = [y for y in self.white if y not in outer]
        a = defaultdict(int)
        kappa = {}
        for y in inner:
            k = defaultdict(int)
            z = y
            while parent[z] is not None:
                z2, spoke, sg = parent[z]
                k[spoke] += sg
                a[spoke] += sg
                z = z2
            kappa[y] = k
        self._weights = (a, kappa, inner)
        return self._weights

    def omega(self, s):
        a = self.weights()[0]
        return sum(a[(t, v)] for t, v in s.items())

    def height(self, y, s):
        k = self.weights()[1][y]
        return sum(k[(t, v)] for t, v in s.items())

    def check_circulation(self):
        """Unit circulation around the hexagon of every inner white face, in the
        direction that makes the crossing signs +1 (the stored face orientation)."""
        a, kappa, inner = self.weights()
        F = self.faces
        for y in inner:
            f = F[y]
            tot = 0
            for i in range(3):
                xi, xj = f[i], f[(i + 1) % 3]
                t = self.dart[(xj, xi)]
                tot += a[(t, xj)] - a[(t, xi)]
            assert tot == 1, (y, tot)
        return True

    # ------------------------------------------------------------ summary
    def summary(self, want_poly=True, max_cover_cycles=16):
        """S, P, M (two ways), m, polynomial as dict omega->coefficient,
        and checks of the disk identity and of (5.3)."""
        res = {}
        S = 0
        M = 0
        for s in self.states():
            S += 1
            if self.is_good(s):
                M += 1
        res['S'] = S
        res['M'] = M
        P = 0
        m = None
        good_pairs = 0
        poly = defaultdict(int)
        ncov = 0
        hist = defaultdict(int)
        for d in self.covers():
            ncov += 1
            cyc = self.cover_cycles(d)
            c = len(cyc)
            hist[c] += 1
            P += 1 << c
            m = c if m is None else min(m, c)
            # disk identity: delta-sum of each cycle is +-3
            for cy in cyc:
                ds = sum(self.delta(a, b) for _, a, b in cy)
                assert abs(ds) == 3, ds
            if want_poly and c <= max_cover_cycles:
                for r, s, eps, js in self.orientations(d):
                    assert js % 3 == 0
                    J = js // 3
                    assert (self.n + J) % 2 == 0
                    assert eps == (-1) ** ((self.n + J) // 2) or eps == -(-1) ** ((self.n + J) // 2)
                    if self.is_good(s):
                        good_pairs += 1
                    poly[self.omega(s)] += eps
        res.update(P=P, m=m, covers=ncov, cover_hist=dict(hist), good_pairs=good_pairs)
        if want_poly:
            poly = {k: v for k, v in poly.items() if v}
            res['poly'] = normalise(poly)
        return res


def normalise(poly):
    """Divide by the monomial of least exponent and make the lowest coefficient
    negative-or-positive in a fixed way: we return the tuple of coefficients from
    the lowest exponent, with the sign chosen so that the top coefficient is +."""
    if not poly:
        return ()
    lo, hi = min(poly), max(poly)
    co = [poly.get(e, 0) for e in range(lo, hi + 1)]
    if co[-1] < 0:
        co = [-x for x in co]
    return tuple(co)


# ---------------------------------------------------------------- primal Hamiltonian cycles
def primal(inst):
    """Primal cubic graph: vertices = faces of T, edge for each edge of T.
    Returns adjacency list with edge keys (frozenset of the T-edge)."""
    adj = defaultdict(list)
    for (a, b), i in inst.dart.items():
        if a < b:
            j = inst.dart[(b, a)]
            e = frozenset((a, b))
            adj[i].append((j, e))
            adj[j].append((i, e))
    return adj


def hamilton(inst, per_edge=True):
    """Number of undirected Hamiltonian cycles of the primal graph and, per edge of T,
    the number of cycles using the dual primal edge. Plain DFS with a degree prune."""
    adj = primal(inst)
    N = len(adj)
    start = 0
    visited = [False] * N
    avail = [3] * N        # neighbours that are unvisited, the path head, or the start
    use = defaultdict(int)
    total = 0
    path_edges = []
    nb = {v: [w for w, _ in adj[v]] for v in adj}
    ed = {v: [e for _, e in adj[v]] for v in adj}
    first = nb[start]
    visited[start] = True

    import sys
    sys.setrecursionlimit(10000)

    def rec(head, count, first_idx):
        nonlocal total
        if count == N:
            for k, w in enumerate(nb[head]):
                if w == start and k is not None:
                    # close; count each undirected cycle once: closing neighbour index > first_idx
                    ci = first.index(head)
                    if ci > first_idx:
                        total += 1
                        if per_edge:
                            for e in path_edges:
                                use[e] += 1
                            use[ed[head][k]] += 1
            return
        for k, w in enumerate(nb[head]):
            if visited[w]:
                continue
            # head becomes interior: its other unvisited neighbours lose one option
            ok = True
            changed = []
            for z in nb[head]:
                if z != w and not visited[z]:
                    avail[z] -= 1
                    changed.append(z)
                    if avail[z] < 2:
                        ok = False
            if ok:
                visited[w] = True
                path_edges.append(ed[head][k])
                rec(w, count + 1, first_idx)
                path_edges.pop()
                visited[w] = False
            for z in changed:
                avail[z] += 1

    for fi, w in enumerate(first):
        # the start stays available to its neighbours: do not decrement
        visited[w] = True
        path_edges.append(ed[start][fi])
        rec(w, 2, fi)
        path_edges.pop()
        visited[w] = False
    return total, dict(use)
