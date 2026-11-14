"""The 279 versus 213 discrepancy on paper/figures/running.json.

Recomputes |Omega| (and the first and second fixed sets, the signed sum) under:
  - the note's recorded layout (roots in stored face order -> (0,0),(100,0),(0,100), vertical rays, first generic shear);
  - the layout the lab's li.py builds (roots in the lab's networkx face order; same recipe);
  - all six assignments of the roots to the three anchor points;
  - 60 random generic ray directions on the note's layout.
Every row runs the full check() of check.py (involutions, signs, fixed sets, walk, moments).

Usage: python research/2026-11-14_opus_referee-involutions/code/running.py
"""
import itertools
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from ref import Inst, Maps  # noqa: E402
from check import check  # noqa: E402

d = json.loads((ROOT / 'paper/figures/running.json').read_text())
faces = [tuple(f) for f in d['faces']]
t0 = d['t0']
anchors = [(0, 0), (100, 0), (0, 100)]


def run(I, label, **kw):
    r = check(I, extra_k=False, **kw)
    r['label'] = label
    r['shear'] = I.shear
    r['direction'] = [str(x) for x in I.d]
    r['root_order'] = list(I.R)
    return r


rows = []
# 1. the note's layout
I = Inst(faces, t0, min_shear=1)
assert I.R == [0, 5, 4]
rows.append(run(I, 'note layout: stored root order 0,5,4, first shear >= 1'))
I0 = Inst(faces, t0)
rows.append(run(I0, 'same root order, first generic shear >= 0 (shear 0)'))
# the note's recorded coordinates, read from its JSON, for comparison of geometry only
geo = json.loads((ROOT / 'proofs/involutions/running-geometry.json').read_text())
from fractions import Fraction as Fr  # noqa: E402
same_pos = all(Fr(geo['pos'][str(v)][0]) == I.pos[v][0] and Fr(geo['pos'][str(v)][1]) == I.pos[v][1] for v in I.V)
# 2. the lab's root order
sys.path.insert(0, str(ROOT / 'workings/barnette_lab'))
import networkx as nx  # noqa: E402
from barnette_lab import Instance  # noqa: E402  (used only to read its face order)
g = nx.Graph()
for f in faces:
    g.add_edges_from(zip(f, f[1:] + f[:1]))
p0 = Instance(g)
outer = next(i for i, f in enumerate(p0.faces) if set(f) == set(faces[t0]))
lab_roots = list(Instance(g, outer).faces[outer])
perm = [lab_roots.index(v) for v in I.R]
I2 = Inst(faces, t0, root_pos=[anchors[perm[k]] for k in range(3)], min_shear=1)
rows.append(run(I2, f'lab li.py layout: lab root order {lab_roots}, first shear >= 1'))
# 3. all six root assignments
for pm in itertools.permutations(range(3)):
    I3 = Inst(faces, t0, root_pos=[anchors[pm[k]] for k in range(3)])
    rows.append(run(I3, f'root assignment {[I.R[k] for k in pm]} -> anchors, shear 0'))
# 4. random directions
rng = random.Random(20261114)
for k in range(60):
    while True:
        dv = (rng.randint(-50, 50), rng.randint(-50, 50))
        if dv != (0, 0):
            break
    try:
        I4 = Inst(faces, t0, direction=dv, shear_search=False)
    except ValueError:
        continue
    rows.append(run(I4, f'direction {dv}'))
keep = ['label', 'root_order', 'shear', 'direction', 'objects', 'fix1', 'fix2', 'signed', 'F', 'm', 'pairs', 'states', 'max_walk', 'tokens_per_pair', 'note_section7_sign_ok', 'moment_m']
out = dict(command='python research/2026-11-14_opus_referee-involutions/code/running.py',
           note_positions_reproduced=same_pos,
           rows=[{k: r[k] for k in keep} for r in rows])
(HERE / 'out' / 'running.json').write_text(json.dumps(out, indent=1, default=str))
for r in out['rows']:
    print(r['label'], '| shear', r['shear'], '| objects', r['objects'], '| fix1', r['fix1'], '| fix2', r['fix2'], '| signed', r['signed'])
objs = sorted({r['objects'] for r in out['rows']})
print('distinct object counts', objs, 'signed sums', sorted({r['signed'] for r in out['rows']}), 'positions reproduced', same_pos)
