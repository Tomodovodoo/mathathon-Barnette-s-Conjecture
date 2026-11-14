from check import *
import hashlib
sources=[]
for d in ['2026-11-14_fable_descent','2026-11-14_astra_induction-lemmas','2026-11-14_fable_induction-completion']:
 for p in (REPO/'research'/d).rglob('*'):
  if p.suffix in ('.md','.py','.cpp','.json','.txt'):
   sources.append(dict(path=str(p.relative_to(REPO)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(BASE/'code/source-manifest.json').write_text(json.dumps(sources,indent=2))
