"""E14: pair existence (flow) vs black-inner separating triangles, all rooted Eulerian
triangulations V <= Vmax.  Also counts rooted instances that have separating triangles
(so the primal graph is not cyclically 4-edge-connected) but still have pairs.
Usage: python exp_obstruction.py Vmax"""
import sys
from tri import load
from states import Rooted
Vmax = int(sys.argv[1])
for V in range(6, Vmax + 1):
    tot = agree = sep_but_pair = sep = 0
    for T in load(V):
        st = bool(T.separating_triangles())
        for f in T.faces():
            R = Rooted(T, f)
            hp = R.has_pair()
            bi = bool(R.black_inner_sep_triangles())
            tot += 1
            agree += (hp == (not bi))
            sep += st
            sep_but_pair += (st and hp)
    print(f"V={V}: rooted {tot}, flow==criterion {agree}, with sep. triangle {sep}, of which pairs exist {sep_but_pair}", flush=True)
