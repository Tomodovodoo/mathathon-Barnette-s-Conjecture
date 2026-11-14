"""Average load and the slot identity over all rainbow trees of an instance.

Usage (from the repository root):
    python research/2026-11-14_fable_referee-topology/code/exp_average.py VMIN VMAX
For every rooted instance with a rainbow tree it checks
  (E) sum over all rainbow trees of c_t = N for every bounded black face t (mean load 1),
  (I) the slot identity c_t + a_t = 2 for every tree and face, a_t = number of points whose
      unique exchange target is t,
  and whether N = 2^n.
"""
import json
import sys
from collections import Counter
from pathlib import Path

import etri
from rainbow import RB

vmin, vmax = int(sys.argv[1]), int(sys.argv[2])
cnt = Counter()
bad = []
for V, idx, f0, I in etri.all_rooted(vmin, vmax):
    rb = RB(I)
    trees = rb.all_trees()
    if not trees:
        continue
    n = I.n
    N = len(trees)
    cnt['instances'] += 1
    tot = Counter()
    for s in trees:
        tot.update(s)
    E_ok = all(tot.get(t, 0) == N for t in I.A)
    groups = [dict() for _ in range(n)]
    for s in trees:
        for j in range(n):
            groups[j].setdefault(s[:j] + s[j + 1:], []).append(s[j])
    nice = True
    for s in trees:
        c = Counter(s)
        a = Counter()
        for j in range(n):
            g = groups[j][s[:j] + s[j + 1:]]
            a[g[0] if g[1] == s[j] else g[1]] += 1
        if any(c.get(t, 0) + a.get(t, 0) != 2 for t in I.A):
            nice = False
            break
    pow2 = (N == 2 ** n)
    seps = len(I.tri.separating_triangles())
    cnt['mean_load_is_1'] += E_ok
    cnt['slot_identity_all_trees'] += nice
    cnt['N_is_2^n'] += pow2
    cnt['slot_iff_pow2'] += (nice == pow2)
    cnt['slot_fails_nosep' if (not nice and seps == 0) else 'slot_fails_sep' if not nice else 'slot_ok'] += 1
    if not E_ok and len(bad) < 5:
        bad.append({'V': V, 'plantri_index': idx, 'outer_face_vertices': list(I.R), 'N': N,
                    'sum_loads': [tot.get(t, 0) for t in I.A]})
out = {'command': 'python research/2026-11-14_fable_referee-topology/code/exp_average.py %d %d' % (vmin, vmax),
       'result': {'range': [vmin, vmax], 'counts': dict(cnt), 'mean_load_failures': bad}}
p = Path(__file__).resolve().parents[1] / 'data' / ('average_%d_%d.json' % (vmin, vmax))
p.write_text(json.dumps(out, indent=1))
print(json.dumps(out['result'], indent=1))
