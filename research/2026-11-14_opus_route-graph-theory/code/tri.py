"""Eulerian sphere triangulations: embedding, face colouring, canonical codes, generation.

A triangulation is stored as a rotation system rot[v] = list of neighbours in
counterclockwise order.  The face to the left of the dart u->v is (u, v, w) with
w = rot[v][idx_v(u) - 1]; faces are listed counterclockwise.

Generation (exhaustive, up to isomorphism including reflection):
  E(6) = {octahedron};
  E(V) = splits of E(V-2)  (insert a degree-4 vertex by splitting a vertex)
         U glues of E(V1), E(V2) along a face, V1 + V2 - 3 = V.
Completeness: a triangulation without separating triangle and V > 6 has a
degree-4 vertex whose contraction (merging one opposite pair) is simple
(PROOFS.md, Lemma G1); one with a separating triangle is a glue of two smaller ones.
"""
import itertools
import networkx as nx


class Tri:
    def __init__(self, rot):
        self.rot = {v: list(ns) for v, ns in rot.items()}
        self.V = sorted(self.rot)
        self.pos = {v: {u: i for i, u in enumerate(ns)} for v, ns in self.rot.items()}
        self._faces = None

    @staticmethod
    def from_edges(edges):
        G = nx.Graph()
        G.add_edges_from(edges)
        ok, emb = nx.check_planarity(G)
        assert ok
        rot = {v: list(reversed(list(emb.neighbors_cw_order(v)))) for v in G.nodes}
        return Tri(rot)

    def edges(self):
        return [(u, v) for u in self.rot for v in self.rot[u] if u < v]

    def nxt(self, u, v):
        """dart following u->v around the face on its left"""
        w = self.rot[v][self.pos[v][u] - 1]
        return v, w

    def faces(self):
        if self._faces is None:
            seen = set()
            fs = []
            for u in self.rot:
                for v in self.rot[u]:
                    if (u, v) in seen:
                        continue
                    f = []
                    d = (u, v)
                    while d not in seen:
                        seen.add(d)
                        f.append(d[0])
                        d = self.nxt(*d)
                    assert len(f) == 3, f
                    fs.append(tuple(f))
            self._faces = fs
        return self._faces

    def check(self):
        V = len(self.rot)
        E = sum(len(x) for x in self.rot.values()) // 2
        F = len(self.faces())
        assert V - E + F == 2, (V, E, F)
        for u in self.rot:
            assert len(set(self.rot[u])) == len(self.rot[u])
            for v in self.rot[u]:
                assert u in self.pos[v]
        return True

    def is_eulerian(self):
        return all(len(ns) % 2 == 0 for ns in self.rot.values())

    def face_colouring(self, black_face=None):
        """dict face(tuple, canonical rotation) -> 0 black / 1 white; black_face gets 0"""
        fs = [canon_face(f) for f in self.faces()]
        dart_face = {}
        for f in fs:
            for i in range(3):
                dart_face[(f[i], f[(i + 1) % 3])] = f
        start = canon_face(black_face) if black_face is not None else fs[0]
        col = {start: 0}
        stack = [start]
        while stack:
            f = stack.pop()
            for i in range(3):
                g = dart_face[(f[(i + 1) % 3], f[i])]
                if g in col:
                    assert col[g] != col[f], "not Eulerian"
                else:
                    col[g] = 1 - col[f]
                    stack.append(g)
        return col

    def canon_code(self):
        best = None
        for u in self.rot:
            for v in self.rot[u]:
                for o in (1, -1):
                    c = self._code_from(u, v, o)
                    if best is None or c < best:
                        best = c
        return best

    def _code_from(self, u, v, o):
        lab = {u: 0}
        order = [u]
        first = {u: v}
        code = []
        i = 0
        while i < len(order):
            w = order[i]
            ns = self.rot[w]
            d = len(ns)
            k = self.pos[w][first[w]]
            for j in range(d):
                x = ns[(k + o * j) % d]
                if x not in lab:
                    lab[x] = len(order)
                    order.append(x)
                    first[x] = w
                code.append(lab[x])
            code.append(-1)
            i += 1
        return tuple(code)

    def relabel(self):
        m = {v: i for i, v in enumerate(sorted(self.rot))}
        return Tri({m[v]: [m[u] for u in ns] for v, ns in self.rot.items()})

    def separating_triangles(self):
        """list of 3-cycles (sorted tuples) that are not faces"""
        fset = {frozenset(f) for f in self.faces()}
        adj = {v: set(ns) for v, ns in self.rot.items()}
        out = []
        for a in self.rot:
            for b in adj[a]:
                if b <= a:
                    continue
                for c in adj[a] & adj[b]:
                    if c <= b:
                        continue
                    if frozenset((a, b, c)) not in fset:
                        out.append((a, b, c))
        return out


