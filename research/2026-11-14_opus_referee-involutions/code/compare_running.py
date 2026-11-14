"""Compare the note's published 279-object table (proofs/involutions/running-objects.json)
object by object with this referee's independent computation in the same layout.
Also lists what the 213-object lab layout and the 279-object note layout have in common.

Usage: python research/2026-11-14_opus_referee-involutions/code/compare_running.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from ref import Inst, Maps  # noqa: E402

d = json.loads((ROOT / 'paper/figures/running.json').read_text())
faces = [tuple(f) for f in d['faces']]
t0 = d['t0']
I = Inst(faces, t0, min_shear=1)
P = I.pairs()
mp = Maps(I, P)
mine = {o: k for k, o in enumerate(mp.objects())}
pub = json.loads((ROOT / 'proofs/involutions/running-objects.json').read_text())


def key(row):
    p = (tuple(row['pair'][0]), tuple(row['pair'][1]))
    return (p, frozenset(tuple(x) for x in row['marks']))


pubkeys = [key(r) for r in pub]
assert len(set(pubkeys)) == len(pubkeys) == 279
same_set = set(pubkeys) == set(mine)
bad = []
for r, k in zip(pub, pubkeys):
    if I.sign(*k) != r['sign']:
        bad.append(('sign', r['id']))
    if mp.iota1(k) != pubkeys[r['iota1']]:
        bad.append(('iota1', r['id']))
    if mp.iota2(k)[0] != pubkeys[r['iota2']]:
        bad.append(('iota2', r['id']))
# the 213 layout
anchors = [(0, 0), (100, 0), (0, 100)]
lab_roots = [0, 4, 5]
perm = [lab_roots.index(v) for v in I.R]
L = Inst(faces, t0, root_pos=[anchors[perm[k]] for k in range(3)], min_shear=1)
ml = Maps(L, P)
lab = set(ml.objects())
tok_note = {p: set(mp.toks(p)) for p in P}
tok_lab = {p: set(ml.toks(p)) for p in P}
per_pair = []
for j, p in enumerate(P):
    per_pair.append(dict(pair=j, tokens_note=len(tok_note[p]), tokens_lab=len(tok_lab[p]),
                         common=len(tok_note[p] & tok_lab[p]),
                         objects_note=sum(1 for o in mine if o[0] == p),
                         objects_lab=sum(1 for o in lab if o[0] == p),
                         m_cycles=len(I.dcycles(p))))
fix2_note = {o for o in mine if mp.iota2(o)[0] == o}
fix2_lab = {o for o in lab if ml.iota2(o)[0] == o}
# second-fixed objects as (pair, set of white faces): layout-free data?
proj = lambda S: sorted((str(o[0]), sorted(w for w, i in o[1])) for o in S)
out = dict(command='python research/2026-11-14_opus_referee-involutions/code/compare_running.py',
           published_set_equals_mine=same_set, mismatches=bad,
           objects_note=len(mine), objects_lab=len(lab), objects_common=len(set(mine) & lab),
           per_pair=per_pair,
           fix2_note_eq_fix2_lab_as_objects=fix2_note == fix2_lab,
           fix2_note_eq_lab_after_forgetting_spokes=proj(fix2_note) == proj(fix2_lab),
           fix2_note=[(P.index(o[0]), sorted(o[1])) for o in fix2_note],
           fix2_lab=[(P.index(o[0]), sorted(o[1])) for o in fix2_lab])
(HERE / 'out' / 'compare-running.json').write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({k: v for k, v in out.items() if k not in ('per_pair', 'fix2_note', 'fix2_lab')}, indent=1))
for row in per_pair:
    print(row)
