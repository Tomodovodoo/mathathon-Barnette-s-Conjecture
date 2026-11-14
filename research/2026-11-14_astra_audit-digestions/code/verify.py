import sys,json,re,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parents[1]/'outputs'
sys.path.insert(0,str(ROOT/'workings/barnette_lab'))
import networkx as nx
from barnette_lab import Instance
from barnette_lab.li import LiMultiObjects

def instance(faces,outer):
 g=nx.Graph()
 for f in faces:g.add_edges_from(zip(f,f[1:]+f[:1]))
 p=Instance(g)
 return Instance(g,next(i for i,f in enumerate(p.faces) if set(f)==set(faces[outer])))

def matchings(g):
 if not g:return [set()]
 v=min(g)
 out=[]
 for w in g[v]:
  h=g.copy();h.remove_nodes_from([v,w])
  out.extend(m|{tuple(sorted((v,w)))} for m in matchings(h))
 return out

results={}
for name in ['octahedron','prism','running']:
 if name=='prism':
  faces=[f for i in range(6) for f in [[6,i,(i+1)%6],[7,(i+1)%6,i]]];outer=0
 else:
  d=json.loads((ROOT/f'paper/figures/{name}.json').read_text());faces=d['faces'];outer=d['t0']
 b=instance(faces,outer);ss=list(b.states());ps=b.pairs(ss)
 hist=Counter()
 for m in matchings(b.G):
  h=b.G.copy();h.remove_edges_from(m);hist[nx.number_connected_components(h)]+=1
 for r,s in ps:
  assert b.sign(r,s)==(-1)**((b.n+b.J(r,s))//2)
  for c in b.qcycles(s):
   q=b.reverse_q((r,s),c);assert b.sign(*q)==-b.sign(r,s)
  for c in b.dcycles(r,s):
   q=b.reverse_d((r,s),c);assert b.sign(*q)==-b.sign(r,s)
 results[name]={'states':len(ss),'pairs':len(ps),'trees':sum(b.is_tree(s) for s in ss),'two_factor_cycles':dict(hist),'polynomial':b.polynomial(ps)}
 if name=='running':
  li=LiMultiObjects(b);objs=list(li.objects(ps));universe=set(objs)
  fixes=[]
  for inv in [li.iota1,li.iota2]:
   fs=[]
   for o in objs:
    q=inv(o);assert q in universe and inv(q)==o
    if q==o:fs.append(o)
    else:assert li.sign(q)!=li.sign(o)
   fixes.append(fs)
  results[name]['li']={'objects':len(objs),'signed_sum':sum((-1)**li.sign(o) for o in objs),'fixed_counts':list(map(len,fixes)),'fixed_sign_counts':[dict(Counter(li.sign(o) for o in fs)) for fs in fixes],'fixed_points':fixes,'lab_faces':b.faces,'lab_A':b.A,'source_face_ids':{str(i):next(j for j,f in enumerate(faces) if set(f)==set(b.faces[i])) for i in range(len(b.faces))}}
(OUT/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf8')
print(json.dumps({k:{a:v for a,v in x.items() if a!='li'} for k,x in results.items()},indent=2))
print('Li:',{k:v for k,v in results['running']['li'].items() if k not in ['fixed_points','lab_faces','lab_A','source_face_ids']})
links=[]
for p in (ROOT/'digestions/steps').glob('*.md'):
 for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf8')):
  if not target.startswith(('http','#')) and not (p.parent/target.split('#')[0]).exists():links.append([str(p.relative_to(ROOT)),target])
(OUT/'links.json').write_text(json.dumps(links,indent=2));print('Broken links:',links)
