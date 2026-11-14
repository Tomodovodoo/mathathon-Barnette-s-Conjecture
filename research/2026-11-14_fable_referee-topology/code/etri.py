"""Independent implementation of rooted Eulerian triangulations and the proof objects.

Written for research/2026-11-14_fable_referee-topology. It shares no code with
research/2026-11-14_opus_route-topology/code/topo.py or workings/barnette_lab.
The only external piece is the plantri binary, whose ASCII output already contains
the rotation system, so no planarity routine is needed.

Conventions
-----------
rot[v]   cyclic list of neighbours of v (plantri order, consistent orientation).
dart     ordered pair (u, v) of adjacent vertices.
face_of  dart -> face index; the face containing dart (u, v) is called the LEFT face
         of u -> v. The other face of the edge is face_of[(v, u)].
delta    delta(u, v) = +1 if the left face of u -> v is black, else -1.
ccw      a directed simple cycle is counterclockwise when the disk it bounds on the
         side away from the outer face t0 lies on its left.
Mirror images exchange nothing in these definitions, so every identity checked here
is independent of whether plantri lists neighbours clockwise or counterclockwise.
"""
import json
import random
import subprocess
from collections import deque
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PLANTRI = REPO / 'workings' / 'barnette_lab' / 'vendor' / 'plantri.exe'


def plantri(v, opts='-ba'):
    """Rotation systems of all Eulerian triangulations with v vertices (3-connected, simple)."""
    run = subprocess.run([str(PLANTRI), opts, str(v)], capture_output=True, text=True)
    out = []
    for line in run.stdout.splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        out.append([[ord(c) - 97 for c in ns] for ns in parts[1].split(',')])
    return out


class Tri:
    def __init__(self, rot):
        self.rot = [list(r) for r in rot]
        self.nv = len(self.rot)
        self.pos = [{u: i for i, u in enumerate(r)} for r in self.rot]
        self.face_of = {}
        self.faces = []
        for u in range(self.nv):
            for v in self.rot[u]:
                if (u, v) in self.face_of:
                    continue
                f = len(self.faces)
                cyc = []
                a, b = u, v
                while (a, b) not in self.face_of:
                    self.face_of[(a, b)] = f
                    cyc.append(a)
                    r = self.rot[b]
                    c = r[(self.pos[b][a] + 1) % len(r)]
                    a, b = b, c
                if len(cyc) != 3:
                    raise ValueError('not a triangulation')
                self.faces.append(tuple(cyc))
        if len(self.faces) != 2 * (self.nv - 2):
            raise ValueError('Euler count fails')
        # proper 2-colouring of the faces
        col = [None] * len(self.faces)
        col[0] = 0
        dq = deque([0])
        while dq:
            f = dq.popleft()
            a, b, c = self.faces[f]
            for (x, y) in ((a, b), (b, c), (c, a)):
                g = self.face_of[(y, x)]
                if col[g] is None:
                    col[g] = 1 - col[f]
                    dq.append(g)
                elif col[g] == col[f]:
                    raise ValueError('not Eulerian')
        self.col = col

    def face_by_vertices(self, triple):
        s = set(triple)
        for i, f in enumerate(self.faces):
            if set(f) == s:
                return i
        raise KeyError(triple)

    def edges(self):
        return [(u, v) for u in range(self.nv) for v in self.rot[u] if u < v]

    def separating_triangles(self):
        """All 3-cycles that are not faces, as sorted triples."""
        fs = {frozenset(f) for f in self.faces}
        out = []
        nb = [set(r) for r in self.rot]
        for a in range(self.nv):
            for b in self.rot[a]:
                if b <= a:
                    continue
                for c in nb[a] & nb[b]:
                    if c > b and frozenset((a, b, c)) not in fs:
                        out.append((a, b, c))
        return out


