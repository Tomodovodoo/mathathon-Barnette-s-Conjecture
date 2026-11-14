"""The authors' stack(6,q) graphs, generated with their families.py (generation only),
then counted with core.py. Also a mixed gluing built with core.py alone."""
import sys, itertools
sys.path.insert(0, '../../2026-11-14_sol_counting-families/code')
sys.dont_write_bytecode = True
from core import *
import families as fam
print('authors stack(6,q), counted by referee code:')
for q in range(1, 6):
    b = fam.stack(6, q)
    g = b.T if hasattr(b, 'T') else b.g
    root = set(b.faces[b.outer]) if hasattr(b, 'outer') else None
    inst = Inst(nx.Graph(g), tuple(root))
    r = inst.summary()
    H, use = hamilton(inst)
    f = inst.faces[inst.t0]
    av = sorted(H - use.get(frozenset(e), 0) for e in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])))
    print(q, 'V', len(g), 'S', r['S'], 'P', r['P'], 'M', r['M'], 'm', r['m'], 'H', H, 'root avoid', av, 'poly', r['poly'])
print('mixed gluing with core.py: first step one permutation, later steps another')
base = bipyramid(6)
found = []
for p1 in itertools.permutations((6, 0, 1)):
    for p2 in itertools.permutations((6, 0, 1)):
        Hs = []
        for q in range(1, 5):
            g = base.copy(); cur = {x: x for x in base.nodes()}
            for step in range(q - 1):
                g, cur = glue(g, [cur[4], cur[5], cur[7]], base, list(p1 if step == 0 else p2))
            Hs.append(hamilton(Inst(g, (6, 0, 1)), per_edge=False)[0])
        if Hs == [8, 20, 60, 180]:
            found.append((p1, p2))
print('pairs (first, later) of images of (v4,v5,S) giving 8,20,60,180:', found)