def canon_face(f):
    i = f.index(min(f))
    return tuple(f[i:] + f[:i]) if isinstance(f, list) else tuple(list(f[i:]) + list(f[:i]))


def octahedron():
    edges = [(0, i) for i in range(1, 5)] + [(5, i) for i in range(1, 5)] + \
            [(1, 2), (2, 3), (3, 4), (4, 1)]
    return Tri.from_edges(edges)


def splits(T):
    """all degree-4 insertions (vertex splits with odd arcs)"""
    out = []
    nv = max(T.rot) + 1
    for v in T.rot:
        ns = T.rot[v]
        d = len(ns)
        for i in range(d):
            for j in range(i + 2, d, 2):
                # arcs between i and j exclusive: j-i-1 odd  <=> j-i even
                if (d - (j - i) - 1) % 2 == 0:
                    continue
                a, b = ns[i], ns[j]
                P = ns[i + 1:j]
                Q = ns[j + 1:] + ns[:i]
                v1, v2, x = v, nv, nv + 1
                rot = {w: list(l) for w, l in T.rot.items()}
                rot[v1] = [a] + P + [b, x]
                rot[v2] = [b] + Q + [a, x]
                rot[x] = [a, v1, b, v2]
                ra = rot[a]; k = ra.index(v); rot[a] = ra[:k] + [v1, x, v2] + ra[k + 1:]
                rb = rot[b]; k = rb.index(v); rot[b] = rb[:k] + [v2, x, v1] + rb[k + 1:]
                for q in Q:
                    rq = rot[q]; k = rq.index(v); rq[k] = v2
                out.append(Tri(rot))
    return out


def glues(T1, T2):
    out = []
    n1 = max(T1.rot) + 1
    f1s = T1.faces()
    E1 = T1.edges()
    for f2 in T2.faces():
        for f1 in f1s:
            for perm in itertools.permutations(f1):
                m = {}
                nxtl = n1
                for w in sorted(T2.rot):
                    if w in f2:
                        m[w] = perm[f2.index(w)]
                    else:
                        m[w] = nxtl
                        nxtl += 1
                E = set(tuple(sorted(e)) for e in E1)
                for (p, q) in T2.edges():
                    E.add(tuple(sorted((m[p], m[q]))))
                out.append(Tri.from_edges(list(E)))
    return out


def generate(Vmax, verbose=False):
    """dict V -> list of Tri (one per isomorphism class), 6 <= V <= Vmax"""
    E = {6: [octahedron().relabel()]}
    for V in range(7, Vmax + 1):
        seen = {}
        cands = []
        if V - 2 in E:
            for T in E[V - 2]:
                cands.extend(splits(T))
        for V1 in range(6, V - 2):
            V2 = V + 3 - V1
            if V2 < V1 or V1 not in E or V2 not in E:
                continue
            for T1 in E[V1]:
                for T2 in E[V2]:
                    cands.extend(glues(T1, T2))
        for T in cands:
            c = T.canon_code()
            if c not in seen:
                T = T.relabel()
                T.check()
                assert T.is_eulerian()
                seen[c] = T
        E[V] = list(seen.values())
        if verbose:
            print(V, len(E[V]), flush=True)
    return E


if __name__ == "__main__":
    import sys
    Vmax = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    generate(Vmax, verbose=True)


def load(V):
    import json, os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", f"eul_{V}.json")
    with open(p) as f:
        return [Tri({int(k): v for k, v in d.items()}) for d in json.load(f)]
