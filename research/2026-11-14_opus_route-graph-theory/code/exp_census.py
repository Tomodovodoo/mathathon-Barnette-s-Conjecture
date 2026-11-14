"""E0: census.  For every Eulerian triangulation (V<=Vmax) and every root face t0:
#states, #tree matchings, pair test, black-inner separating triangles.
Checks barnette_trees Thm 1.2 (i)<=>(ii)<=>(iii) and the unique-mate property.
Usage: python exp_census.py Vmax"""
import sys
from tri import generate, load
from states import Rooted

Vmax = int(sys.argv[1])
rows = []
Vmin = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for V in range(Vmin, Vmax + 1):
    try:
        Ts = load(V)
    except FileNotFoundError:
        Ts = generate(V)[V]
    tot = bad = 0
    for T in Ts:
        for f in T.faces():
            R = Rooted(T, f)
            S = R.states()
            tm = [s for s in S if R.is_tree_matching(s)]
            hp = R.has_pair()
            bi = R.black_inner_sep_triangles()
            ok = (len(tm) > 0) == hp == (len(bi) == 0)
            # unique mate
            for s in tm:
                if len(R.mates(s)) != 1:
                    ok = False
            tot += 1
            bad += (not ok)
            rows.append((V, len(R.T.separating_triangles()) > 0, len(S), len(tm), hp, len(bi)))
    print(f"V={V}: rooted instances {tot}, violations {bad}", flush=True)
import collections
Vmin = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for V in range(Vmin, Vmax + 1):
    r = [x for x in rows if x[0] == V]
    if not r:
        continue
    noST = [x for x in r if not x[1]]
    print(V, "instances", len(r), "no-sep-tri", len(noST),
          "min #TM (no sep tri)", min((x[3] for x in noST), default=None),
          "min TM/states ratio", min((x[3] / x[2] for x in noST), default=None))
