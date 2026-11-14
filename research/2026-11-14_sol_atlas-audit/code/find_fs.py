from independent import *
import subprocess
# Find a small example where the relaxed colour condition excludes a partition.
def partitions_fast(g):
 vs=sorted(g);n=len(vs);adj=[sum(1<<vs.index(v) for v in g[u]) for u in vs];allm=(1<<n)-1
 def tree(mask):
  if not mask:return False
  if sum((adj[i]&mask).bit_count() for i in range(n) if mask>>i&1)!=2*(mask.bit_count()-1):return False
  reached=mask&-mask;front=reached
  while front:
   more=0
   while front:
    b=front&-front;front-=b;more|=adj[b.bit_length()-1]
   front=more&mask&~reached;reached|=front
  return reached==mask
 for mask in range(1,1<<(n-1)):
  if tree(mask) and tree(allm^mask):yield ({vs[i] for i in range(n) if mask>>i&1},{vs[i] for i in range(n) if not mask>>i&1})
found=None
for n in range(6,17):
 run=subprocess.run([str(R/'workings/barnette_lab/vendor/plantri.exe'),'-ba',str(n)],capture_output=True,text=True,check=True)
 for gi,line in enumerate(run.stdout.splitlines()):
  _,s=line.split();g=nx.Graph([(i,ord(c)-97) for i,ns in enumerate(s.split(',')) for c in ns]);col=nx.greedy_color(g,strategy='DSATUR');ps=list(partitions_fast(g))
  for c in range(3):
   ok=[p for p in ps if any(not any(col[u]!=c and col[v]!=c for u,v in g.subgraph(U).edges()) for U in p)]
   if 0<len(ok)<len(ps):found=dict(n=n,index=gi,edges=list(g.edges()),colour=col,B=c,total=len(ps),qualifying=len(ok),accept=[sorted(U) for U in ok[0]],reject=[sorted(U) for U in next(p for p in ps if p not in ok)]);break
  if found:break
 if found:break
assert found
(O/'fs-witness.json').write_text(json.dumps(found,indent=2));print('FS witness',found['n'],found['total'],found['qualifying'])
