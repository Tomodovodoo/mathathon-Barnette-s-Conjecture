"""Rooted Eulerian triangulation: states, pairs, D-cycles, Q_s, J, heights.

Notation follows research/BRIEF.md.  t0 is the outer face and its colour class is
called black.  Every other face is drawn counterclockwise, so a directed cycle is
counterclockwise exactly when the faces on its left do not include t0.
"""
from collections import deque, defaultdict


class Rooted:
    def __init__(self, T, t0):
        self.T = T
        self.t0 = t0
        fc = T.fcol
        self.bc = fc[t0]
        self.A = [f for f in range(T.F) if fc[f] == self.bc and f != t0]
        self.white = [f for f in range(T.F) if fc[f] != self.bc]
        self.R = tuple(T.faces[t0])
        self.Rset = set(self.R)
        self.X = [v for v in range(T.V) if v not in self.Rset]
        self.n = len(self.A)
        assert len(self.X) == self.n
        self.black_of_edge = {}   # undirected edge -> its black face
        for (a, b), f in T.de.items():
            if fc[f] == self.bc:
                self.black_of_edge[frozenset((a, b))] = f
        self._orient_cache = {}
        self._states = None
        self._weights = None

    # ---- local geometry -------------------------------------------------
    def delta(self, v, w):
        """+1 if the black face of vw is on the left of v -> w."""
        return 1 if self.T.fcol[self.T.de[(v, w)]] == self.bc else -1

    def is_ccw(self, cyc):
        """cyc: list of vertices of a simple directed cycle v0 -> v1 -> ... -> v0."""
        key = tuple(cyc)
        m = key.index(min(key))
        key = key[m:] + key[:m]
        if key in self._orient_cache:
            return self._orient_cache[key]
        T = self.T
        h = len(cyc)
        blocked = set()
        for i in range(h):
            blocked.add(frozenset((cyc[i], cyc[(i + 1) % h])))
        start = T.de[(cyc[0], cyc[1 % h])]
        seen = {start}
        dq = deque([start])
        while dq:
            f = dq.popleft()
            a, b, c = T.faces[f]
            for e in ((a, b), (b, c), (c, a)):
                if frozenset(e) in blocked:
                    continue
                g = T.de[(e[1], e[0])]
                if g not in seen:
                    seen.add(g)
                    dq.append(g)
        res = (self.t0 not in seen, frozenset(seen))
        self._orient_cache[key] = res
        return res

    # ---- states ----------------------------------------------------------
    def states(self):
        """All bijections A -> X with s(t) a corner of t, as tuples indexed like A."""
        if self._states is not None:
            return self._states
        T = self.T
        opts = [[v for v in T.faces[f] if v not in self.Rset] for f in self.A]
        n = self.n
        out = []
        cur = [None] * n
        used = set()

        def rec(left):
            if not left:
                out.append(tuple(cur))
                return
            best, bo = None, None
            for i in left:
                o = [v for v in opts[i] if v not in used]
                if best is None or len(o) < len(bo):
                    best, bo = i, o
                    if not o:
                        return
            rest = [i for i in left if i != best]
            for v in bo:
                cur[best] = v
                used.add(v)
                rec(rest)
                used.discard(v)
            cur[best] = None

        rec(list(range(n)))
        self._states = sorted(out)
        return self._states

    def perm_sign(self, s):
        """Sign of the bijection s as a permutation matrix on A x X (fixed orders)."""
        xi = {v: i for i, v in enumerate(self.X)}
        p = [xi[v] for v in s]
        seen = [False] * len(p)
        sign = 1
        for i in range(len(p)):
            if not seen[i]:
                j, ln = i, 0
                while not seen[j]:
                    seen[j] = True
                    j = p[j]
                    ln += 1
                if ln % 2 == 0:
                    sign = -sign
        return sign

    # ---- Q_s and partners --------------------------------------------------
    def Q_edges(self, s):
        """For each t in A (same index), the edge opposite s(t) as a pair."""
        out = []
        for f, v in zip(self.A, s):
            a, b, c = self.T.faces[f]
            out.append(tuple(x for x in (a, b, c) if x != v))
        return out

    def Q_structure(self, s):
        """Returns (valid, forced, cycles).
        valid : s has at least one disjoint partner.
        forced: dict face-index -> r(t) on the tree parts (same for every partner).
        cycles: list of cycles of Q_s; each a list of (face-index, x, y) with the
                edges in cyclic order x -> y."""
        Q = self.Q_edges(s)
        inc = defaultdict(set)
        for i, (x, y) in enumerate(Q):
            inc[x].add(i)
            inc[y].add(i)
        forced = {}
        alive = set(range(self.n))
        stack = [v for v in self.X if len(inc[v]) == 1]
        for v in self.X:
            if len(inc[v]) == 0:
                return False, None, None
        tail_done = set()
        while stack:
            v = stack.pop()
            if v in tail_done or len(inc[v]) != 1:
                continue
            (i,) = inc[v]
            forced[i] = v
            tail_done.add(v)
            alive.discard(i)
            x, y = Q[i]
            w = y if x == v else x
            inc[v].discard(i)
            inc[w].discard(i)
            if w not in self.Rset and w not in tail_done:
                if len(inc[w]) == 1:
                    stack.append(w)
                elif len(inc[w]) == 0:
                    return False, None, None
        for r in self.R:
            if inc[r]:
                return False, None, None
        for v in self.X:
            if v not in tail_done and len(inc[v]) != 2:
                return False, None, None
        cycles = []
        left = set(alive)
        while left:
            i0 = next(iter(left))
            x0, y0 = Q[i0]
            cyc = [(i0, x0, y0)]
            left.discard(i0)
            v = y0
            i = i0
            while v != x0:
                (j,) = inc[v] - {i}
                a, b = Q[j]
                w = b if a == v else a
                cyc.append((j, v, w))
                left.discard(j)
                i, v = j, w
            cycles.append(cyc)
        return True, forced, cycles

    def partners(self, s):
        """List of states r disjoint from s (as tuples), possibly empty."""
        valid, forced, cycles = self.Q_structure(s)
        if not valid:
            return []
        base = [None] * self.n
        for i, v in forced.items():
            base[i] = v
        out = []
        k = len(cycles)
        for mask in range(1 << k):
            r = list(base)
            for c, cyc in enumerate(cycles):
                for (i, x, y) in cyc:
                    r[i] = x if not (mask >> c) & 1 else y
            out.append(tuple(r))
        return out

    # ---- D(r, s) -----------------------------------------------------------
    def D_cycles(self, r, s):
        """Cycles of r(t) -> s(t).  Each cycle: list of (face-index, tail, head)."""
        out_edge = {}
        for i in range(self.n):
            out_edge[r[i]] = (i, r[i], s[i])
        seen = set()
        cycles = []
        for v in self.X:
            if v in seen:
                continue
            cyc = []
            w = v
            while w not in seen:
                seen.add(w)
                e = out_edge[w]
                cyc.append(e)
                w = e[2]
            cycles.append(cyc)
        return cycles

    def J3(self, r, s):
        """3 * J(r, s) = sum of delta(r(t), s(t))."""
        return sum(self.delta(a, b) for a, b in zip(r, s))

    # ---- spoke circulation (Lemma 5.3 of the OpenAI paper) --------------------
    def weights(self):
        """a[(face, v)] integer weights on the spokes of H0 with circulation +1 around
        every bounded face of H0, and the per-face flows aw[w][(face, v)] whose sum is a.
        The three white faces next to t0 form the unbounded face."""
        if self._weights is not None:
            return self._weights
        T = self.T
        outer = set()
        a0, b0, c0 = T.faces[self.t0]
        for e in ((a0, b0), (b0, c0), (c0, a0)):
            outer.add(T.de[(e[1], e[0])])
        node = {w: ('O' if w in outer else w) for w in self.white}
        # spokes: (t, v) with left/right white faces for the traversal centre -> v
        spokes = {}
        adj = defaultdict(list)
        for f in self.A:
            a, b, c = T.faces[f]
            for (vm, v, vp) in ((c, a, b), (a, b, c), (b, c, a)):
                left = node[T.de[(vp, v)]]    # across side v -> vp
                right = node[T.de[(v, vm)]]   # across side vm -> v
                spokes[(f, v)] = (left, right)
                adj[left].append((right, (f, v), +1))   # leaving left: +1 on centre->v
                adj[right].append((left, (f, v), -1))
        parent = {'O': None}
        dq = deque(['O'])
        while dq:
            x = dq.popleft()
            for (y, sp, sg) in adj[x]:
                if y not in parent:
                    # tree edge used from y towards x: y is being left
                    parent[y] = (x, sp, -sg)
                    dq.append(y)
        a = defaultdict(int)
        aw = {}
        for w in self.white:
            if node[w] == 'O':
                continue
            d = defaultdict(int)
            x = w
            while parent[x] is not None:
                p, sp, sg = parent[x]
                d[sp] += sg
                a[sp] += sg
                x = p
            aw[w] = dict(d)
        self._weights = (dict(a), aw, node)
        return self._weights

    def omega(self, s):
        a = self.weights()[0]
        return sum(a.get((f, v), 0) for f, v in zip(self.A, s))

    def height(self, s, w):
        aw = self.weights()[1][w]
        return sum(aw.get((f, v), 0) for f, v in zip(self.A, s))

    def check_weights(self):
        """Circulation of a around every white face w not next to t0 equals 1."""
        T = self.T
        a, aw, node = self.weights()
        for w in self.white:
            if node[w] == 'O':
                continue
            p, q, r = T.faces[w]
            circ = 0
            for (x, y) in ((p, q), (q, r), (r, p)):
                t = T.de[(y, x)]
                if t == self.t0:
                    continue
                circ += a.get((t, y), 0) - a.get((t, x), 0)
            assert circ == 1, (w, circ)
        return True

    def cycle_area(self, cyc):
        """L+ - L- for a D-cycle given as list of (i, tail, head), any direction:
        returns the circulation of a along the spoke detour of the cycle as given."""
        a = self.weights()[0]
        return sum(a.get((self.A[i], h), 0) - a.get((self.A[i], t), 0) for (i, t, h) in cyc)

    def enclosed_white(self, cyc):
        """White faces enclosed by the spoke detour of a counterclockwise cycle given as
        list of (i, tail, head): flood fill over white faces across spokes not on it."""
        T = self.T
        node = self.weights()[2]
        used = set()
        for (i, t, h) in cyc:
            used.add((self.A[i], t))
            used.add((self.A[i], h))
        adj = defaultdict(list)
        for f in self.A:
            a, b, c = T.faces[f]
            for (vm, v, vp) in ((c, a, b), (a, b, c), (b, c, a)):
                if (f, v) in used:
                    continue
                left = node[T.de[(vp, v)]]
                right = node[T.de[(v, vm)]]
                adj[left].append(right)
                adj[right].append(left)
        seen = {'O'}
        dq = deque(['O'])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    dq.append(y)
        return [w for w in self.white if node[w] not in seen]


