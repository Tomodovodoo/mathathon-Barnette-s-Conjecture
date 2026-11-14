"""Core objects for the induction experiments (own implementation, independent of barnette_lab).

A triangulation is stored as faces (oriented vertex triples, all with the same orientation),
a gluing adj[f][i] = (g, j) meaning side i of f (from f[i] to f[i+1]) is glued to side j of g,
and a proper 2-colouring col[f] (0 = black, 1 = white).  Multigraphs (parallel edges, no loops)
are allowed, which the deletion-contraction identities need.

Rooted instance: a triangulation plus a root face t0, recoloured so that t0 is black.
"""
import subprocess, os, sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
PLANTRI = os.path.join(ROOT, 'workings', 'barnette_lab', 'vendor', 'plantri.exe')


class Tri:
    def __init__(self, F, adj, col=None):
        self.F = [tuple(f) for f in F]
        self.adj = [list(a) for a in adj]
        self.verts = sorted({v for f in self.F for v in f})
        if col is None:
            col = two_colour(self.adj)
        self.col = list(col)

    @staticmethod
    def from_faces(F):
        """Simple triangulation: glue by directed edges."""
        de = {}
        for fi, f in enumerate(F):
            for i in range(3):
                de[(f[i], f[(i + 1) % 3])] = (fi, i)
        adj = []
        for fi, f in enumerate(F):
            row = []
            for i in range(3):
                row.append(de[(f[(i + 1) % 3], f[i])])
            adj.append(row)
        return Tri(F, adj)

    def nv(self):
        return len(self.verts)

    def edges(self):
        """Edges indexed by (black face, side)."""
        return [(f, i) for f in range(len(self.F)) if self.col[f] == 0 for i in range(3)]

    def ends(self, f, i):
        F = self.F[f]
        return F[i], F[(i + 1) % 3]

    def degree(self):
        d = {}
        for f in self.F:
            for v in f:
                d[v] = d.get(v, 0) + 1
        return d

    def around(self, x):
        """Faces around x in rotation order, with the neighbour sequence.
        Returns list of (face, idx of x in face)."""
        start = next(fi for fi, f in enumerate(self.F) if x in f)
        out = []
        f = start
        while True:
            i = self.F[f].index(x)
            out.append((f, i))
            g, j = self.adj[f][(i - 1) % 3]  # side from f[i-1] to x
            f = g
            if f == start:
                break
        return out

    def rooted(self, t0):
        col = self.col if self.col[t0] == 0 else [1 - c for c in self.col]
        return Rooted(self, t0, col)

    def is_simple(self):
        seen = set()
        for f, i in self.edges():
            u, v = self.ends(f, i)
            if u == v:
                return False
            k = (min(u, v), max(u, v))
            if k in seen:
                return False
            seen.add(k)
        return True


def two_colour(adj):
    col = [None] * len(adj)
    col[0] = 0
    st = [0]
    while st:
        f = st.pop()
        for g, _ in adj[f]:
            if col[g] is None:
                col[g] = 1 - col[f]
                st.append(g)
            elif col[g] == col[f]:
                raise ValueError('not Eulerian')
    return col


def plantri(n, extra=()):
    out = subprocess.run([PLANTRI, '-b', *extra, '-a', str(n)], capture_output=True, text=True).stdout
    res = []
    for line in out.split('\n'):
        line = line.strip()
        if not line:
            continue
        nv, rest = line.split(' ', 1)
        rot = [[ord(c) - 97 for c in w] for w in rest.split(',')]
        res.append(rot)
    return res


def from_rotation(rot):
    faces = set()
    F = []
    for u, nb in enumerate(rot):
        d = len(nb)
        for k in range(d):
            w, w2 = nb[k], nb[(k + 1) % d]
            tri = (u, w, w2)
            m = min(range(3), key=lambda i: tri[i])
            c = tri[m:] + tri[:m]
            if c not in faces:
                faces.add(c)
                F.append(c)
    return Tri.from_faces(F)


class UF:
    __slots__ = ('p',)

    def __init__(self, vs):
        self.p = {v: v for v in vs}

    def find(self, x):
        p = self.p
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        self.p[a] = b
        return True


