"""Checks every claim of Lemmas 2, 4, 5, 6, 7 and the Section 7 moment identity on one rooted instance.

Usage (from repository root):
  python research/2026-11-14_opus_referee-involutions/code/check.py census 14
  python research/2026-11-14_opus_referee-involutions/code/check.py census 15 --sample
"""
import json
import random
import sys
import time
from collections import Counter
from math import comb, factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ref import Inst, Maps, faces_from_rotation, plantri, Fr  # noqa: E402

OUT = Path(__file__).resolve().parent / 'out'
OUT.mkdir(exist_ok=True)


def ckey(p, c):
    return frozenset((i, frozenset((p[0][i], p[1][i]))) for i in c)


def check(I, order='lex', seed=0, extra_k=True):
    S = I.states()
    P = I.pairs(S)
    if not P:
        return dict(states=len(S), pairs=0)
    key = None
    if order == 'random':
        rng = random.Random(seed)
        memo = {}
        def key(c):
            k = tuple(sorted(c))
            if k not in memo:
                memo[k] = rng.random()
            return memo[k]
    mp = Maps(I, P, order_key=key)
    m = mp.m
    n = I.n
    # Lemma 2 / J: delta-J equals geometric-J; c == n mod 2; every cycle odd, encloses a white face
    area = {}
    for p in P:
        cyc = I.dcycles(p)
        assert I.J(p) == I.J_geometric(p)
        assert len(cyc) % 2 == n % 2 and all(len(c) % 2 == 1 for c in cyc)
        for c in cyc:
            # Lemma 2: delta sum on the cycle is +-3 and matches orientation
            dsum = sum(I.delta(p[0][i], p[1][i]) for i in c)
            assert dsum in (3, -3)
            h = len(c)
            ell = (h + dsum) // 2  # sides with black face to the left
            poly = [I.pos[p[0][i]] for i in c]
            wins = [w for w in I.white if I.inside_poly(poly, I.cen[w])]
            # spoke polygon r(t)->t->s(t) encloses same white points
            spoly = []
            for i in c:
                spoly += [I.pos[p[0][i]], I.cen[I.A[i]]]
            assert wins == [w for w in I.white if I.inside_poly(spoly, I.cen[w])]
            assert wins, 'cycle encloses no white face'
            # parity of ray crossings with the spoke cycle == inside
            for w in I.white:
                assert (len(I.ray_list(p, c, w)) % 2 == 1) == (w in wins)
            area[ckey(p, c)] = len(wins)
    # Lemma 4 directed-cycle claim for Q_s cycles and disk identity on them
    for p in P:
        for K in I.q_cycles(p[1]):
            r, s = p
            dsum = 0
            for i in K:
                f = I.faces[I.A[i]]
                u = next(v for v in f if v not in (r[i], s[i]))
                dsum += I.delta(r[i], u)
            assert dsum in (3, -3)
    objs = list(mp.objects())
    U = set(objs)
    sig = {o: I.sign(o[0], o[1]) for o in objs}
    stats = Counter()
    fix1, fix2 = [], []
    for o in objs:
        q = mp.iota1(o)
        assert q in U, 'iota1 leaves Omega'
        assert mp.iota1(q) == o, 'iota1 not an involution'
        if q == o:
            fix1.append(o)
            assert I.q_forest(o[0][1])
        else:
            assert not I.q_forest(o[0][1])
            assert sig[q] == -sig[o]
            assert q[0][1] == o[0][1] and q[1] == o[1]
        q2, case = mp.iota2(o)
        stats[case] += 1
        assert q2 in U, 'iota2 leaves Omega'
        back, case_back = mp.iota2(q2)
        assert back == o, ('iota2 not involution', o, q2, back)
        assert case_back == case, (case, case_back)
        if q2 == o:
            fix2.append(o)
        else:
            assert sig[q2] == -sig[o]
    # fixed set of iota2: description and sign and count
    for o in fix2:
        p, M = o
        cyc = I.dcycles(p)
        assert len(cyc) == m
        assert sig[o] == (-1) ** (m // 2)
        for c in cyc:
            mk = [(w, i) for (w, i) in M if i in c]
            assert len(mk) == 1
            w, i = mk[0]
            rl = I.ray_list(p, c, w)
            assert len(rl) % 2 == 1 and rl[0][1] == i and rl[0][2] == 1
    covers = {}
    for p in P:
        cyc = I.dcycles(p)
        if len(cyc) == m:
            key_ = frozenset(ckey(p, c) for c in cyc)
            covers.setdefault(key_, 0)
            covers[key_] += 1
    assert all(v == 2 ** m for v in covers.values())
    F = 0
    for D in covers:
        prod = 1
        for c in D:
            prod *= area[c]
        F += prod
    assert len(fix2) == F and F > 0
    signed = sum(sig.values())
    assert signed == (-1) ** (m // 2) * F
    # Garsia-Milne walk (Lemma 7)
    walks = []
    for o0 in fix2:
        seen = {o0}
        o, steps = o0, 0
        while True:
            q = mp.iota1(o)
            if q == o:
                break
            q2, _ = mp.iota2(q)
            assert q2 != q, 'walk ends at a second-fixed object of opposite sign?'
            assert q not in seen and q2 not in seen
            seen |= {q, q2}
            o = q2
            steps += 2
        assert I.q_forest(o[0][1])
        walks.append(steps)
    # moment identity: H(s) = sum over tokens of (+1 left-to-right, -1 otherwise)
    mom = []
    for j in range(m + 1):
        tot = 0
        for p in P:
            Hs = sum(1 - 2 * I.dir(p, w, i) for (w, i) in mp.toks(p))
            eps = (-1) ** ((n + I.J(p)) // 2)
            tot += eps * Hs ** j
        mom.append(tot)
    assert mom[:m] == [0] * m
    ceil_n2 = (n + 1) // 2
    assert mom[m] == factorial(m) * (-1) ** ceil_n2 * signed
    note_formula = (-1) ** ((n - m) // 2) * F  # as printed in Section 7
    fixed_formula = (-1) ** ((n + m) // 2) * F
    assert mom[m] // factorial(m) == fixed_formula
    res = dict(states=len(S), pairs=len(P), m=m, n=n, objects=len(objs), fix1=len(fix1), fix2=len(fix2),
               signed=signed, F=F, cases=dict(stats), max_walk=max(walks), walk_hist=dict(Counter(walks)),
               moment_m=mom[m] // factorial(m), note_section7_sign_ok=(mom[m] // factorial(m) == note_formula),
               tokens_per_pair=sorted(Counter(len(mp.toks(p)) for p in P).items()))
    if extra_k:
        # signed counts with k marks, k != m (not part of the proof; informational)
        ex = {}
        for k in (m - 1, m + 1):
            if k < 0:
                continue
            ex[k] = sum(I.sign(o[0], o[1]) for o in mp.objects(k))
        res['signed_other_k'] = ex
    return res


def census(maxv, minv=6, orders=('lex', 'random')):
    rows = []
    t = time.time()
    for nv in range(minv, maxv + 1):
        for cls, rot in enumerate(plantri(nv)):
            faces = faces_from_rotation(rot)
            assert len(faces) == 2 * nv - 4
            for t0 in range(len(faces)):
                I = Inst(faces, t0)
                for order in orders:
                    r = check(I, order=order, seed=nv * 1000 + cls * 50 + t0, extra_k=(order == 'lex'))
                    r.update(v=nv, cls=cls, root=t0, order=order)
                    rows.append(r)
        print(nv, 'done', round(time.time() - t, 1), 's', flush=True)
    return rows


if __name__ == '__main__':
    if sys.argv[1] == 'census':
        maxv = int(sys.argv[2])
        rows = census(maxv)
        lex = [r for r in rows if r['order'] == 'lex']
        paired = [r for r in lex if r.get('pairs')]
        summ = dict(command=' '.join(['python'] + sys.argv),
                    classes=dict(Counter(r['v'] for r in lex if r['root'] == 0)),
                    rooted=len(lex), paired=len(paired),
                    m_hist=dict(Counter(r['m'] for r in paired)),
                    objects=sum(r['objects'] for r in paired),
                    fix2=sum(r['fix2'] for r in paired),
                    fix1=sum(r['fix1'] for r in paired),
                    max_walk=max(r['max_walk'] for r in paired),
                    walk_hist=dict(sum((Counter({int(k): v for k, v in r['walk_hist'].items()}) for r in paired), Counter())),
                    cases=dict(sum((Counter(r['cases']) for r in paired), Counter())),
                    section7_printed_sign_fails=sum(not r['note_section7_sign_ok'] for r in paired),
                    section7_printed_sign_fails_m_odd=sum((not r['note_section7_sign_ok']) and r['m'] % 2 == 1 for r in paired),
                    m_odd=sum(r['m'] % 2 == 1 for r in paired),
                    random_order_rows_ok=len([r for r in rows if r['order'] == 'random' and r.get('pairs')]),
                    other_k_zero_below=all(r['signed_other_k'].get(r['m'] - 1, 0) == 0 for r in paired),
                    other_k_above_nonzero=sum(r['signed_other_k'][r['m'] + 1] != 0 for r in paired))
        (OUT / f'census-{maxv}.json').write_text(json.dumps(dict(summary=summ, rows=rows), indent=1, default=str))
        print(json.dumps(summ, indent=1))
