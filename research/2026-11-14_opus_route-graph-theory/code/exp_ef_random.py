"""E19: random test of 'every 2-factor of B contains an ordered tree pair'.
Random walk in the exchange graph (Q-reversals change the 2-factor, D-swaps keep it);
each new 2-factor with c <= cmax cycles is tested over all 2^c orientations.
Usage: python exp_ef_random.py V trials steps seed [cmax]"""
import sys, random, json
from pairs import *
from alpha import u_of, pairs_of_factor

V, trials, steps, seed = map(int, sys.argv[1:5])
cmax = int(sys.argv[5]) if len(sys.argv) > 5 else 14
rng = random.Random(seed)
tested = bad = skipped = 0
for trial in range(trials):
    T = random_eulerian_fast(V, rng)
    faces = T.faces(); rng.shuffle(faces)
    R = next((Rooted(T, f) for f in faces if not Rooted(T, f).black_inner_sep_triangles()), None)
    if R is None:
        continue
    r, s = flow_pair(R)
    seen = set()
    for step in range(steps):
        u = u_of(R, r, s)
        key = frozenset(u.items())
        if key not in seen:
            seen.add(key)
            c = len(dcycles(R, r, s))
            if c > cmax:
                skipped += 1
            else:
                tested += 1
                if not any(R.is_tree_matching(s2) for r2, s2 in pairs_of_factor(R, u)):
                    bad += 1
                    if bad == 1:
                        json.dump({"rot": {str(k): v for k, v in T.rot.items()}, "t0": R.t0,
                                   "r": [[list(t), r[t]] for t in R.A], "s": [[list(t), s[t]] for t in R.A]},
                                  open(f"data/ef_fail_{V}_{seed}.json", "w"))
        qcs = fcycles(R, fmap(R, r, s))
        if qcs and rng.random() < 0.6:
            r, s = q_reverse(R, r, s, rng.choice(qcs))
        else:
            r, s = d_swap(R, r, s, rng.choice(dcycles(R, r, s)))
print(f"V={V}: distinct 2-factors tested {tested}, without tree pair {bad}, skipped (c>{cmax}) {skipped}", flush=True)
