"""E8: weak descent (trap) test on random instances.
At sampled pairs (r,s) with k(s)>0:
  weak trap  : no D(r,s)-cycle swap decreases k (current mate only);
  deep trap  : for no mate r' of s (2^k of them) does some D(r',s)-cycle swap decrease k.
Usage: python exp_traps.py V trials steps seed"""
import sys, random, itertools
from pairs import *

def kq(R, r, s):
    return len(fcycles(R, fmap(R, r, s)))

def all_mates(R, r, s):
    qcs = fcycles(R, fmap(R, r, s))
    out = []
    for mask in itertools.product((0, 1), repeat=len(qcs)):
        r2 = r
        for b, c in zip(mask, qcs):
            if b:
                r2, _ = q_reverse(R, r2, s, c)
        out.append(r2)
    return out

def best_move(R, r, s):
    k = kq(R, r, s)
    best = None
    for Dc in dcycles(R, r, s):
        r2, s2 = d_swap(R, r, s, Dc)
        k2 = kq(R, r2, s2)
        if best is None or k2 < best[0]:
            best = (k2, r2, s2)
    return best

if __name__ == "__main__":
    V, trials, steps, seed = map(int, sys.argv[1:5])
    rng = random.Random(seed)
    sampled = wtrap = dtrap = 0
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
                b = best_move(R, r, s)
                if b[0] >= k:
                    wtrap += 1
                    if wtrap == 1:
                        import json
                        json.dump({"rot": {str(a): bb for a, bb in R.T.rot.items()}, "t0": R.t0,
                                   "r": [[list(t), r[t]] for t in R.A], "s": [[list(t), s[t]] for t in R.A]},
                                  open(f"data/weaktrap_{V}_seed{seed}.json", "w"))
                    if all(best_move(R, r2, s)[0] >= k for r2 in all_mates(R, r, s)):
                        dtrap += 1
                        print("DEEP TRAP", V, R.t0, k, flush=True)
                        import json
                        json.dump({"rot": {str(a): b for a, b in R.T.rot.items()}, "t0": R.t0,
                                   "r": [[list(t), r[t]] for t in R.A], "s": [[list(t), s[t]] for t in R.A]},
                                  open(f"data/deeptrap_{V}_{dtrap}.json", "w"))
            if rng.random() < 0.3:
                qcs = fcycles(R, fmap(R, r, s))
                if qcs:
                    r, s = q_reverse(R, r, s, rng.choice(qcs))
                    continue
            r, s = d_swap(R, r, s, rng.choice(dcycles(R, r, s)))
    print(f"V={V} sampled pairs with k>0: {sampled}, weak traps: {wtrap}, deep traps: {dtrap}", flush=True)
