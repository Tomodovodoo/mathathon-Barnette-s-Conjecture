from pathlib import Path
import json
for f in ['labyrinth/seed.py','research/2026-11-14_astra_audit-digestions/code/finalize.py']:
 p=Path(f);s=p.read_text(encoding='utf8').replace('"date": DAY, "result": old_row["result"]','"date": DAY, "was": old_row["result"]').replace("'date':'2026-11-14','result':q['result']","'date':'2026-11-14','was':q['result']");p.write_text(s,encoding='utf8')
p=Path('labyrinth/sota.json');d=json.loads(p.read_text())
for r in d['entries']:
 for h in r.get('previous',[]):
  if 'result' in h:h['was']=h.pop('result')
p.write_text(json.dumps(d,indent=1),encoding='utf8')
