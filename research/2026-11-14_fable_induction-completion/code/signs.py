"""Signs eps(r_s, s) of the tree matchings of T/M by lift class.
usage: python signs.py VMIN VMAX
Classes of a tree matching s' of T/M (outer state with m in {v1, v2}, v1 | v2 separated):
  L  lift is a TM of T
  R  lift fails, rotation is a TM of T
  E  lift fails, rotation fails (pattern P_1 before and after)
Also split by pattern P1 = {a v1 | b v2} or not."""
import sys, collections
import et
from census import pattern_leaves, forest_adj, comp_without


def mate_sign(faces, assign, t0, nv):
    """eps = prod_t delta(r(t), s(t)) for the unique mate r of the tree matching given by
    faces/assign (faces oriented triples). r(t) = tail of the Q-edge of t when the tree is
    oriented towards the root path."""
    adj = [[] for _ in range(nv)]
    for i, (f, u) in enumerate(zip(faces, assign)):
        p, q = [v for v in f if v != u]
        adj[p].append((q, i)); adj[q].append((p, i))
    par_face = {}
    seen = set(t0)
    stack = list(t0)
    while stack:
        y = stack.pop()
        for z, i in adj[y]:
            if z not in seen:
                seen.add(z); par_face[z] = i; stack.append(z)
    r = [None] * len(faces)
    for z, i in par_face.items():
        assert r[i] is None
        r[i] = z
    eps = 1
    for f, u, rr in zip(faces, assign, r):
        assert rr is not None and rr != u
        j = f.index(rr)
        eps *= 1 if f[(j + 1) % 3] == u else -1
    return eps


def main():
    vmin, vmax = int(sys.argv[1]), int(sys.argv[2])
    tot = collections.Counter()
    for nv in range(vmin, vmax + 1):
        for gid, rot in enumerate(et.plantri(nv)):
            for blacks, ri, whites in et.rooted_instances(rot):
                t0 = blacks[ri]
                for (x, a, v1, b, v2) in et.degree4_setups(blacks, whites, t0):
                    nb = (a, v1, b, v2)
                    outer, leaves = pattern_leaves(blacks, ri, nv, x, nb, want_assign=True)
                    for (A_, V1, B_, V2) in ((a, v1, b, v2), (v1, a, v2, b)):
                        idx = {u: nb.index(u) for u in nb}
                        res = et.contract(blacks, ri, x, V1, V2)
                        if res is None:
                            continue
                        keep = V2 if V2 in t0 else V1
                        drop = V1 if keep == V2 else V2
                        cls = collections.Counter()
                        for (m, c, assign) in leaves:
                            if m not in (V1, V2):
                                continue
                            ca, cv1, cb, cv2 = c[idx[A_]], c[idx[V1]], c[idx[B_]], c[idx[V2]]
                            if cv1 == cv2:
                                continue
                            # sign in T/M: relabel drop -> keep in the outer faces
                            f2 = [tuple(keep if v == drop else v for v in f) for f in outer]
                            as2 = [keep if u == drop else u for u in assign]
                            tt0 = tuple(keep if v == drop else v for v in t0)
                            eps = mate_sign(f2, as2, tt0, nv)
                            is_tm = (m == V2 and ca != cv1) or (m == V1 and cb != cv2)
                            p1 = (ca == cv1 and cb == cv2)
                            if is_tm:
                                k = 'L'
                            else:
                                if m == V2:
                                    aa, vv1, bb, vv2 = A_, V1, B_, V2
                                else:
                                    aa, vv1, bb, vv2 = B_, V2, A_, V1
                                g = next(f for f in outer if aa in f and vv2 in f)
                                (cc,) = [v for v in g if v not in (aa, vv2)]
                                adj = forest_adj(outer, assign, t0, nv)
                                K2p = comp_without(adj, vv2, (vv2, cc))
                                k = 'E' if bb in K2p else 'R'
                            cls[(k, p1, eps)] += 1
                        if not cls:
                            continue
                        e_signs = {e for (k, p1, e) in cls if k == 'E'}
                        p1sum = sum(e * n for (k, p1, e), n in cls.items() if p1)
                        p1n = sum(n for (k, p1, e), n in cls.items() if p1)
                        esum = sum(e * n for (k, p1, e), n in cls.items() if k == 'E')
                        en = sum(n for (k, p1, e), n in cls.items() if k == 'E')
                        allsum = sum(e * n for (k, p1, e), n in cls.items())
                        tot['instances with TM'] += 1
                        tot['sum eps != 0'] += allsum != 0
                        if p1n:
                            tot['inst with P1'] += 1
                            tot['P1 sign-balanced'] += (p1sum == 0)
                            tot['P1 all same sign'] += (abs(p1sum) == p1n)
                        if en:
                            tot['inst with E'] += 1
                            tot['E all same sign'] += (abs(esum) == en)
                            tot['E mixed'] += (abs(esum) != en)
                            tot['inst with >=2 E'] += en >= 2
                            tot['E>=2 all same sign'] += (en >= 2 and abs(esum) == en)
                            nonE = sum(n for (k, p1, e), n in cls.items() if k != 'E')
                            tot['E-inst: all TMs are E'] += nonE == 0
        print(nv, dict(tot), flush=True)


main()
