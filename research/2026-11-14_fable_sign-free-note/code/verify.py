"""Numerical check of every statement of proofs/sign-free/sign-free.tex on all rooted instances.

Usage: python verify.py VMIN VMAX [out.json]
A rooted instance is an Eulerian triangulation (plantri -b -a V) with one face chosen as t0.
Every assertion below is a statement of the note; the script stops at the first failure.
"""
import itertools
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'proofs', 'sign-free', 'figures'))
import sf  # noqa: E402

C = {}


def bump(k, v=1):
    C[k] = C.get(k, 0) + v


def split_two_trees(nv, edges):
    """Split a list of 2(nv-1) edges into two spanning trees; return a 0/1 list or None."""
    m = len(edges)
    assert m == 2 * (nv - 1)
    side = [None] * m

    def forest(k, s):
        p = list(range(nv))

        def find(a):
            while p[a] != a:
                p[a] = p[p[a]]
                a = p[a]
            return a
        for i in range(k + 1):
            if side[i] == s:
                a, b = find(edges[i][0]), find(edges[i][1])
                if a == b:
                    return False
                p[a] = b
        return True

    def rec(k, n0, n1):
        if k == m:
            return True
        for s in ((0,) if k == 0 else (0, 1)):
            if (n0 if s == 0 else n1) >= nv - 1:
                continue
            side[k] = s
            if forest(k, s) and rec(k + 1, n0 + (s == 0), n1 + (s == 1)):
                return True
            side[k] = None
        return False
    return list(side) if rec(0, 0, 0) else None


def nash_williams_violated(nv, edges, k=2):
    for mask in range(1, 1 << nv):
        cnt = sum(1 for a, b in edges if (mask >> a) & 1 and (mask >> b) & 1)
        if cnt > k * (bin(mask).count('1') - 1):
            return True
    return False


def components(inst, U):
    U = set(U)
    seen = set()
    c = 0
    for v in U:
        if v not in seen:
            c += 1
            stack = [v]
            seen.add(v)
            while stack:
                a = stack.pop()
                for b in inst.adj[a]:
                    if b in U and b not in seen:
                        seen.add(b)
                        stack.append(b)
    return c


