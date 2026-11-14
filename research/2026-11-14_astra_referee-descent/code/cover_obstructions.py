from check import *
from induction import contract,good,classify
from covers import cover_pairs
import gzip,collections
out={};seen=set()
for filename in ('exceptions_6_13.jsonl','exceptions_14_17.jsonl.gz','exceptions_18.jsonl.gz'):
 p=REPO/'research/2026-11-14_fable_induction-completion/data'/filename;op=gzip.open if p.suffix=='.gz' else open
 with op(p,'rt') as handle:
  for line in handle:
   d=json.loads(line);v=d['V'];R=d['t0'];x,p,q=d['x'],d['v1'],d['v2'];key=(v,d['gid'],tuple(R),x,tuple(sorted((p,q))))
   if key in seen:continue
   seen.add(key);A=[tuple(f) for f in d['blacks'] if set(f)!=set(R)];B,root,_=contract(A,R,x,p,q);pairs=cover_pairs(B,root);groups=collections.defaultdict(list);classes={}
   for rr,ss in pairs:
    if not good(B,root,ss):continue
    if ss not in classes:classes[ss]=classify(A,R,x,p,q,ss)[0]
    groups[info(B,(rr,ss))[0]].append(classes[ss])
   row=out.setdefault(v,dict(contractions=0,exceptions=0,exception_covers=0,all_exception_covers=0,per_cover_half_fail=0,global_half_fail=0));e=sum(c=='E' for c in classes.values());row['contractions']+=1;row['exceptions']+=e;row['global_half_fail']+=2*e>len(classes)
   for cs in groups.values():
    if 'E' not in cs:continue
    e=cs.count('E');row['exception_covers']+=1;row['all_exception_covers']+=e==len(cs);row['per_cover_half_fail']+=2*e>len(cs)
print(json.dumps(out,indent=2));(BASE/'code/cover_obstructions.json').write_text(json.dumps(out,indent=2))
