from pathlib import Path
import subprocess,json
D=Path('E:/Personal/Math/mathathon/barnette-s-conjecture/research/2026-11-14_astra_lean-check');P=Path('E:/lb2')
m=json.loads((P/'lake-manifest.json').read_text()); rows=[]
for entry in m['packages']:
 name=entry['name'];p=P/'.lake/packages'/name
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=p,text=True).strip()
 dirty=subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=p,text=True).strip()
 rows.append({'package':name,'expected':entry.get('rev'),'actual':head,'tracked_diff':dirty})
 assert head==entry['rev'] and not dirty
(D/'cache-integrity.json').write_text(json.dumps(rows,indent=2)+'\n')
print('All',len(rows),'dependency Git heads match the manifest; no tracked source differences from HEAD.')
