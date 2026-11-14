"""Reproduce the numbers printed in the note in its own encoding, with this folder's code.

The canonical census of research/2026-11-14_fable_route-combinatorics/lab/tri.py is used as an
input generator only (class order and face IDs). Layout recipe of the note: Tutte drawing with the
corners of faces[root] at (0,0), (100,0), (0,100), then the first positive integer shear
x -> x + k*y that makes every vertical ray generic.

    python research/2026-11-14_fable_referee-involutions-v2/code/canonical.py VMAX [RAY_VMAX]
Output: code/out/canonical-VMAX.json
"""
import sys, json, time
from fractions import Fraction as Fr
from collections import Counter
from pathlib import Path
HERE = Path(__file__).parent
ROOT = HERE.resolve().parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / 'research/2026-11-14_fable_route-combinatorics/lab'))
from tri import enumerate_classes, from_code
from fp import Inst, Model
from census import all_checks

vmax = int(sys.argv[1]); ray_vmax = int(sys.argv[2]) if len(sys.argv) > 2 else vmax
levels = enumerate_classes(vmax)
tot = Counter(); wit = {}; t0 = time.time()
WIT = {(9, 0, 0), (12, 0, 0), (14, 27, 0), (11, 1, 0)}
for v in sorted(levels):
    if v > vmax:
        continue
    for cls, code in enumerate(sorted(levels[v])):
        tot['classes'] += 1
        faces = from_code(code).faces
        for root in range(len(faces)):
            tot['roots'] += 1
            I = Inst(faces, root)
            if not I.pairs():
                continue
            tot['paired'] += 1
            ref = None
            for mode in ('bfs+', 'bfs-'):
                rec = all_checks(I, I.path_crossings(I.tree_paths(mode)), 1, None, True)
                tot[mode + ':objects'] += rec['objects']; tot[mode + ':fix2'] += rec['fix2']
                tot[mode + ':fix1'] += rec['fix1']
                tot[mode + ':mplus1_zero'] += rec['mplus1'] == 0
                tot[mode + ':maxwalk'] = max(tot[mode + ':maxwalk'], max(rec['walks']))
                ref = ref or (rec['m'], rec['F'], rec['signed'])
                assert ref == (rec['m'], rec['F'], rec['signed'])
            tot['m=%d' % ref[0]] += 1
            if v <= ray_vmax:
                a, b, c = faces[root]
                pos = I.tutte({a: (Fr(0), Fr(0)), b: (Fr(100), Fr(0)), c: (Fr(0), Fr(100))})
                for k in range(1, 10000):
                    sh = {u: (z[0] + k * z[1], z[1]) for u, z in pos.items()}
                    cr, ori = I.ray_crossings(sh, (Fr(0), Fr(1)))
                    if cr is not None:
                        break
                J = I
                if ori < 0:                       # the drawing shows the stored triples clockwise
                    J = Inst([(x, z, y) for (x, y, z) in faces], root)
                    cr, ori = J.ray_crossings(sh, (Fr(0), Fr(1)))
                    assert ori == 1
                rec = all_checks(J, cr, 1, None, False)
                assert ref == (rec['m'], rec['F'], rec['signed'])
                tot['ray:objects'] += rec['objects']; tot['ray:fix2'] += rec['fix2']; tot['ray:fix1'] += rec['fix1']
                tot['ray:mplus1_zero'] += rec['mplus1'] == 0
                for L, cnt in rec['walks'].items():
                    tot['ray:walk%d' % L] += cnt
                if (v, cls, root) in WIT:
                    sep = False
                    V = sorted({x for f in faces for x in f}); E = {frozenset(e) for f in faces for e in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2]))}
                    FS = {frozenset(f) for f in faces}
                    for i, x in enumerate(V):
                        for y in V[i + 1:]:
                            for z in V:
                                if z > y and {frozenset((x, y)), frozenset((y, z)), frozenset((x, z))} <= E and frozenset((x, y, z)) not in FS:
                                    sep = True
                    wit['%d-vertex class %d root %d' % (v, cls, root)] = dict(m=rec['m'], objects=rec['objects'], fix2=rec['fix2'],
                                                                             branch=rec['branch'], separating_triangle=sep)
    print(f'v<={v}', dict(tot), f'[{time.time()-t0:.0f}s]', flush=True)
print(wit)
json.dump({'command': 'canonical.py %d %d' % (vmax, ray_vmax), 'totals': dict(tot), 'witnesses': wit},
          open(HERE / 'out' / f'canonical-{vmax}.json', 'w'), indent=1)
