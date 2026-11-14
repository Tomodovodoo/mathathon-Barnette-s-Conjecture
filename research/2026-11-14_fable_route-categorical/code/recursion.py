"""Direction 4. Multiplicativity and candidate recursions for the number of tree matchings.

    python recursion.py mult NMAX      insertion of a rooted triangulation into a face
    python recursion.py contract NMAX  contraction of a degree-4 vertex

tau(T, t0) is the number of face-rooted tree matchings (states s with H - s a tree).
"""
import sys
from collections import Counter
import networkx as nx

from common import corpus, Tri, UF
from trinity import states


def counts(tri, t0):
    roots = set(tri.faces[t0])
    A = [t for t in tri.black_of(t0) if t != t0]
    X = [v for v in tri.V if v not in roots]
    ss = states(tri, A, X)
    rep = {v: ('R' if v in roots else v) for v in tri.V}
    trees = 0
    for s in ss:
        uf = UF(set(rep.values()))
        ok = True
        for t, v in s.items():
            a, b = tri.opposite_edge(t, v)
            if not uf.union(rep[a], rep[b]):
                ok = False
                break
        trees += ok
    pairs = sum(1 for r in ss for s in ss if all(r[t] != s[t] for t in A))
    return len(ss), pairs, trees


def black_of(self, t0):
    return [f for f in range(self.nf) if self.fcol[f] == self.fcol[t0]]


Tri.black_of = black_of


def face_index(tri, vs):
    vs = frozenset(vs)
    return next(i for i, f in enumerate(tri.faces) if frozenset(f) == vs)


def glue(t1, f1, t2, f2):
    mapping = dict(zip(t2.faces[f2], t1.faces[f1]))
    nxt = max(t1.V) + 1
    for v in t2.V:
        if v not in mapping:
            mapping[v] = nxt
            nxt += 1
    return nx.compose(t1.g, nx.relabel_nodes(t2.g, mapping))


def run_mult(nmax):
    pieces = [(name, Tri(g)) for name, g in corpus(6, nmax)]
    tot = Counter()
    for n1, t1 in pieces:
        for n2, t2 in pieces:
            if len(t1.V) + len(t2.V) - 3 > 14:
                continue
            for t0 in range(t1.nf):
                c1 = counts(t1, t0)
                for f1 in range(t1.nf):
                    if f1 == t0:
                        continue
                    same = t1.fcol[f1] == t1.fcol[t0]
                    for f2 in (0, 1):
                        c2 = counts(t2, f2)
                        g = glue(t1, f1, t2, f2)
                        big = Tri(g)
                        cb = counts(big, face_index(big, t1.faces[t0]))
                        if same:
                            # insertion into a face of the colour of t0: no pair, hence no tree matching
                            assert cb[1] == 0 and cb[2] == 0, (n1, n2, t0, f1, f2, cb)
                            tot['insertions into a black face: pairs = trees = 0'] += 1
                        else:
                            assert cb == tuple(x * y for x, y in zip(c1, c2)), (n1, n2, t0, f1, f2, c1, c2, cb)
                            tot['insertions into a white face: states, pairs, trees all multiply'] += 1
    print(dict(tot))


def run_contract(nmax):
    rows = []
    stat = Counter()
    for name, g in corpus(8, nmax):
        tri = Tri(g)
        for t0 in range(tri.nf):
            roots = set(tri.faces[t0])
            tau = counts(tri, t0)[2]
            for v in tri.V:
                if g.degree(v) != 4 or v in roots:
                    continue
                nb = list(tri.emb.neighbors_cw_order(v))
                res = []
                for a, c in ((nb[0], nb[2]), (nb[1], nb[3])):
                    if g.has_edge(a, c) or set(g[a]) & set(g[c]) != set(nb) - {a, c} | {v}:
                        res.append(None)
                        continue
                    h = g.copy()
                    h.remove_node(v)
                    h = nx.contracted_nodes(h, a, c, self_loops=False)
                    try:
                        small = Tri(h)
                    except Exception:
                        res.append(None)
                        continue
                    r0 = [a if x == c else x for x in tri.faces[t0]]
                    res.append(counts(small, face_index(small, r0))[2])
                rows.append((name, t0, v, tau, res[0], res[1]))
                if res[0] is not None and res[1] is not None:
                    stat['both contractions simple'] += 1
                    stat['tau = tau_ac + tau_bd'] += (tau == res[0] + res[1])
                    stat['tau >= tau_ac + tau_bd'] += (tau >= res[0] + res[1])
                    stat['tau >= max'] += (tau >= max(res))
                for r in res:
                    if r is not None:
                        stat['single contractions'] += 1
                        stat['tau >= tau_contracted'] += (tau >= r)
                        stat['tau > 0 and tau_contracted = 0'] += (tau > 0 and r == 0)
                        stat['tau = 0 and tau_contracted > 0'] += (tau == 0 and r > 0)
    print(dict(stat))
    bad = [r for r in rows if r[4] is not None and r[3] < r[4] or r[5] is not None and r[3] < r[5]]
    print('first rows with tau < tau of a contraction:', bad[:5])
    bad = [r for r in rows if r[3] == 0 and ((r[4] or 0) > 0 or (r[5] or 0) > 0)]
    print('first rows with tau = 0 but a contraction has tree matchings:', bad[:5])


if __name__ == '__main__':
    {'mult': run_mult, 'contract': run_contract}[sys.argv[1]](int(sys.argv[2]))
