"""Eulerian triangulations, states, tree matchings, degree-4 contractions.

Independent implementation for the referee of research/2026-11-14_opus_route-induction.
It shares no code with that folder. Generation uses the plantri 4.5 executable in
workings/barnette_lab/vendor (the brief allows this).

Conventions
-----------
A triangulation is a rotation system `rot[v]` = cyclic list of neighbours, as printed
by `plantri -b -a`. Faces are oriented triples read off the rotation system. A rooted
instance is (blacks, root, nv): the list of black faces as vertex triples, the index
of the root face t0 in that list, and the number of vertex labels. Only the black
faces matter for states, Q_s and tree matchings, so contracted instances (possibly
with parallel edges) are represented by their black triples alone.
"""
import os
import subprocess
import sys

sys.setrecursionlimit(10000)

HERE = os.path.dirname(os.path.abspath(__file__))
PLANTRI = os.path.normpath(os.path.join(HERE, "..", "..", "..", "workings",
                                        "barnette_lab", "vendor", "plantri.exe"))


def plantri(nv):
    """Rotation systems of all Eulerian triangulations with nv vertices, plantri order."""
    out = subprocess.run([PLANTRI, "-b", "-a", str(nv)], capture_output=True, text=True).stdout
    res = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        n, body = line.split(" ", 1)
        rot = [[ord(c) - 97 for c in part] for part in body.split(",")]
        assert len(rot) == int(n)
        res.append(rot)
    return res


def faces_of(rot):
    """Oriented faces (u, v, w): from directed edge (u, v) continue with (v, w) where
    w follows u in rot[v]. Every directed edge lies in exactly one face."""
    nxt = {}
    for v, nb in enumerate(rot):
        d = len(nb)
        for i, u in enumerate(nb):
            nxt[(u, v)] = (v, nb[(i + 1) % d])
    seen = set()
    faces = []
    for e in list(nxt):
        if e in seen:
            continue
        f = []
        cur = e
        while cur not in seen:
            seen.add(cur)
            f.append(cur[0])
            cur = nxt[cur]
        assert len(f) == 3, f
        faces.append(tuple(f))
    return faces


def two_colour(faces):
    """Colour 0/1 so that faces sharing an edge differ. Returns list of colours."""
    side = {}
    for i, f in enumerate(faces):
        for j in range(3):
            side[(f[j], f[(j + 1) % 3])] = i
    col = [None] * len(faces)
    col[0] = 0
    stack = [0]
    while stack:
        i = stack.pop()
        f = faces[i]
        for j in range(3):
            o = side[(f[(j + 1) % 3], f[j])]
            if col[o] is None:
                col[o] = 1 - col[i]
                stack.append(o)
            else:
                assert col[o] != col[i], "not Eulerian"
    return col


def rooted_instances(rot):
    """All rooted instances of a triangulation: every face as t0, its colour class black.
    Yields (blacks, root_index, whites)."""
    faces = faces_of(rot)
    col = two_colour(faces)
    for c in (0, 1):
        blacks = [f for f, cc in zip(faces, col) if cc == c]
        whites = [f for f, cc in zip(faces, col) if cc != c]
        for ri in range(len(blacks)):
            yield blacks, ri, whites


def order_faces(faces, start):
    """Static order: grow from the vertex set `start`, always taking the face with the
    most already-seen corners (ties: first)."""
    seen = set(start)
    rest = list(range(len(faces)))
    order = []
    while rest:
        best = max(rest, key=lambda i: sum(1 for v in faces[i] if v in seen))
        rest.remove(best)
        order.append(best)
        seen.update(faces[best])
    return order


def enum(faces, forbidden, pre_edges, nv, on_leaf, acyclic=True):
    """Enumerate injective corner choices u_i in faces[i], u_i not in `forbidden`.
    With acyclic=True the chosen opposite edges together with pre_edges must be acyclic.
    The caller makes #faces = #allowed vertices so injective means bijective.
    on_leaf(assign, find) is called for each solution; assign[i] is the corner of faces[i].
    Returns the number of solutions."""
    m = len(faces)
    last = {}
    for i, f in enumerate(faces):
        for v in f:
            last[v] = i
    parent = list(range(nv))
    size = [1] * nv
    used = [False] * nv
    for v in forbidden:
        used[v] = True

    def find(a):
        while parent[a] != a:
            a = parent[a]
        return a

    for (a, b) in pre_edges:
        a = find(a)
        b = find(b)
        assert a != b
        parent[b] = a
        size[a] += size[b]
    assign = [None] * m
    count = [0]

    def rec(i):
        if i == m:
            count[0] += 1
            if on_leaf is not None:
                on_leaf(assign, find)
            return
        f = faces[i]
        mand = -1
        cnt = 0
        for v in f:
            if not used[v] and last[v] == i:
                cnt += 1
                mand = v
        if cnt > 1:
            return
        for j in range(3):
            u = f[j]
            if used[u] or (cnt == 1 and u != mand):
                continue
            if acyclic:
                a = find(f[j - 2])
                b = find(f[j - 1])
                if a == b:
                    continue
                if size[a] < size[b]:
                    a, b = b, a
                parent[b] = a
                size[a] += size[b]
                used[u] = True
                assign[i] = u
                rec(i + 1)
                used[u] = False
                parent[b] = b
                size[a] -= size[b]
            else:
                used[u] = True
                assign[i] = u
                rec(i + 1)
                used[u] = False

    rec(0)
    return count[0]


def root_edges(t0):
    return [(t0[0], t0[1]), (t0[1], t0[2])]


