"""Two induced trees <-> tree matchings.
construct(R, s, e0): OpenAI section 6 (white tree rooted at y0, selected sides, P).
partitions(R, e0): all partitions of V(T) into two induced trees, ends of e0 together,
third root of t0 apart.
derive(R, U): s(t) = tail of t's monochromatic edge, edges oriented toward the roots in
P - e0."""
import itertools
from states import Rooted, UF


def construct(R, s, e0):
    e0 = frozenset(e0)
    y0 = R.wf[e0]
    # white tree: spoke (t, s(t)) joins the white faces across the two sides of t at s(t)
    adj = {y: [] for y in R.white}
    for t in R.A:
        v = s[t]
        sides = [frozenset((v, w)) for w in t if w != v]
        y1, y2 = R.wf[sides[0]], R.wf[sides[1]]
        adj[y1].append((y2, t, sides[0]))
        adj[y2].append((y1, t, sides[1]))
    # BFS from y0; each face y != y0 gets the tree edge to its parent; select the side of t
    # (incident with s(t)) bordering y
    P = {e0}
    seen = {y0}
    stack = [y0]
    while stack:
        y = stack.pop()
        for (z, t, side_at_y) in adj[y]:
            if z in seen:
                continue
            seen.add(z)
            stack.append(z)
            # side of t bordering z
            v = s[t]
            side_z = [frozenset((v, w)) for w in t if w != v and R.wf[frozenset((v, w))] == z][0]
            P.add(side_z)
    assert len(seen) == len(R.white), "not a tree"
    return P


def classes(R, P):
    uf = UF(R.T.V)
    for e in P:
        uf.union(*e)
    comps = {}
    for v in R.T.V:
        comps.setdefault(uf.find(v), set()).add(v)
    return list(comps.values())


def is_induced_tree_partition(R, U):
    U = set(U)
    W = set(R.T.V) - U
    for C in (U, W):
        if not C:
            return False
        E = [e for e in R.T.edges() if e[0] in C and e[1] in C]
        if len(E) != len(C) - 1:
            return False
        uf = UF(list(C))
        for e in E:
            if not uf.union(*e):
                return False
    return True


def partitions(R, e0):
    a, b = e0
    c = [r for r in R.R if r not in e0][0]
    others = [v for v in R.T.V if v not in R.R]
    out = []
    for bits in itertools.product((0, 1), repeat=len(others)):
        U = {a, b} | {v for v, bb in zip(others, bits) if bb}
        if is_induced_tree_partition(R, U):
            out.append(frozenset(U))
    return out


def derive(R, U, e0):
    U = set(U)
    mono = [frozenset(e) for e in R.T.edges() if (e[0] in U) == (e[1] in U)]
    P0 = [e for e in mono if e != frozenset(e0)]
    # orient toward roots
    adj = {v: [] for v in R.T.V}
    for e in P0:
        x, y = tuple(e)
        adj[x].append(y); adj[y].append(x)
    parent = {}
    for r in R.R:
        parent[r] = None
        stack = [r]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w not in parent:
                    parent[w] = u
                    stack.append(w)
    s = {}
    for t in R.A:
        e = [frozenset((t[i], t[(i + 1) % 3])) for i in range(3) if frozenset((t[i], t[(i + 1) % 3])) in set(P0)]
        assert len(e) == 1
        x, y = tuple(e[0])
        s[t] = x if parent.get(x) == y else y
    return s
