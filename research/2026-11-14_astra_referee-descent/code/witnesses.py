from check import *
import re
out=[]
for line in (REPO/'research/2026-11-14_fable_descent/data/witnesses.txt').read_text().splitlines():
 fields=line.split(' | '); head=fields[0]
 if len(fields)<3 or not fields[-1].startswith('pair '):out.append(dict(header=head,error='truncated certificate'));continue
 rot=parse(fields[1]); fs,col=faces(rot); root=tuple(map(int,re.search(r't0=(\d+,\d+,\d+)',head)[1].split(',')))
 ri=next(i for i,f in enumerate(fs) if set(f)==set(root)); A=[f for i,f in enumerate(fs) if col[i]==col[ri] and i!=ri]
 pairs=[tuple(map(int,s.split('>'))) for s in fields[-1][5:].split()]
 if len(fields)==4:A=[tuple(map(int,s.split(','))) for s in fields[2][6:].split()]
 else:A=[next(f for f in A if a in f and b in f) for a,b in pairs]
 p=tuple(zip(*pairs)); assert len(set(p[0]))==len(A)==len(set(p[1])); assert all(set(ab)<=set(f) for ab,f in zip(pairs,A))
 k=len(info(A,p)[1]);seen={p};front=[p];radius=None;sizes=[]
 for depth in range(1,6):
  nxt=[]
  for z in front:
   for w in moves(A,z):
    if w not in seen:seen.add(w);nxt.append(w)
  sizes.append(len(nxt))
  if any(len(info(A,w)[1])<k for w in nxt):radius=depth;break
  front=nxt
 out.append(dict(header=head,k=k,c=len(info(A,p)[2]),radius_k=radius,layer_sizes=sizes))
print(json.dumps(out,indent=2));(BASE/'code/witnesses.json').write_text(json.dumps(out,indent=2))
