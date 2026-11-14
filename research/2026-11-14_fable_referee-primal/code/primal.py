"""Referee's own implementation of the objects of proofs/primal/PRIMAL-PROOF.md.

Everything is built from a cubic graph with a rotation system (three
neighbours per vertex in cyclic order).  No code from the author's checker
and no proof object from workings/barnette_lab is used.  The only outside
input is the plantri binary, which lists Eulerian triangulations with their
rotation systems (see gen.py).
"""
from collections import deque
from itertools import combinations


def E(u, v):
    return frozenset((u, v))


class PG:
    """Cubic graph with rotation system rot[v] = [u0, u1, u2]."""

    def __init__(self, rot):
        self.rot = {v: list(ns) for v, ns in rot.items()}
        self.V = list(self.rot)
        for v in self.V:
            assert len(self.rot[v]) == 3, "not cubic"
            for u in self.rot[v]:
                assert v in self.rot[u], "asymmetric adjacency"
        self.simple = all(len(set(self.rot[v])) == 3 and v not in self.rot[v] for v in self.V)
        self.edges = sorted({E(v, u) for v in self.V for u in self.rot[v]}, key=lambda e: sorted(map(repr, e)))
        self.eid = {e: i for i, e in enumerate(self.edges)}
        # face tracing: dart (u,v) is followed by (v,w), w the successor of u at v
        self.dface = {}
        self.faces = []
        for v in self.V:
            for u in self.rot[v]:
                if (v, u) in self.dface:
                    continue
                walk = []
                d = (v, u)
                while d not in self.dface:
                    self.dface[d] = len(self.faces)
                    walk.append(d[0])
                    a, b = d
                    i = self.rot[b].index(a)
                    d = (b, self.rot[b][(i + 1) % 3])
                self.faces.append(walk)
        self.nF = len(self.faces)
        # corner[v][i] lies between the edges v-rot[v][i] and v-rot[v][i+1]
        self.corner = {v: [self.dface[(self.rot[v][i], v)] for i in range(3)] for v in self.V}
        self.efaces = {e: tuple(self.dface[d] for d in (tuple(e), tuple(e)[::-1])) for e in self.edges}
        self.fverts = [set(w) for w in self.faces]
        self.fedges = [set() for _ in self.faces]
        for e, (f, g) in self.efaces.items():
            self.fedges[f].add(e)
            self.fedges[g].add(e)

    # ---- basic graph facts -------------------------------------------------
    def genus0(self):
        return len(self.V) - len(self.edges) + self.nF == 2

    def components(self, removed=frozenset(), verts=None):
        verts = set(self.V) if verts is None else set(verts)
        comps, seen = [], set()
        for s in verts:
            if s in seen:
                continue
            comp, dq = {s}, deque([s])
            seen.add(s)
            while dq:
                x = dq.popleft()
                for y in self.rot[x]:
                    if y in verts and y not in seen and E(x, y) not in removed:
                        seen.add(y)
                        comp.add(y)
                        dq.append(y)
            comps.append(comp)
        return comps

    def connected(self, removed=frozenset(), verts=None):
        return len(self.components(removed, verts)) == 1

    def cut(self, S):
        return {e for e in self.edges if len(e & S) == 1}

    def bipartition(self):
        col = {self.V[0]: 0}
        dq = deque([self.V[0]])
        while dq:
            x = dq.popleft()
            for y in self.rot[x]:
                if y not in col:
                    col[y] = 1 - col[x]
                    dq.append(y)
                elif col[y] == col[x]:
                    return None
        return col

    def three_edge_connected(self):
        if not self.connected():
            return False
        for e in self.edges:
            if not self.connected({e}):
                return False
        for e, f in combinations(self.edges, 2):
            if not self.connected({e, f}):
                return False
        return True

    def three_cuts(self):
        """All vertex bipartitions {S, complement} with exactly three cut edges."""
        out = set()
        for tri in combinations(self.edges, 3):
            comps = self.components(set(tri))
            if len(comps) == 2:
                S = frozenset(comps[0])
                if self.cut(S) == set(tri):
                    out.add(frozenset((S, frozenset(comps[1]))))
        return [tuple(p) for p in out]

    def sep_edge(self, v, i, j):
        """The edge at v between corner i and corner j (i != j)."""
        if (i + 1) % 3 == j:
            return E(v, self.rot[v][j])
        return E(v, self.rot[v][i])

    def perfect_matchings(self):
        col = self.bipartition()
        blacks = [v for v in self.V if col[v] == 0]
        res = []

        def rec(k, used, cur):
            if k == len(blacks):
                res.append(frozenset(cur))
                return
            b = blacks[k]
            for w in self.rot[b]:
                if w not in used:
                    used.add(w)
                    cur.append(E(b, w))
                    rec(k + 1, used, cur)
                    cur.pop()
                    used.discard(w)
        rec(0, set(), [])
        return res

    def cap(self, S, star="*"):
        """Contract the complement of S to the new vertex `star`.

        Returns (cap graph, map from cap edges to edges of self).  The
        rotation at the new vertex is the one of the two cyclic orders that
        gives genus zero; the count of orders that work is returned too.
        """
        S = set(S)
        ends = []
        rot = {}
        emap = {}
        for v in self.V:
            if v not in S:
                continue
            row = []
            for u in self.rot[v]:
                if u in S:
                    row.append(u)
                    emap[E(v, u)] = E(v, u)
                else:
                    row.append(star)
                    ends.append(v)
                    emap[E(v, star)] = E(v, u)
            rot[v] = row
        good = []
        if len(ends) == 3 and len(set(ends)) == 3:
            for order in (ends, ends[::-1]):
                r = dict(rot)
                r[star] = list(order)
                g = PG(r)
                if g.genus0():
                    good.append(g)
        return good, emap, ends


