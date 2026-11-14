"""Referee checks of RAINBOW.md (Fable). Usage: python check_rainbow.py <task> <Vmin> <Vmax>
Tasks: R (Theorem R, identity (R), Lemma R2), S (Lemma X1, Theorem S, Prop U, involutions,
strict descent, Step X, M-convexity). Output: ../data/<task>_<Vmin>_<Vmax>.json
"""
import sys, json, time, itertools, random
from collections import Counter
from core import all_rooted, UF
import rb


def comps(vs, adj):
    vs = set(vs); out = []
    while vs:
        s = vs.pop(); c = {s}; st = [s]
        while st:
            a = st.pop()
            for b in adj[a]:
                if b in vs:
                    vs.discard(b); c.add(b); st.append(b)
        out.append(c)
    return out


def task_R(Vmin, Vmax, rado_max=13):
    out = Counter()
    bad = []
    for V in range(Vmin, Vmax + 1):
        for idx, f0, R in all_rooted(V):
            out['rooted'] += 1
            bi = R.has_black_inner()
            pair = R.two_factor_exists()
            sig = rb.find_rainbow(R)
            if sig is not None:
                assert rb.is_rainbow(R, sig)
                # independent re-check through W (tree-cotree duality)
                assert R.w_is_forest([(t, x) for x, t in sig.items()])
            ex = sig is not None
            out[f'bi={bi},pair={pair},rainbow={ex}'] += 1
            if not (ex == pair == (not bi)):
                bad.append((V, idx, f0))
            # Lemma R2: face-rainbow tree
            E = [(t, v) for t in R.A for v in R.T.faces[t]]
            I = rb.matroid_intersection(E, R.w_is_forest,
                                        lambda S: len({t for t, _ in S}) == len(S))
            out['face_rainbow_exists' if len(I) == R.n else 'face_rainbow_MISSING'] += 1
            # identity (R) on all connected J
            if V <= rado_max:
                T = R.T
                X = R.X
                for m in range(1, 1 << len(X)):
                    J = {X[i] for i in range(len(X)) if m >> i & 1}
                    if len(comps(J, T.adj)) != 1:
                        continue
                    U = set(range(T.V)) - J
                    c = len(comps(U, T.adj))
                    d = 0; sg = 0
                    for (a, b), f in T.dface.items():
                        if a in U and b in U and any(z in J for z in T.faces[f]):
                            d += 1
                            sg += 1 if R.isblack[f] else -1
                    wJ = sum(1 for w in R.white if any(z in J for z in T.faces[w]))
                    lhs = wJ - len(J) - 1
                    assert 6 * lhs == 6 * (c - 1) + 3 * d - sg - 12, (V, idx, f0, J)
                    out['rado_sets'] += 1
                    if lhs < 0:
                        out[f'rado_violation(c,d,sigma)={(c, d, sg)}'] += 1
                        # it must be the interior of a black-inner separating triangle
                        ok = any(s[3] and set(s[1]) == J for s in R.separating_triangles())
                        out['violation_is_black_inner_interior' if ok else 'violation_OTHER'] += 1
    return {'counts': dict(out), 'mismatches': bad}


def plateau_check(R, trees, keyset):
    """Step X on one instance: BFS from excess-0 trees through moves to trees of
    excess >= current. Returns (number reached, total, max plateau depth info)."""
    ex = {k: rb.excess(R, rb.unkey(R, k)) for k in trees}
    reach = {k for k in trees if ex[k] == 0}
    frontier = list(reach)
    while frontier:
        nxt = []
        for k in frontier:
            sig = rb.unkey(R, k)
            adj = rb.tree_adj(R, sig)
            for i, x in enumerate(R.X):
                t2 = rb.alt(R, sig, x, adj)
                k2 = k[:i] + (t2,) + k[i + 1:]
                if k2 not in reach and ex[k2] >= ex[k]:
                    reach.add(k2); nxt.append(k2)
        frontier = nxt
    return len(reach), len(trees)


def is_M_convex(L):
    Ls = set(L)
    for x in L:
        for y in L:
            for i in range(len(x)):
                if x[i] > y[i]:
                    ok = False
                    for j in range(len(x)):
                        if x[j] < y[j]:
                            xm = list(x); xm[i] -= 1; xm[j] += 1
                            yp = list(y); yp[i] += 1; yp[j] -= 1
                            if tuple(xm) in Ls and tuple(yp) in Ls:
                                ok = True; break
                    if not ok:
                        return False, (x, y, i)
    return True, None


