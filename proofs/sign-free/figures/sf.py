"""Objects of the note sign-free.tex.

An Eulerian triangulation T is given by its list of faces; the outer black face is t0.
A = black faces other than t0 (index 0..n-1), X = vertices other than the roots,
H^+ = the arcs from a point in each black face to its corners (called spokes in the code), W = its plane dual.
A map sigma: X -> A is stored as a dict x -> index in A.
"""
import itertools


class Inst:
    def __init__(self, faces, t0):
        """faces: list of sorted vertex triples; t0: index of the outer face (coloured black)."""
        self.faces = [tuple(sorted(f)) for f in faces]
        self.V = 1 + max(max(f) for f in self.faces)
        edge_faces = {}
        for i, f in enumerate(self.faces):
            for e in itertools.combinations(f, 2):
                edge_faces.setdefault(e, []).append(i)
        assert all(len(v) == 2 for v in edge_faces.values())
        self.edge_faces = edge_faces
        col = {t0: 1}
        stack = [t0]
        while stack:
            i = stack.pop()
            for e in itertools.combinations(self.faces[i], 2):
                for j in edge_faces[e]:
                    if j != i:
                        if j not in col:
                            col[j] = 1 - col[i]
                            stack.append(j)
                        assert col[j] != col[i], 'faces not 2-colourable'
        self.t0 = self.faces[t0]
        self.R = set(self.t0)
        self.A = [f for i, f in enumerate(self.faces) if col[i] == 1 and i != t0]
        self.white = [f for i, f in enumerate(self.faces) if col[i] == 0]
        self.black = self.A + [self.t0]          # index n is t0
        self.n = len(self.A)
        self.X = [v for v in range(self.V) if v not in self.R]
        assert len(self.X) == self.n and len(self.white) == self.n + 1
        self.at = {v: [i for i, f in enumerate(self.A) if v in f] for v in range(self.V)}
        self.edges = sorted(edge_faces)
        self.adj = {v: set() for v in range(self.V)}
        for a, b in self.edges:
            self.adj[a].add(b)
            self.adj[b].add(a)
        # spokes (i, v), i in 0..n ; the point of black[i] is vertex V + i of H^+
        self.spokes = [(i, v) for i, f in enumerate(self.black) for v in f]
        self.NH = self.V + self.n + 1
        # white-face graph: edge e(t, v) joins the white faces across the two sides of t at v
        wid = {f: k for k, f in enumerate(self.white)}
        self.wedge = {}
        for i, f in enumerate(self.black):
            for v in f:
                ends = []
                for w in f:
                    if w != v:
                        e = tuple(sorted((v, w)))
                        other = [j for j in edge_faces[e] if self.faces[j] != f][0]
                        ends.append(wid[self.faces[other]])
                self.wedge[(i, v)] = tuple(ends)

    # ---- trees -------------------------------------------------------------
    def h_tree(self, removed):
        """Is H^+ minus the spokes in `removed` a spanning tree of H^+?"""
        p = list(range(self.NH))

        def find(a):
            while p[a] != a:
                p[a] = p[p[a]]
                a = p[a]
            return a
        k = 0
        for s in self.spokes:
            if s in removed:
                continue
            a, b = find(self.V + s[0]), find(s[1])
            if a == b:
                return False
            p[a] = b
            k += 1
        return k == self.NH - 1

    def w_tree(self, spokes):
        """Do the duals of the given spokes form a spanning tree of W?"""
        p = list(range(self.n + 1))

        def find(a):
            while p[a] != a:
                p[a] = p[p[a]]
                a = p[a]
            return a
        k = 0
        for s in spokes:
            a, b = (find(z) for z in self.wedge[s])
            if a == b:
                return False
            p[a] = b
            k += 1
        return k == self.n

    def is_rainbow(self, sig):
        return self.h_tree({(sig[x], x) for x in self.X})

    def rainbow_trees(self):
        """All rainbow trees, by brute force over all maps X -> A with x a corner of sigma(x)."""
        out = []
        for choice in itertools.product(*[self.at[x] for x in self.X]):
            sig = dict(zip(self.X, choice))
            if self.is_rainbow(sig):
                out.append(sig)
        return out

    def load(self, sig):
        c = [0] * self.n
        for x in self.X:
            c[sig[x]] += 1
        return c

    def excess(self, sig):
        return sum(abs(c - 1) for c in self.load(sig))

    def alts(self, sig, x):
        """All faces t' != sigma(x) at x with sigma[x := t'] a rainbow tree (the lemma says: exactly one)."""
        res = []
        for t in self.at[x]:
            if t != sig[x]:
                s2 = dict(sig)
                s2[x] = t
                if self.is_rainbow(s2):
                    res.append(t)
        return res

    def alt(self, sig, x):
        a = self.alts(sig, x)
        assert len(a) == 1
        return a[0]

    def parent(self, sig):
        """Parent of each non-root x in H_sigma rooted at the point of t0 (an index into black)."""
        rem = {(sig[x], x) for x in self.X}
        nb = {v: [] for v in range(self.NH)}
        for s in self.spokes:
            if s not in rem:
                nb[self.V + s[0]].append(s[1])
                nb[s[1]].append(self.V + s[0])
        par = {}
        root = self.V + self.n
        seen = {root}
        stack = [root]
        while stack:
            a = stack.pop()
            for b in nb[a]:
                if b not in seen:
                    seen.add(b)
                    par[b] = a
                    stack.append(b)
        return {x: par[x] - self.V for x in self.X}

    # ---- states, 2-factors -------------------------------------------------
    def good_state(self, s):
        """s: dict index in A -> corner. Definition of the paper: Q_s is a forest with one root per component."""
        p = list(range(self.V))

        def find(a):
            while p[a] != a:
                p[a] = p[p[a]]
                a = p[a]
            return a
        for i, f in enumerate(self.A):
            a, b = (find(v) for v in f if v != s[i])
            if a == b:
                return False
            p[a] = b
        return len({find(r) for r in self.R}) == 3

    def states(self):
        out = []

        def rec(i, s, used):
            if i == self.n:
                out.append(dict(s))
                return
            for v in self.A[i]:
                if v not in self.R and v not in used:
                    s[i] = v
                    used.add(v)
                    rec(i + 1, s, used)
                    used.discard(v)
                    del s[i]
        rec(0, {}, set())
        return out

    def two_factors(self):
        """All 2-factors of the incidence graph, each as its deleted-corner map u: index in A -> corner."""
        need = {x: len(self.at[x]) - 2 for x in self.X}     # number of faces at x that must delete x
        out = []
        left = {x: len(self.at[x]) for x in self.X}

        def rec(i, u, cnt):
            if i == self.n:
                if all(cnt[x] == need[x] for x in self.X):
                    out.append(dict(u))
                return
            f = self.A[i]
            roots = [v for v in f if v in self.R]
            if len(roots) > 1:
                return
            cands = roots if roots else list(f)
            for v in f:
                if v not in self.R:
                    left[v] -= 1
            for v in cands:
                if v in self.R:
                    u[i] = v
                    if all(cnt[x] + left[x] >= need[x] for x in f if x not in self.R):
                        rec(i + 1, u, cnt)
                    del u[i]
                elif cnt[v] < need[v]:
                    ok = all(cnt[x] + left[x] >= need[x] for x in f if x not in self.R and x != v)
                    if ok:
                        u[i] = v
                        cnt[v] += 1
                        rec(i + 1, u, cnt)
                        cnt[v] -= 1
                        del u[i]
            for v in f:
                if v not in self.R:
                    left[v] += 1
        if all(need[x] >= 0 for x in self.X):
            rec(0, {}, {x: 0 for x in self.X})
        return out

    def factor_cycles(self, u):
        """Cycles of the 2-factor with deleted-corner map u, as lists of alternating (x, t) incidences."""
        used = {x: [i for i in self.at[x] if u[i] != x] for x in self.X}
        seen = set()
        cycles = []
        for x0 in self.X:
            if x0 in seen:
                continue
            cyc = []
            x, t = x0, used[x0][0]
            while True:
                seen.add(x)
                cyc.append((x, t))
                y = [v for v in self.A[t] if v != x and v != u[t]][0]
                t2 = [i for i in used[y] if i != t][0]
                x, t = y, t2
                if x == x0:
                    break
            cycles.append(cyc)
        return cycles

    def states_in(self, u):
        """The 2^c states inside the 2-factor u."""
        cycles = self.factor_cycles(u)
        out = []
        for bits in itertools.product((0, 1), repeat=len(cycles)):
            s = {}
            for b, cyc in zip(bits, cycles):
                for (x, t) in cyc:
                    if b == 0:
                        s[t] = x
                    else:
                        y = [v for v in self.A[t] if v != x and v != u[t]][0]
                        s[t] = y
            out.append(s)
        return out

    # ---- separating triangles ---------------------------------------------
    def black_inner_triangles(self):
        """Separating triangles whose three inner faces along the sides are black. Returns (triangle, interior)."""
        fs = set(self.faces)
        blackset = set(self.black)
        res = []
        for tri in itertools.combinations(range(self.V), 3):
            a, b, c = tri
            if b not in self.adj[a] or c not in self.adj[a] or c not in self.adj[b] or tri in fs:
                continue
            rest = [v for v in range(self.V) if v not in tri]
            root = [r for r in self.R if r not in tri][0]
            seen = {root}
            stack = [root]
            while stack:
                v = stack.pop()
                for w in self.adj[v]:
                    if w not in tri and w not in seen:
                        seen.add(w)
                        stack.append(w)
            inner = [v for v in rest if v not in seen]
            if not inner:
                continue
            ok = True
            for e in itertools.combinations(tri, 2):
                for j in self.edge_faces[e]:
                    f = self.faces[j]
                    third = [v for v in f if v not in e][0]
                    if third in inner and f not in blackset:
                        ok = False
            if ok:
                res.append((tri, inner))
        return res

    # ---- the evict walk ----------------------------------------------------
    def step(self, sig, t, a):
        """One step from the walk state (sig, t, a). Returns ('stop', sig') or ('go', (sig', t', y))."""
        res = [x for x in self.X if sig[x] == t and x != a]
        assert len(res) == 1
        y = res[0]
        t2 = self.alt(sig, y)
        was = sum(1 for x in self.X if sig[x] == t2)
        s2 = dict(sig)
        s2[y] = t2
        if was == 0:
            return 'stop', s2
        assert was == 1
        return 'go', (s2, t2, y)

    def iota(self, sig, t, cap=100000):
        """The involution iota_t on good states (sig = s^{-1}). Returns (sig', list of walk states)."""
        x0 = [x for x in self.X if sig[x] == t][0]
        t1 = self.alt(sig, x0)
        s1 = dict(sig)
        s1[x0] = t1
        state = (s1, t1, x0)
        walk = [state]
        for _ in range(cap):
            kind, nxt = self.step(*state)
            if kind == 'stop':
                return nxt, walk
            state = nxt
            walk.append(state)
        raise RuntimeError('walk did not stop')


def key(inst, sig):
    return tuple(sig[x] for x in inst.X)
