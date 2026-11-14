"""E6: anatomy of decreasing moves.  For states s with k(s)>0 and each (mate r, D-cycle Delta):
features -> effect on k.  Features: Delta meets a unicyclic component (vertex set);
Delta meets a Q-cycle; orientation of Delta (cw/ccw); orientation of the Q-cycles under r.
Usage: python exp_moves.py Vmax [Vmin]"""
import sys, collections
from tri import generate, load
from states import Rooted, UF
from lattice import diff_cycles, delta
from exp_descent import kval

def qcomponents(R, s):
    uf = UF(R.T.V)
    Q = R.Q(s)
    for e in Q:
        uf.union(*e)
    comps = collections.defaultdict(set)
    for v in R.T.V:
        comps[uf.find(v)].add(v)
    roots = set(R.R)
    uni = [c for c in comps.values() if not (c & roots)]
    return uni

def qcycles(R, s, r):
    """directed cycles of edges r(t)->u(t)"""
    succ = {}
    for t in R.A:
        u = [w for w in t if w != r[t] and w != s[t]][0]
        succ[r[t]] = u
    cyc = []
    seen = set()
    for x0 in succ:
        path = []
        pos = {}
        y = x0
        while y in succ and y not in seen and y not in pos:
            pos[y] = len(path); path.append(y); y = succ[y]
        if y in pos:
            c = path[pos[y]:]
            d = sum(delta(R, c[i], c[(i + 1) % len(c)]) for i in range(len(c)))
            cyc.append((c, d))
        seen.update(path)
    return cyc

if __name__ == "__main__":
    Vmax = int(sys.argv[1]); Vmin = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    for V in range(Vmin, Vmax + 1):
        Ts = load(V)
        stat = collections.Counter()
        for T in Ts:
            for f in T.faces():
                R = Rooted(T, f)
                if R.black_inner_sep_triangles():
                    continue
                for s in R.states():
                    k = kval(R, s)
                    if not k:
                        continue
                    uni = qcomponents(R, s)
                    univ = set().union(*uni)
                    for r in R.mates(s):
                        qc = qcycles(R, s, r)
                        qcv = set().union(*[set(c) for c, _ in qc])
                        qor = tuple(sorted(d for _, d in qc))
                        for cyc, d in diff_cycles(R, r, s):
                            cs = set(cyc)
                            s2 = dict(s)
                            for t in R.A:
                                if r[t] in cs:
                                    s2[t] = r[t]
                            dk = kval(R, s2) - k
                            key = ("meets_uni" if cs & univ else "misses_uni",
                                   "meets_Qcyc" if cs & qcv else "misses_Qcyc",
                                   "D_ccw" if d == -3 else "D_cw")
                            stat[(key, "dk<0" if dk < 0 else ("dk=0" if dk == 0 else "dk>0"))] += 1
        print(V)
        for kk in sorted(stat):
            print("   ", kk, stat[kk])
