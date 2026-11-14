"""Two-tree packing referee code. Independent of the probabilistic folder's code.

Conventions (research/BRIEF.md): T is an Eulerian triangulation given by a rotation
system, t0 a black face, R its corners, A the other black faces, X the nonroots.
W is the white-face graph: vertices are white faces, and every spoke (t, v) of every
black face t (including t0) gives the edge joining the white faces across the two sides
of t at v.  W is the plane dual of the spoke graph H.

A "2-selection" is a map u: A -> V(T) with u(t) a corner of t (the deleted corner).  Its
support F(u) is the set of spokes (t, v), v != u(t), t in A.  When u comes from a pair
(r, s), F(u) is the pair support E_r + E_s.  The packing question asks whether the W-edges
of F(u) split into two spanning trees of W.
"""
import itertools
import random
import subprocess
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLANTRI = ROOT / 'workings/barnette_lab/vendor/plantri.exe'


# ---------------------------------------------------------------- triangulations

def plantri(vertices, extra=()):
    """Yield rotation systems (list of neighbour lists) of all Eulerian triangulations."""
    out = subprocess.run([str(PLANTRI), '-ba', *extra, str(vertices)], capture_output=True,
                         text=True, check=True).stdout
    for line in out.splitlines():
        n, data = line.split()
        rot = [[ord(c) - ord('a') for c in s] for s in data.split(',')]
        assert len(rot) == int(n)
        yield rot


def rotation_from_faces(faces):
    """Rotation system from a list of oriented triangles (all oriented consistently)."""
    nxt = {}
    for f in faces:
        for i in range(3):
            a, b, c = f[i], f[(i + 1) % 3], f[(i + 2) % 3]
            # around a: going from neighbour c to neighbour b
            nxt[a, c] = b
    verts = sorted({v for f in faces for v in f})
    idx = {v: i for i, v in enumerate(verts)}
    rot = []
    for v in verts:
        nbrs = sorted({b for (a, b) in nxt if a == v})
        start = nbrs[0]
        cyc = [start]
        while True:
            w = nxt[v, cyc[-1]]
            if w == start:
                break
            cyc.append(w)
        assert len(cyc) == len(nbrs), 'not a disk-free rotation'
        rot.append([idx[w] for w in cyc])
    return rot, verts


class Tri:
    """Embedded Eulerian triangulation with a face 2-colouring."""

    def __init__(self, rot):
        self.rot = rot
        self.V = len(rot)
        pos = [{w: i for i, w in enumerate(r)} for r in rot]
        faces, fid = [], {}
        for u in range(self.V):
            for v in rot[u]:
                if (u, v) in fid:
                    continue
                f, a, b = [], u, v
                while (a, b) not in fid:
                    fid[a, b] = len(faces)
                    f.append(a)
                    r = rot[b]
                    c = r[(pos[b][a] - 1) % len(r)]
                    a, b = b, c
                faces.append(tuple(f))
        assert all(len(f) == 3 for f in faces), 'not a triangulation'
        self.faces, self.fid = faces, fid
        # colour faces: faces sharing an edge get opposite colours
        col = [None] * len(faces)
        col[0] = 0
        q = deque([0])
        while q:
            f = q.popleft()
            a, b, c = faces[f]
            for x, y in ((a, b), (b, c), (c, a)):
                g = fid[y, x]
                if col[g] is None:
                    col[g] = 1 - col[f]
                    q.append(g)
                assert col[g] != col[f], 'not Eulerian'
        self.col = col
        self.E = sorted({tuple(sorted(e)) for e in fid})
        self.adj = [set(r) for r in rot]


