from pathlib import Path
import json,itertools,collections,math
R=Path.cwd(); D=R/'research/2026-11-14_astra_lean-check'
def topology(faces):
 edges=collections.defaultdict(list)
 for t,f in enumerate(faces):
  for i in range(3): edges[tuple(sorted((f[i],f[(i+1)%3])))].append(t)
 assert all(len(v)==2 for v in edges.values())
 color={0:0}; todo=[0]
 for t in todo:
  for e,ts in edges.items():
   if t not in ts: continue
   u=ts[0] if ts[1]==t else ts[1]
   if u in color: assert color[u]!=color[t]
   else: color[u]=1-color[t];todo.append(u)
 return edges,color

def states_for(faces,color,root):
 black=[i for i in range(len(faces)) if color[i]==color[root] and i!=root]
 roots=set(faces[root]); states=[]
 def rec(s,used):
  if len(s)==len(black): states.append(tuple(s)); return
  for v in faces[black[len(s)]]:
   if v not in used and v not in roots: rec(s+[v],used|{v})
 rec([],set()); return black,states

def good(faces,black,s):
 parent={v:v for f in faces for v in f}
 def find(v):
  while parent[v]!=v: v=parent[v]
  return v
 for t,v in zip(black,s):
  a,b=[x for x in faces[t] if x!=v]; a,b=find(a),find(b)
  if a==b:return False
  parent[a]=b
 roots=set(parent)-set(s)
 return len({find(v) for v in roots})==len(roots) and {find(v) for v in roots}=={find(v) for v in parent}

def delta(f,a,b): return 1 if (f.index(b)-f.index(a))%3==1 else -1

def pair_checks(faces):
 edges,color=topology(faces); count=0; examples=[]
 for root in range(len(faces)):
  black,states=states_for(faces,color,root); n=len(black); counts=set()
  for r in states:
   for s in states:
    if any(a==b for a,b in zip(r,s)): continue
    ds=[delta(faces[t],a,b) for t,a,b in zip(black,r,s)]
    total=sum(ds); eps=math.prod(ds); assert total%3==0
    ipow=lambda k: (1,1j,-1,-1j)[k%4]
    assert eps==ipow(n)*ipow(total//3)
    assert eps==ipow(-n)*ipow(-total//3)
    nxt=[r.index(v) for v in s]; unseen=set(range(n)); cycles=[]
    while unseen:
     j=min(unseen);cy=[]
     while j in unseen: unseen.remove(j);cy.append(j);j=nxt[j]
     assert sum(ds[j] for j in cy) in (-3,3);cycles.append(cy)
    c=len(cycles); plus=sum(sum(ds[j] for j in cy)==-3 for cy in cycles)
    assert (n+c)%2==0 and eps==(-1)**((n+c)//2+plus)
    counts.add(c);count+=1
  examples.append({'root':root,'states':len(states),'good':sum(good(faces,black,s) for s in states),'cycle_counts':sorted(counts)})
 return {'pairs_checked':count,'roots':examples}

running=json.loads((R/'paper/figures/running.json').read_text())['faces']
prism=[(6,i,(i+1)%6) for i in range(6)]+[(7,(i+1)%6,i) for i in range(6)]
results={'running':pair_checks(running),'hexagonal_bipyramid':pair_checks(prism)}
edges,color=topology(prism); root=0; e0=(0,1); mandatory=edges[e0]; matchings=[]
adj={i:[] for i in range(len(prism))}
for e,(a,b) in edges.items():adj[a].append((b,e));adj[b].append((a,e))
def rec(unused,chosen):
 if not unused:matchings.append(chosen);return
 a=min(unused)
 for b,e in adj[a]:
  if b in unused:rec(unused-{a,b},chosen+[e])
rec(set(range(12))-set(mandatory),[e0])
black,states=states_for(prism,color,root); hcs=[]
for matching in matchings:
 seen={0};todo=[0]
 for a in todo:
  for b,e in adj[a]:
   if e not in matching and b not in seen:seen.add(b);todo.append(b)
 if len(seen)!=12:continue
 # Orient selection minus e0 towards its three roots and read black-face tail.
 seladj=collections.defaultdict(list)
 for a,b in matching:
  if (a,b)!=e0:seladj[a].append(b);seladj[b].append(a)
 parent={v:None for v in prism[root]}; queue=list(parent)
 for a in queue:
  for b in seladj[a]:
   if b not in parent:parent[b]=a;queue.append(b)
 assert len(parent)==8
 s=[]
 for t in black:
  e=next(e for e in matching if t in edges[e]);a,b=e
  s.append(a if parent[a]==b else b)
 assert tuple(s) in states
 hcs.append({'matching':matching,'recovered_state':s,'good':good(prism,black,s)})
results['T5_counterexample']={'root':prism[root],'prescribed_side':e0,'states':states,'good_states':[s for s in states if good(prism,black,s)],'hamiltonian_cycles':hcs}
assert len(states)==3 and len(results['T5_counterexample']['good_states'])==2 and len(hcs)==4
# Exhaustive local sign words, without graph assumptions beyond 3 | sum.
words=0
for n in range(19):
 for bits in range(1<<n):
  neg=bits.bit_count();total=n-2*neg
  if total%3:continue
  assert (-1)**neg==(1,1j,-1,-1j)[(n+total//3)%4]
  words+=1
results['signed_words']={'lengths':'0..18','admissible_words':words}
(D/'numerical.json').write_text(json.dumps(results,indent=2)+'\n')
print('Pairs:',{k:results[k]['pairs_checked'] for k in ('running','hexagonal_bipyramid')})
print('T5: 3 states, 2 good states, 4 eligible Hamiltonian cycles; good flags:',[h['good'] for h in hcs])
print('Sign words:',words)