class Rooted:
    def __init__(self, T, t0, col):
        self.T, self.t0, self.col = T, t0, col
        F = T.F
        self.R = list(F[t0])
        self.A = [f for f in range(len(F)) if col[f] == 0 and f != t0]
        self.X = [v for v in T.verts if v not in self.R]
        self._states = None
        self._D = None

    # ---- states -------------------------------------------------------
    def states(self):
        """All states as dicts face -> corner."""
        if self._states is not None:
            return self._states
        F, A, Xs = self.T.F, self.A, set(self.X)
        # order faces by BFS for pruning
        order = bfs_order(self.T, A)
        last = {}
        for k, f in enumerate(order):
            for v in F[f]:
                if v in Xs:
                    last[v] = k
        closes = [[] for _ in order]
        for v, k in last.items():
            closes[k].append(v)
        res = []
        used = set()
        cur = {}

        def rec(k):
            if k == len(order):
                res.append(dict(cur))
                return
            f = order[k]
            for v in F[f]:
                if v in Xs and v not in used:
                    used.add(v)
                    cur[f] = v
                    if all(u in used for u in closes[k]):
                        rec(k + 1)
                    used.discard(v)
                    del cur[f]

        if len(A) == len(self.X):
            rec(0)
        self._states = res
        return res

    def Qedges(self, s):
        F = self.T.F
        out = []
        for t, v in s.items():
            i = F[t].index(v)
            out.append((t, (i + 1) % 3))
        return out

    def is_TM(self, s):
        F = self.T.F
        uf = UF(self.T.verts)
        R = self.R
        uf.union(R[0], R[1]); uf.union(R[1], R[2])
        for t, v in s.items():
            i = F[t].index(v)
            if not uf.union(F[t][(i + 1) % 3], F[t][(i + 2) % 3]):
                return False
        return True

    def TMs(self):
        return [s for s in self.states() if self.is_TM(s)]

    def mate_of_TM(self, s):
        """The unique mate of a tree matching: orient Q_s towards the roots."""
        F = self.T.F
        nbr = {v: [] for v in self.T.verts}
        for t, v in s.items():
            i = F[t].index(v)
            a, b = F[t][(i + 1) % 3], F[t][(i + 2) % 3]
            nbr[a].append((b, t)); nbr[b].append((a, t))
        r = {}
        seen = set(self.R)
        st = list(self.R)
        while st:
            u = st.pop()
            for w, t in nbr[u]:
                if w not in seen:
                    seen.add(w)
                    r[t] = w
                    st.append(w)
        return r

    def delta(self, t, v, w):
        f = self.T.F[t]
        i = f.index(v)
        return 1 if f[(i + 1) % 3] == w else -1

    def sign_TM(self, s):
        r = self.mate_of_TM(s)
        e = 1
        for t in self.A:
            e *= self.delta(t, r[t], s[t])
        return e

    # ---- D sets (unions of pairs) ------------------------------------
    def Dsets(self):
        """All D: one side per face of A, both ends nonroot, every nonroot degree 2.
        Returns list of lists of (face, side)."""
        if self._D is not None:
            return self._D
        F, A = self.T.F, self.A
        Xs = set(self.X)
        order = bfs_order(self.T, A)
        last = {}
        for k, f in enumerate(order):
            for v in F[f]:
                if v in Xs:
                    last[v] = k
        closes = [[] for _ in order]
        for v, k in last.items():
            closes[k].append(v)
        deg = {v: 0 for v in self.X}
        res, cur = [], []

        def rec(k):
            if k == len(order):
                res.append(list(cur))
                return
            f = order[k]
            for i in range(3):
                u, w = F[f][i], F[f][(i + 1) % 3]
                if u in Xs and w in Xs and deg[u] < 2 and deg[w] < 2:
                    deg[u] += 1; deg[w] += 1
                    cur.append((f, i))
                    if all(deg[z] == 2 for z in closes[k]):
                        rec(k + 1)
                    cur.pop()
                    deg[u] -= 1; deg[w] -= 1

        if len(A) == len(self.X):
            rec(0)
        self._D = res
        return res

    def cycles(self, D):
        F = self.T.F
        nbr = {}
        for f, i in D:
            u, w = F[f][i], F[f][(i + 1) % 3]
            nbr.setdefault(u, []).append((w, (f, i)))
            nbr.setdefault(w, []).append((u, (f, i)))
        seen, cyc = set(), []
        for v in nbr:
            if v in seen:
                continue
            c = []
            prev_e = None
            u = v
            while True:
                seen.add(u)
                (w1, e1), (w2, e2) = nbr[u]
                nxt, e = (w1, e1) if e1 != prev_e else (w2, e2)
                if e1 == e2:  # 2-cycle on parallel edges
                    nxt, e = (w1, e1) if prev_e is None else (w2, e2)
                c.append(e)
                prev_e = e
                u = nxt
                if u == v:
                    break
            cyc.append(c)
        return cyc

    def white_inside(self, C):
        """Number of white faces inside the cycle C (t0 outside)."""
        T = self.T
        block = set()
        for f, i in C:
            block.add((f, i))
            block.add(T.adj[f][i])
        seen = {self.t0}
        st = [self.t0]
        while st:
            f = st.pop()
            for i in range(3):
                if (f, i) in block:
                    continue
                g, _ = T.adj[f][i]
                if g not in seen:
                    seen.add(g); st.append(g)
        return sum(1 for f in range(len(T.F)) if f not in seen and self.col[f] == 1)

    # ---- invariants ----------------------------------------------------
    def invariants(self, full=True):
        S = self.states()
        tms = [s for s in S if self.is_TM(s)]
        inv = {'states': len(S), 'TM': len(tms)}
        if full:
            pos = sum(1 for s in tms if self.sign_TM(s) > 0)
            inv['TMpos'] = pos
            inv['TMneg'] = len(tms) - pos
            Ds = self.Dsets()
            cs = []
            pairs = 0
            for D in Ds:
                cyc = self.cycles(D)
                cs.append((len(cyc), cyc))
                pairs += 2 ** len(cyc)
            inv['D'] = len(Ds)
            inv['pairs'] = pairs
            if Ds:
                cmin = min(c for c, _ in cs)
                inv['cmin'] = cmin
                lc = 0
                nmin = 0
                for c, cyc in cs:
                    if c == cmin:
                        nmin += 1
                        p = 1
                        for C in cyc:
                            p *= self.white_inside(C)
                        lc += p
                inv['Nmin'] = nmin
                inv['lc'] = lc
            else:
                inv['cmin'] = None; inv['Nmin'] = 0; inv['lc'] = 0
        return inv


