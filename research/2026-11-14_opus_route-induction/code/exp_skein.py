"""E5: skein fits and octahedron insertion.
(a) least-squares fit  Y(T) ~ a Y(T1) + b Y(T2) + c  over groups where both merges at x are defined,
    for Y in states, TM, pairs, lc; report max residual of the best fit with integer-rounded coefficients.
(b) octahedron insertion (Batagelj/plantri S-operation) into every non-root face: compare TM(T+) with TM(T) * k.
usage: python exp_skein.py contract_6_16.jsonl VMAX_for_b"""
import sys, json
import numpy as np
from collections import defaultdict, Counter
from tri import *

rows = [json.loads(l) for l in open(sys.argv[1])]
grp = defaultdict(list)
for r in rows:
    grp[(r['V'], r['gid'], r['t0'], r['x'])].append(r)
for Y in ('states', 'TM', 'pairs', 'lc'):
    A, b = [], []
    for g in grp.values():
        if len(g) != 2: continue
        A.append([g[0]['Tp'][Y], g[1]['Tp'][Y], 1]); b.append(g[0]['T'][Y])
    A = np.array(A, float); b = np.array(b, float)
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    res = np.abs(A @ sol - b).max()
    ri = np.round(sol); resi = np.abs(A @ ri - b)
    print(f'{Y:7s} lstsq coeffs {np.round(sol,3)} max residual {res:.3f};  integer {ri} exact in {int((resi==0).sum())}/{len(b)}')


def insert_oct(T, f):
    """Glue an octahedron into face f: new inner triangle (S-operation)."""
    u, v, w = T.F[f]
    m = max(T.verts) + 1
    a, b, c = m, m + 1, m + 2   # a opposite u... inner triangle a b c, a near edge uv etc.
    # faces (same orientation as u v w): u v a? use standard subdivision: inner triangle ab c with
    # a on edge-side vw, b on wu, c on uv: faces u c b, v a c, w b a, a b c, and u v c, v w a, w u b
    F = [g for i, g in enumerate(T.F) if i != f]
    F += [(u, v, c), (v, w, a), (w, u, b), (u, c, b), (v, a, c), (w, b, a), (a, b, c)]
    return Tri.from_faces(F)

Vmax = int(sys.argv[2]); st = Counter()
for V in range(6, Vmax + 1):
    for gid, rot in enumerate(plantri(V)):
        T = from_rotation(rot)
        for t0 in range(len(T.F)):
            R = T.rooted(t0); tm = len(R.TMs())
            for f in range(len(T.F)):
                if f == t0: continue
                Tp = insert_oct(T, f)
                Rp = Tp.rooted(t0)  # face indices < f unchanged; t0 index shifts if t0 > f
                if t0 > f: Rp = Tp.rooted(t0 - 1)
                assert set(Rp.R) == set(R.R)
                tmp = len(Rp.TMs())
                colour = 'white' if R.col[f] == 1 else 'black'
                ratio = (tmp / tm) if tm else (None if tmp == 0 else 'inf')
                st[(colour, ratio)] += 1
print('octahedron insertion: (colour of face relative to root, TM(T+)/TM(T)) ->count', dict(st))
