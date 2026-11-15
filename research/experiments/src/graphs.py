"""Eulerian triangulations: input, constructions and families.

A triangulation is a numpy int32 array of shape (nf, 3), the faces listed
counterclockwise, on the vertices 0..V-1.  Its dual is the cubic graph G whose
vertices are the faces; N = nf = 2V - 4.
"""
import json
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]


# ---------------------------------------------------------------- input

def read_planar_code(path):
    """The plane graphs of a planar-code file, each as a list of neighbour
    lists in clockwise order (vertices numbered from 0)."""
    data = Path(path).read_bytes()
    head = b'>>planar_code<<'
    pos = len(head) if data.startswith(head) else 0
    while pos < len(data):
        n = data[pos]
        pos += 1
        if n == 0:
            raise ValueError('graphs with more than 255 vertices are not supported')
        rot = []
        for _ in range(n):
            end = data.index(0, pos)
            rot.append([b - 1 for b in data[pos:end]])
            pos = end + 1
        yield rot


def faces_of_rotation(rot):
    """The faces of a plane triangulation given by neighbour lists in clockwise
    order, in the order in which a scan of the lists meets them."""
    nxt = {}
    for v, nbrs in enumerate(rot):
        for i, w in enumerate(nbrs):
            nxt[w, v] = nbrs[(i + 1) % len(nbrs)]      # after w -> v comes v -> this
    seen, faces = set(), []
    for v, nbrs in enumerate(rot):
        for w in nbrs:
            if (v, w) not in seen:
                x = nxt[v, w]
                if nxt[w, x] != v:
                    raise ValueError('not a triangulation')
                seen.update(((v, w), (w, x), (x, v)))
                faces.append((v, w, x))
    return np.array(faces, dtype=np.int32)


def rotation_of_faces(F):
    """Neighbour lists in counterclockwise order."""
    succ = {}
    for a, b, c in np.asarray(F).tolist():
        succ[a, b] = c
        succ[b, c] = a
        succ[c, a] = b
    rot = {}
    for (v, w) in succ:
        if v not in rot:
            ring, x = [w], succ[v, w]
            while x != w:
                ring.append(x)
                x = succ[v, x]
            rot[v] = ring
    return [rot[v] for v in range(len(rot))]


def mirror(F):
    return np.ascontiguousarray(np.asarray(F)[:, ::-1])


def degrees(F):
    return np.bincount(np.asarray(F).ravel()) // 1


def relabel(F):
    """Renumber the vertices 0..V-1 in order of first appearance."""
    F = np.asarray(F)
    _, first = np.unique(F.ravel(), return_index=True)
    order = F.ravel()[np.sort(first)]
    new = np.zeros(F.max() + 1, dtype=np.int32)
    new[order] = np.arange(len(order), dtype=np.int32)
    return new[F].astype(np.int32)


def is_eulerian_triangulation(F):
    F = np.asarray(F)
    darts = set()
    for a, b, c in F.tolist():
        for d in ((a, b), (b, c), (c, a)):
            if d in darts or d[0] == d[1]:
                return False
            darts.add(d)
    if any((w, v) not in darts for v, w in darts):
        return False
    V = len(set(F.ravel().tolist()))
    if V - len(darts) // 2 + len(F) != 2:
        return False
    return bool(np.all(np.bincount(F.ravel()) % 2 == 0))


def to_reference(F, t0, k=0):
    """The same labelled triangulation as an object of workings/barnette,
    with e0 the side k of t0."""
    import sys
    sys.path.insert(0, str(REPO / 'workings'))
    from barnette import Triangulation
    faces = {i: tuple(f) for i, f in enumerate(np.asarray(F).tolist())}
    f = faces[t0]
    return Triangulation(faces, t0, (f[k], f[(k + 1) % 3]))


def dual_of_cubic_graph(G):
    """The dual triangulation of a cubic 3-connected planar networkx graph;
    its faces are numbered in the order of the nodes of G."""
    import networkx as nx
    ok, emb = nx.check_planarity(G)
    if not ok:
        raise ValueError('not planar')
    left, k = {}, 0
    seen = set()
    for v, w in emb.edges():
        if (v, w) not in seen:
            f = emb.traverse_face(v, w, seen)
            for d in zip(f, f[1:] + f[:1]):
                left[d] = k
            k += 1
    return np.array([[left[x, y] for y in emb.neighbors_cw_order(x)] for x in G], dtype=np.int32)


