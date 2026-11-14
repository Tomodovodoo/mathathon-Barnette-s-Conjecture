"""Contractions where T/M has tree matchings but none lifts directly (refutes S2 of
route-induction at V = 18). For each such case: does some TM lift-or-rotate, is T free of
separating triangles, is the contraction simple, how many TMs.
usage: python nolift.py V OUT.jsonl"""
import sys, json
import et
from census import pattern_leaves, forest_adj, comp_without

nv = int(sys.argv[1])
out = open(sys.argv[2], "w")
stats = dict(V=nv, contractions_with_TM=0, no_direct_lift=0, no_lift_or_rotation=0,
             no_direct_lift_T_4connected=0)
for gid, rot in enumerate(et.plantri(nv)):
    for blacks, ri, whites in et.rooted_instances(rot):
        t0 = blacks[ri]
        nosep = None
        for (x, a, v1, b, v2) in et.degree4_setups(blacks, whites, t0):
            nb = (a, v1, b, v2)
            outer, leaves = pattern_leaves(blacks, ri, nv, x, nb, want_assign=True)
            idx = {u: nb.index(u) for u in nb}
            for (A_, V1, B_, V2) in ((a, v1, b, v2), (v1, a, v2, b)):
                tmc = lifts = rots = exc = tmT = 0
                fails = []
                for (m, c, assign) in leaves:
                    ca, cv1, cb, cv2 = c[idx[A_]], c[idx[V1]], c[idx[B_]], c[idx[V2]]
                    is_tm = (m in (V2, B_) and ca != cv1) or (m in (V1, A_) and cb != cv2)
                    tmT += is_tm
                    if m in (V1, V2) and cv1 != cv2:
                        tmc += 1
                        if is_tm:
                            lifts += 1
                        else:
                            fails.append((m, assign))
                if tmc == 0:
                    continue
                stats["contractions_with_TM"] += 1
                if lifts:
                    continue
                for (m, assign) in fails:
                    if m == V2:
                        aa, vv1, bb, vv2 = A_, V1, B_, V2
                    else:
                        aa, vv1, bb, vv2 = B_, V2, A_, V1
                    g = next(f for f in outer if aa in f and vv2 in f)
                    (cc,) = [v for v in g if v not in (aa, vv2)]
                    adj = forest_adj(outer, assign, t0, nv)
                    if bb in comp_without(adj, vv2, (vv2, cc)):
                        exc += 1
                    else:
                        rots += 1
                if nosep is None:
                    nosep = not et.separating_triangles(blacks, whites, t0)
                stats["no_direct_lift"] += 1
                stats["no_direct_lift_T_4connected"] += nosep
                stats["no_lift_or_rotation"] += (rots == 0)
                out.write(json.dumps(dict(V=nv, gid=gid, t0=list(t0), x=x, merge=[V1, V2],
                                          others=[A_, B_], TM_T=tmT, TM_contraction=tmc,
                                          lifts=0, rotations_ok=rots, exceptions=exc,
                                          T_has_no_separating_triangle=bool(nosep),
                                          rootnbrs=[v for v in nb if v in t0],
                                          rot=["".join(chr(97 + u) for u in r) for r in rot])) + "\n")
print(json.dumps(stats))
