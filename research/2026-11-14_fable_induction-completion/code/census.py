"""Referee census: reproduces (L), (G), state splitting, the pair criterion, the lift
criterion and the rotation on every rooted degree-4 contraction.

usage: python census.py VMIN VMAX OUT.json [--states VSTATES] [--exc EXC.jsonl]

For every Eulerian triangulation T (plantri -b), every face as root t0, every non-root
vertex x of degree 4 and both merges at x:

  direct     build T/M from the black faces and count its tree matchings from scratch;
  patterns   enumerate "outer states" of T - x (see below) and derive TM(T), TM(T/M)
             and the failing lifts from them; the two computations must agree.

Outer state: an injective choice of corners for the black faces not at x, missing x and
exactly one m of the four neighbours of x, such that the opposite edges plus the two
root edges form a forest F (then F has two components on T - x). The leaf data are m
and the partition of (a, v1, b, v2) into the two components.
"""
import json
import sys
import time

import et


def pattern_leaves(blacks, ri, nv, x, nbrs, want_assign=False):
    """List of (m, ca, cv1, cb, cv2[, faces, assign]) over all outer states."""
    t0 = blacks[ri]
    outer = [f for i, f in enumerate(blacks) if i != ri and x not in f]
    order = et.order_faces(outer, t0)
    outer = [outer[i] for i in order]
    pre = et.root_edges(t0)
    leaves = []
    for m in nbrs:
        if m in t0:
            continue

        def cb(assign, find, m=m):
            c = tuple(find(v) for v in nbrs)
            if want_assign:
                leaves.append((m, c, list(assign)))
            else:
                leaves.append((m, c))
        et.enum(outer, set(t0) | {x, m}, pre, nv, cb)
    return outer, leaves


def forest_adj(outer, assign, t0, nv):
    adj = [[] for _ in range(nv)]
    for f, u in zip(outer, assign):
        p, q = [v for v in f if v != u]
        adj[p].append(q)
        adj[q].append(p)
    for p, q in et.root_edges(t0):
        adj[p].append(q)
        adj[q].append(p)
    return adj


def comp_without(adj, start, cut):
    """Component of `start` after deleting the edge cut = (p, q)."""
    seen = {start}
    stack = [start]
    while stack:
        y = stack.pop()
        for z in adj[y]:
            if (y, z) == cut or (z, y) == cut:
                continue
            if z not in seen:
                seen.add(z)
                stack.append(z)
    return seen


