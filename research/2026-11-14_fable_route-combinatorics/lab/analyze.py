"""Statistics and checks for one rooted Eulerian triangulation."""
from collections import defaultdict
from math import comb, factorial
from rooted import Rooted, dual_ham_cycles


def analyze(R, hams=None, deep=True):
    """Returns a dict of statistics.  Raises AssertionError if a proved statement of
    the three papers fails (that would be a bug here or an error there)."""
    T, n = R.T, R.n
    st = R.states()
    res = {'n': n, 'states': len(st)}
    if st:
        sg = {R.perm_sign(s) for s in st}
        assert len(sg) == 1, "states of both permutation signs"
    R.check_weights()
    info = {}
    for s in st:
        valid, forced, cycles = R.Q_structure(s)
        info[s] = (valid, forced, cycles)
    partnered = [s for s in st if info[s][0]]
    trees = [s for s in partnered if not info[s][2]]
    res['partnered'] = len(partnered)
    res['trees'] = len(trees)
    res['k_hist'] = dict(sorted(_hist(len(info[s][2]) for s in partnered).items()))
    om = {s: R.omega(s) for s in st}
    pairs = []          # (r, s, J, eps, Dkey, ccwflags)
    Dinfo = {}          # Dkey -> list of cycles in ccw orientation [(i, tail, head)...]
    qorient = defaultdict(int)
    for s in partnered:
        ps = R.partners(s)
        assert len(ps) == 2 ** len(info[s][2])
        # disk identity on the cycles of Q_s, both directions
        for cyc in info[s][2]:
            verts = [x for (_, x, _) in cyc]
            ccw, _ = R.is_ccw(verts)
            dsum = sum(R.delta(x, y) for (_, x, y) in cyc)
            assert dsum == (-3 if ccw else 3), "disk identity fails on Q-cycle"
            assert len(cyc) % 2 == 1
        for r in ps:
            assert all(a != b for a, b in zip(r, s))
            cycles = R.D_cycles(r, s)
            J3 = 0
            flags = []
            key = []
            ccw_cycles = []
            for cyc in cycles:
                verts = [t for (_, t, _) in cyc]
                ccw, left = R.is_ccw(verts)
                dsum = sum(R.delta(t, h) for (_, t, h) in cyc)
                assert dsum == (-3 if ccw else 3), "disk identity fails on D-cycle"
                J3 += dsum
                flags.append(ccw)
                key.append(frozenset(frozenset((t, h)) for (_, t, h) in cyc))
                ccw_cycles.append(cyc if ccw else [(i, h, t) for (i, t, h) in reversed(cyc)])
            assert J3 % 3 == 0
            J = J3 // 3
            assert (n + J) % 2 == 0
            eps = -1 if ((n + J) // 2) % 2 else 1
            Dkey = frozenset(key)
            if Dkey not in Dinfo:
                Dinfo[Dkey] = ccw_cycles
            pairs.append((r, s, J, eps, Dkey, tuple(flags)))
    res['pairs'] = len(pairs)
    # sign of a tree matching, cancellation for the others
    mu = defaultdict(int)
    for (r, s, J, eps, Dkey, flags) in pairs:
        mu[s] += eps
    for s in partnered:
        if info[s][2]:
            assert mu[s] == 0
        else:
            assert mu[s] in (1, -1)
    res['trees_plus'] = sum(1 for s in trees if mu[s] == 1)
    res['trees_minus'] = sum(1 for s in trees if mu[s] == -1)
    # D groups
    chist = defaultdict(int)
    areas = {}
    for Dkey, cycs in Dinfo.items():
        chist[len(cycs)] += 1
        ar = []
        for cyc in cycs:
            a = R.cycle_area(cyc)
            if deep:
                assert a == len(R.enclosed_white(cyc)), "area is not the enclosed face count"
            assert a > 0
            ar.append(a)
        areas[Dkey] = ar
    res['D_hist'] = dict(sorted(chist.items()))
    res['groups'] = len(Dinfo)
    assert len(pairs) == sum(2 ** len(c) for c in Dinfo.values())
    if not pairs:
        res['cmin'] = None
        return res, None
    m = min(chist)
    res['cmin'] = m
    # moments of the signed tree measure
    lead = sum(_prod(areas[D]) for D in Dinfo if len(Dinfo[D]) == m)
    res['lead'] = lead
    for j in range(m + 1):
        mom_pairs = sum(eps * om[s] ** j for (r, s, J, eps, Dkey, flags) in pairs)
        mom_trees = sum(mu[s] * om[s] ** j for s in trees)
        assert mom_pairs == mom_trees
        if j < m:
            assert mom_trees == 0, "low moment does not vanish"
        else:
            sign = -1 if ((n - m) // 2) % 2 else 1
            assert mom_trees == sign * factorial(m) * lead, (mom_trees, sign, m, lead)
    extra = {'st': st, 'info': info, 'partnered': partnered, 'trees': trees, 'om': om,
             'pairs': pairs, 'Dinfo': Dinfo, 'areas': areas, 'mu': mu}
    return res, extra


def _hist(it):
    d = defaultdict(int)
    for x in it:
        d[x] += 1
    return d


def _prod(xs):
    p = 1
    for x in xs:
        p *= x
    return p


# ---------------------------------------------------------------------------
def tree_to_cycle(R, s, e0):
    """Section 6 of the OpenAI paper: tree matching s and edge e0 of t0 -> the set P of
    selected edges (one per face).  Returns frozenset of undirected edges."""
    T = R.T
    y0 = T.de[(e0[1], e0[0])] if T.de[(e0[0], e0[1])] == R.t0 else T.de[(e0[0], e0[1])]
    adj = defaultdict(list)
    for f, v in zip(R.A, s):
        a, b, c = T.faces[f]
        k = (a, b, c).index(v)
        vp = (a, b, c)[(k + 1) % 3]
        vm = (a, b, c)[(k + 2) % 3]
        wl = T.de[(vp, v)]    # white face across side v-vp
        wr = T.de[(v, vm)]    # white face across side vm-v
        adj[wl].append((wr, frozenset((v, vm))))   # edge selected if wr is the child
        adj[wr].append((wl, frozenset((v, vp))))
    seen = {y0}
    stack = [y0]
    P = {frozenset(e0)}
    while stack:
        x = stack.pop()
        for (y, side) in adj[x]:
            if y not in seen:
                seen.add(y)
                P.add(side)
                stack.append(y)
    if len(seen) != len(R.white):
        return None
    return frozenset(P)


def cycle_to_state(R, P, e0):
    """Inverse direction: P = edges of T not crossed by a Hamiltonian cycle (one per
    face), e0 in P.  Orient P - e0 towards the roots; s(t) = tail of the edge in t."""
    P0 = [e for e in P if e != frozenset(e0)]
    inc = defaultdict(list)
    for e in P0:
        for v in e:
            inc[v].append(e)
    s = {}
    seen_e = set()
    stack = list(R.R)
    seen_v = set(R.R)
    while stack:
        v = stack.pop()
        for e in inc[v]:
            if e in seen_e:
                continue
            seen_e.add(e)
            (w,) = e - {v}
            if w in seen_v:
                return None
            seen_v.add(w)
            t = R.black_of_edge[e]
            s[t] = w
            stack.append(w)
    if len(s) != R.n or len(set(s.values())) != R.n:
        return None
    return tuple(s[t] for t in R.A)