def task_S(Vmin, Vmax, mconv_max=12):
    out = Counter()
    examples = {}
    for V in range(Vmin, Vmax + 1):
        for idx, f0, R in all_rooted(V):
            if R.has_black_inner():
                continue
            out['instances_with_rainbow'] += 1
            trees = rb.all_rainbow(R)
            keys = [rb.key(R, s) for s in trees]
            keyset = set(keys)
            out['rainbow_trees'] += len(trees)
            F2s = R.two_factors()
            out[f'n2f={min(len(F2s), 3)}'] += 1
            # Lemma X1 by brute force + move = alt
            for sig in trees:
                k = rb.key(R, sig)
                adj = rb.tree_adj(R, sig)
                for i, x in enumerate(R.X):
                    good = [t for t in R.bat[x] if t != sig[x]
                            and (k[:i] + (t,) + k[i + 1:]) in keyset]
                    assert len(good) == 1, 'X1 fails'
                    assert good[0] == rb.alt(R, sig, x, adj)
                out['X1_points_checked'] += len(R.X)
            # Theorem S (1), (2): parent map completes sigma to the unique 2-factor
            for sig in trees:
                adj = rb.tree_adj(R, sig)
                root = R.cidx[R.t0]
                par = {root: None}; st = [root]
                while st:
                    a = st.pop()
                    for b in adj[a]:
                        if b not in par:
                            par[b] = a; st.append(b)
                assert len(par) == R.NH
                parx = {x: R.black[par[x] - R.T.V] for x in R.X}
                deg = Counter(list(sig.values()) + list(parx.values()))
                assert all(parx[x] != sig[x] for x in R.X)
                assert all(deg[t] == 2 for t in R.A)
                cont = [u for u in F2s if all(u[sig[x]] != x for x in R.X)]
                assert len(cont) == 1
                u = cont[0]
                assert all(u[parx[x]] != x for x in R.X)
                out['S12_checked'] += 1
            # Theorem S (3), Prop U, good states: per 2-factor, all 2^n selections
            nr = 0
            for u in F2s:
                fac = {x: [t for t in R.bat[x] if t in u and u[t] != x] for x in R.X}
                assert all(len(fac[x]) == 2 for x in R.X)
                for bits in itertools.product((0, 1), repeat=R.n):
                    sig = {x: fac[x][b] for x, b in zip(R.X, bits)}
                    sp = {x: fac[x][1 - b] for x, b in zip(R.X, bits)}
                    # arcs x -> u(sigma'(x)); acyclic?
                    nxt = {x: u[sp[x]] for x in R.X}
                    acyc = True
                    for x in R.X:
                        seen = set(); y = x
                        while y in nxt and y not in seen:
                            seen.add(y); y = nxt[y]
                        if y in nxt:
                            acyc = False; break
                    tr = rb.key(R, sig) in keyset
                    assert acyc == tr, 'S3 fails'
                    nr += tr
                    if tr and rb.excess(R, sig) == 0:
                        assert R.is_good_state({t: x for x, t in sig.items()})
                # Prop U: G_u has a directed cycle iff another 2-factor exists
                arcs = {x: [u[t] for t in fac[x]] for x in R.X}
                color = {}

                def dfs(a):
                    color[a] = 1
                    for b in arcs.get(a, []):
                        if color.get(b) == 1:
                            return True
                        if b not in color and dfs(b):
                            return True
                    color[a] = 2
                    return False
                cyc = any(dfs(x) for x in R.X if x not in color)
                assert cyc == (len(F2s) > 1), 'Prop U fails'
            assert nr == len(trees), 'rainbow trees not partitioned by 2-factors'
            if len(F2s) == 1:
                assert len(trees) == 2 ** R.n
            # good states and Fable's involutions
            goods = [s for s in R.states() if R.is_good_state(s)]
            gk = {tuple(s[t] for t in R.A) for s in goods}
            assert len(goods) == sum(1 for s in trees if rb.excess(R, s) == 0)
            out['good_states'] += len(goods)
            out['good_count_even' if len(goods) % 2 == 0 else 'good_count_ODD'] += 1
            for s in goods:
                for t in R.A:
                    s2 = rb.iota(R, s, t)
                    k2 = tuple(s2[a] for a in R.A)
                    assert k2 in gk and s2 != s
                    assert rb.iota(R, s2, t) == s
                    out['iota_checked'] += 1
            # strict descent
            for sig in trees:
                e = rb.excess(R, sig)
                if e == 0:
                    continue
                k = rb.key(R, sig)
                adj = rb.tree_adj(R, sig)
                dec = False
                for i, x in enumerate(R.X):
                    t2 = rb.alt(R, sig, x, adj)
                    if rb.excess(R, rb.unkey(R, k[:i] + (t2,) + k[i + 1:])) < e:
                        dec = True; break
                if not dec:
                    out['no_decreasing_move'] += 1
                    if 'strict_descent_fails' not in examples:
                        examples['strict_descent_fails'] = {
                            'V': V, 'plantri_index': idx, 'outer_face': list(R.T.faces[f0]),
                            'rot': R.T.rot, 'sigma': {str(x): list(R.T.faces[t]) for x, t in sig.items()},
                            'excess': e}
            # Step X
            reached, total = plateau_check(R, keys, keyset)
            out['stepX_ok' if reached == total else 'stepX_TRAP'] += 1
            # M-convexity of load vectors
            if V <= mconv_max:
                L = sorted({tuple(rb.loads(R, s)[t] for t in R.A) for s in trees})
                ok, wit = is_M_convex(L)
                out[f'Mconvex={ok},n2f>1={len(F2s) > 1}'] += 1
                if not ok and 'M_convex_fails' not in examples:
                    examples['M_convex_fails'] = {'V': V, 'plantri_index': idx,
                                                  'outer_face': list(R.T.faces[f0]),
                                                  'faces_A': [list(R.T.faces[t]) for t in R.A],
                                                  'x': wit[0], 'y': wit[1], 'i': wit[2]}
        print(V, dict(out), flush=True)
    return {'counts': dict(out), 'examples': examples}


if __name__ == '__main__':
    task, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    t = time.time()
    res = {'R': task_R, 'S': task_S}[task](a, b)
    res['command'] = 'python check_rainbow.py ' + ' '.join(sys.argv[1:])
    res['seconds'] = round(time.time() - t, 1)
    json.dump(res, open(f'../data/{task}_{a}_{b}.json', 'w'), indent=1)
    print(json.dumps(res['counts'], indent=1))
    print('mismatches/examples:', {k: v for k, v in res.items() if k in ('mismatches',)}, res['seconds'])
