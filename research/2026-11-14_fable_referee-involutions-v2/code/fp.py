"""Referee code for Section 5 (marks without a drawing) of proofs/involutions.

Written from the text of involutions.tex and of paper/main/barnette.tex, Section 4.
It imports nothing from the author's, the reviser's or the first referee's code.
plantri (workings/barnette_lab/vendor/plantri.exe -ba v) supplies rotation systems.

A "mode" is a rule that gives every white face w an ordered list of crossings
    (t, v, a)   t a face of A, v a corner of t, a = +1 or -1
where a is the signed crossing of the incidence (spoke) from the centre of t
to v, left to right positive.  Path mode reads the list off a face path
(a = -kappa).  Ray mode reads it off an exact straight-line drawing.
Everything after that (objects, signs, both maps, counts) is the same code.
"""
import subprocess, random, itertools, math
from fractions import Fraction as Fr
from collections import deque, Counter

from pathlib import Path
PLANTRI = str(Path(__file__).resolve().parents[3] / 'workings/barnette_lab/vendor/plantri.exe')


def plantri(v):
    out = subprocess.run([PLANTRI, '-ba', str(v)], capture_output=True, text=True).stdout
    return [[[ord(c) - 97 for c in ns] for ns in line.split()[1].split(',')]
            for line in out.splitlines()]


def trace_faces(rot):
    """Oriented triangles from a rotation system. All faces get the same orientation."""
    succ = {}
    for v, ns in enumerate(rot):
        for i, u in enumerate(ns):
            succ[u, v] = ns[(i + 1) % len(ns)]
    seen, faces = set(), []
    for v, ns in enumerate(rot):
        for u in ns:
            if (u, v) in seen:
                continue
            f, a, b = [], u, v
            while (a, b) not in seen:
                seen.add((a, b)); f.append(a)
                a, b = b, succ[a, b]
            assert len(f) == 3
            faces.append(tuple(f))
    return faces


