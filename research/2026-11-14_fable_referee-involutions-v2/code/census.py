"""Census check of Section 5 and its comparison with rays and with paper/main Section 4.

Run from the repository root:
    python research/2026-11-14_fable_referee-involutions-v2/code/census.py VMAX [RAY_VMAX]
Path modes run on every rooted instance with at most VMAX vertices, ray modes on those with
at most RAY_VMAX (default 12). Output: code/out/census-VMAX.json and .log.
"""
import sys, json, math, random, time
from fractions import Fraction as Fr
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from fp import plantri, trace_faces, Inst, Model

OUT = Path(__file__).parent / 'out'
PATH_MODES = ['bfs+', 'bfs-', 'dfs', 'rand', 'walk']
RAY_DIRS = [(Fr(1, 97), Fr(1)), (Fr(-13, 7), Fr(-1)), (Fr(5), Fr(3, 11))]


def lemma7(I, M, mode_is_path, ori):
    """Parity, alternation and the first-exit rule for every list (the first sentence of Lemma 7).
    ori = +1 if the declared orientation of I is the one seen in the plane (always, in path mode)."""
    n = 0
    for p in M.pairs:
        r, s = p
        for C in M.cyc[p]:
            ins, ccw = I.cyc_info(p, C)
            if ori < 0:
                ccw = not ccw
            for w in I.white:
                L = M.lst(p, C, w)
                # signed crossing of the cycle as traversed r -> centre -> s, left to right positive
                trav = []
                for i in L:
                    k, v, a, _ = M.cr[w][i]
                    trav.append(a if v == s[k] else -a)
                assert (len(L) % 2 == 1) == (w in ins), 'parity'
                assert all(trav[j] != trav[j + 1] for j in range(len(trav) - 1)), 'alternation'
                if w in ins:
                    assert trav[0] == (-1 if ccw else 1), 'first exit'
                elif L:
                    assert trav[0] == (1 if ccw else -1), 'first entry'
                n += 1
    return n