class Inst:
    """Rooted instance: triangulation plus outer face f0, recoloured so that f0 is black."""

    def __init__(self, tri, f0):
        self.tri = tri
        self.f0 = f0
        self.nv = tri.nv
        self.faces = tri.faces
        self.face_of = tri.face_of
        self.black = [tri.col[f] == tri.col[f0] for f in range(len(tri.faces))]
        self.R = tuple(tri.faces[f0])
        self.Rset = set(self.R)
        self.X = [v for v in range(tri.nv) if v not in self.Rset]
        self.A = [f for f in range(len(tri.faces)) if self.black[f] and f != f0]
        self.Wh = [f for f in range(len(tri.faces)) if not self.black[f]]
        self.n = len(self.A)
        assert self.n == len(self.X) == tri.nv - 3
        # black faces at each vertex
        self.bf = [[] for _ in range(tri.nv)]
        for f in range(len(tri.faces)):
            if self.black[f]:
                for v in tri.faces[f]:
                    self.bf[v].append(f)
        # dual edge of the spoke (t, v): the two white faces across the sides of t at v
        self.spoke_dual = {}
        for t in range(len(tri.faces)):
            if not self.black[t]:
                continue
            a, b, c = tri.faces[t]
            for (p, q, r) in ((a, b, c), (b, c, a), (c, a, b)):
                # corner p; sides p-q (dart p->q in t) and r-p (dart r->p in t)
                self.spoke_dual[(t, p)] = (tri.face_of[(q, p)], tri.face_of[(p, r)])

    # ------------------------------------------------------------ basic geometry
    def delta(self, u, v):
        return 1 if self.black[self.face_of[(u, v)]] else -1

    def black_face_of_edge(self, u, v):
        f = self.face_of[(u, v)]
        return f if self.black[f] else self.face_of[(v, u)]

    def opposite_edge(self, t, v):
        a, b, c = self.faces[t]
        if v == a:
            return (b, c)
        if v == b:
            return (c, a)
        return (a, b)

    def inside_faces(self, cyc):
        """Faces on the side of the simple cycle cyc (vertex list) away from f0."""
        h = len(cyc)
        blocked = set()
        for i in range(h):
            u, v = cyc[i], cyc[(i + 1) % h]
            blocked.add((u, v))
            blocked.add((v, u))
        seen = {self.f0}
        dq = deque([self.f0])
        while dq:
            f = dq.popleft()
            a, b, c = self.faces[f]
            for (x, y) in ((a, b), (b, c), (c, a)):
                if (x, y) in blocked:
                    continue
                g = self.face_of[(y, x)]
                if g not in seen:
                    seen.add(g)
                    dq.append(g)
        return [f for f in range(len(self.faces)) if f not in seen]

    def black_inner_triangles(self):
        """Separating triangles whose three inner faces (side away from f0) are black."""
        out = []
        for tr in self.tri.separating_triangles():
            ins = set(self.inside_faces(list(tr)))
            a, b, c = tr
            ok = True
            for (x, y) in ((a, b), (b, c), (c, a)):
                f = self.face_of[(x, y)]
                g = self.face_of[(y, x)]
                inner = f if f in ins else g
                if not self.black[inner]:
                    ok = False
            if ok:
                out.append(tr)
        return out

    # ------------------------------------------------------------ states
    def states(self, limit=None):
        """All states as tuples s with s[i] the vertex chosen in face A[i]."""
        A = self.A
        cand = [[v for v in self.faces[t] if v not in self.Rset] for t in A]
        order = sorted(range(len(A)), key=lambda i: len(cand[i]))
        used = set()
        cur = [None] * len(A)
        out = []

        def rec(j):
            if limit is not None and len(out) >= limit:
                return
            if j == len(order):
                out.append(tuple(cur))
                return
            i = order[j]
            for v in cand[i]:
                if v not in used:
                    used.add(v)
                    cur[i] = v
                    rec(j + 1)
                    used.discard(v)
            cur[i] = None

        rec(0)
        return out

    def random_state(self, rng):
        """A uniformly shuffled augmenting-path matching (not uniform over states)."""
        A = self.A
        cand = [[v for v in self.faces[t] if v not in self.Rset] for t in A]
        for c in cand:
            rng.shuffle(c)
        match_v = {}

        def aug(i, seen):
            for v in cand[i]:
                if v in seen:
                    continue
                seen.add(v)
                if v not in match_v or aug(match_v[v], seen):
                    match_v[v] = i
                    return True
            return False

        idx = list(range(len(A)))
        rng.shuffle(idx)
        for i in idx:
            if not aug(i, set()):
                return None
        s = [None] * len(A)
        for v, i in match_v.items():
            s[i] = v
        return tuple(s)

    def Q_edges(self, s):
        return [self.opposite_edge(t, s[i]) for i, t in enumerate(self.A)]

    def q_structure(self, s):
        """Components of Q_s: list of (vertices, n_edges, n_roots)."""
        par = list(range(self.nv))

        def find(x):
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x

        E = self.Q_edges(s)
        for u, v in E:
            par[find(u)] = find(v)
        comp = {}
        for v in range(self.nv):
            comp.setdefault(find(v), [[], 0, 0])
            comp[find(v)][0].append(v)
            if v in self.Rset:
                comp[find(v)][2] += 1
        for u, v in E:
            comp[find(u)][1] += 1
        return list(comp.values())

    def is_tree_matching(self, s):
        return all(ne == len(vs) - 1 and nr == 1 for vs, ne, nr in self.q_structure(s))

    def n_unicyclic(self, s):
        """Number k of cycles of Q_s if s has a mate, else None."""
        k = 0
        for vs, ne, nr in self.q_structure(s):
            if ne == len(vs) - 1 and nr == 1:
                continue
            if ne == len(vs) and nr == 0:
                k += 1
                continue
            return None
        return k

    def mates(self, s):
        """All states r with r(t) != s(t) for every t, built from orientations of Q_s."""
        if self.n_unicyclic(s) is None:
            return []
        A = self.A
        E = self.Q_edges(s)
        adj = [[] for _ in range(self.nv)]
        for i, (u, v) in enumerate(E):
            adj[u].append((v, i))
            adj[v].append((u, i))
        # peel leaves that are not roots: forced orientation leaf -> neighbour
        deg = [len(a) for a in adj]
        tail = [None] * len(E)
        alive = [True] * len(E)
        dq = deque(v for v in range(self.nv) if deg[v] == 1 and v not in self.Rset)
        while dq:
            v = dq.popleft()
            if deg[v] != 1:
                continue
            for (w, i) in adj[v]:
                if alive[i]:
                    alive[i] = False
                    tail[i] = v
                    deg[v] -= 1
                    deg[w] -= 1
                    if deg[w] == 1 and w not in self.Rset:
                        dq.append(w)
        # what remains: disjoint cycles (roots have degree 0 now)
        cycles = []
        seen = set()
        for i0 in range(len(E)):
            if not alive[i0] or i0 in seen:
                continue
            u0, v0 = E[i0]
            cyc_e = [i0]
            cyc_v = [u0, v0]
            seen.add(i0)
            prev, cur = i0, v0
            while cur != u0:
                for (w, i) in adj[cur]:
                    if alive[i] and i != prev and i not in seen:
                        seen.add(i)
                        cyc_e.append(i)
                        cyc_v.append(w)
                        prev, cur = i, w
                        break
                else:
                    # closing edge back to u0 through a parallel-free graph
                    for (w, i) in adj[cur]:
                        if alive[i] and i != prev and w == u0:
                            cyc_e.append(i)
                            cyc_v.append(w)
                            prev, cur = i, w
                            break
                    else:
                        raise RuntimeError('cycle tracing failed')
            cycles.append((cyc_e, cyc_v[:-1] if cyc_v[-1] == u0 and len(cyc_v) > len(cyc_e) else cyc_v))
        out = []
        k = len(cycles)
        for mask in range(1 << k):
            tl = list(tail)
            for j, (ce, cv) in enumerate(cycles):
                m = len(ce)
                # edge ce[i] joins cv[i] and cv[(i+1) % m]
                for i in range(m):
                    tl[ce[i]] = cv[i] if not (mask >> j) & 1 else cv[(i + 1) % m]
            out.append(tuple(tl))
        return out

    def J3(self, r, s):
        """3 * J(r, s) = sum of delta(r(t), s(t))."""
        return sum(self.delta(r[i], s[i]) for i in range(len(self.A)) if r[i] != s[i])

    def has_pair_flow(self):
        """Degree-2 spanning subgraph of B by augmenting paths on doubled faces."""
        A = self.A
        cand = [[v for v in self.faces[t] if v not in self.Rset] for t in A]
        # each vertex needs 2 distinct faces, each face needs 2 distinct vertices
        cap_v = {v: 2 for v in self.X}
        use = [set() for _ in A]       # vertices used by face i
        load = {v: set() for v in self.X}

        def aug(i, seen):
            for v in cand[i]:
                if v in use[i] or v in seen:
                    continue
                seen.add(v)
                if len(load[v]) < 2:
                    load[v].add(i)
                    use[i].add(v)
                    return True
                for j in list(load[v]):
                    # try to move face j off v
                    load[v].discard(j)
                    use[j].discard(v)
                    if aug(j, seen):
                        load[v].add(i)
                        use[i].add(v)
                        return True
                    load[v].add(j)
                    use[j].add(v)
            return False

        for i in range(len(A)):
            for _ in range(2):
                if not aug(i, set()):
                    return False
        return True


