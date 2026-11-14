"""E9: smallest deep traps and alternative potential m(s) = #nonroots not reaching a root
under the Q-map.  Saves first deep trap per V to data/deeptrap_V.json.
Usage: python exp_traps2.py Vlist trials steps seed"""
import sys, random, json
from pairs import *
from exp_traps import kq, all_mates, best_move

def mval(R, r, s):
    f = fmap(R, r, s)
    Xs = set(R.X)
    good = set(R.R)
    m = 0
    for x in R.X:
        path = []
        y = x
        seen = set()
        while y in Xs and y not in seen and y not in good:
            seen.add(y); y = f[y]
        if y in good:
            pass
        else:
            m += 1
    return m

Vs = [int(v) for v in sys.argv[1].split(",")]
trials, steps, seed = map(int, sys.argv[2:5])
rng = random.Random(seed)
for V in Vs:
    sampled = dtrap = mtrap = 0
    saved = False
    for trial in range(trials):
        T = random_eulerian_fast(V, rng)
        faces = T.faces(); rng.shuffle(faces)
        R = next((Rooted(T, f) for f in faces if not Rooted(T, f).black_inner_sep_triangles()), None)
        if R is None:
            continue
        r, s = flow_pair(R)
        for step in range(steps):
            k = kq(R, r, s)
            if k > 0:
                sampled += 1
                mates = all_mates(R, r, s)
                if all(best_move(R, r2, s)[0] >= k for r2 in mates):
                    dtrap += 1
                    m = mval(R, r, s)
                    mbest = min(mval(R, *d_swap(R, r2, s, Dc)) for r2 in mates for Dc in dcycles(R, r2, s))
                    mtrap += (mbest >= m)
                    if not saved:
                        json.dump({"rot": {str(a): b for a, b in T.rot.items()}, "t0": R.t0,
                                   "r": [[list(t), r[t]] for t in R.A], "s": [[list(t), s[t]] for t in R.A]},
                                  open(f"data/deeptrap_{V}.json", "w"))
                        saved = True
            if rng.random() < 0.3:
                qcs = fcycles(R, fmap(R, r, s))
                if qcs:
                    r, s = q_reverse(R, r, s, rng.choice(qcs)); continue
            r, s = d_swap(R, r, s, rng.choice(dcycles(R, r, s)))
    print(f"V={V}: sampled {sampled}, deep traps {dtrap}, of which also m-traps {mtrap}", flush=True)
