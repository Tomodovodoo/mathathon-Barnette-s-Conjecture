"""Exhaustive small rooted tests; independent primal matching-complement cycle enumeration."""
import sys,json,time,itertools,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'workings/barnette_lab'))
import networkx as nx
from barnette_lab.core import Instance,plantri_graphs,edge,faces_of
from barnette_lab.algorithms import separators,solve
OUT=Path(__file__).resolve().parents[1]
def save(name,obj): (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
def event(s):
 with (OUT/'events.jsonl').open('a') as f:f.write(json.dumps({'time':time.time(),'event':'computed','summary':s,'review':'under-review'})+'\n')
def matchings(g,remaining=None):
 remaining=set(g) if remaining is None else remaining
 if not remaining:yield [];return
 u=min(remaining)
 for v in sorted(set(g[u])&remaining):
  for m in matchings(g,remaining-{u,v}):yield [edge(u,v)]+m
 def unused():pass
def cycles(g):
 result=[]
 for m in matchings(g):
  h=g.copy();h.remove_edges_from(m)
  if nx.is_connected(h):result.append(frozenset(edge(*e) for e in h.edges()))
 return result
def path(g,a,b):
 full=(1<<len(g))-1
 def visit(u,mask):
  if u==b:return mask==full
  for v in g[u]:
   if not mask>>v&1 and visit(v,mask|1<<v):return True
  return False
 return visit(a,1<<a)
def strengthen(g,cs):
 es=sorted(edge(*e) for e in g.edges())
 both=[[list(e),list(f)] for e in es for f in es if e!=f and not any(e in c and f not in c for c in cs)]
 p4=[]
 for a,b in g.edges():
  for x in set(g[a])-{b}:
   for y in set(g[b])-{a,x}:
    p=[x,a,b,y]
    if not any({edge(x,a),edge(a,b),edge(b,y)}<=c for c in cs):p4.append(p)
 col=nx.bipartite.color(g)
 badpaths=[[a,b] for a in g for b in g if a<b and col[a]!=col[b] and not path(g,a,b)]
 return {'hamiltonian_cycles':len(cs),'include_avoid_failures':both,'p4_failures':p4,'opposite_endpoint_failures':badpaths}
def main(maxn):
 rows=[];summary=[]
 exe=ROOT/'workings/barnette_lab/vendor/plantri.exe'
 for n in range(6,maxn+1):
  ts=list(plantri_graphs(n,exe));print('size',n,'graphs',len(ts),flush=True)
  for j,t in enumerate(ts):
   name=f't{n}_{j}';base=Instance(t);cs=cycles(base.G)
   save(f'examples/{name}.json',{'dual_edges':sorted(map(list,t.edges())),'primal_edges':sorted(map(list,base.G.edges())),'faces':base.faces})
   st=strengthen(base.G,cs);st.update(name=name,dual_vertices=n);summary.append(st)
   for outer in range(len(base.faces)):
    b=Instance(t,outer);ss=list(b.states());ps=b.pairs(ss);trees=[s for s in ss if b.is_tree(s)];sep=separators(b)
    assert bool(ps)==(not any(x[2] for x in sep))
    rr={'name':name,'outer':outer,'black':b.black,'states':len(ss),'pairs':len(ps),'trees':len(trees),'separators':[[list(x[0]),x[2]] for x in sep],'edges':[]}
    for e in itertools.combinations(b.faces[outer],2):
     cert=solve(b,e)
     c=frozenset(edge(a,z) for a,z in zip(cert['cycle'],cert['cycle'][1:]+cert['cycle'][:1]))
     assert c in cs and b.dual_edges[edge(*e)] not in c
     ims=collections.Counter()
     for s in trees:
      cert=b.recover(s,e);cy=cert['cycle'];key=tuple(sorted(edge(a,z) for a,z in zip(cy,cy[1:]+cy[:1])))
      assert frozenset(key) in cs
      ims[key]+=1
     rr['edges'].append({'e0':e,'avoiding':sum(b.dual_edges[edge(*e)] not in c for c in cs),'image':len(ims),'multiplicities':sorted(ims.values())})
    rows.append(rr)
   save('data/roots.json',rows);save('data/strengthenings.json',summary)
   event(f'{name}: all roots and prescriptions checked; {len(cs)} Hamiltonian cycles')
 print('done',len(summary),'graphs',len(rows),'roots',flush=True)
if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else 12)
