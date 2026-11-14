"""E18: does every 2-factor of B (every D, i.e. every unordered pair up to cycle
orientations) contain an ordered tree pair?  Exhaustive.  Usage: python exp_every_factor.py Vmax [Vmin]"""
import sys
from tri import load
from states import Rooted
Vmax = int(sys.argv[1]); Vmin = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for V in range(Vmin, Vmax + 1):
    inst = facs_tot = bad = 0
    ex = None
    for T in load(V):
        for f in T.faces():
            R = Rooted(T, f)
            if R.black_inner_sep_triangles():
                continue
            inst += 1
            facs = {}
            for s in R.states():
                tm = R.is_tree_matching(s)
                for r in R.mates(s):
                    key = frozenset((t, frozenset((r[t], s[t]))) for t in R.A)
                    facs[key] = facs.get(key, False) or tm
            facs_tot += len(facs)
            nb = sum(1 for v in facs.values() if not v)
            bad += nb
            if nb and ex is None:
                ex = (T.rot, R.t0, [k for k, v in facs.items() if not v][0])
    print(V, "instances", inst, "2-factors", facs_tot, "2-factors without tree pair", bad, flush=True)
    if ex:
        print("   example:", ex[0], ex[1])
        ex = None
