"""Cross-check own counts (states, pairs, TM) against workings/barnette_lab on V<=13, all roots."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','..','..','workings','barnette_lab'))
import networkx as nx
from tri import *
from barnette_lab.core import Instance
bad = 0; tot = 0
for n in range(6, 14):
    for rot in plantri(n):
        T = from_rotation(rot)
        g = nx.Graph([(u, w) for u, nb in enumerate(rot) for w in nb])
        for t0 in range(len(T.F)):
            I = Instance(g, outer=None) if False else None
            # find lab face index equal to our face
            lab = Instance(g, outer=0)
            idx = [set(f) for f in lab.faces].index(set(T.F[t0]))
            lab = Instance(g, outer=idx)
            S = list(lab.states()); P = lab.pairs(S)
            tm = sum(1 for s in S if lab.is_tree(s) and any(all(a != b for a, b in zip(r, s)) for r in S))
            inv = T.rooted(t0).invariants()
            tot += 1
            if (len(S), len(P), tm) != (inv['states'], inv['pairs'], inv['TM']):
                bad += 1; print('DIFF', n, t0, (len(S), len(P), tm), inv)
print('instances', tot, 'differences', bad)
