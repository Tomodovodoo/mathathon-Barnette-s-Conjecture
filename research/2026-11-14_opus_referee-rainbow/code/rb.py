"""Rainbow trees, moves, the surplus walk, matroid intersection. Own implementation."""
import itertools
from core import UF


def matroid_intersection(E, ind1, ind2):
    """Max common independent set by shortest augmenting paths (Edmonds / Lawler)."""
    I = []
    while True:
        Iset = set(I)
        out = [e for e in E if e not in Iset]
        X1 = {y for y in out if ind1(I + [y])}
        X2 = {y for y in out if ind2(I + [y])}
        if not X1:
            return I
        # exchange graph
        adj = {e: [] for e in E}
        for x in I:
            rest = [z for z in I if z != x]
            for y in out:
                if ind1(rest + [y]):
                    adj[x].append(y)
                if ind2(rest + [y]):
                    adj[y].append(x)
        # BFS from X1 to X2
        par = {y: None for y in X1}
        q = list(X1)
        end = None
        for y in q:
            if y in X2:
                end = y
                break
        qi = 0
        while end is None and qi < len(q):
            a = q[qi]; qi += 1
            for b in adj[a]:
                if b not in par:
                    par[b] = a
                    q.append(b)
                    if b in X2 and b not in Iset:
                        end = b
                        break
        if end is None:
            return I
        path = []
        while end is not None:
            path.append(end)
            end = par[end]
        S = Iset.symmetric_difference(path)
        I = list(S)


def point_spokes(R):
    return [(t, x) for x in R.X for t in R.bat[x]]


def find_rainbow(R):
    E = point_spokes(R)

    def ind2(S):
        pts = [x for (_, x) in S]
        return len(pts) == len(set(pts))
    I = matroid_intersection(E, R.w_is_forest, ind2)
    if len(I) < R.n:
        return None
    return {x: t for (t, x) in I}


def is_rainbow(R, sig):
    return R.H_minus_is_tree([(t, x) for x, t in sig.items()])


def all_rainbow(R):
    X = R.X
    res = []
    for combo in itertools.product(*[R.bat[x] for x in X]):
        sig = dict(zip(X, combo))
        if is_rainbow(R, sig):
            res.append(sig)
    return res


def tree_adj(R, sig):
    """Adjacency of F_sigma = H minus the spokes (sigma(x), x)."""
    adj = {i: [] for i in range(R.NH)}
    for t in R.black:
        c = R.cidx[t]
        for v in R.T.faces[t]:
            if sig.get(v) == t:
                continue
            adj[c].append(v); adj[v].append(c)
    return adj


def alt(R, sig, x, adj=None):
    """All t' != sigma(x) at x such that sigma[x:=t'] is rainbow, computed via the
    fundamental cycle: path in F_sigma from the centre of sigma(x) to x."""
    if adj is None:
        adj = tree_adj(R, sig)
    src = R.cidx[sig[x]]
    par = {src: None}
    st = [src]
    while st:
        a = st.pop()
        if a == x:
            break
        for b in adj[a]:
            if b not in par:
                par[b] = a
                st.append(b)
    prev = par[x]  # the centre adjacent to x on the path
    return R.black[prev - R.T.V]


def loads(R, sig):
    c = {t: 0 for t in R.A}
    for x, t in sig.items():
        c[t] += 1
    return c


def excess(R, sig):
    return sum(abs(v - 1) for v in loads(R, sig).values())


def key(R, sig):
    return tuple(sig[x] for x in R.X)


def unkey(R, k):
    return dict(zip(R.X, k))


# ---- the surplus walk ("evict the resident") ----
def walk_step(R, sig, t, arrival):
    """One step from walk state (sig, t, arrival). Returns ('stop', sig') when the move
    of the resident lands in an empty face, else ('go', sig', t', resident)."""
    res = [x for x, f in sig.items() if f == t and x != arrival]
    assert len(res) == 1
    y = res[0]
    t2 = alt(R, sig, y)
    c2 = sum(1 for f in sig.values() if f == t2)
    sig2 = dict(sig); sig2[y] = t2
    if c2 == 0:
        return ('stop', sig2)
    assert c2 == 1
    return ('go', sig2, t2, y)


def iota(R, s, t, maxsteps=100000):
    """Fable's involution iota_t on good states. s: dict face -> point."""
    sig = {x: f for f, x in s.items()}
    x0 = s[t]
    t1 = alt(R, sig, x0)
    sig[x0] = t1
    state = (sig, t1, x0)
    for _ in range(maxsteps):
        r = walk_step(R, *state)
        if r[0] == 'stop':
            out = r[1]
            return {f: x for x, f in out.items()}
        state = r[1:]
    raise RuntimeError('walk did not stop')
