from potentials import *
root=REPO/'research/2026-11-14_fable_descent/data';candidates={};missing={}
files=sorted(root.glob('census_*.txt'))+sorted(root.glob('exhaustive_random_*.txt'))
for fn in files:
 for line in fn.read_text().splitlines():
  if not line.startswith('W ') or 'pot=' not in line or 'SIGNED' in line:continue
  name=re.search(r'pot=([^ ]+)',line)[1]
  if name=='k':continue
  if ' | pair ' not in line:missing.setdefault(name,[]).append(fn.name);continue
  V=int(re.search(r'V=(\d+)',line)[1]);kind=line.split()[1]
  key=(name,kind)
  if key not in candidates or V<candidates[key][0]:candidates[key]=(V,line,fn.name)
out=[]
for key,(v,line,fn) in sorted(candidates.items()):
 r=run(line);r['source']=fn;out.append(r);print(r,flush=True)
 (BASE/'code/all_potentials.json').write_text(json.dumps(dict(checked=out,truncated=missing),indent=2))
