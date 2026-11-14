import etri, sys
from rainbow import RB
from collections import Counter
from fractions import Fraction
vmin, vmax = int(sys.argv[1]), int(sys.argv[2])
seen=set()
for V, idx, f0, I in etri.all_rooted(vmin, vmax):
    rb = RB(I)
    trees = rb.all_trees()
    if not trees: continue
    lev = Counter()
    per_face2 = Counter(); per_face0 = Counter()
    for s in trees:
        c = Counter(s)
        n2 = sum(1 for v in c.values() if v == 2)
        lev[2*n2] += 1
        for t in I.A:
            if c.get(t,0)==2: per_face2[t]+=1
            if c.get(t,0)==0: per_face0[t]+=1
    N = len(trees)
    nstates = len(I.states())
    key=(V,idx,tuple(sorted(lev.items())))
    if key in seen: continue
    seen.add(key)
    mean = Fraction(sum(e*k for e,k in lev.items()), N)
    print(V, idx, f0, 'n=%d'%I.n, 'N=%d'%N, 'states=%d'%nstates, 'levels', dict(sorted(lev.items())), 'mean_exc', mean,
          'P2 per face', sorted(set(Fraction(per_face2[t],N) for t in I.A)), 'P0', sorted(set(Fraction(per_face0[t],N) for t in I.A)))