def triangulation_of_graph(T):
    """Faces of a 3-connected planar triangulation given as a networkx graph."""
    import networkx as nx
    ok, emb = nx.check_planarity(T)
    seen, faces = set(), []
    for v, w in emb.edges():
        if (v, w) not in seen:
            faces.append(emb.traverse_face(v, w, seen))
    return relabel(np.array(faces, dtype=np.int32))


# -------------------------------------------------------- local moves

def split_vertex(F, a, b, d):
    """The split of the vertex a along its edges to b and d: a keeps the
    neighbours met counterclockwise from b to d, a new vertex c takes the
    others, and a new vertex of degree four is joined to a, b, c, d.  Both
    groups must have an odd number of vertices strictly between b and d."""
    F = np.asarray(F)
    ring = rotation_of_faces(F)[a]
    i, j = ring.index(b), ring.index(d)
    group2 = set()
    k = j
    while ring[k] != b:
        group2.add(ring[k])
        k = (k + 1) % len(ring)
    p, q = (j - i) % len(ring) - 1, len(group2) - 1
    if p % 2 == 0 or q % 2 == 0 or p < 1 or q < 1:
        raise ValueError('the split does not keep the degrees even')
    c, v = int(F.max()) + 1, int(F.max()) + 2
    out = []
    for f in F.tolist():
        if a in f:
            x, y = [u for u in (f * 2)[f.index(a) + 1:f.index(a) + 3]]
            if x in group2 and (y in group2 or y == b):
                f = [c if u == a else u for u in f]
        out.append(f)
    out += [[v, b, a], [v, a, d], [v, d, c], [v, c, b]]
    return np.array(out, dtype=np.int32)


def insert_octahedron(F, f):
    """Three new vertices of degree four inside the face f."""
    F = np.asarray(F)
    x, y, z = F[f].tolist()
    p, q, r = int(F.max()) + 1, int(F.max()) + 2, int(F.max()) + 3
    new = [[x, y, r], [y, z, p], [z, x, q], [y, p, r], [z, q, p], [x, r, q], [p, q, r]]
    return np.array([g for i, g in enumerate(F.tolist()) if i != f] + new, dtype=np.int32)


def all_splits(F):
    """All triangulations obtained from F by one vertex split."""
    for a, ring in enumerate(rotation_of_faces(F)):
        d = len(ring)
        for i in range(d):
            for gap in range(2, d - 1, 2):
                j = (i + gap) % d
                if i < j:
                    yield split_vertex(F, a, ring[i], ring[j])


# ------------------------------------------------- global constructions

def subdivide(F, k):
    """Every face cut into k^2 triangles; the new vertices have degree six."""
    return goldberg_coxeter(F, k, 0)


def leapfrog(F):
    """The Goldberg-Coxeter construction with parameters (1, 1)."""
    return goldberg_coxeter(F, 1, 1)


def _mul_omega(z):
    return (-z[1], z[0] + z[1])


