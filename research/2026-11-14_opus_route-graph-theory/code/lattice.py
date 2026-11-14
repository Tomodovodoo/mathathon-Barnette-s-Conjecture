"""State lattice tools (Propp/Felsner lattice of perfect matchings of B).
For states r, s the faces with r(t) != s(t) give edges r(t)->s(t) forming disjoint
directed cycles in T; by the disk identity each has delta-sum -3 (ccw) or +3 (cw)."""
from states import Rooted

def delta(R, v, w):
    """+1 if the black face of edge vw lies on the left of v->w"""
    t = R.bf[frozenset((v, w))]
    i = t.index(v)
    return 1 if t[(i + 1) % 3] == w else -1

def diff_cycles(R, r, s):
    """list of (cycle vertex list, delta-sum) for the cycles of r^{-1}s"""
    succ = {r[t]: s[t] for t in R.A if r[t] != s[t]}
    seen = set()
    out = []
    for x in succ:
        if x in seen:
            continue
        cyc = []
        y = x
        while y not in seen:
            seen.add(y)
            cyc.append(y)
            y = succ[y]
        d = sum(delta(R, cyc[i], cyc[(i + 1) % len(cyc)]) for i in range(len(cyc)))
        out.append((cyc, d))
    return out

def extremes(R, S):
    """states s such that every other state r differs from s only by cycles that are
    clockwise as r->s ... returns (mins, maxs): mins = no ccw cycle r(t)->s(t)? We use:
    s is 'min' if for all r, all cycles of edges s(t)->r(t) are clockwise (delta=+3)."""
    mins, maxs = [], []
    for s in S:
        allcw = allccw = True
        for r in S:
            for cyc, d in diff_cycles(R, s, r):
                assert d in (3, -3), d
                if d == -3:
                    allcw = False
                else:
                    allccw = False
            if not allcw and not allccw:
                break
        if allcw:
            mins.append(s)
        if allccw:
            maxs.append(s)
    return mins, maxs

def face_flips(R, s):
    """white triangles avoiding the roots that are alternating for s;
    returns list of (face, delta-sum of the 3-cycle s(t)->next)"""
    out = []
    Rs = set(R.R)
    for y in R.white:
        if Rs & set(y):
            continue
        # black faces across the sides of y
        ok = True
        for i in range(3):
            a, b = y[i], y[(i + 1) % 3]
            t = R.bf[frozenset((a, b))]
            if s[t] not in (a, b):
                ok = False
        if ok:
            out.append(y)
    return out
