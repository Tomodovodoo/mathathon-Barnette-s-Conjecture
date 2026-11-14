from pathlib import Path
import re,json,sys
sys.path.insert(0,'digestions/route-map')
import routes
from collections import Counter
files=['digestions/steps/09-what-is-still-open.md','digestions/steps/00-overview.md','labyrinth/README.md','digestions/route-map/HOW-IT-WORKS.md']
bad=[]
for fn in files:
 for target in re.findall(r'\]\(([^)]+)\)',Path(fn).read_text(encoding='utf8')):
  if not target.startswith(('https:','http:','#')) and not (Path(fn).parent/target.split('?')[0]).exists():bad.append([fn,target])
print('broken local links',bad)
scan={}
for folder in ['astra_induction-lemmas','opus_two-tree-packing','sol_referee-main','fable_coldread-main','opus_referee-involutions']:
 p=Path('research/2026-11-14_'+folder+'/REPORT.md');scan[str(p)]=p.exists()
result={'route_counts':dict(Counter(r['status'] for r in routes.R)),'total_routes':len(routes.R),'broken_local_links':bad,'final_report_scan':scan}
Path('research/2026-11-14_sol_map-update/validation.json').write_text(json.dumps(result,indent=2))
assert not bad