def check_instance(inst, rng, all_u):
    n, X, A = inst.n, inst.X, inst.A
    bump('rootings')

    # ---- Section 2: duality, and good states as rainbow trees of excess 0 ----
    trees = {}
    for choice in itertools.product(*[inst.at[x] for x in X]):
        sig = dict(zip(X, choice))
        rem = [(sig[x], x) for x in X]
        a = inst.h_tree(set(rem))
        assert a == inst.w_tree(rem)                      # Lemma (duality)
        bump('maps tested for duality')
        if a:
            trees[choice] = sig
    states = inst.states()
    good = set()
    for s in states:
        inv = {s[i]: i for i in range(n)}
        k = sf.key(inst, inv)
        g = inst.good_state(s)
        assert g == (k in trees)                           # Lemma: good iff F_sigma is a tree
        if g:
            good.add(k)
    assert good == {k for k, sig in trees.items() if inst.excess(sig) == 0}
    bump('states', len(states))
    bump('good states', len(good))
    bump('rainbow trees', len(trees))

    # ---- Section 3: Step R ----
    bit = inst.black_inner_triangles()
    factors = inst.two_factors()
    assert (len(trees) > 0) == (len(bit) == 0) == (len(factors) > 0)   # Theorem R, Corollary
    bump('rootings with a rainbow tree', 1 if trees else 0)
    blackset = set(inst.black)
    viol = 0
    for r in range(1, n + 1):
        for J in itertools.combinations(X, r):
            Js = set(J)
            if components(inst, Js) != 1:
                continue
            U = [v for v in range(inst.V) if v not in Js]
            Us = set(U)
            wJ = sum(1 for f in inst.white if Js & set(f))
            c = components(inst, U)
            d = sg = 0
            for (a, b), fl in inst.edge_faces.items():
                if a in Us and b in Us:
                    for j in fl:
                        f = inst.faces[j]
                        if not set(f) <= Us:
                            d += 1
                            sg += 1 if f in blackset else -1
            lhs = wJ - len(J) - 1
            assert 6 * lhs == 6 * (c - 1) + 3 * d - sg - 12             # identity (2)
            assert d >= 3 and sg % 3 == 0 and (sg - d) % 2 == 0 and abs(sg) <= d
            bump('connected sets J')
            if lhs < 0:
                viol += 1
                assert (c, d, sg) == (1, 3, 3)
                assert any(set(inner) == Js for _, inner in bit)
    bump('sets J violating (1)', viol)
    assert (viol == 0) == (len(bit) == 0)
    for tri, inner in bit:                                                # converse count W = I
        I = len(inner)
        assert sum(1 for f in inst.white if set(f) & set(inner)) == I
    if not trees:
        return
    bump('2-factors', len(factors))
    bump('rootings with one 2-factor', 1 if len(factors) == 1 else 0)

    # ---- Section 4: Theorem S ----
    fkeys = [tuple(u[i] for i in range(n)) for u in factors]
    per_factor = {fk: 0 for fk in fkeys}
    for k, sig in trees.items():
        par = inst.parent(sig)
        cnt = [0] * n
        u = {}
        for x in X:
            assert par[x] != sig[x] and par[x] < n                        # (a)
            cnt[sig[x]] += 1
            cnt[par[x]] += 1
        assert cnt == [2] * n
        for i in range(n):
            u[i] = [v for v in A[i] if not (v in sig and sig[v] == i) and not (v in par and par[v] == i)][0]
        fk = tuple(u[i] for i in range(n))
        assert fk in per_factor
        per_factor[fk] += 1
        cont = [g for g in factors if all(g[sig[x]] != x for x in X)]
        assert len(cont) == 1                                            # exactly one 2-factor contains sigma
    for u, fk in zip(factors, fkeys):
        used = {x: [i for i in inst.at[x] if u[i] != x] for x in X}
        assert all(len(used[x]) == 2 for x in X)
        nrb = ngood = 0
        both = False
        for bits in itertools.product((0, 1), repeat=n):
            sig = {x: used[x][b] for x, b in zip(X, bits)}
            sigp = {x: used[x][1 - b] for x, b in zip(X, bits)}
            nxt = {x: u[sigp[x]] for x in X}                             # the arc x -> u(sigma'(x))
            acyc = True
            for x in X:
                y, steps = x, 0
                while y in nxt and steps <= n:
                    y = nxt[y]
                    steps += 1
                if steps > n:
                    acyc = False
                    break
            rb = sf.key(inst, sig) in trees
            assert rb == acyc                                            # (b)
            if rb:
                nrb += 1
                if sf.key(inst, sigp) in trees:
                    both = True
                onearc = sorted(sigp.values()) == list(range(n))
                assert onearc == (sf.key(inst, sig) in good)
                ngood += onearc
        assert nrb == per_factor[fk]
        assert both                                                      # Theorem (two rainbow trees per cover)
        # Corollary: a tree meeting the face condition inside the cover (one of the two used corners per face)
        assert any(inst.h_tree({(i, ch[i]) for i in range(n)})
                   for ch in itertools.product(*[[v for v in A[i] if v != u[i]] for i in range(n)]))
        bump('2-factors containing a face-rainbow tree')
        bump('2-factors split into two rainbow trees')
        # (c): G_u has a directed cycle iff another 2-factor exists
        out = {x: [u[i] for i in used[x]] for x in X}
        colr = {}

        def dfs(v):
            colr[v] = 1
            for w in out.get(v, []):
                if colr.get(w) == 1 or (w not in colr and dfs(w)):
                    return True
            colr[v] = 2
            return False
        cyc = any(v not in colr and dfs(v) for v in X)
        assert cyc == (len(factors) > 1)
        if not cyc:
            assert nrb == 2 ** n
            c = len(inst.factor_cycles(u))
            assert ngood == 2 ** c == sum(1 for s in inst.states_in(u) if inst.good_state(s))
        gs = sum(1 for s in inst.states_in(u) if inst.good_state(s))
        assert gs == ngood
        if gs == 0:
            bump('covers without a good state')
    assert sum(per_factor.values()) == len(trees)

    # ---- Section 5: the exchange, the walk, evenness ----
    keys = list(trees)
    mv = {}
    exc = {k: inst.excess(trees[k]) for k in keys}
    for k in keys:
        sig = trees[k]
        row = []
        for x in X:
            al = inst.alts(sig, x)
            assert len(al) == 1                                           # Lemma (unique exchange)
            s2 = dict(sig)
            s2[x] = al[0]
            row.append(sf.key(inst, s2))
        mv[k] = row
        bump('(tree, point) exchanges', n)
    for k in keys:
        ld = inst.load(trees[k])
        for j, x in enumerate(X):
            assert mv[mv[k][j]][j] == k                                   # the exchange is an involution
            if ld[k[j]] == 2:
                assert ld[mv[k][j][j]] <= 1 and exc[mv[k][j]] <= exc[k]

    def step(k, t, a):
        j = [j for j in range(n) if k[j] == t and X[j] != a][0]
        k2 = mv[k][j]
        t2 = k2[j]
        was = sum(1 for z in k if z == t2)
        if was == 0:
            return None, k2
        assert was == 1
        return (k2, t2, X[j]), k2

    def mirror(S):
        k, t, a = S
        y = [X[j] for j in range(n) if k[j] == t and X[j] != a][0]
        return (k, t, y)
    for k in keys:                                                        # Lemma (reversal) on every walk state
        ld = inst.load(trees[k])
        for t in range(n):
            if ld[t] == 2:
                for a in [X[j] for j in range(n) if k[j] == t]:
                    S = (k, t, a)
                    S2, _ = step(*S)
                    bump('walk states')
                    if S2 is not None:
                        back, _ = step(*mirror(S2))
                        assert back == mirror(S)

    def iota(k, t):
        j = [j for j in range(n) if k[j] == t][0]
        k1 = mv[k][j]
        S = (k1, k1[j], X[j])
        m = 1
        seen = {S}
        while True:
            assert exc[S[0]] == 2 and inst.load(trees[S[0]])[t] == 0
            S2, kk = step(*S)
            if S2 is None:
                return kk, m
            assert S2 not in seen
            seen.add(S2)
            S = S2
            m += 1
    for k in good:
        for t in range(n):
            k2, m = iota(k, t)
            assert k2 in good and k2 != k                                 # Theorem (evenness)
            assert iota(k2, t)[0] == k
            bump('evaluations of iota')
            C['longest evict walk'] = max(C.get('longest evict walk', 0), m)
    assert len(good) % 2 == 0

    # ---- Section 7: strict descent and Step X ----
    stuck = [k for k in keys if exc[k] > 0 and all(exc[k2] >= exc[k] for k2 in mv[k])]
    if stuck:
        bump('trees of positive excess without a decreasing exchange', len(stuck))
        C.setdefault('first V where strict descent fails', inst.V)
    reach = set(good)
    stack = list(good)
    while stack:
        k = stack.pop()
        for k2 in mv[k]:
            if k2 not in reach and exc[k2] >= exc[k]:
                reach.add(k2)
                stack.append(k2)
    assert len(reach) == len(keys)                                        # Step X on this instance
    bump('rootings where Step X holds')

    # ---- Section 6: packing ----
    def w_edges(u):
        return [inst.wedge[(i, v)] for i in range(n) for v in A[i] if v != u[i]]

    def tr_edges(u):
        rho = inst.V
        idx = {x: j for j, x in enumerate(X)}
        idx.update({r: n for r in inst.R})
        return [(idx[u[i]], idx[v]) for i in range(n) for v in A[i] if v != u[i]]
    maps = [dict(u) for u in factors]
    if all_u:
        maps += [dict(enumerate(ch)) for ch in itertools.product(*A)]
    else:
        maps += [{i: rng.choice(A[i]) for i in range(n)} for _ in range(20)]
    for u in maps:
        assert split_two_trees(n + 1, w_edges(u)) is not None             # Theorem (two trees of W)
        te = tr_edges(u)
        assert all(a != b for a, b in te)
        assert split_two_trees(n + 1, te) is not None                     # Theorem (two forests of T)
        bump('deleted-corner maps split on both sides')


