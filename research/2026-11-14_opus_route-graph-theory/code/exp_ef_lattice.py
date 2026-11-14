"""E20: 'every 2-factor contains a tree pair', sampling 2-factors by BFS over face flips of
the alpha-orientation lattice from the flow 2-factor (cap N nodes).
Usage: python exp_ef_lattice.py V trials seed [N] [cmax]"""
import sys, random, json
from pairs import *
from alpha import u_of, pairs_of_factor, face_data

V, trials, seed = map(int, sys.argv[1:4])
N = int(sys.argv[4]) if len(sys.argv) > 4 else 300
cmax = int(sys.argv[5]) if len(sys.argv) > 5 else 14
rng = random.Random(seed)
tot = bad = skipped = 0
sizes = []
for trial in range(trials):
    T = random_eulerian_fast(V, rng)
    faces = T.faces(); rng.shuffle(faces)
    R = next((Rooted(T, f) for f in faces if not Rooted(T, f).black_inner_sep_triangles()), None)
    if R is None:
        continue
    r, s = flow_pair(R)
    u0 = u_of(R, r, s)
    fd = face_data(R)
    seen = {frozenset(u0.items())}
    queue = [u0]
    while queue and len(seen) < N:
        u = queue.pop(0)
        for y, sides in fd:
            for k in (0, 1):
                if all(u[t] == (a if k == 0 else b) for (t, a, b) in sides):
                    u2 = dict(u)
                    for (t, a, b) in sides:
                        u2[t] = b if k == 0 else a
                    key = frozenset(u2.items())
                    if key not in seen:
                        seen.add(key); queue.append(u2)
    sizes.append(len(seen))
    for key in seen:
        u = dict(key)
        prs = pairs_of_factor(R, u)
        r1, s1 = next(prs)
        c = len(dcycles(R, r1, s1))
        if c > cmax:
            skipped += 1; continue
        tot += 1
        if not any(R.is_tree_matching(s2) for r2, s2 in pairs_of_factor(R, u)):
            bad += 1
            if bad == 1:
                json.dump({"rot": {str(k): v for k, v in T.rot.items()}, "t0": R.t0,
                           "u": [[list(t), u[t]] for t in R.A]}, open(f"data/ef_fail_{V}_{seed}.json", "w"))
print(f"V={V}: lattice sizes {sorted(sizes)[-5:]} (max of {len(sizes)}), 2-factors tested {tot}, without tree pair {bad}, skipped {skipped}", flush=True)
