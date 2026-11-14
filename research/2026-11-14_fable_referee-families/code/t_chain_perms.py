"""Prism chain: all six identifications of the new cap (N,v0,v1) with the old white face (v4,v5,S),
the same one at every step. Hamiltonian counts and root avoidance for q=1..5."""
import itertools, sys
from core import *
base = bipyramid(6)
for perm in itertools.permutations((6, 0, 1)):          # images of (v4, v5, S) are perm
    row = []
    for q in range(1, 6):
        g = base.copy(); cur = {x: x for x in base.nodes()}
        for _ in range(q - 1):
            g, cur = glue(g, [cur[4], cur[5], cur[7]], base, list(perm))
        inst = Inst(g, (6, 0, 1))
        H, use = hamilton(inst, per_edge=True)
        av = [H - use.get(frozenset(e), 0) for e in ((6, 0), (6, 1), (0, 1))]
        row.append((H, av))
    names = {6: 'N', 0: 'v0', 1: 'v1'}
    print('(v4,v5,S) <- (%s,%s,%s):' % tuple(names[x] for x in perm), row); sys.stdout.flush()