def bfs_order(T, A):
    Aset = set(A)
    if not A:
        return []
    order, seen = [], {A[0]}
    st = [A[0]]
    # BFS through faces sharing a vertex
    vf = {}
    for f in A:
        for v in T.F[f]:
            vf.setdefault(v, []).append(f)
    from collections import deque
    q = deque([A[0]])
    while q:
        f = q.popleft()
        order.append(f)
        for v in T.F[f]:
            for g in vf[v]:
                if g not in seen:
                    seen.add(g); q.append(g)
    for f in A:
        if f not in seen:
            order.append(f)
    return order


# ---- reductions --------------------------------------------------------

def rebuild(T, remove, new_faces, glue_pairs, newcol, rename):
    """Remove faces, add new faces, apply vertex renaming, and glue.
    glue_pairs: list of ((f,i),(g,j)) in terms of 'old' face ids or ('n',k) for new faces.
    Returns (Tri, facemap old->new)."""
    keep = [f for f in range(len(T.F)) if f not in remove]
    fmap = {f: k for k, f in enumerate(keep)}
    nk = len(keep)
    for k in range(len(new_faces)):
        fmap[('n', k)] = nk + k
    F = [tuple(rename.get(v, v) for v in T.F[f]) for f in keep] + \
        [tuple(rename.get(v, v) for v in nf) for nf in new_faces]
    col = [T.col[f] for f in keep] + list(newcol)
    adj = [[None] * 3 for _ in F]
    for f in keep:
        for i in range(3):
            g, j = T.adj[f][i]
            if g not in remove:
                adj[fmap[f]][i] = (fmap[g], j)
    for (f, i), (g, j) in glue_pairs:
        adj[fmap[f]][i] = (fmap[g], j)
        adj[fmap[g]][j] = (fmap[f], i)
    assert all(a is not None for row in adj for a in row)
    return Tri(F, adj, col), fmap


