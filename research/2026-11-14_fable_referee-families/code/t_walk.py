"""Height-marked walk of route-probabilistic PROOFS section 6, implemented from the text.

Object: (r, s, k) with (r, s) a pair and k = (k_1..k_m), k_i in {1..H_i(s)},
H_i = shifted height of a fixed inner white face w_i.
Q-involution: reverse a cycle of Q_s chosen from s alone (changes r only).
D-involution: on the cover of (r, s), read each k_i as a token of the ordered pool
[b_i base tokens, then one token per CCW cycle containing w_i, in a fixed cycle order];
reverse the first cycle that no slot has chosen; re-encode ranks.
The script checks, on every marked object of each instance:
 both maps are involutions, both reverse epsilon off their fixed sets,
 Q-fixed = marked good pairs, D-fixed = minimum covers, all CCW, slots <-> cycles bijectively,
 all D-fixed objects have one sign, and every walk from a D-fixed object ends at a good pair.
"""
import sys, itertools
from collections import defaultdict
from core import *


def setup(inst):
    a, kappa, inner = inst.weights()
    states = list(inst.states())
    covs = list(inst.covers())
    m = min(len(inst.cover_cycles(d)) for d in covs)
    # a minimum cover and one white face inside each of its cycles
    d0 = next(d for d in covs if len(inst.cover_cycles(d)) == m)
    ors = list(inst.orientations(d0))
    base = ors[0][1]
    ws = []
    for i in range(m):
        s1 = ors[1 << i][1]
        y = next(y for y in inner if inst.height(y, s1) != inst.height(y, base))
        ws.append(y)
    shift = [-min(inst.height(y, s) for s in states) for y in ws]
    return dict(m=m, ws=ws, shift=shift, covs=covs)


def H(inst, st, i, s):
    return inst.height(st['ws'][i], s) + st['shift'][i]


def cover_of(r, s):
    return {t: (r[t], s[t]) for t in s}


def cyc_key(cyc):
    return tuple(sorted(t for t, _, _ in cyc))


def analyse(inst, st, r, s):
    """Cycles of the cover in canonical order, their CCW flags, and for each slot
    the base count b_i and the list of cycle indices that contain w_i."""
    d = cover_of(r, s)
    cycles = sorted(inst.cover_cycles(d), key=cyc_key)
    ccw = []
    for cyc in cycles:
        t, a, b = cyc[0]
        # the stored direction a->b is the actual direction iff r[t]==a
        ds = sum(inst.delta(x, y) for _, x, y in cyc)
        actual = ds if r[t] == a else -ds
        ccw.append(actual == -3)        # checked in t_sanity: delta-sum -3 <=> larger omega
    return cycles, ccw


def flip(r, s, cyc):
    r2, s2 = dict(r), dict(s)
    for t, _, _ in cyc:
        r2[t], s2[t] = s[t], r[t]
    return r2, s2


def inside(inst, st, r, s, cycles, ccw):
    """a[i][c] = 1 if w_i lies inside cycle c; b_i = H_i of the all-clockwise orientation."""
    rc, sc = dict(r), dict(s)
    for c, cyc in enumerate(cycles):
        if ccw[c]:
            rc, sc = flip(rc, sc, cyc)
    b = [H(inst, st, i, sc) for i in range(st['m'])]
    ain = []
    for i in range(st['m']):
        row = []
        for cyc in cycles:
            r2, s2 = flip(rc, sc, cyc)
            dlt = H(inst, st, i, s2) - b[i]
            assert dlt in (0, 1), dlt     # height rises by one exactly when a cycle around w_i turns CCW
            row.append(dlt)
        ain.append(row)
    return b, ain


def decode(b, ain, ccw, k):
    """rank -> token. Token = ('b', j) or ('c', cycle index)."""
    toks = []
    for i, ki in enumerate(k):
        pool = [('b', j) for j in range(b[i])] + [('c', c) for c in range(len(ccw)) if ccw[c] and ain[i][c]]
        toks.append(pool[ki - 1])
    return toks


def encode(b, ain, ccw, toks):
    k = []
    for i, tk in enumerate(toks):
        pool = [('b', j) for j in range(b[i])] + [('c', c) for c in range(len(ccw)) if ccw[c] and ain[i][c]]
        k.append(pool.index(tk) + 1)
    return tuple(k)


def Dmap(inst, st, obj):
    r, s, k = obj
    cycles, ccw = analyse(inst, st, r, s)
    b, ain = inside(inst, st, r, s, cycles, ccw)
    toks = decode(b, ain, ccw, k)
    chosen = {tk[1] for tk in toks if tk[0] == 'c'}
    unc = [c for c in range(len(cycles)) if c not in chosen]
    if not unc:
        return obj, True
    c = unc[0]
    r2, s2 = flip(r, s, cycles[c])
    ccw2 = list(ccw)
    ccw2[c] = not ccw[c]
    return (r2, s2, encode(b, ain, ccw2, toks)), False