def density(V, tally):
    """Lemma (density) on every nonempty U, every rooting with V vertices."""
    for idx, rot in enumerate(sf.plantri(V)):
        fs = sf.faces_of(rot)
        cache = {}
        for k in range(len(fs)):
            inst = sf.Inst(fs, k)
            ck = frozenset(inst.black)
            if ck not in cache:
                adjm = [sum(1 << w for w in inst.adj[v]) for v in range(V)]
                e = [0] * (1 << V)
                for U in range(1, 1 << V):
                    low = (U & -U).bit_length() - 1
                    rest = U & (U - 1)
                    e[U] = e[rest] + bin(adjm[low] & rest).count('1')
                fm = [sum(1 << v for v in f) for f in inst.black]
                b = [sum(1 for m in fm if m & U == m) for U in range(1 << V)]
                cache[ck] = [e[U] - b[U] - 2 * bin(U).count('1') + 2 for U in range(1 << V)]
            base = cache[ck]
            rm = sum(1 << r for r in inst.R)
            worst = max(base[U] + max(0, bin(U & rm).count('1') - 1) for U in range(1, 1 << V))
            has = len(inst.black_inner_triangles()) > 0
            assert (worst <= 0) == (not has)
            tally['density: rootings'] = tally.get('density: rootings', 0) + 1
            if has:
                tally['density: rootings where it fails (black inner triangle)'] = tally.get('density: rootings where it fails (black inner triangle)', 0) + 1
            else:
                assert worst == 0
                # Proposition: forcing u(t_i) onto a black-inner triangle is impossible here; nothing to test


