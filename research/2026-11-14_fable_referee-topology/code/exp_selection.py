"""Rainbow trees against selections from 2-factors of B.

Usage (from the repository root):
    python research/2026-11-14_fable_referee-topology/code/exp_selection.py VMIN VMAX
A 2-factor of B is a spanning subgraph with all degrees 2 (the union of a pair). A selection of
a 2-factor picks one of its two edges at every non-root. For every rooted instance the script
lists all 2-factors and all rainbow trees and compares the two families.
"""
import json
import sys
from collections import Counter
from itertools import product
from pathlib import Path

import etri
from rainbow import RB

vmin, vmax = int(sys.argv[1]), int(sys.argv[2])
cnt = Counter()
ex = []
for V, idx, f0, I in etri.all_rooted(vmin, vmax):
    rb = RB(I)
    trees = rb.all_trees()
    if not trees:
        continue
    X = rb.X
    n = I.n
    cnt['instances'] += 1
    states = I.states()
    # 2-factors as frozensets of (point, face) edges
    facs = set()
    for s in states:
        for r in I.mates(s):
            facs.add(frozenset([(s[i], I.A[i]) for i in range(n)] + [(r[i], I.A[i]) for i in range(n)]))
    facs = list(facs)
    cnt['two_factors'] += len(facs)
    tset = set(trees)
    opts = []
    sel_all = set()
    non_tree_sel = 0
    for F2 in facs:
        at = {x: [] for x in X}
        for (x, t) in F2:
            at[x].append(t)
        assert all(len(v) == 2 for v in at.values())
        for choice in product(*[at[x] for x in X]):
            sel_all.add(choice)
    non_tree_sel = len(sel_all - tset)
    not_sel = len(tset - sel_all)
    N = len(trees)
    cnt['rainbow_trees'] += N
    cnt['selections'] += len(sel_all)
    cnt['selections_not_trees'] += non_tree_sel
    cnt['trees_not_selections'] += not_sel
    cnt['families_equal'] += (non_tree_sel == 0 and not_sel == 0)
    cnt['unique_two_factor'] += (len(facs) == 1)
    cnt['unique_iff_N_pow2'] += ((len(facs) == 1) == (N == 2 ** n))
    cnt['every_tree_is_a_selection'] += (not_sel == 0)
    cnt['every_selection_is_a_tree'] += (non_tree_sel == 0)
    if (non_tree_sel or not_sel) and len(ex) < 6:
        ex.append({'V': V, 'plantri_index': idx, 'outer_face_vertices': list(I.R), 'two_factors': len(facs), 'N': N,
                   'selections': len(sel_all), 'selections_not_trees': non_tree_sel, 'trees_not_selections': not_sel})
out = {'command': 'python research/2026-11-14_fable_referee-topology/code/exp_selection.py %d %d' % (vmin, vmax),
       'result': {'range': [vmin, vmax], 'counts': dict(cnt), 'examples_where_families_differ': ex}}
(Path(__file__).resolve().parents[1] / 'data' / ('selection_%d_%d.json' % (vmin, vmax))).write_text(json.dumps(out, indent=1))
print(json.dumps(out['result'], indent=1))
