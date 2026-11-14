"""Referee checks of PROOFS.md (Opus two-tree packing). Own code.
Usage: python check_packing.py <task> <Vmin> <Vmax> [extra]
 L12   Lemma 1.2 for every vertex set U, every rooting (numpy over all 2^V sets)
 PACK  Thm 2.1 (W side, Nash-Williams checked directly on W), Prop 2.3, Thm 2.7 (T/R side),
       Thm 3.3 (two point-rainbow trees), Cor 3.2(a)(b), Cor 2.6, on pair supports and random maps
 BAD   2-factors (pair supports) containing no good state
"""
import sys, json, time, itertools, random
from collections import Counter
import numpy as np
from core import all_rooted, plantri, Tri, Rooted, UF
import rb


def task_L12(Vmin, Vmax):
    out = Counter()
    worst = {}
    for V in range(Vmin, Vmax + 1):
        masks = np.arange(1, 1 << V, dtype=np.int64)
        bits = ((masks[:, None] >> np.arange(V)) & 1).astype(np.int8)
        size = bits.sum(1).astype(np.int64)
        for idx, rot in enumerate(plantri(V)):
            tri = Tri(rot)
            E = np.array(tri.edges)
            e = (bits[:, E[:, 0]] & bits[:, E[:, 1]]).sum(1).astype(np.int64)
            for f0 in range(len(tri.faces)):
                R = Rooted(tri, f0)
                Fb = np.array([tri.faces[t] for t in R.black])
                b = (bits[:, Fb[:, 0]] & bits[:, Fb[:, 1]] & bits[:, Fb[:, 2]]).sum(1).astype(np.int64)
                r = np.array(sorted(R.R))
                rho = bits[:, r].sum(1).astype(np.int64)
                lhs = e - b + np.maximum(0, rho - 1)
                slack = 2 * size - 2 - lhs
                bi = R.has_black_inner()
                ms = int(slack.min())
                out[f'V={V},black_inner={bi},min_slack={ms}'] += 1
                # (3.2): U containing R
                full = rho == 3
                ms32 = int((2 * size - 4 - (e - b))[full].min())
                out[f'black_inner={bi},min_slack_32={ms32}'] += 1
                if bi:
                    # where is the violation? check it is at the outside of a black-inner triangle
                    viol = masks[slack < 0]
                    outs = set()
                    for s in R.separating_triangles():
                        if s[3]:
                            m = sum(1 << v for v in range(V) if v not in s[1])
                            outs.add(m)
                    ok = all(int(m) in outs or True for m in viol)
                    out['bi_violating_sets'] += len(viol)
                    out['bi_violating_sets_that_are_triangle_outsides'] += sum(1 for m in viol if int(m) in outs)
        print(V, flush=True)
    return {'counts': dict(out)}


def nw_ok(nv, edges, k):
    """Nash-Williams covering condition: every nonempty vertex set S spans at most k(|S|-1) edges."""
    if not edges:
        return True
    E = np.array(edges)
    masks = np.arange(1, 1 << nv, dtype=np.int64)
    bits = ((masks[:, None] >> np.arange(nv)) & 1).astype(np.int8)
    inside = (bits[:, E[:, 0]] & bits[:, E[:, 1]]).sum(1)
    return bool((inside <= k * (bits.sum(1) - 1)).all())


def split_two_trees(nv, edges):
    """Explicit split of a multigraph's edge list into two forests (matroid intersection on
    two copies vs. the partition 'each edge used once'). Returns the two lists or None."""
    E = [(i, c) for i in range(len(edges)) for c in (0, 1)]

    def ind1(S):
        ufs = [UF(nv), UF(nv)]
        for i, c in S:
            if not ufs[c].union(*edges[i]):
                return False
        return True

    def ind2(S):
        ids = [i for i, _ in S]
        return len(ids) == len(set(ids))
    I = rb.matroid_intersection(E, ind1, ind2)
    if len(I) < len(edges):
        return None
    return [[edges[i] for i, c in I if c == cc] for cc in (0, 1)]


def support_spokes(R, u):
    return [(t, v) for t in R.A for v in R.T.faces[t] if v != u[t]]


def W_edges(R, spokes):
    return [R.wedge(t, v) for (t, v) in spokes]


def TR_edges(R, u):
    """Kept edges of T/R: in each t in A, the two edges at u(t). Roots -> one vertex."""
    idx = {x: i for i, x in enumerate(R.X)}
    rho = len(R.X)
    m = lambda v: idx.get(v, rho)
    out = []
    for t in R.A:
        a = u[t]
        for v in R.T.faces[t]:
            if v != a:
                out.append((m(a), m(v)))
    return out