class Rooted:
    """Rooted instance: t0 is face index `outer`, coloured black."""

    def __init__(self, tri, outer):
        self.tri = tri
        blackcol = tri.col[outer]
        F = tri.faces
        self.outer = outer
        self.black = [i for i in range(len(F)) if tri.col[i] == blackcol]
        self.white = [i for i in range(len(F)) if tri.col[i] != blackcol]
        self.widx = {f: i for i, f in enumerate(self.white)}
        self.R = set(F[outer])
        self.X = [v for v in range(tri.V) if v not in self.R]
        self.A = [t for t in self.black if t != outer]
        self.n = len(self.A)
        assert self.n == len(self.X)
        # white face across the undirected edge {a,b}
        self.wacross = {}
        for (a, b), f in tri.fid.items():
            if tri.col[f] != blackcol:
                self.wacross[frozenset((a, b))] = self.widx[f]
        # W-edge of spoke (t, v)
        self.wedge = {}
        for t in self.black:
            a, b, c = F[t]
            for v, (p, q) in ((a, (b, c)), (b, (a, c)), (c, (a, b))):
                self.wedge[t, v] = (self.wacross[frozenset((v, p))], self.wacross[frozenset((v, q))])
        self.dblack = {v: 0 for v in range(tri.V)}
        for t in self.black:
            for v in F[t]:
                self.dblack[v] += 1

    # ------------------------------------------------------------ states, pairs
    def two_factors(self, limit=None):
        """Enumerate deleted-corner maps u of 2-factors of B (pair supports)."""
        F = self.tri.faces
        need = {x: self.dblack[x] - 2 for x in self.X}   # times x must be deleted
        A = self.A
        opts = []
        for t in A:
            roots = [v for v in F[t] if v in self.R]
            if len(roots) > 1:
                raise AssertionError('bounded face with two roots')
            opts.append(roots if roots else list(F[t]))
        # faces left that can still delete x
        remaining = {x: sum(1 for t, o in zip(A, opts) if x in o) for x in self.X}
        u = [None] * len(A)
        out = []

        def rec(i):
            if limit is not None and len(out) >= limit:
                return
            if i == len(A):
                out.append(tuple(u))
                return
            t = A[i]
            for v in opts[i]:
                for w in opts[i]:
                    if w in need:
                        remaining[w] -= 1
                ok = True
                if v in need:
                    if need[v] == 0:
                        ok = False
                    else:
                        need[v] -= 1
                if ok:
                    # feasibility: every x still needs <= remaining
                    if all(need[w] <= remaining[w] for w in opts[i] if w in need):
                        u[i] = v
                        rec(i + 1)
                    if v in need:
                        need[v] += 1
                for w in opts[i]:
                    if w in need:
                        remaining[w] += 1
        rec(0)
        return out

    def support(self, u):
        """W-edges of the 2-selection with deleted corners u (list aligned with A)."""
        F = self.tri.faces
        es = []
        for t, d in zip(self.A, u):
            for v in F[t]:
                if v != d:
                    es.append((t, v, *self.wedge[t, v]))
        return es

    def bcycles(self, u):
        """Alternating cycles of the 2-factor with deleted corners u: lists of (t, v)."""
        F = self.tri.faces
        at_x = {x: [] for x in self.X}
        used = {}
        for t, d in zip(self.A, u):
            used[t] = [v for v in F[t] if v != d]
            for v in used[t]:
                at_x[v].append(t)
        seen, cycles = set(), []
        for t0 in self.A:
            if t0 in seen:
                continue
            cyc, t, v = [], t0, used[t0][0]
            while True:
                seen.add(t)
                cyc.append((t, v))
                t2 = at_x[v][0] if at_x[v][1] == t else at_x[v][1]
                v2 = used[t2][0] if used[t2][1] == v else used[t2][1]
                cyc.append((t2, v))
                t, v = t2, v2
                if t == t0:
                    break
            cycles.append(cyc)
        return cycles

    def states_in(self, u):
        """The 2^c states of the pair group with deleted corners u, as dicts t->v."""
        cyc = self.bcycles(u)
        halves = [(c[0::2], c[1::2]) for c in cyc]
        for bits in itertools.product((0, 1), repeat=len(halves)):
            s = {}
            for b, h in zip(bits, halves):
                for t, v in h[b]:
                    s[t] = v
            yield s

    def is_tree_state(self, s):
        es = [self.wedge[t, s[t]] for t in self.A]
        return is_spanning_tree(len(self.white), es)


