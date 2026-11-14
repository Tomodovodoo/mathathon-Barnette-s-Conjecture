import etri, random, sys
from rainbow import RB
from collections import Counter
rng = random.Random(1)
cnt = Counter()
shown = 0
vmin, vmax = int(sys.argv[1]), int(sys.argv[2])
for V, idx, f0, I in etri.all_rooted(vmin, vmax):
    rb = RB(I)
    trees = rb.all_trees()
    if not trees: continue
    for s in rng.sample(trees, min(60, len(trees))):
        sigma = dict(zip(rb.X, s))
        pts0 = {}
        for x, t in sigma.items(): pts0.setdefault(t, []).append(x)
        twos = [t for t in pts0 if len(pts0[t]) == 2]
        for t in twos:
            for x_in in pts0[t]:
                pts = {k: list(v) for k, v in pts0.items()}
                sg = dict(sigma)
                tt, xi = t, x_in
                faces = [tt]; points = []
                while True:
                    y = [p for p in pts[tt] if p != xi][0]
                    (t2,) = rb.move_target(sg, y)
                    load2 = len(pts.get(t2, []))
                    sg[y] = t2; pts[tt].remove(y); pts.setdefault(t2, []).append(y)
                    faces.append(t2); points.append(y)
                    if load2 == 0: break
                    tt, xi = t2, y
                cnt['walks'] += 1
                cnt['face_revisit'] += (len(set(faces)) < len(faces))
                cnt['point_revisit'] += (len(set(points)) < len(points))
                cnt['maxlen'] = max(cnt['maxlen'], len(points))
                cnt['maxlen_minus_n'] = max(cnt.get('maxlen_minus_n', -99), len(points) - I.n)
                if len(set(faces)) < len(faces) and shown < 3:
                    shown += 1; print('revisit', V, idx, f0, [list(I.faces[f]) for f in faces], points)
print(dict(cnt))