def dual_ham_cycles(T):
    """All Hamiltonian cycles of the dual cubic graph G = T*, each as a frozenset of
    undirected edges of T (the edges crossed)."""
    F = T.F
    adj = [[] for _ in range(F)]
    for (a, b), f in T.de.items():
        g = T.de[(b, a)]
        adj[f].append((g, frozenset((a, b))))
    res = set()
    start = 0
    (n1, e1), (n2, e2), (n3, e3) = adj[start]
    visited = [False] * F
    visited[start] = True
    path = []

    def dfs(v, count, target, tedge):
        if count == F:
            for (g, e) in adj[v]:
                if g == start and e == tedge:
                    res.add(frozenset(path + [e]))
            return
        for (g, e) in adj[v]:
            if not visited[g]:
                visited[g] = True
                path.append(e)
                dfs(g, count + 1, target, tedge)
                path.pop()
                visited[g] = False

    # cycle through start uses two of its three edges: (e1,e2), (e1,e3), (e2,e3)
    for (first, fe), (last, le) in (((n1, e1), (n2, e2)), ((n1, e1), (n3, e3)), ((n2, e2), (n3, e3))):
        visited[first] = True
        path.append(fe)
        dfs(first, 2, last, le)
        path.pop()
        visited[first] = False
    return res
