"""The rotation rho at a degree-4 vertex and its statistics.
For a contraction c (merge q into p at x) and a lift-type state s of T whose projection is a TM of T'
but s itself is not a TM ("failing lift"):
  beta* = black face at x taking x, v* = its merged corner, c2 = its third corner,
  beta_o = the other black face at x (takes v_o),
  g = black face across the side c2-v_o of the white face (x, c2, v_o).
Prediction: s(g) = c2, and rho(s) := s with beta*: x -> c2, beta_o: v_o -> x, g: c2 -> v_o is a TM.
usage: python rho.py VMIN VMAX [maxshow]"""
import sys
from tri import *
from exp_contract import project, key
from collections import Counter


def rho_data(R, c, s):
    T = R.T; x, p, q = c['x'], c['p'], c['q']
    blacks = [t for t in c['faces'] if R.col[t] == 0]
    bstar = [t for t in blacks if s.get(t) == x][0]
    bo = [t for t in blacks if t != bstar][0]
    b = T.F[bstar]
    vstar = p if p in b else q
    vo = q if vstar == p else p
    c2 = [u for u in b if u not in (x, vstar)][0]
    W = [t for t in c['faces'] if R.col[t] == 1 and c2 in T.F[t] and vo in T.F[t]][0]
    fW = T.F[W]
    side = [i for i in range(3) if {fW[i], fW[(i + 1) % 3]} == {c2, vo}][0]
    g, _ = T.adj[W][side]
    return bstar, bo, g, c2, vo, vstar


if __name__ == '__main__':
    vmin, vmax = int(sys.argv[1]), int(sys.argv[2])
    maxshow = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    for V in range(vmin, vmax + 1):
        st = Counter(); shown = 0
        for gid, rot in enumerate(plantri(V)):
            T = from_rotation(rot)
            cons = list(contractions(T))
            for t0 in range(len(T.F)):
                R = T.rooted(t0)
                if not R.TMs(): continue
                for c in cons:
                    if t0 in c['faces'] or c['loop']: continue
                    Rn = c['T'].rooted(c['fmap'][t0]); rename = {c['q']: c['p']}
                    tmsN = {key(s) for s in Rn.TMs()}
                    images = set(); nfail = 0; ok = 0
                    for s in R.states():
                        sp = project(R, Rn, s, c['fmap'], rename)
                        if sp is None or key(sp) not in tmsN or R.is_TM(s): continue
                        nfail += 1
                        bstar, bo, g, c2, vo, vstar = rho_data(R, c, s)
                        if g == R.t0 or s.get(g) != c2:
                            st['s(g) != c2'] += 1; continue
                        s2 = dict(s); s2[bstar] = c2; s2[bo] = x = c['x']; s2[g] = vo
                        if R.is_TM(s2):
                            st['rho TM'] += 1; ok += 1; images.add(key(s2))
                        else:
                            st['rho not TM'] += 1
                            if shown < maxshow:
                                shown += 1
                                print('  exception V', V, 'gid', gid, 't0', T.F[t0], 'x', c['x'], 'merge', c['q'], '->', c['p'], 'roots nbr', len({c['p'], c['q'], c['o1'], c['o3']} & set(R.R)))
                    if len(images) != ok: st['rho not injective'] += 1
                    if nfail: st['instances with failures'] += 1
                    if nfail and ok == nfail: st['instances fully covered by rho'] += 1
        print(V, dict(st), flush=True)
