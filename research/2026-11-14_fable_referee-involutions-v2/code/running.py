"""The running example: every number of Section 9 and of Figures 1 to 3, recomputed.

Run from the repository root:
    python research/2026-11-14_fable_referee-involutions-v2/code/running.py
Output: code/out/running.json
"""
import sys, json, re, math
from fractions import Fraction as Fr
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from fp import Inst, Model
from census import all_checks

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent / 'out'
src = json.load(open(ROOT / 'paper/figures/running.json'))
assert src == json.load(open(ROOT / 'proofs/involutions/running.json')), 'copied input differs'
geo = json.load(open(ROOT / 'proofs/involutions/running-geometry.json'))
pos = {int(k): (Fr(v[0]), Fr(v[1])) for k, v in geo['pos'].items()}
cen = {int(k): (Fr(v[0]), Fr(v[1])) for k, v in geo['centers'].items()}
res = {}

# The stored triples are clockwise in the note's layout (roots 0, 5, 4 at (0,0), (100,0), (0,100) before the shear).
stored = [tuple(f) for f in src['faces']]
mirror = [(a, c, b) for (a, b, c) in stored]
I = Inst(mirror, src['t0'])
assert sorted(I.A) == [0, 2, 7, 9, 11, 13, 15, 17, 19, 21]
for t in I.A:                                   # centres are barycentres
    assert cen[t] == tuple(sum(pos[v][i] for v in I.faces[t]) / 3 for i in (0, 1))