def contractions(T):
    """All degree-4 contractions.  Yields dict with x, merged pair (p,q), other pair (o1,o3),
    the resulting Tri (vertex q renamed p), and the face map."""
    deg = T.degree()
    for x in T.verts:
        if deg[x] != 4:
            continue
        ar = T.around(x)
        faces = [f for f, _ in ar]
        # neighbour sequence: in face (f,i), the vertices f[i+1], f[i+2]
        nbs = []
        for f, i in ar:
            nbs.append(T.F[f][(i + 1) % 3])
        # face k contains x, nbs[k], nbs[k-1]?  determine outer side of each face
        outer = []
        for f, i in ar:
            j = (i + 1) % 3  # side opposite x
            outer.append(T.adj[f][j])
        # face k is x, nb_k, nb_{k'} ; compute its two non-x vertices
        pairs_k = [set(T.F[f]) - {x} for f, _ in ar]
        for sel in (0, 1):
            # merge the two neighbours that are opposite
            n4 = []
            # recover cyclic neighbour order a0,a1,a2,a3 such that face k = {a_k, a_{k+1}}
            a = cyc_order(pairs_k)
            p, q = a[sel], a[sel + 2]
            o1, o3 = a[sel + 1], a[(sel + 3) % 4]
            if p == q:
                continue
            # faces containing edge (o, p) and (o, q) for o in (o1,o3)
            def face_with(u, w):
                for k, pk in enumerate(pairs_k):
                    if pk == {u, w}:
                        return k
            k1, k2 = face_with(o1, p), face_with(o1, q)
            k3, k4 = face_with(o3, p), face_with(o3, q)
            glue = [(outer[k1], outer[k2]), (outer[k3], outer[k4])]
            # sanity: outer sides must not be among removed faces
            if any(g in faces for g, _ in [outer[k1], outer[k2], outer[k3], outer[k4]]):
                continue
            Tn, fmap = rebuild(T, set(faces), [], glue, [], {q: p})
            # loops?
            loop = any(len(set(f)) < 3 for f in Tn.F)
            yield dict(x=x, p=p, q=q, o1=o1, o3=o3, faces=faces, T=Tn, fmap=fmap, loop=loop)


def cyc_order(pairs_k):
    """Given the 4 two-sets {a_k,a_{k+1}} in rotation order, return a0..a3."""
    s0, s1 = pairs_k[0], pairs_k[1]
    common = (s0 & s1).pop()
    a0 = (s0 - {common}).pop()
    a1 = common
    a2 = (s1 - {common}).pop()
    s2 = pairs_k[2]
    a3 = (s2 - {a2}).pop()
    return [a0, a1, a2, a3]


def p_reductions(T):
    """Inverse of Batagelj's P-operation: two adjacent degree-4 vertices b,c with two
    common neighbours a,d; the six faces at b and c form the quadrilateral x a e d,
    replaced by the two faces x a e, x e d (new edge x e)."""
    deg = T.degree()
    nb = {}
    for f in T.F:
        for v in f:
            nb.setdefault(v, set()).update(set(f) - {v})
    done = set()
    for b in T.verts:
        if deg[b] != 4:
            continue
        for c in nb[b]:
            if deg[c] != 4 or (c, b) in done:
                continue
            done.add((b, c))
            com = nb[b] & nb[c]
            if len(com) != 2:
                continue
            a, d = sorted(com)
            xs = nb[b] - {a, c, d}
            es = nb[c] - {a, b, d}
            if len(xs) != 1 or len(es) != 1:
                continue
            x, e = xs.pop(), es.pop()
            if x == e:
                continue
            remove = [f for f in range(len(T.F)) if b in T.F[f] or c in T.F[f]]
            if len(remove) != 6:
                continue
            simple = e not in nb[x]
            # outer sides of the quadrilateral
            outer = {}
            for f in remove:
                for i in range(3):
                    u, w = T.F[f][i], T.F[f][(i + 1) % 3]
                    if b not in (u, w) and c not in (u, w):
                        outer[frozenset((u, w))] = (f, i, u, w)
            if set(outer) != {frozenset((x, a)), frozenset((a, e)), frozenset((e, d)), frozenset((d, x))}:
                continue
            if any(T.adj[f][i][0] in remove for f, i, _, _ in outer.values()):
                continue
            # new face 1 contains x a in the same direction as the removed face
            f1, i1, u1, w1 = outer[frozenset((x, a))]
            third = e
            nf1 = (u1, w1, third)
            f2, i2, u2, w2 = outer[frozenset((d, x))]
            nf2 = (u2, w2, e)
            newf = [nf1, nf2]
            glue = []
            for k, nf in enumerate(newf):
                for i in range(3):
                    key = frozenset((nf[i], nf[(i + 1) % 3]))
                    if key == frozenset((x, e)):
                        continue
                    f, j, _, _ = outer[key]
                    glue.append(((('n', k)), i, T.adj[f][j]))
            # x-e sides
            i1 = [i for i in range(3) if frozenset((nf1[i], nf1[(i + 1) % 3])) == frozenset((x, e))][0]
            i2 = [i for i in range(3) if frozenset((nf2[i], nf2[(i + 1) % 3])) == frozenset((x, e))][0]
            gp = [((nk, i), og) for nk, i, og in glue] + [((('n', 0), i1), (('n', 1), i2))]
            newcol = [T.col[f1], T.col[f2]]
            Tn, fmap = rebuild(T, set(remove), newf, gp, newcol, {})
            yield dict(b=b, c=c, a=a, d=d, x=x, e=e, faces=remove, T=Tn, fmap=fmap, simple=simple)
