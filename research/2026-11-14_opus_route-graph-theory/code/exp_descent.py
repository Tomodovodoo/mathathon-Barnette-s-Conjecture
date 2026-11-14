"""E4: local search.  k(s) = number of unicyclic components of Q_s (s has 2^k mates,
or none).  Moves: for a mate r of s and a cycle C of D(r,s), s' = s with s(t):=r(t) on C.
Trap = state s with a mate, k(s)>0, and every move gives k(s') >= k(s).
Usage: python exp_descent.py Vmax"""
import sys, collections
from tri import generate, load
from states import Rooted, UF
from lattice import diff_cycles

def kval(R, s):
    """None if no mate, else number of unicyclic components"""
    V = R.T.V
    uf = UF(V)
    Q = R.Q(s)
    for e in Q:
        uf.union(*e)
    comp_e = collections.Counter(uf.find(e[0]) for e in Q)
    comp_v = collections.Counter(uf.find(v) for v in V)
    comp_r = collections.Counter(uf.find(v) for v in R.R)
    k = 0
    for c, nv in comp_v.items():
        ne, nr = comp_e[c], comp_r[c]
        if nr == 1 and ne == nv - 1:
            continue
        if nr == 0 and ne == nv:
            k += 1
            continue
        return None
    return k

if __name__ == '__main__':
    Vmax = int(sys.argv[1])
    Vmin = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    for V in range(Vmin, Vmax + 1):
        try:
            Ts = load(V)
        except FileNotFoundError:
            Ts = generate(V)[V]
        traps = 0; tot = 0; strict_traps = 0
        ex = None
        for T in Ts:
            for f in T.faces():
                R = Rooted(T, f)
                if R.black_inner_sep_triangles():
                    continue
                for s in R.states():
                    k = kval(R, s)
                    if not k:
                        continue
                    tot += 1
                    best = 10**9
                    for r in R.mates(s):
                        for cyc, d in diff_cycles(R, r, s):
                            cs = set(cyc)
                            s2 = dict(s)
                            for t in R.A:
                                if r[t] in cs:
                                    s2[t] = r[t]
                            k2 = kval(R, s2)
                            assert k2 is not None
                            best = min(best, k2)
                    if best >= k:
                        traps += 1
                        if ex is None:
                            ex = (V, T.rot, R.t0, s, k)
                    if best > k:
                        strict_traps += 1
        print(V, "states with k>0:", tot, "traps (no decreasing move):", traps, "strict:", strict_traps, flush=True)
        if ex and ex[0] == V:
            print("   example", ex)
