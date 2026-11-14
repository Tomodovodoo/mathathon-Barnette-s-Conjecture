"""E2-E4.  usage: python exp_misc.py VMIN VMAX
E2 good contraction: for every rooted (T,t0) with a pair, is there a degree-4 contraction avoiding t0
   whose result has a pair?  (split by: T has a separating triangle or not; T' simple or not)
E3 P-reduction (inverse Batagelj P): TM(T) >= TM(T''), pair preservation.
E4 candidate induction hypotheses, tested as statements on every rooted instance with a pair:
   HCs  every (t in A, nonroot corner u) has a TM with s(t) = u
   HCr  every (t in A, nonroot corner u) has a TM whose mate r has r(t) = u
   HQin every edge e of a face t in A whose opposite corner is nonroot lies in Q_s for some TM
   HQout every edge of a face in A avoids Q_s for some TM
"""
import sys, json
from collections import Counter
from tri import *
from exp_contract import project, key


def sep_triangle(T):
    nb = {}
    for f in T.F:
        for v in f:
            nb.setdefault(v, set()).update(set(f) - {v})
    faces = {frozenset(f) for f in T.F}
    for u in nb:
        for v in nb[u]:
            if v <= u: continue
            for w in nb[u] & nb[v]:
                if w <= v: continue
                if frozenset((u, v, w)) not in faces:
                    return True
    return False


vmin, vmax = int(sys.argv[1]), int(sys.argv[2])
for V in range(vmin, vmax + 1):
    e2 = Counter(); e3 = Counter(); e4 = Counter(); ex = {}
    for gid, rot in enumerate(plantri(V)):
        T = from_rotation(rot)
        sep = sep_triangle(T)
        cons = list(contractions(T)); preds = list(p_reductions(T))
        for t0 in range(len(T.F)):
            R = T.rooted(t0)
            tms = R.TMs()
            if not tms:
                continue
            # E2
            good_simple = good_any = False
            for c in cons:
                if t0 in c['faces'] or c['loop']: continue
                Rn = c['T'].rooted(c['fmap'][t0])
                if Rn.TMs():
                    good_any = True
                    if c['T'].is_simple(): good_simple = True
            e2[('sep' if sep else 'nosep', 'good simple' if good_simple else ('good multigraph only' if good_any else 'NONE'))] += 1
            if not good_any: ex.setdefault('E2 none', (V, gid, t0))
            # E3
            for pr in preds:
                if t0 in pr['faces']: continue
                Rn = pr['T'].rooted(pr['fmap'][t0])
                tn = len(Rn.TMs())
                e3['P-reductions'] += 1
                if not pr['simple']: e3['non-simple'] += 1
                if tn > len(tms): e3['TM increases'] += 1; ex.setdefault('E3 increase', (V, gid, t0, pr['b'], pr['c']))
                if tn == 0: e3['pair lost'] += 1
            # E4
            F = T.F; Rs = set(R.R)
            mates = [R.mate_of_TM(s) for s in tms]
            okCs = okCr = okQin = okQout = True
            for t in R.A:
                for u in F[t]:
                    if u in Rs: continue
                    if not any(s[t] == u for s in tms): okCs = False; ex.setdefault('HCs', (V, gid, t0, F[t], u))
                    if not any(r[t] == u for r in mates): okCr = False; ex.setdefault('HCr', (V, gid, t0, F[t], u))
                    # edge opposite u
                    if not any(s[t] == u for s in tms): okQin = False
                for i in range(3):
                    opp = F[t][(i + 2) % 3]
                    if not any(s[t] != opp for s in tms): okQout = False; ex.setdefault('HQout', (V, gid, t0, F[t], i))
            e4['instances'] += 1
            for name, okk in (('HCs', okCs), ('HCr', okCr), ('HQin', okQin), ('HQout', okQout)):
                if okk: e4[name + ' holds'] += 1
    print(json.dumps({'V': V, 'E2': {' / '.join(k): v for k, v in e2.items()}, 'E3': e3, 'E4': e4, 'examples': ex}), flush=True)
