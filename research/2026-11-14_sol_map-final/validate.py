from pathlib import Path
import json,re,sys,hashlib
from collections import Counter
sys.path.insert(0,'digestions/route-map');import routes as rt
out=Path('research/2026-11-14_sol_map-final')
owned=[Path('digestions/steps/00-overview.md'),Path('digestions/steps/09-what-is-still-open.md')]+list(Path('digestions/route-map').glob('*.md'))+list(Path('labyrinth').rglob('*.md'))+list(out.glob('*.md'))
bad=[];checked=0
for p in owned:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
  target=target.strip('<>')
  if target.startswith(('http:','https:','mailto:','data:','#')):continue
  f=target.split('#')[0].split('?')[0]
  if not f:continue
  checked+=1
  if not (p.parent/f).exists():bad.append([str(p),target])
# All deliverable links must now resolve.
assert not bad,bad
status=Counter(r['status'] for r in rt.R)
kinds=Counter(rt.KIND_OF.get(r['id'],'computation') for r in rt.R)
# Matrix omits computations by design. Keep both totals explicit.
matrix=Counter(rt.KIND_OF[r['id']] for r in rt.R if r['status']!='COMPUTED')
d=json.loads(Path('research/2026-11-14_fable_descent/data/census_summary.json').read_text())
sums={k:sum(v[k] for v in d['totals'].values() if v['V']<=22) for k in ('pairs','rooted_with_pair','tree_pairs')}
assert sums['pairs']==49325864 and sums['rooted_with_pair']==4656948
assert all(sum(x['khist'].values())==x['pairs'] for x in d['totals'].values())
assert all(x['trap1']==0 for v,x in d['potentials']['k'].items() if int(v)<=22)
walk=json.loads(Path('research/2026-11-14_fable_referee-topology/data/walk_exhaust_13_14_all.json').read_text())['result']['counts']
assert walk['instances']==672
# Enumerate the elementary two-cover arithmetic separately from its planar hypotheses.
for j in range(8):
 for c1 in range(j+1,10):
  for c2 in range(j+1,10):
   for a in (0,2**j):
    M=2**c1+2**c2-2*a
    assert M>=2**min(c1,c2)
    if M==2**min(c1,c2):assert c1==c2==j+1 and a==2**j
scans={}
for tag in ['fable_descent','astra_lean-check','sol_referee-main-v2','opus_coldread-main-v2','fable_referee-involutions-v2','opus_two-tree-packing','astra_induction-lemmas']:
 p=Path('research/2026-11-14_'+tag+'/REPORT.md');scans[str(p)]={'exists':p.exists(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None}
result={'total_routes':len(rt.R),'routes_by_status':dict(status),'routes_by_kind_including_computations':dict(kinds),'matrix_routes_by_kind_excluding_computations':dict(matrix),'local_links_checked':checked,'broken_local_links':bad,'late_reports':scans,'spot_checks':{'descent_totals':sums,'descent_no_closed_plateau_through':22,'two_cover_arithmetic':'j=0..7; j<c1,c2<=9; a=0 or 2^j; weak bound and equality condition pass','scope':'Retained outputs and elementary arithmetic, not independent enumeration or full proof review.'}}
(out/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf8')
lines=['# Final route counts','','From routes.py. Reproduce with `python -X utf8 -B research/2026-11-14_sol_map-final/validate.py`.','','| Status | Routes |','|---|---:|']
for k in rt.STATUS_ORDER:lines.append(f'| {k} | {status[k]} |')
lines+=['| Total | '+str(len(rt.R))+' |','','| Kind | All routes | Non-computed matrix routes |','|---|---:|---:|']
for k in list(dict(rt.KINDS))+['computation']:lines.append(f'| {k} | {kinds[k]} | {matrix[k]} |')
lines+=['','The matrix excludes all COMPUTED entries, including those assigned a mathematical kind. The computation row contains checks with no mathematical-kind assignment.']
(out/'COUNTS.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print(json.dumps(result,indent=2))