def main():
    vmin, vmax, outpath = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    vstates = 0
    excpath = None
    args = sys.argv[4:]
    while args:
        if args[0] == "--states":
            vstates = int(args[1])
        elif args[0] == "--exc":
            excpath = args[1]
        args = args[2:]
    excf = open(excpath, "w") if excpath else None
    summary = {}
    for nv in range(vmin, vmax + 1):
        t = time.time()
        S = dict(V=nv, triangulations=0, rooted=0, rooted_with_pair=0,
                 pair_iff_TM_fail=0, criterion_fail=0, TM_odd=0,
                 contractions=0, loops=0, simple=0,
                 L_fail=0, L_fail_simple=0, pattern_vs_direct_fail=0,
                 split_checked=0, split_fail=0,
                 tm_of_contraction_positive=0, some_lift_fail=0,
                 lift_fail=0, lift_fail_simple=0,
                 local_condition_fail=0, rot_ok=0, rot_exc=0, rot_exc_simple=0,
                 rot_exc_rootfree=0, rot_criterion_fail=0,
                 nosep_rooted=0, G_fail=0, G_fail_ids=[],
                 pair_lost_simple=0, old_lemma_fail_simple=0)
        for gid, rot in enumerate(et.plantri(nv)):
            S["triangulations"] += 1
            for blacks, ri, whites in et.rooted_instances(rot):
                t0 = blacks[ri]
                S["rooted"] += 1
                tm = et.tree_matchings(blacks, ri, nv)
                pair = et.has_pair_flow(blacks, ri)
                S["rooted_with_pair"] += pair
                if (tm > 0) != pair:
                    S["pair_iff_TM_fail"] += 1
                if tm % 2:
                    S["TM_odd"] += 1
                seps = et.separating_triangles(blacks, whites, t0)
                if pair != (not any(ib for _, ib in seps)):
                    S["criterion_fail"] += 1
                nosep = not seps
                good = False
                st = et.count_states(blacks, ri, nv) if nv <= vstates else None
                for (x, a, v1, b, v2) in et.degree4_setups(blacks, whites, t0):
                    nb = (a, v1, b, v2)
                    outer, leaves = pattern_leaves(blacks, ri, nv, x, nb, want_assign=True)
                    stsum = 0
                    both = True
                    # the two merges: M = (v1, v2) in naming (a, v1, b, v2);
                    #                 N = (a, b)  in naming (v1, a, v2, b)
                    for (A_, V1, B_, V2) in ((a, v1, b, v2), (v1, a, v2, b)):
                        idx = {A_: nb.index(A_), V1: nb.index(V1), B_: nb.index(B_), V2: nb.index(V2)}
                        res = et.contract(blacks, ri, x, V1, V2)
                        if res is None:
                            S["loops"] += 1
                            both = False
                            continue
                        S["contractions"] += 1
                        cb_, cri = res
                        tmc = et.tree_matchings(cb_, cri, nv)
                        simple = et.is_simple(cb_)
                        S["simple"] += simple
                        if st is not None:
                            stsum += et.count_states(cb_, cri, nv)
                        if tm < tmc:
                            S["L_fail"] += 1
                            S["L_fail_simple"] += simple
                        # pattern side
                        p_tmc = 0
                        p_tm = 0
                        lifts = 0
                        mtype_tm = 0
                        fails = []
                        for (m, c, assign) in leaves:
                            ca, cv1, cb2, cv2 = c[idx[A_]], c[idx[V1]], c[idx[B_]], c[idx[V2]]
                            is_tm = (m in (V2, B_) and ca != cv1) or (m in (V1, A_) and cb2 != cv2)
                            p_tm += is_tm
                            if m in (V1, V2):
                                mtype_tm += is_tm
                                if cv1 != cv2:
                                    p_tmc += 1
                                    if is_tm:
                                        lifts += 1
                                    else:
                                        fails.append((m, assign))
                        if p_tmc != tmc or p_tm != tm:
                            S["pattern_vs_direct_fail"] += 1
                        if tmc > 0:
                            S["tm_of_contraction_positive"] += 1
                            if lifts == 0:
                                S["some_lift_fail"] += 1
                        if simple:
                            pc = et.has_pair_flow(cb_, cri)
                            if pair and not pc:
                                S["pair_lost_simple"] += 1
                            if pc:
                                good = True
                            if mtype_tm > lifts:
                                S["old_lemma_fail_simple"] += 1
                        S["lift_fail"] += len(fails)
                        if simple:
                            S["lift_fail_simple"] += len(fails)
                        rootnb = [v for v in nb if v in t0]
                        for (m, assign) in fails:
                            # mirror so that the missing vertex is "v2"
                            if m == V2:
                                aa, vv1, bb, vv2 = A_, V1, B_, V2
                            else:
                                aa, vv1, bb, vv2 = B_, V2, A_, V1
                            g = next(f for f in outer if aa in f and vv2 in f)
                            (cc,) = [v for v in g if v not in (aa, vv2)]
                            sg = assign[outer.index(g)]
                            if sg != aa:
                                S["local_condition_fail"] += 1
                                continue
                            adj = forest_adj(outer, assign, t0, nv)
                            K2p = comp_without(adj, vv2, (vv2, cc))
                            exc = bb in K2p
                            # independent test of the rotated state
                            new = list(assign)
                            new[outer.index(g)] = vv2
                            adj2 = forest_adj(outer, new, t0, nv)
                            # rotated: beta1 takes aa (edge x-vv1), beta2 takes x (edge bb-vv2)
                            adj2[x].append(vv1); adj2[vv1].append(x)
                            adj2[bb].append(vv2); adj2[vv2].append(bb)
                            seen = comp_without(adj2, t0[0], None)
                            nverts = len({v for f in blacks for v in f})
                            is_tree = len(seen) == nverts
                            if is_tree == exc:
                                S["rot_criterion_fail"] += 1
                            if exc:
                                S["rot_exc"] += 1
                                S["rot_exc_simple"] += simple
                                if not rootnb:
                                    S["rot_exc_rootfree"] += 1
                                if excf:
                                    excf.write(json.dumps(dict(
                                        V=nv, gid=gid, t0=list(t0), x=x, a=aa, v1=vv1, b=bb, v2=vv2,
                                        c=cc, simple=bool(simple), rootnbrs=rootnb,
                                        outer=[list(f) for f in outer], assign=assign,
                                        blacks=[list(f) for f in blacks],
                                        whites=[list(f) for f in whites])) + "\n")
                            else:
                                S["rot_ok"] += 1
                    if st is not None and both:
                        S["split_checked"] += 1
                        if st != stsum:
                            S["split_fail"] += 1
                if nosep and nv >= 8:
                    S["nosep_rooted"] += 1
                    if not good:
                        S["G_fail"] += 1
                        S["G_fail_ids"].append([gid, list(t0)])
        S["seconds"] = round(time.time() - t, 1)
        summary[nv] = S
        print(json.dumps(S), flush=True)
    json.dump(summary, open(outpath, "w"), indent=1)


if __name__ == "__main__":
    main()
