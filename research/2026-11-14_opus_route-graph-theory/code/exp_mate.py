"""E3: for each tree matching s with unique mate r: orientation pattern of the cycles of
D(r,s) (#cw, #ccw), and whether (s_min, s_max) is a disjoint pair / forest pair.
Usage: python exp_mate.py Vmax"""
import sys, collections
from tri import generate, load
from states import Rooted
from lattice import extremes, diff_cycles

Vmax = int(sys.argv[1])
Vmin = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for V in range(Vmin, Vmax + 1):
    try:
        Ts = load(V)
    except FileNotFoundError:
        Ts = generate(V)[V]
    pat = collections.Counter()
    mm = collections.Counter()
    for T in Ts:
        for f in T.faces():
            R = Rooted(T, f)
            if R.black_inner_sep_triangles():
                continue
            S = R.states()
            for s in S:
                if R.is_tree_matching(s):
                    (r,) = R.mates(s)
                    cs = diff_cycles(R, r, s)
                    pat[(sum(d == 3 for _, d in cs), sum(d == -3 for _, d in cs))] += 1
            (mn,), (mx,) = extremes(R, S)
            disj = all(mn[t] != mx[t] for t in R.A)
            mm[(disj, disj and R.is_tree_matching(mx), disj and R.is_tree_matching(mn))] += 1
    print(V, "mate-cycle (cw,ccw) pattern:", dict(pat))
    print("   (min,max) disjoint / Q_max forest / Q_min forest:", dict(mm), flush=True)
