"""Which outer face t0 of the 14-vertex triangulation gives the best example?
For every face as t0: root degrees, states, pairs, cyclic pairs, and whether some
pair has a D-cycle or a reversible Q-cycle with a strictly interior vertex.
Run: python research/2026-11-14_fable_figures-review/explore_roots.py
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'paper' / 'figures'))
from model import Model
d = json.loads((ROOT / 'paper' / 'figures' / 'example.json').read_text())
rows = []
for t0 in range(len(d['faces'])):
    m = Model(d['faces'], t0)
    st = m.states(); ps = m.pairs(st)
    cyc = [(r, s) for r, s in ps if not m.Q_is_forest(s)]
    forest_states = {s for r, s in ps if m.Q_is_forest(s)}
    dI = qI = 0; best = None
    for r, s in ps:
        for c in m.directed_cycles(m.D(r, s)):
            k = m.disk(c)
            assert k['B'] + k['W'] == 2 * k['I'] + k['h'] - 2 and k['B'] == k['I'] + k['l']
            assert k['delta_sum'] == (-3 if k['ccw'] else 3)
            if k['I'] >= 1: dI += 1
        if not m.Q_is_forest(s):
            for c in m.directed_cycles(m.Q_directed(r, s)):
                k = m.disk(c)
                assert k['delta_sum'] == (-3 if k['ccw'] else 3)
                if k['I'] >= 1: qI += 1
    rows.append(dict(t0=t0, face=m.F[t0], deg=[m.T.degree(v) for v in m.roots], states=len(st), pairs=len(ps),
                     cyclic=len(cyc), cyclic_states=len({s for r, s in cyc}), forest_states=len(forest_states), D_I=dI, Q_I=qI))
    print(rows[-1], flush=True)
(Path(__file__).parent / 'explore_roots.json').write_text(json.dumps(rows, indent=1))