def Qmap(inst, st, obj):
    r, s, k = obj
    if inst.is_good(s):
        return obj, True
    # orient opposite edges r(t) -> u(t); find the directed cycle through the least vertex on a cycle
    nxt = {}
    for t in s:
        u = next(x for x in inst.faces[t] if x not in (r[t], s[t]))
        nxt[r[t]] = (u, t)
    best = None
    for v0 in sorted(nxt):
        v, seen = v0, set()
        while v in nxt and v not in seen:
            seen.add(v)
            v = nxt[v][0]
        if v == v0:
            best = v0
            break
    assert best is not None
    r2 = dict(r)
    v = best
    while True:
        u, t = nxt[v]
        r2[t] = u
        v = u
        if v == best:
            break
    return (r2, s, k), False


def key(obj):
    r, s, k = obj
    return (tuple(sorted(r.items())), tuple(sorted(s.items())), k)


def eps_of(inst, r, s):
    e = 1
    for t in s:
        e *= inst.delta(r[t], s[t])
    return e


def run(inst, name):
    st = setup(inst)
    m = st['m']
    objs = []
    for d in st['covs']:
        for r, s, eps, js in inst.orientations(d):
            hs = [H(inst, st, i, s) for i in range(m)]
            assert all(h >= 0 for h in hs)
            for k in itertools.product(*[range(1, h + 1) for h in hs]):
                objs.append((r, s, k))
    allk = {key(o) for o in objs}
    dfix, qfix, signed = [], [], 0
    for o in objs:
        e = eps_of(inst, o[0], o[1])
        signed += e
        o2, f = Dmap(inst, st, o)
        assert key(o2) in allk
        if f:
            dfix.append(o)
            cycles, ccw = analyse(inst, st, o[0], o[1])
            assert len(cycles) == m and all(ccw)
        else:
            assert eps_of(inst, o2[0], o2[1]) == -e
            assert key(Dmap(inst, st, o2)[0]) == key(o)
        o3, f = Qmap(inst, st, o)
        assert key(o3) in allk
        if f:
            qfix.append(o)
        else:
            assert eps_of(inst, o3[0], o3[1]) == -e
            assert key(Qmap(inst, st, o3)[0]) == key(o)
    signs = {eps_of(inst, o[0], o[1]) for o in dfix}
    assert len(signs) == 1
    assert signs == {(-1) ** ((inst.n - m) // 2)} or signs == {-(-1) ** ((inst.n - m) // 2)}
    assert signed == sum(eps_of(inst, o[0], o[1]) for o in dfix) == sum(eps_of(inst, o[0], o[1]) for o in qfix)
    maxlen = 0
    for o in dfix:
        cur, steps = o, 0
        while True:
            nx_, f = Qmap(inst, st, cur)
            if f:
                break
            cur = nx_
            steps += 1
            nx_, f = Dmap(inst, st, cur)
            assert not f, 'walk reached a second D-fixed object'
            cur = nx_
            steps += 1
        assert inst.is_good(cur[1])
        maxlen = max(maxlen, steps)
    print(name, 'V', len(inst.g), 'm', m, 'objects', len(objs), 'D-fixed', len(dfix), 'Q-fixed', len(qfix),
          'signed sum', signed, 'fixed sign', signs, '(-1)^((n-m)/2) =', (-1) ** ((inst.n - m) // 2), 'longest walk', maxlen)
    sys.stdout.flush()
    return dict(name=name, m=m, objects=len(objs), dfixed=len(dfix), qfixed=len(qfix), signed=signed, longest=maxlen)


if __name__ == '__main__':
    import json
    out = []
    out.append(run(Inst(bipyramid(4), (4, 0, 1)), 'cube'))
    out.append(run(Inst(bipyramid(8), (8, 0, 1)), 'prism8'))
    for q in (2, 3):
        g, root = prism_chain(q, 2)
        out.append(run(Inst(g, root), f'chain q={q}'))
    for L in (1, 2, 3):
        out.append(run(Inst(tube(6, L), (0, 1, 7)), f'tube6 L={L}'))
    maxv = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    cnt = 0
    for V in range(6, maxv + 1):
        for gi, g in enumerate(plantri_eulerian(V)):
            faces = oriented_faces(g)
            for fi in range(len(faces)):
                inst = Inst(g, fi, faces=faces)
                if next(inst.covers(), None) is None:
                    continue
                out.append(run(inst, f'plantri_{V}_{gi} root {sorted(inst.R)}'))
                cnt += 1
    print('plantri roots with a pair walked:', cnt)
    json.dump(out, open('out_walk.json', 'w'), indent=1)