class Inst:
    """Rooted Eulerian triangulation. The triples in `faces` are declared counterclockwise:
    a face lies to the left of each of its three darts."""

    def __init__(self, faces, t0):
        self.faces = [tuple(f) for f in faces]
        self.t0 = t0
        self.left = {}
        for i, (a, b, c) in enumerate(self.faces):
            for d in ((a, b), (b, c), (c, a)):
                assert d not in self.left
                self.left[d] = i
        assert all((b, a) in self.left for (a, b) in self.left)
        nf = len(self.faces)
        self.adj = {i: [] for i in range(nf)}       # dual graph, with the shared side
        for (a, b), i in self.left.items():
            self.adj[i].append(self.left[b, a])
        col = {t0: 0}; q = deque([t0])
        while q:
            i = q.popleft()
            for j in self.adj[i]:
                if j not in col:
                    col[j] = 1 - col[i]; q.append(j)
                else:
                    assert col[j] != col[i]
        self.black = [i for i in range(nf) if col[i] == 0]
        self.white = [i for i in range(nf) if col[i] == 1]
        self.A = [i for i in self.black if i != t0]
        self.R = set(self.faces[t0])
        self.V = sorted({v for f in self.faces for v in f})
        self.X = [v for v in self.V if v not in self.R]
        self.n = len(self.A)
        assert len(self.X) == self.n and len(self.black) == len(self.white)
        self.pos = {t: k for k, t in enumerate(self.A)}
        self._inside = {}
        self.states = self._states(None)

    # ---------- states and pairs
    def _states(self, avoid):
        A, faces, R = self.A, self.faces, self.R
        out = []

        def rec(k, used, cur):
            if k == len(A):
                out.append(tuple(cur)); return
            for v in faces[A[k]]:
                if v in R or v in used or (avoid is not None and avoid[k] == v):
                    continue
                used.add(v); cur.append(v)
                rec(k + 1, used, cur)
                cur.pop(); used.discard(v)
        rec(0, set(), [])
        return out

    def pairs(self):
        return [(r, s) for s in self.states for r in self._states(s)]

    def delta(self, u, v):
        return 1 if self.left[u, v] in self.black else -1

    def third(self, k, a, b):
        return next(x for x in self.faces[self.A[k]] if x != a and x != b)

    # ---------- cycles of D_p
    def dcycles(self, p):
        """Cycles of D_p as tuples of positions in A, in the order of traversal."""
        r, s = p
        byr = {v: k for k, v in enumerate(r)}
        seen, out = set(), []
        for k0 in range(self.n):
            if k0 in seen:
                continue
            cyc, k = [], k0
            while k not in seen:
                seen.add(k); cyc.append(k); k = byr[s[k]]
            out.append(tuple(cyc))
        return out

    def inside(self, edges):
        """Faces separated from t0 by a set of undirected edges (frozenset of frozensets)."""
        if edges in self._inside:
            return self._inside[edges]
        seen = {self.t0}; q = deque([self.t0])
        while q:
            i = q.popleft()
            a, b, c = self.faces[i]
            for d in ((a, b), (b, c), (c, a)):
                if frozenset(d) in edges:
                    continue
                j = self.left[d[1], d[0]]
                if j not in seen:
                    seen.add(j); q.append(j)
        ins = frozenset(set(range(len(self.faces))) - seen)
        self._inside[edges] = ins
        return ins

    def cyc_info(self, p, cyc):
        """(inside faces, is_counterclockwise) for a cycle of D_p."""
        r, s = p
        edges = frozenset(frozenset((r[k], s[k])) for k in cyc)
        ins = self.inside(edges)
        lefts = {self.left[r[k], s[k]] in ins for k in cyc}
        assert len(lefts) == 1 and ins
        return ins, lefts.pop()

    def J(self, p):
        r, s = p
        tot = sum(self.delta(r[k], s[k]) for k in range(self.n))
        assert tot % 3 == 0
        return tot // 3

    # ---------- Q_s
    def qcycles(self, p):
        """Cycles of Q_s as sorted tuples of supplying positions; needs the partner r."""
        r, s = p
        out_edge = {}
        for k in range(self.n):
            out_edge[r[k]] = (k, self.third(k, r[k], s[k]))
        seen, cycles = {}, []
        for v0 in self.X:
            if v0 in seen:
                continue
            path, v = [], v0
            while v in out_edge and v not in seen:
                seen[v] = v0; path.append(v); v = out_edge[v][1]
            if v in out_edge and seen[v] == v0:      # closed a new cycle at v
                i = path.index(v)
                cycles.append(tuple(sorted(out_edge[x][0] for x in path[i:])))
        return sorted(cycles)

    def qcycles_from_s(self, s):
        """The same cycles from s alone: 2-core of the graph Q_s (each component is unicyclic or a tree)."""
        edges = {}
        for k in range(self.n):
            a, b = [x for x in self.faces[self.A[k]] if x != s[k]]
            edges[k] = (a, b)
        deg = Counter()
        for a, b in edges.values():
            deg[a] += 1; deg[b] += 1
        alive = dict(edges); changed = True
        while changed:
            changed = False
            for k, (a, b) in list(alive.items()):
                if deg[a] == 1 or deg[b] == 1:
                    del alive[k]; deg[a] -= 1; deg[b] -= 1; changed = True
        # remaining edges form disjoint cycles when a partner exists
        comp, cycles = {}, []
        for k, (a, b) in alive.items():
            if k in comp:
                continue
            cyc, stack = [], [k]
            while stack:
                e = stack.pop()
                if e in comp:
                    continue
                comp[e] = k; cyc.append(e)
                for e2, (c, d) in alive.items():
                    if e2 not in comp and {c, d} & set(alive[e]):
                        stack.append(e2)
            cycles.append(tuple(sorted(cyc)))
        return sorted(cycles)

    # ---------- face paths
    def side(self, i, j):
        sh = set(self.faces[i]) & set(self.faces[j])
        assert len(sh) == 2
        return sh

    def path_crossings(self, paths):
        """paths[w] = [w, f1, ..., t0]. Returns cr[w] = list of (k, v, a, step) and kappa data."""
        cr = {}
        for w in self.white:
            P = paths[w]
            assert P[0] == w and P[-1] == self.t0 and len(set(P)) == len(P)
            assert all(P[i + 1] in self.adj[P[i]] for i in range(len(P) - 1))
            lst = []
            for i in range(1, len(P) - 1):
                t = P[i]
                if t not in self.pos:
                    continue
                e_in, e_out = self.side(P[i - 1], t), self.side(t, P[i + 1])
                (v,) = e_in & e_out
                (a1,) = e_in - {v}
                (b1,) = e_out - {v}
                f = self.faces[t]
                ccw = (v, a1, b1) in (f, f[1:] + f[:1], f[2:] + f[:2])
                kappa = 1 if ccw else -1          # main paper, Section 4: v on the left iff v, a', b' counterclockwise
                lst.append((self.pos[t], v, -kappa, i))
            cr[w] = lst
        return cr

    def tree_paths(self, kind, seed=0):
        rng = random.Random(seed)
        nf = len(self.faces)
        parent = {self.t0: None}
        if kind in ('bfs+', 'bfs-'):
            q = deque([self.t0])
            while q:
                i = q.popleft()
                for j in sorted(self.adj[i], reverse=(kind == 'bfs-')):
                    if j not in parent:
                        parent[j] = i; q.append(j)
        elif kind == 'dfs':
            stack = [self.t0]
            while stack:
                i = stack[-1]
                nxt = [j for j in sorted(self.adj[i]) if j not in parent]
                if nxt:
                    parent[nxt[0]] = i; stack.append(nxt[0])
                else:
                    stack.pop()
        elif kind == 'rand':                       # random spanning tree (random Prim)
            frontier = [(self.t0, j) for j in self.adj[self.t0]]
            while len(parent) < nf:
                i, j = frontier.pop(rng.randrange(len(frontier)))
                if j in parent:
                    continue
                parent[j] = i
                frontier.extend((j, x) for x in self.adj[j] if x not in parent)
        elif kind == 'walk':                       # no tree: an independent loop-erased walk for each white face
            paths = {}
            for w in self.white:
                P = [w]
                while P[-1] != self.t0:
                    j = rng.choice(self.adj[P[-1]])
                    if j in P:
                        P = P[:P.index(j) + 1]
                    else:
                        P.append(j)
                paths[w] = P
            return paths
        else:
            raise ValueError(kind)
        paths = {}
        for w in self.white:
            P = [w]
            while parent[P[-1]] is not None:
                P.append(parent[P[-1]])
            paths[w] = P
        return paths

    # ---------- exact drawing and rays
    def tutte(self, corners=None):
        """Exact Tutte drawing, outer triangle t0, bounded faces counterclockwise."""
        a, b, c = self.faces[self.t0]
        # darts of t0 have t0 on the left, so in the plane (t0 unbounded) the roots run clockwise: a, b, c
        fixed = corners or {a: (Fr(0), Fr(0)), b: (Fr(0), Fr(1)), c: (Fr(1), Fr(0))}
        nb = {v: set() for v in self.V}
        for (u, v) in self.left:
            nb[u].add(v)
        X = self.X; idx = {v: i for i, v in enumerate(X)}
        n = len(X)
        M = [[Fr(0)] * (n + 2) for _ in range(n)]
        for v in X:
            i = idx[v]; M[i][i] = Fr(len(nb[v]))
            for u in nb[v]:
                if u in idx:
                    M[i][idx[u]] -= 1
                else:
                    M[i][n] += fixed[u][0]; M[i][n + 1] += fixed[u][1]
        for c0 in range(n):
            piv = next(r for r in range(c0, n) if M[r][c0] != 0)
            M[c0], M[piv] = M[piv], M[c0]
            pv = M[c0][c0]; M[c0] = [x / pv for x in M[c0]]
            for r in range(n):
                if r != c0 and M[r][c0] != 0:
                    f = M[r][c0]; M[r] = [x - f * y for x, y in zip(M[r], M[c0])]
        pos = dict(fixed)
        for v in X:
            pos[v] = (M[idx[v]][n], M[idx[v]][n + 1])
        return pos

    def ray_crossings(self, pos, d, cen=None):
        """Crossings of the ray from each white barycentre in direction d with all spokes of A."""
        cross = lambda p, q: p[0] * q[1] - p[1] * q[0]
        sub = lambda p, q: (p[0] - q[0], p[1] - q[1])
        bary = lambda f: tuple(sum(pos[v][i] for v in self.faces[f]) / 3 for i in (0, 1))
        cen = cen or {f: bary(f) for f in range(len(self.faces)) if f != self.t0}
        # orientation of the drawing
        f = self.faces[self.A[0]]
        ori = 1 if cross(sub(pos[f[1]], pos[f[0]]), sub(pos[f[2]], pos[f[0]])) > 0 else -1
        cr = {}
        for w in self.white:
            W = cen[w]; lst = []
            for P in list(pos.values()) + [cen[t] for t in self.A]:
                if cross(d, sub(P, W)) == 0:
                    return None, ori                 # not generic
            for k, t in enumerate(self.A):
                C = cen[t]
                for v in self.faces[t]:
                    e = sub(pos[v], C)
                    den = cross(d, e)
                    if den == 0:                     # spoke parallel to the ray, and not on its line
                        continue
                    tau = cross(sub(C, W), e) / den
                    mu = cross(sub(W, C), d) / cross(e, d)
                    if tau > 0 and 0 < mu < 1:
                        lst.append((tau, k, v, 1 if den < 0 else -1))
            lst.sort()
            cr[w] = [(k, v, a, None) for (_, k, v, a) in lst]
        return cr, ori


