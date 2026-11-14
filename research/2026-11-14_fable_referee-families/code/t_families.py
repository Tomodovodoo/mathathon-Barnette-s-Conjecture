"""Referee replay of FAMILIES.md sections 1 and 2 (prisms and tubes) with core.py."""
import json, time, sys
from core import *

def det_states(inst):
    """|det K_B| by fraction-free elimination (exact integers)."""
    idx = {v: i for i, v in enumerate(inst.X)}
    Mx = [[0] * inst.n for _ in inst.A]
    for i, t in enumerate(inst.A):
        for v in inst.corners[t]:
            Mx[i][idx[v]] = 1
    n = inst.n; prev = 1; sign = 1
    for k in range(n - 1):
        if Mx[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if Mx[i][k]), None)
            if sw is None: return 0
            Mx[k], Mx[sw] = Mx[sw], Mx[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                Mx[i][j] = (Mx[i][j] * Mx[k][k] - Mx[i][k] * Mx[k][j]) // prev
        prev = Mx[k][k]
    return abs(Mx[n - 1][n - 1])

out = {}
# ---- prisms
rows = []
for m in range(2, 13):
    p = 2 * m
    inst = Inst(bipyramid(p), (p, 0, 1))
    r = inst.summary()
    H, use = hamilton(inst)
    rail = sorted({H - use.get(frozenset((p, i)), 0) for i in range(p)} | {H - use.get(frozenset((p + 1, i)), 0) for i in range(p)})
    rung = sorted({H - use.get(frozenset((i, (i + 1) % p)), 0) for i in range(p)})
    expect = tuple([-1] + [0] * (m - 2) + [1])
    ok = (r['S'] == m and r['P'] == 2 and r['M'] == 2 and r['m'] == 1 and r['poly'] == expect
          and H == 2 * m + 2 and rail == [2] and rung == [2 * m - 2])
    rows.append(dict(m=m, S=r['S'], P=r['P'], M=r['M'], cmin=r['m'], poly=r['poly'], H=H, rail=rail, rung=rung, ok=ok))
    print('prism', rows[-1]); sys.stdout.flush()
out['prisms'] = rows

# ---- tubes: full enumeration
def tube_root(p, L):
    return (0, 1, p + 1) if L >= 1 else (p, 0, 1)   # {v00,v01,v11}; L=0: {A,v00,v01}
rows = []
for p, Lmax, Hmax in ((4, 6, 6), (6, 4, 4)):
    for L in range(0, Lmax + 1):
        t = time.time()
        g = tube(p, L)
        inst = Inst(g, tube_root(p, L))
        r = inst.summary()
        row = dict(p=p, L=L, N=2 * (len(g) - 2), S=r['S'], det=det_states(inst), P=r['P'], M=r['M'], good_pairs=r['good_pairs'], cmin=r['m'], poly=r['poly'])
        if L <= Hmax:
            H, use = hamilton(inst)
            row['H'] = H
            if L >= 1:
                row['avoid'] = [H - use.get(frozenset(e), 0) for e in ((0, 1), (0, p + 1), (1, p + 1))]
        row['sec'] = round(time.time() - t, 1)
        rows.append(row); print('tube', row); sys.stdout.flush()
out['tubes'] = rows
json.dump(out, open('out_families.json', 'w'), indent=1, default=list)