cr, ori = I.ray_crossings(pos, (Fr(0), Fr(1)), cen)
assert cr is not None and ori == 1, 'the layout is generic and matches the mirrored triples'
rec = all_checks(I, cr, 1, None, False)
M = Model(I, cr)
res['note layout'] = rec
print('note layout', rec)
assert len(I.states) == 12 and len(M.pairs) == 8 and rec['m'] == 2 and rec['objects'] == 279
assert rec['fix2'] == 9 and rec['signed'] == -9 and rec['F'] == 9
n, m = I.n, 2
assert (-1) ** ((n + m) // 2) * rec['F'] == 9          # normalized lowest coefficient
objs = list(M.objects())
fix2 = [o for o in objs if M.iota2(o) == o]
assert all(M.sign(o) == -1 and M.iota1(o) == o for o in fix2)   # all negative, all first-fixed

# ---- the printed table, parsed from the TeX
tex = open(ROOT / 'proofs/involutions/example-table.tex').read()
st = {int(a): tuple(int(x) for x in b.split(',')) for a, b in re.findall(r'^(\d+) & \$([\d,]+)\$\\\\', tex, re.M)}
assert len(st) == 12 and set(st.values()) == set(I.states)
pr = {int(a): (st[int(b)], st[int(c)]) for a, b, c in re.findall(r'^(\d+) & (\d+) & (\d+)\\\\', tex, re.M)}
assert len(pr) == 8 and set(pr.values()) == set(M.pairs)
rows = re.findall(r'^(\d+) & (\d+) & \$([\d:,]+)\$ & ([+-]) & (\d+) & (\d+)\\\\', tex, re.M)
assert len(rows) == 279
def key(o):                                     # a token w:t names the s-spoke of face t crossed by the ray of w
    p, Mk = o
    return (p, frozenset((w, I.A[cr[w][i][0]]) for (w, i) in Mk))
mine = {key(o): o for o in objs}
assert len(mine) == 279
tab = {}
for oid, pid, toks, sg, i1, i2 in rows:
    tab[int(oid)] = ((pr[int(pid)], frozenset(tuple(int(x) for x in t.split(':')) for t in toks.split(','))), sg, int(i1), int(i2))
assert {k for k, *_ in tab.values()} == set(mine)
bad = 0
for oid, (k, sg, i1, i2) in tab.items():
    o = mine[k]
    bad += (M.sign(o) == 1) != (sg == '+')
    bad += key(M.iota1(o)) != tab[i1][0]
    bad += key(M.iota2(o)) != tab[i2][0]
assert bad == 0
res['table'] = 'all 279 rows agree: object, sign, iota1, iota2; 12 states and 8 pairs agree'
print(res['table'])

# ---- Figures 1 and 2: object 1 and its second image
o1 = mine[tab[1][0]]
tr = []
img = M.iota2(o1, tr)
res['figure 2'] = {'object': 1, 'tokens': sorted(tab[1][0][1]), 'image id': tab[1][3], 'branch': tr[0],
                   'tokens of image': sorted(key(img)[1]),
                   'cycles': [[I.A[k] for k in C] for C in M.cyc[o1[0]]]}
print('figure 2', res['figure 2'])
# a move of the other kind in the same drawing, for a replacement figure
cands = []
for o in objs:
    tr = []
    b = M.iota2(o, tr)
    if b != o and tr[0] != 'unmarked':
        cands.append((tr[0], [oid for oid, v in tab.items() if v[0] == key(o)][0], sorted(key(o)[1]), sorted(key(b)[1])))
res['token moves'] = Counter(c[0] for c in cands)
res['token move examples'] = cands[:12]
print('token moves', res['token moves'], cands[:6])

# ---- Figure 3: the increasing-ID breadth-first face tree
paths = I.tree_paths('bfs+')
pc = I.path_crossings(paths)
fig3 = {}
for w in (6, 18):
    fig3[w] = {'path': paths[w], 'turns': [(I.A[k], v, -a) for (k, v, a, _) in pc[w]]}
res['figure 3'] = fig3
print('figure 3', fig3)
assert paths[6] == [6, 0, 5, 4] and paths[18] == [18, 7, 6, 0, 5, 4]
assert fig3[6]['turns'] == [(0, 6, 1)] and fig3[18]['turns'] == [(7, 7, 1), (0, 6, 1)]
for kind in ('bfs+', 'bfs-', 'dfs', 'rand', 'walk'):
    r = all_checks(I, I.path_crossings(I.tree_paths(kind, 5)), 1, None, True)
    res['paths ' + kind] = r
    print('paths', kind, {k: r[k] for k in ('objects', 'fix1', 'fix2', 'signed', 'walks')})
    assert r['fix2'] == 9 and r['signed'] == -9

# ---- orientation of the main paper's drawing of the same example
# paper/main Figure "pair": D(beta, alpha) has a counterclockwise 7-cycle 6,1,2,3,9,10,11 and a clockwise triangle 8,7,12.
Im = Inst(stored, src['t0'])
Mm = Model(Im, Im.path_crossings(Im.tree_paths('bfs+')))
hits = []
for p in Mm.pairs:
    r, s = p
    nxt = dict(zip(r, s))
    if all(nxt[a] == b for a, b in zip([6, 1, 2, 3, 9, 10, 11], [1, 2, 3, 9, 10, 11, 6])) and nxt[8] == 7 and nxt[7] == 12:
        for C in Mm.cyc[p]:
            hits.append((len(C), Im.cyc_info(p, C)[1]))
res['main paper orientation'] = {'pair (beta, alpha) in stored orientation: (length, counterclockwise)': sorted(hits)}
print(res['main paper orientation'])
assert sorted(hits) == [(3, False), (7, True)], 'stored triples are counterclockwise in the main paper drawing'
# Table 2 of the main paper: epsilon and omega for shortest paths
tabm = sorted((math.prod(Im.delta(p[0][k], p[1][k]) for k in range(Im.n)),
               sum(-a for w in Im.white for (k, v, a, _) in Mm.cr[w] if p[1][k] == v)) for p in Mm.pairs)
res['main paper (eps, omega), bfs+ paths'] = tabm
print('main paper (eps, omega):', tabm)
sig = sum(e * w * w for e, w in tabm)
assert sig == 18
# the step f6 -> f0 -> f5 of Figure 3, in the main paper's orientation
k0 = [(-a) for (k, v, a, _) in Mm.cr[6] if Im.A[k] == 0]
res['kappa at (f0, corner 6) on the path of w6: note layout, main paper drawing'] = [1, k0[0]]
print('kappa at f0 corner 6: note +1, main paper', k0[0])
json.dump(res, open(OUT / 'running.json', 'w'), indent=1, default=str)
