"""Direction 2. Trinity, triality and triangle factors.

    python trinity.py tutte NMAX      states of (T, t0) against arborescences of the three Tutte digraphs
    python trinity.py factors NMAX    Hamiltonian cycles as acyclic triangle factors; the three projections
    python trinity.py tworoot NMAX    states and tree matchings rooted at two vertices instead of a face
"""
import sys
from collections import Counter, defaultdict
from itertools import combinations
import sympy as sp

from common import corpus, Tri, UF, hamiltonian_partitions


def states(tri, faces, verts):
    """Bijections faces -> verts with s(t) a corner of t."""
    vs = set(verts)
    faces = sorted(faces, key=lambda t: sum(1 for v in tri.faces[t] if v in vs))
    out = []

    def rec(i, used, cur):
        if i == len(faces):
            out.append(dict(cur))
            return
        t = faces[i]
        for v in tri.faces[t]:
            if v in vs and v not in used:
                cur[t] = v
                used.add(v)
                rec(i + 1, used, cur)
                used.discard(v)
                del cur[t]

    if len(faces) == len(vs):
        rec(0, set(), {})
    return out


def q_forest(tri, s):
    uf = UF(tri.V)
    for t, v in s.items():
        a, b = tri.opposite_edge(t, v)
        if not uf.union(a, b):
            return False
    return True


def run_tutte(nmax):
    ok = 0
    for name, g in corpus(6, nmax):
        tri = Tri(g)
        for t0 in tri.black:
            roots = set(tri.faces[t0])
            A = [t for t in tri.black if t != t0]
            X = [v for v in tri.V if v not in roots]
            ss = states(tri, A, X)
            for c in range(3):
                Vc = [v for v in tri.V if tri.col[v] == c]
                root = next(v for v in roots if tri.col[v] == c)
                idx = {v: i for i, v in enumerate(v for v in Vc if v != root)}
                L = sp.zeros(len(idx), len(idx))
                arc = {}
                for t in A:
                    v = next(x for x in tri.faces[t] if tri.col[x] == c)
                    w = tri.third(tri.across(t, v), tri.opposite_edge(t, v))
                    assert tri.col[w] == c
                    arc[t] = (v, w)
                    if v in idx:
                        L[idx[v], idx[v]] += 1
                        if w in idx:
                            L[idx[v], idx[w]] -= 1
                narb = L.det() if len(idx) else 1
                images = set()
                for s in ss:
                    arcs = frozenset(t for t in A if tri.col[s[t]] == c)
                    nxt = {arc[t][0]: arc[t][1] for t in arcs}
                    assert set(nxt) == set(idx)
                    for v in idx:
                        x, steps = v, 0
                        while x != root:
                            x = nxt[x]
                            steps += 1
                            assert steps <= len(Vc)
                    images.add(arcs)
                assert len(images) == len(ss) == narb, (name, t0, c, len(images), len(ss), narb)
                ok += 1
    print('rooted triangulations x colours checked:', ok)
    print('in each: state -> colour-c arc set is injective, its image is acyclic, and #states = det of the reduced Laplacian')


def triangle_factor(tri, lab, v1, v2):
    """Oriented mono edges: black face -> tail, white face -> tail, black -> white."""
    par = {}
    adj = defaultdict(list)
    P = [e for e in tri.g.edges() if lab[e[0]] == lab[e[1]]]
    for a, b in P:
        adj[a].append(b)
        adj[b].append(a)
    for r in (v1, v2):
        stack = [r]
        par[r] = None
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in par:
                    par[y] = x
                    stack.append(y)
    assert len(par) == len(tri.V)
    mbv, mwv, mbw = {}, {}, {}
    for v, p in par.items():
        if p is None:
            continue
        e = frozenset((v, p))
        b, w = tri.eface[e, 0], tri.eface[e, 1]
        mbv[b], mwv[w], mbw[b] = v, v, w
    return mbv, mwv, mbw


def run_factors(nmax):
    tot = Counter()
    for name, g in corpus(6, nmax):
        tri = Tri(g)
        loc = Counter()
        for lab in hamiltonian_partitions(tri):
            c0 = [v for v in tri.V if lab[v] == 0]
            c1 = [v for v in tri.V if lab[v] == 1]
            for v1 in c0:
                for v2 in c1:
                    mbv, mwv, mbw = triangle_factor(tri, lab, v1, v2)
                    assert len(mbv) == len(mwv) == tri.k
                    fb, fw = q_forest(tri, mbv), q_forest(tri, mwv)
                    loc['factors'] += 1
                    loc['black projection is a tree matching'] += fb
                    loc['white projection is a tree matching'] += fw
                    loc['both'] += fb and fw
                    loc['neither'] += (not fb) and (not fw)
        tot.update(loc)
        print(name, dict(loc), flush=True)
    print('TOTAL', dict(tot))


def run_tworoot(nmax):
    """Two-root states: bijections from ALL black faces to V minus {v1, v2}."""
    for name, g in corpus(6, nmax):
        tri = Tri(g)
        nsep = len(tri.separating_triangles())
        hams = hamiltonian_partitions(tri)
        ham_edges = {frozenset(frozenset(e) for e in tri.g.edges() if lab[e[0]] == lab[e[1]]) for lab in hams}
        reached = set()
        loc = Counter()
        pairs_with_tree = 0
        for v1, v2 in combinations(tri.V, 2):
            ss = states(tri, tri.black, [v for v in tri.V if v not in (v1, v2)])
            trees = [s for s in ss if q_forest(tri, s)]
            loc['states'] += len(ss)
            loc['tree'] += len(trees)
            pairs_with_tree += bool(trees)
            for s in trees:
                ends = {}
                for t, v in s.items():
                    ws = []
                    for u in tri.faces[t]:
                        if u != v:
                            ws.append((tri.eface[frozenset((u, v)), 1], frozenset((u, v))))
                    ends[t] = ws
                sols = []
                order = list(ends)

                def rec(i, used, cur):
                    if len(sols) > 2:
                        return
                    if i == len(order):
                        sols.append(list(cur))
                        return
                    for w, e in ends[order[i]]:
                        if w not in used:
                            used.add(w)
                            cur.append(e)
                            rec(i + 1, used, cur)
                            cur.pop()
                            used.discard(w)

                rec(0, set(), [])
                loc['orientations=%d' % len(sols)] += 1
                good = 0
                for P in sols:
                    if frozenset(P) in ham_edges:
                        good += 1
                        reached.add(frozenset(P))
                loc['hamiltonian orientations=%d' % good] += 1
        print(name, 'V=%d sep3=%d' % (len(g), nsep), 'root pairs with a two-root tree matching: %d of %d;'
              % (pairs_with_tree, len(tri.V) * (len(tri.V) - 1) // 2), dict(sorted(loc.items())),
              'Hamiltonian cycles reached %d of %d' % (len(reached), len(ham_edges)), flush=True)


if __name__ == '__main__':
    {'tutte': run_tutte, 'factors': run_factors, 'tworoot': run_tworoot}[sys.argv[1]](int(sys.argv[2]))
