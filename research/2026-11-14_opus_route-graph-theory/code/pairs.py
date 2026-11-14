"""Pairs without enumeration: flow pair, the Q-map f, D-cycles, exchanges, descent.

For a pair (r, s): u(t) = third corner.  The Q-map is f(x) = u(r^{-1}(x)) on X
(the edge r(t)->u(t) of Q_s, oriented by the mate r).  Q_s is a rooted forest
iff f has no cycle; k = number of f-cycles.  D-cycles: x -> s(r^{-1}(x)).
"""
import random
import networkx as nx
from tri import Tri, splits, octahedron
from states import Rooted


def flow_pair(R):
    G = nx.DiGraph()
    for x in R.X:
        G.add_edge("S", ("x", x), capacity=2)
    for t in R.A:
        G.add_edge(("t", t), "K", capacity=2)
        for v in R.corners[t]:
            G.add_edge(("x", v), ("t", t), capacity=1)
    val, fl = nx.maximum_flow(G, "S", "K")
    if val != 2 * R.n:
        return None
    # 2-factor of B -> two perfect matchings by alternating along its cycles
    nbt = {t: [] for t in R.A}
    nbx = {x: [] for x in R.X}
    for x in R.X:
        for (tag, t), c in fl[("x", x)].items():
            if c:
                nbt[t].append(x)
                nbx[x].append(t)
    r, s = {}, {}
    for t0 in R.A:
        if t0 in r:
            continue
        t = t0
        x = nbt[t][0]
        while t not in r:
            r[t] = x
            t2 = [u for u in nbx[x] if u != t][0]
            s[t2] = x
            x = [y for y in nbt[t2] if y != x][0]
            t = t2
    return r, s


def third(t, a, b):
    return [w for w in t if w != a and w != b][0]


def fmap(R, r, s):
    f = {}
    for t in R.A:
        f[r[t]] = third(t, r[t], s[t])
    return f


def fcycles(R, f):
    Xs = set(R.X)
    state = {}
    cycles = []
    for x0 in R.X:
        if x0 in state:
            continue
        path = []
        y = x0
        while y in Xs and y not in state:
            state[y] = 1
            path.append(y)
            y = f[y]
        if y in Xs and state.get(y) == 1 and y in path:
            cycles.append(path[path.index(y):])
        for p in path:
            state[p] = 2
    return cycles


def dcycles(R, r, s):
    inv = {r[t]: t for t in R.A}
    seen = set()
    out = []
    for x0 in R.X:
        if x0 in seen:
            continue
        c = []
        y = x0
        while y not in seen:
            seen.add(y)
            c.append(y)
            y = s[inv[y]]
        out.append(c)
    return out


def d_swap(R, r, s, cyc):
    cs = set(cyc)
    r2, s2 = dict(r), dict(s)
    for t in R.A:
        if r[t] in cs:
            r2[t], s2[t] = s[t], r[t]
    return r2, s2


def q_reverse(R, r, s, qcyc):
    cs = set(qcyc)
    r2 = dict(r)
    for t in R.A:
        if r[t] in cs:
            r2[t] = third(t, r[t], s[t])
    return r2, s


def is_pair(R, r, s):
    return (all(r[t] != s[t] for t in R.A) and len(set(r.values())) == R.n
            and len(set(s.values())) == R.n
            and all(r[t] in t and s[t] in t for t in R.A))


def random_eulerian(V, rng):
    T = octahedron().relabel()
    while len(T.rot) < V:
        cands = splits(T)
        T = rng.choice(cands)
    return T.relabel()


def random_eulerian_fast(V, rng):
    """random split sequence without listing all splits"""
    from tri import Tri
    T = octahedron().relabel()
    while len(T.rot) < V:
        v = rng.choice(list(T.rot))
        ns = T.rot[v]
        d = len(ns)
        i = rng.randrange(d)
        j = (i + 2 * rng.randrange(1, d // 2)) % d
        # build via splits() restricted: emulate by filtering
        sp = [S for S in _splits_at(T, v, i, j)]
        T = sp[0]
    return T.relabel()


def _splits_at(T, v, i, j):
    ns = T.rot[v]
    d = len(ns)
    k = (j - i) % d
    rot_ns = ns[i:] + ns[:i]
    a, b = rot_ns[0], rot_ns[k]
    P = rot_ns[1:k]
    Q = rot_ns[k + 1:]
    nv = max(T.rot) + 1
    v1, v2, x = v, nv, nv + 1
    rot = {w: list(l) for w, l in T.rot.items()}
    rot[v1] = [a] + P + [b, x]
    rot[v2] = [b] + Q + [a, x]
    rot[x] = [a, v1, b, v2]
    ra = rot[a]; kk = ra.index(v); rot[a] = ra[:kk] + [v1, x, v2] + ra[kk + 1:]
    rb = rot[b]; kk = rb.index(v); rot[b] = rb[:kk] + [v2, x, v1] + rb[kk + 1:]
    for q in Q:
        rq = rot[q]; kk = rq.index(v); rq[kk] = v2
    yield Tri(rot)
