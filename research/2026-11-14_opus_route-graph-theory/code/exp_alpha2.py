"""E17: (a) validate flip_to_extreme against the enumerated lattice minimum (V<=Vmax_exh);
(b) random large instances: does the minimal / maximal 2-factor contain a tree pair?
Usage: python exp_alpha2.py validate Vmax | random V trials seed"""
import sys, random
from tri import load
from states import Rooted
from pairs import flow_pair, random_eulerian_fast
from alpha import u_of, flip_to_extreme, pairs_of_factor
from exp_alpha import tutte_positions

def has_tree_pair(R, u):
    return any(R.is_tree_matching(s) for r, s in pairs_of_factor(R, u))

if sys.argv[1] == "validate":
    import exp_alpha  # noqa
    for V in range(6, int(sys.argv[2]) + 1):
        ok = tot = 0
        for T in load(V):
            for f in T.faces():
                R = Rooted(T, f)
                if R.black_inner_sep_triangles():
                    continue
                P = tutte_positions(R)
                S = R.states()
                us = set()
                for s in S:
                    for r in R.mates(s):
                        u0 = u_of(R, r, s)
                        us.add(frozenset(flip_to_extreme(R, u0, +1, P).items()))
                tot += 1
                ok += (len(us) == 1) and has_tree_pair(R, dict(next(iter(us))))
        print(V, "instances", tot, "greedy min unique from every start & has tree pair:", ok, flush=True)
else:
    V, trials, seed = map(int, sys.argv[2:5])
    rng = random.Random(seed)
    stat = dict(inst=0, min_ok=0, max_ok=0, start_ok=0)
    worst = None
    for _ in range(trials):
        T = random_eulerian_fast(V, rng)
        faces = T.faces(); rng.shuffle(faces)
        R = next((Rooted(T, f) for f in faces if not Rooted(T, f).black_inner_sep_triangles()), None)
        if R is None:
            continue
        P = tutte_positions(R)
        r, s = flow_pair(R)
        u0 = u_of(R, r, s)
        umin = flip_to_extreme(R, u0, +1, P)
        umax = flip_to_extreme(R, u0, -1, P)
        stat['inst'] += 1
        a = has_tree_pair(R, umin); b = has_tree_pair(R, umax); c = has_tree_pair(R, u0)
        stat['min_ok'] += a; stat['max_ok'] += b; stat['start_ok'] += c
        stat['both_fail'] = stat.get('both_fail', 0) + ((not a) and (not b))
        if not b and not stat.get('saved_max'):
            import json
            json.dump({"rot": {str(k): v for k, v in T.rot.items()}, "t0": R.t0,
                       "u": [[list(t), umax[t]] for t in R.A]}, open(f"data/alpha_max_fail_{V}_{seed}.json", "w"))
            stat['saved_max'] = 1
        if not a and worst is None:
            import json
            json.dump({"rot": {str(k): v for k, v in T.rot.items()}, "t0": R.t0,
                       "u": [[list(t), umin[t]] for t in R.A]}, open(f"data/alpha_min_fail_{V}_{seed}.json", "w"))
            worst = True
    print(f"V={V}", stat, flush=True)
