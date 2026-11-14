"""E1: degree-4 contractions (inverse of Batagelj's Q-operation) on all rooted Eulerian triangulations.

usage: python exp_contract.py VMIN VMAX OUT.jsonl

For every triangulation T from plantri -b, every root face t0, every degree-4 vertex x
whose four faces avoid t0, and both ways of merging opposite neighbours (q into p), write one row
with the invariants of (T,t0) and (T',t0'), whether T' is simple, how many neighbours of x are
roots, and the lift statistics over all states s of T:
  A      s TM of T, of lift type, projection s' a TM of T'
  B      s TM of T, of lift type, s' a state but not a TM
  C      s TM of T, not of lift type (it is of lift type for the other merge at x)
  b      s' TM of T' whose unique preimage s is not a TM
  LC     s' TM of T' satisfying the local condition (see local_condition)
  LCbad  LC holds but s is not a TM (predicted 0)
  liftOK number of TMs of T' whose preimage is a TM (= A)
"""
import sys, json, time
from collections import Counter
from tri import *


def project(R, Rn, s, fmap, rename):
    sp = {}
    for t, v in s.items():
        if t in fmap:
            sp[fmap[t]] = rename.get(v, v)
    if set(sp) != set(Rn.A) or len(set(sp.values())) != len(sp) or set(sp.values()) != set(Rn.X):
        return None
    return sp


def key(s):
    return tuple(sorted(s.items()))


def local_condition(R, c, s):
    """For a lift-type state s of T: beta* = black face at x with s(beta*) = x, v* its merged
    corner, c2 its third corner, W the white face (x, c2, v_o), g the black face across the side
    c2 v_o of W.  LC: s(g) is the corner of g other than c2 and v_o, so that the edge c2 v of T'
    lies in Q of the projection."""
    T = R.T
    x, p, q = c['x'], c['p'], c['q']
    bstar = [t for t in c['faces'] if R.col[t] == 0 and s.get(t) == x]
    if len(bstar) != 1:
        return False
    b = T.F[bstar[0]]
    vstar = p if p in b else q
    vo = q if vstar == p else p
    c2 = [u for u in b if u not in (x, vstar)][0]
    W = [t for t in c['faces'] if R.col[t] == 1 and c2 in T.F[t] and vo in T.F[t]][0]
    fW = T.F[W]
    side = [i for i in range(3) if {fW[i], fW[(i + 1) % 3]} == {c2, vo}][0]
    g, _ = T.adj[W][side]
    if g == R.t0:
        return False
    third = [u for u in T.F[g] if u not in (c2, vo)][0]
    return s.get(g) == third


def analyse(R, c):
    """Row of statistics for one rooted instance and one contraction c."""
    t0 = R.t0
    row = dict(x=c['x'], p=c['p'], q=c['q'], o1=c['o1'], o3=c['o3'], loop=c['loop'])
    row['rootnbrs'] = len({c['p'], c['q'], c['o1'], c['o3']} & set(R.R))
    if c['loop']:
        return row, None
    Tn = c['T']
    row['simple'] = Tn.is_simple()
    Rn = Tn.rooted(c['fmap'][t0])
    row['Tp'] = Rn.invariants()
    rename = {c['q']: c['p']}
    tmsN = {key(s) for s in Rn.TMs()}
    st = Counter()
    for s in R.states():
        sp = project(R, Rn, s, c['fmap'], rename)
        isT = R.is_TM(s)
        if sp is None:
            if isT:
                st['C'] += 1
            continue
        isTp = key(sp) in tmsN
        lc = local_condition(R, c, s)
        if isT and isTp: st['A'] += 1
        if isT and not isTp: st['B'] += 1
        if isTp and not isT: st['b'] += 1
        if isTp and lc: st['LC'] += 1
        if isTp and lc and not isT: st['LCbad'] += 1
    row.update({k: st[k] for k in ('A', 'B', 'C', 'b', 'LC', 'LCbad')})
    row['liftOK'] = st['A']
    return row, Rn


def main(vmin, vmax, out):
    fo = open(out, 'w')
    for n in range(vmin, vmax + 1):
        t1 = time.time()
        rots = plantri(n)
        rows = 0
        for gid, rot in enumerate(rots):
            T = from_rotation(rot)
            cons = list(contractions(T))
            for t0 in range(len(T.F)):
                R = T.rooted(t0)
                inv = R.invariants()
                for c in cons:
                    if t0 in c['faces']:
                        continue
                    row, _ = analyse(R, c)
                    row.update(V=n, gid=gid, t0=t0, T=inv)
                    fo.write(json.dumps(row) + '\n'); rows += 1
        print(n, len(rots), rows, round(time.time() - t1, 1), flush=True)
    fo.close()


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
