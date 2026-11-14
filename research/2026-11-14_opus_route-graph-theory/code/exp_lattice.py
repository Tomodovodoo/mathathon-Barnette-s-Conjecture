"""E2: are the extreme states of the matching lattice tree matchings?
Usage: python exp_lattice.py Vmax"""
import sys
from tri import generate, load
from states import Rooted
from lattice import extremes

Vmax = int(sys.argv[1])
Vmin = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for V in range(Vmin, Vmax + 1):
    try:
        Ts = load(V)
    except FileNotFoundError:
        Ts = generate(V)[V]
    c = dict(inst=0, min_tm=0, max_tm=0, either=0, nmin1=0)
    ex = None
    for T in Ts:
        for f in T.faces():
            R = Rooted(T, f)
            if R.black_inner_sep_triangles():
                continue
            S = R.states()
            mins, maxs = extremes(R, S)
            c['inst'] += 1
            c['nmin1'] += (len(mins) == 1 and len(maxs) == 1)
            a = all(R.is_tree_matching(s) for s in mins)
            b = all(R.is_tree_matching(s) for s in maxs)
            c['min_tm'] += a
            c['max_tm'] += b
            c['either'] += a or b
            if not a and ex is None:
                ex = (T.rot, f)
    print(V, c, flush=True)
    if ex:
        print("   first min-not-tree example:", ex)
