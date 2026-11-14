import etri, sys
from rainbow import RB
from collections import Counter
vmin, vmax = int(sys.argv[1]), int(sys.argv[2])
cnt = Counter()
for V, idx, f0, I in etri.all_rooted(vmin, vmax):
    rb = RB(I)
    trees = rb.all_trees()
    if not trees: continue
    n = I.n; X = rb.X
    cnt['instances'] += 1
    for j in range(n):
        pass
    groups = [dict() for _ in range(n)]
    for s in trees:
        for j in range(n):
            groups[j].setdefault(s[:j] + s[j+1:], []).append(s[j])
    for s in trees:
        c = Counter(s); a = Counter()
        for j in range(n):
            g = groups[j][s[:j] + s[j+1:]]
            alt = g[0] if g[1] == s[j] else g[1]
            a[alt] += 1
        ok = all(c.get(t, 0) + a.get(t, 0) == 2 for t in I.A) and a.get(I.f0, 0) == 0
        cnt['trees'] += 1; cnt['identity_ok'] += ok
        if not ok and cnt['shown'] < 3:
            cnt['shown'] += 1
            print(V, idx, f0, [(c.get(t,0), a.get(t,0)) for t in I.A], 'a_t0', a.get(I.f0,0))
print(dict(cnt))
