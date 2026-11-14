from pathlib import Path
import json,collections
root=Path.cwd(); out=root/'research/2026-11-14_sol_digest-fixes'
p=root/'digestions/route-map/routes.py';s=p.read_text();s+='''
_upd('R.x1',label='acyclic Q_s alone is enough',text='Every state with acyclic Q_s is good, without requiring a partner or one root per component.',lesson='Acyclicity without a partner is insufficient. The final definition of good state includes one root per component; good states themselves do suffice for recovery.')
_upd('E.1',label='tree of faces by duality',text='The complement of S_s gives the dual tree Y_s of faces. Suppressing its degree-two black nodes recovers the older white-face tree.',where='paper/main/barnette.tex Lemma 3.6; O Lemma 2.1; L Cor. 27; T 7.1')
_upd('E2.1',label='root Y_s at t0',text='Each black face selects its side shared with its child in Y_s rooted at t0. This is the same selection as the older white-tree orientation.',where='paper/main/barnette.tex Lemma 3.6; O 6.1; L Claim 31; T 7.1')
_upd('U.7h',where='+; rr/REPORT.md; rr/data/stepx_18_1542-1541-103-104-105-106-107-108-109-11.json',text='Step X asks that every point-rainbow tree reach a good state without increasing black-face excess, using both plateau move types. Author checks all roots through V=17 and 1,485 of 1,543 graphs at V=18. Independent referee checks through V=12 and completes seven more V=18 graphs, all 224 roots and 7,999,488 enumerated multi-cover rainbow trees. Fifty-one graphs remain incomplete, with some roots of one tested. This is finite evidence; Step X is open.',test='Complete the remaining V=18 graphs; prove every positive-excess component has an exit. Do not confuse this excess with q(s).')
''';p.write_text(s,encoding='utf8')
# Recompute the new completed-graph counts from rows, excluding partial graph 108.
p=root/'research/2026-11-14_opus_referee-rainbow/data/stepx_18_1542-1541-103-104-105-106-107-108-109-11.json'
data=json.loads(p.read_text()); rows=[r for r in data['rows'] if isinstance(r[0],int) and r[0]!=108]
print('rows sample',rows[:1]);print('rows lengths',collections.Counter(map(len,rows)))
print('complete indices',sorted({r[0] for r in rows}), 'rows',len(rows))
print('sum trees',sum(r[3] for r in rows))
nums=json.loads((out/'numbers.json').read_text()); nums['rainbow_completed_graphs']=len({r[0] for r in rows});nums['rainbow_completed_roots']=len({r[0] for r in rows})*(2*18-4);nums['rainbow_completed_multi_trees']=sum(r[3] for r in rows)
assert nums['rainbow_completed_roots']==224 and nums['rainbow_completed_multi_trees']==7999488
(out/'numbers.json').write_text(json.dumps(nums,indent=2)+'\n')
p=root/'digestions/steps/09-what-is-still-open.md';s=p.read_text().replace('the referee independently reaches $V=12$.', 'the referee independently reaches $V=12$ and completes seven more $V=18$ graphs, leaving 51 incomplete. Their 224 roots include 7,999,488 enumerated rainbow trees in the multiple-cover cases, re-summed in [our arithmetic check](../../research/2026-11-14_sol_digest-fixes/numbers.json).');p.write_text(s,encoding='utf8')