# ---------------------------------------------------------------- generators
def all_rooted(vmin, vmax, roots='all'):
    """Yield (V, index, f0, Inst). roots='all' uses every face as outer face."""
    for v in range(vmin, vmax + 1):
        for idx, rot in enumerate(plantri(v)):
            tri = Tri(rot)
            fs = range(len(tri.faces)) if roots == 'all' else roots(tri)
            for f0 in fs:
                yield v, idx, f0, Inst(tri, f0)


def load_rot_json(path):
    d = json.load(open(path))
    rot = [d['rot'][str(i)] for i in range(len(d['rot']))]
    return rot, d


def octahedron_rot():
    # vertices 0..5, antipodes (0,5), (1,3), (2,4)
    return [[1, 2, 3, 4], [0, 4, 5, 2], [0, 1, 5, 3], [0, 2, 5, 4], [0, 3, 5, 1], [1, 4, 3, 2]]


def split_vertex(rot, v, i, j):
    """Degree-4 insertion at v: neighbours a = rot[v][i], b = rot[v][j] stay adjacent to both
    halves; v keeps the neighbours strictly between i and j (cyclically), a new vertex v2 gets
    the others, and a new vertex x of degree 4 is joined to a, v, b, v2.
    Requires an odd number of neighbours strictly inside each of the two arcs."""
    rot = [list(r) for r in rot]
    d = len(rot[v])
    a, b = rot[v][i], rot[v][j]
    arc1 = [rot[v][(i + k) % d] for k in range(1, (j - i) % d)]
    arc2 = [rot[v][(j + k) % d] for k in range(1, (i - j) % d)]
    assert len(arc1) % 2 == 1 and len(arc2) % 2 == 1
    v2 = len(rot)
    x = v2 + 1
    # around v (same orientation as before): a, arc1, b, then x
    rot[v] = [a] + arc1 + [b, x]
    rot.append([b] + arc2 + [a, x])          # v2: b, arc2, a, x
    rot.append([a, v2, b, v])                # x: fixed below by orientation test
    for u in arc2:
        k = rot[u].index(v)
        rot[u][k] = v2
    # at a the old order was ..., arc1[0], v, arc2[-1], ...; now arc1[0], v, x, v2, arc2[-1]
    k = rot[a].index(v)
    rot[a][k:k + 1] = [v, x, v2]
    # at b the old order was ..., arc2[0], v, arc1[-1], ...; now arc2[0], v2, x, v, arc1[-1]
    k = rot[b].index(v)
    rot[b][k:k + 1] = [v2, x, v]
    for xr in ([a, v2, b, v], [a, v, b, v2]):
        rot[x] = xr
        try:
            Tri(rot)
            return rot
        except Exception:
            continue
    raise ValueError('split failed')