def all_checks(I, cr, ori=1, order=None, is_path=False, lists=True):
    """Every assertion for one instance in one mode. Returns a record."""
    M = Model(I, cr, order)
    m, n = M.m, I.n
    rec = {}
    if lists:
        rec['lists'] = lemma7(I, M, is_path, ori)
    # the invariant F
    covers = {}
    for p in M.pairs:
        if len(M.cyc[p]) == m:
            key = frozenset(frozenset((p[0][k], p[1][k])) for k in range(n))
            if key not in covers:
                covers[key] = math.prod(sum(1 for f in I.cyc_info(p, C)[0] if f in I.white) for C in M.cyc[p])
    F = sum(covers.values())
    assert F > 0
    objs = list(M.objects()); S = set(objs)
    assert len(S) == len(objs)
    sig = {o: M.sign(o) for o in objs}
    fix1, fix2 = [], []
    branch = Counter()
    for o in objs:
        p = o[0]
        # first map
        a = M.iota1(o)
        assert a in S and M.iota1(a) == o
        qs = I.qcycles_from_s(p[1])
        assert qs == I.qcycles(p)                    # the cycles of Q_s are read from s alone
        assert (a == o) == (not qs)
        if a == o:
            fix1.append(o)
        else:
            assert sig[a] == -sig[o] and a[0][1] == p[1] and a[1] == o[1]
            assert abs(M.Jc[a[0]] - M.Jc[p]) == 2
        # second map
        tr = []
        b = M.iota2(o, tr)
        assert b in S, 'iota2 leaves Omega'
        tr2 = []
        assert M.iota2(b, tr2) == o, 'iota2 not an involution'
        if b == o:
            fix2.append(o)
        else:
            assert sig[b] == -sig[o], 'iota2 sign'
            assert tr == tr2
            branch[tr[0]] += 1
    # fixed set of the second map
    assert len(fix2) == F, (len(fix2), F)
    assert all(sig[o] == (-1) ** (m // 2) for o in fix2)
    assert sum(sig.values()) == (-1) ** (m // 2) * F
    for o in fix2:
        p, Mk = o
        assert len(M.cyc[p]) == m
        for C in M.cyc[p]:
            (w, i), = [(w, i) for (w, i) in Mk if cr[w][i][0] in C]
            assert w in I.cyc_info(p, C)[0] and M.lst(p, C, w)[0] == i
    # alternating walk from every second-fixed object
    wl = Counter()
    for o in fix2:
        seen, cur, moves = {o}, o, 0
        while True:
            nx = M.iota1(cur)
            if nx == cur:
                break
            assert nx not in seen; seen.add(nx); cur = nx; moves += 1
            nx = M.iota2(cur)
            assert nx != cur and nx not in seen; seen.add(nx); cur = nx; moves += 1
        assert not I.qcycles(cur[0])
        wl[moves] += 1
    # moments of H (left to right positive) with the phase eps = (-1)^((n+J)/2) = prod delta
    H = {}
    for p in M.pairs:
        H[p] = sum(cr[w][i][2] for (w, i) in M.tokens(p))
        eps = (-1) ** (((n + M.Jc[p]) // 2) % 2)
        assert (n + M.Jc[p]) % 2 == 0
        assert eps == math.prod(I.delta(p[0][k], p[1][k]) for k in range(n))
        H[p] = (eps, H[p])
    for j in range(m):
        assert sum(e * h ** j for e, h in H.values()) == 0
    lead = sum(e * h ** m for e, h in H.values())
    assert lead == math.factorial(m) * (-1) ** (((n + m) // 2) % 2) * F
    assert lead == math.factorial(m) * (-1) ** (-(-n // 2) % 2) * sum(sig.values())
    # k = m - 1 and k = m + 1 marks: signed counts through elementary symmetric functions
    def esym(vals, k):
        e = [1] + [0] * k
        for x in vals:
            for j in range(k, 0, -1):
                e[j] += x * e[j - 1]
        return e[k]
    cnt = {}
    for k in (m - 1, m + 1):
        cnt[k] = sum((-1 if (M.Jc[p] // 2) % 2 else 1) * esym([cr[w][i][2] for (w, i) in M.tokens(p)], k) for p in M.pairs)
    assert cnt[m - 1] == 0
    rec.update(m=m, F=F, objects=len(objs), fix1=len(fix1), fix2=len(fix2), signed=sum(sig.values()),
               walks=dict(wl), branch=dict(branch), mplus1=cnt[m + 1])
    if is_path:
        # paper/main Section 4: omega = -H, Lemma 4.6 increments, Proposition 4.8
        om = {p: -H[p][1] for p in M.pairs}
        sigma = sum(H[p][0] * om[p] ** m for p in M.pairs)
        assert sigma == (-1) ** (((n - m) // 2) % 2) * math.factorial(m) * F
        for j in range(m):
            assert sum(H[p][0] * om[p] ** j for p in M.pairs) == 0
        def eta(s, y):
            return sum(-a for (k, v, a, _) in cr[y] if s[k] == v)
        for p in M.pairs:
            for C in M.cyc[p]:
                ins, ccw = I.cyc_info(p, C)
                if ccw:
                    continue
                p2 = M.reverse(p, C)
                for y in I.white:
                    assert eta(p2[1], y) - eta(p[1], y) == (1 if y in ins else 0), 'Lemma 4.6'
    return rec


def run(vmax, ray_vmax):
    t0 = time.time()
    OUT.mkdir(exist_ok=True)
    log = open(OUT / f'census-{vmax}.log', 'w')
    def say(*a):
        line = ' '.join(str(x) for x in a); print(line, flush=True); log.write(line + '\n'); log.flush()
    tot = Counter(); rows = []; mcount = Counter(); classes = Counter(); geo = 0
    for v in range(6, vmax + 1):
        for ci, rot in enumerate(plantri(v)):
            classes[v] += 1
            faces = trace_faces(rot)
            for root in range(len(faces)):
                I = Inst(faces, root)
                tot['roots'] += 1
                pairs = I.pairs()
                if not pairs:
                    continue
                tot['paired'] += 1
                row = {'v': v, 'class': ci, 'root': root, 'n': I.n, 'states': len(I.states), 'pairs': len(pairs)}
                seed = 1000 * v + 37 * ci + root
                ref = None
                for mode in PATH_MODES:
                    paths = I.tree_paths(mode, seed)
                    cr = I.path_crossings(paths)
                    rng = random.Random(seed + 1)
                    perm = {}
                    order = None if mode in ('bfs+', 'dfs') else (lambda key, perm=perm, rng=rng: perm.setdefault(key, rng.random()))
                    rec = all_checks(I, cr, 1, order, True)
                    row[mode] = rec
                    for k in ('objects', 'fix1', 'fix2', 'lists'):
                        tot[mode + ':' + k] += rec[k]
                    tot[mode + ':mplus1_zero'] += rec['mplus1'] == 0
                    tot[mode + ':maxwalk'] = max(tot[mode + ':maxwalk'], max(rec['walks']))
                    for b, c in rec['branch'].items():
                        tot[mode + ':' + b] += c
                    if ref is None:
                        ref = (rec['m'], rec['F'], rec['signed'])
                        mcount[rec['m']] += 1
                    assert ref == (rec['m'], rec['F'], rec['signed'])
                if v <= ray_vmax:
                    pos = I.tutte()
                    # geometric test of kappa: the corner cut off lies on the left of the chord between the side midpoints
                    for mode in ('bfs+', 'walk'):
                        paths = I.tree_paths(mode, seed)
                        for w, lst in I.path_crossings(paths).items():
                            P = paths[w]
                            for (k, vv, a, i) in lst:
                                mid = lambda e: tuple(sum(pos[x][c] for x in e) / 2 for c in (0, 1))
                                p_in, p_out = mid(I.side(P[i - 1], P[i])), mid(I.side(P[i], P[i + 1]))
                                cr_ = (p_out[0] - p_in[0]) * (pos[vv][1] - p_in[1]) - (p_out[1] - p_in[1]) * (pos[vv][0] - p_in[0])
                                assert (cr_ > 0) == (a == -1), 'kappa geometry'
                                geo += 1
                    used = 0
                    for d in RAY_DIRS:
                        cr, ori = I.ray_crossings(pos, d)
                        if cr is None:
                            continue
                        assert ori == 1
                        used += 1
                        name = 'ray%d' % used
                        rec = all_checks(I, cr, ori, None, False)
                        row[name] = rec
                        assert ref == (rec['m'], rec['F'], rec['signed'])
                        for k in ('objects', 'fix1', 'fix2', 'lists'):
                            tot[name + ':' + k] += rec[k]
                        tot[name + ':maxwalk'] = max(tot[name + ':maxwalk'], max(rec['walks']))
                        tot[name + ':roots'] += 1
                        if used == 2:
                            break
                    assert used == 2
                tot['F'] += ref[1]
                rows.append(row)
        say(f'v<={v}: classes {sum(classes.values())} roots {tot["roots"]} paired {tot["paired"]} F-total {tot["F"]} m {dict(mcount)} [{time.time()-t0:.0f}s]')
    for k in sorted(tot):
        say(k, tot[k])
    say('kappa geometry checks', geo)
    json.dump({'vmax': vmax, 'ray_vmax': ray_vmax, 'classes': dict(classes), 'm_histogram': dict(mcount),
               'totals': dict(tot), 'rows': rows}, open(OUT / f'census-{vmax}.json', 'w'), indent=0, default=str)


if __name__ == '__main__':
    vmax = int(sys.argv[1]); ray = int(sys.argv[2]) if len(sys.argv) > 2 else min(vmax, 12)
    run(vmax, ray)