def tree_matchings(blacks, ri, nv, collect=False):
    """Number (or list) of tree matchings of the rooted instance. A tree matching is a
    state s such that Q_s plus two root edges is a spanning tree."""
    t0 = blacks[ri]
    A = [f for i, f in enumerate(blacks) if i != ri]
    order = order_faces(A, t0)
    A = [A[i] for i in order]
    out = []
    cb = None
    if collect:
        def cb(assign, find):
            out.append(dict(zip(A, assign)))
    n = enum(A, t0, root_edges(t0), nv, cb)
    return out if collect else n


def count_states(blacks, ri, nv):
    t0 = blacks[ri]
    A = [f for i, f in enumerate(blacks) if i != ri]
    order = order_faces(A, t0)
    A = [A[i] for i in order]
    return enum(A, t0, [], nv, None, acyclic=False)


def has_pair_flow(blacks, ri):
    """Two disjoint states exist iff the incidence graph on A, X has a 2-factor.
    Max flow: source -> face (cap 2), face -> corner (cap 1), corner -> sink (cap 2)."""
    t0 = set(blacks[ri])
    A = [f for i, f in enumerate(blacks) if i != ri]
    X = sorted({v for f in A for v in f} - t0)
    xi = {v: i for i, v in enumerate(X)}
    nA = len(A)
    if nA != len(X):
        return False
    adj = [[xi[v] for v in f if v in xi] for f in A]
    use = [[0] * len(a) for a in adj]          # flow on face->corner edges
    fdeg = [0] * nA
    xdeg = [0] * len(X)
    back = [[] for _ in X]                      # (face, slot) incident edges
    for i, a in enumerate(adj):
        for k, x in enumerate(a):
            back[x].append((i, k))

    def augment(i, seenA, seenX):
        seenA.add(i)
        for k, x in enumerate(adj[i]):
            if use[i][k] or x in seenX:
                continue
            seenX.add(x)
            if xdeg[x] < 2:
                use[i][k] = 1
                xdeg[x] += 1
                return True
            for (i2, k2) in back[x]:
                if use[i2][k2] and i2 not in seenA:
                    if augment(i2, seenA, seenX):
                        use[i2][k2] = 0
                        use[i][k] = 1
                        return True
        return False

    total = 0
    for i in range(nA):
        for _ in range(2):
            if augment(i, set(), set()):
                fdeg[i] += 1
                total += 1
    return total == 2 * nA


# ---------------------------------------------------------------- structure

def edges_from_faces(faces):
    """Multiset of undirected edges, one per face side of the given faces."""
    es = []
    for f in faces:
        for j in range(3):
            a, b = f[j], f[(j + 1) % 3]
            es.append((a, b) if a < b else (b, a))
    return es


def is_simple(blacks):
    es = edges_from_faces(blacks)
    return len(set(es)) == len(es) and all(a != b for a, b in es)


def adjacency(blacks):
    adj = {}
    for a, b in edges_from_faces(blacks):
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return adj


def separating_triangles(blacks, whites, t0):
    """For a simple triangulation: list of (triangle, inner_black) where inner_black is
    True when the faces along the triangle on the side away from t0 are black."""
    adj = adjacency(blacks)
    facial = {frozenset(f) for f in blacks} | {frozenset(f) for f in whites}
    isblack = {frozenset(f): True for f in blacks}
    verts = sorted(adj)
    res = []
    for u in verts:
        for v in adj[u]:
            if v <= u:
                continue
            for w in adj[u] & adj[v]:
                if w <= v:
                    continue
                tri = frozenset((u, v, w))
                if tri in facial:
                    continue
                # component of T - tri containing a vertex of t0
                start = next(z for z in t0 if z not in tri)
                comp = {start}
                stack = [start]
                while stack:
                    y = stack.pop()
                    for z in adj[y]:
                        if z not in tri and z not in comp:
                            comp.add(z)
                            stack.append(z)
                cols = set()
                for f in facial:
                    if len(f & tri) == 2:
                        (third,) = f - tri
                        if third not in comp:
                            cols.add(isblack.get(f, False))
                assert len(cols) == 1, (tri, cols)
                res.append((tuple(sorted(tri)), cols.pop()))
    return res


def degree4_setups(blacks, whites, t0):
    """All (x, a, v1, b, v2) with x a non-root vertex of degree 4, black faces
    {x,a,v1}, {x,b,v2}, white faces {x,v1,b}, {x,v2,a}. Each x appears once; the
    mirror naming (a<->b, v1<->v2) describes the same configuration."""
    deg = {}
    for f in blacks:
        for v in f:
            deg[v] = deg.get(v, 0) + 2
    out = []
    for x in sorted(deg):
        if deg[x] != 4 or x in t0:
            continue
        bf = [f for f in blacks if x in f]
        wf = [set(f) - {x} for f in whites if x in f]
        assert len(bf) == 2 and len(wf) == 2
        a, v1 = [v for v in bf[0] if v != x]
        others = [v for v in bf[1] if v != x]
        (b,) = [v for v in others if {v1, v} in wf]
        (v2,) = [v for v in others if v != b]
        assert {v2, a} in wf
        out.append((x, a, v1, b, v2))
    return out


def contract(blacks, ri, x, keep, drop):
    """Delete the faces at x and rename drop -> keep. Returns (blacks', ri') or None if
    a loop would appear (keep ~ drop). If drop is a root, keep and drop are swapped."""
    t0 = blacks[ri]
    if drop in t0:
        keep, drop = drop, keep
    if drop in t0:
        return None                      # both roots: adjacent, loop
    new = []
    nri = None
    for i, f in enumerate(blacks):
        if x in f:
            continue
        if keep in f and drop in f:
            return None                  # loop
        g = tuple(keep if v == drop else v for v in f)
        if i == ri:
            nri = len(new)
        new.append(g)
    return new, nri


def contract_whites(whites, x, keep, drop):
    return [tuple(keep if v == drop else v for v in f) for f in whites if x not in f]