# ---------------------------------------------------------------- matroid tools

class DSU:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, a):
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        self.p[a] = b
        return True


def is_spanning_tree(m, es):
    if len(es) != m - 1:
        return False
    d = DSU(m)
    return all(d.union(a, b) for a, b in es)


def forest_path(adj, a, b):
    """Edge ids on the path from a to b in a forest given as adjacency {v: {w: eid}}, or None."""
    if a == b:
        return []
    prev = {a: None}
    q = deque([a])
    while q:
        x = q.popleft()
        for y, e in adj[x].items():
            if y not in prev:
                prev[y] = (x, e)
                if y == b:
                    path = []
                    while prev[y] is not None:
                        x, e = prev[y]
                        path.append(e)
                        y = x
                    return path
                q.append(y)
    return None


def two_tree_partition(m, ends, k=2):
    """Partition edges (list of (a,b), parallel edges allowed) into two forests on m vertices.

    Edmonds' matroid-partition algorithm with shortest augmenting paths.  Returns a list of
    colours 0/1, or None if no partition into two forests exists (then the caller should
    produce a density witness)."""
    colour = [None] * len(ends)
    adj = [{v: {} for v in range(m)} for _ in range(k)]

    def put(e, c):
        a, b = ends[e]
        adj[c][a][b] = e
        adj[c][b][a] = e
        colour[e] = c

    def take(e):
        a, b = ends[e]
        c = colour[e]
        del adj[c][a][b]
        del adj[c][b][a]
        colour[e] = None

    for e0 in range(len(ends)):
        if ends[e0][0] == ends[e0][1]:
            return None  # loop
        parent = {e0: None}
        q = deque([e0])
        term = None
        while q and term is None:
            x = q.popleft()
            a, b = ends[x]
            for c in range(k):
                if colour[x] == c:
                    continue
                path = forest_path(adj[c], a, b)
                if path is None:
                    term = (x, c)
                    break
                for y in path:
                    if y not in parent:
                        parent[y] = (x, c)
                        q.append(y)
        if term is None:
            return None
        x, c = term
        while True:
            if colour[x] is not None:
                take(x)
            put(x, c)
            if parent[x] is None:
                break
            y, c2 = parent[x]
            # y enters forest c2, and x (on its cycle in c2) has just left c2
            x, c = y, c2
            if colour[x] is not None:
                take(x)
    # verify (independent of the algorithm)
    for c in range(k):
        d = DSU(m)
        for e, cc in enumerate(colour):
            if cc == c and not d.union(*ends[e]):
                raise AssertionError('partition produced a cycle')
    return colour


def density_witness(m, ends, k=2):
    """Brute force or flow: a vertex set S with |F[S]| > k(|S|-1).  Returns (S, excess)."""
    import networkx as nx
    best = None
    for v in range(m):
        # max over S containing v of |F[S]| - k|S|  via max closure
        g = nx.DiGraph()
        for i, (a, b) in enumerate(ends):
            g.add_edge('s', ('e', i), capacity=1)
            g.add_edge(('e', i), ('v', a), capacity=float('inf'))
            g.add_edge(('e', i), ('v', b), capacity=float('inf'))
        for w in range(m):
            g.add_edge(('v', w), 't', capacity=k)
        # force v: give it infinite profit instead: connect s->v
        g.add_edge('s', ('v', v), capacity=10 ** 9)
        cut, (S, _) = nx.minimum_cut(g, 's', 't')
        verts = sorted(w for (tag, w) in [x for x in S if isinstance(x, tuple)] if tag == 'v')
        inside = sum(1 for a, b in ends if a in verts and b in verts)
        exc = inside - k * (len(verts) - 1)
        if best is None or exc > best[1]:
            best = (verts, exc)
    return best


def check_packing(m, ends):
    """Return ('pack', colours) or ('fail', witness)."""
    col = two_tree_partition(m, ends)
    if col is not None:
        return 'pack', col
    return 'fail', density_witness(m, ends)