def task_PACK(Vmin, Vmax, nrand=10, seed=1):
    rng = random.Random(seed)
    out = Counter()
    for V in range(Vmin, Vmax + 1):
        for idx, f0, R in all_rooted(V):
            bi = R.has_black_inner()
            nW = len(R.white)
            F2s = R.two_factors() if not bi else []
            pair = bool(F2s)
            assert pair == (not bi)
            # Cor 2.6: W minus the triangle of t0 is three spanning trees
            We = W_edges(R, [(t, v) for t in R.A for v in R.T.faces[t]])
            out[f'cor2.6_pair={pair}_ok={nw_ok(nW, We, 3)}'] += 1
            maps = [('pair', u) for u in F2s]
            for _ in range(nrand):
                maps.append(('rand', {t: rng.choice(R.T.faces[t]) for t in R.A}))
            if bi:
                # Prop 2.3 maps: on each black-inner triangle put u(t_i) on the triangle
                for s in R.separating_triangles():
                    if s[3]:
                        for _ in range(3):
                            u = {t: rng.choice(R.T.faces[t]) for t in R.A}
                            for ti in s[2]:
                                u[ti] = rng.choice([v for v in R.T.faces[ti] if v in s[0]])
                            maps.append(('prop2.3', u))
            for kind, u in maps:
                sp = support_spokes(R, u)
                wok = nw_ok(nW, W_edges(R, sp), 2)
                tok = nw_ok(len(R.X) + 1, TR_edges(R, u), 2)
                out[f'{kind}_pair={pair}_W2trees={wok}_TR2trees={tok}'] += 1
                if kind == 'rand' and bi:
                    # 'only if' of Prop 2.3 (author: computed only)
                    trap = any(s[3] and all(u[ti] in s[0] for ti in s[2]) for s in R.separating_triangles())
                    out[f'rand_bi_fail={not wok}_triangle_pattern={trap}'] += 1
                if kind == 'prop2.3':
                    assert not wok
            # explicit splits on a few pair supports, re-verified as spanning trees of W
            for u in F2s[:2]:
                sp = support_spokes(R, u)
                sl = split_two_trees(nW, W_edges(R, sp))
                assert sl is not None and all(len(x) == nW - 1 for x in sl)
                out['explicit_W_split'] += 1
            # Thm 3.3 and Cor 3.2 inside each pair support (brute force over 2^n)
            for u in F2s:
                fac = {x: [t for t in R.bat[x] if t in u and u[t] != x] for x in R.X}
                both = 0; one = 0
                for bits in itertools.product((0, 1), repeat=R.n):
                    sig = {x: fac[x][b] for x, b in zip(R.X, bits)}
                    if rb.is_rainbow(R, sig):
                        one += 1
                        sp2 = {x: fac[x][1 - b] for x, b in zip(R.X, bits)}
                        if rb.is_rainbow(R, sp2):
                            both += 1
                out[f'thm3.3_split_exists={both > 0}'] += 1
                out[f'cor3.2b_point_rainbow_exists={one > 0}'] += 1
                # Cor 3.2(a): face-rainbow tree inside the support
                cher = [[v for v in R.T.faces[t] if v != u[t]] for t in R.A]
                fa = any(R.H_minus_is_tree(list(zip(R.A, ch))) for ch in itertools.product(*cher))
                out[f'cor3.2a_face_rainbow_exists={fa}'] += 1
        print(V, dict(out), flush=True)
    return {'counts': dict(out)}


def states_in_support(R, u):
    """The 2^c states inside the 2-factor u (alternating halves of its cycles)."""
    nb = {}
    for t in R.A:
        for v in R.T.faces[t]:
            if v != u[t]:
                nb.setdefault(('f', t), []).append(('v', v))
                nb.setdefault(('v', v), []).append(('f', t))
    seen = set(); cycles = []
    for t in R.A:
        if ('f', t) in seen:
            continue
        cyc = []; a = ('f', t); prev = None
        while True:
            seen.add(a); cyc.append(a)
            nx = [b for b in nb[a] if b != prev]
            prev, a = a, nx[0]
            if a == ('f', t):
                break
        cycles.append(cyc)
    res = []
    for ori in itertools.product((0, 1), repeat=len(cycles)):
        s = {}
        for cyc, o in zip(cycles, ori):
            L = len(cyc)
            for i in range(0, L, 2):
                s[cyc[i][1]] = cyc[(i + 1) % L][1] if o == 0 else cyc[(i - 1) % L][1]
        res.append(s)
    return res, len(cycles)


def task_BAD(Vmin, Vmax, only_idx=None):
    out = Counter(); ex = []
    for V in range(Vmin, Vmax + 1):
        for idx, rot in enumerate(plantri(V)):
            if only_idx is not None and idx != only_idx:
                continue
            tri = Tri(rot)
            for f0 in range(len(tri.faces)):
                R = Rooted(tri, f0)
                if R.has_black_inner():
                    continue
                for u in R.two_factors():
                    sts, c = states_in_support(R, u)
                    assert len(sts) == 2 ** c
                    for s in sts:
                        assert len(set(s.values())) == R.n and all(s[t] in R.T.faces[t] for t in R.A)
                    g = sum(1 for s in sts if R.is_good_state(s))
                    out['supports'] += 1
                    if g == 0:
                        out['supports_without_good_state'] += 1
                        ex.append({'V': V, 'plantri_index': idx, 'outer_face': list(tri.faces[f0]),
                                   'cycles': c, 'u': {str(list(tri.faces[t])): u[t] for t in R.A}})
        print(V, dict(out), flush=True)
    return {'counts': dict(out), 'examples': ex[:20]}


if __name__ == '__main__':
    task, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    t = time.time()
    if task == 'BAD' and len(sys.argv) > 4:
        res = task_BAD(a, b, int(sys.argv[4]))
    else:
        res = {'L12': task_L12, 'PACK': task_PACK, 'BAD': task_BAD}[task](a, b)
    res['command'] = 'python check_packing.py ' + ' '.join(sys.argv[1:])
    res['seconds'] = round(time.time() - t, 1)
    suffix = '_'.join(sys.argv[2:])
    json.dump(res, open(f'../data/{task}_{suffix}.json', 'w'), indent=1)
    print(json.dumps(res['counts'], indent=1), res['seconds'])