class Model:
    """Objects and the two maps for one instance and one crossing mode."""

    def __init__(self, inst, cr, order=None, marks=None):
        self.I = inst; self.cr = cr
        self.pairs = inst.pairs()
        self.order = order or (lambda key: key)       # total order on unoriented cycles (sorted position tuples)
        self.cyc = {p: inst.dcycles(p) for p in self.pairs}
        self.m = min(len(c) for c in self.cyc.values()) if self.pairs else None
        self.k = self.m if marks is None else marks
        self.Jc = {p: inst.J(p) for p in self.pairs}

    def tokens(self, p):
        r, s = p
        return [(w, i) for w in self.I.white for i, (k, v, a, _) in enumerate(self.cr[w]) if s[k] == v]

    def objects(self):
        for p in self.pairs:
            for M in itertools.combinations(self.tokens(p), self.k):
                yield (p, frozenset(M))

    def sign(self, o):
        p, M = o
        dsum = sum((1 - self.cr[w][i][2]) // 2 for (w, i) in M)       # d = 0 iff left to right
        return -1 if (self.Jc[p] // 2 + dsum) % 2 else 1

    def is_object(self, o):
        p, M = o
        return p in self.cyc and len(M) == self.k and all(p[1][self.cr[w][i][0]] == self.cr[w][i][1] for (w, i) in M)

    def iota1(self, o):
        p, M = o; r, s = p
        qc = self.I.qcycles(p)
        if not qc:
            return o
        K = min(qc, key=self.order)
        r2 = list(r)
        for k in K:
            r2[k] = self.I.third(k, r[k], s[k])
        return ((tuple(r2), s), M)

    def lst(self, p, C, w):
        r, s = p; Cs = set(C)
        return [i for i, (k, v, a, _) in enumerate(self.cr[w]) if k in Cs and v in (r[k], s[k])]

    def reverse(self, p, C):
        r, s = list(p[0]), list(p[1])
        for k in C:
            r[k], s[k] = s[k], r[k]
        return (tuple(r), tuple(s))

    def iota2(self, o, trace=None):
        p, M = o; I = self.I
        cycs = sorted((tuple(sorted(c)) for c in self.cyc[p]), key=self.order)
        which = {k: C for C in cycs for k in C}
        tok = {C: [] for C in cycs}
        for (w, i) in M:
            tok[which[self.cr[w][i][0]]].append((w, i))
        for C in cycs:                                   # case 1
            if not tok[C]:
                if trace is not None: trace.append('unmarked')
                return (self.reverse(p, C), M)
        assert len(cycs) == self.m and all(len(v) == 1 for v in tok.values())
        r, s = p
        info = {}
        for C in cycs:
            (w, i), = tok[C]
            ins, _ = I.cyc_info(p, C)
            L = self.lst(p, C, w)
            info[C] = (w, i, w in ins, L, L.index(i) + 1)
        chosen = next((C for C in cycs if not info[C][2]), None)
        if chosen is None:
            chosen = next((C for C in cycs if info[C][4] != 1), None)
        if chosen is None:
            return o
        w, i, isin, L, j = info[chosen]
        if not isin:
            assert len(L) % 2 == 0
            j2 = j + 1 if j % 2 else j - 1
        else:
            assert len(L) % 2 == 1 and j >= 2
            j2 = j + 1 if j % 2 == 0 else j - 1
        i2 = L[j2 - 1]
        k2, v2 = self.cr[w][i2][0], self.cr[w][i2][1]
        if s[k2] == v2:
            if trace is not None: trace.append('move')
            p2 = p
        else:
            assert r[k2] == v2
            if trace is not None: trace.append('move+reverse')
            p2 = self.reverse(p, chosen)
        return (p2, (M - {(w, i)}) | {(w, i2)})
