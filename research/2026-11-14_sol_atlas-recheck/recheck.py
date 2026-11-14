"""Run from repository root: python -X utf8 research/2026-11-14_sol_atlas-recheck/recheck.py.

Independent recount and saved-data reconciliation, no atlas figure imports.
Does not rerun the underlying graph censuses or check Lean propositions.
"""
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf8'))

b = read('proofs/blueprint/blueprint.json')
nodes = {n['id']: n for n in b['nodes']}
route = b['analysis']['skeleton']
assert len(route) == len(set(route)) == 34
groups = {k: sorted(i for i in route if nodes[i]['status'] == k)
          for k in ('exact', 'translation', 'weaker', 'none')}
assert {k: len(v) for k, v in groups.items()} == dict(exact=5, translation=17, weaker=10, none=2)
table = (ROOT / 'research/2026-11-14_opus_lean-integration/STATUS-TABLE.md').read_text(encoding='utf8')
labels = {'exact': '**exact**', 'translation': '**after translation**',
          'weaker': '**weaker / different**', 'none': '**none**'}
for k, ids in groups.items():
    for i in ids:
        row, = [r for r in table.splitlines() if r.startswith('| ') and f'`{i}`' in r]
        assert labels[k] in row, (i, k)

g = read('research/2026-11-14_astra_induction-lemmas/data/g_structure_8_19.json')['per_V']
assert sum(r.get('rooted', 0) for r in g.values()) == 62416
assert max(map(int, g)) == 19
# The source code asserts any(any(v) for v in good.values()) for every root, V>6.
ind = (read('research/2026-11-14_astra_referee-descent/code/induction_6_16.json')
       + read('research/2026-11-14_astra_referee-descent/code/induction_17_18.json'))
assert sum(r.get('contractions', 0) for r in ind) == 1202792
assert sum(r.get('exceptions', 0) for r in ind) == 7940
assert max(r['V'] for r in ind) == 18
assert all(r.get(k, 0) == 0 for r in ind for k in ('half_fail', 'bijection_fail', 'inequality_fail'))

c = read('digestions/atlas/computed.json')
assert c['blueprint']['counts'] == {k: len(v) for k, v in groups.items()}
for k, ids in groups.items():
    assert c['blueprint'][k if k != 'none' else 'no_counterpart'] == ids
bars = c['open']['open_statements']
assert [(r['every_case_two_programs'], r['every_case_one_program'], r['sampled_to']) for r in bars] == [
    (22, 22, 100), (16, 24, None), (20, 23, 200), (12, 17, 120), (19, 19, None), (18, 18, None)]
assert [r['counterexample_at'] for r in c['open']['refuted']] == [12,18,18,24,33,33,33,38]
assert [r['known_smallest'] for r in c['open']['refuted']] == [False,True,True,False,False,False,False,False]
result = dict(command=__doc__.splitlines()[0], route_groups=groups,
              route_counts={k: len(v) for k,v in groups.items()},
              G_saved_roots=62416, induction_saved_contractions=1202792,
              induction_saved_exceptions=7940, chart_matches=True)
(OUT / 'recheck.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8')
print(json.dumps(result, indent=2))
