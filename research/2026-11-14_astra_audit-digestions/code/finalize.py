from pathlib import Path
import subprocess,json,hashlib
R=Path.cwd();A=R/'research/2026-11-14_astra_audit-digestions';O=A/'outputs'
p=A/'AUDIT.md';s=p.read_text(encoding='utf8').replace('C2 <- R2 AND(C3, C4, C5, C6)','C2 <- R2 AND(C3, C4, C5, C6, O13, O14, O15, O16)');p.write_text(s,encoding='utf8')
# Retain the pre-audit SOTA row as history, including status-only improvements.
base=json.loads(subprocess.check_output(['git','show','50a7556^:labyrinth/sota.json'],text=True,encoding='utf8'))
p=R/'labyrinth/sota.json';now=json.loads(p.read_text());old={r['id']:r for r in base['entries']}
for r in now['entries']:
 if r['id'] in old:
  q=old[r['id']]
  if (q['result'],q['status'])!=(r['result'],r['status']):
   entry={'date':'2026-11-14','was':q['result'],'status':q['status']}
   if entry not in r.setdefault('previous',[]):r['previous'].append(entry)
p.write_text(json.dumps(now,indent=1),encoding='utf8')
cmds=[['python','-X','utf8','-B',str(A/'code'/f)] for f in ['verify.py','extended.py','details.py','recovery.py']]+[['python','-X','utf8','-B','digestions/route-map/build_map.py'],['python','-X','utf8','-B','labyrinth/seed.py'],['python','-X','utf8','-B','labyrinth/lab.py','check'],['python','-X','utf8','-B','labyrinth/lab.py','build']]
with (O/'final-checks.log').open('w',encoding='utf8') as log:
 for cmd in cmds:
  proc=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8');log.write('COMMAND '+subprocess.list2cmdline(cmd)+'\nEXIT '+str(proc.returncode)+'\n'+proc.stdout+proc.stderr+'\n');assert proc.returncode==0,proc.stderr
paths=['digestions/steps','digestions/route-map','labyrinth']
patch=subprocess.check_output(['git','diff','50a7556^','--',*paths]);(O/'canonical-changes.patch').write_bytes(patch)
files=subprocess.check_output(['git','diff','--name-only','50a7556^','--',*paths],text=True).splitlines()
files+=['digestions/steps/img/two-covers.png','digestions/steps/img/bad-cover-16.png']
manifest={f:{'sha256':hashlib.sha256((R/f).read_bytes()).hexdigest(),'bytes':(R/f).stat().st_size} for f in sorted(set(files)) if (R/f).is_file()}
(O/'snapshot.json').write_text(json.dumps(manifest,indent=2))
lines=['# Change log','','Exact textual edits are in outputs/canonical-changes.patch. That patch covers all tracked canonical edits against the parent of audit commit 50a7556; the two new PNGs are listed below. Replacement-level prose ledgers are outputs/edits.json and outputs/reader-edits.json. One-time migration scripts preserve subsequent route, status and wording edits.','','## Changes by purpose','','- Steps 00–09 and glossary: findings A01–A11, A21, A23, A25–A27; ten reader bridges; explicit Li fixed-point data and orientation comparison.','- HOW-IT-WORKS: corrected modular-count scope, cycle signs, Li mark multiplicities, lattice status and the meaning of route labels.','- routes.py: added new manuscript, family and older-approach routes; corrected LP and matroid claims; integrated the late topology referee and provisional lattice refutation.','- build_map.py: source/shared/choice labels and proof-supplied matrix legend; regenerated every map, overview, matrix, DOT, JSON and written inventory.','- seed.py: preprint tier policy, claim-specific reviews, append-only event preservation, SOTA history and new manuscript row.','- labyrinth data, STATUS and dashboard: regenerated from canonical sources. README tier explanation corrected. Existing frontier data unchanged.','- Two new step figures: generated from the figure toolkit without editing paper/figures.','','## Every changed canonical file','','| File | Bytes | SHA-256 |','|---|---:|---|']
for f,m in manifest.items():lines.append(f"| `{f}` | {m['bytes']} | `{m['sha256']}` |")
(A/'CHANGELOG.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('All eight final commands passed; exact patch and manifest saved.')
