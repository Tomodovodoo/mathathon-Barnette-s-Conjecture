"""Checks  #TM(T) >= #TM(T/M) + #TM(T/N) - |E_M| - |E_N|  and |E_M| = |E_N| for every
root and every non-root degree-4 vertex (RESIDUAL-CASES.md, Theorem 4).
usage: python superadd.py VMIN VMAX OUT.json"""
import sys, json
import et
from census import pattern_leaves, forest_adj, comp_without

vmin, vmax, outp = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
res = {}
for nv in range(vmin, vmax + 1):
    S = dict(V=nv, vertex_root_pairs=0, EM_ne_EN=0, superadd_fail=0, superadd_tight=0,
             exceptions_with_one_contraction_TM_free=0, all_TMs_exceptional=0,
             two_sided_pairs=0, max_exception_fraction=0.0)
    for gid, rot in enumerate(et.plantri(nv)):
        for blacks, ri, whites in et.rooted_instances(rot):
            t0 = blacks[ri]
            for (x, a, v1, b, v2) in et.degree4_setups(blacks, whites, t0):
                nb = (a, v1, b, v2)
                outer, leaves = pattern_leaves(blacks, ri, nv, x, nb, want_assign=True)
                tm = 0
                tmc = [0, 0]
                exc = [0, 0]
                for (m, c, assign) in leaves:
                    ca, cv1, cb, cv2 = c
                    is_tm = (m in (v2, b) and ca != cv1) or (m in (v1, a) and cb != cv2)
                    tm += is_tm
                    for k, (A_, V1, B_, V2, sep) in enumerate(((a, v1, b, v2, cv1 != cv2),
                                                                (v1, a, v2, b, ca != cb))):
                        if m in (V1, V2) and sep:
                            tmc[k] += 1
                            if not is_tm:
                                if m == V2:
                                    aa, vv1, bb, vv2 = A_, V1, B_, V2
                                else:
                                    aa, vv1, bb, vv2 = B_, V2, A_, V1
                                g = next(f for f in outer if aa in f and vv2 in f)
                                (cc,) = [v for v in g if v not in (aa, vv2)]
                                adj = forest_adj(outer, assign, t0, nv)
                                if bb in comp_without(adj, vv2, (vv2, cc)):
                                    exc[k] += 1
                S["vertex_root_pairs"] += 1
                S["EM_ne_EN"] += exc[0] != exc[1]
                S["superadd_fail"] += tm < tmc[0] + tmc[1] - exc[0] - exc[1]
                S["superadd_tight"] += (tm == tmc[0] + tmc[1] - exc[0] - exc[1]) and exc[0] > 0
                if tmc[0] and tmc[1]:
                    S["two_sided_pairs"] += 1
                    S["max_exception_fraction"] = max(S["max_exception_fraction"],
                                                      exc[0] / tmc[0], exc[1] / tmc[1])
                    if exc[0] == tmc[0] and exc[1] == tmc[1]:
                        S["all_TMs_exceptional"] += 1
                elif exc[0] or exc[1]:
                    S["exceptions_with_one_contraction_TM_free"] += 1
    res[nv] = S
    print(json.dumps(S), flush=True)
json.dump(res, open(outp, "w"), indent=1)
