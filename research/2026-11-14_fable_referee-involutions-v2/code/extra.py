"""Remaining displayed signs and one witness of Section 7.

    python research/2026-11-14_fable_referee-involutions-v2/code/extra.py
(a) On every paired root through 14 vertices (plantri input): every cycle of D_p is odd, its delta-sum is
    -3 counterclockwise and +3 clockwise, J = clockwise - counterclockwise, J = c = n mod 2, and
    delta(u,s) - delta(r,s) = 2 delta(r,u) in every face of every pair.
(b) 11-vertex class 1 root 0 of the canonical census, in the note's drawing: objects at which the second
    map takes the interior nonfirst branch.
Output: code/out/extra.json
"""
import sys, json
from fractions import Fraction as Fr
from collections import Counter
from pathlib import Path
HERE = Path(__file__).parent; ROOT = HERE.resolve().parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / 'research/2026-11-14_fable_route-combinatorics/lab'))
from fp import plantri, trace_faces, Inst, Model
from tri import enumerate_classes, from_code
res = Counter()
for v in range(6, 15):
    for rot in plantri(v):
        faces = trace_faces(rot)
        for root in range(len(faces)):
            I = Inst(faces, root)
            for p in I.pairs():
                r, s = p; res['pairs'] += 1
                cw = ccw = 0
                for C in I.dcycles(p):
                    ins, is_ccw = I.cyc_info(p, C)
                    assert len(C) % 2 == 1
                    assert sum(I.delta(r[k], s[k]) for k in C) == (-3 if is_ccw else 3)
                    assert any(f in I.white for f in ins)
                    ccw += is_ccw; cw += not is_ccw; res['cycles'] += 1
                assert I.J(p) == cw - ccw and (I.J(p) - I.n) % 2 == 0 and (cw + ccw - I.n) % 2 == 0
                for k in range(I.n):
                    u = I.third(k, r[k], s[k])
                    assert I.delta(u, s[k]) - I.delta(r[k], s[k]) == 2 * I.delta(r[k], u)
out = {'a': dict(res)}
levels = enumerate_classes(11)
faces = from_code(sorted(levels[11])[1]).faces
I = Inst(faces, 0)
a, b, c = faces[0]
pos = I.tutte({a: (Fr(0), Fr(0)), b: (Fr(100), Fr(0)), c: (Fr(0), Fr(100))})
for k in range(1, 10000):
    sh = {u: (z[0] + k * z[1], z[1]) for u, z in pos.items()}
    cr, ori = I.ray_crossings(sh, (Fr(0), Fr(1)))
    if cr is not None:
        break
if ori < 0:
    I = Inst([(x, z, y) for (x, y, z) in faces], 0); cr, ori = I.ray_crossings(sh, (Fr(0), Fr(1)))
M = Model(I, cr); cnt = Counter()
for o in M.objects():
    tr = []; b2 = M.iota2(o, tr)
    if b2 == o or tr[0] == 'unmarked':
        continue
    p, Mk = o
    allin = all(w in I.cyc_info(p, next(C for C in M.cyc[p] if cr[w][i][0] in C))[0] for (w, i) in Mk)
    cnt[('interior nonfirst ' if allin else 'exterior ') + tr[0]] += 1
out['b'] = {'m': M.m, 'objects': sum(1 for _ in M.objects()), 'branches': dict(cnt)}
print(out)
json.dump(out, open(HERE / 'out/extra.json', 'w'), indent=1)