def glue_octahedron(rot, tri, f):
    """Insert an octahedron into face f: three new vertices, creates a separating triangle."""
    rot = [list(r) for r in rot]
    a, b, c = tri.faces[f]
    n = len(rot)
    p, q, r = n, n + 1, n + 2          # p opposite c (between a, b), q opposite a, r opposite b
    # face (a, b, c) traced as darts a->b, b->c, c->a. In rot[b], a is followed by c.
    # So in rot[x] the face lies between pred and succ: at b between a and c, etc.
    def ins(x, first, new):
        k = rot[x].index(first)
        rot[x][k + 1:k + 1] = new
    ins(b, a, [p, q])
    ins(c, b, [q, r])
    ins(a, c, [r, p])
    for cand in ((([a, r, q, b]), ([b, p, r, c]), ([c, q, p, a])),
                 (([b, q, r, a]), ([c, r, p, b]), ([a, p, q, c]))):
        rr = [list(z) for z in rot] + [list(cand[0]), list(cand[1]), list(cand[2])]
        try:
            Tri(rr)
            return rr
        except Exception:
            continue
    raise ValueError('glue failed')


def random_eulerian(v_target, rng, glue_prob=0.0):
    """Random Eulerian triangulation by degree-4 insertions (and optional octahedron gluings).
    Not uniform. Simplicity is checked after every step."""
    rot = octahedron_rot()
    while len(rot) < v_target:
        if glue_prob and len(rot) + 3 <= v_target and rng.random() < glue_prob:
            tri = Tri(rot)
            try:
                rot = glue_octahedron(rot, tri, rng.randrange(len(tri.faces)))
            except Exception:
                pass
            continue
        if len(rot) + 2 > v_target:
            break
        v = rng.randrange(len(rot))
        d = len(rot[v])
        i = rng.randrange(d)
        gaps = [g for g in range(2, d - 1, 2)]
        if not gaps:
            continue
        j = (i + rng.choice(gaps)) % d
        try:
            new = split_vertex(rot, v, i, j)
        except Exception:
            continue
        if all(len(set(r)) == len(r) for r in new):
            rot = new
    return rot