def prop_obstruction(inst, rng):
    """Proposition: with a black-inner separating triangle and u(t_i) on it, no split into two trees."""
    n, A = inst.n, inst.A
    for tri, inner in inst.black_inner_triangles():
        u = {i: rng.choice(A[i]) for i in range(n)}
        for i, f in enumerate(A):
            on = [v for v in f if v in tri]
            if len(on) == 2 and [v for v in f if v not in tri][0] in inner:
                u[i] = rng.choice(on)
        edges = [inst.wedge[(i, v)] for i in range(n) for v in A[i] if v != u[i]]
        assert nash_williams_violated(n + 1, edges)
        bump('obstructed maps (black inner triangle)')


def main():
    vmin, vmax = int(sys.argv[1]), int(sys.argv[2])
    out = sys.argv[3] if len(sys.argv) > 3 else None
    rng = random.Random(1)
    t0 = time.time()
    perV = {}
    for V in range(vmin, vmax + 1):
        before = dict(C)
        cnt = 0
        for idx, face, inst in sf.rootings(V):
            check_instance(inst, rng, all_u=(inst.n <= 7))
            prop_obstruction(inst, rng)
            cnt += 1
        if V <= 13:
            density(V, C)
        perV[V] = {k: C[k] - before.get(k, 0) for k in C if isinstance(C[k], int) and k not in ('longest evict walk', 'first V where strict descent fails')}
        print(f'V={V}: {cnt} rootings done, {time.time() - t0:.0f}s', flush=True)
    res = {'command': 'python verify.py ' + ' '.join(sys.argv[1:]), 'seconds': round(time.time() - t0, 1), 'totals': C, 'per_V': perV}
    print(json.dumps(res, indent=1))
    if out:
        with open(out, 'w') as f:
            json.dump(res, f, indent=1)


if __name__ == '__main__':
    main()
