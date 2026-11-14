"""Eulerian triangulations of the sphere (duals of Barnette graphs).

A triangulation is a list of faces (a, b, c), each listed counterclockwise for one
fixed orientation of the sphere.  Generation: closure of the octahedron under

  P (4-split)       : split a vertex w along two of its edges into w, w' and put a
                      new vertex of degree 4 between them  (+2 vertices);
  Q (octahedron)    : replace a face by an octahedron glued along it (+3 vertices).

Both keep all degrees even.  The class counts are compared in enumerate.py with the
published counts of 3-connected cubic bipartite planar graphs.
"""
from collections import deque


class Tri:
    def __init__(self, faces):
        self.faces = [tuple(f) for f in faces]
        self.F = len(self.faces)
        self.V = 1 + max(max(f) for f in self.faces)
        self.de = {}    # directed edge (a, b) -> index of the face having a->b counterclockwise
        self.nxt = {}   # (w, a) -> b, the neighbour after a counterclockwise around w
        for i, (a, b, c) in enumerate(self.faces):
            for e, third in (((a, b), c), ((b, c), a), ((c, a), b)):
                if e in self.de:
                    raise ValueError("directed edge twice: not an oriented surface")
                self.de[e] = i
                self.nxt[e] = third
        for (a, b) in self.de:
            if (b, a) not in self.de:
                raise ValueError("open surface")
        self.prv = {(w, b): a for (w, a), b in self.nxt.items()}
        E = len(self.de) // 2
        if self.V - E + self.F != 2:
            raise ValueError("not a sphere")
        # face 2-colouring (exists iff all degrees are even)
        col = [None] * self.F
        col[0] = 0
        dq = deque([0])
        while dq:
            f = dq.popleft()
            a, b, c = self.faces[f]
            for e in ((a, b), (b, c), (c, a)):
                g = self.de[(e[1], e[0])]
                if col[g] is None:
                    col[g] = 1 - col[f]
                    dq.append(g)
                elif col[g] == col[f]:
                    raise ValueError("faces not 2-colourable")
        self.fcol = col

    def nbrs(self, w):
        """Neighbours of w in counterclockwise order."""
        a = next(b for (x, b) in self.de if x == w)
        out = [a]
        b = self.nxt[(w, a)]
        while b != a:
            out.append(b)
            b = self.nxt[(w, b)]
        return out

    def degree(self, w):
        return len(self.nbrs(w))

    def is_simple(self):
        # the dict de already forbids repeated directed edges; loops:
        return all(len(set(f)) == 3 for f in self.faces)

    def vertex_colouring(self):
        """Proper 3-colouring col: V -> {0,1,2}.  Faces of colour class fcol==fcol[0]
        read 0,1,2 counterclockwise, the others clockwise."""
        col = {}
        a, b, c = self.faces[0]
        col[a], col[b], col[c] = 0, 1, 2
        dq = deque([0])
        seen = {0}
        while dq:
            f = dq.popleft()
            x, y, z = self.faces[f]
            for (p, q, r) in ((x, y, z), (y, z, x), (z, x, y)):
                g = self.de[(q, p)]
                third = self.nxt[(q, p)]
                want = 3 - col[p] - col[q]
                if third in col:
                    if col[third] != want:
                        raise ValueError("not 3-colourable")
                else:
                    col[third] = want
                if g not in seen:
                    seen.add(g)
                    dq.append(g)
        return col

    def separating_triangles(self):
        fs = {frozenset(f) for f in self.faces}
        adj = {v: set(self.nbrs(v)) for v in range(self.V)}
        out = []
        for a in range(self.V):
            for b in adj[a]:
                if b > a:
                    for c in adj[a] & adj[b]:
                        if c > b and frozenset((a, b, c)) not in fs:
                            out.append((a, b, c))
        return out


def octahedron():
    return Tri([(0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 5, 2),
                (1, 3, 2), (1, 4, 3), (1, 5, 4), (1, 2, 5)])


def split(T, w, i, j):
    """Operation P at vertex w between its neighbours nb[i] and nb[j] (i < j).
    Needs j - i even >= 2 and deg(w) - (j - i) even >= 2."""
    nb = T.nbrs(w)
    d = len(nb)
    assert 0 <= i < j < d and (j - i) % 2 == 0 and j - i >= 2 and d - (j - i) >= 2
    wp, v = T.V, T.V + 1
    moved = set()
    for k in range(j, i + d):
        moved.add(frozenset((w, nb[k % d], nb[(k + 1) % d])))
    faces = []
    for f in T.faces:
        if frozenset(f) in moved:
            f = tuple(wp if x == w else x for x in f)
        faces.append(f)
    faces += [(w, nb[j], v), (w, v, nb[i]), (wp, nb[i], v), (wp, v, nb[j])]
    return Tri(faces)


def insert_octahedron(T, fi):
    """Operation Q in face fi."""
    p, q, r = T.faces[fi]
    x, y, z = T.V, T.V + 1, T.V + 2
    faces = [f for k, f in enumerate(T.faces) if k != fi]
    faces += [(p, q, z), (q, r, x), (r, p, y), (p, z, y), (q, x, z), (r, y, x), (x, y, z)]
    return Tri(faces)


def _code(T, a, b, step):
    lab = {a: 0, b: 1}
    order = [a, b]
    ref = {a: b, b: a}
    code = []
    i = 0
    while i < len(order):
        w = order[i]
        r = ref[w]
        x = r
        row = []
        while True:
            if x not in lab:
                lab[x] = len(order)
                order.append(x)
                ref[x] = w
            row.append(lab[x])
            x = step[(w, x)]
            if x == r:
                break
        code.append(tuple(row))
        i += 1
    return tuple(code)


def canon(T):
    """Canonical code up to isomorphism of the sphere map, reflections included."""
    best = None
    for step in (T.nxt, T.prv):
        for (a, b) in T.de:
            c = _code(T, a, b, step)
            if best is None or c < best:
                best = c
    return best


def from_code(code):
    faces = set()
    for w, row in enumerate(code):
        d = len(row)
        for k in range(d):
            tri = (w, row[k], row[(k + 1) % d])
            m = tri.index(min(tri))
            faces.add(tri[m:] + tri[:m])
    return Tri(sorted(faces))


def children(T):
    out = []
    for w in range(T.V):
        d = T.degree(w)
        for i in range(d):
            for j in range(i + 2, d, 2):
                if d - (j - i) >= 2:
                    out.append(split(T, w, i, j))
    return out


def children_Q(T):
    return [insert_octahedron(T, f) for f in range(T.F)]


def enumerate_classes(vmax, verbose=False):
    """Dictionary V -> sorted list of canonical codes, for 6 <= V <= vmax."""
    levels = {v: set() for v in range(6, vmax + 4)}
    levels[6].add(canon(octahedron()))
    for v in range(6, vmax + 1):
        for code in sorted(levels[v]):
            T = from_code(code)
            if v + 2 <= vmax:
                for U in children(T):
                    levels[v + 2].add(canon(U))
            if v + 3 <= vmax:
                for U in children_Q(T):
                    levels[v + 3].add(canon(U))
        if verbose:
            print(v, len(levels[v]), flush=True)
    return {v: sorted(levels[v]) for v in range(6, vmax + 1)}
