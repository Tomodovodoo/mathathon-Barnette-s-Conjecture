"""E13: do the two faces through e0 (t0 black, y0 white with colours swapped) together
cover all induced-tree partitions?  Usage: python exp_induced2.py Vmax [Vmin]"""
import sys
from tri import load
from states import Rooted
from induced import construct, classes, partitions

def image(R, e0):
    out = set()
    for s in R.states():
        if R.is_tree_matching(s):
            cl = classes(R, construct(R, s, e0))
            out.add(frozenset([C for C in cl if e0[0] in C][0]))
    return out

Vmax = int(sys.argv[1]); Vmin = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for V in range(Vmin, Vmax + 1):
    c = dict(edges=0, covered=0, disjoint_images=0)
    for T in load(V):
        done = set()
        for f in T.faces():
            for i in range(3):
                e0 = (f[i], f[(i + 1) % 3])
                if frozenset(e0) in done:
                    continue
                done.add(frozenset(e0))
                R1 = Rooted(T, f)
                y0 = R1.wf[frozenset(e0)] if R1.col[R1.t0] == 0 else None
                g = [h for h in T.faces() if set(e0) <= set(h) and set(h) != set(f)][0]
                R2 = Rooted(T, g)
                if R1.black_inner_sep_triangles() and R2.black_inner_sep_triangles():
                    continue
                I1 = image(R1, e0) if not R1.black_inner_sep_triangles() else set()
                I2 = image(R2, e0) if not R2.black_inner_sep_triangles() else set()
                parts = set(partitions(R1, e0))
                assert parts == set(partitions(R2, e0))
                c['edges'] += 1
                c['covered'] += (I1 | I2) == parts
                c['disjoint_images'] += not (I1 & I2)
    print(V, c, flush=True)
