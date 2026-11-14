"""E12: is s -> partition (construction) a bijection from tree matchings onto induced-tree
partitions with the prescribed root pattern?  Usage: python exp_induced.py Vmax [Vmin]"""
import sys
from tri import load
from states import Rooted
from induced import construct, classes, partitions, derive

Vmax = int(sys.argv[1]); Vmin = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for V in range(Vmin, Vmax + 1):
    c = dict(inst=0, bij=0, derived_tm=0, roundtrip=0)
    nums = []
    for T in load(V):
        for f in T.faces():
            R = Rooted(T, f)
            if R.black_inner_sep_triangles():
                continue
            e0 = (R.t0[0], R.t0[1])
            TM = [s for s in R.states() if R.is_tree_matching(s)]
            img = {}
            for s in TM:
                P = construct(R, s, e0)
                cl = classes(R, P)
                assert len(cl) == 2
                U = [C for C in cl if e0[0] in C][0]
                img[frozenset(s.items())] = frozenset(U)
            parts = partitions(R, e0)
            c['inst'] += 1
            ok_der = all(R.is_tree_matching(derive(R, U, e0)) for U in parts)
            c['derived_tm'] += ok_der
            rt = all(img.get(frozenset(derive(R, U, e0).items())) == U for U in parts)
            c['roundtrip'] += rt
            inj = len(set(img.values())) == len(img)
            c['bij'] += (inj and set(img.values()) == set(parts))
            nums.append((len(TM), len(parts)))
    print(V, c, "sample (#TM,#partitions):", nums[:6], flush=True)
