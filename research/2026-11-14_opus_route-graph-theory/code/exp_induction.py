"""E5: degree-4 contraction / expansion.
For rooted T (no black-inner separating triangle), a degree-4 vertex x off t0 with
rotation (a, v1, b, v2), merge v1,v2 -> v (when simple) to get T'.  Projection pi:
states s of T with s(beta_a), s(beta_b) not in {a, b} -> states of T' (rename v1,v2 -> v).
Questions per (T, t0, x, merge):
  P1: does T' have a tree matching (i.e. no black-inner separating triangle)?
  P2: if yes, does some tree matching of T project to a tree matching of T'?
  P3: does EVERY tree matching of T' have a lift that is a tree matching of T?
Usage: python exp_induction.py Vmax [Vmin]"""
import sys, collections
from tri import generate, load, Tri, canon_face
from states import Rooted

def contract(T, x, i):
    """merge the pair (rot[x][i], rot[x][i+2]); return (T', v1, v2) or None"""
    ns = T.rot[x]
    assert len(ns) == 4
    v1, v2 = ns[i], ns[i + 2]
    a, b = ns[(i + 1) % 4], ns[(i + 3) % 4]
    if v2 in T.pos[v1]:
        return None
    common = set(T.rot[v1]) & set(T.rot[v2])
    if common != {a, b, x}:
        return None
    E = set()
    for (p, q) in T.edges():
        if x in (p, q):
            continue
        p2 = v1 if p == v2 else p
        q2 = v1 if q == v2 else q
        E.add(tuple(sorted((p2, q2))))
    return Tri.from_edges(list(E)), v1, v2

Vmax = int(sys.argv[1]); Vmin = int(sys.argv[2]) if len(sys.argv) > 2 else 8
for V in range(Vmin, Vmax + 1):
    try:
        Ts = load(V)
    except FileNotFoundError:
        Ts = generate(V)[V]
    c = collections.Counter()
    for T in Ts:
        for f in T.faces():
            R = Rooted(T, f)
            if R.black_inner_sep_triangles():
                continue
            S = R.states()
            TM = [s for s in S if R.is_tree_matching(s)]
            for x in T.V:
                if len(T.rot[x]) != 4 or x in f:
                    continue
                for i in (0, 1):
                    res = contract(T, x, i)
                    if res is None:
                        continue
                    T2, v1, v2 = res
                    ren = lambda w: v1 if w == v2 else w
                    f2 = tuple(ren(w) for w in f)
                    R2 = Rooted(T2, f2)
                    # map faces of T (not containing x) to faces of T2
                    fm = {}
                    for t in R.A:
                        if x in t:
                            continue
                        key = frozenset(ren(w) for w in t)
                        fm[t] = [t2 for t2 in R2.A if frozenset(t2) == key][0]
                    TM2 = [s for s in R2.states() if R2.is_tree_matching(s)]
                    TM2set = {frozenset(s.items()) for s in TM2}
                    c['cases'] += 1
                    c['P1 T2 has TM'] += bool(TM2)
                    if not TM2:
                        c['T2 obstructed: has sep tri'] += 1
                        continue
                    nbr = set(T.rot[x])
                    a, b = T.rot[x][(i + 1) % 4], T.rot[x][(i + 3) % 4]
                    proj_ok = False
                    lifted = set()
                    for s in TM:
                        bet = [t for t in R.A if x in t]
                        if any(s[t] in (a, b) for t in bet):
                            continue
                        s2 = frozenset((fm[t], ren(s[t])) for t in R.A if x not in t)
                        if s2 in TM2set:
                            proj_ok = True
                            lifted.add(s2)
                    c['P2 some TM projects to TM'] += proj_ok
                    c['P3 every TM of T2 lifts'] += (lifted == TM2set)
    print(V, dict(c), flush=True)