class Rooted:
    """G with root b0: colour classes, A, R, X, states, signs, flow, potentials."""

    def __init__(self, G, b0, orient=1, alpha=None):
        self.G = G
        self.b0 = b0
        col = G.bipartition()
        self.black = {v for v in G.V if col[v] == col[b0]}
        self.white = set(G.V) - self.black
        self.A = [v for v in G.V if v in self.black and v != b0]
        self.R = set(G.corner[b0])
        self.X = [f for f in range(G.nF) if f not in self.R]
        self.orient = orient
        self.bend = {e: next(v for v in e if v in self.black) for e in G.edges}
        self.wend = {e: next(v for v in e if v in self.white) for e in G.edges}
        self.alpha = alpha if alpha is not None else self.path_flow()
        self.pot = self.potentials()
        self._states = None

    # ---- signs -------------------------------------------------------------
    def delta(self, b, f, g):
        c = self.G.corner[b]
        i, j = c.index(f), c.index(g)
        assert i != j
        return self.orient if (i + 1) % 3 == j else -self.orient

    def third(self, b, f, g):
        return next(x for x in self.G.corner[b] if x != f and x != g)

    def edge_between(self, b, f, g):
        c = self.G.corner[b]
        return self.G.sep_edge(b, c.index(f), c.index(g))

    # ---- Lemma 6: flow and potentials -------------------------------------
    def path_flow(self):
        G = self.G
        par = {self.b0: None}
        dq = deque([self.b0])
        while dq:
            x = dq.popleft()
            for y in G.rot[x]:
                if y not in par:
                    par[y] = x
                    dq.append(y)
        alpha = {e: 0 for e in G.edges}
        for w in self.white:
            y = w
            while par[y] is not None:
                x = par[y]            # the path runs x -> y
                alpha[E(x, y)] += 1 if x in self.black else -1
                y = x
        return alpha

    def divergence(self, v):
        s = sum(self.alpha[E(v, u)] for u in self.G.rot[v])
        return s if v in self.black else -s

    def potentials(self):
        """a(b, corner_j) with a(b, corner_0) = 0, from (5.2)."""
        G = self.G
        pot = {}
        for b in self.A:
            c = G.corner[b]
            a = [0, 0, 0]
            for i in (0, 1):
                e = G.sep_edge(b, i, i + 1)
                a[i + 1] = a[i] - self.delta(b, c[i], c[i + 1]) * self.alpha[e]
            pot[b] = {c[i]: a[i] for i in range(3)}
        return pot

    # ---- states and pairs --------------------------------------------------
    def states(self):
        if self._states is None:
            G, A, Xs = self.G, self.A, set(self.X)
            res = []

            def rec(k, used, cur):
                if k == len(A):
                    res.append(tuple(cur))
                    return
                for f in G.corner[A[k]]:
                    if f in Xs and f not in used:
                        used.add(f)
                        cur.append(f)
                        rec(k + 1, used, cur)
                        cur.pop()
                        used.discard(f)
            if len(A) == len(self.X):
                rec(0, set(), [])
            self._states = res
        return self._states

    def is_pair(self, r, s):
        return all(x != y for x, y in zip(r, s))

    def eps(self, r, s):
        p = 1
        for b, f, g in zip(self.A, r, s):
            p *= self.delta(b, f, g)
        return p

    def q_edge(self, b, f):
        """The edge at b that is not on face f = s(b)."""
        c = self.G.corner[b]
        i = c.index(f)
        return E(b, self.G.rot[b][(i + 2) % 3])

    def Q(self, s):
        return [self.q_edge(b, f) for b, f in zip(self.A, s)]

    # ---- cut side ----------------------------------------------------------
    def cut_side(self, edges):
        """Shore of G - edges avoiding b0, or None if this is not a bond."""
        comps = self.G.components(set(edges))
        if len(comps) != 2:
            return None
        S = comps[0] if self.b0 not in comps[0] else comps[1]
        if self.G.cut(S) != set(edges):
            return None
        return S

    def circuit_data(self, circ):
        """circ: list of (tail face, black vertex, edge, head face), cyclic.

        Returns the quantities of Lemmas 2, 3, 5 and 6 for this directed
        face circuit, computed straight from the definitions.
        """
        G = self.G
        edges = [c[2] for c in circ]
        faces = [c[0] for c in circ]
        S = self.cut_side(edges)
        if S is None:
            return None
        h = len(circ)
        BS = S & self.black
        WS = S & self.white
        ES = {e for e in G.edges if e & S}
        US = {f for f in range(G.nF) if G.fverts[f] & S}
        ell = sum(1 for e in edges if self.bend[e] in S)
        deltas = [self.delta(b, f, g) for f, b, e, g in circ]
        sig = {d * ((1 if b in S else 0) - (1 if self.wend[e] in S else 0))
               for d, (f, b, e, g) in zip(deltas, circ)}
        mixed = {f for f in range(G.nF) if (G.fverts[f] & S) and (G.fverts[f] - S)}
        slope = sum(self.pot[b][g] - self.pot[b][f] for f, b, e, g in circ)
        return dict(S=S, h=h, ell=ell, nS=len(S), nBS=len(BS), nWS=len(WS), nES=len(ES),
                    nUS=len(US), US=US, deltas=deltas, dsum=sum(deltas), sigma=sig,
                    mixed=mixed, faces=set(faces), slope=slope,
                    rootfree=not (US & self.R))

    # ---- circuits of a pair and of Q_s ------------------------------------
    def pair_circuits(self, r, s):
        """The directed face circuits of D(r,s): tail r(b), head s(b)."""
        nxt = {}
        for b, f, g in zip(self.A, r, s):
            nxt[f] = (f, b, self.edge_between(b, f, g), g)
        seen, out = set(), []
        for f in self.X:
            if f in seen:
                continue
            circ, x = [], f
            while x not in seen:
                seen.add(x)
                circ.append(nxt[x])
                x = nxt[x][3]
            assert x == f
            out.append(circ)
        return out

    def state_circuits(self, r):
        """All directed face circuits made of links leaving r(b) across an edge at b."""
        G = self.G
        out_links = {}
        for b, f in zip(self.A, r):
            c = G.corner[b]
            i = c.index(f)
            out_links[f] = [(f, b, G.sep_edge(b, i, (i + 1) % 3), c[(i + 1) % 3]),
                            (f, b, G.sep_edge(b, i, (i + 2) % 3), c[(i + 2) % 3])]
        res = []

        def dfs(start, path, on):
            f = path[-1][3]
            if f == start:
                res.append(list(path))
                return
            if f in on or f not in out_links or f < start:
                return
            on.add(f)
            for l in out_links[f]:
                path.append(l)
                dfs(start, path, on)
                path.pop()
            on.discard(f)

        for start in self.X:
            for l in out_links[start]:
                dfs(start, [l], {start})
        return res


def undirected_cycles(nodes, links):
    """All simple cycles (length >= 1) of a multigraph.  links: list of (id, u, v)."""
    adj = {x: [] for x in nodes}
    for i, u, v in links:
        adj[u].append((i, v))
        adj[v].append((i, u))
    res = set()

    def dfs(start, x, used_e, on, path):
        for i, y in adj[x]:
            if i in used_e:
                continue
            if y == start:
                res.add(frozenset(path + [i]))
            elif y not in on and y > start:
                on.add(y)
                dfs(start, y, used_e | {i}, on, path + [i])
                on.discard(y)

    for s in nodes:
        dfs(s, s, frozenset(), {s}, [])
    return res


def is_forest(nodes, links):
    par = {x: x for x in nodes}

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for i, u, v in links:
        a, b = find(u), find(v)
        if a == b:
            return False
        par[a] = b
    return True


def padd(p, q):
    n = max(len(p), len(q))
    r = [0] * n
    for i, c in enumerate(p):
        r[i] += c
    for i, c in enumerate(q):
        r[i] += c
    return r


def pmul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r


def pscale(c, p):
    return [c * x for x in p]


def ptrim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p
