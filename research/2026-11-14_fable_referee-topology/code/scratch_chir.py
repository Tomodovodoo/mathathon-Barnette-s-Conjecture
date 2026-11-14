import etri, random
from rainbow import RB
from collections import Counter
rng = random.Random(1)
cnt = Counter()
shown = 0
for V, idx, f0, I in etri.all_rooted(8, 12):
    rb = RB(I)
    trees = rb.all_trees()
    if not trees: continue
    for s in rng.sample(trees, min(40, len(trees))):
        sigma = dict(zip(rb.X, s))
        pts = {}
        for x, t in sigma.items(): pts.setdefault(t, []).append(x)
        twos = [t for t in pts if len(pts[t]) == 2]
        if not twos: continue
        t = rng.choice(twos); x_in = rng.choice(pts[t])
        seq = []
        sg = dict(sigma)
        while True:
            y = [p for p in pts[t] if p != x_in][0]
            # chirality: is dart x_in -> y inside t (black on left)?
            chi = 1 if I.face_of[(x_in, y)] == t else -1
            (t2,) = rb.move_target(sg, y)
            load2 = len(pts.get(t2, []))
            seq.append(chi)
            sg[y] = t2; pts[t].remove(y); pts.setdefault(t2, []).append(y)
            if load2 == 0: break
            t, x_in = t2, y
        cnt['walks'] += 1
        cnt['len>=2'] += (len(seq) >= 2)
        cnt['constant_chirality'] += (len(set(seq)) == 1)
        if len(seq) >= 3 and shown < 12:
            shown += 1; print(V, idx, seq)
print(dict(cnt))
