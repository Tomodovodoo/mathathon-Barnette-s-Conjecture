import etri, random
from rainbow import RB
from collections import Counter
rng = random.Random(11)
cnt = Counter()
for V, idx, f0, I in etri.all_rooted(6, 13):
    rb = RB(I); trees = rb.all_trees()
    if not trees: continue
    n = I.n; Aidx = {t: i for i, t in enumerate(I.A)}
    L = set()
    for s in trees:
        c = [0]*n
        for t in s: c[Aidx[t]] += 1
        L.add(tuple(c))
    Ls = sorted(L); ok = True
    for _ in range(4000):
        c = rng.choice(Ls); c2 = rng.choice(Ls)
        for i in range(n):
            if c[i] > c2[i]:
                good = False
                for j in range(n):
                    if c[j] < c2[j]:
                        a = list(c); a[i]-=1; a[j]+=1; b = list(c2); b[i]+=1; b[j]-=1
                        if tuple(a) in L and tuple(b) in L: good = True; break
                if not good: ok = False; break
        if not ok: break
    facs = set()
    for s in I.states():
        for r in I.mates(s):
            facs.add(frozenset([(s[i], I.A[i]) for i in range(n)] + [(r[i], I.A[i]) for i in range(n)]))
    cnt[(len(facs), ok)] += 1
print(dict(cnt))
