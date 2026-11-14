"""E10: 'hole' test.  If TM were the set of common bases of two matroids on the spoke
set, conv(TM) would contain no 0/1 point outside TM (the common-base polytope of two
matroids is integral and its 0/1 points are exactly the common bases).  Any 0/1 point
of conv(TM) is a fractional perfect matching, hence a state.  So we test every non-tree
state for membership in conv(TM) by LP.
Usage: python exp_hole.py Vmax [Vmin]"""
import sys
import numpy as np
from scipy.optimize import linprog
from tri import load
from states import Rooted

def in_hull(points, x):
    P = np.array(points, dtype=float).T  # d x m
    m = P.shape[1]
    A = np.vstack([P, np.ones((1, m))])
    b = np.concatenate([x, [1.0]])
    res = linprog(np.zeros(m), A_eq=A, b_eq=b, bounds=[(0, None)] * m, method="highs")
    return res.status == 0, res

Vmax = int(sys.argv[1]); Vmin = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for V in range(Vmin, Vmax + 1):
    inst = holes = 0
    first = None
    for T in load(V):
        for f in T.faces():
            R = Rooted(T, f)
            if R.black_inner_sep_triangles():
                continue
            spokes = [(t, v) for t in R.A for v in R.corners[t]]
            idx = {sp: i for i, sp in enumerate(spokes)}
            vec = lambda s: np.array([1.0 if s[t] == v else 0.0 for (t, v) in spokes])
            S = R.states()
            TM = [s for s in S if R.is_tree_matching(s)]
            non = [s for s in S if not R.is_tree_matching(s)]
            inst += 1
            if len(TM) < 3:
                continue
            pts = [vec(s) for s in TM]
            h = False
            for s in non:
                ok, res = in_hull(pts, vec(s))
                if ok:
                    h = True
                    if first is None:
                        first = (V, T.rot, R.t0, s, [(TM[i], round(w, 3)) for i, w in enumerate(res.x) if w > 1e-9])
                    break
            holes += h
    print(V, "instances", inst, "with a hole (non-tree state in conv(TM))", holes, flush=True)
    if first and first[0] == V:
        print("   example:", first)