def _cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def goldberg_coxeter(F, k, l):
    """The Goldberg-Coxeter construction GC_{k,l}: every face is replaced by
    the part of the triangular lattice inside the triangle with corners
    0, k + l w, (k + l w) w, where w is a primitive sixth root of unity.  The
    result has (k^2 + kl + l^2)(V - 2) + 2 vertices; the old vertices keep
    their degrees and the new ones have degree six."""
    from math import gcd
    F = np.asarray(F).tolist()
    if (k, l) == (1, 0):
        return np.array(F, dtype=np.int32)
    g = gcd(k, l)
    z0 = (k, l)
    corners = [(0, 0), z0, _mul_omega(z0)]
    units = [(1, 0)]
    for _ in range(5):
        units.append(_mul_omega(units[-1]))
    left = {}
    for fi, f in enumerate(F):
        for j in range(3):
            left[f[j], f[(j + 1) % 3]] = (fi, j)
    ids, V = {}, max(max(f) for f in F) + 1

    def ident(key):
        nonlocal V
        if key not in ids:
            ids[key] = V
            V += 1
        return ids[key]

    def classify(fi, p):
        """The global vertex at the lattice point p of the chart of the face
        fi, or None if p is outside the closed triangle."""
        f = F[fi]
        cr = [_cross((corners[(j + 1) % 3][0] - corners[j][0], corners[(j + 1) % 3][1] - corners[j][1]),
                     (p[0] - corners[j][0], p[1] - corners[j][1])) for j in range(3)]
        if min(cr) < 0:
            return None
        zero = [j for j in range(3) if cr[j] == 0]
        if len(zero) == 2:                      # a corner
            j = next(j for j in range(3) if corners[j] == p)
            return f[j]
        if len(zero) == 1:                      # on the side j -> j+1
            j = zero[0]
            u, w = f[j], f[(j + 1) % 3]
            step = ((corners[(j + 1) % 3][0] - corners[j][0]) // g,
                    (corners[(j + 1) % 3][1] - corners[j][1]) // g)
            d = (p[0] - corners[j][0], p[1] - corners[j][1])
            i = d[0] // step[0] if step[0] else d[1] // step[1]
            return ident(('e', u, w, i) if u < w else ('e', w, u, g - i))
        return ident(('f', fi, p))

    def unit_mul(u, z):
        for _ in range(units.index(u)):
            z = _mul_omega(z)
        return z

    lo = min(c[0] for c in corners) - abs(k) - abs(l) - 1, min(c[1] for c in corners) - abs(k) - abs(l) - 1
    hi = max(c[0] for c in corners) + abs(k) + abs(l) + 1, max(c[1] for c in corners) + abs(k) + abs(l) + 1
    out = {}
    for fi, f in enumerate(F):
        # charts of the three neighbours, as maps from this chart
        maps = []
        for j in range(3):
            gi, gj = left[f[(j + 1) % 3], f[j]]       # in g the side runs w -> u
            pu, pw = corners[j], corners[(j + 1) % 3]
            qw, qu = corners[gj], corners[(gj + 1) % 3]
            dp, dq = (pw[0] - pu[0], pw[1] - pu[1]), (qw[0] - qu[0], qw[1] - qu[1])
            u = next(u for u in units if unit_mul(u, dp) == dq)
            maps.append((gi, u, pu, qu))
        point = {}
        for a in range(lo[0], hi[0] + 1):
            for b in range(lo[1], hi[1] + 1):
                p = (a, b)
                v = classify(fi, p)
                inside = v is not None
                if v is None:
                    for gi, u, pu, qu in maps:
                        d = unit_mul(u, (p[0] - pu[0], p[1] - pu[1]))
                        v = classify(gi, (qu[0] + d[0], qu[1] + d[1]))
                        if v is not None:
                            break
                if v is not None:
                    point[p] = (v, inside)
        for (a, b), (v, inside) in point.items():
            for tri in (((a, b), (a + 1, b), (a, b + 1)), ((a + 1, b), (a + 1, b + 1), (a, b + 1))):
                if all(t in point for t in tri) and any(point[t][1] for t in tri):
                    vs = [point[t][0] for t in tri]
                    i = vs.index(min(vs))
                    out[tuple(vs[i:] + vs[:i])] = True
    return relabel(np.array(list(out), dtype=np.int32))


def barycentric(rot):
    """The barycentric subdivision of a plane map given by neighbour lists in
    a consistent cyclic order: its vertices are the vertices, edges and faces
    of the map."""
    nv = len(rot)
    nxt = {}
    for v, nbrs in enumerate(rot):
        for i, w in enumerate(nbrs):
            nxt[w, v] = nbrs[(i + 1) % len(nbrs)]
    eid, k = {}, nv
    for v, nbrs in enumerate(rot):
        for w in nbrs:
            if v < w:
                eid[v, w] = eid[w, v] = k
                k += 1
    seen, faces = set(), []
    for v, nbrs in enumerate(rot):
        for w in nbrs:
            if (v, w) not in seen:
                x, y = v, w
                while (x, y) not in seen:
                    seen.add((x, y))
                    faces.append((x, eid[x, y], k))
                    faces.append((eid[x, y], y, k))
                    x, y = y, nxt[x, y]
                k += 1
    return np.array(faces, dtype=np.int32)


# ------------------------------------------------------------ families

def octahedron():
    return np.array([[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 1],
                     [5, 2, 1], [5, 3, 2], [5, 4, 3], [5, 1, 4]], dtype=np.int32)


def bipyramid(k):
    """The dual of the prism over a 2k-gon, k >= 2: V = 2k + 2, N = 4k."""
    return tube(k, 1)


def tube(k, m):
    """Two vertices of degree 2k joined by m rings of 2k vertices; between
    consecutive rings the vertices with even index have three neighbours in
    the next ring and those with odd index one.  The dual has two 2k-gons,
    2k quadrilaterals and 2k(m-1) hexagons; N = 4km.  tube(k, 1) is the dual
    of the prism, tube(2, m) and tube(3, m) have only 4- and 6-faces."""
    c = 2 * k
    ring = lambda j, i: 2 + j * c + i % c
    faces = []
    for i in range(c):
        faces.append((0, ring(0, i + 1), ring(0, i)))
        faces.append((1, ring(m - 1, i), ring(m - 1, i + 1)))
    for j in range(m - 1):
        for i in range(c):
            a, b, a2, b2 = ring(j, i), ring(j, i + 1), ring(j + 1, i), ring(j + 1, i + 1)
            if i % 2 == 0:
                faces += [(a, b, b2), (a, b2, a2)]
            else:
                faces += [(a, b, a2), (b, b2, a2)]
    return np.array(faces, dtype=np.int32)


def nanotube(m):
    """The dual of examples.nanotube(m): N = 6m + 2."""
    import sys
    sys.path.insert(0, str(REPO / 'workings'))
    from barnette import examples
    return dual_of_cubic_graph(examples.nanotube(m))


def octahedral(k, l):
    """GC_{k,l} of the octahedron: six vertices of degree four, the others of
    degree six; N = 8(k^2 + kl + l^2); the dual has six 4-faces and
    hexagons otherwise.  (1,0) is the cube, (1,1) the truncated octahedron."""
    return goldberg_coxeter(octahedron(), k, l)


PLATONIC = {
    'tetrahedron': [[1, 2, 3], [0, 3, 2], [0, 1, 3], [0, 2, 1]],
    'cube': [[1, 3, 4], [2, 0, 5], [3, 1, 6], [0, 2, 7], [7, 5, 0], [4, 6, 1], [5, 7, 2], [6, 4, 3]],
}


def omnitruncated(name):
    """The barycentric subdivision of a Platonic solid; its dual is the
    truncated octahedron (tetrahedron), the great rhombicuboctahedron (cube)
    or the great rhombicosidodecahedron (dodecahedron)."""
    import networkx as nx
    G = {'tetrahedron': nx.tetrahedral_graph, 'cube': nx.cubical_graph,
         'dodecahedron': nx.dodecahedral_graph}[name]()
    return barycentric(rotation_of_graph(G))


def rotation_of_graph(G):
    """Neighbour lists (clockwise) of a planar networkx graph on 0..n-1."""
    import networkx as nx
    ok, emb = nx.check_planarity(G)
    if not ok:
        raise ValueError('not planar')
    return [list(emb.neighbors_cw_order(v)) for v in range(len(G))]


def stacked_octahedra(depth, mode='chain'):
    """Octahedra inserted repeatedly.  'chain': each new octahedron goes into
    the central face of the previous one (nested separating triangles);
    'all': at every level an octahedron goes into every face of the
    octahedra added at the previous level."""
    F = octahedron()
    if mode == 'chain':
        for _ in range(depth):
            F = insert_octahedron(F, len(F) - 1)
        return F
    new = list(range(len(F)))
    for _ in range(depth):
        nxt = []
        for f in sorted(new, reverse=True):
            F = insert_octahedron(F, f)
            # the removed face shifts the later ones down by one
            nxt = [g - 1 for g in nxt] + list(range(len(F) - 7, len(F)))
        new = nxt
    return F


def split_bipyramid(k):
    """The bipyramid over a 2k-gon in which one apex is split in halves
    repeatedly until every part has degree at most eight: one vertex of
    degree 2k remains, so the dual has a single very large face."""
    F = bipyramid(k)
    todo = [1]
    while todo:
        a = todo.pop()
        ring = rotation_of_faces(F)[a]
        d = len(ring)
        if d <= 8:
            continue
        gap = d // 2 if (d // 2) % 2 == 0 else d // 2 + 1
        F = split_vertex(F, a, ring[0], ring[gap])
        todo += [a, int(F.max()) - 1]
    return F


def trap_chain(k):
    """The triangulation stored in research/instances/trap-chain-k.json, with
    its faces in the stored order, and the index of t0."""
    d = json.loads((REPO / 'research' / 'instances' / f'trap-chain-{k}.json').read_text())
    return np.array(d['faces'], dtype=np.int32), d['faces'].index(d['t0']), d


def face_vector(F):
    """The numbers of faces of each size of the dual G: {size: count}; a
    vertex of degree d of T is a face of size d of G."""
    deg = np.bincount(np.asarray(F).ravel())
    sizes, counts = np.unique(deg, return_counts=True)
    return {int(s): int(c) for s, c in zip(sizes, counts)}
